from __future__ import division
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pyqtgraph.exporters
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse import vstack
#from scipy.misc import toimage
from scipy.interpolate import griddata
from PIL.ImageQt import ImageQt
from multiprocessing import Pool
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
#import qimage2ndarray
import tempfile
import shutil
import subprocess, os
import zipfile
from zipfile import ZipFile
import json
from util.icons import Icon
import sys

IMPORT_LOCATION = "/apps/importfile/bin/importfile"

PART_BUTTON = "part button"
FILM_BUTTON = "film button"

filelist=[]

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.mkPen('k')

QW=QtWidgets
QC=QtCore
QG=QtGui

class Main(QW.QMainWindow):
    """
    Main window containing the widget. Adds menu bar / tool bar functionality.
    """
    def __init__(self,mode='local', repo_dir = '', *args,**kwargs):
        super(Main,self).__init__(*args,**kwargs)

        self.mode = mode
        self.repo_dir = repo_dir
        self.mainWidget = NDRaman(mode=mode)
        self.setCentralWidget(self.mainWidget)

        # building main menu
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)

        importAction = QG.QAction("&Import",self)
        importAction.setIcon(Icon('download.svg'))
        importAction.triggered.connect(self.mainWidget.openFileName)

        # exportAction = QG.QAction("&Export",self)
        # exportAction.setIcon(Icon('upload.svg'))
        # exportAction.triggered.connect(self.mainWidget.exportTrigger)

        # clearAction = QG.QAction("&Clear",self)
        # clearAction.setIcon(Icon('trash.svg'))
        # clearAction.triggered.connect(lambda _: self.mainWidget.clear())

        exitAction = QG.QAction("&Exit",self)
        exitAction.setIcon(Icon('log-out.svg'))
        exitAction.triggered.connect(self.close)
        
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(importAction)
        # fileMenu.addAction(exportAction)
        # fileMenu.addAction(clearAction)
        if mode == 'local':
            fileMenu.addAction(exitAction)

        aboutAction = QG.QAction("&About",self)
        aboutAction.setIcon(Icon('info.svg'))
        aboutAction.triggered.connect(self.showAboutDialog)

        testImageAction = QG.QAction("&Import Test Spectrum",self)
        testImageAction.setIcon(Icon('image.svg'))
        testImageAction.triggered.connect(self.importTestSpectrum)

        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(testImageAction)
        helpMenu.addAction(aboutAction)

        self.show()

    def showAboutDialog(self):
        about_dialog = QW.QMessageBox(self)
        about_dialog.setText("About This Tool")
        about_dialog.setWindowModality(QC.Qt.WindowModal)
        copyright_path = os.path.join(self.repo_dir,'COPYRIGHT')
        print(f"okay:{copyright_path}")
        if os.path.isfile(copyright_path):
            with open(copyright_path,'r') as f:
                copyright = f.read()
                print(f"hey:{copyright}")
        else:
            copyright = ""

        version_path =  os.path.join(self.repo_dir,'VERSION')
        if os.path.isfile(version_path):
            with open(os.path.join(self.repo_dir,'VERSION'),'r') as f:
                version = f.read()
        else:
            version = ""

        about_text = "Version: %s \n\n"%version
        about_text += copyright

        about_dialog.setInformativeText(about_text)
        about_dialog.exec()

    def importTestSpectrum(self):
        path = os.path.join(self.repo_dir,'data','raw','test_spec.txt')
        filelist.append(path)
        self.mainWidget.filmfitbut.setEnabled(True)
        self.mainWidget.partfitbut.setEnabled(True)

class NDRaman(QtWidgets.QWidget):
    def __init__(self, mode='local',parent=None):
        super(NDRaman,self).__init__(parent=parent)
        self.singleSpect=SingleSpect()
        self.resize(1440,600)
        self.spect_type=''
        self.data=[]
        self.mode=mode

        self.layout=QtWidgets.QGridLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.displayWidget=QtWidgets.QStackedWidget()
        self.displayWidget.addWidget(self.singleSpect)
        self.layout.addWidget(self.displayWidget,2,0,1,3)

        self.flbut=QtWidgets.QPushButton('Upload File')
        self.flbut.setToolTip("Please upload a .txt or .csv file")
        self.flbut.clicked.connect(self.openFileName)
        self.flbut.setMinimumSize(220,50)
        self.layout.addWidget(self.flbut,0,0)

        self.partfitbut=QtWidgets.QPushButton('Do Particle Fitting')
        self.partfitbut.clicked.connect(lambda: self.doFitting(PART_BUTTON))
        self.partfitbut.setCheckable(True)
        self.partfitbut.setEnabled(False)
        self.partfitbut.setMinimumSize(220,50)
        self.layout.addWidget(self.partfitbut,0,1)
    
        self.filmfitbut=QtWidgets.QPushButton('Do Film Fitting')
        self.filmfitbut.clicked.connect(lambda: self.doFitting(FILM_BUTTON))
        self.filmfitbut.setCheckable(True)
        self.filmfitbut.setEnabled(False)
        self.filmfitbut.setMinimumSize(220,50)
        self.layout.addWidget(self.filmfitbut,1,1)

        self.download_but=QtWidgets.QPushButton('Download Data')
        self.download_but.clicked.connect(self.downloadData)
        self.download_but.setFixedSize(500,50)
        self.download_but.setEnabled(False)
        self.download_list=[]

        self.statusBar=QtWidgets.QProgressBar()
        self.statusBar.setMinimumHeight(50)
        self.layout.addWidget(self.statusBar,0,2)

        self.errmsg=QtWidgets.QMessageBox()
        self.downloadMsg=QtWidgets.QMessageBox()
        self.cnfmdnld=False

        self.pathmade=False

    def openFileName(self):
        if self.mode == 'local':
            try:
                fpath = QtGui.QFileDialog.getOpenFileName()
                if isinstance(fpath,tuple):
                   fpath = fpath[0]
            except Exception as e:
                print(e)
        elif self.mode == 'nanohub':
            try:
                fpath = subprocess.check_output(IMPORT_LOCATION,shell=True).strip().decode("utf-8")
            except Exception as e:
                print(e)

        filelist.append(fpath)
        if filelist[-1]!=u'':
            if filelist[-1][-3:]!='txt' and filelist[-1][-3:]!='csv':
                self.errmsg.setIcon(QtWidgets.QMessageBox.Critical)
                self.errmsg.setText('Please upload a .txt or .csv')
                self.errmsg.exec_()

                del filelist[-1]
            else:
                self.partfitbut.setEnabled(True)
                self.filmfitbut.setEnabled(True)
        else:
            del filelist[-1]

        self.f_list=filelist

    def checkFileType(self, flnm):
        if flnm[-3:]=='csv':
            self.data=pd.read_csv(flnm)
        else:
            self.data=pd.read_table(flnm)

        cols=self.data.shape[1]
        rows=self.data.shape[0]
        if cols == 1:
            self.data=pd.DataFrame(self.data.iloc[0:rows/2,0],self.data.iloc[rows/2:rows,0])
            self.spect_type='single'
        elif cols == 2:
            self.spect_type='single'
            if type(self.data.iloc[0,0]) is str:
                self.data=self.data.iloc[1:rows,:]
            else:
                self.data=self.data
        else:
            self.spect_type='map'
            self.errmsg.setIcon(QtWidgets.QMessageBox.Critical)
            self.errmsg.setText('Please upload a single spectrum')
            self.errmsg.exec_()

    def doFitting(self, button):
        if not self.pathmade:
                self.make_temp_dir()
        map_i=1
        sing_i=1
        for flnm in filelist:
            self.checkFileType(flnm)
            if self.spect_type=='single':

                self.newpath=str(self.dirpath)+'/SingleSpect'+str(sing_i)
                if not os.path.exists(self.newpath):
                    os.makedirs(self.newpath)
                    sing_i+=1
                shutil.copy2(flnm,self.newpath)

                self.widget=self.singleSpect
                self.displayWidget.setCurrentWidget(self.widget)

                x=np.array(self.data.iloc[:,0])
                y=np.array(self.data.iloc[:,1])

                self.widget.plotSpect(x,y, button)
                self.filmfitbut.setEnabled(False)
                self.partfitbut.setEnabled(False)
                self.download_but.setEnabled(True)
            # else:

            #     throw error message
    def make_temp_dir(self):
        self.dirpath = tempfile.mkdtemp()
        self.pathmade=True

    def downloadData(self):
        self.downloadMsg.setIcon(QtWidgets.QMessageBox.Question)
        self.downloadMsg.setWindowTitle('Confirm Download')
        self.downloadMsg.setText('The Raman spectrum(s) following files will be downloaded:\n'+'\n'.join('{}'.format(item[0]) for item in self.f_list))
        self.downloadMsg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        # self.downloadMsg.buttonClicked.connect(self.msgbtn)
        self.downloadMsg.exec_()


class SingleSpect(QtWidgets.QWidget): 
    def __init__(self, parent=None):
        super(SingleSpect,self).__init__(parent=parent)
        self.layout=QtWidgets.QGridLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

    def Single_Lorentz(self, x,a,w,b):
        return a*(((w/2)**2)/(((x-b)**2)+((w/2)**2)))

    def backgroundFit(self,x,y):
        I_raw=y
        W=x

        polyx=np.array([W[0],W[int(len(W)/2)],W[len(W)-1]])
        polyy=np.array([I_raw[0],I_raw[int(len(W)/2)],I_raw[len(W)-1]])        
        bkgfit=np.polyfit(polyx,polyy,2)
        bkgpoly=(bkgfit[0]*W**2)+(bkgfit[1]*W)+bkgfit[2]
        I_raw=I_raw-bkgpoly
    
        m=(I_raw[len(W)-1]-I_raw[0])/(W[len(W)-1]-W[0])
        b=I_raw[len(W)-1]-m*W[len(W)-1]
        bkglin=m*W+b
    
        I_raw=I_raw-bkglin
    
        I=((I_raw-np.min(I_raw))/np.max(I_raw-np.min(I_raw)));
        return I

    def fitToPlot(self,x,y, button):
        I=self.backgroundFit(x,y)
        pG=[0.5*np.max(I), 65, 1602] #a w b
        pDiam=[np.max(I), 6, 1332]
        pD=[0.7*np.max(I),65,1347]
        
        #fit Diamond peak
        Diam_param,Diam_cov=curve_fit(self.Single_Lorentz,x,y,bounds=([0.3*np.max(I),0,1300],[1*np.max(I),10,1340]), p0=pDiam)
        Diam_fit=self.Single_Lorentz(x,Diam_param[0],Diam_param[1],Diam_param[2])

        #fit G peak
        G_param,G_cov=curve_fit(self.Single_Lorentz,x,y,bounds=([.3*np.max(I),30,1500],[1*np.max(I),70,1800]),p0=pG)
        G_fit=self.Single_Lorentz(x,G_param[0],G_param[1],G_param[2])


        #fit D peak
        D_param,D_cov=curve_fit(self.Single_Lorentz,x,y,bounds=([.3*np.max(I),40,1340],[1*np.max(I),80,1470]),p0=pD)
        D_fit=self.Single_Lorentz(x,D_param[0],D_param[1],D_param[2])

        param_dict={'G':{'a':G_param[0],'w':G_param[1],'b':G_param[2]},'Diam_param':{'a':Diam_param[0],'w':Diam_param[1],'b':Diam_param[2]},'D':{'a':D_param[0],'w':D_param[1],'b':D_param[2]}}

        y_fit=Diam_fit+G_fit+D_fit 
        

        self.fit_plot=pg.plot(x,y_fit,pen='k')
        self.fit_plot.setMenuEnabled(False)
        self.fit_plot.setRange(yRange=[0,1])
        self.fit_plot.setLabel('left','I<sub>norm</sub>[arb]')
        self.fit_plot.setLabel('bottom',u'\u03c9'+'[cm<sup>-1</sup>]')
        self.fit_plot.win.hide()

        self.overlay_plot=pg.plot()
        self.overlay_plot.addLegend(offset=(-1,1))
        self.overlay_plot.plot(x,y,pen='g',name='Raw Data')
        self.overlay_plot.plot(x,y_fit,pen='r',name='Fitted Data')
        self.overlay_plot.setMenuEnabled(False)
        self.overlay_plot.setLabel('left','I<sub>norm</sub>[arb]')
        self.overlay_plot.setLabel('bottom',u'\u03c9'+'[cm<sup>-1</sup>]')
        self.overlay_plot.win.hide()
        exporter2=pg.exporters.ImageExporter(self.overlay_plot.plotItem)
        exporter2.params.param('width').setValue(1024, blockSignal=exporter2.widthChanged)
        exporter2.params.param('height').setValue(860, blockSignal=exporter2.heightChanged)
        if button == PART_BUTTON:
            self.fitting_params=QtWidgets.QLabel(
            """Fitting Parameters:
                Diamond Peak:
                    """u'\u03b1'"""="""+str(round(Diam_param[0],4))+"""
                    """u'\u0393'"""="""+str(round(Diam_param[1],4))+"""
                    """u'\u03c9'"""="""+str(round(Diam_param[2],4))+"""
                G Peak:
                    """u'\u03b1'"""="""+str(round(G_param[0],4))+"""
                    """u'\u0393'"""="""+str(round(G_param[1],4))+"""
                    """u'\u03c9'"""="""+str(round(G_param[2],4))+"""
                D Peak:
                    """u'\u03b1'"""="""+str(round(D_param[0],4))+"""
                    """u'\u0393'"""="""+str(round(D_param[1],4))+"""
                    """u'\u03c9'"""="""+str(round(D_param[2],4))+"""  
                Int(D)/Int(G) = """+str(round((D_param[0]/G_param[0]),4))+"""
                """
                #"""
                #Particle Size:
                #"""     
            )
        elif button == FILM_BUTTON:
            self.fitting_params=QtWidgets.QLabel(
            """Fitting Parameters:
            Diamond Peak:
                """u'\u03b1'"""="""+str(round(Diam_param[0],4))+"""
                """u'\u0393'"""="""+str(round(Diam_param[1],4))+"""
                """u'\u03c9'"""="""+str(round(Diam_param[2],4))+"""
            G Peak:
                """u'\u03b1'"""="""+str(round(G_param[0],4))+"""
                """u'\u0393'"""="""+str(round(G_param[1],4))+"""
                """u'\u03c9'"""="""+str(round(G_param[2],4))+"""
            D Peak:
                """u'\u03b1'"""="""+str(round(D_param[0],4))+"""
                """u'\u0393'"""="""+str(round(D_param[1],4))+"""
                """u'\u03c9'"""="""+str(round(D_param[2],4))+"""  
Int(D)/Int(G) = """+str(round((D_param[0]/G_param[0]),4))+"""
Quality = """+'.'+str(round(100*(Diam_param[0]/(Diam_param[0]+(G_param[0]+D_param[0])/233))))+"""
"""u'\u03c3'"""(GPa) = """" """+str(round((-1.08)*(Diam_param[2]-1332),4))+"""
            """)
        else:
             raise ValueError("Bad button name")

        pal = self.fitting_params.palette()
        pal.setColor(self.fitting_params.backgroundRole(), Qt.white)
        self.fitting_params.setPalette(pal)
        self.fitting_params.setAutoFillBackground(True)
        self.fitting_params.setMinimumSize(340,500)
        self.layout.addWidget(self.fitting_params,2,2)

    def plotSpect(self,x,y, button):
        """
        Normalize
        """
        y_norm=[]
        for i in y:
            y_norm.append((i-np.min(y))/(np.max(y)-np.min(y)))

        self.spect_plot=pg.plot(x,y_norm,pen='k')
        self.spect_plot.setMenuEnabled(False)
        self.spect_plot.setMinimumSize(220,500)
        self.spect_plot.setLabel('left','I<sub>norm</sub>[arb]')
        self.spect_plot.setLabel('bottom',u'\u03c9'+'[cm<sup>-1</sup>]')
        self.spect_plot.win.hide()

        self.fitToPlot(x,y_norm, button)

        self.TabWidget=QtWidgets.QTabWidget()
        self.TabWidget.addTab(self.fit_plot,"Fit")
        self.TabWidget.addTab(self.overlay_plot,"Overlay")
        #self.TabWidget.addTab(self.diff_plot,"Diffs") commented out
        self.TabWidget.setMinimumSize(220,500)

        self.layout.addWidget(self.TabWidget,2,1)
        self.layout.addWidget(self.spect_plot,2,0)


def main():
    nargs = len(sys.argv)
    if nargs > 1:
        mode = sys.argv[1]
    else:
        mode = 'local'
    if mode not in ['nanohub','local']:
        mode = 'local'

    REPO_DIR = "."
    if mode == 'local':
        REPO_DIR = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
    else:
        if os.environ.get("RUN_LOCATION"):
            REPO_DIR = os.environ.get("RUN_LOCATION")
    print()
    app=QtWidgets.QApplication([])
    raman=Main(mode=mode, repo_dir=REPO_DIR)
    #raman.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

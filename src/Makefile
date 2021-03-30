
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))
DESTDIR := $(abspath $(current_dir)../bin)

all:
	@echo "Run 'make install'"

ndraman:
	cd .. && pip install --upgrade -t ${DESTDIR} .
	cp -p ../VERSION ${DESTDIR}
	cp -p -r ../src/ndraman/util/icons_catalogue ${DESTDIR}/ndraman/util
	cp -p ../LICENSE ${DESTDIR}

install:
	. /etc/environ.sh; use -e -r anaconda-6; $(MAKE) ndraman

clean:
	rm -rf ${DESTDIR}/*.dist-info

distclean: clean
	rm -rf ${DESTDIR}/*

.PHONY: all ndraman install clean distclean

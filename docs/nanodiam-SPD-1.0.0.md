# nanoMFG Software Planning Document
<!-- Replace text below with long title of project:short-name -->
## Tool for Raman of Nanodiamond: nanodiam
### Target Release: 1.0.0 : December 31, 2020

## Development Team
<!-- Complete table for all team members 
 roles: lead, developer, reviewer
 status: active, inactive
-->
Name | Role | github user | nanohub user | email | status
---|---|---|---|---|---
Lili Cai| Lead | lilicaiuiuc| |lilicai@illinois.edu| active
Adrian Manjarrez | Developer | adrianm3 | amanjarrez | adrianm3@illinois.edu | active
Darren Adams | Developer | dadamsncsa | Darren K Adams| dadams@illinois.edu | active
Aagam Shah | Developer | AagamShah97 | aagam2 | aagam2@illinois.edu | active
 |  |  |  |  | 

**nanoMFG Github Team(s):** @nanodiam-dev
**nanoHUB Group(s):**

## 1. Introduction
This tool will be used to analyze the Raman spectra of nanodiamonds.

### 1.1 Purpose and Vision Statement
<!-- Why are we building this tool?
What is the key benefit
How does it relate to existing tools and existing software?
How does it fit into the overall objectives for the nano **manufacturing** node?
Who will use this software?
-->
The key benefit of developing this tool will be to more efficiently analyze the Raman spectra of nanodiamonds, and it will be similar in concept to the Graphene Raman Fitting Tool. The primary users of this software will consist of researchers studying nanodiamond samples. Currently, there are no applications tailored to nanodiamond analysis, and with this application they will be able to gather/review data from the nanodiamond spectrum more quickly and efficiently. Furthermore, this tool will be included in a larger toolset that will be used for the analysis and synthesis of nanodiamond samples. The scope of this project will fit into the overall objectives of the nano manufacturing node by progressing nanodiamond research and analysis.  



### 1.2 References
<!--List any documents or background material that are relevant.  Links are useful. For instance, a link to a wiki or readme page in the project repository, or link to a uploaded file (doc, pdf, ppt, etc.).-->
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5635142/  
https://en.wikipedia.org/wiki/Raman_spectroscopy#Applications  
https://nanohub.org/resources/graft

## 2 Overview and Major Planned Features
<!--Provide and overview characterising this proposed release.  Describe how users will interact with each proposed feature. Include a schematic/diagram to illustrate an overview of proposed software and achitecture componets for the project-->
Users will be able to upload a nanodiamond Raman spectrum dataset in the form of .txt or .csv. The dataset will then be converted into interactive graphs and readable data similar to the graphene fitting tool. Additionally, the tool will also be able to calculate the the ratio of the diamond peak intensity to the "D" and "G" peak intensities, and the FWHM of the respective peaks, to determine diamond/non-diamond phase quanities and quality.

### 2.1 Product Background and Strategic Fit
<!--Provide context for the proposed product.  Is this a completely new projects, or next version of an existing project? This can include a description of any contextual research, or the status of any existing prototype application.  If this SPD describes a component, describe its relationship to larger system. Can include diagrams.-->
This project is a build-off of the exisitng Graphene Raman Fitting Tool. Many of the functions will be similar, such as the upload file function and the way in which the outputs are displayed.  Further, this Raman analysis tool will be a part of a larger toolset used to optomize the analysis and synthesis of nanodiamonds.

### 2.2 Scope and Limitations for Current Release
<!--List the all planned goals/features for this release.  These should be links to issues.  Add a new subsection for each release.  Equally important, document feature you explicity are not doing at this time-->
Goals:
Make sure inputs (data) lead to correct outputs (graphs)

##### 2.2.1 Planned Features
Features:  
Place mouse cursor on graph to see specific values  
Add function to type in a value in the x-axis to see its correspoding value in the y-axis, vice versa

#### 2.2.2 Release Notes
##### v#.#.#

### 2.3 Scope and Limitations for Subsequent Releases
<!--Short summary of  future envisioned roadmap for subsequent efforts.-->

### 2.3 Operating Environment
<!--Describe the target environment.  Identify components or application that are needed.  Describe technical infrastructure need to support the application.-->
The appliction will be operated on the nanoHub website. It will also be available for download for local use. 

### 2.4 Design and Implementation Constraints
<!--This could include pre-existing code that needs to be incorporated ,a certain programming language or toolkit and software dependencies.  Describe the origin and rationale for each constraint.-->
Code from the Graphene Raman Fitting Tool will be adjusted to fit the needs of the nanodiamond raman spectrum. This includes changing values and certain parts of the code. 


## 3 User Interaction and Design

### 3.1 Classes of Users
<!--Identify classes (types) of users that you anticipate will use the product.  Provide any relevant context about each class that may influence how the product is used: 
The tasks the class of users will perform
Access and privilege level
Features used
Experience level
Type of interaction
Provide links to any user surveys, questionnaires, interviews, feedback or other relevant information.-->
The intended users will be researchers who are utilizing nanodiamonds in their research for either growth or other nanodiamond applications.  
Users will upload .txt or .csv files to view the Raman spectrum and data. They will then be able to interact with the data and save it locally. 
Access to the application will be the same for everyone, and no experience level will be necessary to use the software. However, an understanding of the nanodiamond Raman spectrum will be required. 

### 3.2 User Requirements
<!-- Provide a list of issue links to document the main set of user requirements to be satisfied by this release.  Use the user requirement template to draft thense issues.  A well written user requirement should be easy to justify (Rational) and should be testable.  List in order of priority as must have, should have or nice to have for each use case. -->
Allow the user to upload .txt and .csv files  
Quickly the load Raman spectrum graph after "fitting" button is clicked  
Function to allow user to save data locally

### 3.3 Proposed User Interface
<!--Could include drawn mockups, screenshots of prototypes, comparison to existing software and other descriptions.-->
UI will be similar to that of the Graphene Raman Fitting Tool. There will be a button to upload or drag and drop files. Once uploaded, the output graphs/data will apear in small windows with the ability to save/print.  
Example of Outputs From the Graphene Raman Fitting Tool:
<img alt = "Graphene Raman Fitting Tool Output" src = "https://github.com/nanoMFG/nanodiam/blob/adrianm3-patch-1/docs/fitting.PNG">

### 3.4 Documentation Plan
<!-- List planned documentation activities -->

### 3.5 User Outreach Plan
<!-- List upcoming activities designed to elicit user feedback and/or engage new users.  Use issues for activities that will be completed this iteration-->
Initial outreach will begin with the lab members of Cai Research group to determine ease of use and functionality. Following the internal outreach and possible updates to the tool, external colleauges will be asked to sample the tool. Lastly, the tool could be included in future newsletters to reach a larger set of users. 

## 4. Data And Quality Attributes

### 4.1 Data Dictionary
<!--Summarize inputs and outputs for the application.-->
The input will be the a raman spectrum file. The outputs will be the graph of the spectrum and also corresponding values of sp2/sp3 peaks.  

### 4.2 Usability and Performance
<!--Summarize usability requirements such as easy of adoption for new users (eg example data),  inline documentation, avoiding errors, efficient interaction, etc.  Describe performance expectations  and/or document challenges.  Note you can reference user requirements from above if needed. -->
Example data will be provided so that the user can see what to expect from their own data. 


### 4.3 Testing, Verification and Validation
<!--Describe What data is necessary to verify the basic functionality of the application.  Provide a testing plan that includes a list of issues for each planned activity.  Describe data sets that are needed to test validation.-->
Data from different nanodiamond spectrums (from ones available online or personal data) will be used as inputs, and I will make sure the outputs match the data.

### 4.4 Uncertainty Quantification
<!--Identify and document possible sources of uncertainty. Categorize with standard labels, such as parametric, structural, algorithmic, experimental, interpolation.
Develop a plan for measuring and documenting uncertainty, e.g., using forward propagation or inverse UQ, and showing it in the application, if applicable.-->

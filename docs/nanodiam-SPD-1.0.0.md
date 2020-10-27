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
Adrian Manjarrez | developer | adrianm3 | amanjarrez | adrianm3@illinois.edu | active
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
The key benefit of developing this tool will be to more efficiently analyze the Raman spectra of nanodiamonds. It will be similar in concept to the Graphene Raman Fitting Tool, and primary users of this software will consist of researchers growning nanodiamond samples.



### 1.2 References
<!--List any documents or background material that are relevant.  Links are useful. For instance, a link to a wiki or readme page in the project repository, or link to a uploaded file (doc, pdf, ppt, etc.).-->
https://en.wikipedia.org/wiki/Raman_spectroscopy#Applications  
https://nanohub.org/resources/graft

## 2 Overview and Major Planned Features
<!--Provide and overview characterising this proposed release.  Describe how users will interact with each proposed feature. Include a schematic/diagram to illustrate an overview of proposed software and achitecture componets for the project-->
Users will be able to upload files and view graphs/data similar to the graphene fitting tool. 

### 2.1 Product Background and Strategic Fit
<!--Provide context for the proposed product.  Is this a completely new projects, or next version of an existing project? This can include a description of any contextual research, or the status of any existing prototype application.  If this SPD describes a component, describe its relationship to larger system. Can include diagrams.-->
This project is a build-off of the exisitng Graphene Raman Fitting Tool. Many of the functions will be similar. 

### 2.2 Scope and Limitations for Current Release
<!--List the all planned goals/features for this release.  These should be links to issues.  Add a new subsection for each release.  Equally important, document feature you explicity are not doing at this time-->
Goals:  
Successfuly upload it to nanohub  
make sure inputs lead to correct outputs

##### 2.2.1 Planned Features
Features:  
be able to place mouse cursor on graph to see specific values  
possilby type in a value in the x-axis to see its correspoding value in the y-axis, vice versa

#### 2.2.2 Release Notes
##### v#.#.#

### 2.3 Scope and Limitations for Subsequent Releases
<!--Short summary of  future envisioned roadmap for subsequent efforts.-->

### 2.3 Operating Environment
<!--Describe the target environment.  Identify components or application that are needed.  Describe technical infrastructure need to support the application.-->
The appliction will be operated on the nanohub website. I also plan to include a way to download the tool for local use.  

### 2.4 Design and Implementation Constraints
<!--This could include pre-existing code that needs to be incorporated ,a certain programming language or toolkit and software dependencies.  Describe the origin and rationale for each constraint.-->
Code from the Graphene Raman Fitting Tool will be adjusted to fit the needs of nanodiamond raman. This includes changing values and certain parts of the code. 


## 3 User Interaction and Design

### 3.1 Classes of Users
<!--Identify classes (types) of users that you anticipate will use the product.  Provide any relevant context about each class that may influence how the product is used: 
The tasks the class of users will perform
Access and privilege level
Features used
Experience level
Type of interaction
Provide links to any user surveys, questionnaires, interviews, feedback or other relevant information.-->
Anticipated users will be researchers who are working with nanodiamonds. This could include ND growth, ND applications, etc. Access to the application will be the same for everyone and no experience level will be necessary. Although, the user must be knowledgable about the Raman data. 
### 3.2 User Requirements
<!-- Provide a list of issue links to document the main set of user requirements to be satisfied by this release.  Use the user requirement template to draft thense issues.  A well written user requirement should be easy to justify (Rational) and should be testable.  List in order of priority as must have, should have or nice to have for each use case. -->
Well placed button  
Clear and easy to read output graphs/data  
Include user manual with pictures depicting how to use the application and what to expect from the outputs

### 3.3 Proposed User Interface
<!--Could include drawn mockups, screenshots of prototypes, comparison to existing software and other descriptions.-->
UI will be similar to that of the Graphene Raman Fitting Tool. There will be a button to upload or drag and drop files. Once uploaded, the graphs/data will apear in small windows with the ability to save/print.  

### 3.4 Documentation Plan
<!-- List planned documentation activities -->

### 3.5 User Outreach Plan
<!-- List upcoming activities designed to elicit user feedback and/or engage new users.  Use issues for activities that will be completed this iteration-->
Contact colleagues to test the program
Include it in the next nanoHub newsletter
## 4. Data And Quality Attributes

### 4.1 Data Dictionary
<!--Summarize inputs and outputs for the application.-->
The input will be the a raman spectrum file. The outputs will be the graph of the spectrum and also corresponding values of sp2/sp3 peaks.  

### 4.2 Usability and Performance
<!--Summarize usability requirements such as easy of adoption for new users (eg example data),  inline documentation, avoiding errors, efficient interaction, etc.  Describe performance expectations  and/or document challenges.  Note you can reference user requirements from above if needed. -->
Users must be knowledgable about the nanodiamond spectrum, although example data will be provided. Additionally, an instruction manual will be included to explain the layout, features, and how to use the program.  


### 4.3 Testing, Verification and Validation
<!--Describe What data is necessary to verify the basic functionality of the application.  Provide a testing plan that includes a list of issues for each planned activity.  Describe data sets that are needed to test validation.-->
Data from different nanodiamond spectrums (from ones available online or personal data) will be used as inputs, and I will make sure the outputs match the data.

### 4.4 Uncertainty Quantification
<!--Identify and document possible sources of uncertainty. Categorize with standard labels, such as parametric, structural, algorithmic, experimental, interpolation.
Develop a plan for measuring and documenting uncertainty, e.g., using forward propagation or inverse UQ, and showing it in the application, if applicable.-->

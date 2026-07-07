---
title: "Lecture9 InfoVis Intro"
source_pdf: "markdown_files/lecture pdf/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c.pdf"
converted: 2026-07-07
pages: 29
---

# Lecture9 InfoVis Intro

**Source:** `markdown_files/lecture pdf/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c.pdf`  
**Converted:** 2026-07-07  
**Pages:** 29

## Lecture Text

<!-- Page 1 -->
Big Data Visual Analytics (CS 661)
Instructor: Soumya Dutta
Department of Computer Science and Engineering
Indian Institute of Technology Kanpur (IITK)
email: soumyad@cse.iitk.ac.in

<!-- Page 2 -->
2
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Acknowledgements
• Some of the following slides are adapted from the excellent course 
materials and tutorials made available by:
• Prof. Michelle Borkin (Northeastern University)

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Assignment 1 - Due: 15/06/26 11:59pm
• Part 1: Simplified isocontour algorithm for 2D data without handling marching 
square cases or ambiguity cases explicitly
• Traverse the cell vertices in counterclockwise order
• Not allowed to use VTK’s contour filter, write your own code following the method we 
discussed in class
• You do not have to implement the entire marching squares algorithm
• If we see you implemented marching squares, even if your code works, you will get 0
• You do not have to handle marching squares cases
• This is a simplified version of the marching squares algorithm
• Part 2: VTK Volume Rendering, Transfer Function, and Shading
• Consult VTK’s manual, examples for help
• Read the instructions carefully!!
• If you do not follow instructions, points will be deducted

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Assignment 1 - Submission Process
• Submission through HelloIITK
• Only one group member needs to submit from each group
• Submit Python scripts in a single Zipped file
• README.txt file is mandatory with detailed instructions of how to run 
your code and pass parameters and anything else you want the TA to 
know for running your code
• If we cannot run your code, you will not get points
• We will only grade the code submitted in HelloIITK
• Do not email me your code
• Do not submit wrong version of your code
• No deadline extension!

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Academic Integrity for Assignments
• We will perform plagiarism check of your codes
• If we find plagiarism, heavy punishment will be followed
• You will get 0 and will be reported to institute
• So, write your own code!
• We also may ask you to explain how your code works and its logic and if you 
or your group members cannot explain, points will be deducted

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How to Say Nothing with Scientific Visualization
• Never include a color legend
• Avoid annotation
• Never mention error characteristics
• When in doubt, smooth
• Avoid providing performance data
• Never learn anything about the data or the discipline
• Never compare with others
• Never cite references of data
• Claim generalizability but show result on a single data
• Use view angle to hide shortcomings
• ‘This is easily extended to 3D’
Fourteen Ways to Say Nothing with Scientific Visualization, Eric Raible, NASA, in IEEE Computer.

<!-- Page 7 -->
Information 
Visualization

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Information Visualization (InfoVis)
• The use of computer-supported, interactive 
visual representations of data to amplify 
cognition
• Data is not necessarily defined on a spatial domain
• Data is not always numerical 
 
• Data is inherently discrete
• The study of transforming data, information, 
and knowledge into interactive visual 
representations 
Table data
Graph data

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Information Visualization for Business Data
Interactive, topic-based visual text summarization and analysis.
Time (Year 2008)
Topic strength
Visual summary of about 10,000 emails in 2008

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Information Visualization for Science Data
Living Liquid: Design and Evaluation of an Exploratory Visualization Tool for Museum Visitors
Circle viewer with indicators of environmental 
variables at the selected location. Silica: inorganic SiO2 
concentration; Temp: temperature; Nutrient: inorganic 
NO3 concentration; Light: photosynthetically available 
radiation.
Exploratory Data Visualization Tool for Museum Visitors

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Information Visualization for Soccer Data
SoccerStories: A Kick-off for Visual Soccer Analysis, https://www.youtube.com/watch?v=eFIorHSMiSQ

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Information Visualization for ML Classifiers
ConfusionFlow: A model-agnostic visualization for temporal analysis of classifier confusion
• A detailed evaluation 
of classifiers for 
model selection and 
debugging 
• An interactive, 
comparative, model 
agnostic visualization 
system

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Information Visualization for ML Model Explainability
https://gandissect.csail.mit.edu/

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Brief Taxonomy of InfoVis Techniques
• InfoVis Techniques
• Empirical Methods
• Interaction
• Frameworks
• Applications
A survey on information visualization: recent advances and challenges, Liu et al.

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Empirical Methods
• Empirical methods are categorized as 
• Model and Evaluation
• Model
• Visual representation model
• Data driven model
• Evaluation
• User studies are the most used in InfoVis and offer a scientifically sound 
method to measure visualization performance
• Statistical methods such as ANOVA

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Interaction
• Interaction is a fundamental aspect of InfoVis techniques
• Two Interaction categories
• WIMP (windows, icons, mouse, pointer )
• Post-WIMP
• Touch interfaces
• Another operation-based categorization of interactions
• select, explore, reconfigure, encode, abstract/elaborate, filter, and connect

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Frameworks/Systems
• Researchers have proposed a variety 
of visualization systems such as 
Improvise, the InfoVis Toolkit, and 
Prefuse to support the creation and 
customization of visualization 
applications. 
• More recently, a new web-based 
library called Data-Driven Documents 
(D3) has become a very popular 
toolkit to construct interactive 
visualizations on the web 
• https://d3js.org/ 
https://observablehq.com/@d3/galleryhttps://observablehq.com/@d3/gallery

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications
• Different types of data and applications
• Graph data visualization
• Text data visualization
• Map data visualization
• Multivariate data visualization
• Time series visualization
• Many more…

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Exploratory Data Analysis
“The greatest value of a picture is 
when it forces us to notice what we 
never expected to see.”
                                           - John Tukey

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
InfoVis: Big Data Aspects
• Common objectives for big data visualization 
• Decision initiation or modification 
• Enhance understanding 
• Considerations for creating big data visualization systems
• Source data
• Information transfer to the audience
• Design choices/scalability
• Enhance visualization by Graphical overlays
• Highlights
• Encodings
• Summary statistics 
• Annotations

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
InfoVis: Issues and Risks
• Imprecision and Inaccuracy
• Display information at a lower level of precision and accuracy than numerical 
or tabular formats
• Optical Significance 
• Viewer can interpret a difference or pattern as meaningful based on their 
perception, sometimes without corresponding quantitative evidence to 
support this interpretation
• Visualization Oversaturation 
• A dramatic increase in deficient and flawed visualizations

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data analysis 
and Visualization

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data Visualization: Matplotlib
• The most basic and Python’s standard data 
visualization library
• A comprehensive library for creating static, 
animated, and interactive visualizations in Python.
• https://matplotlib.org/
• Examples: 
https://matplotlib.org/stable/gallery/index.html

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data Visualization: Seaborn
• Built on top of Matplotlib but with better aesthetics 
and interactivity
• It provides a high-level interface for drawing 
attractive and informative statistical graphics.
• https://seaborn.pydata.org/
• Examples: https://seaborn.pydata.org/examples

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data Visualization: Bokeh
• Bokeh is a Python library for creating interactive 
visualizations for modern web browsers. 
• Build beautiful graphics, ranging from simple plots to 
complex dashboards
• Create JavaScript-powered visualizations without 
writing any JavaScript code
• https://docs.bokeh.org/en/latest/

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data Visualization: Plotly Dash
• Dash is an Open-Source Python library for creating 
reactive, Web-based applications
• Built on top of Plotly.js and React.js
• User interface library for creating analytical web 
applications
• https://dash.plotly.com/
• https://dash.gallery/Portal/

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data Visualization: Streamlit
• Streamlit is an open-source Python framework 
that lets you quickly turn data scripts into 
interactive web applications—without needing 
to write HTML, CSS, or JavaScript.
• Developers write ordinary Python scripts and add 
Streamlit commands
• The framework launches a local web server that 
renders the interface automatically
• https://streamlit.io/

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data Visualization: PyDeck
• PyDeck is a Python library for creating high-
performance, interactive geospatial and 3D 
visualizations in the browser.
• It is built on top of deck.gl (from the JavaScript 
ecosystem) 
• Allows users to control the powerful WebGL 
visualizations using Python
• https://deckgl.readthedocs.io/en/latest/

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Libraries for Data Visualization: D3
• D3 - Data-Driven Documents
• D3.js is a JavaScript library for manipulating documents 
based on data. 
• D3 helps you bring data to life using HTML, SVG, and CSS.
• D3’s emphasis on web standards gives you the full 
capabilities of modern browsers 
• Combines powerful visualization components and a data-
driven approach to DOM manipulation
• https://d3js.org/

## Figures

### Page 1

![Page 1](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_001.png)

### Page 2

![Page 2](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_002.png)

### Page 3

![Page 3](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_003.png)

### Page 4

![Page 4](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_004.png)

### Page 5

![Page 5](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_005.png)

### Page 6

![Page 6](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_006.png)

### Page 7

![Page 7](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_007.png)

### Page 8

![Page 8](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_008.png)

### Page 9

![Page 9](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_009.png)

### Page 10

![Page 10](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_010.png)

### Page 11

![Page 11](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_011.png)

### Page 12

![Page 12](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_012.png)

### Page 13

![Page 13](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_013.png)

### Page 14

![Page 14](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_014.png)

### Page 15

![Page 15](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_015.png)

### Page 16

![Page 16](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_016.png)

### Page 17

![Page 17](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_017.png)

### Page 18

![Page 18](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_018.png)

### Page 19

![Page 19](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_019.png)

### Page 20

![Page 20](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_020.png)

### Page 21

![Page 21](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_021.png)

### Page 22

![Page 22](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_022.png)

### Page 23

![Page 23](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_023.png)

### Page 24

![Page 24](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_024.png)

### Page 25

![Page 25](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_025.png)

### Page 26

![Page 26](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_026.png)

### Page 27

![Page 27](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_027.png)

### Page 28

![Page 28](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_028.png)

### Page 29

![Page 29](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_029.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_002.png)

### embedded_003

![embedded_003](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_016.png)

### embedded_017

![embedded_017](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_018.png)

### embedded_019

![embedded_019](assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_019.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_002.png` | 2 |
| Page 3 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_003.png` | 3 |
| Page 4 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_004.png` | 4 |
| Page 5 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_005.png` | 5 |
| Page 6 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_006.png` | 6 |
| Page 7 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_007.png` | Information  |
| Page 8 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_008.png` | 8 |
| Page 9 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_009.png` | 9 |
| Page 10 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_010.png` | 10 |
| Page 11 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_011.png` | 11 |
| Page 12 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_012.png` | 12 |
| Page 13 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_013.png` | 13 |
| Page 14 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_014.png` | 14 |
| Page 15 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_015.png` | 15 |
| Page 16 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_016.png` | 16 |
| Page 17 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_017.png` | 17 |
| Page 18 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_018.png` | 18 |
| Page 19 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_019.png` | 19 |
| Page 20 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_020.png` | 20 |
| Page 21 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_021.png` | 21 |
| Page 22 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_022.png` | 22 |
| Page 23 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_023.png` | 23 |
| Page 24 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_024.png` | 24 |
| Page 25 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_025.png` | 25 |
| Page 26 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_026.png` | 26 |
| Page 27 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_027.png` | 27 |
| Page 28 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_028.png` | 28 |
| Page 29 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/page_029.png` | 29 |
| embedded_001 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_002.png` | Embedded raster image |
| embedded_003 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_016.png` | Embedded raster image |
| embedded_017 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_018.png` | Embedded raster image |
| embedded_019 | `assets/Lecture9_InfoVis_Intro_9418acac-e7a9-40e0-8885-34e3c8edb80c/embedded_019.jpg` | Embedded raster image |

---
title: "Lecture3 Scientific Data VTK"
source_pdf: "markdown_files/lecture pdf/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5.pdf"
converted: 2026-07-07
pages: 55
---

# Lecture3 Scientific Data VTK

**Source:** `markdown_files/lecture pdf/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5.pdf`  
**Converted:** 2026-07-07  
**Pages:** 55

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
• Prof. Han-Wei Shen (The Ohio State University)
• Prof. Klaus Mueller (State University of New York at Stony Brook)
• David DeMarle (Intel)

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Reading Materials for Lectures 1 & 2
• Visualization Analysis and Design by T. Munzner
• Chapter 1, Chapter 2, Chapter 5
• Book available online at IITK Library
Reading Materials for Lecture 3 (Today)
• The Visualization Toolkit by Will Schroeder, Ken Martin, Bill Lorensen
• Chapter 1, Chapter 4, Chapter 5
• Get the pdf: https://vtk.org/vtk-textbook/ 
• Reference for learning VTK:
• VTK User’s Guide
• Get the pdf: https://vtk.org/vtk-users-guide/
• Examples: https://kitware.github.io/vtk-examples/site/Python/

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Form Assignment Groups
• Form groups of 3 for assignments 
• Fill in the group member details here: 
https://docs.google.com/spreadsheets/d/1faSZQixVgGhzfbG1vFEO5H
pMGWalUqbMs5VAov8Lv0E/edit?usp=sharing
• Deadline: May 31, 2026

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Data Analysis and 
Visualization

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Imaging, Computer Graphics, and Visualization 
Image processing
Computer Graphics
Visualization
• Study of 2D pictures, 
or images
• Transform, extract 
features, etc.
• Analyze the data
• Process of creating 
images using a 
computer
• 2D paint-and-draw
• Sophisticated 3D 
rendering techniques, 
animation
• Process of exploring, 
transforming, and 
viewing data as 
images, and plots 
• Gain understanding 
and insight into the 
data
“the purpose of visualization is insight, not pictures” – Ben 
Shneiderman

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Visualization (SciVis)
• Technique for comprehending data & knowledge extraction from 
the results of simulations, computations, or measurements
• Field in computer science that encompasses 
• data representation and processing algorithms
• visual representations
• user interface
• other sensory presentation such as sound, touch, AR, VR
• Relatively (new) domain of research (~ 36 years) 
• Formal inception in 1987 by US NSF 
• “Visualization in Scientific Computing” by McCormick et al.

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Example – Application in Climate Science
https://www.youtube.com/watch?v=8Df96rx3i9g

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Example – Application in Asteroid Impact Assessment
https://www.youtube.com/watch?v=95z0qRNFFxs

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Big Data in Scientific Computing and Visualization
• Big data describes datasets that are so large, 
complex, or rapidly changing that they push the 
very limits of our analytical capability1
1NIST Big Data Public Working Group: (https://bigdatawg.nist.gov/_uploadfiles/NIST.SP.1500-1.pdf)
El Capitan World’s fastest supercomputer at LLNL, 
credit: LLNL
Megascale (106 FLOPS) (1961)
Gigascale (109 FLOPS)  (1972)
Terascale (1012 FLOPS) (1997)
Petascale (1015 FLOPS)  (2009)
Exascale (1018 FLOPS) (2022)

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Big Data in Scientific Computing and Visualization
MFIX-Exa: Studies CLR
Exa-Star: Simulation of Universe
TURBO: Studies Engine Stall
Deliver high-fidelity multiphase flow 
modeling capabilities for applications 
in reducing CO2 emissions from fossil 
fuel power plants.
Enable understanding of rotating 
stall in Jet engines and develop 
stall detection as well as stall 
prevention measures.
The target science includes simulations 
of astrophysical explosions (such as 
supernovae and neutron stars) to 
understand the cosmic origin and the 
fundamental physics.
The simulation will use billions of 
particles to model the physics. A 
simulation with 200 million particles and 
100 time steps will need 160 TB storage.
Just a single revolution produces 
5TB of data and hundreds of 
revolutions are needed to run.
Targeted to simulate 8192^3 
resolution grid with 6 scalar 
quantities, i.e., 4TB per time step

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• The “5Vs” of Big Data
Big Data Characterization
• Velocity: Rate at which data is generated
• Volume: The extreme size of the data
• Variety: Diverse types of structured and 
unstructured data
• Veracity: Quality and truthfulness of the 
data
• Value: Contributes to informed decision 
making
Velocity
Veracity
Variety
Value
Volume

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• The “5Vs” of Big Data
Big Data Characterization
• Velocity: Rate at which data is generated
• Volume: The extreme size of the data
• Variety: Diverse types of structured and 
unstructured data
• Veracity: Quality and truthfulness of the 
data
• Value: Contributes to informed decision 
making
Velocity
Veracity
Variety
Value
Volume
The 6th V: Visualization!

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization Pipeline

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization Pipeline

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization Pipeline

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Direct and Inverse Mapping

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Direct and Inverse Mapping

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Representation & 
Scientific Data Model

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Representation
• Scientific data is continuous in nature
• Measure of physical quantities that are studied by various disciplines
• Mathematically, a continuous data is defined as a function
• In practice, such data is sampled in a discrete form in computers for 
representation, manipulation, analysis, and visualization

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset
• A scientific dataset is a related collection of data with a spatial context
• In practice, we deal with discrete datasets sampled from a continuous 
domain for digital representation

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Example
Continuous domain
Discrete samples
Discrete samples: Grid points
Grid points connected to form cells
Data values are given at grid points
Reconstructed data from grid points

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Various Cell Types
Linear Cell Types
Non-linear Cells Types

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Demo Linear Cell
Code: 
https://examples.vtk.org/site/Pyth
on/GeometricObjects/LinearCellsD
emo/

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Attribute Data

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Grid Types
Grid types
Uniform (regular) grid
Rectilinear grid
Structured grid
Unstructured grid

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Uniform (regular) Grid
•
Axis aligned box
•
Sample points are equally spaced

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Rectilinear Grid
•
Axis aligned box
•
Sample points are nonequally spaced

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Structured Grid
•
Allow explicit placement of every sample point
•
Yet preserve the matrix-like ordering
•
Structured grids can be seen as a deformation of 
uniform/rectilinear grids

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scientific Dataset: Unstructured Grid
•
Allow us to define both the sample points and cells explicitly 
•
Different cell types can be mixed
•
Connectivity is explicitly specified

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization Toolkit (VTK)
https://vtk.org/

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
What is VTK?
• VTK: Visualization Toolkit
• An open source, freely available 
software library for 3D visualization, 
graphics, and image processing
• Support for hundreds of algorithms
• Object-oriented design with diﬀerent 
interpreted language wrappers.
Vtk.org

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Installing VTK
• https://anaconda.org/conda-forge/vtk
• You can also use pip to install VTK

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK: Resources
• Examples: https://kitware.github.io/vtk-examples/site/Python/
• VTK User’s Guide: https://vtk.org/vtk-users-guide/
• VTK Textbook: https://vtk.org/vtk-textbook/

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK System Architecture
Wrapper (Python)
C++ core
•Tcl/Tk source
•Java JDK
•Python source
Source code 
Installation: If you want
to extend vtk
All class source
code (could take 
hours to 
compile)
Binary Installation: if you will 
use the classes to build your
applicatoin
Libraries and includes 
(dll and .h files)
Or
(.a and .h files)
•Tcl/Tk shell
•Java interpreter
•Python interpreter

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
(https://vtk.org/doc/nightly/html/classes.html)
VTK classes

<!-- Page 37 -->
37
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Data Types

<!-- Page 38 -->
38
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Pipeline Execution
Source
Filter
Mapper
Actor
Renderer
Direction of data flow
Render Window

<!-- Page 39 -->
39
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Pipeline Execution: Source
Source
Filter
Mapper
Actor
Renderer
Direction of data flow
• Source indicates the dataset source
• Involves data loader of various types
• Uniform, structured, rectilinear, etc.
Render Window

<!-- Page 40 -->
40
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Pipeline Execution: Filter
Source
Filter
Mapper
Actor
Renderer
Direction of data flow
• Filters are another name of algorithms in VTK
• threshold, connected component, surface 
extraction, volume render, etc.
Render Window

<!-- Page 41 -->
41
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Pipeline Execution: Mapper
Source
Filter
Mapper
Actor
Renderer
Direction of data flow
• Mappers convert data into graphical primitives
• Mappers require one or more input data objects, 
output from Filters
• Example: vtkPolyDataMapper, which takes geometry
such as cylinder or cone as input and convert it to 
renderable geometry
Render Window

<!-- Page 42 -->
42
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Pipeline Execution: Actor
Source
Filter
Mapper
Actor
Renderer
Direction of data flow
• Actors represent graphical data or objects with various 
properties for rendering
• A VTK actor contains
– object properties (color, shading type, etc.)
– geometry
– transformations
• VTK actors need to work together with lights (vtkLight) and 
camera (vtkCamera) to make a scene
Render Window

<!-- Page 43 -->
43
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Pipeline Execution: Renderer
Source
Filter
Mapper
Actor
Renderer
Direction of data flow
• vtkRenderer coordinates the rendering process
involving lights, camera, and actors
• vtkRenderer creates a default camera and light if 
not present, but needs to have at least one actor
Render Window

<!-- Page 44 -->
44
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Pipeline Execution: Render Window
Source
Filter
Mapper
Actor
Renderer
Direction of data flow
• The class, vtkRenderWindow ties the 
entire rendering process together
• Manages all the platform dependent window 
management issues and hide the details from
the user
Render Window

<!-- Page 45 -->
45
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 46 -->
46
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 47 -->
47
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 48 -->
48
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 49 -->
49
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 50 -->
50
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 51 -->
51
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 52 -->
52
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 53 -->
53
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 54 -->
54
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program

<!-- Page 55 -->
55
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Simple VTK Program
$> Python Pyramid.py
Demo

## Figures

### Page 1

![Page 1](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_001.png)

### Page 2

![Page 2](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_002.png)

### Page 3

![Page 3](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_003.png)

### Page 4

![Page 4](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_004.png)

### Page 5

![Page 5](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_005.png)

### Page 6

![Page 6](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_006.png)

### Page 7

![Page 7](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_007.png)

### Page 8

![Page 8](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_008.png)

### Page 9

![Page 9](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_009.png)

### Page 10

![Page 10](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_010.png)

### Page 11

![Page 11](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_011.png)

### Page 12

![Page 12](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_012.png)

### Page 13

![Page 13](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_013.png)

### Page 14

![Page 14](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_014.png)

### Page 15

![Page 15](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_015.png)

### Page 16

![Page 16](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_016.png)

### Page 17

![Page 17](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_017.png)

### Page 18

![Page 18](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_018.png)

### Page 19

![Page 19](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_019.png)

### Page 20

![Page 20](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_020.png)

### Page 21

![Page 21](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_021.png)

### Page 22

![Page 22](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_022.png)

### Page 23

![Page 23](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_023.png)

### Page 24

![Page 24](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_024.png)

### Page 25

![Page 25](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_025.png)

### Page 26

![Page 26](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_026.png)

### Page 27

![Page 27](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_027.png)

### Page 28

![Page 28](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_028.png)

### Page 29

![Page 29](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_029.png)

### Page 30

![Page 30](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_030.png)

### Page 31

![Page 31](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_031.png)

### Page 32

![Page 32](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_032.png)

### Page 33

![Page 33](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_033.png)

### Page 34

![Page 34](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_034.png)

### Page 35

![Page 35](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_035.png)

### Page 36

![Page 36](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_036.png)

### Page 37

![Page 37](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_037.png)

### Page 38

![Page 38](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_038.png)

### Page 39

![Page 39](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_039.png)

### Page 40

![Page 40](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_040.png)

### Page 41

![Page 41](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_041.png)

### Page 42

![Page 42](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_042.png)

### Page 43

![Page 43](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_043.png)

### Page 44

![Page 44](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_044.png)

### Page 45

![Page 45](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_045.png)

### Page 46

![Page 46](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_046.png)

### Page 47

![Page 47](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_047.png)

### Page 48

![Page 48](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_048.png)

### Page 49

![Page 49](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_049.png)

### Page 50

![Page 50](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_050.png)

### Page 51

![Page 51](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_051.png)

### Page 52

![Page 52](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_052.png)

### Page 53

![Page 53](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_053.png)

### Page 54

![Page 54](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_054.png)

### Page 55

![Page 55](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_055.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_002.png)

### embedded_003

![embedded_003](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_013.png)

### embedded_014

![embedded_014](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_015.png)

### embedded_016

![embedded_016](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_016.png)

### embedded_017

![embedded_017](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_020.png)

### embedded_021

![embedded_021](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_023.png)

### embedded_024

![embedded_024](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_024.png)

### embedded_025

![embedded_025](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_026.jpg)

### embedded_027

![embedded_027](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_027.png)

### embedded_028

![embedded_028](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_028.jpg)

### embedded_029

![embedded_029](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_029.jpg)

### embedded_030

![embedded_030](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_030.png)

### embedded_031

![embedded_031](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_031.jpg)

### embedded_032

![embedded_032](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_032.png)

### embedded_033

![embedded_033](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_034.jpg)

### embedded_035

![embedded_035](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_035.jpg)

### embedded_036

![embedded_036](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_036.jpg)

### embedded_037

![embedded_037](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_037.jpg)

### embedded_038

![embedded_038](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_038.jpg)

### embedded_039

![embedded_039](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_039.jpg)

### embedded_040

![embedded_040](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_040.jpg)

### embedded_041

![embedded_041](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_041.png)

### embedded_042

![embedded_042](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_042.jpg)

### embedded_043

![embedded_043](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_043.png)

### embedded_044

![embedded_044](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_044.jpg)

### embedded_045

![embedded_045](assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_045.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_002.png` | 2 |
| Page 3 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_003.png` | 3 |
| Page 4 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_004.png` | 4 |
| Page 5 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_005.png` | 5 |
| Page 6 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_006.png` | 6 |
| Page 7 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_007.png` | 7 |
| Page 8 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_008.png` | 8 |
| Page 9 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_009.png` | 9 |
| Page 10 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_010.png` | 10 |
| Page 11 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_011.png` | 11 |
| Page 12 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_012.png` | 12 |
| Page 13 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_013.png` | 13 |
| Page 14 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_014.png` | 14 |
| Page 15 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_015.png` | 15 |
| Page 16 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_016.png` | 16 |
| Page 17 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_017.png` | 17 |
| Page 18 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_018.png` | 18 |
| Page 19 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_019.png` | 19 |
| Page 20 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_020.png` | 20 |
| Page 21 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_021.png` | 21 |
| Page 22 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_022.png` | 22 |
| Page 23 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_023.png` | 23 |
| Page 24 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_024.png` | 24 |
| Page 25 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_025.png` | 25 |
| Page 26 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_026.png` | 26 |
| Page 27 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_027.png` | 27 |
| Page 28 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_028.png` | 28 |
| Page 29 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_029.png` | 29 |
| Page 30 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_030.png` | 30 |
| Page 31 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_031.png` | 31 |
| Page 32 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_032.png` | 32 |
| Page 33 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_033.png` | 33 |
| Page 34 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_034.png` | 34 |
| Page 35 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_035.png` | 35 |
| Page 36 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_036.png` | 36 |
| Page 37 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_037.png` | 37 |
| Page 38 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_038.png` | 38 |
| Page 39 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_039.png` | 39 |
| Page 40 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_040.png` | 40 |
| Page 41 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_041.png` | 41 |
| Page 42 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_042.png` | 42 |
| Page 43 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_043.png` | 43 |
| Page 44 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_044.png` | 44 |
| Page 45 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_045.png` | 45 |
| Page 46 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_046.png` | 46 |
| Page 47 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_047.png` | 47 |
| Page 48 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_048.png` | 48 |
| Page 49 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_049.png` | 49 |
| Page 50 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_050.png` | 50 |
| Page 51 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_051.png` | 51 |
| Page 52 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_052.png` | 52 |
| Page 53 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_053.png` | 53 |
| Page 54 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_054.png` | 54 |
| Page 55 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/page_055.png` | 55 |
| embedded_001 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_002.png` | Embedded raster image |
| embedded_003 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_013.png` | Embedded raster image |
| embedded_014 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_015.png` | Embedded raster image |
| embedded_016 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_016.png` | Embedded raster image |
| embedded_017 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_020.png` | Embedded raster image |
| embedded_021 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_023.png` | Embedded raster image |
| embedded_024 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_024.png` | Embedded raster image |
| embedded_025 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_026.jpg` | Embedded raster image |
| embedded_027 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_027.png` | Embedded raster image |
| embedded_028 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_028.jpg` | Embedded raster image |
| embedded_029 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_029.jpg` | Embedded raster image |
| embedded_030 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_030.png` | Embedded raster image |
| embedded_031 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_031.jpg` | Embedded raster image |
| embedded_032 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_032.png` | Embedded raster image |
| embedded_033 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_034.jpg` | Embedded raster image |
| embedded_035 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_035.jpg` | Embedded raster image |
| embedded_036 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_036.jpg` | Embedded raster image |
| embedded_037 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_037.jpg` | Embedded raster image |
| embedded_038 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_038.jpg` | Embedded raster image |
| embedded_039 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_039.jpg` | Embedded raster image |
| embedded_040 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_040.jpg` | Embedded raster image |
| embedded_041 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_041.png` | Embedded raster image |
| embedded_042 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_042.jpg` | Embedded raster image |
| embedded_043 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_043.png` | Embedded raster image |
| embedded_044 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_044.jpg` | Embedded raster image |
| embedded_045 | `assets/Lecture3_Scientific_Data_VTK_adeb987d-2921-49db-9cf8-44c9807335b5/embedded_045.jpg` | Embedded raster image |

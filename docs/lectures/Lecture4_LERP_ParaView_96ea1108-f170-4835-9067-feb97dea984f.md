---
title: "Lecture4 LERP ParaView"
source_pdf: "markdown_files/lecture pdf/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f.pdf"
converted: 2026-07-07
pages: 47
---

# Lecture4 LERP ParaView

**Source:** `markdown_files/lecture pdf/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f.pdf`  
**Converted:** 2026-07-07  
**Pages:** 47

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
Study Materials
• The Visualization Toolkit by Will Schroeder, Ken Martin, Bill Lorensen
• Chapter 1, Chapter 4, Chapter 5
• Get the pdf: https://vtk.org/vtk-textbook/ 
• Reference for learning VTK:
• VTK User’s Guide
• Get the pdf: https://vtk.org/vtk-users-guide/
• Examples: https://kitware.github.io/vtk-examples/site/Python/
• ParaView Tutorial:
• https://www.youtube.com/watch?v=sXY72e3Ce4g&list=PLGj2a3KTwhRZ7Xup
M7f36czTGlJvqq7_N&index=3

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Linear Interpolation for 
Scientific Data

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Why Interpolation?
• All visualization  algorithms must deal with discrete data 
• What if an algorithm require value at a point which is inside a cell?
Value 
at P
Interpolation
6
4
4.5
5.5

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Linear Interpolation (LERP) 
• Linear Interpolation (lerp): connecting two points with a straight line 
in the function plot 
𝑦= 𝑓(𝑥)
𝑋
𝑌
𝑥1
𝑃
𝑥2
𝑦1
𝑦2
True value
Interpolated 
value

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Linear Interpolation (LERP)
• General form:
𝑣1
𝑣3
𝑣2
𝑣4
•  
P
𝑣𝑖 : value at vertex 𝑖
𝑤𝑖 : weight for 𝑣𝑖
(weighted sum) 
𝑉𝑝= ' 𝑤𝑖∗𝑣𝑖

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Linear Interpolation (LERP)
• General form:
• Essential information needed: 
• Cell type 
• Data value at cell corners
• Parametric coordinates of the point in question (P)
• Related to the position of point P  in the cell
𝑣1
𝑣3
𝑣2
𝑣4
•  
P
𝑣𝑖 : value at vertex 𝑖
𝑤𝑖 : weight for 𝑣𝑖
(weighted sum) 
𝑉𝑝= ' 𝑤𝑖∗𝑣𝑖

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
LERP in Line
• Parametric coordinate of P:  a  =    a / (a+b)  
a
b
v1
v2
P
• Linearly interpolated value of P: 
Vp ?
lerp(v1,v2, a )
Vp  =  (1- a ) * V1    +   a  * V2

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Triangle 
A
B
C
P
Vp ?

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Triangle 
A
B
C
P
Vp ?
dA
dB
dC

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Triangle 
A
B
C
P
Vp ?
dA
dB
dC
• Parametric coordinates of P:  (a,b,g)
 a = dA / (dA + dB + dC)  
 b = dB / (dA + dB + dC)  
 g = dC / (dA + dB + dC) 
Baricentric Coordinates 
• Linearly interpolated value of P:  VA * a + VB * b + VC * g

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Rectangle
A
B
C
D
Vp ?
P
Slides adapted from Prof. Han-Wei Shen

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Rectangle
A
B
C
D
Vp ?
P
• Parametric coordinates of P:  (a,b) 
   
a = a / width; 
a
a

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Rectangle
A
B
C
D
Vp ?
P
L1
L2
• Value  at L1 = Lerp(VA,VB,a) ;       
• Value  at L2 = Lerp(VC,VD,a)  ;       
  
• Parametric coordinates of P:  (a,b) 
   
a = a / width; 
a
a

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Rectangle
A
B
C
D
Vp ?
P
L1
L2
b
a
• Parametric coordinates of P:  (a,b) 
   
a = a / width; 
a

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Rectangle
A
B
C
D
Vp ?
P
L1
L2
b
a
• Parametric coordinates of P:  (a, b) 
   
a = a / width; b =   b / height 
a

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Rectangle
A
B
C
D
Vp ?
P
L1
L2
• Linearly interpolated value of P:  Lerp(VL2, VL1, b) 
b
a
• Parametric coordinates of P:  (a, b) 
   
a = a / width; b =   b / height 
a

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Rectangle
A
B
C
D
Vp ?
P
L1
L2
• Linearly interpolated value of P:  Lerp(VL2, VL1, b) 
b
a
• Parametric coordinates of P:  (a, b) 
   
a = a / width; b =   b / height 
a
Bi-linear interpolation
Bi-Lerp(VA,VB, VC,VD)

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Cube 
x
y
z
V2
V6
V4
V0
V5
V1
V3
V7
P

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Cube 
x
y
z
V2
V6
V4
V0
V5
V1
V3
V7
B
A
• Value  at A = Bi-Lerp(V0,V1,V2,V3) ; 
 
• Value  at B  = Bi-Lerp(V4,V5,V6,V7) ;
  
P

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Cube 
x
y
z
V2
V6
V4
V0
V5
V1
V3
V7
B
A
P
• Value  at A = Bi-Lerp(V0,V1,V2,V3) ; 
 
• Value  at B  = Bi-Lerp(V4,V5,V6,V7) ;

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Cube 
x
y
z
V2
V6
V4
V0
V5
V1
V3
V7
B
A
P
Tri-linear 
interpolation
• Value  at A = Bi-Lerp(V0,V1,V2,V3) ; 
• Value  at B  = Bi-Lerp(V4,V5,V6,V7) ;
• Value  at P  =  Lerp(A,B, PA/AB);

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Cube: Another Way 
x
y
z
c
a
b
V2
V6
V4
V0
V5
V1
V3
V7
P
• Parametric coordinates of P:  (a,b,g) 
a = a / width 
b =  b / depth
   g =   c / height

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Cube: Another Way 
x
y
z
c
a
b
V2
V6
V4
V0
V5
V1
V3
V7
P
• Value at P = 
    (1-a)(1-b)(1-g)V0 + a(1-b)(1-g)V1 + 
    (1-a)b(1-g)V2 + ab(1-g)V3 + 
    (1-a)(1-b)gV4 + a(1-b)gV5 +
    (1-a)bgV6 + abgV7 
• Parametric coordinates of P:  (a,b,g) 
a = a / width 
b =  b / depth 
   g =   c / height

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Tetrahedron
P
A
B
C
D

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Tetrahedron
P
• Break the tetrahedron ABCD into four sub tetrahedra: ABCP, 
BDCP, ACDP, ADBP
• Calculate the volume of each small tetrahedra 
• Calculate P’s parametric (tetrahedral) coordinates based 
on the ratios of the sub-volumes 
A
B
C
D

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Lerp in Tetrahedron
P
A
B
C
D
• Tetrahedral coordinates of P:  (a,b,g,d)
   a = VBDCP / VABCD 
 
b = VACDP / VABCD 
  g = VADBP / VABCD
  d = VABCP / VABCD  
• Linearly interpolated value of P:  VA * a + VB * b + VC * g + VD * d

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Volume of Tetrahedron
1 (x1,y1,z1)
2 (x2,y2,z2)
3 (x3,y3,z3)
4 (x4,y4,z4)
V will be positive if when you look at the triangle 123 from vertex 4, 
vertex 1 2 3 are in a counterclockwise order

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Visualization with 
ParaView

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
What is ParaView
• An open-source, scalable, multi-platform 
visualization application
• Support for distributed computation models 
to process large data sets
• An open, flexible, and intuitive user interface
• An extensible, modular architecture based on 
open standards
• A flexible BSD 3 Clause license
• Commercial maintenance and support

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
ParaView on the Desktop

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
ParaView on the Web

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Python scripts can control ParaView with or without the GUI in 
order to create reproducible and customizable visualizations.
ParaView Scripting - Python

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
ParaView Immersive

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
ParaView for HPC

<!-- Page 37 -->
37
IITK CS661: Big Data Visual Analytics: Soumya Dutta
ParaView Catalyst
Community Atmosphere Model Data Visualized using ParaView Catalyst’s 
In Situ Capability

<!-- Page 38 -->
38
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Ranges Handled by ParaView
• Used for all ranges of data size
• Landmarks of usage
–6 billion structured cells (2005)
–250 million unstructured cells (2005)
–Billions of AMR cells (2008)
–Scaling test over 1 Trillion cells (2010)
–6.33 billion unstructured cells in ParaView Catalyst (2016)
–1.1 trillion unstructured cells scaling test (2016)

<!-- Page 39 -->
39
IITK CS661: Big Data Visual Analytics: Soumya Dutta
ParaView Client
pvpython
ParaWeb
Catalyst
Custom App
UI (Qt Widgets, Python Wrappings)
ParaView Server
VTK
OpenGL
MPI
IceT
Etc.
ParaView Application Architecture

<!-- Page 40 -->
40
IITK CS661: Big Data Visual Analytics: Soumya Dutta
•
ParaView Data (.pvd)
•
VTK (.vtp, .vtu, .vti, .vts, .vtr)
•
VTK Legacy (.vtk)
•
VTK Multi Block 
(.vtm,.vtmb,.vtmg,.vthd,.vthb)
•
Partitioned VTK
(.pvtu, .pvti, .pvts, .pvtr)
•
ADAPT (.nc, .cdf, .elev, .ncd)
•
ANALYZE (.img, .hdr)
•
ANSYS (.inp)
•
AVS UCD (.inp)
•
BOV (.bov)
•
BYU (.g)
•
CAM NetCDF (.nc, .ncdf)
•
CCSM MTSD
(.nc, .cdf, .elev, .ncd)
•
CCSM STSD
(.nc, .cdf, .elev, .ncd)
•
CEAucd (.ucd, .inp)
•
CGNS (.cgns)
•
CMAT (.cmat)
•
CML (.cml)
•
CTRL (.ctrl)
•
Chombo (.hdf5, .h5)
•
Claw (.claw)
•
Comma Separated Values 
(.csv)
•
Cosmology Files 
(.cosmo, .gadget2)
•
Curve2D (.curve, .ultra, .ult, .u)
•
DDCMD (.ddcmd)
•
Digital Elevation Map (.dem)
•
Dyna3D(.dyn)
•
EnSight (.case, .sos)
•
Enzo boundary and hierarchy
•
ExodusII
(.g, .e, .exe, .ex2, .ex2v.., etc)
•
ExtrudedVol (.exvol)
•
FVCOM (MTMD, MTSD,
Particle, STSD)
•
Facet Polygonal Data
•
Flash multiblock files
•
Fluent Case Files (.cas)
•
GGCM (.3df, .mer)
•
GTC (.h5)
•
GULP (.trg)
•
Gadget (.gadget)
•
Gaussian Cube File (.cube)
•
JPEG Image (.jpg, .jpeg)
•
LAMPPS Dump (.dump)
•
LAMPPS Structure Files
•
LODI (.nc, .cdf, .elev, .ncd)
•
LODI Particle
(.nc, .cdf, .elev, .ncd)
•
LS-DYNA (.k, .lsdyna, .d3plot, 
d3plot)
•
M3DCl (.h5)
•
MFIX Unstructred Grid (.RES)
•
MM5 (.mm5)
•
MPAS NetCDF (.nc, .ncdf)
•
Meta Image (.mhd, .mha)
•
Miranda (.mir, .raw)
•
Multilevel 3d Plasma 
(.m3d, .h5)
•
NASTRAN (.nas, .f06)
•
Nek5000 Files
•
Nrrd Raw Image (.nrrd, .nhdr)
•
OpenFOAM Files (.foam)
•
PATRAN (.neu)
•
PFLOTRAN (.h5)
•
PLOT2D (.p2d)
•
PLOT3D (.xyz, .q, .x, .vp3d)
•
PLY Polygonal File Format
•
PNG Image Files
•
POP Ocean Files
•
ParaDIS Files
•
Phasta Files (.pht)
•
Pixie Files (.h5)
•
ProSTAR (.cel, .vrt)
•
Protein Data Bank 
(.pdb, .ent, .pdb)
•
Raw Image Files
•
Raw NRRD image files (.nrrd)
•
SAMRAI (.samrai)
•
SAR (.SAR, .sar)
•
SAS
(.sasgeom, .sas, .sasdata)
•
SESAME Tables
•
SLAC netCDF mesh and mode 
data
•
SLAC netCDF particle data
•
Silo (.silo, .pdb)
•
Spheral (.spheral, .sv)
•
SpyPlot CTH
•
SpyPlot (.case)
•
SpyPlot History (.hscth)
•
Stereo Lithography (.stl)
•
TFT Files
•
TIFF Image Files
•
TSurf Files
•
Tecplot ASCII (.tec, .tp)
•
Tecplot Binary (.plt)
•
Tetrad (.hdf5, .h5)
•
UNIC (.h5)
•
VASP CHGCA (.CHG)
•
VASP OUT (.OUT)
•
VASP POSTCAR (.POS)
•
VPIC (.vpc)
•
VRML (.wrl)
•
Velodyne (.vld, .rst)
•
VizSchema (.h5, .vsh5)
•
Wavefront Polygonal Data
•
WindBlade (.wind)
•
XDMF and hdf5 (.xmf, .xdmf)
•
XMol Molecule
Supported Data Types by ParaView

<!-- Page 41 -->
41
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Render View
User Interface
Menu bar
Toolbar
Pipeline 
Browser
Properties 
Panel
Advanced 
Toggle

<!-- Page 42 -->
42
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Representation

<!-- Page 43 -->
43
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Calculator
Glyph
Contour
Stream Tracer
Clip
Warp (vector)
Slice
Group Datasets
Threshold
Extract Level 
Extract Subset
Common Filters

<!-- Page 44 -->
44
IITK CS661: Big Data Visual Analytics: Soumya Dutta
~ 150 filters
+ C++ plugins
+ python filters
Filters Menu

<!-- Page 45 -->
45
IITK CS661: Big Data Visual Analytics: Soumya Dutta
•
Help Menu
– Getting Started
– The ParaView Tutorials
– The ParaView Guide
• aka The Book
– The ParaView web page
• www.paraview.org
– ParaView discussion forum
• https://discourse.paraview.org/
More Information
Tutorial: https://www.youtube.com/watch?v=sXY72e3Ce4g&list=PLGj2a3KTwhRZ7XupM7f36czTGlJvqq7_N&index=3

<!-- Page 46 -->
46
IITK CS661: Big Data Visual Analytics: Soumya Dutta
ParaView
Demo

<!-- Page 47 -->
47
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Examples

## Figures

### Page 1

![Page 1](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_001.png)

### Page 2

![Page 2](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_002.png)

### Page 3

![Page 3](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_003.png)

### Page 4

![Page 4](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_004.png)

### Page 5

![Page 5](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_005.png)

### Page 6

![Page 6](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_006.png)

### Page 7

![Page 7](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_007.png)

### Page 8

![Page 8](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_008.png)

### Page 9

![Page 9](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_009.png)

### Page 10

![Page 10](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_010.png)

### Page 11

![Page 11](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_011.png)

### Page 12

![Page 12](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_012.png)

### Page 13

![Page 13](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_013.png)

### Page 14

![Page 14](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_014.png)

### Page 15

![Page 15](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_015.png)

### Page 16

![Page 16](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_016.png)

### Page 17

![Page 17](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_017.png)

### Page 18

![Page 18](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_018.png)

### Page 19

![Page 19](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_019.png)

### Page 20

![Page 20](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_020.png)

### Page 21

![Page 21](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_021.png)

### Page 22

![Page 22](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_022.png)

### Page 23

![Page 23](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_023.png)

### Page 24

![Page 24](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_024.png)

### Page 25

![Page 25](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_025.png)

### Page 26

![Page 26](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_026.png)

### Page 27

![Page 27](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_027.png)

### Page 28

![Page 28](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_028.png)

### Page 29

![Page 29](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_029.png)

### Page 30

![Page 30](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_030.png)

### Page 31

![Page 31](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_031.png)

### Page 32

![Page 32](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_032.png)

### Page 33

![Page 33](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_033.png)

### Page 34

![Page 34](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_034.png)

### Page 35

![Page 35](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_035.png)

### Page 36

![Page 36](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_036.png)

### Page 37

![Page 37](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_037.png)

### Page 38

![Page 38](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_038.png)

### Page 39

![Page 39](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_039.png)

### Page 40

![Page 40](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_040.png)

### Page 41

![Page 41](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_041.png)

### Page 42

![Page 42](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_042.png)

### Page 43

![Page 43](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_043.png)

### Page 44

![Page 44](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_044.png)

### Page 45

![Page 45](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_045.png)

### Page 46

![Page 46](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_046.png)

### Page 47

![Page 47](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_047.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_002.png)

### embedded_003

![embedded_003](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_003.png)

### embedded_004

![embedded_004](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_020.png)

### embedded_021

![embedded_021](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_021.png)

### embedded_022

![embedded_022](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_022.png)

### embedded_023

![embedded_023](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_023.png)

### embedded_024

![embedded_024](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_024.png)

### embedded_025

![embedded_025](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_025.png)

### embedded_026

![embedded_026](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_026.png)

### embedded_027

![embedded_027](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_027.png)

### embedded_028

![embedded_028](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_028.png)

### embedded_029

![embedded_029](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_029.png)

### embedded_030

![embedded_030](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_030.jpg)

### embedded_031

![embedded_031](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_031.jpg)

### embedded_032

![embedded_032](assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_032.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_002.png` | 2 |
| Page 3 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_003.png` | 3 |
| Page 4 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_004.png` | 4 |
| Page 5 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_005.png` | 5 |
| Page 6 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_006.png` | 6 |
| Page 7 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_007.png` | 7 |
| Page 8 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_008.png` | 8 |
| Page 9 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_009.png` | 9 |
| Page 10 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_010.png` | 10 |
| Page 11 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_011.png` | 11 |
| Page 12 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_012.png` | 12 |
| Page 13 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_013.png` | 13 |
| Page 14 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_014.png` | 14 |
| Page 15 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_015.png` | 15 |
| Page 16 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_016.png` | 16 |
| Page 17 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_017.png` | 17 |
| Page 18 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_018.png` | 18 |
| Page 19 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_019.png` | 19 |
| Page 20 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_020.png` | 20 |
| Page 21 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_021.png` | 21 |
| Page 22 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_022.png` | 22 |
| Page 23 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_023.png` | 23 |
| Page 24 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_024.png` | 24 |
| Page 25 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_025.png` | 25 |
| Page 26 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_026.png` | 26 |
| Page 27 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_027.png` | 27 |
| Page 28 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_028.png` | 28 |
| Page 29 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_029.png` | 29 |
| Page 30 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_030.png` | 30 |
| Page 31 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_031.png` | 31 |
| Page 32 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_032.png` | 32 |
| Page 33 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_033.png` | 33 |
| Page 34 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_034.png` | 34 |
| Page 35 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_035.png` | 35 |
| Page 36 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_036.png` | 36 |
| Page 37 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_037.png` | 37 |
| Page 38 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_038.png` | 38 |
| Page 39 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_039.png` | 39 |
| Page 40 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_040.png` | 40 |
| Page 41 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_041.png` | 41 |
| Page 42 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_042.png` | 42 |
| Page 43 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_043.png` | 43 |
| Page 44 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_044.png` | 44 |
| Page 45 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_045.png` | 45 |
| Page 46 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_046.png` | 46 |
| Page 47 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/page_047.png` | 47 |
| embedded_001 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_002.png` | Embedded raster image |
| embedded_003 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_003.png` | Embedded raster image |
| embedded_004 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_020.png` | Embedded raster image |
| embedded_021 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_021.png` | Embedded raster image |
| embedded_022 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_022.png` | Embedded raster image |
| embedded_023 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_023.png` | Embedded raster image |
| embedded_024 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_024.png` | Embedded raster image |
| embedded_025 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_025.png` | Embedded raster image |
| embedded_026 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_026.png` | Embedded raster image |
| embedded_027 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_027.png` | Embedded raster image |
| embedded_028 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_028.png` | Embedded raster image |
| embedded_029 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_029.png` | Embedded raster image |
| embedded_030 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_030.jpg` | Embedded raster image |
| embedded_031 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_031.jpg` | Embedded raster image |
| embedded_032 | `assets/Lecture4_LERP_ParaView_96ea1108-f170-4835-9067-feb97dea984f/embedded_032.jpg` | Embedded raster image |

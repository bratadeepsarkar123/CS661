---
title: "Lecture5 Isocontour"
source_pdf: "markdown_files/lecture pdf/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988.pdf"
converted: 2026-07-07
pages: 57
---

# Lecture5 Isocontour

**Source:** `markdown_files/lecture pdf/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988.pdf`  
**Converted:** 2026-07-07  
**Pages:** 57

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
Study Materials for Lecture 5
• William E. Lorensen and Harvey E. Cline. 1987, “Marching cubes: A 
high resolution 3D surface construction algorithm”. SIGGRAPH 
Comput. Graph. 21, 4 (July 1987), 163–169. 
https://doi.org/10.1145/37402.37422.
• Reference: “Resolving the Ambiguity in Marching Cubes” by Nielson 
and Hamman, IEEE VIS’91.
• The Visualization Toolkit by Will Schroeder, Ken Martin, Bill Lorensen
• Chapter 6

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour Algorithm
(2D and 3D)

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
What is an Isocontour?
• An Isocontour is a curve(2D)/surface(3D) 
in a scalar field where the value of the 
scalar function is constant across the 
domain
– 2D: isoline
– 3D: Isosurface
– A technique for analyzing and visualizing 
scalar field data or scalar functions
2D isocontour: Isoline
3D isocontour: Isosurface

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour: Isobar – Lines with Equal Pressure
https://www.newscentermaine.com/

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour
https://web.cs.ucdavis.edu/~okreylos/PhDStudies/Spring2000/ECS277/FootIso.png
Application in Medical Science:
Isosurface of bone and skin

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour
Isocontour (Isobar) at Pressure=250

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour Demo with 
ParaView

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour also Known As ‘Level Set’
• Suppose that F : Rn→R is a function and C is in the range of F. 
• A level set corresponding to an output C is a set of all points x in the 
domain of F with the property that F(x)=C
• In other words, all the points in the level set are assigned the same 
value, C, by the function F, and any point in the domain of F with 
output C is in that level set 
https://ximera.osu.edu/mooculus/calculus3/functionsOfSeveralVariables/digInLevelSets, wikipedia

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Scalar Data 
• Data is sampled from a continuous domain 
• Discrete sampled domain is represented as 
a grid/mesh
• Triangular mesh, cube mesh etc.
• The function value (scalar value) specified 
at mesh/grid vertices
• Values can be interpolated within the 
mesh to get value at a query location

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
v1
v2
v3
v4
v1,v2,v3,v4 all are > C
No isoline in this cell
One cell

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
v1
v2
v3
v4
v1,v2,v3,v4 all are > C
No isoline in this cell
v1,v2,v3,v4 all are < C
No isoline in this cell
v1
v2
v3
v4
One cell
One cell

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
v1
v2
v3
v4
v1,v2,v3,v4 all are > C
No isoline in this cell
v1,v2,v3,v4 all are < C
No isoline in this cell
Otherwise, cell 
contains isocontour
segment 
v1
v2
v3
v4
v1
v2
v3
v4
One cell
One cell
Active cell

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2D Isocontour Extraction: Marching Squares
• Given a 2D scalar field, compute isocontour (isoline) for isovalue = C
• This is usually done in a cell-by-cell manner using Marching Squares algorithm
Contour value (isovalue) = C
Value > C
Value < C

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour in a 2D Cell
• Finding Isocontour in a cell is an inverse problem of value 
interpolation

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontouring by Linear Interpolation
• Compute isocontour within a cell based on linear interpolation
• Identify edges that are ‘zero crossing’
• Values at the two end points are greater (+) 
and smaller (--)  than the contour value
• Calculate the positions in those edges that has 
value equal to isovalue
• Connect the points with a line
P0 (-)
P1 (-)
P3 (+)
P2 (+)

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Step 1: Identify Edges
• Edges that have values greater (+) and less (--) than the contour values 
must contain a point P that has f(p) = C
• This is based on the assumption that values vary linearly and continuously 
across the edge
V2
V1
C
P1
P2
V1
V2

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Step 2: Compute Intersection
• The intersection point f(p) = C on the edge can be computed by linear 
interpolation
d1/d2 = (v1--  C) / (C  -    v2)
p = (v1--   C)/(v1 --    v2) * (p2  --  p1) + p1
(p – p1)/(p2  --  p1)= (v1--  C) / (v1 --   v2)
V2
V1
C
P1
P2
V1
V2
p
d1
d2

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Step 3: Connect the Dots
• Based on the principle of linear interpolation, all points along the line 
P4P5 have values equal to C (isovalue)
Repeat Step1 – Step 3 for all cells
P0 (-)
P1 (-)
P3 (+)
P2 (+)
P4
P5

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Isocontour Cases
• How many ways can an isocontour intersect a rectangular cell?
P4
P3
P2
P1
1: > C
0: < C
P4
P3
P1
P2
• The value at each vertex can be either 
greater or less than the contour value
• So, there are 2 x 2 x 2 x 2 = 16 cases

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Unique Topological Cases
• There are only four unique topological cases
(1) No intersection
(2) Intersect with two adjacent edges
(3) Intersect with two opposite cases
(4) Two contours pass through the cell

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• 2D Isocontouring algorithm for 
square meshes:
• Process one cell at a time
• Compare the values at 4 
vertices with the contour value 
C and identify intersected edges
• Linearly interpolate along the 
intersected edges
• Connect the interpolated points
together
Putting it All Together

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dealing with Ambiguous Cases
• Ambiguous face: A face that has two diagonally opposite points with 
the same sign
+
+
-
-
+
+
-
-
+
+
-
-
How to connect?
Both configurations are possible!

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dealing with Ambiguous Cases
• Ambiguous face: A face that has two diagonally opposite points with 
the same sign
Broken Contour
Connected Contour

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dealing with Ambiguous Cases
• Ambiguous face: A face that has two diagonally opposite points with 
the same sign
+
+
-
-
+
+
-
-
+
+
-
-
How to connect?
Both configurations are possible!
• One way to resolve: Use 
Asymptotic decider
The Asymptotic Decider: Resolving 
the Ambiguity in Marching Cubes 
by Nielson and Hamman, IEEE 
VIS’91

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• The 2D algorithm extends naturally to 3D where the data will have 3D 
cells
• Identify ‘active cells’: cells that intersect with the Isosurface
• Linear interpolation along edges in active cells
• Compute surface patches within each cell based on the edges that 
have intersected with the Isosurface
3D Isocontour: Isosurface
Cube/Rectangular cell
Tetrahedron cell

<!-- Page 37 -->
37
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell
• Active cells: min value < C < max value
• Mark cell vertices that are greater than C with “+” 
and smaller than C with “-”
• Each cell has 4 vertices
• Each vertex can have value greater or less than C
• Hence, 2x2x2x2 = 16 possible combinations
• Only three unique topological cases
Tetrahedron cell

<!-- Page 38 -->
38
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 1
• Case 1: No intersection (all vertices are either outside or inside)
• Values at all cell vertices are either larger or smaller than the     
isovalue C
• If we assume that cell values greater than the contour value C as ‘outside’ and 
smaller as ‘inside’, then all cell vertices are either completely inside or outside 
of the isosurface

<!-- Page 39 -->
39
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 2
• Case 2: One vertex outside (or inside)
• Isosurface only intersects with edges that have ‘+’ and ‘–’ vertices at 
two ends

<!-- Page 40 -->
40
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 2
• Case 2: One vertex outside (or inside)
• Isosurface only intersects with edges that have ‘+’ and ‘–’ vertices at 
two ends

<!-- Page 41 -->
41
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 2
• Case 2: One vertex outside (or inside)
• Compute intersection points on active edges

<!-- Page 42 -->
42
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 2
• Case 2: One vertex outside (or inside)
• Connect intersection points into a triangle

<!-- Page 43 -->
43
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 3
• Case 3: Two vertices outside (or inside)
• Isosurface only intersects with edges that have ‘+’ and ‘–’ vertices at 
two ends

<!-- Page 44 -->
44
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 3
• Case 3: Two vertices outside (or inside)
• Isosurface only intersects with edges that have ‘+’ and ‘–’ vertices at 
two ends

<!-- Page 45 -->
45
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 3
• Case 3: Two vertices outside (or inside)
• Compute intersection points on active edges

<!-- Page 46 -->
46
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Tetrahedral Cell: Case 3
• Case 3: Two vertices outside (or inside)
• Connect intersection points into a triangle

<!-- Page 47 -->
47
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• With 8 vertices in a cell, each having a value 
greater or smaller than the contour value, there 
can be 28 = 256 possible cases
3D Isocontour: Cube/Rectangular Cells
Cube/Rectangular cell

<!-- Page 48 -->
48
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• With 8 vertices in a cell, each having a value 
greater or smaller than the contour value, there 
can be 28 = 256 possible cases
3D Isocontour: Cube/Rectangular Cells
Cube/Rectangular cell
But the total number of unique topological cases is much 
less than 256

<!-- Page 49 -->
49
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Case Reduction
• The topology of the surface does not change, and the unique number 
of cases reduces to 15 from 256
• Value Symmetry
• Rotational Symmetry
+
+
_
_
_
_
_
_
+
+
_
_
+
+
+
+
Value Symmetry

<!-- Page 50 -->
50
IITK CS661: Big Data Visual Analytics: Soumya Dutta
3D Isosurface Unique Cases
• 15 Topologically Unique Cases
Wikipedia

<!-- Page 51 -->
51
IITK CS661: Big Data Visual Analytics: Soumya Dutta
VTK Demo: Marching Cubes Cases
Source: https://gitlab.kitware.com/vtk/vtk-examples/-
/tree/master/src/Python/VisualizationAlgorithms/MarchingCases.py

<!-- Page 52 -->
52
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Marching Cubes Algorithm
• Lorensen and Cline in 1987 
• Mark each cell corner with a bit
• Vi is 1 if value > C (C=isovalue)
• Vi is 0 if value < C 
• Each cell has an index mapped to a value 
ranged [0,255]

<!-- Page 53 -->
53
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Marching Cubes Algorithm
• Based on the values at the vertices, map the cell to one of the 15 cases 
• Perform a table lookup to see what edges have intersections

<!-- Page 54 -->
54
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Marching Cubes Algorithm
• Perform linear interpolation to compute the intersection points at 
the edges 
• Connect the points to form surface patches
• Sequentially scan through the cells – row by row, layer by layer

<!-- Page 55 -->
55
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Ambiguity in Marching Cubes
Arbitrarily choosing marching cubes cases leads to holes in the isosurface

<!-- Page 56 -->
56
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dealing With Ambiguity
• Use ‘Asymptotic decider’
• Idea is similar and extends to 3D
• More details can be found is the paper: “Resolving the Ambiguity in Marching 
Cubes” by Nielson and Hamman, IEEE VIS’91

<!-- Page 57 -->
57
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Marching Cubes Algorithm: Animation
https://www.youtube.com/watch?v=B_xk71YopsA

## Figures

### Page 1

![Page 1](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_001.png)

### Page 2

![Page 2](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_002.png)

### Page 3

![Page 3](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_003.png)

### Page 4

![Page 4](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_004.png)

### Page 5

![Page 5](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_005.png)

### Page 6

![Page 6](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_006.png)

### Page 7

![Page 7](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_007.png)

### Page 8

![Page 8](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_008.png)

### Page 9

![Page 9](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_009.png)

### Page 10

![Page 10](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_010.png)

### Page 11

![Page 11](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_011.png)

### Page 12

![Page 12](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_012.png)

### Page 13

![Page 13](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_013.png)

### Page 14

![Page 14](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_014.png)

### Page 15

![Page 15](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_015.png)

### Page 16

![Page 16](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_016.png)

### Page 17

![Page 17](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_017.png)

### Page 18

![Page 18](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_018.png)

### Page 19

![Page 19](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_019.png)

### Page 20

![Page 20](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_020.png)

### Page 21

![Page 21](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_021.png)

### Page 22

![Page 22](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_022.png)

### Page 23

![Page 23](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_023.png)

### Page 24

![Page 24](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_024.png)

### Page 25

![Page 25](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_025.png)

### Page 26

![Page 26](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_026.png)

### Page 27

![Page 27](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_027.png)

### Page 28

![Page 28](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_028.png)

### Page 29

![Page 29](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_029.png)

### Page 30

![Page 30](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_030.png)

### Page 31

![Page 31](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_031.png)

### Page 32

![Page 32](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_032.png)

### Page 33

![Page 33](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_033.png)

### Page 34

![Page 34](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_034.png)

### Page 35

![Page 35](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_035.png)

### Page 36

![Page 36](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_036.png)

### Page 37

![Page 37](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_037.png)

### Page 38

![Page 38](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_038.png)

### Page 39

![Page 39](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_039.png)

### Page 40

![Page 40](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_040.png)

### Page 41

![Page 41](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_041.png)

### Page 42

![Page 42](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_042.png)

### Page 43

![Page 43](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_043.png)

### Page 44

![Page 44](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_044.png)

### Page 45

![Page 45](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_045.png)

### Page 46

![Page 46](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_046.png)

### Page 47

![Page 47](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_047.png)

### Page 48

![Page 48](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_048.png)

### Page 49

![Page 49](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_049.png)

### Page 50

![Page 50](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_050.png)

### Page 51

![Page 51](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_051.png)

### Page 52

![Page 52](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_052.png)

### Page 53

![Page 53](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_053.png)

### Page 54

![Page 54](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_054.png)

### Page 55

![Page 55](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_055.png)

### Page 56

![Page 56](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_056.png)

### Page 57

![Page 57](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_057.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_009.png)

### embedded_010

![embedded_010](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_016.png)

### embedded_017

![embedded_017](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_017.png)

### embedded_018

![embedded_018](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_018.png)

### embedded_019

![embedded_019](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_019.png)

### embedded_020

![embedded_020](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_021.png)

### embedded_022

![embedded_022](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_022.png)

### embedded_023

![embedded_023](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_023.png)

### embedded_024

![embedded_024](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_024.png)

### embedded_025

![embedded_025](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_025.png)

### embedded_026

![embedded_026](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_026.png)

### embedded_027

![embedded_027](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_028.png)

### embedded_029

![embedded_029](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_029.png)

### embedded_030

![embedded_030](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_030.png)

### embedded_031

![embedded_031](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_031.png)

### embedded_032

![embedded_032](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_032.jpg)

### embedded_033

![embedded_033](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_034.png)

### embedded_035

![embedded_035](assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_035.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_002.png` | 2 |
| Page 3 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_003.png` | 3 |
| Page 4 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_004.png` | 4 |
| Page 5 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_005.png` | 5 |
| Page 6 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_006.png` | 6 |
| Page 7 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_007.png` | 7 |
| Page 8 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_008.png` | 8 |
| Page 9 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_009.png` | 9 |
| Page 10 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_010.png` | 10 |
| Page 11 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_011.png` | 11 |
| Page 12 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_012.png` | 12 |
| Page 13 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_013.png` | 13 |
| Page 14 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_014.png` | 14 |
| Page 15 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_015.png` | 15 |
| Page 16 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_016.png` | 16 |
| Page 17 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_017.png` | 17 |
| Page 18 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_018.png` | 18 |
| Page 19 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_019.png` | 19 |
| Page 20 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_020.png` | 20 |
| Page 21 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_021.png` | 21 |
| Page 22 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_022.png` | 22 |
| Page 23 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_023.png` | 23 |
| Page 24 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_024.png` | 24 |
| Page 25 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_025.png` | 25 |
| Page 26 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_026.png` | 26 |
| Page 27 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_027.png` | 27 |
| Page 28 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_028.png` | 28 |
| Page 29 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_029.png` | 29 |
| Page 30 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_030.png` | 30 |
| Page 31 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_031.png` | 31 |
| Page 32 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_032.png` | 32 |
| Page 33 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_033.png` | 33 |
| Page 34 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_034.png` | 34 |
| Page 35 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_035.png` | 35 |
| Page 36 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_036.png` | 36 |
| Page 37 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_037.png` | 37 |
| Page 38 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_038.png` | 38 |
| Page 39 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_039.png` | 39 |
| Page 40 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_040.png` | 40 |
| Page 41 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_041.png` | 41 |
| Page 42 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_042.png` | 42 |
| Page 43 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_043.png` | 43 |
| Page 44 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_044.png` | 44 |
| Page 45 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_045.png` | 45 |
| Page 46 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_046.png` | 46 |
| Page 47 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_047.png` | 47 |
| Page 48 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_048.png` | 48 |
| Page 49 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_049.png` | 49 |
| Page 50 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_050.png` | 50 |
| Page 51 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_051.png` | 51 |
| Page 52 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_052.png` | 52 |
| Page 53 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_053.png` | 53 |
| Page 54 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_054.png` | 54 |
| Page 55 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_055.png` | 55 |
| Page 56 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_056.png` | 56 |
| Page 57 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/page_057.png` | 57 |
| embedded_001 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_009.png` | Embedded raster image |
| embedded_010 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_016.png` | Embedded raster image |
| embedded_017 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_017.png` | Embedded raster image |
| embedded_018 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_018.png` | Embedded raster image |
| embedded_019 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_019.png` | Embedded raster image |
| embedded_020 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_021.png` | Embedded raster image |
| embedded_022 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_022.png` | Embedded raster image |
| embedded_023 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_023.png` | Embedded raster image |
| embedded_024 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_024.png` | Embedded raster image |
| embedded_025 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_025.png` | Embedded raster image |
| embedded_026 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_026.png` | Embedded raster image |
| embedded_027 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_028.png` | Embedded raster image |
| embedded_029 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_029.png` | Embedded raster image |
| embedded_030 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_030.png` | Embedded raster image |
| embedded_031 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_031.png` | Embedded raster image |
| embedded_032 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_032.jpg` | Embedded raster image |
| embedded_033 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_034.png` | Embedded raster image |
| embedded_035 | `assets/Lecture5_Isocontour_08cd0aee-a6b6-4693-a079-ed8c4df2e988/embedded_035.jpg` | Embedded raster image |

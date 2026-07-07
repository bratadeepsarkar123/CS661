---
title: "Lecture6 Volume Rendering"
source_pdf: "markdown_files/lecture pdf/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83.pdf"
converted: 2026-07-07
pages: 45
---

# Lecture6 Volume Rendering

**Source:** `markdown_files/lecture pdf/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83.pdf`  
**Converted:** 2026-07-07  
**Pages:** 45

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
• Engel, Hadwiger, Salama; Real time volume graphics tutorial, EuroGraphics
2006

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Study Materials for Lecture 6
• The Visualization Toolkit by Will Schroeder, Ken Martin, Bill Lorensen
• Chapter 7 (Volume Rendering section)
• GPU Gems Volume Rendering:
• https://developer.nvidia.com/gpugems/gpugems/part-vi-beyond-
triangles/chapter-39-volume-rendering-techniques
• For detailed mathematical modeling and algorithm
• Optical Models for Direct Volume Rendering by Nelson Max

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Volume Rendering Demo in ParaView
-Von Karman Vortex Street Visualization
https://www.youtube.com/watch?v=k9FPxuhFlTo

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Volume Rendering Demo in ParaView
-Von Karman Vortex Street Visualization

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Volume Rendering

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Medical Science
CT Angiography

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Medical Science

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Geology
Deformed plastic model

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Archeology
Historical Statute

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Materials Science
Quality Control

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Biology
Biological soil 
samples

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Computational Sciences
Study Combustion 
process

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Indirect Visualization of Volume Data
• Isosurface based rendering for 3D data
• Example of indirect technique for volume data exploration
• Using geometric representations
• Points, meshes, surfaces, etc.
Isosurface
Geometric mesh of the isosurface

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Volume Rendering
• Surface visualization is a way of showing data as opaque 
objects
• Though you can apply transparency on surfaces
• Many applications demand techniques that allows “see-
through” capability
• Make parts of the data (semi)transparent so the data behind 
can be seen
• Volume Rendering technique is the answer!
• Direct mapping of underlying 3D data into an image space
• Assumes data as a translucent gel that allows light to go 
through
Opaque
Semi-transparent

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Volume Rendering Key Idea
• Data is considered as a translucent gel
• Rays are cast into the volume data through each pixel to observe data 
values
• Rays accumulate color and opacity values along the ray for final pixel color
Image plane
3D Data
Data samples 
along the ray

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Sampling via Trilinear Interpolation
Grid of the data set
A single cube cell of the data

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Sampling via Trilinear Interpolation
A single cube cell of the data
Sample point 
where data value 
needs to be 
computed
View ray

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Different Volume Rendering Algorithms
• Image-order techniques
• Ray casting approaches
• Object-order techniques
• Splatting
• Texture mapping

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Different Volume Rendering Algorithms
• Image-order techniques
• Ray casting approaches
• Object-order techniques
• Splatting
• Texture mapping

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Image-Order Volume Rendering Techniques
• Typically known as Ray 
casting methods
• Given an image plane, for 
each pixel, we compute the 
color by casting a ray through 
each pixel to the data
• We evaluate the data along 
the ray using some pre-
specified functions for 
computing the final pixel 
color

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Image-Order Volume Rendering Techniques
• How do we accumulate the data values along the ray to produce a 
final pixel color?
1. Maximum Intensity Projection (MIP)
2. Average Intensity Projection (AIP)
3. Distance to a value
4. Compositing

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
1. Maximum Intensity Projection (MIP)
• Compute the maximum intensity 
(data) value along each casted ray and 
the map the value to a color using a 
color scale
Image plane
Take the maximum 
value

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
2. Average Intensity Projection (AIP)
• Compute the average intensity (data) 
value along each casted ray and the 
map the value to a color using a color 
scale
Image plane
Take the average 
value

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
3. Distance to a Value Projection
• Distance to value 30 is shown in the 
rendered image
• Provides the notion of the depth as to 
where the data value 30 is encountered
Image plane
Take the distance to a 
specific value when 
encountered first

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
4. Composite Values Along the Ray
• Use an alpha (opacity) composting 
technique to blend the color values 
obtained from data samples along the 
ray
Image plane
Blend/composite colors 
from the samples

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
AIP vs MIP
https://www.youtube.com/watch?v=Uu_h49xEls8
AIP: Lower noise and smoother edges
MIP: Good for bright structures

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
MIP vs Compositing-based Volume Rendering
Maximum Intensity Projection
Compositing
https://europepmc.org/article/med/20607017

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
MIP vs Compositing-based Volume Rendering
Maximum Intensity Projection
Compositing
Software Infrastructure for exploratory visualization and data analysis: Past, present, and future, Silva and Freire, 2008

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Effect of Step Size During Ray Traversal
• The quality of the image produced from the data depends on the step 
size when each ray is traversed through the data
• Large hop/step size causes artifacts in the final image
• Smaller step size makes image more accurate but also computationally more 
expensive
Step size

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Transparency and Opacity
• Other than RGB color values, there is one more channel – opacity (A)
• Compute RGBA color components
• Opacity (A) = 1 – transparency (T)
• Range [0.0 ... 1.0] 
• Opacity (A) multiplied by RGB color creates a weighting effect

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Ray Casting and Compositing
• Direct Volume Rendering
Wikipedia
1. Ray Casting        2. Sampling             3. Shading            4. Compositing

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Ray Casting and Compositing
• Direct Volume Rendering
Wikipedia
1. Ray Casting        2. Sampling             3. Shading            4. Compositing

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Ray Casting and Compositing
• Direct Volume Rendering
Wikipedia
1. Ray Casting        2. Sampling             3. Shading            4. Compositing

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Ray Casting and Compositing
• Direct Volume Rendering
Wikipedia
1. Ray Casting        2. Sampling             3. Shading            4. Compositing

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Ray Casting and Compositing
• Direct Volume Rendering
Wikipedia
1. Ray Casting        2. Sampling             3. Shading            4. Compositing

<!-- Page 37 -->
37
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Ray Casting and Compositing
• Direct Volume Rendering
https://www.sciencedirect.com/science/article/pii/S009784931830030X

<!-- Page 38 -->
38
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Shading: Phong Illumination Model
• Shading is the process of computing final color for each pixel 
considering its color, opacity, location of the viewer, distance and 
direction of the light, etc.
• Phong Illumination = ambient + diffuse + specular

<!-- Page 39 -->
39
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Shading: Normal Vector for a Volume Data?
• Gradient is used as a proxy for the normal vector in scalar data
• How to compute the gradient vector?
• Central Differences
is the gradient vector

<!-- Page 40 -->
40
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Shading: Normal Vector for a Volume Data?
• Why Gradient makes sense to use as the normal vector in scalar data?
• The gradient vector points in the direction of the maximum rate of change in V
• The gradient is perpendicular (normal) to the isosurface at a point
• This perpendicularity ensures that the gradient naturally aligns with the 
normal vector required for lighting calculations
is a vector tangent to the surface

<!-- Page 41 -->
41
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Shading: Phong Illumination Model
• Illumination = ambient + diffuse + specular
Ambient
Diffuse
Specular
Ambient + 
Diffuse + Specular
https://svenbob.github.io/report%20of%20Project3

<!-- Page 42 -->
42
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Effect of Shading in Volume Visualization
Without shading
With shading

<!-- Page 43 -->
43
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Effect of Shading in Volume Visualization
Without shading
With shading

<!-- Page 44 -->
44
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Opacity and Color Blending: Compositing

<!-- Page 45 -->
45
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Opacity and Color Blending: Compositing

## Figures

### Page 1

![Page 1](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_001.png)

### Page 2

![Page 2](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_002.png)

### Page 3

![Page 3](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_003.png)

### Page 4

![Page 4](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_004.png)

### Page 5

![Page 5](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_005.png)

### Page 6

![Page 6](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_006.png)

### Page 7

![Page 7](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_007.png)

### Page 8

![Page 8](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_008.png)

### Page 9

![Page 9](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_009.png)

### Page 10

![Page 10](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_010.png)

### Page 11

![Page 11](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_011.png)

### Page 12

![Page 12](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_012.png)

### Page 13

![Page 13](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_013.png)

### Page 14

![Page 14](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_014.png)

### Page 15

![Page 15](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_015.png)

### Page 16

![Page 16](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_016.png)

### Page 17

![Page 17](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_017.png)

### Page 18

![Page 18](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_018.png)

### Page 19

![Page 19](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_019.png)

### Page 20

![Page 20](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_020.png)

### Page 21

![Page 21](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_021.png)

### Page 22

![Page 22](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_022.png)

### Page 23

![Page 23](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_023.png)

### Page 24

![Page 24](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_024.png)

### Page 25

![Page 25](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_025.png)

### Page 26

![Page 26](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_026.png)

### Page 27

![Page 27](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_027.png)

### Page 28

![Page 28](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_028.png)

### Page 29

![Page 29](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_029.png)

### Page 30

![Page 30](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_030.png)

### Page 31

![Page 31](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_031.png)

### Page 32

![Page 32](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_032.png)

### Page 33

![Page 33](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_033.png)

### Page 34

![Page 34](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_034.png)

### Page 35

![Page 35](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_035.png)

### Page 36

![Page 36](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_036.png)

### Page 37

![Page 37](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_037.png)

### Page 38

![Page 38](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_038.png)

### Page 39

![Page 39](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_039.png)

### Page 40

![Page 40](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_040.png)

### Page 41

![Page 41](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_041.png)

### Page 42

![Page 42](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_042.png)

### Page 43

![Page 43](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_043.png)

### Page 44

![Page 44](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_044.png)

### Page 45

![Page 45](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_045.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_020.png)

### embedded_021

![embedded_021](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_023.jpg)

### embedded_024

![embedded_024](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_024.jpg)

### embedded_025

![embedded_025](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_026.jpg)

### embedded_027

![embedded_027](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_028.jpg)

### embedded_029

![embedded_029](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_029.jpg)

### embedded_030

![embedded_030](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_030.jpg)

### embedded_031

![embedded_031](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_031.jpg)

### embedded_032

![embedded_032](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_032.jpg)

### embedded_033

![embedded_033](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_034.png)

### embedded_035

![embedded_035](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_035.jpg)

### embedded_036

![embedded_036](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_036.jpg)

### embedded_037

![embedded_037](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_037.jpg)

### embedded_038

![embedded_038](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_038.jpg)

### embedded_039

![embedded_039](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_039.jpg)

### embedded_040

![embedded_040](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_040.jpg)

### embedded_041

![embedded_041](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_041.jpg)

### embedded_042

![embedded_042](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_042.jpg)

### embedded_043

![embedded_043](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_043.png)

### embedded_044

![embedded_044](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_044.png)

### embedded_045

![embedded_045](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_045.png)

### embedded_046

![embedded_046](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_046.png)

### embedded_047

![embedded_047](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_047.jpg)

### embedded_048

![embedded_048](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_048.jpg)

### embedded_049

![embedded_049](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_049.jpg)

### embedded_050

![embedded_050](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_050.png)

### embedded_051

![embedded_051](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_051.jpg)

### embedded_052

![embedded_052](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_052.jpg)

### embedded_053

![embedded_053](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_053.png)

### embedded_054

![embedded_054](assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_054.png)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_002.png` | 2 |
| Page 3 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_003.png` | 3 |
| Page 4 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_004.png` | 4 |
| Page 5 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_005.png` | 5 |
| Page 6 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_006.png` | 6 |
| Page 7 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_007.png` | 7 |
| Page 8 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_008.png` | 8 |
| Page 9 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_009.png` | 9 |
| Page 10 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_010.png` | 10 |
| Page 11 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_011.png` | 11 |
| Page 12 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_012.png` | 12 |
| Page 13 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_013.png` | 13 |
| Page 14 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_014.png` | 14 |
| Page 15 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_015.png` | 15 |
| Page 16 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_016.png` | 16 |
| Page 17 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_017.png` | 17 |
| Page 18 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_018.png` | 18 |
| Page 19 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_019.png` | 19 |
| Page 20 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_020.png` | 20 |
| Page 21 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_021.png` | 21 |
| Page 22 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_022.png` | 22 |
| Page 23 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_023.png` | 23 |
| Page 24 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_024.png` | 24 |
| Page 25 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_025.png` | 25 |
| Page 26 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_026.png` | 26 |
| Page 27 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_027.png` | 27 |
| Page 28 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_028.png` | 28 |
| Page 29 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_029.png` | 29 |
| Page 30 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_030.png` | 30 |
| Page 31 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_031.png` | 31 |
| Page 32 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_032.png` | 32 |
| Page 33 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_033.png` | 33 |
| Page 34 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_034.png` | 34 |
| Page 35 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_035.png` | 35 |
| Page 36 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_036.png` | 36 |
| Page 37 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_037.png` | 37 |
| Page 38 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_038.png` | 38 |
| Page 39 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_039.png` | 39 |
| Page 40 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_040.png` | 40 |
| Page 41 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_041.png` | 41 |
| Page 42 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_042.png` | 42 |
| Page 43 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_043.png` | 43 |
| Page 44 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_044.png` | 44 |
| Page 45 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/page_045.png` | 45 |
| embedded_001 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_020.png` | Embedded raster image |
| embedded_021 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_023.jpg` | Embedded raster image |
| embedded_024 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_024.jpg` | Embedded raster image |
| embedded_025 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_026.jpg` | Embedded raster image |
| embedded_027 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_028.jpg` | Embedded raster image |
| embedded_029 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_029.jpg` | Embedded raster image |
| embedded_030 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_030.jpg` | Embedded raster image |
| embedded_031 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_031.jpg` | Embedded raster image |
| embedded_032 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_032.jpg` | Embedded raster image |
| embedded_033 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_034.png` | Embedded raster image |
| embedded_035 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_035.jpg` | Embedded raster image |
| embedded_036 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_036.jpg` | Embedded raster image |
| embedded_037 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_037.jpg` | Embedded raster image |
| embedded_038 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_038.jpg` | Embedded raster image |
| embedded_039 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_039.jpg` | Embedded raster image |
| embedded_040 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_040.jpg` | Embedded raster image |
| embedded_041 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_041.jpg` | Embedded raster image |
| embedded_042 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_042.jpg` | Embedded raster image |
| embedded_043 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_043.png` | Embedded raster image |
| embedded_044 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_044.png` | Embedded raster image |
| embedded_045 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_045.png` | Embedded raster image |
| embedded_046 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_046.png` | Embedded raster image |
| embedded_047 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_047.jpg` | Embedded raster image |
| embedded_048 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_048.jpg` | Embedded raster image |
| embedded_049 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_049.jpg` | Embedded raster image |
| embedded_050 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_050.png` | Embedded raster image |
| embedded_051 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_051.jpg` | Embedded raster image |
| embedded_052 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_052.jpg` | Embedded raster image |
| embedded_053 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_053.png` | Embedded raster image |
| embedded_054 | `assets/Lecture6_Volume_Rendering_c61f8180-71a9-4cb9-9e1e-46e0c141ed83/embedded_054.png` | Embedded raster image |

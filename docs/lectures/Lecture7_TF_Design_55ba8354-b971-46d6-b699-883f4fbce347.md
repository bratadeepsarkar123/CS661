---
title: "Lecture7 TF Design"
source_pdf: "markdown_files/lecture pdf/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347.pdf"
converted: 2026-07-07
pages: 35
---

# Lecture7 TF Design

**Source:** `markdown_files/lecture pdf/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347.pdf`  
**Converted:** 2026-07-07  
**Pages:** 35

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
• Prof. Tino Weinkauf (KTH Stockholm)

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Study Materials for Lecture 7
• The Visualization Toolkit by Will Schroeder, Ken Martin, Bill Lorensen
• Chapter 7 (Volume Rendering section)
• Transfer function:
• State of the Art in Transfer Functions for Direct Volume Rendering, Ljung et 
al., EuroVis 2016
• Multidimensional Transfer Functions for Interactive Volume Rendering, TVCG 
2002
• Visibility-Driven Transfer Functions, IEEE PacificVis

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Types of Volume Rendering Pipelines
• Pre-shaded pipeline
• Classify and shade the data 
first and then perform ray 
casting and compositing
• Color and opacity values are 
interpolated
Pre-shaded pipeline

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Types of Volume Rendering Pipelines
• Pre-shaded pipeline
• Classify and shade the data 
first and then perform ray 
casting and compositing
• Color and opacity values are 
interpolated
• Post-shaded pipeline
• Directly ray cast into the data, 
get data values at query 
location and use transfer 
function to shade and then 
composite
• Data value are interpolated
Post-shaded pipeline
Pre-shaded pipeline

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Pre-shaded vs Post-shaded Volume Rendering
Blurry edge
Sharp edge

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Transfer Function
• Determines what color & opacity a sample value should have 
• Input: an interpolated data value 
• Output: a color and opacity (RGBA) 
Transfer Function
0
1
Scalar data value color scale

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Transfer Function
• At the simplest form, we can think of four 1D transfer functions
• Red, Green, Blue, Alpha (opacity)
Data value
Data value
Data value
Data value
Intensity of Red
Intensity of Green
Intensity of Blue
Opacity
1.0
1.0
1.0
1.0

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification and Shading
• We have already seen that shading is the process of assigning color 
values to data points considering parameters of the rendering system
• Classification: Mapping data values to opacities
• Region of interest à High Opacity so that clearly seen
• Unimportant regions à Full or semi transparent
Data value
Opacity
1.0
0.0
V = value of interest
Data value
Opacity
1.0
0.0
V1
V2

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification: Color + Opacity Transfer Function
• Distinguish between different materials or features in the data
Single color for all data values and all data values have opacity = 1.0

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification: Color + Opacity Transfer Function
• Distinguish between different materials or features in the data
Set opacity function as a ramp function, shows some structure inside

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification: Color + Opacity Transfer Function
• Distinguish between different materials or features in the data
Add two more colors in the color transfer function, fish is blue, background is green

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification: Color + Opacity Transfer Function
• Distinguish between different materials or features in the data
Modified opacity transfer function to remove some of the background

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification: Color + Opacity Transfer Function
• Distinguish between different materials or features in the data
Use a different color transfer function and try to engineer a more effective opacity function

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification: Color + Opacity Transfer Function
• Distinguish between different materials or features in the data
Change the opacity function to remove the background and the fish is seen clearly

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Transfer Function Design
• Goal:
• Use transfer functions to show salient features from the data set and 
deemphasize the unimportant data

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Transfer Function Design
• Goal:
• Use transfer functions to show salient features from the data set and 
deemphasize the unimportant data
• Challenges:
• Without knowing what data values correspond to important data values, how 
do we design a good transfer function?
• A small difference in transfer function can change the visualization drastically
• Lots of manual tweaking might be required!

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Transfer Function Design
• Goal:
• Use transfer functions to show salient features from the data set and 
deemphasize the unimportant data
• Challenges:
• Without knowing what data values correspond to important data values, how 
do we design a good transfer function?
• A small difference in transfer function can change the visualization drastically
• Lots of manual tweaking might be required!
• Need algorithms and strategies that can automatically analyze data 
design an effective transfer function given all possible transfer 
functions in the search space

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Trail and Error + Domain Knowledge
• Manually control colors for scalar values and try different opacity 
functions to find an optimal one
• Use domain knowledge about the data set to guide the design 
process
• E.g.: what range of values correspond to bone and skin?
• Can take significant amount of time!

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Histogram
• Histogram: A histogram is an approximate representation of a statistical 
distribution. The area under a histogram can be normalized and used as a 
probability distribution function
Source: Wikipedia

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
1D Histogram Assisted Transfer Function Design
• Different features in data set can have different value ranges
• Value clusters can be seen from histogram plots
• Assign different colors for different clusters/histogram regions

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
1D Histogram Assisted Transfer Function Design
• Different features in data set can have different value ranges
• Value clusters can be seen from histogram plots
• Assign different colors for different clusters/histogram regions

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
1D Histogram Assisted Transfer Function Design
• Different features in data set can have different value ranges
• Value clusters can be seen from histogram plots
• Assign different colors for different clusters/histogram regions
Data Values
Opacity
Opacity Transfer 
Function with 
Histogram

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Multi-dimensional Transfer Function
• Use the gradient information of the data to design a better 
transfer function that can highlight boundaries clearly
• Distinct features/materials have roughly constant data value
• Data values transition smoothly from one material to the next 
Gradient of f:

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Multi-dimensional Transfer Function
• Use the gradient information of the data to design a better 
transfer function that can highlight boundaries clearly
• Distinct features/materials have roughly constant data value
• Data values transition smoothly from one material to the next 
Multidimensional Transfer Functions for Interactive Volume Rendering, TVCG 2002

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Multi-dimensional Transfer Function
• Use the gradient information of the data to design a better 
transfer function that can highlight boundaries clearly
• Distinct features/materials have roughly constant data value
• Data values transition smoothly from one material to the next 
Relationships between f, f’, f’’ in an ideal boundary 
Multidimensional Transfer Functions for Interactive Volume Rendering, TVCG 2002

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Multi-dimensional Transfer Function
• Use the gradient information of the data to design a better 
transfer function that can highlight boundaries clearly
• Distinct features/materials have roughly constant data value
• Data values transition smoothly from one material to the next 
Relationships between f, f’, f’’ in an ideal boundary 
Multidimensional Transfer Functions for Interactive Volume Rendering, TVCG 2002

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Multi-dimensional Transfer Function
a: Air
b: Tissue
c: Bone
d: Air and tissue boundary
e: Tissue and bone boundary
f: Air and bone boundary
1D Transfer Function
2D Transfer Function
X-axis: Data Value, Y-axis: Gradient
Multidimensional Transfer Functions for Interactive Volume Rendering, TVCG 2002
a

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visibility Histogram Guided Transfer Functions
• A semi-automatic approach for 
generating opacity transfer function
• The visibility of a sample refers to 
the contribution of a sample to the 
final image, in terms of opacity
• Visibility depends on
• Opacity of the sample
• The viewpoint which affects the 
accumulated opacity in front of the 
sample
Visibility-Driven Transfer Functions, IEEE PacificVis

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visibility Histogram Guided Transfer Functions
• Suppose 𝐴 is in front of 𝐵, which is in front of 𝐶: Eye à A à B à C
• For a sample 𝑖:
Visibility-Driven Transfer Functions, IEEE PacificVis 
A scalar value will have a high visibility if it is not occluded by previous 
samples, and is assigned high opacity
αi = opacity of the sample
Ti = accumulated transparency from eye to that sample
Visibility histogram: Distribution of the 
visibility function in relation to the 
domain values of the volume
•
How much does scalar value 
𝑘 contribute to the rendered image
•
This is view dependent

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visibility Histogram Guided Transfer Functions
• Visibility Histogram: Distribution of the visibility function in relation 
to the domain values of the volume
Visibility-Driven Transfer Functions, IEEE PacificVis 
Visibility Histogram

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visibility Histogram Guided Transfer Functions
• Visibility Histogram: Distribution of the visibility function in relation 
to the domain values of the volume
Visibility-Driven Transfer Functions, IEEE PacificVis 
User wants to see bones
with clarity
Visibility Histogram can provide the guidance
But we can’t see 
bons as flesh and 
skin is blocking it

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visibility Histogram Guided Transfer Functions
Visibility-Driven Transfer Functions, IEEE PacificVis 
Now, bones are clearly seen
Manual but there is Visibility
Histogram that provides 
guidance as to how to 
modify the opacity function
Can we do better?

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visibility Histogram Guided Transfer Functions
• Semi-automatic transfer function design using Visibility Histogram
• Use Optimization technique
• selection of the best solution, regarding some criterion, from some set of 
available alternatives by minimizing an energy function
• Energy function considers characteristics of a good opacity transfer 
function
• User satisfaction: minimize mismatch between user provided initial and 
computer transfer function
• Visibility: maximize visibility of samples
• Constraints: Constraints for opacity transfer function parameters
Visibility-Driven Transfer Functions, IEEE PacificVis

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visibility Histogram Guided Transfer Functions
Visibility-Driven Transfer Functions, IEEE PacificVis

## Figures

### Page 1

![Page 1](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_001.png)

### Page 2

![Page 2](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_002.png)

### Page 3

![Page 3](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_003.png)

### Page 4

![Page 4](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_004.png)

### Page 5

![Page 5](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_005.png)

### Page 6

![Page 6](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_006.png)

### Page 7

![Page 7](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_007.png)

### Page 8

![Page 8](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_008.png)

### Page 9

![Page 9](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_009.png)

### Page 10

![Page 10](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_010.png)

### Page 11

![Page 11](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_011.png)

### Page 12

![Page 12](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_012.png)

### Page 13

![Page 13](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_013.png)

### Page 14

![Page 14](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_014.png)

### Page 15

![Page 15](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_015.png)

### Page 16

![Page 16](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_016.png)

### Page 17

![Page 17](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_017.png)

### Page 18

![Page 18](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_018.png)

### Page 19

![Page 19](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_019.png)

### Page 20

![Page 20](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_020.png)

### Page 21

![Page 21](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_021.png)

### Page 22

![Page 22](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_022.png)

### Page 23

![Page 23](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_023.png)

### Page 24

![Page 24](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_024.png)

### Page 25

![Page 25](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_025.png)

### Page 26

![Page 26](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_026.png)

### Page 27

![Page 27](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_027.png)

### Page 28

![Page 28](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_028.png)

### Page 29

![Page 29](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_029.png)

### Page 30

![Page 30](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_030.png)

### Page 31

![Page 31](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_031.png)

### Page 32

![Page 32](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_032.png)

### Page 33

![Page 33](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_033.png)

### Page 34

![Page 34](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_034.png)

### Page 35

![Page 35](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_035.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_013.png)

### embedded_014

![embedded_014](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_023.jpg)

### embedded_024

![embedded_024](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_024.jpg)

### embedded_025

![embedded_025](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_026.png)

### embedded_027

![embedded_027](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_027.png)

### embedded_028

![embedded_028](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_028.jpg)

### embedded_029

![embedded_029](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_029.jpg)

### embedded_030

![embedded_030](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_030.jpg)

### embedded_031

![embedded_031](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_031.png)

### embedded_032

![embedded_032](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_032.jpg)

### embedded_033

![embedded_033](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_034.jpg)

### embedded_035

![embedded_035](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_035.jpg)

### embedded_036

![embedded_036](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_036.jpg)

### embedded_037

![embedded_037](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_037.jpg)

### embedded_038

![embedded_038](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_038.jpg)

### embedded_039

![embedded_039](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_039.png)

### embedded_040

![embedded_040](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_040.jpg)

### embedded_041

![embedded_041](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_041.jpg)

### embedded_042

![embedded_042](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_042.jpg)

### embedded_043

![embedded_043](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_043.jpg)

### embedded_044

![embedded_044](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_044.jpg)

### embedded_045

![embedded_045](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_045.jpg)

### embedded_046

![embedded_046](assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_046.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_002.png` | 2 |
| Page 3 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_003.png` | 3 |
| Page 4 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_004.png` | 4 |
| Page 5 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_005.png` | 5 |
| Page 6 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_006.png` | 6 |
| Page 7 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_007.png` | 7 |
| Page 8 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_008.png` | 8 |
| Page 9 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_009.png` | 9 |
| Page 10 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_010.png` | 10 |
| Page 11 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_011.png` | 11 |
| Page 12 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_012.png` | 12 |
| Page 13 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_013.png` | 13 |
| Page 14 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_014.png` | 14 |
| Page 15 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_015.png` | 15 |
| Page 16 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_016.png` | 16 |
| Page 17 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_017.png` | 17 |
| Page 18 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_018.png` | 18 |
| Page 19 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_019.png` | 19 |
| Page 20 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_020.png` | 20 |
| Page 21 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_021.png` | 21 |
| Page 22 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_022.png` | 22 |
| Page 23 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_023.png` | 23 |
| Page 24 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_024.png` | 24 |
| Page 25 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_025.png` | 25 |
| Page 26 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_026.png` | 26 |
| Page 27 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_027.png` | 27 |
| Page 28 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_028.png` | 28 |
| Page 29 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_029.png` | 29 |
| Page 30 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_030.png` | 30 |
| Page 31 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_031.png` | 31 |
| Page 32 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_032.png` | 32 |
| Page 33 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_033.png` | 33 |
| Page 34 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_034.png` | 34 |
| Page 35 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/page_035.png` | 35 |
| embedded_001 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_013.png` | Embedded raster image |
| embedded_014 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_023.jpg` | Embedded raster image |
| embedded_024 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_024.jpg` | Embedded raster image |
| embedded_025 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_026.png` | Embedded raster image |
| embedded_027 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_027.png` | Embedded raster image |
| embedded_028 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_028.jpg` | Embedded raster image |
| embedded_029 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_029.jpg` | Embedded raster image |
| embedded_030 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_030.jpg` | Embedded raster image |
| embedded_031 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_031.png` | Embedded raster image |
| embedded_032 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_032.jpg` | Embedded raster image |
| embedded_033 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_034.jpg` | Embedded raster image |
| embedded_035 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_035.jpg` | Embedded raster image |
| embedded_036 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_036.jpg` | Embedded raster image |
| embedded_037 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_037.jpg` | Embedded raster image |
| embedded_038 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_038.jpg` | Embedded raster image |
| embedded_039 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_039.png` | Embedded raster image |
| embedded_040 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_040.jpg` | Embedded raster image |
| embedded_041 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_041.jpg` | Embedded raster image |
| embedded_042 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_042.jpg` | Embedded raster image |
| embedded_043 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_043.jpg` | Embedded raster image |
| embedded_044 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_044.jpg` | Embedded raster image |
| embedded_045 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_045.jpg` | Embedded raster image |
| embedded_046 | `assets/Lecture7_TF_Design_55ba8354-b971-46d6-b699-883f4fbce347/embedded_046.jpg` | Embedded raster image |

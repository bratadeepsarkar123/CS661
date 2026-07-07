---
title: "Lecture18 Sampling 2"
source_pdf: "markdown_files/lecture pdf/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528.pdf"
converted: 2026-07-07
pages: 25
---

# Lecture18 Sampling 2

**Source:** `markdown_files/lecture pdf/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528.pdf`  
**Converted:** 2026-07-07  
**Pages:** 25

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
Study Materials for Lecture 19
• Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis, IEEE Transactions on 
Visualization and Computer Graphics (TVCG), 2021, Volume 27, Issue 12, pp. 4439-4454.

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Driven Importance-based Sampling
• Is SRS always the preferred choice?
• No, depends on the application and goal
• We may need to preserve certain data more 
accurately than others
• Features (regions of interest) in the data
• All data points are NOT equally likely to get picked
• Sample data points based on an importance 
criterion to achieve the desired objective
• How to define and construct an importance 
function? 
Original data showing the 
important region
What SRS will give us
What we want, more samples from 
the important region

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Driven Importance-based Sampling
• How to design an appropriate importance function/criterion?
• Idea: Assign more importance to the data points with low value 
occurrence/probability
Data Histogram
Acceptance Function
Data Histogram after Sampling
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Histogram
Acceptance Function
Data Histogram after Sampling
• Similar in spirit to performing Entropy maximization
• Entropy: In information theory, the entropy of a random variable is 
the average level of "information", "surprise", or "uncertainty" 
inherent to the variable's possible outcomes. 
Data Driven Importance-based Sampling
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Histogram
Acceptance Function
Data Histogram after Sampling
Entropy = 𝐻𝑋= −∑! 𝑝𝑥∗log(𝑝𝑥)
• Base 2 with log gives the result in units of bits
Data Driven Importance-based Sampling
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Histogram
Acceptance Function
Data Histogram after Sampling
Entropy = 𝐻𝑋= −∑! 𝑝𝑥∗log(𝑝𝑥)
Uniform distribution has 
maximum entropy
Data Driven Importance-based Sampling
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Importance-based Sampling Pseudo Code
• How do we create an acceptance function that is implicitly going to 
maximize entropy of the data value distribution?
In Situ Data-Driven Adaptive Sampling for Large-scale Simulation Data Summarization

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Reconstruction From Sampled Data
• A naïve reconstruction method is nearest 
neighbor interpolation
• Fast execution but quality is not good
• Linear interpolation-based reconstruction
• Create a 3D convex hull using all sampled points
• a set of points in a plane (or higher-dimensional space) is 
the smallest convex shape that encloses all the given 
points.
• Convert the points into a polygonal mesh using 
Delaunay triangulation
• Next, for each grid point in the reconstruction grid, 
the value is obtained by linearly interpolating scalar 
values from the vertices of the simplex that encloses 
the current grid point 
Convex hull
In Situ Data-Driven Adaptive Sampling for Large-scale Simulation Data Summarization

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Results of Importance Sampling
Reconstruction using 
stratified random Sampling
(1% points sampled)
Original data (volume 
rendered)
Reconstruction using 
Importance-based Sampling
(1% points sampled)
In Situ Data-Driven Adaptive Sampling for Large-scale Simulation Data Summarization

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Results of Importance Sampling
Stratified Random Sampling
(0.5% points sampled)
Importance-based Sampling
(0.5% points sampled)
Systematic Sampling
(1.5% points sampled)
In Situ Data-Driven Adaptive Sampling for Large-scale Simulation Data Summarization

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Quality and Performance Evaluation
Showing linear correlation values with the original data
(Higher is better)
In Situ Data-Driven Adaptive Sampling for Large-scale Simulation Data Summarization

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Improved Importance-based Sampling
• How to select a subset of data points that are informative and 
preserve features?
Informative regions are the birds, and the 
homogeneous sky is background.
High gradient regions are important
•
Analyze the data value occurrence and local smoothness/gradient
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Smoothness/Gradient Visualization
2D histogram of water fraction and its 
gradient magnitude
Volume visualization of gradient
of water fraction.
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Joint Multi-Criteria Sampling
Value-based Sampling
Smoothness-based Sampling
H – Data value Histogram
IF – Importance function
M – Total num. of points to be selected
B – Num. of histogram Bins
C – Expected num. of samples per bin
H – Data value, Grad. Mag. Histogram
IF – Importance function
M – Total num. of points to be selected
B – Num. of histogram Bins
C – Expected num. of samples per bin
Blue: Original Hist. 
Orange: selected points
Blue: Original Hist. 
Orange: selected points
Acceptance function for 
the histogram
Acceptance function for 
the histogram
2D Histogram of data value and Gradient Magnitude
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• First compute the Importance function (IF) based on value-based 
sampling
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021
Joint Multi-Criteria Sampling
Value Histogram
Gradient Histogram
• Use gradient to prioritize samples when selecting from each histogram 
bin of value-based histogram
Joint Multi-Criteria Sampling

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Overall Framework for Multi Criteria Sampling
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Results of Importance Sampling
Original data showing the important region
Random Sampling
Value-based Sampling
Smoothness-based Sampling
Joint Multi-Criteria Sampling
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Query-driven Analysis
Result of a query of pressure ≥ -5000.0 AND ≤ -500.0
Result of a query of Mixfrac var >= 0.3 AND <= 0.5
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Reconstruction of Data
Original data
Reconstructed data
Original data
Reconstructed data
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Applications: Isocontour of Data
Original contour
Reconstructed contour
Original contour
Reconstructed contour
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Quality Evaluation
Signal to noise Ratio
Correlation coefficient
𝑆𝑁𝑅= 20 ∗𝑙𝑜𝑔10
𝜎𝑟𝑎𝑤
𝜎𝑛𝑜𝑖𝑠𝑒
Corr(X, Y) = 𝑐𝑜𝑣(𝑋, 𝑌)
𝜎𝑋𝜎𝑌
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Comparison with Zfp Compression Method
Joint multi criteria sampling (1%)
Zfp at fixed rate (1%)
Zfp at fixed accuracy
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Error Analysis
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Implementation & Performance
A. Biswas, S. Dutta et al., "Probabilistic Data-Driven Sampling via Multi-Criteria Importance Analysis", IEEE TVCG 2021

## Figures

### Page 1

![Page 1](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_001.png)

### Page 2

![Page 2](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_002.png)

### Page 3

![Page 3](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_003.png)

### Page 4

![Page 4](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_004.png)

### Page 5

![Page 5](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_005.png)

### Page 6

![Page 6](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_006.png)

### Page 7

![Page 7](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_007.png)

### Page 8

![Page 8](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_008.png)

### Page 9

![Page 9](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_009.png)

### Page 10

![Page 10](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_010.png)

### Page 11

![Page 11](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_011.png)

### Page 12

![Page 12](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_012.png)

### Page 13

![Page 13](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_013.png)

### Page 14

![Page 14](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_014.png)

### Page 15

![Page 15](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_015.png)

### Page 16

![Page 16](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_016.png)

### Page 17

![Page 17](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_017.png)

### Page 18

![Page 18](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_018.png)

### Page 19

![Page 19](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_019.png)

### Page 20

![Page 20](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_020.png)

### Page 21

![Page 21](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_021.png)

### Page 22

![Page 22](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_022.png)

### Page 23

![Page 23](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_023.png)

### Page 24

![Page 24](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_024.png)

### Page 25

![Page 25](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_025.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_008.png)

### embedded_009

![embedded_009](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_019.png)

### embedded_020

![embedded_020](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_020.png)

### embedded_021

![embedded_021](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_021.png)

### embedded_022

![embedded_022](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_022.png)

### embedded_023

![embedded_023](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_023.jpg)

### embedded_024

![embedded_024](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_024.jpg)

### embedded_025

![embedded_025](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_025.png)

### embedded_026

![embedded_026](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_026.png)

### embedded_027

![embedded_027](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_028.jpg)

### embedded_029

![embedded_029](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_029.jpg)

### embedded_030

![embedded_030](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_030.jpg)

### embedded_031

![embedded_031](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_031.jpg)

### embedded_032

![embedded_032](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_032.jpg)

### embedded_033

![embedded_033](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_034.jpg)

### embedded_035

![embedded_035](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_035.jpg)

### embedded_036

![embedded_036](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_036.jpg)

### embedded_037

![embedded_037](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_037.jpg)

### embedded_038

![embedded_038](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_038.jpg)

### embedded_039

![embedded_039](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_039.jpg)

### embedded_040

![embedded_040](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_040.jpg)

### embedded_041

![embedded_041](assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_041.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_002.png` | 2 |
| Page 3 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_003.png` | 3 |
| Page 4 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_004.png` | 4 |
| Page 5 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_005.png` | 5 |
| Page 6 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_006.png` | 6 |
| Page 7 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_007.png` | 7 |
| Page 8 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_008.png` | 8 |
| Page 9 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_009.png` | 9 |
| Page 10 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_010.png` | 10 |
| Page 11 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_011.png` | 11 |
| Page 12 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_012.png` | 12 |
| Page 13 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_013.png` | 13 |
| Page 14 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_014.png` | 14 |
| Page 15 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_015.png` | 15 |
| Page 16 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_016.png` | 16 |
| Page 17 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_017.png` | 17 |
| Page 18 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_018.png` | 18 |
| Page 19 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_019.png` | 19 |
| Page 20 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_020.png` | 20 |
| Page 21 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_021.png` | 21 |
| Page 22 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_022.png` | 22 |
| Page 23 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_023.png` | 23 |
| Page 24 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_024.png` | 24 |
| Page 25 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/page_025.png` | 25 |
| embedded_001 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_008.png` | Embedded raster image |
| embedded_009 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_019.png` | Embedded raster image |
| embedded_020 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_020.png` | Embedded raster image |
| embedded_021 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_021.png` | Embedded raster image |
| embedded_022 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_022.png` | Embedded raster image |
| embedded_023 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_023.jpg` | Embedded raster image |
| embedded_024 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_024.jpg` | Embedded raster image |
| embedded_025 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_025.png` | Embedded raster image |
| embedded_026 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_026.png` | Embedded raster image |
| embedded_027 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_028.jpg` | Embedded raster image |
| embedded_029 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_029.jpg` | Embedded raster image |
| embedded_030 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_030.jpg` | Embedded raster image |
| embedded_031 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_031.jpg` | Embedded raster image |
| embedded_032 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_032.jpg` | Embedded raster image |
| embedded_033 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_034.jpg` | Embedded raster image |
| embedded_035 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_035.jpg` | Embedded raster image |
| embedded_036 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_036.jpg` | Embedded raster image |
| embedded_037 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_037.jpg` | Embedded raster image |
| embedded_038 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_038.jpg` | Embedded raster image |
| embedded_039 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_039.jpg` | Embedded raster image |
| embedded_040 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_040.jpg` | Embedded raster image |
| embedded_041 | `assets/Lecture18_Sampling_2_0debfd35-1cf6-4631-aad6-7e6613a2f528/embedded_041.jpg` | Embedded raster image |

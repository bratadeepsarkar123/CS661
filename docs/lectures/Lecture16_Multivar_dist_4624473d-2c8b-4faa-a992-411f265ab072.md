---
title: "Lecture16 Multivar dist"
source_pdf: "markdown_files/lecture pdf/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072.pdf"
converted: 2026-07-07
pages: 24
---

# Lecture16 Multivar dist

**Source:** `markdown_files/lecture pdf/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072.pdf`  
**Converted:** 2026-07-07  
**Pages:** 24

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
CS661 Quiz
• Date: July 6th Monday
• Where: LH-20
• When: 4:00pm-6:00pm
• Syllabus: Starting from lecture 11 (High Dimensional Data) - 
everything discussed until July 5th

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Study Materials for Lecture 16
• CoDDA: A Flexible Copula-based Distribution Driven Analysis Framework for 
Large-Scale Multivariate Data, Hazarika et al., IEEE TVCG.

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Multivariate Data Models using Distributions
• Multivariate Histogram
• Storage footprint of a multivariate histogram can increase exponentially with 
the number of variables and the desired level of discretization 
• Sparse representations can be used by storing only non-zero bins
• Multivariate GMM
• Estimation of multivariate GMM using Expectation-Maximization is 
computationally expensive 
• Model complexity increases with the number of variables
• Multivariate KDE
• Often computationally expensive and storage inefficient
• Important to preserve the dependency/correlations between 
variables for downstream multivariate analysis

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Concept of Copula
• Definition: A 𝑑-dimensional Copula is a CDF with uniform marginals. For 
𝑑-uniform random variables, it can be denoted as 𝑪(𝒖𝟏, 𝒖𝟐, … , 𝒖𝒅) .
• “Every joint CDF in 𝓡𝒅 inherently embodies a copula function”: Sklar 
(1959)
• Sklar’s Theorem provides the mathematical basis for splitting the problem 
of joint distribution estimation into two parts (using Copula functions):
1.
Estimating individual univariate marginal distributions.
2.
Estimating the dependencies between the random variables.

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distribution Transformation Property
• Property 1: If 𝑈 is a uniform random variable (i.e., 𝑈 ~ 𝑈𝑛𝑖𝑓[0,1] ) and 𝐹𝑋 is 
a CDF of random variable 𝑋, then its inverse function 𝐹!
"# (𝑈)  corresponds 
to the random variable 𝑋  (i.e., 𝐹!
"# (𝑈)~ 𝑋)
0.0
1.0
0.0
2.0
-2.0
𝑈
𝐹!
"#
𝑋

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Property 2: If a real-valued random variable 𝑋 has a continuous cumulative 
distribution function 𝐹𝑋, then 𝐹𝑋(𝑋) ~ 𝑈𝑛𝑖𝑓[0,1] 
0.0
1.0
0.0
2.0
-2.0
𝑈
𝑋
𝐹𝑋
Distribution Transformation Property

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Consider a bivariate distribution of 2 random variables 𝑋 and 𝑌 with a strong 
negative correlation coefficient of −0.9
• Let, 𝐹𝑋 and 𝐹𝑌 be their respective CDFs.
• So, we have: 𝐹𝑋 , 𝐹𝑌 and 𝜌= −0.9
 
Concept of Copula: Bivariate Example
𝒀
𝑿

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Concept of Copula: Bivariate Example
𝒀′
𝑿′
𝑼𝒀
𝑼𝑿
• Step 1: Draw samples from a bivariate standard normal distribution with the 
desired correlation
• Step 2: Transform the Gaussian marginal distributions to Uniform distributions 
i.e., 𝑈𝑋 and 𝑈𝑌 [Property 2] 
• Step 3: Transform 𝑈𝑋 and 𝑈𝑌 to the desired marginal distribution forms using 
the inverse function of 𝐹𝑋 and 𝐹𝑌 [Property 1] 
𝒀
𝑿

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Concept of Copula: Bivariate Example
𝒀′
𝑿′
𝑼𝒀
𝑼𝑿
𝒀
𝑿
• Step 2 represents samples generated from a Gaussian Copula
• Gaussian Copula à standard normal distribution
• Final distribution à Meta-Gaussian distribution

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• What information to store in our multivariate data summaries?
Multivariate Data Summary Using Copula

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Consider multivariate system of variables 𝒗𝟏, 𝒗𝟐, 𝒗𝟑, 𝒗𝟒
• Univariate distributions, 𝜽𝒊 à distribution parameters for ith variable 
• Dependency structure (correlation matrix for Gaussian Copula)
Multivariate Data Summary Using Copula
𝒗𝟏
𝒗𝟐
𝒗𝟑
𝒗𝟒
𝒗𝟏
𝒗𝟐
𝒗𝟑
𝒗𝟒
𝟏
𝝆𝟏𝟐𝝆𝟏𝟑𝝆𝟏𝟒
𝝆𝟐𝟏
𝟏
𝝆𝟐𝟑𝝆𝟐𝟒
𝝆𝟑𝟏𝝆𝟑𝟐𝟏
𝝆𝟑𝟒
𝝆𝟒𝟏𝝆𝟒𝟐𝝆𝟒𝟑𝟏

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Consider multivariate system of variables 𝒗𝟏, 𝒗𝟐, 𝒗𝟑, 𝒗𝟒
• Univariate distributions, 𝜽𝒊 à distribution parameters for ith variable
• Dependency structure (correlation matrix for Gaussian Copula)
𝒗𝟏
𝒗𝟐
𝒗𝟑
𝒗𝟒
𝒗𝟏
𝒗𝟐
𝒗𝟑
𝒗𝟒
𝟏
𝝆𝟏𝟐𝝆𝟏𝟑𝝆𝟏𝟒
𝝆𝟐𝟏
𝟏
𝝆𝟐𝟑𝝆𝟐𝟒
𝝆𝟑𝟏𝝆𝟑𝟐𝟏
𝝆𝟑𝟒
𝝆𝟒𝟏𝝆𝟒𝟐𝝆𝟒𝟑𝟏
Multivariate Data Summary Using Copula

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Storage footprint = ;𝒊)𝟏
𝐧
𝒔𝒊𝒛𝒆(𝜽𝒊) +
elems from upper or lower triangular matrix)
𝒗𝟏
𝒗𝟐
𝒗𝟑
𝒗𝟒
𝒗𝟏
𝒗𝟐
𝒗𝟑
𝒗𝟒
𝟏
𝝆𝟏𝟐𝝆𝟏𝟑𝝆𝟏𝟒
𝝆𝟐𝟏
𝟏
𝝆𝟐𝟑𝝆𝟐𝟒
𝝆𝟑𝟐𝝆𝟑𝟐𝟏
𝝆𝟑𝟒
𝝆𝟒𝟐𝝆𝟒𝟐𝝆𝟒𝟑𝟏
Multivariate Data Summary Using Copula

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Storing only the value distribution misses the spatial context of the data
Spatial Distributions
< 𝒗>

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Consider 𝒙 and 𝒚 distributions (uniform) along with 𝒗 
Spatial Distributions
𝒗
𝒗
𝒙
𝑦
𝟏
𝝆𝒗𝒙
𝝆𝒗𝒚
𝝆𝒙𝒗
𝟏
𝟎
𝝆𝒚𝒗𝟎
𝟏
𝒙
𝒚
< 𝒗, 𝒙, 𝒚>
𝒗
𝒙
𝒚
MV Data Summaries

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
𝒗
𝒗
𝒙
𝑦
𝟏
𝝆𝒗𝒙
𝝆𝒗𝒚
𝝆𝒙𝒗
𝟏
𝟎
𝝆𝒚𝒗𝟎
𝟏
𝒙
𝒚
< 𝒗, 𝒙, 𝒚>
𝒗
𝒙
𝒚
• Consider 𝒙 and 𝒚 distributions (uniform) along with 𝒗 
Spatial Distributions
MV Data Summaries

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
𝒗
𝒗
𝒙
𝑦
𝟏
𝝆𝒗𝒙
𝝆𝒗𝒚
𝝆𝒙𝒗
𝟏
𝟎
𝝆𝒚𝒗𝟎
𝟏
𝒙
𝒚
< 𝒗, 𝒙, 𝒚>
𝒗
𝒙
𝒚
• Consider 𝒙 and 𝒚 distributions (uniform) along with 𝒗 
Spatial Distributions
MV Data Summaries

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Create statistical realizations of the scalar fields from the multivariate data 
summaries
• Utilize the spatial information to reconstruct the scalar field by computing 
local particle density estimate for the grid locations
• The sample scalar field can be generated in arbitrary user-specified grid 
resolution
Multivariate Sampling For Reconstruction

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Combustion
(mixfrac)
Isabel
(pressure)
Raw
Copula-based Reconstruction
Multivariate Sampling-based Visualization
CoDDA: A Flexible Copula-based Distribution Driven Analysis Framework for Large-Scale Multivariate Data

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Preserving Correlations
Original var 1
Original var 2
Original 
scatter plot
Copula-based
MV Histogram-based

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Query-driven methods are a class of highly effective visualization 
strategies
• Analysis tasks can be targeted only for the queried regions
• Selectively sample only from distributions which satisfy the user query
Probabilistic Query-driven Analysis
0.3 < 𝑀𝑖𝑥𝑓𝑟𝑎𝑐< 0.7 𝑨𝑵𝑫 𝑦!" > 0.0006
𝑷(0.3 < 𝑀𝑖𝑥𝑓𝑟𝑎𝑐< 0.7 𝑨𝑵𝑫 𝑦!" > 0.0006)
CoDDA: A Flexible Copula-based Distribution Driven Analysis Framework for Large-Scale Multivariate Data

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Query-driven methods are a class of highly effective visualization 
strategies
• Analysis tasks can be targeted only for the queried regions
• Selectively sample only from distributions which satisfy the user query
−2000 < 𝑃𝑟𝑒𝑠𝑠𝑢𝑟𝑒< 500 𝑨𝑵𝑫 40 <  𝑉𝑒𝑙𝑜𝑐𝑖𝑡𝑦< 50
𝑷(−2000 < 𝑃𝑟𝑒𝑠𝑠𝑢𝑟𝑒< 500 𝑨𝑵𝑫 40 <  𝑉𝑒𝑙𝑜𝑐𝑖𝑡𝑦< 50)
Probabilistic Query-driven Analysis
CoDDA: A Flexible Copula-based Distribution Driven Analysis Framework for Large-Scale Multivariate Data

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Performance and Storage
CoDDA: A Flexible Copula-based Distribution Driven Analysis Framework for Large-Scale Multivariate Data
• Copula-based modeling + hybrid distribution-based summarization
• 496.8 GB raw data could be reduced down to 19.8GB distribution-
based data

## Figures

### Page 1

![Page 1](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_001.png)

### Page 2

![Page 2](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_002.png)

### Page 3

![Page 3](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_003.png)

### Page 4

![Page 4](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_004.png)

### Page 5

![Page 5](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_005.png)

### Page 6

![Page 6](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_006.png)

### Page 7

![Page 7](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_007.png)

### Page 8

![Page 8](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_008.png)

### Page 9

![Page 9](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_009.png)

### Page 10

![Page 10](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_010.png)

### Page 11

![Page 11](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_011.png)

### Page 12

![Page 12](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_012.png)

### Page 13

![Page 13](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_013.png)

### Page 14

![Page 14](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_014.png)

### Page 15

![Page 15](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_015.png)

### Page 16

![Page 16](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_016.png)

### Page 17

![Page 17](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_017.png)

### Page 18

![Page 18](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_018.png)

### Page 19

![Page 19](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_019.png)

### Page 20

![Page 20](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_020.png)

### Page 21

![Page 21](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_021.png)

### Page 22

![Page 22](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_022.png)

### Page 23

![Page 23](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_023.png)

### Page 24

![Page 24](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_024.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_002.png)

### embedded_003

![embedded_003](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_003.png)

### embedded_004

![embedded_004](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_004.png)

### embedded_005

![embedded_005](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_005.png)

### embedded_006

![embedded_006](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_006.png)

### embedded_007

![embedded_007](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_007.png)

### embedded_008

![embedded_008](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_009.png)

### embedded_010

![embedded_010](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_010.png)

### embedded_011

![embedded_011](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_011.png)

### embedded_012

![embedded_012](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_012.png)

### embedded_013

![embedded_013](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_013.png)

### embedded_014

![embedded_014](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_014.png)

### embedded_015

![embedded_015](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_017.png)

### embedded_018

![embedded_018](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_023.jpg)

### embedded_024

![embedded_024](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_024.jpg)

### embedded_025

![embedded_025](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_026.jpg)

### embedded_027

![embedded_027](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_028.jpg)

### embedded_029

![embedded_029](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_029.png)

### embedded_030

![embedded_030](assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_030.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_002.png` | 2 |
| Page 3 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_003.png` | 3 |
| Page 4 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_004.png` | 4 |
| Page 5 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_005.png` | 5 |
| Page 6 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_006.png` | 6 |
| Page 7 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_007.png` | 7 |
| Page 8 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_008.png` | 8 |
| Page 9 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_009.png` | 9 |
| Page 10 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_010.png` | 10 |
| Page 11 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_011.png` | 11 |
| Page 12 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_012.png` | 12 |
| Page 13 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_013.png` | 13 |
| Page 14 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_014.png` | 14 |
| Page 15 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_015.png` | 15 |
| Page 16 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_016.png` | 16 |
| Page 17 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_017.png` | 17 |
| Page 18 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_018.png` | 18 |
| Page 19 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_019.png` | 19 |
| Page 20 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_020.png` | 20 |
| Page 21 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_021.png` | 21 |
| Page 22 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_022.png` | 22 |
| Page 23 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_023.png` | 23 |
| Page 24 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/page_024.png` | 24 |
| embedded_001 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_002.png` | Embedded raster image |
| embedded_003 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_003.png` | Embedded raster image |
| embedded_004 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_004.png` | Embedded raster image |
| embedded_005 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_005.png` | Embedded raster image |
| embedded_006 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_006.png` | Embedded raster image |
| embedded_007 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_007.png` | Embedded raster image |
| embedded_008 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_009.png` | Embedded raster image |
| embedded_010 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_010.png` | Embedded raster image |
| embedded_011 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_011.png` | Embedded raster image |
| embedded_012 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_012.png` | Embedded raster image |
| embedded_013 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_013.png` | Embedded raster image |
| embedded_014 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_014.png` | Embedded raster image |
| embedded_015 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_017.png` | Embedded raster image |
| embedded_018 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_023.jpg` | Embedded raster image |
| embedded_024 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_024.jpg` | Embedded raster image |
| embedded_025 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_026.jpg` | Embedded raster image |
| embedded_027 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_028.jpg` | Embedded raster image |
| embedded_029 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_029.png` | Embedded raster image |
| embedded_030 | `assets/Lecture16_Multivar_dist_4624473d-2c8b-4faa-a992-411f265ab072/embedded_030.jpg` | Embedded raster image |

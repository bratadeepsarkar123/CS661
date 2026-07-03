---
title: "Lecture11 HighDimVis (Part 2)"
source_pdf: "markdown_files/lecture pdf/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf.pdf"
converted: 2026-07-07
pages: 24
---

# Lecture11 HighDimVis (Part 2)

**Source:** `markdown_files/lecture pdf/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf.pdf`  
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
Study Materials for Lecture 11
• Visualizing High-Dimensional Data: Advances in the Past Decade; S. 
Liu et al., TVCG2016
• t-SNE: https://distill.pub/2016/misread-tsne/
• UMAP: https://pair-code.github.io/understanding-umap/

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Acknowledgements
• Some of the following slides are adapted from the excellent course 
materials and tutorials made available by:
• Prof. Klaus Mueller (State University of New York at Stony Brook)
• Prof. Tamara Munzner (University of British Columbia)
• Zaur Fataliyev (Research Scientist – Meta)
• Andreas Kollegger (neo4j)

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Final Project Group Formation
• Form your project team by June 20th and update the google sheet 
with details of project members
• https://docs.google.com/spreadsheets/d/17JwSTvZNrZI1waj1ZZDyZaIVwMGk
Y2fR9SQ_6fzlclo/edit?usp=sharing
• Group size: 7/8/9 (8 is preferred) 
• Submit your project proposal by June 23rd in HelloIITK
• Once I approve your proposal, start working on it!
• If I see your work is trivial, insufficient, and does not meet the quality 
bar during the final presentation, you will not get a good grade for the 
project
• So, if you are in doubt, talk to me as you work on the project!

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Final Class Project: What is Expected?
• You will build a visual-analytics interface/software to solve a problem 
from an application domain
• You are expected to have knowledge about your domain of 
application and the tasks you have picked must reflect that
• Your tasks should be meaningful, and you should be able to explain 
why you are doing something
• You should be able to tell a coherent story about your data through 
your visualization interface
• Random set of plots will not help
• You need to justify why you picked certain type of plots

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Final Class Project: What is Expected?
• You are expected to show meaningful patterns from your data 
through your interface
• Since this is a visualization focused course, so even if you do a very 
sophisticated modeling, your visualization interface still should be the 
main focus for grading
• How you are presenting your results will matter
• You are expected to write a comprehensive report of your work that 
describes the details of the methodologies and visualization 
techniques that you have used
• You should justify your design choices for your interface
• Such as: Why a bar chart and not a Pie chart!

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Final Class Project: How Will It be Graded?
• Grading will be done on your overall idea + quality of work, 
presentation, and report
• Total marks: 300
• Overall quality: 100 (group)
• Presentation + Q&A: 100 (individually graded)
• Report: 100 (group)
• Each group member should be present during final presentation and 
participate in the presentation 
• Schedule of presentations will be shared later
• Guidelines for submitting code and report will be shared later

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dimensionality Reduction Techniques
• Principal Component Analysis (PCA)
• Linear Discriminant Analysis (LDA)
Linear methods
• t-Distributed Stochastic Neighbor Embedding (t-SNE)
• Uniform Manifold Approximation and Projection (UMAP)
• Multidimensional Scaling (MDS)
• ISOMAP
• Locally linear embedding (LLE)
• Laplacian Eigenmap (LE)
Non-linear methods

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dimensionality Reduction Techniques
• Principal Component Analysis (PCA)
• Linear Discriminant Analysis (LDA)
Linear methods
• t-Distributed Stochastic Neighbor Embedding (t-SNE)
• Uniform Manifold Approximation and Projection (UMAP)
• Multidimensional Scaling (MDS)
• ISOMAP
• Locally linear embedding (LLE)
• Laplacian Eigenmap (LE)
Non-linear methods

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Principal Component Analysis (PCA)
• Unsupervised technique for extracting variance structure from high 
dimensional data to represent data in a lower dimensional space 
• An orthogonal (linear) projection of the data into a subspace so that the 
variance of the projected data is maximized
• Useful for:
• Visualization
• Further processing by machine learning algorithms
• More efficient use of resources (e.g., time, memory, space)
• In general: fewer dimensions à better generalization and modeling

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Principal Component Analysis
• A linear transformation that chooses a new coordinate system for the 
data such that greatest variance by any projection of the data comes 
to lie on the first axis (first principal component), the second greatest 
variance on the second axis, and so on….
• How to reduce data dimension with PCA? 
• Principal components are sorted in the order of their “explained 
variance” in the data
• Eliminating later principal components allow dimension reduction

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Principal Component Analysis
2D Example data set
https://stats.stackexchange.com/questions/2691/making-sense-of-principal-component-analysis-eigenvectors-eigenvalues/140579

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Principal Component Analysis
Animated view of how PCA works conceptually
https://stats.stackexchange.com/questions/2691/making-sense-of-principal-component-analysis-eigenvectors-eigenvalues/140579

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Steps of PCA Algorithm 
• Suppose we have a dataset with n records and m features for each 
record, i.e., data has n rows and m columns
1. Standardize the data:
2. Calculate the covariance matrix of the standardized data matrix
3. Calculate the eigen decomposition of the covariance matrix
• Results in a list of eigenvalues and a list of eigenvectors
4. Sort eigenvalues in descending order to get a ranking for the 
eigenvectors (principal components) or axes of the new subspace

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How to Project Data into a Lower Dimension?
• A total of k components (k < m) can be 
selected to create a projection 
subspace.
• The k eigenvectors are called principal 
components, that have the k largest 
eigenvalues
• Data can be projected into the k-
dimensional subspace via matrix 
multiplication
https://programmathically.com/principal-components-analysis-explained-for-dummies/

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
PCA: Explained Variance
• Explained variance is a statistical measure of how much variance in a 
dataset can be attributed to each of the principal components 
• How much of the total variance is “explained” by each component
• Ordered (large to small) eigenvalues can help
• Explained variance for ith principal component:
: ith eigen value of covariance matrix

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization of Data using PCA
• Wine data set
• 178 records, 13 features for each record
https://archive.ics.uci.edu/ml/datasets/wine

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization of Data using PCA
• Scatter plot for selected pairwise features (attributes)

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization of Data using PCA
• Scatter plot for selected pairwise features (attributes)
• Color points by class label

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization of Data using PCA
• Scatter plot using two first principal components as axes after 
PCA is applied
PC1
PC2
PC1
PC2
PCA with no standardization
PCA with standardization

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visualization of Data using PCA
• Scatter plot using two first principal components as axes after 
PCA is applied
• Color points by class label
PC1
PC2
PC1
PC2
PCA with no standardization
PCA with standardization

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
PCA on MNIST data

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
PCA on MNIST data
PC1
PC2

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
PCA on MNIST data
PCA is not able 
to separate 
classes clearly
PC1
PC2

## Figures

### Page 1

![Page 1](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_001.png)

### Page 2

![Page 2](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_002.png)

### Page 3

![Page 3](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_003.png)

### Page 4

![Page 4](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_004.png)

### Page 5

![Page 5](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_005.png)

### Page 6

![Page 6](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_006.png)

### Page 7

![Page 7](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_007.png)

### Page 8

![Page 8](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_008.png)

### Page 9

![Page 9](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_009.png)

### Page 10

![Page 10](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_010.png)

### Page 11

![Page 11](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_011.png)

### Page 12

![Page 12](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_012.png)

### Page 13

![Page 13](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_013.png)

### Page 14

![Page 14](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_014.png)

### Page 15

![Page 15](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_015.png)

### Page 16

![Page 16](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_016.png)

### Page 17

![Page 17](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_017.png)

### Page 18

![Page 18](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_018.png)

### Page 19

![Page 19](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_019.png)

### Page 20

![Page 20](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_020.png)

### Page 21

![Page 21](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_021.png)

### Page 22

![Page 22](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_022.png)

### Page 23

![Page 23](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_023.png)

### Page 24

![Page 24](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_024.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_002.png)

### embedded_003

![embedded_003](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_003.png)

### embedded_004

![embedded_004](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_005.png)

### embedded_006

![embedded_006](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_007.png)

### embedded_008

![embedded_008](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_008.png)

### embedded_009

![embedded_009](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_009.png)

### embedded_010

![embedded_010](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_010.png)

### embedded_011

![embedded_011](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_011.png)

### embedded_012

![embedded_012](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_012.png)

### embedded_013

![embedded_013](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_013.png)

### embedded_014

![embedded_014](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_014.png)

### embedded_015

![embedded_015](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_015.png)

### embedded_016

![embedded_016](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_016.png)

### embedded_017

![embedded_017](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_017.png)

### embedded_018

![embedded_018](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_018.png)

### embedded_019

![embedded_019](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_019.png)

### embedded_020

![embedded_020](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_020.png)

### embedded_021

![embedded_021](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_023.png)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_002.png` | 2 |
| Page 3 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_003.png` | 3 |
| Page 4 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_004.png` | 4 |
| Page 5 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_005.png` | 5 |
| Page 6 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_006.png` | 6 |
| Page 7 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_007.png` | 7 |
| Page 8 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_008.png` | 8 |
| Page 9 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_009.png` | 9 |
| Page 10 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_010.png` | 10 |
| Page 11 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_011.png` | 11 |
| Page 12 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_012.png` | 12 |
| Page 13 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_013.png` | 13 |
| Page 14 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_014.png` | 14 |
| Page 15 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_015.png` | 15 |
| Page 16 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_016.png` | 16 |
| Page 17 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_017.png` | 17 |
| Page 18 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_018.png` | 18 |
| Page 19 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_019.png` | 19 |
| Page 20 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_020.png` | 20 |
| Page 21 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_021.png` | 21 |
| Page 22 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_022.png` | 22 |
| Page 23 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_023.png` | 23 |
| Page 24 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/page_024.png` | 24 |
| embedded_001 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_002.png` | Embedded raster image |
| embedded_003 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_003.png` | Embedded raster image |
| embedded_004 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_005.png` | Embedded raster image |
| embedded_006 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_007.png` | Embedded raster image |
| embedded_008 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_008.png` | Embedded raster image |
| embedded_009 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_009.png` | Embedded raster image |
| embedded_010 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_010.png` | Embedded raster image |
| embedded_011 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_011.png` | Embedded raster image |
| embedded_012 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_012.png` | Embedded raster image |
| embedded_013 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_013.png` | Embedded raster image |
| embedded_014 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_014.png` | Embedded raster image |
| embedded_015 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_015.png` | Embedded raster image |
| embedded_016 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_016.png` | Embedded raster image |
| embedded_017 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_017.png` | Embedded raster image |
| embedded_018 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_018.png` | Embedded raster image |
| embedded_019 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_019.png` | Embedded raster image |
| embedded_020 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_020.png` | Embedded raster image |
| embedded_021 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture11_HighDimVis_part_2_102cc91f-a90b-49c9-95f4-1bd27625f1bf/embedded_023.png` | Embedded raster image |

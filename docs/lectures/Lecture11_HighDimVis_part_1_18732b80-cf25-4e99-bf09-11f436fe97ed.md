---
title: "Lecture11 HighDimVis (Part 1)"
source_pdf: "markdown_files/lecture pdf/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed.pdf"
converted: 2026-07-07
pages: 16
---

# Lecture11 HighDimVis (Part 1)

**Source:** `markdown_files/lecture pdf/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed.pdf`  
**Converted:** 2026-07-07  
**Pages:** 16

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
• Zaur Fataliyev  (Research Scientist – Meta)
• Andreas Kollegger (neo4j)

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
High Dimensional Data
• In statistics, high dimensional data is a data where the number of 
attributes (features) are larger than the number of samples
• In practice, often, when a data set has large number of attributes, it is 
also referred to as high dimensional data
• Examples: biological data, gene expression data, social media user data, 
network data, etc.
Tabular data
Microarray data
Graph data

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Intuition: Why High-Dimensional Data Can Be A 
Problem?
• Imagine a situation in which the number of observations and features 
in a dataset are almost equal
• Effective number of observations per features is low
• Result: Models (Statistical or ML) can overfit and so less generalizable
High dim. data, 
overfitting in regression

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Understanding High-Dimensional Objects
• Feature vectors are typically high 
dimensional 
• We do not understand such vectors 
well – why?
• Because we don’t learn to 
see/perceive high-dim objects when 
our vision system develops
• We only perceive 3D world!
Fig source: Wikipedia
3D projection of a 4D cube

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Curse of Dimensionality
• A phenomenon related with high dimensional data
• Challenging to identify meaningful patterns while analyzing and visualizing 
the data
• With increasing dimensionality, the volume of the space increases 
rapidly, making the data sparse in high dimension
• To obtain a reliable result, the amount of data needed often grows 
exponentially with the dimensionality
• Distance computation between objects in high dimensional space 
becomes difficult

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Sparseness in High Dimensional Space
• Space gets extremely sparse
• with every extra dimension points get pulled apart further 
• distances become meaningless

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Space and Memory Management
• Indexing (and storage) gets very expensive with increasing 
dimensionality
• Exponential growth in the number of dimensions

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Space and Memory Management
• Indexing (and storage) gets very expensive with increasing 
dimensionality
• Exponential growth in the number of dimensions

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Space and Memory Management
• Indexing (and storage) gets very expensive with increasing 
dimensionality
• Exponential growth in the number of dimensions

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Space and Memory Management
• Indexing (and storage) gets very expensive with increasing 
dimensionality
• Exponential growth in the number of dimensions

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Space and Memory Management
• Indexing (and storage) gets very expensive with increasing 
dimensionality
• Exponential growth in the number of dimensions 
• 4D: 65k cells 5D: 1M cells 6D: 16M cells 7D: 268M cells

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
High Dimension: In Machine Learning
• Hughes’ Phenomenon: With a fixed number of training samples, the 
average (expected) predictive power of a classifier or regressor first 
increases as the number of dimensions or features used is increased 
but beyond a certain dimensionality it starts deteriorating instead of 
improving steadily
https://builtin.com/data-science/curse-dimensionality

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
High Dimensional Data Analysis and Visualization
Visualizing High-Dimensional Data: Advances in the Past Decade 
Visualizing High-Dimensional Data: Advances in the Past Decade

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dimensionality Reduction: Why?
• Produce embedding of high dimensional data into low 
dimensional space
• Visual analysis of high dimensional data
• Useful for feature engineering in ML techniques
• Helps in finding redundant features from large scale data

## Figures

### Page 1

![Page 1](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_001.png)

### Page 2

![Page 2](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_002.png)

### Page 3

![Page 3](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_003.png)

### Page 4

![Page 4](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_004.png)

### Page 5

![Page 5](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_005.png)

### Page 6

![Page 6](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_006.png)

### Page 7

![Page 7](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_007.png)

### Page 8

![Page 8](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_008.png)

### Page 9

![Page 9](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_009.png)

### Page 10

![Page 10](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_010.png)

### Page 11

![Page 11](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_011.png)

### Page 12

![Page 12](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_012.png)

### Page 13

![Page 13](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_013.png)

### Page 14

![Page 14](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_014.png)

### Page 15

![Page 15](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_015.png)

### Page 16

![Page 16](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_016.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_002.png)

### embedded_003

![embedded_003](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_009.png)

### embedded_010

![embedded_010](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_014.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_002.png` | 2 |
| Page 3 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_003.png` | 3 |
| Page 4 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_004.png` | 4 |
| Page 5 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_005.png` | 5 |
| Page 6 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_006.png` | 6 |
| Page 7 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_007.png` | 7 |
| Page 8 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_008.png` | 8 |
| Page 9 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_009.png` | 9 |
| Page 10 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_010.png` | 10 |
| Page 11 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_011.png` | 11 |
| Page 12 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_012.png` | 12 |
| Page 13 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_013.png` | 13 |
| Page 14 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_014.png` | 14 |
| Page 15 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_015.png` | 15 |
| Page 16 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/page_016.png` | 16 |
| embedded_001 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_002.png` | Embedded raster image |
| embedded_003 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_009.png` | Embedded raster image |
| embedded_010 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture11_HighDimVis_part_1_18732b80-cf25-4e99-bf09-11f436fe97ed/embedded_014.jpg` | Embedded raster image |

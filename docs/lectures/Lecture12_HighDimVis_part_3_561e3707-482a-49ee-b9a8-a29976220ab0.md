---
title: "Lecture12 HighDimVis (Part 3)"
source_pdf: "markdown_files/lecture pdf/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0.pdf"
converted: 2026-07-07
pages: 29
---

# Lecture12 HighDimVis (Part 3)

**Source:** `markdown_files/lecture pdf/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0.pdf`  
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
• Prof. Klaus Mueller (State University of New York at Stony Brook)
• Prof. Tamara Munzner (University of British Columbia)
• Zaur Fataliyev  (Research Scientist – Meta)

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Study Materials for Lecture 12
• Visualizing High-Dimensional Data: Advances in the Past Decade; S. 
Liu et al., TVCG2016
• t-SNE: https://distill.pub/2016/misread-tsne/
• UMAP: https://pair-code.github.io/understanding-umap/
• Footnotes in slides

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-Distributed Stochastic Neighbor Embedding (t-SNE)
• PCA is not always effective in finding patterns in low dimensional 
projected space
• It is a linear algorithm, meaning that it cannot represent complex nonlinear 
relationship between features
• t-Distributed Stochastic Neighbor Embedding: A nonlinear 
dimensionality reduction technique
• t-SNE is specifically designed for high dimensional data visualization 
purposes
• Paper: https://jmlr.org/papers/v9/vandermaaten08a.html
• ~51,000 citations!!

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-SNE : Underlying Idea
Measure pairwise distances between high dimensional and low 
dimensional points
https://medium.com/

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-SNE : Underlying Idea
Original high-dim. data 
Probability table 
(for high-dim. points)
Low-dim. data 
Probability table 
(for low-dim. points)
Make these two as 
close as possible by 
moving low-dim. data
KL divergence
(minimize)
(Fixed)
(Adjustable)
creates similarity 
probabilities based 
on Gaussian 
distribution 
Creates similarity 
probabilities based 
on Student’s 
t-distribution

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-SNE : Underlying Idea
High Dim data
Similarity Probability 
table in high dimension
StatQuest

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-SNE : Underlying Idea
High Dim data
Similarity Probability 
table in high dimension
Initial Similarity 
Probability table in low 
dimension
Low Dim data
StatQuest

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-SNE : Underlying Idea
High Dim data
Similarity Probability 
table in high dimension
Final Similarity 
Probability table in low 
dimension
Low Dim data
StatQuest

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-SNE: Measure Distances and Optimize
• Similarity of datapoints in high dimensional space
KL Divergence: Kullback–Leibler 
divergence is a measure of how 
one probability distribution P is 
different from a second, 
reference probability 
distribution Q 
• Similarity of datapoints in low dimensional space
• Cost function: Minimize KL Divergence

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
What is the t in the t-SNE ?
• To measure distance between points in the low dimensional space, a 
student’s t-distribution is used instead of a Gaussian distribution
Blue: Gaussian distribution
Red: t-Distribution
• The student’s t-distribution has a heavier tail 
compared to the Gaussian distribution

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Why t-distribution? Crowding Problem
• Goal is to preserve local structure in low 
dimensional embedding
• Points which are far apart in high dimensional 
space should be far apart after projection
• The heavy tailed t-distribution helps to 
achieve it
High dim
Low dim
t-SNE

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Execution of t-SNE on MNIST Data
https://colah.github.io/posts/2014-10-Visualizing-MNIST/

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
t-SNE on MNIST Data

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How to use t-SNE Effectively
• A key hyperparameter is perplexity
• It is a parameter that determines how to balance attention between 
local and global structures
• Intuition:  A guess about the number of close neighbors each point 
has that should be preserved
• Changing this parameter has significant impact on final layout
https://distill.pub/2016/misread-tsne/

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Impact of Perplexity in t-SNE
https://distill.pub/2016/misread-tsne/

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Impact of Epsilon (#iterations) in t-SNE
https://distill.pub/2016/misread-tsne/

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Other Key Aspects of t-SNE
https://distill.pub/2016/misread-tsne/
• Cluster sizes in a t-SNE plot may mean nothing
• Distances between clusters might not mean anything
• Random noise doesn’t always look random
• For topology, you need more than one plot at different perplexity 
values
• Try with different number of iterations to ensure the algorithm has 
converged

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Excellent Online Resource for Learning t-SNE
• https://distill.pub/2016/misread-tsne/
https://distill.pub/2016/misread-tsne/

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Uniform Manifold Approximation and Projection (UMAP)
• A dimensionality reduction technique that assumes the available data 
samples are locally connected and locally (uniformly) distributed 
across a topological space (manifold), which can be approximated 
from these finite data samples and mapped (projected) to a lower-
dimensional space.
• Key steps:
• Learning the manifold structure in the high-dimensional space
• Finding a low-dimensional representation of the high dim. manifold
• Idea: Given the high dimensional graph structure, UMAP projects the 
data into lower dimensions via a force-directed graph layout algorithm
• Paper: https://arxiv.org/abs/1802.03426
• ~15,000 citations!!

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Simplex and Simplicial Complex
• A simplicial complex is a set composed of 
points, line segments, triangles, and their n-
dimensional counterparts 
• A simplex is a generalization of the notion of a triangle or tetrahedron 
to arbitrary dimensions
wikipedia

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
UMAP
• Conceptually very similar to t-SNE
• Construct a high dimensional graph representation of the data
• Optimizes a low-dimensional graph to be as structurally similar as possible
• Idea behind constructing the high dimensional graph
• Build a ‘fuzzy simplicial complex’
• A weighted graph where edge weights represent likelihood that two points are 
connected
• Connectedness: Grow a radius outward from each point and when it overlaps 
with a neighbor, connect the points
• Then make the graph "fuzzy" by decreasing the likelihood of connection as 
the radius grows outward
• Each point must be connected to at least its closest neighbor to capture local 
structure
https://pair-code.github.io/understanding-umap/

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
UMAP: High Dimensional Graph Construction
https://pair-code.github.io/understanding-umap/

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Two Important Parameters of UMAP
• Number of nearest neighbors
• the number of approximate nearest neighbors used to construct the initial 
high-dimensional graph
• Minimum distance
• the minimum distance between points in low-dimensional space controls how 
tightly UMAP clumps points together
• Low values leading to more tightly packed embeddings
• Larger values will make UMAP pack points together more loosely, focusing 
instead on the preservation of the broad topological structure
https://pair-code.github.io/understanding-umap/

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Two Important Parameters of UMAP
https://pair-code.github.io/understanding-umap/

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
UMAP vs t-SNE

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
UMAP vs t-SNE
Fashion MNIST Data

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Comments to both t-SNE and UMAP Methods
• Hyperparameters really matter!
• Cluster sizes may mean nothing
• Distances between clusters might not mean anything
• You may need more than one plot
• Random noise doesn’t always look random

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Comparative Study & Performance
MNIST dataset (downsampled to 2000 points)
PCA: 0.82 sec
LLE: 260 sec
Isomap: 280 sec
t-SNE: 250 sec
UMAP: 44 sec

## Figures

### Page 1

![Page 1](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_001.png)

### Page 2

![Page 2](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_002.png)

### Page 3

![Page 3](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_003.png)

### Page 4

![Page 4](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_004.png)

### Page 5

![Page 5](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_005.png)

### Page 6

![Page 6](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_006.png)

### Page 7

![Page 7](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_007.png)

### Page 8

![Page 8](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_008.png)

### Page 9

![Page 9](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_009.png)

### Page 10

![Page 10](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_010.png)

### Page 11

![Page 11](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_011.png)

### Page 12

![Page 12](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_012.png)

### Page 13

![Page 13](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_013.png)

### Page 14

![Page 14](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_014.png)

### Page 15

![Page 15](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_015.png)

### Page 16

![Page 16](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_016.png)

### Page 17

![Page 17](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_017.png)

### Page 18

![Page 18](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_018.png)

### Page 19

![Page 19](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_019.png)

### Page 20

![Page 20](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_020.png)

### Page 21

![Page 21](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_021.png)

### Page 22

![Page 22](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_022.png)

### Page 23

![Page 23](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_023.png)

### Page 24

![Page 24](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_024.png)

### Page 25

![Page 25](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_025.png)

### Page 26

![Page 26](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_026.png)

### Page 27

![Page 27](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_027.png)

### Page 28

![Page 28](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_028.png)

### Page 29

![Page 29](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_029.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_013.png)

### embedded_014

![embedded_014](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_014.png)

### embedded_015

![embedded_015](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_021.png)

### embedded_022

![embedded_022](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_023.png)

### embedded_024

![embedded_024](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_024.png)

### embedded_025

![embedded_025](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_026.jpg)

### embedded_027

![embedded_027](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_028.jpg)

### embedded_029

![embedded_029](assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_029.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_002.png` | 2 |
| Page 3 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_003.png` | 3 |
| Page 4 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_004.png` | 4 |
| Page 5 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_005.png` | 5 |
| Page 6 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_006.png` | 6 |
| Page 7 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_007.png` | 7 |
| Page 8 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_008.png` | 8 |
| Page 9 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_009.png` | 9 |
| Page 10 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_010.png` | 10 |
| Page 11 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_011.png` | 11 |
| Page 12 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_012.png` | 12 |
| Page 13 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_013.png` | 13 |
| Page 14 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_014.png` | 14 |
| Page 15 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_015.png` | 15 |
| Page 16 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_016.png` | 16 |
| Page 17 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_017.png` | 17 |
| Page 18 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_018.png` | 18 |
| Page 19 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_019.png` | 19 |
| Page 20 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_020.png` | 20 |
| Page 21 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_021.png` | 21 |
| Page 22 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_022.png` | 22 |
| Page 23 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_023.png` | 23 |
| Page 24 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_024.png` | 24 |
| Page 25 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_025.png` | 25 |
| Page 26 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_026.png` | 26 |
| Page 27 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_027.png` | 27 |
| Page 28 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_028.png` | 28 |
| Page 29 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/page_029.png` | 29 |
| embedded_001 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_013.png` | Embedded raster image |
| embedded_014 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_014.png` | Embedded raster image |
| embedded_015 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_021.png` | Embedded raster image |
| embedded_022 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_023.png` | Embedded raster image |
| embedded_024 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_024.png` | Embedded raster image |
| embedded_025 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_026.jpg` | Embedded raster image |
| embedded_027 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_028.jpg` | Embedded raster image |
| embedded_029 | `assets/Lecture12_HighDimVis_part_3_561e3707-482a-49ee-b9a8-a29976220ab0/embedded_029.jpg` | Embedded raster image |

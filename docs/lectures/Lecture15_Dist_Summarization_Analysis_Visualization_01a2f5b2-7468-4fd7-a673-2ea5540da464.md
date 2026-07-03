---
title: "Lecture15 Dist Summarization Analysis Visualization"
source_pdf: "markdown_files/lecture pdf/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464.pdf"
converted: 2026-07-07
pages: 35
---

# Lecture15 Dist Summarization Analysis Visualization

**Source:** `markdown_files/lecture pdf/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464.pdf`  
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
Study Materials for Lecture 15
• SLIC Superpixels Compared to State-of-the-Art Superpixel Methods, Achanta et al.
• Homogeneity guided probabilistic data summaries for analysis and visualization 
of large-scale data sets, Dutta et al. IEEE PacificVis.
• Statistical visualization and analysis of large data using a value-based spatial 
distribution, Wang et al., IEEE PacificVis.
• Distribution Driven Extraction and Tracking of Features for Time-varying Data 
Analysis, Dutta et al., IEEE TVCG.

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distribution-based Large 
Data Summarization and 
Visualization

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distribution Models for Big Data Summarization
• Distribution models that can be estimated efficiently and has a 
compact memory footprint is preferred over other models
• For Univariate Data:
• Histograms: Fast but takes more space
• KDE: Computationally expensive and takes more space
• Gaussian: Fast but often the model is too simple
• Gaussian mixture model: Parameter estimation can be a little expensive, but 
representation is compact
• For Multivariate Data:
• Many of the standard multivariate models become either slow or space 
inefficient
• Statistical Copula functions can be used effectively

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distribution-based Data Summarization 
Strategies
Global distribution model: A single distribution model to 
represent the entire data set
•
Significant data reduction is possible
•
Coarse representation of the data
•
Not suitable for fine grained visual analysis

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distribution-based Data Summarization 
Strategies
Global distribution model: A single distribution model to 
represent the entire data set
•
Significant data reduction is possible
•
Coarse representation of the data
•
Not suitable for fine grained visual analysis
Local distribution model: Data is divided into small blocks 
and then each block is summarized using a separate 
distribution model
•
Data reduction at an acceptable range is possible
•
Fine details of the data and statistical properties are 
preserved
•
Preferred over global model for scientific data 
summarization

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Local/Region-wise Distribution-based Data 
Modeling
• Local Statistical distribution-based data 
modeling
• Partition data into local regions
• Summarize each region with a statistical 
distribution model
• Benefits:
• Distributions preserve local statistical data 
properties
• Reduce data size significantly
• Enables sampling-based analysis and reconstruction
• Allows uncertainty quantification
Local distribution-based data model

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Goals of a Region-wise Statistical Summarization
• Produce coherent partitions
• Similar data values are grouped together
• Partitions are spatially contiguous
• Preserve the statistical properties of 
the data accurately
• Minimize sampling errors
• Efficient feature analysis
• Use appropriate distribution models 
for summarization
• A compact storage representation

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Produce coherent partitions
• Similar data values are grouped together
• Partitions are spatially contiguous
• Preserve the statistical properties of 
the data accurately
• Minimize sampling errors
• Efficient feature analysis
• Use appropriate distribution models 
for summarization
• A compact storage representation
Goals of a Region-wise Statistical Summarization

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
A Superior Solution for Region-wise Statistical 
Summarization
• Generate partitions based on data 
homogeneity
• Simple Linear Iterative Clustering (SLIC)
• Produces irregular shaped partitions/clusters
• Value variation inside partitions is minimized 
• Reduced sampling error
s
2s
SLIC concept
!
" # $
% &&
&&
"'
$% &
&
!
"
!
"
#!$% ! "
C
'
()*
()*
α
α
=
−
+
−
−
https://www.iro.umontreal.ca/~mignotte/IFT6150/Articles/SLIC_Superpixels.pdf

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
SLIC Partitioning and Distribution Modeling
• Generate partitions based on data 
homogeneity
• Summarize each partition using a 
hybrid distribution scheme 
• A single Gaussian or a mixture of Gaussians
• Reduce data size and a compact representation

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
SLIC Partitioning and Distribution Modeling
Raw Data
SLIC Partitioned Data
Distribution based 
Modeling

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Hybrid Distribution-based Summarization
• Each SLIC partition is summarized using 
• Either a single Gaussian or a mixture of 
Gaussians (GMM)
• The decision is made based on a Normality test
• Expectation Maximization (EM) for 
GMM parameter estimation
• A hybrid distribution-based data set
• Compact statistical representation
• Significantly smaller than the raw data
SLIC 
partition
Normality 
test
Summarize 
with a GMM
Summarize 
with single 
Gaussian
Yes
No

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Spatial Distribution-augmented Statistical Data 
Summarization

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Value Estimation
(Bayes’ Rule)
Value estimation 
(PDF) at location, ℓ
Block Histogram
Spatial Distribution
(GMM)
Data Modeling
(A Local Block)
Partition 
Raw Data
Any 
spatial location
(ℓ )
Statistical Visualizations 
from PDFs
Spatial Distribution-augmented Statistical Data 
Summarization 
Slides adapted from Prof. Ko-Chih Wang

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Block histogram summarizes data samples in a block
• Bin 𝑏! represents a continuous data value range [𝐿"!, 𝑈"!]
• 𝐻𝑏! =
#("!)
∑"#$
%&' #("")       (normalized frequency of bin b')
• 𝑁(𝑏!): number of grid points whose values are in range 𝐿"!, 𝑈"!
Prob.
Data Value
Data of a block
Spatial Distribution-augmented Statistical Data 
Summarization 
Slides adapted from Prof. Ko-Chih Wang

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Block histogram does not retain samples’ location 
information
• Each bin attaches a spatial distribution: {𝑆!, 𝑆", … 𝑆#$"}
• 𝑆!! : maps a spatial location (ℓ) to a probability
• Estimated by a multivariate GMM (Spatial GMM)
• Spatial GMM modeling
• Collect coordinates of all grid points assigned to bin 𝑏" 
• Use EM algorithm to estimate the parameters of the GMM
• Repeat the process for each bin
EM Algorithm
Spatial Distribution-augmented Statistical Data 
Summarization 
Slides adapted from Prof. Ko-Chih Wang

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• The complexity of the spatial distribution of each bin are quite 
different
• Increases storage overhead if we use too many Gaussian components
• May have insufficient modeling quality if fewer Gaussian components  are 
used
• Use an adaptive scheme to determine the best number of Gaussian 
components
• Bayesian Information Criterion (BIC) evaluates the fitting quality
• Given an upper bound of number of Gaussian components
• The number of Gaussian components with the best (least) BIC is selected
Spatial Distribution-augmented Statistical Data 
Summarization 
Slides adapted from Prof. Ko-Chih Wang

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Bayesian Information Criterion (BIC)
• BIC is a criterion of model selection given different model 
configurations
• Lower values of BIC are preferred
• Tries to balance between the number of model parameters (model 
complexity) and how well the model fits the data
𝐵𝐼𝐶= 𝑘∗𝑙𝑛𝑛−2 ∗ln(𝐿)
• 𝐿 is the maximized value of likelihood function
• 𝑛 = sample size
• 𝑘 = number of model parameters

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• A probability density function (PDF) at a given 
location ℓ
• Possible values at ℓ and their associated probability
• Combine the histogram and spatial GMMs by Bayes’ 
rule
• Bayes’ rule 
• The prior is adjusted by the associated evidence
• 𝑃ℓ𝑏# =
$%&&"# ℓ∗(("#)
∑!$%
&'( $%&&"! ℓ∗(("!)
• Prior: block histogram
• Evidences: probabilities of spatial GMMs at ℓ 
• Posterior: estimated PDF at ℓ
Prob.
Prob.
Spatial Distribution-augmented Statistical Data 
Summarization: Value Estimation 
Slides adapted from Prof. Ko-Chih Wang

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data/Storage Reduction
• SLIC-based partitioning + hybrid modeling Technique
• 100 GB raw data could be reduced to 10.8 GB distribution-based 
data
• Reduced data needs only ~10% of the raw data storage
• Spatial GMM + value distribution-based modeling
• 10.61 GB raw data could be reduced to 0.152 GB distribution-
based data (323 block size)
• Reduced data needs only 1.39% of the raw data storage

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
What Can We Do With the Distribution-based 
Reduced Data?
• Reconstruct the full resolution data
• Bayes' Rule-based method of reconstruction using Spatial distribution models
• Monte Carlo sampling for SLIC-based hybrid distribution models
• Distribution-based feature search 
• Feature extraction and tracking
• Many more ……

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Box Muller Transform
• Box Muller Transform is used to generate pairwise independent 
Standard Normally distributed values
• Let U1 and U2 are independent samples chosen from a Uniform 
distribution defined over (0,1)
• Compute:
• We can show that Z0 and Z1 are coming from Standard Normal 
distributions

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Box Muller Transform for GMM
• Box Muller Transform gives us samples that follow Standard Normal 
distributions
• But we have Gaussian mixture models (GMM)
• So, apply the following steps to generate samples from a GMM:
• Generate a random number 𝑟 between 0 - 1
• Find the Gaussian component for which ∑( 𝑤𝑒𝑖𝑔ℎ𝑡𝑘≥𝑟
• Use Box Muller Transform to sample a value from the selected Gaussian 
component

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Monte Carlo Sampling-based Reconstruction
• Monte Carlo Sampling is used to reconstruct the full data from distribution models
• Box Muller Transform on GMM and Gaussians
• Regular partitioning is not optimal
• Does not consider inherent data coherency
Regular partitioning
High value variation in 
partition distributions
High sampling error in 
reconstructed data
Ground truth data

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Monte Carlo Sampling-based Reconstruction
• Generate partitions based on data homogeneity
• Simple Linear Iterative Clustering (SLIC)
• Produces irregular shaped partitions/clusters
• Value variation inside partitions is minimized 
• Reduced sampling error
Ground truth data
Smooth reconstruction 
using SLIC partitioning
Low value 
variation in 
partition 
distributions
SLIC partitioning

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Bayes’ Rule-based Method of Reconstruction using 
Spatial Distribution
Block histogram
Size: 131.4MB
Block Size: 22)
Block histogram w/ 
interpolation
Size: 131.4MB
Block Size: 22)
Block GMM
Size: 163.71MB
Block Size: 10)
Our approach
Size: 151.54MB
Block Size: 32)
Raw data
Size: 10871MB
Resolution: 2545x2545x440
Spatial Distribution

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Spatial Distribution
(100MB)
Bayes’ Rule-based Method of Reconstruction using 
Spatial Distribution

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distribution Similarity-based Feature Search 
Selection of feature
Feature distribution
to be searched
Regions with similar 
distributions for 
regular partitioning
Regions with similar 
distributions for K-d 
tree partitioning
Regions with similar 
distributions for SLIC 
partitioning
Selection of feature
Feature distribution
to be searched
Regions with similar 
distributions for 
regular partitioning
Regions with similar 
distributions for K-d 
tree partitioning
Regions with similar 
distributions for SLIC 
partitioning

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How to Compute Similarity Between Distributions?
• Kullback–Leibler divergence: Amount of work needed to 
convert one distribution to other 
• Earth Mover’s distance: Minimum cost of turning mass of one 
distribution to another. For 1-D distributions, this can be 
shown as a sum of the differences between their cumulative 
distributions
• Bhattacharya distance:
where
P and Q are probability 
distributions defined 
on the same domain

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distribution-driven Feature Extraction and Tracking
• Vaguely define features
• Vortex core, hurricane eye, tumor in medical data
• Traditional feature tracking algorithms
• Assume precise feature definition
• Distribution-based Methods
• Can extract imprecisely defined features robustly
• Track the extracted features over time
Model target feature as a distribution
Temporal data distributions via 
Incremental estimation
Estimate 
foreground 
possibility
Estimate 
similarity with 
target
Feature–aware 
classification field
+
Distribution Driven Extraction and Tracking of Features for Time-varying Data Analysis

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Incremental GMM Modeling for Time-varying Data
New data points observed
GMM before update
GMM after update
• Update weights as:
𝜔𝑘, 𝑡= 1 −𝛼𝜔𝑘, 𝑡+  𝛼(𝑀𝑘, 𝑡) , 
𝑀𝑘, 𝑡= 1 for matched dist., 0 for others
• Update means and covariances for the matched distribution as:
𝜇𝑡= (1 −𝜌) 𝜇𝑡-1 + 𝜌𝑥𝑡
𝜎,- = (1 −𝜌) 𝜎,./
-
+ 𝜌𝑥𝑡 −𝜇𝑡𝑇𝑥𝑡 −𝜇𝑡 ,  𝜌=  𝛼∗𝑁𝑥𝑡 𝜇k,𝜎k)
Σ𝑘, 𝑡 = 𝜎!
-I, where I = Identity matrix, 𝛼 = learning rate
http://www.ai.mit.edu/projects/vsam/Publications/stauffer_cvpr98_track.pdf

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• A block is classified as foreground if new data
• do not match any existing Gaussians 
• match with a newly created Gaussian
• Similarity of a block with the target GMM is 
estimated by Bhattacharya distance
!
!
!
!
"
#
$
!"#$%#"&'( )
* )
* )
* )
+",,*-*.*)/
-
0
'
=
!
!
!
"
#
$
"
!
#
!"#"$%&"'( '
" '
)*&#
" '
'
+*!!","$"'(
,
,
-
ψ
= −
!
!
!
"
"
# $
%
#
$
%
!
"
#
$
#
$
#
$
% %
% %
ψ
ωω ξ
=
=
= ∑∑
Low similarity 
value
Target 
distribution
High similarity 
value
Conceptual diagram for foreground estimation
Distribution-driven Feature Extraction and Tracking
Classification using Foreground Detection
Distribution Similarity Based Classification
𝜉𝑝, 𝑝′ = ( 
* 𝜇−𝜇+ 𝑇
,-,!
.
𝜇−𝜇+ + ( 
. ln[
"#"!
$
|,||,!|]
Distribution Driven Extraction and Tracking of Features for Time-varying Data Analysis

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
• Final Feature-aware Classification field:
• Tracking in Classification Field: Segment the data using the threshold, apply Connected 
Component algorithm
• Attribute based tracking:
! "
#
! "
!$
"#
! "
!"#$%&"
'
(')'*#&'$+
'
!,&"-&,%./
'
0,(('1'*'$+
1
0,(('1'*'$+
1
0,(('1'*'$+
1
γ
γ
=
+
−
+
=
Foreground measure
Similarity measure
Final combined field
Distribution Driven Extraction and Tracking of Features for Time-varying Data Analysis
Distribution-driven Feature Extraction and Tracking
Volume, 
mass, 
shape, 
CoG

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Selection of the target feature in Vortex data
Feature at T = 3
Feature at T = 6
Feature at T = 15
Feature at T = 20
Feature at T=10
Feature at T=20
Selection of the target feature in Earthquake data
Distribution Driven Extraction and Tracking of Features for Time-varying Data Analysis
Distribution-driven Feature Extraction and Tracking

## Figures

### Page 1

![Page 1](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_001.png)

### Page 2

![Page 2](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_002.png)

### Page 3

![Page 3](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_003.png)

### Page 4

![Page 4](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_004.png)

### Page 5

![Page 5](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_005.png)

### Page 6

![Page 6](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_006.png)

### Page 7

![Page 7](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_007.png)

### Page 8

![Page 8](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_008.png)

### Page 9

![Page 9](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_009.png)

### Page 10

![Page 10](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_010.png)

### Page 11

![Page 11](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_011.png)

### Page 12

![Page 12](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_012.png)

### Page 13

![Page 13](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_013.png)

### Page 14

![Page 14](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_014.png)

### Page 15

![Page 15](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_015.png)

### Page 16

![Page 16](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_016.png)

### Page 17

![Page 17](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_017.png)

### Page 18

![Page 18](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_018.png)

### Page 19

![Page 19](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_019.png)

### Page 20

![Page 20](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_020.png)

### Page 21

![Page 21](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_021.png)

### Page 22

![Page 22](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_022.png)

### Page 23

![Page 23](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_023.png)

### Page 24

![Page 24](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_024.png)

### Page 25

![Page 25](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_025.png)

### Page 26

![Page 26](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_026.png)

### Page 27

![Page 27](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_027.png)

### Page 28

![Page 28](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_028.png)

### Page 29

![Page 29](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_029.png)

### Page 30

![Page 30](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_030.png)

### Page 31

![Page 31](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_031.png)

### Page 32

![Page 32](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_032.png)

### Page 33

![Page 33](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_033.png)

### Page 34

![Page 34](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_034.png)

### Page 35

![Page 35](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_035.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_012.png)

### embedded_013

![embedded_013](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_018.png)

### embedded_019

![embedded_019](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_023.jpg)

### embedded_024

![embedded_024](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_024.jpg)

### embedded_025

![embedded_025](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_026.jpg)

### embedded_027

![embedded_027](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_028.jpg)

### embedded_029

![embedded_029](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_029.jpg)

### embedded_030

![embedded_030](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_030.png)

### embedded_031

![embedded_031](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_031.jpg)

### embedded_032

![embedded_032](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_032.png)

### embedded_033

![embedded_033](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_034.jpg)

### embedded_035

![embedded_035](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_035.jpg)

### embedded_036

![embedded_036](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_036.jpg)

### embedded_037

![embedded_037](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_037.jpg)

### embedded_038

![embedded_038](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_038.jpg)

### embedded_039

![embedded_039](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_039.jpg)

### embedded_040

![embedded_040](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_040.jpg)

### embedded_041

![embedded_041](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_041.jpg)

### embedded_042

![embedded_042](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_042.jpg)

### embedded_043

![embedded_043](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_043.jpg)

### embedded_044

![embedded_044](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_044.jpg)

### embedded_045

![embedded_045](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_045.png)

### embedded_046

![embedded_046](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_046.png)

### embedded_047

![embedded_047](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_047.png)

### embedded_048

![embedded_048](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_048.png)

### embedded_049

![embedded_049](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_049.png)

### embedded_050

![embedded_050](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_050.png)

### embedded_051

![embedded_051](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_051.png)

### embedded_052

![embedded_052](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_052.png)

### embedded_053

![embedded_053](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_053.png)

### embedded_054

![embedded_054](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_054.png)

### embedded_055

![embedded_055](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_055.png)

### embedded_056

![embedded_056](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_056.jpg)

### embedded_057

![embedded_057](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_057.jpg)

### embedded_058

![embedded_058](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_058.jpg)

### embedded_059

![embedded_059](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_059.jpg)

### embedded_060

![embedded_060](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_060.jpg)

### embedded_061

![embedded_061](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_061.jpg)

### embedded_062

![embedded_062](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_062.jpg)

### embedded_063

![embedded_063](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_063.jpg)

### embedded_064

![embedded_064](assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_064.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_002.png` | 2 |
| Page 3 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_003.png` | 3 |
| Page 4 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_004.png` | 4 |
| Page 5 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_005.png` | 5 |
| Page 6 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_006.png` | 6 |
| Page 7 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_007.png` | 7 |
| Page 8 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_008.png` | 8 |
| Page 9 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_009.png` | 9 |
| Page 10 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_010.png` | 10 |
| Page 11 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_011.png` | 11 |
| Page 12 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_012.png` | 12 |
| Page 13 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_013.png` | 13 |
| Page 14 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_014.png` | 14 |
| Page 15 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_015.png` | 15 |
| Page 16 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_016.png` | 16 |
| Page 17 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_017.png` | 17 |
| Page 18 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_018.png` | 18 |
| Page 19 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_019.png` | 19 |
| Page 20 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_020.png` | 20 |
| Page 21 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_021.png` | 21 |
| Page 22 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_022.png` | 22 |
| Page 23 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_023.png` | 23 |
| Page 24 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_024.png` | 24 |
| Page 25 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_025.png` | 25 |
| Page 26 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_026.png` | 26 |
| Page 27 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_027.png` | 27 |
| Page 28 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_028.png` | 28 |
| Page 29 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_029.png` | 29 |
| Page 30 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_030.png` | 30 |
| Page 31 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_031.png` | 31 |
| Page 32 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_032.png` | 32 |
| Page 33 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_033.png` | 33 |
| Page 34 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_034.png` | 34 |
| Page 35 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/page_035.png` | 35 |
| embedded_001 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_012.png` | Embedded raster image |
| embedded_013 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_018.png` | Embedded raster image |
| embedded_019 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_023.jpg` | Embedded raster image |
| embedded_024 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_024.jpg` | Embedded raster image |
| embedded_025 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_026.jpg` | Embedded raster image |
| embedded_027 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_028.jpg` | Embedded raster image |
| embedded_029 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_029.jpg` | Embedded raster image |
| embedded_030 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_030.png` | Embedded raster image |
| embedded_031 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_031.jpg` | Embedded raster image |
| embedded_032 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_032.png` | Embedded raster image |
| embedded_033 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_034.jpg` | Embedded raster image |
| embedded_035 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_035.jpg` | Embedded raster image |
| embedded_036 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_036.jpg` | Embedded raster image |
| embedded_037 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_037.jpg` | Embedded raster image |
| embedded_038 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_038.jpg` | Embedded raster image |
| embedded_039 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_039.jpg` | Embedded raster image |
| embedded_040 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_040.jpg` | Embedded raster image |
| embedded_041 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_041.jpg` | Embedded raster image |
| embedded_042 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_042.jpg` | Embedded raster image |
| embedded_043 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_043.jpg` | Embedded raster image |
| embedded_044 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_044.jpg` | Embedded raster image |
| embedded_045 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_045.png` | Embedded raster image |
| embedded_046 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_046.png` | Embedded raster image |
| embedded_047 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_047.png` | Embedded raster image |
| embedded_048 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_048.png` | Embedded raster image |
| embedded_049 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_049.png` | Embedded raster image |
| embedded_050 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_050.png` | Embedded raster image |
| embedded_051 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_051.png` | Embedded raster image |
| embedded_052 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_052.png` | Embedded raster image |
| embedded_053 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_053.png` | Embedded raster image |
| embedded_054 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_054.png` | Embedded raster image |
| embedded_055 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_055.png` | Embedded raster image |
| embedded_056 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_056.jpg` | Embedded raster image |
| embedded_057 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_057.jpg` | Embedded raster image |
| embedded_058 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_058.jpg` | Embedded raster image |
| embedded_059 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_059.jpg` | Embedded raster image |
| embedded_060 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_060.jpg` | Embedded raster image |
| embedded_061 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_061.jpg` | Embedded raster image |
| embedded_062 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_062.jpg` | Embedded raster image |
| embedded_063 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_063.jpg` | Embedded raster image |
| embedded_064 | `assets/Lecture15_Dist_Summarization_Analysis_Visualization_01a2f5b2-7468-4fd7-a673-2ea5540da464/embedded_064.jpg` | Embedded raster image |

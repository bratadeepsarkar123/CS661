---
title: "Lecture17 Sampling 1"
source_pdf: "markdown_files/lecture pdf/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78.pdf"
converted: 2026-07-07
pages: 36
---

# Lecture17 Sampling 1

**Source:** `markdown_files/lecture pdf/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78.pdf`  
**Converted:** 2026-07-07  
**Pages:** 36

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
Population, Sample, and Sampling
• “Population” is the entire set of items from which you 
draw data for a statistical study (sampling frame)
• A “sample” is a subset of a population
• “Sampling” is the process of selecting a subset from a 
population and is called sample
• Goal of sampling:
• The primary objective of sampling is to select a subset of data 
from a large population, which might be impossible to handle 
and sometimes we cannot even have access to the entire 
population
• Data reduction and representative selection for performing 
statistical analysis and inference about the population
• Save time, space, and money
• Practical approach for solving challenging problems
c
Population
Sample
Sampling
Inference

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Real-life Motivating Applications
• Applications of Sampling and sample-based analysis is widespread
• Sampling is everywhere since it is impossible to keep/access all the data
• Suppose we want to measure the average height of the males in 
India
• Based on our capability, we can measure heights for 10,000 
males/day
• India has around 717 million male population*
• It would take 71,700 days, roughly 197 years!
• Would you do it? Do you think this is practical approach even 
with more resources?
• What if tomorrow I want to know the average height  of the 
female population in India?
*https://statisticstimes.com/demographics/country/india-sex-ratio.php
Sampling is the fundamental tool for any kind of survey
Sampling to further scientific discovery
• Suppose we wish to predict climate accurately for the near 
future or want to understand fundamental physics or want to 
assess the impact of an asteroid hitting our earth!
• We use large-scale computational simulations that attempts 
to model these phenomena accurately
• These simulations generate petabytes (1015 bytes) of data, 
soon to reach exabyte (1018)
• We simply cannot keep/analyze all the data and even if we try, 
the cost and resource will be prohibitive
How can/should we sample big data to achieve our goals above?

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification of Sampling Techniques
Non-probabilistic 
Approaches
Convenience 
Sampling
Judgmental 
Sampling
Quota 
Sampling
Snowball 
Sampling
Probabilistic 
Approaches
Simple 
Random 
Sampling
Systematic 
Sampling
Stratified 
Sampling
Cluster 
Sampling
Advanced/Multi-stage 
Approaches
Rejection 
Sampling
Importance-
based 
Sampling
Blue Noise 
Sampling 
Many other 
approaches
• Non-probabilistic 
approaches
• Items selected by not 
considering their probability 
of occurrence

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification of Sampling Techniques
Non-probabilistic 
Approaches
Convenience 
Sampling
Judgmental 
Sampling
Quota 
Sampling
Snowball 
Sampling
Probabilistic 
Approaches
Simple 
Random 
Sampling
Systematic 
Sampling
Stratified 
Sampling
Cluster 
Sampling
Advanced/Multi-stage 
Approaches
Rejection 
Sampling
Importance-
based 
Sampling
Blue Noise 
Sampling 
Many other 
approaches
• Non-probabilistic 
approaches
• Items selected by not 
considering their probability 
of occurrence
• Probabilistic approaches
• Items selected based on their 
occurrence in the population
• Prevalent in Data Science 
applications
• Gives good estimations of 
statistic

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Classification of Sampling Techniques
Non-probabilistic 
Approaches
Convenience 
Sampling
Judgmental 
Sampling
Quota 
Sampling
Snowball 
Sampling
Probabilistic 
Approaches
Simple 
Random 
Sampling
Systematic 
Sampling
Stratified 
Sampling
Cluster 
Sampling
Advanced/Multi-stage 
Approaches
Rejection 
Sampling
Importance-
based 
Sampling
Blue Noise 
Sampling 
Many other 
approaches
• Non-probabilistic approaches
• Items selected by not considering 
their probability of occurrence
• Probabilistic approaches
• Items selected based on their 
occurrence in the population
• Prevalent in Data Science 
applications
• Gives good estimations of statistic
• Advanced approaches
• Largely probabilistic
• Often data-driven
• Sometimes application-specific

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Non-Probabilistic Sampling 
Approaches

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Convenience sampling
• Convenience sampling
• It is one of the easiest and common form of sampling
• Sample observations are selected based on ease of accessibility and 
convenience
• Sample is not a true representation of the population
• Generalization and statistical inference using samples generated by 
convenience sampling may not be accurate
• Can be used for initial or informal pilot study
• Also known as grab sampling

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Convenience sampling

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Judgmental sampling
• Judgmental sampling
• It is a non-probabilistic method where existing knowledge is used to select 
sample observations from the population
• Sample is not a true representation of the population
• Generalization and statistical inference using samples generated by 
convenience sampling may not be accurate
• Judgmental sampling could be computationally less expensive than others 
and gives the sample set where the user is interested in

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Judgmental sampling

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Quota sampling
• Quota sampling
• It is a non-probabilistic method where sample observations are selected 
based on some pre-defined ‘quota’
• First the population is divided into mutually exclusive groups based on certain 
characteristics and traits
• Then judgmental sampling is performed inside each group to select 
observations to satisfy a pre-defined criterion
• May have bias in selected sample
• This is a non-probabilistic version of stratified sampling

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Quota sampling

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Quota sampling

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Snowball sampling
• Snowball sampling
• It is a non-probabilistic sampling method where the current selected 
observations dictate how subsequent observations will be selected
• This is also known as chain sampling or referral sampling
• The sampled observations grow like a rolling snowball, hence the name
• The sampling process starts with a small pool of observations and then the 
selection process propagates via nominations of the initial observations
• This method is heavily used in social computing, graph sampling 
applications
• Produces a biased estimate of the population but can often reveal 
hidden patterns

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Snowball sampling

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Probabilistic Sampling 
Approaches

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Systematic Sampling
• Observations or data points are selected at regular interval from the 
population 
• Steps:
• Calculate the sampling interval ( I = N/n)
• Draw a random number (<=I) for the starting data point
• Draw every Ith data point from the starting point
• Ensures a good representativeness of the population in the selected 
sample

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Systematic Sampling
• Observations or data points are selected at regular interval from the 
population 
9X9 = 81 data points before sampling
25 data points selected after sampling

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Simple Random Sampling (SRS)
• The most basic sampling technique, widely used 
with favorable properties
• Provides theoretical basis for the more complicated 
methods
• Idea: Every item/point in the population has equal 
probability of being selected
• If we have N points and we wish to select a sample of n 
points ( n <= N) then each point has initially probability 
1/N to get selected
• In practice, we can generate random numbers using the 
indices of points to select the desired number of points
• Random sampling gives unbiased estimations 
about the population
• Statistic estimated on sample faithfully reflects the 
statistic about population
• Mean, variance, higher order moments etc. 
Number of points = 100000
Average (mean): 5.0
Standard Deviation = 2.0
10% sample 
Average (mean): 4.974
Standard Deviation = 2.008

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Simple Random Sampling (SRS)
• Randomly select points from population
9X9 = 81 data points before sampling
25 data points selected after sampling

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Randomization Theory for Simple Random Sampling
• Simple Random Sampling (SRS) gives unbiased estimator about the population
• Let us show that sample mean is an unbiased estimator of population mean
• To do this, we need to show expected value of the sample mean is equal to the population mean
Population mean:
Sample mean:
We need to show: 
Each 𝑋! has Expected Value  𝜇: Since each 𝑋! is sampled uniformly from the population 𝑋", 𝑋#, 𝑋$, … 𝑋%

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Stratified Sampling
• Classify the population into several homogeneous strata
• This process is called stratification
• Determine the sample size
• Randomly sample points from each strata
• Disproportionate sampling
• Proportionate sampling
• Combine sampled results from each strata

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Stratified Sampling
• Classify the population into several homogeneous strata
• Determine the sample size
• Randomly sample points from each strata
• Disproportionate sampling
• Proportionate sampling
• Combine results from each strata
Disproportionate sampling
Proportionate sampling
Strata
Population

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Cluster Sampling
• The population is first clustered into mutually 
exclusive heterogeneous groups
• The clustering is done based on some global 
criteria
• Each cluster must represent the population as 
best as possible
• Clusters are internally heterogeneous but 
externally homogeneous
• Then sample is selected from a randomly 
selected single or multiple group of clusters
https://statisticsbyjim.com/basics/cluster-sampling/

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Single-stage Cluster Sampling
• After the clusters are formed, 
either a single or a set of clusters 
are selected at random
• All the data points in such clusters 
are combined for analysis
• This is suitable when the data set 
is not too large, and a subset of 
clusters can be handled efficiently

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Two-stage Cluster Sampling
• After the clusters are formed, either a single or a set of clusters are 
selected at random
• Simple random sampling is performed inside each cluster to select 
subset of data points from each selected cluster
• All the selected points are are combined for analysis
• This is more of a practical approach that can handle relatively large 
data sets as two steps of filtering is applied

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Cluster Sampling: Advantages
• If the cluster generation process produces clusters that are very 
similar to the entire population and each cluster can represent it well, 
then using cluster sampling method reliable results can be produced
• Often suitable for large scale data sets
• Applicable when the entire population is impossible to access

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Advanced Sampling 
Approaches

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Inverse Transform Sampling
• What happens behind the scene when we generate sample points 
from a specific type of distribution
• Set up:
• We have numbers between 𝑈~[0,1] coming from a Uniform distribution
• We want points that follow Exponential(𝜆) distribution
Pdf of exponential distribution
Cdf of exponential distribution

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Inverse Transform Sampling
• We have uniform numbers between 𝑈~[0,1] coming from a Uniform distribution
• We want points that follow Exponential(𝜆) distribution
• We want 𝑇𝑈= 𝑋 so that we transform uniform numbers to Exponential 
distribution
𝐹𝑋= 𝑃𝑋≤𝑥= 𝑃𝑇𝑈≤𝑥= 𝑃𝑈≤𝑇!" 𝑥
= 𝑇!" 𝑥
 
So, we have, 𝐹𝑋= 𝑇!" 𝑥 hence, 𝑇𝑥= 𝐹!"(𝑋)

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Remember: Distribution Transformation Property
• If 𝑈 is a uniform random variable (i.e., 𝑈 ~ 𝑈𝑛𝑖𝑓[0,1] ) and 𝐹𝑋 is a CDF of 
random variable 𝑋, then its inverse function 𝐹#
!" (𝑈)  corresponds to the 
random variable 𝑋  (i.e., 𝐹#
!" (𝑈)~ 𝑋)
0.0
1.0
0.0
2.0
-2.0
𝑈
𝐹!
"#
𝑋

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Rejection Sampling
• Rejection sampling is a method for generating samples from a density function 𝑓𝑥 
by drawing sample points from another distribution ℎ(𝑥) that is easier to sample
• When we do not know how to sample using 𝑓𝑥or its CDF is difficult to 
compute, inverse CDF is not available, etc.
• Steps:
• Generate a sample from ℎ(𝑥)
• Accept the sample point with acceptance prob: 
𝑓(𝑥)
𝐶∗ℎ(𝑥) , C is a constant to ensure 𝐶∗ℎ𝑥≥𝑓(𝑥)
𝑓𝑥= 𝑝𝑙𝑜𝑡 𝑜𝑓 𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛 (𝑅𝑒𝑑)
𝐶∗ℎ𝑥= 𝑁𝑜𝑟𝑚𝑎𝑙 𝐷𝑖𝑠𝑡𝑟𝑖𝑏𝑢𝑡𝑖𝑜𝑛 (𝐵𝑙𝑎𝑐𝑘)
Density
Values
Intuition: High acceptance probability for a 
specific sample point drawn from ℎ(𝑥) 
indicates that the sample is highly likely for 
distribution 𝑓(𝑥) and so accept it.
•
 𝐶 is a normalizing constant to ensure 
𝐶∗ℎ𝑥≥𝑓(𝑥) as the ratio 
&(()
*∗,(() is 
interpreted as probability value

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Why Rejection Sampling Works?
• We have 𝑓(𝑥) as the density function of 𝑥
• Initially points come from ℎ𝑥, so they follow ℎ(𝑥)
• The probability that a point can be accepted is:
• Probability with which it is generated * acceptance probability
• ℎ𝑥∗
D E
F∗G E = D E
F     à Notice that ℎ𝑥cancels out!
• So, the accepted samples have density proportional to 𝑓(𝑥)/C

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Blue Noise Sampling
• Blue noise: Characterized by a power spectral density that decreases logarithmically with 
frequency
• Blue noise has more energy at higher frequencies and less at lower frequencies
• Blue noise sampling: Blue noise sampling aims to create a distribution of points that 
appears random but avoids clustering or patterns, resulting in a more uniform and visually 
appealing distribution
• emphasize higher frequencies while suppressing lower frequencies
Systematic
Random
Blue Noise

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Blue Noise Sampling
• Poisson disk / Dart Throwing for Blue noise sampling
• No two samples withing a radius r are allowed
• Sample points are picked from a uniform distribution, and the sample 
points that obey the minimum distance property with respect to the 
sample points currently in the set are kept, while the others are 
discarded.

## Figures

### Page 1

![Page 1](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_001.png)

### Page 2

![Page 2](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_002.png)

### Page 3

![Page 3](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_003.png)

### Page 4

![Page 4](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_004.png)

### Page 5

![Page 5](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_005.png)

### Page 6

![Page 6](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_006.png)

### Page 7

![Page 7](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_007.png)

### Page 8

![Page 8](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_008.png)

### Page 9

![Page 9](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_009.png)

### Page 10

![Page 10](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_010.png)

### Page 11

![Page 11](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_011.png)

### Page 12

![Page 12](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_012.png)

### Page 13

![Page 13](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_013.png)

### Page 14

![Page 14](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_014.png)

### Page 15

![Page 15](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_015.png)

### Page 16

![Page 16](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_016.png)

### Page 17

![Page 17](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_017.png)

### Page 18

![Page 18](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_018.png)

### Page 19

![Page 19](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_019.png)

### Page 20

![Page 20](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_020.png)

### Page 21

![Page 21](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_021.png)

### Page 22

![Page 22](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_022.png)

### Page 23

![Page 23](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_023.png)

### Page 24

![Page 24](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_024.png)

### Page 25

![Page 25](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_025.png)

### Page 26

![Page 26](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_026.png)

### Page 27

![Page 27](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_027.png)

### Page 28

![Page 28](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_028.png)

### Page 29

![Page 29](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_029.png)

### Page 30

![Page 30](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_030.png)

### Page 31

![Page 31](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_031.png)

### Page 32

![Page 32](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_032.png)

### Page 33

![Page 33](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_033.png)

### Page 34

![Page 34](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_034.png)

### Page 35

![Page 35](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_035.png)

### Page 36

![Page 36](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_036.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_003.png)

### embedded_004

![embedded_004](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_004.png)

### embedded_005

![embedded_005](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_007.png)

### embedded_008

![embedded_008](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_008.png)

### embedded_009

![embedded_009](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_009.png)

### embedded_010

![embedded_010](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_015.png)

### embedded_016

![embedded_016](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_018.png)

### embedded_019

![embedded_019](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_019.png)

### embedded_020

![embedded_020](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_020.png)

### embedded_021

![embedded_021](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_023.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_002.png` | 2 |
| Page 3 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_003.png` | 3 |
| Page 4 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_004.png` | 4 |
| Page 5 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_005.png` | 5 |
| Page 6 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_006.png` | 6 |
| Page 7 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_007.png` | 7 |
| Page 8 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_008.png` | 8 |
| Page 9 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_009.png` | 9 |
| Page 10 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_010.png` | 10 |
| Page 11 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_011.png` | 11 |
| Page 12 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_012.png` | 12 |
| Page 13 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_013.png` | 13 |
| Page 14 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_014.png` | 14 |
| Page 15 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_015.png` | 15 |
| Page 16 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_016.png` | 16 |
| Page 17 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_017.png` | 17 |
| Page 18 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_018.png` | 18 |
| Page 19 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_019.png` | 19 |
| Page 20 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_020.png` | 20 |
| Page 21 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_021.png` | 21 |
| Page 22 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_022.png` | 22 |
| Page 23 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_023.png` | 23 |
| Page 24 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_024.png` | 24 |
| Page 25 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_025.png` | 25 |
| Page 26 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_026.png` | 26 |
| Page 27 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_027.png` | 27 |
| Page 28 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_028.png` | 28 |
| Page 29 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_029.png` | 29 |
| Page 30 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_030.png` | 30 |
| Page 31 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_031.png` | 31 |
| Page 32 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_032.png` | 32 |
| Page 33 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_033.png` | 33 |
| Page 34 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_034.png` | 34 |
| Page 35 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_035.png` | 35 |
| Page 36 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/page_036.png` | 36 |
| embedded_001 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_003.png` | Embedded raster image |
| embedded_004 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_004.png` | Embedded raster image |
| embedded_005 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_007.png` | Embedded raster image |
| embedded_008 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_008.png` | Embedded raster image |
| embedded_009 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_009.png` | Embedded raster image |
| embedded_010 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_015.png` | Embedded raster image |
| embedded_016 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_018.png` | Embedded raster image |
| embedded_019 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_019.png` | Embedded raster image |
| embedded_020 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_020.png` | Embedded raster image |
| embedded_021 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture17_Sampling_1_0cac6119-cb31-43a7-bd6b-7730c28ced78/embedded_023.jpg` | Embedded raster image |

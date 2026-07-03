---
title: "Lecture2 VA Handling Data"
source_pdf: "markdown_files/lecture pdf/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304.pdf"
converted: 2026-07-07
pages: 51
---

# Lecture2 VA Handling Data

**Source:** `markdown_files/lecture pdf/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304.pdf`  
**Converted:** 2026-07-07  
**Pages:** 51

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
materials made available by:
• Prof. Klaus Mueller (State University of New York at Stony Brook)
• Prof. Tamara Munzner (University of British Columbia)

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Design and Visual 
Variables

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Key Visual Representations
• Gestalt Principles 
• The tendency to perceive elements as belonging to a group, based on 
certain visual properties 
• Pre-attentiveness 
• Certain low level visual aspects are recognized before conscious 
awareness 
• Visual variables
• The different visual aspects that can be used to encode information

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Gestalt Principles
• “Gestalt” is German for “unified whole”
• Grasp the "totality" of something before worrying about the details 
• Proximity: nearby things feel grouped
• Similarity: similar items seem connected
• Closure: fill in the missing parts
Rubin’s vase
What do you see in this figure?
What do you see in this figure?

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Pre-attentiveness
• Also called pop-out

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Variables
• Two planar variables
• Spatial dimensions (X and Y)

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Variables
• Two planar variables
• Spatial dimensions (X and Y)
• Six Retinal variables
• Size
• Color
• Shape
• Orientation
• Texture
• Brightness

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Variables
• Two planar variables
• Spatial dimensions (X and Y)
• Six Retinal variables
• Size
• Color
• Shape
• Orientation
• Texture
• Brightness
• Retinal variables allow for one more variable to be encoded

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Variables
Planar
Size
Brightness
Shape
Texture
Color
Orientation

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Take Aways 
• Planar variable is the strongest visual variable 
• Maps to proximity 
• Provides an intuitive organization of information
• Things close together are perceptually grouped together (Gestalt)
• Size and brightness are good secondary visual variables to encode 
relative magnitude
• Color is a good visual variable for labeling
• Texture can do this as well, but it does not support pop-out much
• Shape provides only limited pop-out

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Considerations with Scalability for Big Data
• Must be scalable to
• Number of data points 
• Number of dimensions
• Data sources
• Diversity of data sources (heterogeneity) 
• Number of users

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Considerations with Scalability for Big Data
• Must be scalable to
• Number of data points 
• Number of dimensions
• Data sources
• Diversity of data sources (heterogeneity) 
• Number of users
Visual Analytics can help!

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
What is Visual Analytics
• Visualization plus... 
• Data processing (analytics) 
• Intelligent computing (AI, machine learning)
• Interaction (HCI) 
• Pattern discovery
• Storytelling and sensemaking
• Behavioral psychology (cognitive science, human factors)
Visual Analytics is the process of analytical reasoning often 
supported by a highly interactive visual interface/tool

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Information Seeking Mantra
• Ben Shneiderman’s Mantra: Overview, zoom and filter, then details-on-demand! 
Overview first

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Information Seeking Mantra
• Ben Shneiderman’s Mantra: Overview, zoom and filter, then details-on-demand! 
Zoom

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Information Seeking Mantra
• Ben Shneiderman’s Mantra: Overview, zoom and filter, then details-on-demand! 
Filter

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Visual Information Seeking Mantra
• Ben Shneiderman’s Mantra: Overview, zoom and filter, then details-on-demand! 
Details on demand

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Another Paradigm: Focus + Context
• Focus + Context:
• One single view which shows information in direct context 
• Maintains continuity and do not require viewer to shift back and forth
• But: there is distortion!
https://www.youtube.com/watch?v=acsFQvv4B0Q

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Use of Visualization
• Visual Perception
• Fast screening of lot of data
• Pattern recognition
• High-level cognition
• Interaction
• Direct manipulation of data and visualization (Human in the loop)
• Two-way communication
Humans are important!
But Humans are imperfect too!!

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Humans Are Imperfect
• Change Blindness
• Failure to notice (often large) changes in subsequent frames
• Inattentional Blindness
• Failing to observe an object in a visual scene due to focused attention on 
some other objects in the scene
• The "Invisible Gorilla" experiment
• Limited Working Memory
• Our mind can hold only limited amount of visual information
• Overloading visualization with multiple charts can overwhelm users, leading 
to missed insights
• Also related to chartjunk!
21

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Humans Are Imperfect
• Color Perception Issues
• Humans may have difficulty in distinguishing one color from another
• Affect interpretation of visualization for colorblind users
• Impact of Confirmation Bias
• Our mind often favors information that confirms existing beliefs ignoring 
contradictory evidence
• Leads to misinterpretation and missing key evidence from visualization
• Overemphasis on Prominent/Pop-out Features
• Bright colorful elements can distract users from observing subtle features
• Anchoring Effect
• Our mind often rely heavily on the first piece of information encountered
22

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Humans Are Imperfect
•
Spot the difference: Change blindness
Source: Google

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Humans Are Imperfect
•
Spot the difference: Change blindness
Source: Wikipedia

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Human Limitations for Visualization
• The Magic Number Seven (7 ± 2) for visualization
• Not more than 7 ± 2 segments in a pie chart 
• Not more than 7 ± 2 colors in a line chart 
• and so on …..
Miller, G.. (1956). "The magical number seven, plus or minus two: Some limits on our capacity for processing information".

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Example of Visual Complexity
Do we really need the background grid?
Maybe not!

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Handling Data

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
What Do We Do After Getting the Raw Data?
• Real world data can be dirty!
• Data cleaning (Wrangling)
• Missing values
• Noisy data
• Deal with outliers
• Standardize/normalize
• Resolve inconsistency
• Fuse/merge
https://blog.insycle.com/data-cleaning-hubspot
Data Cleaning Cycle

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Missing Data: Why?
• Data may not be always available/complete!
• Missing data may be due to 
• Equipment malfunction 
• Inconsistent with other recorded data and thus deleted
• Data not entered due to misunderstanding
• Certain data may not be considered important at the time of entry 
• Many more other reasons

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Missing Data: How to Handle?
• How would you estimate the missing value for a dataset? 
• Ignore or put in a default value 
• Manually fill in (can be tedious or infeasible for large data)
• Use the available value of the nearest neighbor 
• Average over all the values
• Use a predictive method (regression) 
• Use AI/ML models to predict missing data

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Normalization and Standardization
• Sometimes we like to have all variables on the same scale 
• Min-max normalization
• Standardization

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Normalization and Standardization
• Sometimes we like to have all variables on the same scale 
• Min-max normalization
• Standardization
• Clipping tails and outliers
• set all values beyond ± 3s to value at 3s

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Normalization

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Standardization

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Robust Scaling
• IQR = Q3 – Q1
• Difference between the 75th percentile and the 25th percentile data
• Immune to outliers 
• Relies on the median and IQR, which are robust to extreme values
• Ensures that most of the data falls within a consistent range after scaling

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Comparison Among Diff. Methods of Scaling
Raw Data
Min-max normalization
Standardization
Robust Scaling
https://www.geeksforgeeks.org/standardscaler-minmaxscaler-and-robustscaler-techniques-ml/

<!-- Page 37 -->
37
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Noisy Data
• Noise = Random error in a measured variable 
• Faulty data collection instruments 
• Data entry problems
• Data transmission problems
• Technology limitation 
• Inconsistency in naming convention

<!-- Page 38 -->
38
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Noisy Data: What to Do?
• Binning
• Replace data with bin centers

<!-- Page 39 -->
39
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Noisy Data: What to Do?
• Binning
• Replace data with bin centers
• Clustering
• Detect and remove outliers

<!-- Page 40 -->
40
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Noisy Data: What to Do?
• Binning
• Replace data with bin centers
• Clustering
• Detect and remove outliers
• Semi-automated method
• Combined human and computer inspection
• Detect suspicious value and check manually

<!-- Page 41 -->
41
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Noisy Data: What to Do?
• Binning
• Replace data with bin centers
• Clustering
• Detect and remove outliers
• Semi-automated method
• Combined human and computer inspection
• Detect suspicious value and check manually
• Regression
• Fit to a regression function and detect 
outliers

<!-- Page 42 -->
42
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Noisy Data: What to Do?
• Binning
• Replace data with bin centers
• Clustering
• Detect and remove outliers
• Semi-automated method
• Combined human and computer inspection
• Detect suspicious value and check manually
• Regression
• Smooth data by fitting to a regression 
function
• Outliers are not always noise! Be careful!

<!-- Page 43 -->
43
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Deal with Small Data
• Can you invent meaningful new data?

<!-- Page 44 -->
44
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Deal with Small Data à Data Augmentation
• Can you invent meaningful new data?
• Data Augmentation
• Strategy to artificially synthesize new data from 
existing data

<!-- Page 45 -->
45
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Deal with Small Data à Data Augmentation
• Can you invent meaningful  new data?
• Data Augmentation
• Strategy to artificially synthesize new data from 
existing data 
• Common techniques are (for images) 
• rotations 
• Translations
• Zooms
• Flips
• color perturbations 
• crops 
• add noise by jittering

<!-- Page 46 -->
46
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Synthetic Data Generation for Imbalanced 
Classification
• When data has severe imbalance in 
the class representation
• If you use such data for ML model 
training, it will perform poorly for the 
minority class
• SMOTE (Synthetic Minority 
Oversampling Technique) can help
• A data augmentation method
Imbalanced Data

<!-- Page 47 -->
47
IITK CS661: Big Data Visual Analytics: Soumya Dutta
SMOTE: Synthetic Data Generation for Imbalanced 
Classification
• How do we generate samples for minority class? 
1. Randomly under-sample the majority class
2. Select a minority class instance (x) at random and find its k-nearest 
minority class neighbors
3. Select one of the k neighbors at random, say (y)
4. The synthetic instances are generated as a convex combination of the two 
chosen instances x and y

<!-- Page 48 -->
48
IITK CS661: Big Data Visual Analytics: Soumya Dutta
SMOTE: Synthetic Data Generation for Imbalanced 
Classification
• Example:
Imbalanced Data
SMOTE + random under-sampling
https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/

<!-- Page 49 -->
49
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Augmentation for Visualization
• Generate new samples according to the data distributions 
• Cluster the data (outliers may form clusters!) 
• The size of each cluster represents its percentage in the population 
• Randomize new samples – bigger clusters get more samples 
Augmentation rate ~ Cluster size

<!-- Page 50 -->
50
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Deal with Big Data à Data Reduction!
• Purpose
• Reduce the data to a size that can be feasibly stored without missing on 
important information
• Reduce the data so a mining algorithm can be feasibly run 
• Alternatives
• Buy more storage
• Buy more computers or faster ones
• Develop more efficient algorithms
• In practice, all of this is happening at the same time 
• But the growth of data and complexities is faster
• So, data reduction is important!
•

<!-- Page 51 -->
51
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Reduction: How?
• Summarization (Later in the course)
• Binning
• Distribution-based
• Clustering
• Sampling (Later in the course)
• Systematic/Regular
• Random
• Stratified
• Adaptive/Data-driven
• Importance-driven
• Cluster-based
• Dimension Reduction (Later in the course)
• AI/ML techniques (Later in the course)
Big Data
Summary Data
Sampling
AI/ML model

## Figures

### Page 1

![Page 1](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_001.png)

### Page 2

![Page 2](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_002.png)

### Page 3

![Page 3](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_003.png)

### Page 4

![Page 4](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_004.png)

### Page 5

![Page 5](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_005.png)

### Page 6

![Page 6](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_006.png)

### Page 7

![Page 7](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_007.png)

### Page 8

![Page 8](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_008.png)

### Page 9

![Page 9](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_009.png)

### Page 10

![Page 10](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_010.png)

### Page 11

![Page 11](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_011.png)

### Page 12

![Page 12](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_012.png)

### Page 13

![Page 13](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_013.png)

### Page 14

![Page 14](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_014.png)

### Page 15

![Page 15](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_015.png)

### Page 16

![Page 16](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_016.png)

### Page 17

![Page 17](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_017.png)

### Page 18

![Page 18](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_018.png)

### Page 19

![Page 19](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_019.png)

### Page 20

![Page 20](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_020.png)

### Page 21

![Page 21](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_021.png)

### Page 22

![Page 22](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_022.png)

### Page 23

![Page 23](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_023.png)

### Page 24

![Page 24](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_024.png)

### Page 25

![Page 25](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_025.png)

### Page 26

![Page 26](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_026.png)

### Page 27

![Page 27](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_027.png)

### Page 28

![Page 28](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_028.png)

### Page 29

![Page 29](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_029.png)

### Page 30

![Page 30](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_030.png)

### Page 31

![Page 31](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_031.png)

### Page 32

![Page 32](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_032.png)

### Page 33

![Page 33](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_033.png)

### Page 34

![Page 34](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_034.png)

### Page 35

![Page 35](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_035.png)

### Page 36

![Page 36](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_036.png)

### Page 37

![Page 37](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_037.png)

### Page 38

![Page 38](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_038.png)

### Page 39

![Page 39](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_039.png)

### Page 40

![Page 40](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_040.png)

### Page 41

![Page 41](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_041.png)

### Page 42

![Page 42](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_042.png)

### Page 43

![Page 43](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_043.png)

### Page 44

![Page 44](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_044.png)

### Page 45

![Page 45](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_045.png)

### Page 46

![Page 46](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_046.png)

### Page 47

![Page 47](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_047.png)

### Page 48

![Page 48](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_048.png)

### Page 49

![Page 49](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_049.png)

### Page 50

![Page 50](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_050.png)

### Page 51

![Page 51](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_051.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_003.png)

### embedded_004

![embedded_004](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_005.png)

### embedded_006

![embedded_006](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_006.png)

### embedded_007

![embedded_007](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_007.png)

### embedded_008

![embedded_008](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_008.png)

### embedded_009

![embedded_009](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_009.png)

### embedded_010

![embedded_010](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_010.png)

### embedded_011

![embedded_011](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_011.png)

### embedded_012

![embedded_012](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_012.png)

### embedded_013

![embedded_013](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_023.png)

### embedded_024

![embedded_024](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_024.jpg)

### embedded_025

![embedded_025](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_026.png)

### embedded_027

![embedded_027](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_028.png)

### embedded_029

![embedded_029](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_029.png)

### embedded_030

![embedded_030](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_030.png)

### embedded_031

![embedded_031](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_031.jpg)

### embedded_032

![embedded_032](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_032.jpg)

### embedded_033

![embedded_033](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_034.jpg)

### embedded_035

![embedded_035](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_035.jpg)

### embedded_036

![embedded_036](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_036.png)

### embedded_037

![embedded_037](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_037.png)

### embedded_038

![embedded_038](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_038.jpg)

### embedded_039

![embedded_039](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_039.jpg)

### embedded_040

![embedded_040](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_040.jpg)

### embedded_041

![embedded_041](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_041.jpg)

### embedded_042

![embedded_042](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_042.jpg)

### embedded_043

![embedded_043](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_043.jpg)

### embedded_044

![embedded_044](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_044.png)

### embedded_045

![embedded_045](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_045.png)

### embedded_046

![embedded_046](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_046.jpg)

### embedded_047

![embedded_047](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_047.png)

### embedded_048

![embedded_048](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_048.png)

### embedded_049

![embedded_049](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_049.png)

### embedded_050

![embedded_050](assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_050.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_002.png` | 2 |
| Page 3 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_003.png` | 3 |
| Page 4 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_004.png` | 4 |
| Page 5 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_005.png` | 5 |
| Page 6 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_006.png` | 6 |
| Page 7 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_007.png` | 7 |
| Page 8 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_008.png` | 8 |
| Page 9 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_009.png` | 9 |
| Page 10 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_010.png` | 10 |
| Page 11 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_011.png` | 11 |
| Page 12 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_012.png` | 12 |
| Page 13 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_013.png` | 13 |
| Page 14 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_014.png` | 14 |
| Page 15 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_015.png` | 15 |
| Page 16 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_016.png` | 16 |
| Page 17 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_017.png` | 17 |
| Page 18 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_018.png` | 18 |
| Page 19 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_019.png` | 19 |
| Page 20 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_020.png` | 20 |
| Page 21 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_021.png` | 21 |
| Page 22 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_022.png` | 22 |
| Page 23 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_023.png` | 23 |
| Page 24 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_024.png` | 24 |
| Page 25 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_025.png` | 25 |
| Page 26 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_026.png` | 26 |
| Page 27 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_027.png` | 27 |
| Page 28 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_028.png` | 28 |
| Page 29 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_029.png` | 29 |
| Page 30 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_030.png` | 30 |
| Page 31 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_031.png` | 31 |
| Page 32 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_032.png` | 32 |
| Page 33 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_033.png` | 33 |
| Page 34 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_034.png` | 34 |
| Page 35 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_035.png` | 35 |
| Page 36 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_036.png` | 36 |
| Page 37 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_037.png` | 37 |
| Page 38 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_038.png` | 38 |
| Page 39 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_039.png` | 39 |
| Page 40 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_040.png` | 40 |
| Page 41 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_041.png` | 41 |
| Page 42 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_042.png` | 42 |
| Page 43 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_043.png` | 43 |
| Page 44 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_044.png` | 44 |
| Page 45 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_045.png` | 45 |
| Page 46 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_046.png` | 46 |
| Page 47 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_047.png` | 47 |
| Page 48 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_048.png` | 48 |
| Page 49 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_049.png` | 49 |
| Page 50 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_050.png` | 50 |
| Page 51 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/page_051.png` | 51 |
| embedded_001 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_003.png` | Embedded raster image |
| embedded_004 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_005.png` | Embedded raster image |
| embedded_006 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_006.png` | Embedded raster image |
| embedded_007 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_007.png` | Embedded raster image |
| embedded_008 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_008.png` | Embedded raster image |
| embedded_009 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_009.png` | Embedded raster image |
| embedded_010 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_010.png` | Embedded raster image |
| embedded_011 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_011.png` | Embedded raster image |
| embedded_012 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_012.png` | Embedded raster image |
| embedded_013 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_023.png` | Embedded raster image |
| embedded_024 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_024.jpg` | Embedded raster image |
| embedded_025 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_026.png` | Embedded raster image |
| embedded_027 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_028.png` | Embedded raster image |
| embedded_029 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_029.png` | Embedded raster image |
| embedded_030 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_030.png` | Embedded raster image |
| embedded_031 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_031.jpg` | Embedded raster image |
| embedded_032 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_032.jpg` | Embedded raster image |
| embedded_033 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_034.jpg` | Embedded raster image |
| embedded_035 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_035.jpg` | Embedded raster image |
| embedded_036 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_036.png` | Embedded raster image |
| embedded_037 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_037.png` | Embedded raster image |
| embedded_038 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_038.jpg` | Embedded raster image |
| embedded_039 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_039.jpg` | Embedded raster image |
| embedded_040 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_040.jpg` | Embedded raster image |
| embedded_041 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_041.jpg` | Embedded raster image |
| embedded_042 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_042.jpg` | Embedded raster image |
| embedded_043 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_043.jpg` | Embedded raster image |
| embedded_044 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_044.png` | Embedded raster image |
| embedded_045 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_045.png` | Embedded raster image |
| embedded_046 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_046.jpg` | Embedded raster image |
| embedded_047 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_047.png` | Embedded raster image |
| embedded_048 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_048.png` | Embedded raster image |
| embedded_049 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_049.png` | Embedded raster image |
| embedded_050 | `assets/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304/embedded_050.jpg` | Embedded raster image |

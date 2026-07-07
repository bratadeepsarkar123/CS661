---
title: "Lecture13 Stats refresher"
source_pdf: "markdown_files/lecture pdf/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30.pdf"
converted: 2026-07-07
pages: 40
---

# Lecture13 Stats refresher

**Source:** `markdown_files/lecture pdf/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30.pdf`  
**Converted:** 2026-07-07  
**Pages:** 40

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
Study Materials for Lecture 13
• https://jdstorey.org/fas/index.html
• https://online.stat.psu.edu/stat500/lesson/0
• A Gentle Tutorial of the EM Algorithm and its Application to 
Parameter Estimation for Gaussian Mixture and Hidden Markov 
Models
• EM Algorithm: 
https://stephens999.github.io/fiveMinuteStats/intro_to_em.html

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Random Variables and 
Distributions

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Random Variable
• Let S be a sample space of an experiment
• S is associated with a probability measure P
• A random variable X is a real valued function on S
• Key property: It is a function whose values have probabilities attached 
with it

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Random Variable: Example
• Let us flip a fair coin three times
• Sample space S = {hhh, hht, hth, htt, thh, tht, tth, ttt}
• Assume X is a function on S,  so that X is the number of heads (h)
• So, we have,
• {hhh à 3, hht à 2, hth à 2, htt à 2, thh à 2, tht à 2, tth à 1, 
ttt à 0}
• X is a random variable

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Random Variable: Example
• We can answer questions like:
• P(X=0) = P(ttt) = 1/8
• P(X = 1) = P(htt ) + P(tht ) + P(tth) = 3/8
• P(X = 2) = P(hht ) + P(hth) + P(thh) = 3/8
• P(X = 3) = P(hhh) = 1/8
• We can tabulate it:

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Random Variable (RV): Example
• Rolling a fair die
• Assume a RV: X = the number that comes up
• X takes values 1,2,3,4,5,6 with probability 1/6

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Discrete and Continuous Random Variable
• A random variable is said to be discrete if its set of possible values is a 
discrete set
• Example: Rolling a fair die and measuring the value that shows up
• A random variable is said to be continuous when it can assume an 
uncountable number of values
• Example: Depth of a pool, height of all the males, etc.

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Expected Value and Variance of a Discrete RV
• Expected Value (mean):
𝐸𝑋= $ 𝑥𝑖∗𝑝𝑥𝑖,
𝑝𝑥= 𝑃𝑀𝐹
• Variance:
𝑉𝑎𝑟𝑋= $ 𝑥−𝐸𝑋
2 ∗𝑝(𝑥)
• Standard Deviation:
𝑆𝐷𝑋=
𝑉𝑎𝑟(𝑋)
https://jdstorey.org/fas/random-variables.html

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Expected Value and Variance of a Continuous RV
• Expected Value (mean):
𝐸𝑋= 4
!"
"
𝑥∗𝑓𝑥𝑑𝑥, 
𝑓𝑥= 𝑃𝐷𝐹
• Variance:
𝑉𝑎𝑟𝑋= 4
!"
"
𝑥−𝐸𝑋
2 ∗𝑓𝑥 𝑑𝑥
• Standard Deviation:
𝑆𝐷𝑋=
𝑉𝑎𝑟(𝑋)
https://jdstorey.org/fas/random-variables.html

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Probability Distribution Function
• A probability distribution function is a mathematical function that 
provides probabilities of occurrence for the possible outcomes of a 
random variable
• Probability Mass Function (PMF): The probability distribution of a 
discrete random variable is called probability mass function
• Probability Density Function (PDF): The probability distribution of a 
continuous random variable is called probability density function

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Probability Distribution Function: Properties
• Discrete case: PMF
• 𝑝𝑥= 𝑃𝑋= 𝑥
1. 𝑝𝑥≥0
2. ∑#$$ &'(()*$+ ,  𝑝𝑥= 1
3. 𝑝𝑥= 0 for all 𝑥 outside a 
discrete range 
• Continuous case: PDF
• 𝑓𝑥
1. 𝑓𝑥≥0
2. ∫!"
" 𝑓𝑥𝑑𝑥= 1 
Probability is 
evaluated as area 
under the curve
𝑃 (𝑥 =𝑐) = 0 The probability that 𝑥 takes on any individual 
value is zero. The area below the curve between 𝑥=𝑐 and 
𝑥=𝑐 has no width, and therefore no area.
Data values
Probability
Probability
density
Data values

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Cumulative Distribution Function (CDF)
• Discrete RV: Non decreasing function
                    𝐹𝑋𝑥= 𝑝𝑋≤𝑥= ∑,!-, 𝑝(𝑥𝑖)
PMF
CDF
https://jdstorey.org/fas/random-variables.html
CDF is a right continuous function
for discrete RV

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Cumulative Distribution Function (CDF)
• Continuous RV: Non decreasing function
                                   𝐹𝑋𝑥= ∫!"
, 𝑓𝑥𝑑𝑥
PDF
CDF
https://jdstorey.org/fas/random-variables.html
CDF is a 
continuous 
function 
here

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Discrete: Uniform Distribution
• Distribution assigns equal probabilities to a finite set of values

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Continuous: Exponential Distribution

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Continuous: Beta Distribution

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Continuous: Normal (Gaussian) Distribution

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Reading a Normal (Gaussian) Distribution

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Continuous: Standard Normal Distribution
• It is the normal distribution with a mean equal to 0 and a standard 
deviation (also variance) equal to 1
• The standard normal distribution is often abbreviated to Z. It is 
frequently used to simplify working with normal distributions.
Standard Normal PDF
Standard Normal CDF

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Continuous: Standard Normal Distribution
• It is the normal distribution with a mean equal to 0 and a standard 
deviation (also variance) equal to 1
• The standard normal distribution is often abbreviated to Z. It is 
frequently used to simplify working with normal distributions.
Standard Normal PDF
Standard Normal CDF

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Continuous: Standard Normal Distribution
• It is the normal distribution with a mean equal to 0 and a standard 
deviation (also variance) equal to 1
• The standard normal distribution is often abbreviated to Z. It is 
frequently used to simplify working with normal distributions.
Standard Normal PDF
Standard Normal CDF

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Joint Probability Distribution Function
• If we have multiple random 
variables, defined over the same 
probability space S, then the joint 
probability distribution is the 
distribution function that is defined 
over all possible event combinations 
of all the random variables
• Joint probability density function for 
two continuous random variables 𝑋 
and 𝑌can be represented as 
𝑓𝑋𝑌(𝑥, 𝑦)

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Joint Probability Distribution Function
• The concept of joint probability distribution function is generalizable 
and goes beyond two variables: 𝑓𝑋1𝑋2𝑋3 … 𝑋𝑛(𝑥1, 𝑥2, 𝑥3, … 𝑥𝑛)
• For two variable case, 𝑓𝑋𝑌(𝑥, 𝑦) must be a non-negative function and 
the following must hold:
E
!"
"
𝑓𝑋𝑌𝑥, 𝑦𝑑𝑥𝑑𝑦= 1
• Joint Cumulative Distribution function (CDF)
𝐹𝑋𝑌𝑥, 𝑦= P 𝑋≤𝑎, 𝑌≤𝑏=
E
!" !"
# *
𝑓𝑋𝑌𝑥, 𝑦𝑑𝑥𝑑𝑦

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Marginal Probability Distribution Functions
• From the joint probability distribution function, we can find the 
marginal probability distributions by integrating the joint distribution 
function 𝑓𝑋𝑌(𝑥, 𝑦)
𝑓𝑋𝑥= ∫!"
" 𝑓𝑋𝑌𝑥, 𝑦𝑑𝑦, for all 𝑥
𝑓𝑌𝑦= ∫!"
" 𝑓𝑋𝑌𝑥, 𝑦𝑑𝑥, for all y
• Marginal distribution functions (also known as univariate 
distributions) are probability distribution functions of individual 
random variables

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Independence
• The continuous random variables are statistically independent if their 
joint probability distribution function factors into a product of their 
marginal distributions
𝑓𝑥1, 𝑥2, 𝑥3, … , 𝑥𝑛= 𝑓𝑥1 𝑓𝑥2 𝑓𝑥3 … 𝑓(𝑥𝑛)

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Conditional Probability and Bayes’ Rule
• Conditional probability: It is the probability of an event given another 
event has occurred
𝑓.|012(𝑥) = Pr
𝑋= 𝑥} ∩{𝑌= 𝑦
Pr 𝑌= 𝑦
= 𝑓.,0(𝑥, 𝑦)
𝑓𝑌(𝑦)
• Bayes’ Rule:
𝑓.|012 𝑥=
𝑓0|.1, 𝑦∗𝑓𝑋(𝑥)
𝑓𝑌(𝑦)
𝑓!|#$% 𝑥 = Conditional probability of 𝑋 = 𝑥 given 𝑌 = 𝑦. This is also called posterior probability
𝑓#|!$& 𝑦 = Conditional probability of 𝑌 = 𝑦 given 𝑋 = 𝑥. This is called likelihood
𝑓𝑋(𝑥) = marginal of 𝑋, also the prior probability of 𝑋= 𝑥
𝑓𝑌(𝑦) = marginal probability of 𝑌

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Representations of Distribution Functions
• Non-parametric model
• Histogram
• Kernel Density Estimation (KDE)
• Parametric models
• Gaussian (Normal)
• Gaussian mixture models (GMM)

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Non-parametric Distributions: Histogram
• Histogram: A histogram is an approximate representation of a statistical 
distribution. The area under a histogram can be normalized and used as a 
probability distribution function.
https://in.mathworks.com/
Univariate Histogram
Joint Histogram

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Non-parametric Distributions: KDE
• f(x) is the KDE function
• n = number of data points
• b = bandwidth
• K(.) = Non-negative symmetric kernel 
function such as uniform, triangular, 
Gaussian etc.
• KDE: Kerner Density Estimation is a popular method of distribution estimation 
technique from sample data. Formally it is defined as follows:
Univariate KDE
Joint KDE

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parametric Distribution: GMM
• Gaussian Mixture Model (GMM): Represent a probability distribution 
function as a convex combination of  multiple Gaussian functions
!
"
#
$
"
%
&
#
!
"
"
"
"
# $
% $
ω
µ σ
=
= ∑
𝜔 = Weights of the Gaussian components
K = Number of Gaussian components in the mixture 
model
Fig. source: https://stats.stackexchange.com

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parameter Estimation Techniques
• Estimation of Gaussian distribution parameters are trivial
• Maximum Likelihood Estimate (MLE)
• Same as computing mean and variance
• Estimation of GMM parameters require Expectation Maximization 
(EM) algorithm
• Iterative technique to fit GMM parameters
• Incremental schemes for GMM parameter estimation
• Fast and approximate method to estimate GMM parameters
• Can model streaming time-varying data

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Expectation Maximization (EM) for GMM
• Initialize: means (𝜇), covariances (Σ), and weights (𝜔)
• Iterate until convergence:
• E-step:  Evaluate posterior probabilities given current parameters
𝛾!
" =
𝜔𝑘 𝒩𝑥𝑛 𝜇𝑘, Σ𝑘)
∑#$%
!
𝜔𝑗 𝒩𝑥𝑛 𝜇𝑗, Σ𝑗)
• M-step: Update the parameters to maximize the expected log-likelihood of 
the observed data
𝜔𝑘 = 
&!
&
      and 𝑁𝑘 = ∑"$%
&
𝛾!
"
𝜇𝑘 = 1
𝑁𝑘
-
"$%
&
𝛾!
"  𝑥𝑛
Σ 𝑘 = %
&! ∑"$%
&
𝛾!
" (𝑥𝑛 - 𝜇𝑘) (𝑥𝑛 - 𝜇𝑘)T
• Evaluate log likelihood at the end of each iteration and check for 
convergence
The theory of the method is 
much more involved!
For a detailed derivation:
•
 A Gentle Tutorial of the EM 
Algorithm and its Application 
to Parameter  Estimation for 
Gaussian Mixture and Hidden 
Markov Models
•
https://stephens999.github.io
/fiveMinuteStats/intro_to_em
.html

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How EM Algorithm Works

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How EM Algorithm Works

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How EM Algorithm Works

<!-- Page 37 -->
37
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How EM Algorithm Works

<!-- Page 38 -->
38
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How EM Algorithm Works

<!-- Page 39 -->
39
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How EM Algorithm Works

<!-- Page 40 -->
40
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Incremental GMM Modeling for Time-varying Data
New data points observed
GMM before update
GMM after update
• Update weights as:
𝜔𝑘, 𝑡= 1 −𝛼𝜔𝑘, 𝑡+  𝛼∗𝑀𝑘, 𝑡 , 
𝑀𝑘, 𝑡= 1 for matched dist., 0 for others
• Update means and covariances for the matched distribution as:
𝜇𝑡= (1 −𝜌) 𝜇𝑡-1 + 𝜌𝑥𝑡
𝜎'( = (1 −𝜌) 𝜎')*
(
+ 𝜌𝑥𝑡 −𝜇𝑡𝑇𝑥𝑡 −𝜇𝑡 ,  𝜌=  𝛼∗𝑁𝑥𝑡 𝜇k,𝜎k)
Σ𝑘, 𝑡 = 𝜎+
(I, where I = Identity matrix, 𝛼 = learning rate
http://www.ai.mit.edu/projects/vsam/Publications/stauffer_cvpr98_track.pdf

## Figures

### Page 1

![Page 1](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_001.png)

### Page 2

![Page 2](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_002.png)

### Page 3

![Page 3](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_003.png)

### Page 4

![Page 4](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_004.png)

### Page 5

![Page 5](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_005.png)

### Page 6

![Page 6](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_006.png)

### Page 7

![Page 7](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_007.png)

### Page 8

![Page 8](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_008.png)

### Page 9

![Page 9](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_009.png)

### Page 10

![Page 10](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_010.png)

### Page 11

![Page 11](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_011.png)

### Page 12

![Page 12](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_012.png)

### Page 13

![Page 13](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_013.png)

### Page 14

![Page 14](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_014.png)

### Page 15

![Page 15](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_015.png)

### Page 16

![Page 16](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_016.png)

### Page 17

![Page 17](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_017.png)

### Page 18

![Page 18](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_018.png)

### Page 19

![Page 19](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_019.png)

### Page 20

![Page 20](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_020.png)

### Page 21

![Page 21](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_021.png)

### Page 22

![Page 22](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_022.png)

### Page 23

![Page 23](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_023.png)

### Page 24

![Page 24](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_024.png)

### Page 25

![Page 25](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_025.png)

### Page 26

![Page 26](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_026.png)

### Page 27

![Page 27](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_027.png)

### Page 28

![Page 28](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_028.png)

### Page 29

![Page 29](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_029.png)

### Page 30

![Page 30](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_030.png)

### Page 31

![Page 31](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_031.png)

### Page 32

![Page 32](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_032.png)

### Page 33

![Page 33](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_033.png)

### Page 34

![Page 34](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_034.png)

### Page 35

![Page 35](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_035.png)

### Page 36

![Page 36](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_036.png)

### Page 37

![Page 37](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_037.png)

### Page 38

![Page 38](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_038.png)

### Page 39

![Page 39](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_039.png)

### Page 40

![Page 40](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_040.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_013.jpg)

### embedded_014

![embedded_014](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_014.jpg)

### embedded_015

![embedded_015](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_015.jpg)

### embedded_016

![embedded_016](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_016.jpg)

### embedded_017

![embedded_017](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_017.jpg)

### embedded_018

![embedded_018](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_018.jpg)

### embedded_019

![embedded_019](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_019.jpg)

### embedded_020

![embedded_020](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_023.jpg)

### embedded_024

![embedded_024](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_024.png)

### embedded_025

![embedded_025](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_025.png)

### embedded_026

![embedded_026](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_026.png)

### embedded_027

![embedded_027](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_028.png)

### embedded_029

![embedded_029](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_029.jpg)

### embedded_030

![embedded_030](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_030.jpg)

### embedded_031

![embedded_031](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_031.jpg)

### embedded_032

![embedded_032](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_032.jpg)

### embedded_033

![embedded_033](assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_033.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_002.png` | 2 |
| Page 3 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_003.png` | 3 |
| Page 4 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_004.png` | 4 |
| Page 5 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_005.png` | 5 |
| Page 6 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_006.png` | 6 |
| Page 7 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_007.png` | 7 |
| Page 8 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_008.png` | 8 |
| Page 9 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_009.png` | 9 |
| Page 10 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_010.png` | 10 |
| Page 11 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_011.png` | 11 |
| Page 12 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_012.png` | 12 |
| Page 13 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_013.png` | 13 |
| Page 14 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_014.png` | 14 |
| Page 15 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_015.png` | 15 |
| Page 16 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_016.png` | 16 |
| Page 17 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_017.png` | 17 |
| Page 18 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_018.png` | 18 |
| Page 19 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_019.png` | 19 |
| Page 20 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_020.png` | 20 |
| Page 21 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_021.png` | 21 |
| Page 22 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_022.png` | 22 |
| Page 23 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_023.png` | 23 |
| Page 24 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_024.png` | 24 |
| Page 25 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_025.png` | 25 |
| Page 26 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_026.png` | 26 |
| Page 27 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_027.png` | 27 |
| Page 28 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_028.png` | 28 |
| Page 29 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_029.png` | 29 |
| Page 30 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_030.png` | 30 |
| Page 31 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_031.png` | 31 |
| Page 32 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_032.png` | 32 |
| Page 33 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_033.png` | 33 |
| Page 34 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_034.png` | 34 |
| Page 35 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_035.png` | 35 |
| Page 36 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_036.png` | 36 |
| Page 37 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_037.png` | 37 |
| Page 38 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_038.png` | 38 |
| Page 39 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_039.png` | 39 |
| Page 40 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/page_040.png` | 40 |
| embedded_001 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_013.jpg` | Embedded raster image |
| embedded_014 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_014.jpg` | Embedded raster image |
| embedded_015 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_015.jpg` | Embedded raster image |
| embedded_016 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_016.jpg` | Embedded raster image |
| embedded_017 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_017.jpg` | Embedded raster image |
| embedded_018 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_018.jpg` | Embedded raster image |
| embedded_019 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_019.jpg` | Embedded raster image |
| embedded_020 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_023.jpg` | Embedded raster image |
| embedded_024 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_024.png` | Embedded raster image |
| embedded_025 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_025.png` | Embedded raster image |
| embedded_026 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_026.png` | Embedded raster image |
| embedded_027 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_028.png` | Embedded raster image |
| embedded_029 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_029.jpg` | Embedded raster image |
| embedded_030 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_030.jpg` | Embedded raster image |
| embedded_031 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_031.jpg` | Embedded raster image |
| embedded_032 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_032.jpg` | Embedded raster image |
| embedded_033 | `assets/Lecture13_Stats_refresher_b8c1f353-a201-4d59-91fb-a8fc4522cf30/embedded_033.jpg` | Embedded raster image |

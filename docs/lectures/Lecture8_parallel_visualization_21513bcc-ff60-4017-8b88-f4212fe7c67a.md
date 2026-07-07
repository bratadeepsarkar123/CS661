---
title: "Lecture8 parallel visualization"
source_pdf: "markdown_files/lecture pdf/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a.pdf"
converted: 2026-07-07
pages: 45
---

# Lecture8 parallel visualization

**Source:** `markdown_files/lecture pdf/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a.pdf`  
**Converted:** 2026-07-07  
**Pages:** 45

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

<!-- Page 3 -->
3
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Study Materials for Lecture 8
• Parallel Algorithms:
• https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-
computing-tutorial
• Parallel Volume Rendering Using Binary Swap Image Composition, Ma et al.
• Parallel Volume Rendering on the IBM Blue Gene/P, Peterka et al.

<!-- Page 4 -->
4
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Accelerating Volume Rendering
• Early ray termination
• Empty space skipping
• Adaptive sampling

<!-- Page 5 -->
5
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Early Ray Termination
• In front to back compositing, we keep track of accumulated opacities 
separately
• We can stop ray traversal when accumulated alpha/opacity for a ray 
reaches 1 and nothing behind will be visible

<!-- Page 6 -->
6
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Empty Region Skipping
• Skip Empty Cells
• Homogeneity acceleration
• Approximate homogeneous regions 
with fewer sample points

<!-- Page 7 -->
7
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Adaptive Sampling
• Increase sample density in high-gradient regions
• Decrease sample density in low-gradient/homogeneous regions

<!-- Page 8 -->
8
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Dealing with Large-Scale Data 
via Parallel Data Processing 
and Visualization

<!-- Page 9 -->
9
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Why Parallel Programming?
• Utilize the aggregated memory from all computing elements to store 
very large data sets
• Utilize the aggregated compute power to share the expensive task 
workload 
• Utilize the aggregated I/O bandwidth, if a parallel file system is 
available 
• Data computed from large scale simulations are typically stored in a 
file system connected to a supercomputer

<!-- Page 10 -->
10
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Computing Paradigms 
• Shared-memory parallelism 
• Distributed-memory parallelism 
• Hybrid parallelism

<!-- Page 11 -->
11
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Shared Memory Parallelism
• Shared-memory parallelism 
• All PEs can access the shared memory, hence have the same view of the data 
• No explicit message passing is needed 
• Computation are done through multiple threads (libraries such as OpenMP) 
https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial

<!-- Page 12 -->
12
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Distributed Memory Parallelism
• Distributed-memory parallelism 
• Data are distributed across the local memory of different Processing 
Element (PE) 
• Coordination among PEs is done through message passing (libraries such as 
MPI) 
• Tasks are run on each core within each processing node 
https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial

<!-- Page 13 -->
13
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Hybrid Parallelism
• Hybrid parallelism
• Hybrid parallelism refers to a blend of distributed- and shared-memory parallel 
programming techniques within a single application
• Each node has multiple threads running shared memory parallelism, but nodes have 
distributed memory and communicate with one another using message passing 
• Most modern clusters and supercomputers provide hybrid parallelism capability 
https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial

<!-- Page 14 -->
14
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Programming API – Shared Memory
• Open Multi-Processing (OpenMP) - Shared Memory Parallelism
• Latest OpenMP versions also supports GPUs
https://docs.nersc.gov/development/programming-models/openmp/
https://www.openmp.org/

<!-- Page 15 -->
15
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Programming API – Shared Memory
• Open Multi-Processing (OpenMP) - Shared Memory Parallelism
• Latest OpenMP versions also supports GPUs
https://docs.nersc.gov/development/programming-models/openmp/
https://www.openmp.org/

<!-- Page 16 -->
16
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Programming API – Distributed Memory
• Message Passing Interface (MPI) – Distributed Parallelism
Network
Node 1
Node 2
Param Sanganak at IITK
Total number of nodes: 332 (20 + 312) 
o Service nodes: 20 (Master+ Login+ Service+ Management) 
o CPU only nodes: 150  (Total 7200 cores, 28800GB memory)
o GPU nodes: 20 
o High Memory nodes:78
https://www.hpc.iitk.ac.in/static/paramsanganak/documents/PARAM_Sanganak-User-Manual.pdf
• Different implementations of MPI:
• Open MPI (https://www.open-mpi.org/)
• MVAPICH (https://mvapich.cse.ohio-state.edu/)
• MPICH (https://www.mpich.org/)

<!-- Page 17 -->
17
IITK CS661: Big Data Visual Analytics: Soumya Dutta
OpenMP vs MPI
MPI
OpenMP
Available from different vendors and gets compiled on 
Windows, macOS, and Linux operating systems.
An add-on in a compiler such as a GNU compiler and 
Intel compiler.
Supports parallel computation for distributed-memory 
and shared-memory systems.
Supports parallel computation for shared-memory 
systems only.
A process-based parallelism.
A thread-based parallelism.
With MPI, each process has its own memory space 
and executes independently from the other processes.
With OpenMP, threads share the same resources and 
access shared memory.
Processes exchange data by passing messages to each 
other.
There is no notion of message-passing. Threads access 
shared memory.
Process creation overhead occurs one time.
It depends on the implementation. More overhead 
can occur when creating threads to join a task.
https://hpc.nmsu.edu/discovery/mpi/mpi-openmp/

<!-- Page 18 -->
18
IITK CS661: Big Data Visual Analytics: Soumya Dutta
OpenMP vs MPI: Hello World

<!-- Page 19 -->
19
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Steps for a Parallel Distributed Algorithm
• Data Decomposition
• Distribute decomposed data to processors
• Parallelly process data and apply the algorithm, communicate if 
needed
• Aggregate partial results from different processors to produce the 
final result

<!-- Page 20 -->
20
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Decomposition
After decomposition, data blocks are distributed to processors 
Large Data

<!-- Page 21 -->
21
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Distribution
• After decomposition, data blocks 
need to be distributed to 
processors 
• Proper distribution is critical for 
the overall performance and 
minimizing overhead
• What overhead?
• Load imbalance
• Communication of data over 
network among processors
• Synchronization

<!-- Page 22 -->
22
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Distribution Techniques
• Contiguous distributions

<!-- Page 23 -->
23
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Distribution Techniques
• Block cyclic (round robin) 
distribution

<!-- Page 24 -->
24
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Data Distribution Techniques
• Workload aware

<!-- Page 25 -->
25
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Data Processing and Aggregation of 
Partial Results

<!-- Page 26 -->
26
IITK CS661: Big Data Visual Analytics: Soumya Dutta
How to Ensure Continuity at Boundaries
• Need ‘Ghost cells’
• For interpolation-based tasks, we need to replicate and share boundary data 
points with neighboring processors
• Cells in the duplicated layers are called ghost cells

<!-- Page 27 -->
27
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Isosurface Extraction and 
Parallel Volume Rendering

<!-- Page 28 -->
28
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Isosurface Extraction
• Parallel Marching Cubes (Squares)
• Observation: Each cell can be 
processed in parallel as there is no 
dependency among cells
• Steps:
• Divide the data into chunks of equal size 
• Each processing element (processor) 
runs Marching Cubes for the cells in the 
chucks that are assigned to it 
• Return the resulting triangles back to a 
master node, or render the triangles if 
parallel rendering is desired

<!-- Page 29 -->
29
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Volume Rendering
• Parallel Volume Rendering
• Parallel by pixel – Fits better for Shared memory approach
•
No image compositing needed
•
No communication 
•
Full data need to be accessible 
by all threads 
•
Difficult to scale to large data

<!-- Page 30 -->
30
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Volume Rendering
• Parallel Volume Rendering
• Parallel by pixel – Fits better for Shared memory approach
• Parallel by data – Fits better for Distributed Memory approach
•
Image compositing needed 
•
Communication needed
•
Data are distributed
•
Easy to scale to large data 
•
No image compositing needed
•
No communication 
•
Full data need to be accessible 
by all threads 
•
Difficult to scale to large data

<!-- Page 31 -->
31
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Volume Rendering
Parallel Volume Rendering on the IBM Blue Gene/P, Peterka et al.
How to do this compositing in parallel efficiently?

<!-- Page 32 -->
32
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering
• Composite partial images generated from sub-domains 
• Minimize communication: send and receive images 
• Compositing needs to follow the visibility order of ray casting 
technique

<!-- Page 33 -->
33
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering

<!-- Page 34 -->
34
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Load balancing is not good: Only 
half of the processors are busy at 
every new stage 
Parallel Image Compositing for Volume Rendering

<!-- Page 35 -->
35
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving

<!-- Page 36 -->
36
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving 
Divide each image into two halves, and give half to the other PE to composite

<!-- Page 37 -->
37
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving 
Divide each image into two halves, and give half to the other PE to composite

<!-- Page 38 -->
38
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving 
Divide the half image further into top and bottom halves, and give it to the corresponding PE of to composite

<!-- Page 39 -->
39
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving 
Divide the half image further into top and bottom halves, and give it to the corresponding PE of to composite

<!-- Page 40 -->
40
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving 
Divide the 1/4 image further into left and right halves, and give it to the corresponding PE of to composite

<!-- Page 41 -->
41
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving 
Divide the 1/4 image further into left and right halves, and give it to the corresponding PE of to composite

<!-- Page 42 -->
42
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Parallel Image Compositing for Volume Rendering: 
A better strategy
• keep every processor (PE) busy all the time
• Recursive halving 
Divide the 1/4 image further into left and right halves, and give it to the corresponding PE of to composite 
Load balanced 
approach: all 
processors are 
busy with equal 
workload at all 
the time

<!-- Page 43 -->
43
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Hybrid Parallel Volume Rendering
• Use MPI + OpenMP together to extract fine grained parallelism for 
very large-scale data set
Network
Static/Dynamic Analyses for Validation and Improvements of Multi-Model HPC Applications.
Node A
Node B

<!-- Page 44 -->
44
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Hybrid Parallel Volume Rendering
• Use MPI + OpenMP together to extract fine grained parallelism for 
very large-scale data set
1/2 Data
1/2 Data
Network
Static/Dynamic Analyses for Validation and Improvements of Multi-Model HPC Applications.
Data Decomposition
Node A
Node B

<!-- Page 45 -->
45
IITK CS661: Big Data Visual Analytics: Soumya Dutta
Hybrid Parallel Volume Rendering
• Use MPI + OpenMP together to extract fine grained parallelism for 
very large-scale data set
1/2 Data
1/2 Data
Each OpenMP thread 
inside node A casts a 
ray into the sub-volume
Network
Static/Dynamic Analyses for Validation and Improvements of Multi-Model HPC Applications.
Each OpenMP thread 
inside node B casts a 
ray into the sub-volume
Data Decomposition
Node A
Node B

## Figures

### Page 1

![Page 1](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_001.png)

### Page 2

![Page 2](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_002.png)

### Page 3

![Page 3](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_003.png)

### Page 4

![Page 4](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_004.png)

### Page 5

![Page 5](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_005.png)

### Page 6

![Page 6](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_006.png)

### Page 7

![Page 7](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_007.png)

### Page 8

![Page 8](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_008.png)

### Page 9

![Page 9](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_009.png)

### Page 10

![Page 10](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_010.png)

### Page 11

![Page 11](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_011.png)

### Page 12

![Page 12](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_012.png)

### Page 13

![Page 13](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_013.png)

### Page 14

![Page 14](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_014.png)

### Page 15

![Page 15](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_015.png)

### Page 16

![Page 16](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_016.png)

### Page 17

![Page 17](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_017.png)

### Page 18

![Page 18](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_018.png)

### Page 19

![Page 19](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_019.png)

### Page 20

![Page 20](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_020.png)

### Page 21

![Page 21](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_021.png)

### Page 22

![Page 22](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_022.png)

### Page 23

![Page 23](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_023.png)

### Page 24

![Page 24](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_024.png)

### Page 25

![Page 25](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_025.png)

### Page 26

![Page 26](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_026.png)

### Page 27

![Page 27](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_027.png)

### Page 28

![Page 28](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_028.png)

### Page 29

![Page 29](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_029.png)

### Page 30

![Page 30](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_030.png)

### Page 31

![Page 31](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_031.png)

### Page 32

![Page 32](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_032.png)

### Page 33

![Page 33](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_033.png)

### Page 34

![Page 34](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_034.png)

### Page 35

![Page 35](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_035.png)

### Page 36

![Page 36](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_036.png)

### Page 37

![Page 37](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_037.png)

### Page 38

![Page 38](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_038.png)

### Page 39

![Page 39](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_039.png)

### Page 40

![Page 40](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_040.png)

### Page 41

![Page 41](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_041.png)

### Page 42

![Page 42](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_042.png)

### Page 43

![Page 43](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_043.png)

### Page 44

![Page 44](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_044.png)

### Page 45

![Page 45](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_045.png)

## Embedded Images

### embedded_001

![embedded_001](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_001.jpg)

### embedded_002

![embedded_002](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_002.jpg)

### embedded_003

![embedded_003](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_003.jpg)

### embedded_004

![embedded_004](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_004.jpg)

### embedded_005

![embedded_005](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_005.jpg)

### embedded_006

![embedded_006](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_006.jpg)

### embedded_007

![embedded_007](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_007.jpg)

### embedded_008

![embedded_008](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_008.jpg)

### embedded_009

![embedded_009](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_009.jpg)

### embedded_010

![embedded_010](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_010.jpg)

### embedded_011

![embedded_011](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_011.jpg)

### embedded_012

![embedded_012](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_012.jpg)

### embedded_013

![embedded_013](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_013.png)

### embedded_014

![embedded_014](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_014.png)

### embedded_015

![embedded_015](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_015.png)

### embedded_016

![embedded_016](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_016.png)

### embedded_017

![embedded_017](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_017.png)

### embedded_018

![embedded_018](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_018.png)

### embedded_019

![embedded_019](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_019.png)

### embedded_020

![embedded_020](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_020.jpg)

### embedded_021

![embedded_021](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_021.jpg)

### embedded_022

![embedded_022](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_022.jpg)

### embedded_023

![embedded_023](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_023.jpg)

### embedded_024

![embedded_024](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_024.jpg)

### embedded_025

![embedded_025](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_025.jpg)

### embedded_026

![embedded_026](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_026.jpg)

### embedded_027

![embedded_027](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_027.jpg)

### embedded_028

![embedded_028](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_028.png)

### embedded_029

![embedded_029](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_029.png)

### embedded_030

![embedded_030](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_030.png)

### embedded_031

![embedded_031](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_031.png)

### embedded_032

![embedded_032](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_032.jpg)

### embedded_033

![embedded_033](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_033.jpg)

### embedded_034

![embedded_034](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_034.jpg)

### embedded_035

![embedded_035](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_035.png)

### embedded_036

![embedded_036](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_036.png)

### embedded_037

![embedded_037](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_037.png)

### embedded_038

![embedded_038](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_038.png)

### embedded_039

![embedded_039](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_039.png)

### embedded_040

![embedded_040](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_040.png)

### embedded_041

![embedded_041](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_041.png)

### embedded_042

![embedded_042](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_042.png)

### embedded_043

![embedded_043](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_043.png)

### embedded_044

![embedded_044](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_044.jpg)

### embedded_045

![embedded_045](assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_045.jpg)

## Table of Figures

| Figure | Asset | Description |
|--------|-------|-------------|
| Page 1 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_001.png` | Big Data Visual Analytics (CS 661) |
| Page 2 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_002.png` | 2 |
| Page 3 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_003.png` | 3 |
| Page 4 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_004.png` | 4 |
| Page 5 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_005.png` | 5 |
| Page 6 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_006.png` | 6 |
| Page 7 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_007.png` | 7 |
| Page 8 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_008.png` | 8 |
| Page 9 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_009.png` | 9 |
| Page 10 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_010.png` | 10 |
| Page 11 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_011.png` | 11 |
| Page 12 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_012.png` | 12 |
| Page 13 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_013.png` | 13 |
| Page 14 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_014.png` | 14 |
| Page 15 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_015.png` | 15 |
| Page 16 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_016.png` | 16 |
| Page 17 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_017.png` | 17 |
| Page 18 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_018.png` | 18 |
| Page 19 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_019.png` | 19 |
| Page 20 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_020.png` | 20 |
| Page 21 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_021.png` | 21 |
| Page 22 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_022.png` | 22 |
| Page 23 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_023.png` | 23 |
| Page 24 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_024.png` | 24 |
| Page 25 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_025.png` | 25 |
| Page 26 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_026.png` | 26 |
| Page 27 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_027.png` | 27 |
| Page 28 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_028.png` | 28 |
| Page 29 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_029.png` | 29 |
| Page 30 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_030.png` | 30 |
| Page 31 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_031.png` | 31 |
| Page 32 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_032.png` | 32 |
| Page 33 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_033.png` | 33 |
| Page 34 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_034.png` | 34 |
| Page 35 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_035.png` | 35 |
| Page 36 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_036.png` | 36 |
| Page 37 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_037.png` | 37 |
| Page 38 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_038.png` | 38 |
| Page 39 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_039.png` | 39 |
| Page 40 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_040.png` | 40 |
| Page 41 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_041.png` | 41 |
| Page 42 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_042.png` | 42 |
| Page 43 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_043.png` | 43 |
| Page 44 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_044.png` | 44 |
| Page 45 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/page_045.png` | 45 |
| embedded_001 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_001.jpg` | Embedded raster image |
| embedded_002 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_002.jpg` | Embedded raster image |
| embedded_003 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_003.jpg` | Embedded raster image |
| embedded_004 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_004.jpg` | Embedded raster image |
| embedded_005 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_005.jpg` | Embedded raster image |
| embedded_006 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_006.jpg` | Embedded raster image |
| embedded_007 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_007.jpg` | Embedded raster image |
| embedded_008 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_008.jpg` | Embedded raster image |
| embedded_009 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_009.jpg` | Embedded raster image |
| embedded_010 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_010.jpg` | Embedded raster image |
| embedded_011 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_011.jpg` | Embedded raster image |
| embedded_012 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_012.jpg` | Embedded raster image |
| embedded_013 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_013.png` | Embedded raster image |
| embedded_014 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_014.png` | Embedded raster image |
| embedded_015 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_015.png` | Embedded raster image |
| embedded_016 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_016.png` | Embedded raster image |
| embedded_017 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_017.png` | Embedded raster image |
| embedded_018 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_018.png` | Embedded raster image |
| embedded_019 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_019.png` | Embedded raster image |
| embedded_020 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_020.jpg` | Embedded raster image |
| embedded_021 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_021.jpg` | Embedded raster image |
| embedded_022 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_022.jpg` | Embedded raster image |
| embedded_023 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_023.jpg` | Embedded raster image |
| embedded_024 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_024.jpg` | Embedded raster image |
| embedded_025 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_025.jpg` | Embedded raster image |
| embedded_026 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_026.jpg` | Embedded raster image |
| embedded_027 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_027.jpg` | Embedded raster image |
| embedded_028 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_028.png` | Embedded raster image |
| embedded_029 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_029.png` | Embedded raster image |
| embedded_030 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_030.png` | Embedded raster image |
| embedded_031 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_031.png` | Embedded raster image |
| embedded_032 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_032.jpg` | Embedded raster image |
| embedded_033 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_033.jpg` | Embedded raster image |
| embedded_034 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_034.jpg` | Embedded raster image |
| embedded_035 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_035.png` | Embedded raster image |
| embedded_036 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_036.png` | Embedded raster image |
| embedded_037 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_037.png` | Embedded raster image |
| embedded_038 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_038.png` | Embedded raster image |
| embedded_039 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_039.png` | Embedded raster image |
| embedded_040 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_040.png` | Embedded raster image |
| embedded_041 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_041.png` | Embedded raster image |
| embedded_042 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_042.png` | Embedded raster image |
| embedded_043 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_043.png` | Embedded raster image |
| embedded_044 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_044.jpg` | Embedded raster image |
| embedded_045 | `assets/Lecture8_parallel_visualization_21513bcc-ff60-4017-8b88-f4212fe7c67a/embedded_045.jpg` | Embedded raster image |

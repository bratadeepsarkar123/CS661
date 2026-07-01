# CS661: Project Proposal Report
## The Global Knowledge & Wealth Paradox

**Group 10**  
**June 23, 2026**

## 1 Introduction

Academic research plays a crucial role in driving innovation, developing skilled talent, and supporting economic growth. However, the global research landscape is far from uniform. While a large share of research funding is concentrated in wealthier nations, countries differ significantly in how effectively they translate these investments into scientific output and impact. Our project presents a web-based interactive visual analytics platform designed to explore and understand the global academic ecosystem. By combining economic indicators with publication metrics and institutional data, the platform helps examine how countries convert financial resources into research excellence. It highlights patterns, identifies outliers, and explores the role of factors such as purchasing power and economic conditions in shaping research performance. In addition, the project provides a focused analysis of India's rapidly growing higher education and research sector. Through intuitive visualizations, users can track how different countries have contributed to the global academic landscape over time and observe changes in both the quantity and quality of research at the global level as well as within India. The goal is to make complex research trends accessible, enabling deeper insights into the factors that influence scientific progress worldwide.

## 2 Data Sources

To capture the intersections between economics, institutional scale, and scientific impact, our system will ingest and clean data from the following open repositories:

* **Macroeconomical Parameters:** World Bank (WB) API, OECD MSTI (Main Science and Technology Indicators), OpenAlex, SCImago Journal Country Rank (SJR) Kaggle Dataset. Contains Core Parameters for 243 countries/governing regions over 29 years.
* **Journal Ranking and Publishing Volume Data:** SCImago Journal & Country Rank (Scopus) Database Name: SCImago Journal & Country Rank (SJR) Contains data from 135 countries and a total of 75539 unique journals over 27 years.
* **Dynamic Evolution of Top Research Topics Over Time (1950-2025) and Citation Data for Domestic and International Citation Impact:** OpenAlex. Data of 228 countries and 7 unique topics over 75 years classifying 8,158,030 publications.
* **India Domestic Higher Education Network:** OpenAlex, NIRF, AISHE, SCImago Institutions Rankings (SIR). Individual Research and Collaboration Data of 45000+ Indian Colleges by year for 2015-2024

## 3 Specific Tasks

To execute this project with our 8-member team, we will complete the following operational stages:

* **Multi-Source Data Consolidation:** Ingest and reconcile open datasets spanning national macroeconomics (World Bank, UNESCO UIS), bibliometric indices (OpenAlex, SCImago SJR/SIR), and India-specific institutional records (NIRF, AISHE, ROR). Build a unified schema linking countries, institutions, publication years, and quality tiers.
* **Data Normalization and Preprocessing:** Clean heterogeneous naming across sources, compute year-wise publication and citation metrics, and derive tier-level aggregates (e.g., premier vs. state/affiliated) for the India deep-dive module.
* **Interactive Visualization Engineering:** Implement a single-screen visual analytics dashboard with five linked modules high-dimensional peer clustering (t-SNE/UMAP), global quality shift (ridgeline), top research topics (bar chart race), collaboration premium (dumbbell plot), and India's domestic higher-education collaboration network (geospatial node-link map).
* **Analytical Storytelling and Inference:** Encode comparative narratives across modules wealth vs. research behavior, Q1/Q4 quality divergence, field momentum, international co-authorship citation gain, and domestic elite state asymmetry in India using consistent cross-year filtering and documented metric definitions.
* **Cross-Filter and Integration Layer:** Provide shared controls (global year slider, hover tooltips, sortable encodings, and panel expand/back navigation) so users can compare countries, fields, and institutional tiers without page reloads. Backend pre-computation (Python/Pandas) feeds a React + D3.js frontend for responsive interaction.

## 4 Visualization Tasks

Our visual analytics platform will feature five core interactive visualization plots on a single 1080p overview screen, each expandable to fullscreen for detail-on-demand exploration:

### 4.1 High-Dimensional Peer Clustering (t-SNE / UMAP)

This module projects countries from a high-dimensional space of macroeconomic and academic indicators (R&D spend, GDP, publications, citations etc.) into 2D using t-SNE/UMAP. The goal is to reveal *scientific peer groups*, nations that behave similarly in research and funding, independent of geographic proximity.

* **Interactions:** Users hover over nodes for country-level metric tooltips, brush or click to highlight clusters, and optionally sync with a global year filter to observe how membership in performance groups shifts over time (e.g., convergence of resource-rich economies toward mid-tier European profiles, or China's trajectory relative to India).
* **Visuals:** A 2D scatter plot with one node per country; **node size** encodes total publication volume and **color** encodes regional affiliation. Overview shows the clustered layout at a glance; fullscreen enables richer labeling, zoom, and trajectory emphasis for selected countries.

### 4.2 Global Quality Shift (Ridgeline / Joyplot)

This module tracks how the global mix of publication quality evolves over time by contrasting elite (Q1) and low-tier (Q4) output. It visualizes whether the research ecosystem is polarizing, a "Q4 flood" alongside an "elite breakaway", rather than remaining near historical parity.

* **Interactions:** A year slider (with optional play/pause) animates ridgeline rows across the timeline. Hover highlights a single year or country slice; users can read structural shifts such as divergence from an early near-parity baseline toward separated quality tiers in recent decades.
* **Visuals:** A time-series ridgeline plot with overlapping density curves per year. Color encodes quality tier (Q1 vs Q4); restrained annotations mark key transitions (e.g., parity baseline, elite breakaway, Q4 surge). Overview shows the headline trend; fullscreen exposes finer year-by-year comparison.

### 4.3 Top-10 Research Topics (Bar Chart Race)

This module ranks the ten most-published research topics globally (or for a filtered region) and shows how field prominence changes across years: for example, the rise of AI and Machine Learning, genomics, infectious-disease research, or newer fields such as urban sustainability.

* **Interactions:** Timeline controls (play, pause, scrub, speed) advance year-by-year; bars reorder in real time as ranks change. Users can spot upward/downward momentum and the entry or exit of topics from the top 10.
* **Visuals:** An animated horizontal bar chart race: **Y-axis** = topic rank (dynamic sorting), **X-axis** = publication volume, **color** = field/category. Overview shows the current top 10 snapshot; fullscreen widens labels and controls for longer field names and finer year stepping.

### 4.4 The Collaboration Premium (Dumbbell Plot)

This module quantifies whether internationally co-authored research receives higher citation impact than domestic-only work. It tests the "collaboration premium," the citation gap between purely domestic papers and papers with foreign co-authors, across countries.

* **Interactions:** Users sort by domestic impact, international impact, citation gain, or country name. Hover reveals exact citation rates and sample context; sorting exposes outliers (e.g., economies where elite output depends heavily on external partnerships).
* **Visuals:** A horizontal dumbbell plot per country: left marker = domestic citation impact, right marker = international impact, connecting line = citation gain. Distinct marker shapes or colors separate domestic vs international encoding. Overview shows top countries by gain; fullscreen shows the full ranked list.

### 4.5 India Domestic Higher Education Network (Geospatial Node-Link Map)

This module maps India’s *domestic* higher-education collaboration landscape: who co-publishes with whom inside India, and how elite institutions (IITs, IISc, top central universities) differ from the state and affiliated tier in output, quality, and funding.

* **Interactions:** Overview shows a sparse hub map and a one-line tier comparison. Clicking the panel opens fullscreen: ~80 institutions, hub corridors (NCR, Bengaluru, Mumbai, Chennai), and focus+context on node click (highlight ego-network, detail card with Funding | Publications tabs). A global year slider updates edges and volumes; international co-authorship counts toward institution size but not domestic edge drawing.
* **Visuals:** Geospatial node-link map on an India outline: **position** = latitude/longitude, **node color** = tier (premier vs state/affiliated), **node area** = total publication volume (√ scaling), **edge width** = domestic co-publication count. Fullscreen adds tier comparison panels (citations/paper, Q1%, funding); overview limits labels to ~12 hubs and hub-to-hub edges only. A graphical-integrity footnote states that ~120 research-active institutions appear on the map while broader affiliated-college scale is represented in tier aggregates.

## 5 Overall Solution

The final system will be deployed as a single-page, web-based interactive data application. Rather than using standard scrolling templates, the dashboard will operate like an integrated software interface featuring persistent control panels for filtering and querying parameters. The interface will allow users to conduct comparative analyses across countries, institutions, and years. This will help them uncover how funding profiles, economic conditions, and national systems alter the trajectory of global academic research.

## 6 Tech Stack

To satisfy the requirements of building a tailored visualization layout from scratch, our architecture is defined as follows:

* **Data Engineering:** Python batch pipelines (Pandas, Requests, PyArrow) for multi-source ingestion, PPP normalization, and export of pre-computed JSON payloads.
* **Frontend Application:** JavaScript (React.js with Vite) coupled with D3.js for rendering responsive network topologies, geographical maps, and custom interactive charts.
* **Data Storage:** CSV and Parquet during ETL, with compact JSON files served to the frontend for low-latency interaction.

## 7 Team Members & Responsibilities

To ensure equal and balanced individual contributions, our 7-member group is organized into clear operational verticals:

### Core Project Tasks

* **1. Data Processing & Database Setup**
    * **What to do:** Gather the data, clean up missing text, convert economic values, and set up the server and database to store everything safely.
    * **Assigned to:** Bratadeep Sarkar(240285) & Amgoth Rahul(240108)

* **2. Building All Visual Charts & Maps**
    * **What to do:** Code all the visual elements, including the interactive map of universities, the animated bar charts, and the 2D scatter plots.
    * **Assigned to:** Nikhil Patel(240696) & Prakhar Patel(240767)

* **3. Frontend Website Development**
    * **What to do:** Build the main single-page website using React so users have a place to view and interact with all the charts.
    * **Assigned to:** Abhinav Bhardwaj(240030) & Saksham Agrahari(240911)

* **4. Interactive Filters & Controls**
    * **What to do:** Write the code that connects the user interface to the data, allowing the charts to update automatically when a user clicks buttons or moves sliders.
    * **Assigned to:** Aditya Chittora(240054) & Nikhil Patel(240696)

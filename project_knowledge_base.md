# Project Knowledge Base

This document serves as a persistent store for meaningful discoveries, dataset details, feasibility reports, and overarching project goals. It will be updated iteratively so that any future agent can start with full context.

## 1. Project Context
- **Course**: CS661 Big Data Visual Analytics (IIT Kanpur)
- **Goal**: Build a highly complex, interactive visual analytics system from scratch (using Dash, Plotly, D3.js) focusing on domain-driven storytelling and dimensionality reduction.
- **Key Requirement**: Must process large datasets, avoiding standard static dashboards.

## 2. Dataset Feasibility Tracking
- **UNESCO UIS - GERD Data**: 
  - *Status*: Feasibility check COMPLETE.
  - *Target*: Gross domestic expenditure on R&D for ~180 countries x 30 years.
  - *Findings*: **Web scraping is NOT required.** The UNESCO UIS provides a direct Data API and Bulk Data Download Service (BDDS). The data can be programmatically fetched natively in JSON/CSV formats without hitting CAPTCHAs or dynamic rendering blockers.
  - *Code Reference*: The Scraper Agent created a working Python script utilizing the `unesco_reader` package at `C:\Users\brata\.gemini\antigravity\scratch\test_uis_data.py`. The script targets `indicatorCode: EXPGDP.TOT` and successfully retrieves 3,867 records.

## 3. Summarization Progress
- **Document**: `gemini_chats.md`
- **Progress**: **100% COMPLETE**. The entire ~1600 line document has been incrementally summarized in chunks and saved securely to `gemini_chats_summary.md`.

### Chunk 1 Summary: Intro & Project Idea 1
- **Course Context**: CS661 Big Data Visual Analytics (IIT Kanpur). Projects must use advanced interactive systems (Dash/Plotly/D3.js) and dimensionality reduction instead of basic dashboards.
- **EcoScan (Project 1)**: Environmental Data Science & Climate Change.
  - *Data*: CO2 emissions merged with World Bank socio-economic/vulnerability metrics.
  - *Story*: Correlating economic profile with environmental damage and vulnerability.
  - *Key Tasks*: High-dimensional cluster inspection (UMAP/t-SNE), PCA feature contribution biplots, temporal trajectory tracking, dynamic cross-filtering sandboxes, and geographical mapping versus climate risk charts.

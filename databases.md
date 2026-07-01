# CS661 Visual Analytics Datasets

This document tracks all the databases we are compiling to answer our complex visualization questions (such as comparing IIT Kanpur vs. TUM Germany, analyzing how they publish, how they are funded, and the quality of life for scientists).

## Core Datasets (Encountered So Far)

| Dataset | Source / URL | What It Contains (Scale) |
| :--- | :--- | :--- |
| **UNESCO UIS - GERD Data** | stats.uis.unesco.org | Global research funding metrics, GERD by sector (~180 countries x 30 years) |
| **World Bank Open Data** | data.worldbank.org | Macroeconomic indicators (GDP, PPP, PCI) & publication counts (200+ countries x 60+ years) |
| **SCImago (SJR)** | scimagojr.com | Country-level scientometrics, Q1-Q4 journal distributions, h-index (240 countries, 1996-2024) |
| **Times Higher Education (THE)** | timeshighereducation.com | Global university rankings and scaling metrics (2000+ universities) |
| **NIRF Rankings** | nirfindia.org | Institutional rankings specifically for India (5000+ institutions) |
| **OpenAlex** | openalex.org | Massive bibliometric graph: papers, citations, authors, institutional networks (250M+ papers) |
| **Semantic Scholar** | semanticscholar.org | Open academic graph of papers and citations (200M+ records) |
| **Crossref** | crossref.org | DOI registration metadata for publications (~130M records) |
| **Leiden Ranking Raw Data** | leidenranking.com | University collaboration indexes and scientific impact metrics (1400+ universities) |
| **IMF World Economic Outlook** | imf.org | Global economic data (190 countries) |
| **OECD Statistics / MSTI** | stats.oecd.org | Highly granular R&D stats for OECD members (38 countries + partners, since 1981) |
| **UN Human Development Index** | hdr.undp.org | Quality of life, education, and life expectancy metrics (191 countries) |
| **NSF HERD Survey** | ncses.nsf.gov | Granular R&D spending for every US university, broken down by field and source |
| **AISHE** | aishe.gov.in | Indian university enrollment and faculty data |
| **DST / NSTMIS** | dst.gov.in | Indian national R&D spend by sector |
| **UGC Recognized Institutions** | ugc.gov.in | Location and type data for Indian universities |
| **National Bureau of Statistics China** | data.stats.gov.cn/english/ | Annual R&D by sector for China |

---

## Newly Discovered Datasets (For Institutional Deep-Dives)

To answer the new questions specifically focusing on the institutional scale (e.g., IIT Kanpur vs. TUM), publication mechanisms, and the "Life of a Scientist," we will incorporate the following new datasets:

### 1. "How each publishes its research" (Open Access vs. Closed, Collaboration Types)
| Dataset | Source / URL | What It Contains (Scale) |
| :--- | :--- | :--- |
| **Unpaywall API** | unpaywall.org | Database of open access (OA) scholarly articles. Maps DOIs to free PDFs. Crucial for seeing if a university locks its research behind paywalls. (50M+ OA records) |
| **DOAJ** | doaj.org | Directory of Open Access Journals metadata. |
| **Dimensions.ai** | dimensions.ai | Links publications directly to grants, patents, and clinical trials. (Freemium API available for scientometrics). |

### 2. "How much money it gets for research" (Grant-Level / Institutional Funding)
| Dataset | Source / URL | What It Contains (Scale) |
| :--- | :--- | :--- |
| **CORDIS (EU Research)** | cordis.europa.eu | The European Commission's primary source for EU-funded research projects (Horizon Europe/Horizon 2020). Vital for checking TUM Germany's funding. |
| **NIH RePORTER** | reporter.nih.gov | US biomedical grants (excellent for comparing US elite institution budgets). |
| **Gateway to Research (GtR)** | gtr.ukri.org | UK research grant funding data. |

### 3. "What life is like for scientists there" (Quality of Life, Salaries, Cost of Living)
| Dataset | Source / URL | What It Contains (Scale) |
| :--- | :--- | :--- |
| **Numbeo / Expatistan Cost of Living** | numbeo.com | Massive crowdsourced cost-of-living data by city (e.g., Kanpur vs. Munich). Vital for converting nominal scientist salaries into true local purchasing power. |
| **Academic Salaries / AAUP** | aaup.org / H1B Data | Datasets regarding professor and post-doc compensation globally. |
| **World Happiness Report Data** | worldhappiness.report | Gallup World Poll data scoring social support, freedom to make life choices, and corruption perceptions by country. |
| **Scholars at Risk (SAR) Index** | scholarsatrisk.org | Tracks academic freedom and incidents restricting scientific inquiry globally. |

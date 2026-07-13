# River owners (locked)

**Date:** 2026-07-12  
**Clean channel:** `CS661_Dataset/raw_vault/READY_FOR_TEAM/`  
**Guide:** `RIVER_PIPELINE_REPORT.md`

One owner per metric label. Taps must not invent values. Distinct “publications” rivers keep distinct UI names.

| Metric label | Owner river | Pool / consumer | Forbidden |
|--------------|-------------|-----------------|-----------|
| **Country H-index (display / UMAP / G2)** | OpenAlex **calendar-year cohort H (W=1)** → `country_year_h_openalex_cohort.csv` → panel `H_Index` / `H_Index_Yearly` — see [`G1_CUSTOM_YEARLY_H.md`](G1_CUSTOM_YEARLY_H.md) | G1 `viz1_data.js` (`H_Index`); G2 sidebar **join from VIZ1** (same field) | G2 `base + 2×(year−1999)`; claiming SCImago is yearly; inventing H without OpenAlex/SCImago river |
| **Country H-index (SCImago stock, audit)** | SCImago Country Rank → `g1_features_panel.csv` / `scimago_country_rank_1996_2024.csv` → panel `H_Index_SCImago` (flat across years) | Audit / fallback when yearly cell missing | `_QUARANTINE/sjr_country_metrics.STUB_H.csv`; master `H_Index_STUB_*`; treating stock as year-varying |
| **GDP per capita (PPP)** | World Bank `NY.GDP.PCAP.PP.CD` in `g1_features_panel.csv` | G1; G2 sidebar join from VIZ1 (ISO3/alias) | G2 invented growth; `data.js` fake GDP |
| **GERD % GDP** | **Gated hierarchy** → `gerd_pct_gdp_hierarchical.csv` (WB base; OECD fills true holes only if country overlap ≤0.05 pp; UIS≡WB) + **display LOCF ffill** in pool (`GERD_Source=LOCF:<src>:yYYYY`) — see [`RIVER_GERD_HIERARCHY.md`](RIVER_GERD_HIERARCHY.md), [`G2_CARRY_AND_GERD_FFILL.md`](G2_CARRY_AND_GERD_FFILL.md) | G1; G2 sidebar join from VIZ1 (same LOCF) | G2 hardcoded `rd`; Frankenstein OECD stitch on conflict countries; inventing GERD without a prior observation |
| **G1 publication size** | WB scientific articles → else SCImago Documents (`Total_Docs` / policy) | G1 bubble size | OpenAlex country totals for bubble size |
| **G2 Q1/Q4 / publisher docs** | `q1_q4_country_year.csv` (publisher **Country**) | `ridgeline_data.js` | master stub Q%; author-country fantasy |
| **G3 topic works** | OpenAlex concepts — **exactly 7** live IDs; AI = Machine learning **`C119857082`**; Quantum **`C58053490`**; shared 1974 window (no hard milestone floors — see [`G3_FLOORS_REVISED.md`](G3_FLOORS_REVISED.md), [`G3_FIX_PLAN.md`](G3_FIX_PLAN.md)) | `viz3_data.js` | mega-AI `C154945302` in pool; ASJC `2500` for Quantum; friend `scrape_openalex_data.py` ASJC subfield path; any 8th concept in the tap |
| **G4 collab cites/paper** | `collaboration_premium.csv` | `viz4_data.js` (`VIZ4_BY_YEAR`) | `data.js` `COLLAB_DATA` stub |
| **G5 India network** | Processed vault / `dashboard/data/india_network/*.json` | `india_network.js` | `DATA.getIndiaNetwork` demo growth |

## Publications naming (do not merge)

| Graph | Honest name | Unit |
|-------|-------------|------|
| G1 | WB / SCImago **country journal articles · documents** | Author-country article counts (policy: WB else SCImago Documents) |
| G2 | **Publisher-country journal documents** (Q1/Q4 path) | Docs in journals whose publisher is in that country |
| G3 | OpenAlex **concept / topic works** | Works tagged with locked concept IDs |
| G4 | OpenAlex **collab paper counts** (domestic vs intl) | Papers in premium split (not a single “pubs” KPI) |
| G5 | OpenAlex **institution works** (stock) | Per-institute totals |

## Quarantine

See `CS661_Dataset/_QUARANTINE/README.md`.

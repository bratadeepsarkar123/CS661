# CS661 Lecture Theory → Implementation Mapping

**Project:** *The Global Knowledge & Wealth Paradox* (Group 10, IIT Kanpur)  
**Generated:** 2026-07-07  
**Scope:** Full pipeline (ingestion → cleaning → network construction → export → dashboard) for all five dashboard panels, with emphasis on **Graph 5 (India Domestic HE Network)**.

---

## Executive summary

This project applies CS661 **information visualization** and **visual analytics** theory to a five-panel interactive dashboard (`dashboard/`). Lecture concepts appear at three layers:

1. **Pipeline design** — staged ETL, filtering, feasibility gates, verification checklists, and compact JSON export (Lectures 2, 15, 18).
2. **Network / graph analytics** — institution nodes, domestic co-authorship edges, hub detection, corridor annotations, triad precomputation (Lectures 9–10 relationship viz; graph data from Lecture 9).
3. **Visualization encoding & interaction** — Shneiderman overview→detail, Munzner focus+context, Tufte graphical integrity, 7±2 cognitive limits, visual variables (Lectures 2, 9–10, 11).

**Maturity split (important for graders):**

| Panel | Viz type | Data status | Primary lecture grounding |
|-------|----------|-------------|---------------------------|
| 1 | t-SNE peer clustering (`graph1.html`) | Synthetic + pre-baked coordinates in `data.js` | L11 high-dimensional DR |
| 2 | Global quality shift (beeswarm block flow) | Synthetic ridgeline-derived data | L10 distribution viz; L15 summarization intent |
| 3 | Top research topics bar race | Synthetic topic volumes | L10 time-series / trend viz |
| 4 | Collaboration premium dumbbell | Synthetic citation gaps | L10 comparative viz |
| **5** | **India domestic HE network (Leaflet + D3)** | **Real OpenAlex + NIRF + SCImago ETL** | **L2, L9–10, L11, L15, L18 — fullest application** |

**Graph 5** is the only module with a complete numbered pipeline (`scripts/india_network/00`–`10`), verification report (`data/processed/verification_report.md`, 15/15 passed), and lecture-aligned design spec (`india_domestic_he_network_plan.md`).

---

## Part A — Lecture PDF → Markdown conversion status

**Canonical image-rich location (2026-07-07):** `docs/lectures/` — each lecture MD includes YAML frontmatter, extracted text, per-page PNG renders at 150 DPI, embedded raster assets, a `## Figures` section, and a table-of-figures index. See [`docs/lectures/README.md`](lectures/README.md).

**Legacy text-only copies:** `markdown_files/markdown_files/` (same basename, no images). Prefer `docs/lectures/` for agent or human review.

**Source PDFs:** `markdown_files/lecture pdf/`

| PDF | Markdown | Status (2026-07-07) |
|-----|----------|---------------------|
| `Lecture1_Introduction_*.pdf` | `Lecture1_Introduction_*.md` | Already existed |
| `Lecture2_VA_Handling_Data_*.pdf` | `Lecture2_VA_Handling_Data_*.md` | Already existed |
| `Lecture3`–`Lecture8` (scientific viz) | Matching `.md` | Already existed |
| `Lecture9_InfoVis_Intro_*.pdf` | Matching `.md` | Already existed |
| `Lecture10_InfoVis_Principles_*.pdf` | Matching `.md` | Already existed |
| `Lecture11` parts 1–2, `Lecture12` part 3 | Matching `.md` | Already existed |
| `Lecture13_Stats_refresher_*.pdf` | Matching `.md` | Already existed (OCR garbled — use PDF for figures) |
| `Lecture15`–`Lecture17` | Matching `.md` | Already existed (L15–L17 OCR garbled — use PDF) |
| `Lecture18_Sampling_2_*.pdf` | `Lecture18_Sampling_2_*.md` | **Converted this session** (PyMuPDF) |
| `Lecture19_DL_*.pdf` | `Lecture19_DL_*.md` | **Converted this session** (PyMuPDF) |
| `cs661_after_midesem.pdf` | — | **Skipped** (cumulative reading bundle per user instruction) |

**Tool used:** `scripts/convert_lecture_pdfs.py` (PyMuPDF / `fitz`) — page renders via `get_pixmap()` at 150 DPI, plus embedded image extraction. Page-delimited `<!-- Page N -->` headers in the text section.

**Image asset layout:** `docs/lectures/assets/<lecture_stem>/page_001.png`, … — 766 page images and 753 embedded images across 19 lectures (2026-07-07).

**Missing lecture numbers:** No Lecture 14 PDF in the repo. Lectures 20–22 referenced inside L19 slides are not present as separate files.

---

## Master mapping table

| Lecture / theory concept | Where used (graph + pipeline stage) | How implemented (files / scripts) | Notes |
|--------------------------|-------------------------------------|-----------------------------------|-------|
| Visual Analytics = viz + analytics + interaction (L2) | All panels; especially Graph 5 fullscreen | `dashboard/app.js`, `dashboard/india_network.js` | Year scrubber, hover tooltips, click-to-detail |
| Shneiderman: Overview → zoom/filter → details-on-demand (L2) | Grid thumbnails → fullscreen → node/edge detail | `dashboard/index.html`, `app.js` `openViz()`, `india_network.js` focus panel | Documented in `india_domestic_he_network_plan.md` §0, §1.5 |
| Focus + context (L2 slide 19; L10 Munzner Ch.14) | Graph 5 map interaction | `india_network.js`: `FOCUS_X_RATIO`, dimmed context edges, right detail panel | `design/module5/M5-03-focus-fisheye.md` |
| Visual variables: position, size, color (L2) | Graph 5 nodes/edges | Geo lat/lon; `radius` ∝ √`total_works`; tier color `#3b82f6` / `#a855f7`; edge width ∝ weight | `09_export_payloads.py` `_node_radius()`, `india_network.js` |
| Gestalt proximity / similarity (L2) | Graph 5 hub clustering; Viz 2 tier blocks | Map geography; corridor city groups in `config.CORRIDOR_CITIES` | Hub per corridor enforced in `06_build_domestic_edges.py` |
| 7±2 working memory limit (L2, L10) | Overview thumbnails across all viz | Max ~3 callouts per panel; Graph 5 overview: 12 hubs, 40 edges | `config.py`: `HUB_COUNT=12`, `MAX_EDGES_OVERVIEW=40` |
| Chartjunk reduction (L10) | Graph 5 map styling | No grid, no drop shadows, ≤2 tier colors, ≤12 labels | Plan §2.3 checklist; `india_network.js` minimal basemap |
| Tufte graphical integrity (L10) | Graph 5 footnotes; Viz 2 integrity variant | Mandatory footnote: ~120 map nodes vs ~40k colleges in tier averages; SCImago year label | `verification_report.md` SCImago check; `design/module2/M2-08-integrity-sparse-overview.md` |
| Lie factor / no 3D distortion (L10) | Node sizing | Area ∝ `total_works` via sqrt scaling, not 3D spheres | `09_export_payloads.py` |
| Distribution visualization (L10) | Viz 2 quality tiers; ridgeline design docs | Beeswarm/block flow by Q1/Q4 ratio; `DATA.getRidgelineData()` | Evolved from ridgeline wireframe to beeswarm in `app.js` `renderViz2` |
| Comparative visualization — dumbbell (L10) | Viz 4 | D3 dumbbell: domestic vs intl citations/paper | `app.js` `renderViz4`, `data.js` `COLLAB_DATA` |
| Trend / time series (L10) | Global year slider; Viz 3 bar race; Graph 5 year slices | `APP.year` in `app.js`; `2015`–`2024` JSON slices | `09b_export_year_slices.py`, `manifest.json` |
| Relationship / network visualization (L9–L10) | Graph 5 | Nodes = institutions, edges = domestic co-authorship | `06_build_domestic_edges.py`, Leaflet overlay |
| High-dimensional data & DR (L11) | Viz 1 t-SNE clustering | `graph1.html` iframe; `data.js` `tsneX/tsneY` per country | Real t-SNE ETL not yet wired — coordinates baked |
| Curse of dimensionality → summarize (L11, L15) | Entire dashboard load strategy | Pre-compute aggregates offline; browser reads JSON only | `09_export_payloads.py`, `india_network_data.js` bundle |
| Distribution summarization / compact payloads (L15 PDF) | Graph 5 export | Overview ~29 KB, full ~100 KB; year slices | `10_verification_checklist.py` size checks |
| Importance-based sampling (L18) | Institution inclusion caps; hub selection | Premier top 60 + state top 60; top-12 hubs by degree; pilot `--pilot-top 30` | `config.py` caps; `06_build_domestic_edges.compute_hubs` |
| Data handling / cleaning (L2) | Full Module 5 ETL | Fuzzy name match, manual overrides, geocode stack resolution | `03_build_institution_master.py`, `03b_apply_campus_geocoding.py`, `data/nirf_institute_id_overrides.csv` |
| Verification & negative tests (course + L2 integrity) | Post-ETL gate | 15-check checklist incl. IITK↔IITD positive, foreign co-auth negative | `10_verification_checklist.py` |
| Linked views / brushing (L10 Ch.12) | Global year + region filters | Year updates Graph 5 via `loadYearPayload`; region filter on Viz 2 | `app.js` shared `APP` state |
| Scientific viz (L3–L8 VTK, volume, contours) | — | Not used in dashboard | VTK assignments separate from course project dashboard |
| Deep learning / NeRF (L19) | — | Not applied | Future work only |
| ICM-style staged pipeline | Module 5 ETL | Numbered scripts `00`–`10`, plain-text artifacts between stages | Aligns with sequential review pattern |

---

## Graph 5 — India Domestic HE Network (pipeline stage by stage)

### Timeline (when each stage runs)

| Order | Stage | Script(s) | Output artifact | Lecture tie-in |
|-------|-------|-----------|-----------------|----------------|
| 0 | Detect publication year range | `00_detect_year_range.py` | `data/processed/year_range.json` | Temporal filtering (L10 trend viz) |
| 1 | Download raw sources | `01_download_sources.py`, `01b`–`01g` | `data/raw/*` | L2 data acquisition |
| 1d–1f | NIRF PDF scrape (funding, patents) | `01e_scrape_nirf_funding_from_pdfs.py`, `01f_scrape_nirf_patents_from_pdfs.py` | Raw PDF extracts | Heterogeneous sources (L2 scalability) |
| 2 | Fetch OpenAlex institutions (IN education) | `02_fetch_openalex_institutions.py` | `openalex_institutions.parquet` | Graph node registry |
| 3 | Build institution master | `03_build_institution_master.py`, `03a`, `03b` | `institution_master.csv` (120 rows) | Entity resolution / data fusion |
| 4 | Feasibility gate | `04_feasibility_domestic_edges.py` | `feasibility_report.md` | Early validation before viz investment |
| 5 | Fetch works metadata | `05_fetch_openalex_works.py`, `05b_assemble_works_from_cache.py` | `works_raw.parquet` | Big-data fetch with cache resume |
| 6 | Filter works, build edges, mark hubs | `06_build_domestic_edges.py`, `06b_build_collaboration_triads.py` | `domestic_works.parquet`, `collaboration_edges_full.csv`, `hub_flags.csv`, triads | **Network construction + W-filters** |
| 7 | Join SCImago quality | `07_join_scimago_quality.py` | `institution_quality_static.csv` | Static quality snapshot with integrity footnote |
| 8 | Join NIRF funding & patents | `08_join_nirf_funding.py`, `08b_join_nirf_patents.py` | `institution_funding.csv`, `institution_patents.csv` | Attribute enrichment for detail panel |
| 9 | Export JSON payloads | `09_export_payloads.py`, `09b_export_year_slices.py` | `public/india_network/*.json` | L15 compact summarization for client |
| 9b | Copy to dashboard | `run_pipeline.ps1` | `dashboard/data/india_network/` | Deployment handoff |
| 10 | Verification checklist | `10_verification_checklist.py` | `verification_report.md` | Tufte / integrity testing |

**Orchestration:** `scripts/india_network/run_pipeline.ps1` (light vs heavy mode via `INDIA_ETL_MEMORY`).

### Work filters W1–W5 (network semantics)

Implemented in `scripts/india_network/filters.py` → `work_passes_filters()`:

| Filter | Rule | Purpose |
|--------|------|---------|
| **W1** | `YEAR_MIN` ≤ `publication_year` ≤ `YEAR_MAX` (2015–2024) | Temporal scope for year slider |
| **W2** | `type` ∈ `{article, review, book-chapter}` | Exclude non-research work types |
| **W3** | Every `authorships[].institutions[].country_code == 'IN'`; exclude unaffiliated | **Domestic-only** collaboration definition |
| **W4** | ≥ 2 distinct OpenAlex institution IDs present in `institution_master` | True multi-institution collaboration |
| **W5** | Edge `weight` ≥ `EDGE_WEIGHT_MIN_FULL` (2) at aggregation | Noise reduction on pair counts |

**Post-filter graph construction** (`06_build_domestic_edges.py`):

- Deduplicate works by `id`.
- For each domestic work, enumerate institution pairs (`itertools.combinations`).
- Sum co-authorship `weight` and `citation_weight` per (inst_a, inst_b, year).
- **Hub detection:** top 12 by weighted degree + one hub per geographic corridor (`CORRIDOR_CITIES`).

**Triads** (`06b`, `triad_builder.py`): precompute 3+ institution papers for focus-mode star layouts in the UI.

### Export tiers (overview vs full)

`09_export_payloads.py` applies lecture **reduce items** principle:

| Payload | Nodes | Edges | Thresholds |
|---------|-------|-------|------------|
| Overview | Hubs + high-degree subset (~45) | ≤ 40, weight ≥ 5, hub-to-hub bias | Grid thumbnail / fast load |
| Full | Up to 120 | ≤ 300, weight ≥ 2 | Fullscreen exploration |
| Per-year slices | Same logic per year | `09b_export_year_slices.py` | Linked time slider |

### Visualization layer (`dashboard/india_network.js`)

| Design choice | Implementation | Lecture basis |
|---------------|----------------|---------------|
| Geographic position encoding | Leaflet map, India bounds clamp, `india_outline.geojson` | L2 planar variables |
| Tier color (2 categories) | Premier blue / state purple | L2 color for labels; 7±2 |
| Node area | `radius` from √`total_works` | L2 size for magnitude |
| Edge width | Stroke width from normalized weight | L2 retinal variable |
| Focus + context on click | Center-left focus, dim non-neighbors, right panel (funding, pubs, patents, triads) | L10 Munzner Ch.14 |
| No live API in browser | `INDIA_NETWORK_DATA` bundled JS | L15 pre-summarization |
| Integrity footnote | Tier aggregate strip + map scope disclaimer | L10 Tufte |

**Verification proof (2026-07-01):** 15/15 checks passed — 108,705 domestic works, 13,236 edge rows, IIT Kanpur ↔ IIT Delhi weight 234, foreign co-auth correctly excluded.

---

## Other visualizations

### Viz 1 — High-dimensional peer clustering (Graph 1)

| Aspect | Detail |
|--------|--------|
| **Files** | `dashboard/app.js` `renderViz1()` → iframe `graph1.html`; `dashboard/data.js` country `tsneX`/`tsneY` |
| **Lecture concepts** | L11 t-SNE/UMAP for projecting high-D country feature vectors to 2D; L2 position encoding |
| **Pipeline** | **Not yet built** — coordinates are illustrative. Planned: World Bank + OpenAlex features → sklearn t-SNE → JSON (see `lecture-driven-dashboard-plan.md`, `design/module1/`) |
| **Interaction** | Fullscreen iframe; hover country in graph1 POC |

### Viz 2 — Global quality shift

| Aspect | Detail |
|--------|--------|
| **Files** | `dashboard/app.js` `renderViz2()`; `dashboard/data.js` `getRidgelineData()`; `dashboard/ridgeline_data.js` |
| **Lecture concepts** | L10 **distribution visualization** (Q1/Q4 ratio tiers); L10 trend over 1999–2024; Gestalt continuity in flow ribbons |
| **Encoding** | Countries classified Elite (ratio ≥2), Balanced, Q4-Dominant; block height ∝ country count |
| **Pipeline** | Synthetic data generator in `data.js`. Real pipeline planned in `global_quality_shift_agent_handoff.md` (SCImago quartile shares by country-year) |
| **Design docs** | `design/module2/M2-01-classic-ridgeline.md`, `M2-08-integrity-sparse-overview.md` |

### Viz 3 — Top research topics (bar race)

| Aspect | Detail |
|--------|--------|
| **Files** | `dashboard/app.js` `renderViz3()`; `dashboard/viz3_data.js`; `data.js` `TOPICS` array |
| **Lecture concepts** | L10 trend/time-series; animated ranking for temporal pattern discovery |
| **Pipeline** | Synthetic topic volumes with growth trends. Planned: OpenAlex `concepts` aggregation by year |
| **Interaction** | Play/pause race, year scrubber, glassmorphism UI |

### Viz 4 — Collaboration premium (dumbbell)

| Aspect | Detail |
|--------|--------|
| **Files** | `dashboard/app.js` `renderViz4()`; `data.js` `COLLAB_DATA` |
| **Lecture concepts** | L10 **comparative visualization**; dumbbell length = citation premium (intl − domestic) |
| **Encoding** | Red = domestic cites/paper, green = intl co-auth cites/paper, connector shows gap |
| **Pipeline** | Static 2024 demo values. Planned: OpenAlex authorship country flags → groupby mean citations |
| **Design docs** | `design/module4/M4-01-classic-dumbbell.md` |

### graph1.html (standalone POC)

Large embedded D3 t-SNE/scatter proof-of-concept referenced by Viz 1 fullscreen. Established the **Python → JSON → D3** pattern reused for Module 5 JSON export.

---

## Cross-cutting pipeline concepts

### Staged ETL as review gates (ICM-aligned)

Module 5 uses **numbered scripts** with plain-text/CSV/Parquet/JSON handoffs between stages — matching Interpretable Context Methodology principles:

- Each script has a single job (fetch / join / filter / export / verify).
- Humans can inspect `data/processed/*` before UI consumption.
- `run_pipeline.ps1` documents the execution order.

### Data quality & verification

| Practice | Location | Lecture / course link |
|----------|----------|----------------------|
| Feasibility gate before full fetch | `04_feasibility_domestic_edges.py` | Avoid building viz on insufficient data |
| 15-point verification checklist | `10_verification_checklist.py` | Positive + negative filter tests |
| Manual institution overrides | `data/manual_institution_overrides.csv`, `nirf_institute_id_overrides.csv` | Human-in-the-loop entity resolution |
| NIRF coverage gap report | `data/processed/nirf_coverage_gaps.md` | Tufte: document missing data |
| Collision / coordinate audit | `03b_apply_campus_geocoding.py`, verification campus stack check | Spatial integrity |

### Pre-computation vs interactive analytics

| Layer | Approach | Theory |
|-------|----------|--------|
| Browser | Static JSON + bundled `india_network_data.js` | L15 distribution summarization; no client-side aggregation of 100k+ works |
| Batch Python | pandas/pyarrow parquet, filtered exports | L2 scalability; L11 curse of dimensionality |
| Overnight fetch | `overnight_supervisor.py`, cache resume | L18 sampling — prioritize high-works institutions in pilot mode |

### Dashboard shell (all graphs)

| Feature | File | Theory |
|---------|------|--------|
| Gallery → fullscreen | `dashboard/index.html`, `app.js` | Shneiderman overview first |
| Global year 2015–2024 | `APP.year` | Linked views (L10) |
| Dark theme `#0f172a` | `dashboard/style.css` | Consistent retinal pre-attentive backdrop |
| D3 tooltips | `app.js` `showTip()` | Details on demand |

### Planning & theory documentation in repo

| Document | Role |
|----------|------|
| `lecture-driven-dashboard-plan.md` | Maps 17+ lectures to five-panel contract |
| `india_domestic_he_network_plan.md` | Module 5 cognitive design + ETL spec with lecture citations |
| `design/module*/` | Per-module variant specs citing L2/L10 |
| `.cursor/plans/lecture-driven_dashboard_plan_c70ad434.plan.md` | IDE plan mirror |
| `project_knowledge_base.md` | Dataset feasibility notes |
| `CS661_PROJECT.md` | Official 7-module proposal (compressed to 5 panels) |

---

## Gaps — lecture topics not yet applied

| Lecture area | Topic | Status in project |
|--------------|-------|-------------------|
| L3–L8 | VTK, volume rendering, isocontours, transfer functions, parallel viz | **Not used** (scientific viz track; separate assignments) |
| L13, L16 | Stats refresher, multivariate distributions, copulas | Partially referenced in design docs; **no copula/GMM in ETL** |
| L15, L17 (MD) | Distribution summarization, sampling theory | Applied **in spirit** (JSON export) but MD files OCR-corrupted; full GMM/KDE pipeline not implemented |
| L18 | Importance sampling | Hub/cap selection only — not full TVCG 2021 importance function |
| L19 | Deep learning, NeRF, implicit neural representations | **Not applied** to dashboard |
| L11 | t-SNE / UMAP | Viz 1 uses **static** coordinates, not live DR from feature matrix |
| L10 | Ridgeline / joyplot | Design intent in Module 2; **implemented as beeswarm block chart** instead |
| Proposal §4.1, §4.4 | Wealth→R&D choropleth, bubble pack | Dropped from 5-panel UI (noted in `lecture-driven-dashboard-plan.md`) |
| React `hierarchy-app/` | Original scaffold | Superseded by vanilla `dashboard/` for delivery; `IndiaNetworkPanel.jsx` partial |

---

## Appendix — Lecture file index (PDF → MD)

```
markdown_files/lecture pdf/                          markdown_files/markdown_files/
├── Lecture1_Introduction_*.pdf          ───────►  Lecture1_Introduction_*.md
├── Lecture2_VA_Handling_Data_*.pdf      ───────►  Lecture2_VA_Handling_Data_*.md
├── Lecture3_Scientific_Data_VTK_*.pdf ───────►  Lecture3_Scientific_Data_VTK_*.md
├── Lecture4_LERP_ParaView_*.pdf         ───────►  Lecture4_LERP_ParaView_*.md
├── Lecture5_Isocontour_*.pdf            ───────►  Lecture5_Isocontour_*.md
├── Lecture6_Volume_Rendering_*.pdf      ───────►  Lecture6_Volume_Rendering_*.md
├── Lecture7_TF_Design_*.pdf             ───────►  Lecture7_TF_Design_*.md
├── Lecture8_parallel_visualization_*.pdf───────►  Lecture8_parallel_visualization_*.md
├── Lecture9_InfoVis_Intro_*.pdf       ───────►  Lecture9_InfoVis_Intro_*.md
├── Lecture10_InfoVis_Principles_*.pdf ───────►  Lecture10_InfoVis_Principles_*.md
├── Lecture11_HighDimVis_part_1_*.pdf    ───────►  Lecture11_HighDimVis_part_1_*.md
├── Lecture11_HighDimVis_part_2_*.pdf    ───────►  Lecture11_HighDimVis_part_2_*.md
├── Lecture12_HighDimVis_part_3_*.pdf    ───────►  Lecture12_HighDimVis_part_3_*.md
├── Lecture13_Stats_refresher_*.pdf      ───────►  Lecture13_Stats_refresher_*.md  [OCR garbled]
├── Lecture15_Dist_Summarization_*.pdf   ───────►  Lecture15_Dist_Summarization_*.md  [OCR garbled]
├── Lecture16_Multivar_dist_*.pdf        ───────►  Lecture16_Multivar_dist_*.md  [OCR garbled]
├── Lecture17_Sampling_1_*.pdf           ───────►  Lecture17_Sampling_1_*.md  [OCR garbled]
├── Lecture18_Sampling_2_*.pdf           ───────►  Lecture18_Sampling_2_*.md  [NEW 2026-07-07]
├── Lecture19_DL_*.pdf                   ───────►  Lecture19_DL_*.md  [NEW 2026-07-07]
└── cs661_after_midesem.pdf              ───────►  (skipped — not converted)
```

**Also in `markdown_files/markdown_files/` (non-lecture):** `CS661_PROJECT.md`, `Details for Course Project.md`, `sample_proposal.md`.

---

## Quick reference — key implementation paths

```
CS661/
├── dashboard/                    # Shipped UI (vanilla JS + D3 + Leaflet)
│   ├── index.html, app.js        # 5-panel gallery + renderViz1–5
│   ├── india_network.js          # Graph 5 Leaflet network
│   ├── data.js                   # Modules 1–4 synthetic data
│   ├── graph1.html               # Viz 1 t-SNE POC
│   └── data/india_network/       # Real JSON payloads (2015–2024)
├── scripts/india_network/        # Module 5 ETL pipeline (00–10)
├── data/processed/                 # Parquet/CSV intermediates + verification_report.md
├── docs/                         # This report
├── lecture-driven-dashboard-plan.md
└── india_domestic_he_network_plan.md
```

---

*For live demo: `cd dashboard && python -m http.server 8766` → http://localhost:8766*

---

## Appendix — Lecture Markdown with page images (agent context)

All lecture conversions under **`docs/lectures/`** are designed so an AI agent (or human reviewer) can reconstruct the full slide deck visually without opening the original PDF:

1. **Read the Markdown** for extracted text and structure (`## Lecture Text`, `<!-- Page N -->` markers).
2. **Follow relative image links** in `## Figures` — each slide is `assets/<lecture_stem>/page_NNN.png` (150 DPI PNG).
3. **Consult `## Embedded Images`** when slides contain distinct raster figures extracted separately from page renders.
4. **Use `## Table of Figures`** as a quick index mapping page numbers to asset paths and first-line text snippets.

**Index:** [`docs/lectures/README.md`](lectures/README.md) lists all 19 lectures with page and embedded image counts.

**Skipped:** `cs661_after_midesem.pdf` (post-midsem compilation bundle) — not converted.

**Re-run conversion:** `python scripts/convert_lecture_pdfs.py` (requires `pymupdf`).

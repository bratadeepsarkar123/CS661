# CS661 Dashboard — Pipeline Fix Plan

**Scope:** End-to-end source → transform → validate → bundle → UI-label equality.  
**Not in scope:** UI caps, hiding bad rows, EMA smoothing, or footnotes that excuse broken metrics.  
**Primary owner graph:** Graph 5 (India Domestic HE Network).  
**Live app:** `dashboard/`  
**Local country master (G1–G4):** `CS661_Dataset/`  
**G5 ETL:** `scripts/india_network/` → `data/processed/` → `public/india_network/` → `dashboard/data/india_network/`  

**Partner report status:** `dashboard/SOURCE_RECONCILIATION_REPORT.md` was **not present** at plan time. This plan aligns with audited outputs already in-repo:

- `dashboard/_recon_source_equality_out.txt`
- `dashboard/_audit_g2_g5_out.txt`
- `dashboard/_audit_viz1_extra_out.txt`
- `CS661 Project/data/processed/verification_report.md` (23/23 PASS — **gates are too weak**; they do not catch silent static fields or top-300 edge drops)

If the partner report appears later, merge its file inventory into §1.1 / §2 partner-ask tables; do not weaken the acceptance tests below.

---

# 0. Principles

**Done means backend = frontend = source equality.**

1. Every UI number is traceable to a named raw file + transform step + year semantics.
2. If a field is **intentionally static** (e.g. SCImago 2019 snapshot), the payload carries `*_year` / `*_note`, and the UI label says so. Static ≠ silent.
3. If a field is **year-sliced** (edges, funding, ranks), values must change when the slider changes *or* the UI must show an explicit mismatch note tied to the mapped season (already partially done for NIRF).
4. No transform may invent, cap, or smooth values to “look better” without documenting the policy in both ETL and UI.
5. Validation gates must fail the build on: dangling edges, orphan nodes, silent static fields mislabeled as yearly, integrity violations (`q1+q4 > total`), wrong ASJC codes, and missing country names.
6. Bundle is mechanical: processed artifacts → dashboard payload → UI consumes only bundled fields (no synthetic GDP/R&D overlays).

---

# 1. Graph 5 — Full pipeline fix plan (PRIMARY)

## 1.1 Current pipeline map

```
RAW
├── OpenAlex institutions ………… scripts/india_network/02_fetch_openalex_institutions*.py
│                                 → data/processed/openalex_institutions.parquet
├── OpenAlex works cache ……… 05_fetch_openalex_works.py → data/cache/openalex/
│                                 → 05b_assemble_works_from_cache.py
│                                 → data/processed/domestic_works.parquet
├── NIRF rankings / funding / patents
│     01b/01d/01e/01f/01g/01h_*.py + acquisition/*
│     → data/raw/nirf_*.csv + data/cache/nirf/
├── SCImago India IR …………… 01_download_sources.py / manual
│                                 → data/raw/scimago_india.csv (used as 2019 snapshot)
└── Geo overrides ………………… data/manual_institution_overrides.csv
                                  data/nirf_institute_id_overrides.csv

ENTITY RESOLUTION
├── 03_build_institution_master.py + 03a_enrich + 03b_geocode
│     → data/processed/institution_master.csv (120 nodes)
└── nirf_utils.py + report_nirf_gaps.py
      → data/processed/nirf_match_losers.csv (10 losers today)

TEMPORAL JOINS
├── 06_build_domestic_edges.py → collaboration_edges_full.csv (year, weight, citation_weight)
├── 06b_build_collaboration_triads.py / triad_builder.py
├── 07_join_scimago_quality.py → institution_quality_static.csv  [STATIC 2019]
├── 08_join_nirf_funding.py → institution_funding.csv + institution_funding_by_year.csv
└── 08b_join_nirf_patents.py → institution_patents.csv + institution_patents_by_year.csv

EXPORT / BUNDLE
├── 09_export_payloads.py + 09b_export_year_slices.py
│     → public/india_network/{YYYY}_{overview|full}.json + all_years_* + manifest.json
│     → copy → dashboard/data/india_network/
├── regenerate_india_network_data_js.py → dashboard/india_network_data.js
├── 10_verification_checklist.py → CS661 Project/data/processed/verification_report.md
└── UI: dashboard/india_network.js (+ app.js Graph 5 shell)
```

**Orchestrators (extend, do not rewrite):**

| Script | Role |
|--------|------|
| `scripts/india_network/run_pipeline.ps1` | Post-assemble pass (03a→07→05b/06→08→09b→copy) |
| `scripts/india_network/run_post_assemble.ps1` | Lighter post-cache path |
| `scripts/india_network/overnight_supervisor.py` | Numbered stage runner |
| `scripts/india_network/config.py` | Thresholds: `MAX_EDGES_FULL=300`, `EDGE_WEIGHT_MIN_FULL=2`, `FULL_NODE_CAP=120` |

**Processed CSVs mirrored under** `CS661 Project/data/processed/` (and checkpoints under `data/checkpoints/`). Canonical working tree for ETL is **`data/processed/`** at repo root.

## 1.2 What’s correct today vs what’s misleading

### Actually correct (keep)

| Asset | Why it’s honest |
|-------|-----------------|
| Per-year collaboration edges in `collaboration_edges_full.csv` | Calendar-year domestic co-pubs; temporal variance real (2015 sum≪2022) |
| Year-mapped NIRF funding / patents / ranks in full JSON | `*_by_year` tables + `slider_year_to_*` in `nirf_utils.py`; IISc funding varies 2020 vs 2023 |
| `manifest.json` season lists | Documents funding AYs, patent years, NIRF seasons, `quality_year: 2019` |
| `quality_note` / `temporal_metrics_note` in JSON meta | SCImago static + NIRF season mapping spelled out in payload |
| Geo integrity | 120/120 lat/lon; 0 dangling edges in full slices |
| IITK↔IITI **in CSV** | All years 2015–2024 present; weights sum to 95 |

### Misleading / incomplete honesty

| Issue | Evidence | Root cause |
|-------|----------|------------|
| **Top-300 silent drop** | IITK–IITI 2023 weight=8 in CSV; 2023 full min weight≈15 → edge absent in JSON; UI shows “no partners” | `build_edges(...).head(MAX_EDGES_FULL)` in `09_export_payloads.py` |
| **`total_works` / `radius` static across slider** | 2015 vs 2024: 120/120 identical | Copied from lifetime OpenAlex `works_count` on master, not year slice |
| **UI label half-wrong** | Sidebar: `OpenAlex works (2015–24)` | Label implies windowed count; value is **lifetime** `works_count` (and IIT Madras / IIT Palakkad = **0**) |
| **`scimago_pct` static** | Documented in meta — OK if labels stay explicit | Already honest in meta; keep static OR regenerate multi-year |
| **10 NIRF unmatched** | `nirf_match_losers.csv` | Fuzzy/ID uniqueness gaps — funding/patents unavailable for those nodes |
| **Verification report overclaims** | 23/23 PASS while IITK–IITI vanishes and works are static | Gates don’t test focus-institution partner recall or year-varying works |
| **Overview ≠ full semantics** | Overview: hub↔hub, max 40 edges, min weight 5 | Fine if UI says “overview mode”; easy to confuse with “the network” |
| **2024 patent/funding clamp** | Patent 2023+ → 2022; funding 2024 → 2022-23 | Documented in `temporal_metrics_note`; UI mismatch notes exist — keep truthful |

## 1.3 Target schema (per year slice)

### `manifest.json`

| Field | Source | Year semantics | May be static? |
|-------|--------|----------------|----------------|
| `available_years` | Edge years present | Calendar | No |
| `quality_year` | SCImago snapshot year used | Explicit | Yes (if multi-year IR unavailable) |
| `funding_academic_years` | Scraped NIRF AYs | Academic | No |
| `patent_calendar_years` | Scraped patent years | Calendar | No |
| `nirf_ranking_seasons` | Ranking seasons on disk | Season | No |

### Node (full payload)

| Field | Source | Year semantics | Static OK? |
|-------|--------|----------------|------------|
| `id`, `openalex_id`, `name`, `tier`, `city`, `state`, `lat`, `lon` | master + geo | Entity | Yes |
| `is_hub`, `color`, `tier` | hub_flags / tier rules | Entity | Yes |
| `total_works` | **Decide (Stage D)** — preferred: year-specific works from OpenAlex cache / domestic works | Calendar year of slider **or** lifetime with label `lifetime_works` | Only if renamed + labeled |
| `radius` | Derived from the works field used for encoding | Same as works field | Same as works |
| `works_scope` | New: `"calendar_year"` \| `"lifetime"` \| `"window_2015_2024"` | Meta | Required |
| `scimago_pct`, `scimago_year` | `institution_quality_static` or multi-year IR | Snapshot year in `scimago_year` | Yes if labeled |
| `nirf_rank`, `nirf_ranking_season`, `nirf_ranking_category`, `nirf_rank_year_mismatch` | NIRF rankings | Mapped season | No (values change) |
| `research_funding_cr`, `sponsored_projects`, `total_expenditure_cr`, `funding_academic_year`, `funding_year_mismatch`, `funding_status` | NIRF funding by AY | Mapped AY | No |
| `patents_*`, `patent_calendar_year`, `patent_year_mismatch`, `patent_status` | NIRF patents | Mapped calendar | No |
| `nirf_match_status` | match / unranked / blocked | Entity | Yes |

### Edge

| Field | Source | Year semantics | Static OK? |
|-------|--------|----------------|------------|
| `source`, `target` | institution ids | — | — |
| `weight` | Domestic co-pub count | **Calendar year of slice** (all_years = sum) | No |
| `citation_weight` | Sum of cited_by on those works | Same year | No |
| Optional `excluded_reason` | Only in partner-detail endpoints | — | — |

### Meta (keep + tighten)

- `quality_note`, `temporal_metrics_note`, `coverage` (matched/losers/funding/patents counts)
- **New:** `edge_policy` (`top_n` / `weight_floor` / `dual`), `edge_min_weight_observed`, `works_policy`

## 1.4 Concrete fix stages (extend existing ETL)

**Decision: extend `scripts/india_network/` — do not rewrite.** Numbered scripts already encode ICM-style stages. Add gates + edge policy + works policy; fix master zeros.

### Stage A — Raw ingest

| Action | Script / path |
|--------|----------------|
| Confirm OpenAlex cache completeness for 120 master IDs | `validate_openalex_cache.py`, `05_fetch_openalex_works.py` |
| Re-fetch institution metadata for **IIT Madras (`I24676775`)** and **IIT Palakkad (`I4210113248`)** (works_count=0 today) | `02_fetch_openalex_institutions.py` or targeted patch in `03a_enrich_institution_master.py` |
| Keep NIRF PDF scrapes current | `01e` / `01f` / `01h` |
| SCImago: either keep 2019 snapshot **or** acquire multi-year IR if partner has it | `data/raw/scimago_india.csv` + `07_join_scimago_quality.py` |
| Optional AISHE | `validate_aishe.py` (already optional; missing is OK) |

**User alone:** yes for OpenAlex re-enrich + NIRF (API key in `.env`).  
**Partner:** only if they have multi-year SCImago India IR dumps beyond 2019.

### Stage B — Entity resolution (OpenAlex ↔ NIRF)

| Action | Path |
|--------|------|
| Resolve 10 losers in `data/processed/nirf_match_losers.csv` via `data/nirf_institute_id_overrides.csv` | IIT Goa, SRM, HS Gour, IACS, Allahabad, G.S. College, Shivaji, Mangalore, Karpagam, Rajasthan (ID uniqueness) |
| Re-run `08_join_nirf_funding.py` / `08b_join_nirf_patents.py` | Raise funding coverage above 104/120 where PDFs exist |
| Keep uniqueness guards (no duplicate funding clusters) | Existing checks in `10_verification_checklist.py` |

**User alone:** mostly (manual NIRF ID lookup on nirfindia.org). Partner not required.

### Stage C — Temporal metrics

| Metric | Policy (freeze this) |
|--------|----------------------|
| Edges | Calendar year = slider year; `all_years` = sum of yearly weights |
| Funding | Map via `slider_year_to_funding_academic_year`; clamp notes already correct |
| Patents | Map via `slider_year_to_patent_calendar_year`; 2023+ → 2022 documented |
| NIRF ranks | Nearest available season; mismatch flags on |
| SCImago | Remain 2019 **unless** multi-year raw arrives; never pretend yearly |

No change needed to mapping functions if UI/copy stays aligned — fix is edge + works policy.

### Stage D — Publication counts (decision)

**Recommend:** dual fields, one encoding source.

1. `lifetime_works` = OpenAlex `works_count` (entity attribute).
2. `year_works` = count of that institution’s works in OpenAlex cache with `publication_year == slider` (and same type filters as edges: article/review/book-chapter).
3. UI Publications tab:
   - Primary: `year_works` labeled **“OpenAlex works in {year}”**
   - Secondary: `lifetime_works` labeled **“OpenAlex works (all years)”**
4. `radius` / size encoding: use **`year_works`** so the year slider changes node size honestly; fall back to lifetime only in `all_years` rollup.
5. Remove the false label `OpenAlex works (2015–24)` unless you literally sum 2015–2024 cache counts into a third field `window_works`.

**Compute path:** extend `09_export_payloads.build_nodes` to aggregate from `domestic_works.parquet` / works cache — **no new partner file** if cache is complete.

### Stage E — Edge threshold policy (recommendation)

**Recommend: dual mode + focus-institution guarantee (not silent top-300 only).**

| Mode | Policy | Use |
|------|--------|-----|
| **Overview** | Keep: hubs, min weight 5, max 40 | Map default |
| **Full network** | Keep top-300 for global clutter control **but** write `edge_policy` + `edge_floor_weight` into meta | Global view |
| **Focus / “show all partners”** | When a node is selected, partner list + star edges come from **untruncated** year edges for that node (`weight >= 2`), not from the top-300 subset | Detail panel + map focus |

Implementation sketch (extend, don’t rewrite):

1. In `09_export_payloads.py`, also emit `partners_by_inst` (or keep full edge table per year as `YYYY_edges_all.json` gzipped) for weights ≥ 2 among the 120 nodes.
2. Or: raise `MAX_EDGES_FULL` only after measuring; still add focus-untruncated path so IITK–IITI never disappears when selected.
3. UI (`india_network.js`): partner list / focus edges read untruncated adjacency; overview still uses capped edges.
4. Document exclusion: if global mode hides an edge, detail mode must still show it.

**Do not** “fix” IITK–IITI by only raising N until that one edge appears — that’s another silent policy.

### Stage F — Validation gates (must pass before bundle)

Extend `10_verification_checklist.py` + add `verify_graph5_display.py` CI-style checks:

1. **Focus partner recall:** For fixtures `(IIT Kanpur, IIT Indore)` and `(IIT Kanpur, IIT Delhi)`, every year with CSV weight ≥ 2 must appear in **focus/untruncated** partner API; years below global top-300 must be flagged in a *coverage* report, not silently absent from detail.
2. **Works year variance:** For ≥50 institutions, `year_works(2015)` ≠ `year_works(2022)` (or documented sparse).
3. **No zero works for premier IITs:** Madras/Bombay/Delhi/Kanpur/Kharagpur/Madras/Roorkee/Guwahati/Hyderabad/Indore/BHU/ISM — `lifetime_works > 0`.
4. **Funding variance:** Keep existing IISc 2020 vs 2023 check.
5. **Geo / dangling:** Keep existing.
6. **Static field registry:** Any field listed as static must appear in `quality_note` / `works_scope`; any field labeled yearly must vary or carry mismatch flag.
7. **Schema:** every full node has required keys; overview edges ⊆ overview nodes.
8. **Losers report:** count + names written; funding coverage printed; fail if matched NIRF id but funding join silently null without status.

### Stage G — Bundle + UI copy alignment

| Step | Command / file |
|------|----------------|
| Export | `python scripts/india_network/09b_export_year_slices.py` |
| Sync | Already copies to `dashboard/data/india_network/` |
| JS bundle | `python scripts/india_network/regenerate_india_network_data_js.py` |
| UI | `dashboard/india_network.js`: works labels; focus uses untruncated partners; encoding blurb says size ∝ √(year works) |
| Kill false claims in report | Refresh `verification_report.md` only after new gates; remove any “all partners shown” implication |
| Copy also to `CS661 Project/data/processed/` if that tree is used for submission zip | Keep one canonical `data/processed/` |

## 1.5 Files to change

| Layer | Files |
|-------|--------|
| Config | `scripts/india_network/config.py` (`MAX_EDGES_*` docs; optional new constants) |
| Export | `09_export_payloads.py`, `09b_export_year_slices.py` |
| Master / enrich | `03a_enrich_institution_master.py`, overrides CSVs |
| NIRF | `nirf_institute_id_overrides.csv`, `08_*.py` if join rules change |
| Verify | `10_verification_checklist.py`, `verify_graph5_display.py` |
| Bundle | `regenerate_india_network_data_js.py` → `dashboard/india_network_data.js` + JSON under `dashboard/data/india_network/` |
| UI | `dashboard/india_network.js` (labels + focus edge source) |
| Docs / claims | `CS661 Project/data/processed/verification_report.md`, proposal/report tex if it claims top-300 = complete network |

## 1.6 Acceptance tests

| # | Test | Pass criterion |
|---|------|----------------|
| 1 | IITK–IITI | CSV weights match focus-panel weights for 2015–2024; 2023 shows 8 (not 0) in detail |
| 2 | IITK–IITD | Remains in global top-300 where weight high; always in focus list |
| 3 | IISc funding | 2020 ≠ 2023; matches `institution_funding_by_year.csv` |
| 4 | Geo | 0 invalid coords; campuses in India bbox |
| 5 | Dangling | 0 orphan edges in overview and full |
| 6 | Works | Premier IIT `lifetime_works > 0`; `year_works` changes for majority across 2015 vs 2022 |
| 7 | Labels | No UI string claims yearly for static SCImago; works label matches `works_scope` |
| 8 | Losers | ≤10 unmatched **or** documented; each has `nirf_match_status` |

## 1.7 Effort estimate & partner dependency

| Work | Who | Effort |
|------|-----|--------|
| Edge dual-mode + focus untruncated | User (extend 09 + UI) | 1–2 days |
| Year-specific works from cache | User | 1 day |
| Fix IITM/Palakkad works_count | User (OpenAlex re-fetch) | 0.5 day |
| NIRF override 10 losers | User (manual IDs) | 0.5–1 day |
| Stronger verification gates | User | 0.5 day |
| Multi-year SCImago IR | **Partner optional** | Only if available |
| Re-crawl all OpenAlex works | User overnight (`INDIA_ETL_MEMORY=high`) | 1 night if cache holes |

**G5 can be source-true without partner files** except optional multi-year SCImago. Raw G5 data lives under `data/` + OpenAlex API — **not** in `CS661_Dataset/`.

## 1.8 Order of execution (G5 only, week-style)

| Day | Work |
|-----|------|
| **D1** | Fix master zeros (IITM/Palakkad); add NIRF ID overrides for losers; re-run 03a → 08/08b |
| **D2** | Implement Stage D year_works in export; regenerate all year JSON; update UI labels |
| **D3** | Implement Stage E focus-untruncated partners; acceptance test IITK–IITI all years |
| **D4** | Harden Stage F gates; fail build on regressions; refresh verification_report |
| **D5** | Bundle (`09b` + `regenerate_india_network_data_js.py`); viva checklist walkthrough |

---

# 2. Graphs 1–4 — Pipeline fix plans

Shared local inputs: `CS661_Dataset/master_dataset.csv`, `raw_worldbank.csv`, `raw_openalex_docs.csv`, `raw_wb_publications.csv`, `sjr_country_metrics.csv` (**yearless**), `collaboration_premium.csv`, `merge_scimago_kaggle.py` (partner machine paths hardcoded — rewrite for this repo).

**No in-repo ETL that regenerates `viz1_data.js` / `ridgeline_data.js` / `viz3_data.js` / `viz4_data.js`.** Payloads are frozen JS blobs. Fix = **regen scripts you add** under e.g. `scripts/country_panels/` + freeze into `dashboard/`.

---

## 2.1 Graph 1 — `viz1_data.js` (UMAP / peer clustering)

### Current pipeline hypothesis

`master_dataset.csv` (WB GDP/GERD + OA/WB docs + broken H) → unknown UMAP offline → `viz1_data.js` (`Country_Code`, `Year`, `Total_Docs`, `H_Index`, `GERD_Percent_GDP`, `GDP_Per_Capita_PPP`, `x`, `y`). Frontend matches master for many 2015–2022 spots; **H_Index is yearless SJR** (`sjr_country_metrics.csv`) broadcast to all years → Ireland H=111 > USA H=53. Null `Country_Name` (27 rows). UMAP `x` reverses often → UI EMA patch in `app.js` (anti-pattern). Credits claim “World Bank API live” (`data.js`, `index.html`) — **false**.

### Root cause class

**Wrong join / yearless quality metric + missing names + projection instability** (not a UI bug).

### Target source of truth

| Field | Source |
|-------|--------|
| GDP PPP | World Bank `NY.GDP.PCAP.PP.CD` from `raw_worldbank.csv` (no live API required) |
| GERD % GDP | WB `GB.XPD.RSDV.GD.ZS` / UNESCO UIS / OECD MSTI (`RD_Spending_Data_Guide.md`) |
| Total docs | Prefer **SCImago country-year Documents** OR OpenAlex country-year — pick one and label; stop mixing without suffix |
| H-index | **SCImago country-year H index** (full Kaggle/SJR panel with `Year`) — never yearless broadcast |
| x,y | Recompute UMAP/t-SNE **per year independently** or use stable features without year-to-year Procrustes; do not EMA |

### Regen stages

1. Build `country_year_master.parquet` with ISO3 + name + metrics (drop null names).
2. Join **yearly** SJR H / docs.
3. Impute GERD with explicit `gerd_imputed` flag (no silent carry-forward without flag).
4. Fit embedding; export `viz1_data.js`.
5. Validate: USA H ≫ IRL H; H varies across years for large countries; G1 docs policy documented vs G2 totals.

### Validation spot-checks

USA/CHN/IND/GBR × 2015/2020/2022: H and docs vs SJR raw; no null names; Ireland not above USA on H.

### Partner file asks (exact)

1. **Full SCImago/SJR country rank CSV with `Year`** (the file `merge_scimago_kaggle.py` calls `scimago_country_rank.csv`) — not the yearless `sjr_country_metrics.csv`.
2. Confirmation whether G1 `Total_Docs` should be SJR Documents or OpenAlex (today FE ≪ OA in recon diffs).
3. Any existing UMAP notebook/script used to produce `x,y` (if not, you regenerate).

### UI contract

- Remove “World Bank API live” / “Fetching live data…”.
- Label axes as projection of declared features; remove EMA once data is stable.
- Tooltip: show `gerd_imputed` when set.

---

## 2.2 Graph 2 — `ridgeline_data.js`

### Current pipeline hypothesis

Country-year Q1/Q4/**total** counts → `REAL_RIDGELINE_DATA` with `ratio = min(5, q1/q4)`. Audit: 172 capped ratios; 569 rows with `q1+q4 > total`; UK/USA Q1 inflated vs master Q1%. `getCountryMetrics()` in `app.js` injects **synthetic** GDP/R&D/H with 2.5% GDP growth. Taiwan (and others) banned if **any** year has `q1 === 0` (`countriesWithMissingData`).

### Root cause class

**Capped transform + integrity-broken counts + synthetic overlay + hostile missing-data filter.**

### Target source of truth

SCImago/SJR country-year: documents in Q1 / Q4 / total (or journal-share metrics — but then plot **percentages**, not fake counts). World Bank/OECD for filter GDP/R&D **from master**, not `getCountryMetrics`.

### Regen stages

1. Ingest yearly SJR quartile document counts (or percents).
2. Enforce `q1 + q4 + q2 + q3 = total` (or store percents only).
3. **Delete ratio cap**; store true `q1/q4` (UI can winsorize display only with a labeled toggle — default uncapped).
4. Replace `getCountryMetrics` with joins to `country_year_master`.
5. Taiwan: include years with data; don’t lifetime-ban on a single zero year.

### Validation spot-checks

USA/CHN/IND/GBR 2015/2020/2022: ratio uncapped; `q1+q4 ≤ total`; UK Q1 not absurdly > USA if source says otherwise; Taiwan visible when data exists.

### Partner file asks (exact)

1. Same **yearly SJR** panel with Q1/Q4 document counts (or clear percent fields).
2. Script or notebook that produced capped `ridgeline_data.js` (to know unit definitions).
3. Do **not** send another capped export.

### UI contract

- Remove synthetic `getCountryMetrics` GDP/R&D/H.
- Remove lifetime ban on `q1===0` once.
- Credits: SCImago SJR (static file), not live WB API.

---

## 2.3 Graph 3 — `viz3_data.js`

### Current pipeline hypothesis

OpenAlex topic × country × year counts bundled as `CSV_DATA`. UI map `topicSubfields` in `app.js` sets **Quantum Computing → ASJC/subfield 2500** (= Materials Science). Other topics use weak proxies (1702, 1308, …). Local `raw_openalex_docs.csv` is country-year totals only — **no topic breakdown**.

### Root cause class

**Wrong ASJC / topic proxy** (+ missing raw for regen).

### Target source of truth

OpenAlex **topics** or **concepts** with documented IDs (prefer topics API), not Scopus ASJC 2500 for quantum. If ASJC must be used: Quantum Physics ≈ 3101 / related, never 2500.

### Regen stages

1. Partner delivers topic-country-year extract with `topic_id` / `subfield_id` + definition table.
2. Rebuild `viz3_data.js`; sync `topicSubfields` labels to real IDs.
3. Gate: Quantum rows must not carry Materials Science id; infectious spike 2020 retained as sanity check.

### Validation spot-checks

USA/CHN/IND/GBR 2015/2020/2022 for AI + Quantum; Quantum definition note in UI; no 2025 leakage unless labeled forecast.

### Partner file asks (exact)

1. OpenAlex extract: `year, country_iso3, topic_id, topic_display_name, works_count` for the 7 dashboard topics (or agreed replacements).
2. Mapping CSV: `dashboard_topic → openalex_topic_id(s)` with human definitions.
3. Confirmation that current `2500` quantum series should be **discarded**, not relabeled.

### UI contract

- Fix `topicSubfields` / gradient name `g-materials` for quantum.
- Subtitle shows real OpenAlex topic names.

---

## 2.4 Graph 4 — `viz4_data.js`

### Current pipeline hypothesis

111 countries, fields `domestic`, `international`, `gain`, all values at **0.1 precision** — looks hand-rounded. `CS661_Dataset/collaboration_premium.csv` has **year-level** OpenAlex-style domestic vs international citation averages for ~20 countries (2010–2024) — **not** identical to FE snapshot (e.g. USA domestic 16.9 in FE vs ~3–4 avg citations in recent premium years — different metric/window).

### Root cause class

**Unclear provenance / possible hand-built aggregate**; not a transparent freeze of `collaboration_premium.csv`.

### Target source of truth

Reproduce from OpenAlex (or SCImago) with a written formula, e.g. mean citations for domestic-only vs international co-authored works, fixed year window (recommend **2019–2023** or single year **2022**), ISO country set from shared master.

### Regen stages

1. Freeze metric definition in `scripts/country_panels/g4_premium.md`.
2. Compute from raw works or from expanded premium CSV for all ISO3 in master.
3. Export full precision (2–3 decimals); UI may round for display.
4. Optional year slider later; v1 can be one window if labeled.

### Validation spot-checks

USA/CHN/IND/CHE/SGP gain ordering vs recomputed raw; `gain = international - domestic`; no universal `.1` grid unless source is that coarse.

### Partner file asks (exact)

1. Code or SQL that created `collaboration_premium.csv`.
2. Whether `viz4_data.js` was derived from it or from a different spreadsheet.
3. If only 20-country premium exists, either expand extract to ~100+ countries or shrink the viz to those 20 (honest coverage).

### UI contract

- Title/footnote: exact window + formula.
- Region colors stay; drop any implication of live API.

---

## 2.5 Cross-graph dependencies (G1–G4)

| Shared asset | Used by |
|--------------|---------|
| ISO3 + English name master | G1–G4 |
| Year window policy | See §3 |
| `country_year_master` (GDP, GERD, docs, H, Q1/Q4) | G1, G2 filters |
| Yearly SJR panel | G1 H/docs, G2 quartiles |
| OpenAlex topic extract | G3 only |
| Collaboration premium extract | G4 only |

---

# 3. Coordination plan across all graphs

## 3.1 Shared country ISO master

Create `data/processed/country_master.csv`:

`iso3, iso2, name_en, region_g1, region_g2, region_g4, wb_code, is_taiwan_policy, ...`

Single join key for all country graphs. Taiwan: include with ISO3 `TWN` and explicit policy (WB often omits — don’t delete SJR rows).

## 3.2 Shared year window policy

| Graph | Recommended window | Notes |
|-------|-------------------|--------|
| G5 | **2015–2024** | Already locked in `config.YEAR_MIN/MAX` |
| G1 | **1996–2024** if SJR+WB allow; else 1999–2022 for GERD-complete core | Document sparse tail |
| G2 | Align with G1 core overlap: **1999–2022** (or 2024 if quartile totals exist) | Drop years without quartile integrity |
| G3 | **2000–2024** (truncate 1950–1999 noise unless story needs history) | Drop 2025 unless real |
| G4 | Single window **2019–2023** or year **2022** | Label clearly |

Do not claim one global 1996–2024 for every metric.

## 3.3 Single `data/processed/` layout

```
data/processed/
  country_master.csv
  country_year_master.parquet   # G1/G2
  g3_topic_country_year.parquet
  g4_collab_premium_country.parquet
  institution_master.csv        # G5
  collaboration_edges_full.csv  # G5
  institution_*_by_year.csv     # G5
  verification/
    g1_gates.md … g5_gates.md
```

Dashboard freeze:

```
dashboard/
  viz1_data.js
  ridgeline_data.js
  viz3_data.js
  viz4_data.js
  data/india_network/*.json
  india_network_data.js
```

## 3.4 Freeze / bundle process

1. Run graph ETL → write `data/processed/...`
2. Run `scripts/country_panels/freeze_dashboard.py` (to add) copying/emitting JS/JSON into `dashboard/`
3. G5: existing `09b` + `regenerate_india_network_data_js.py`
4. Commit payloads only after gates pass
5. Zip for course: from `dashboard/` + report — not from `_zip_extract/` trees

## 3.5 Report / viva claim alignment (kill false claims)

| Claim | Reality | Action |
|-------|---------|--------|
| “World Bank API live” | Static CSVs / JS | Delete from `data.js`, `index.html`, loading copy |
| “React” (if present in report) | Vanilla JS + D3 + Plotly | Fix report |
| G5 “complete partners” / top-300 = full | Truncated | Say overview/full/focus policies |
| Verification 23/23 = source-true | Weak gates | Replace with Stage F |
| G1 UMAP from live wealth/R&D/quality | H broken; EMA hiding jitter | Fix data; remove EMA |
| G2 ratio story | Capped at 5 | Uncap or label “capped” (prefer uncap) |
| G3 Quantum | Materials Science id | Fix or drop topic |
| G4 precision | Hand-round smell | Regen with formula |

## 3.6 Suggested global sequence

**G5 → G2 → G1 → G3 → G4**

| Order | Why |
|-------|-----|
| **G5 first** | Your ownership; ETL already exists; highest viva demo risk (IITK); no partner blocker for core honesty |
| **G2 next** | Clearest integrity bugs (`q1+q4>total`, ratio cap); shares SJR yearly ask with G1 |
| **G1 after G2** | Needs same yearly SJR; embedding regen after metrics fixed |
| **G3** | Blocked on partner OpenAlex topic dump |
| **G4 last** | Needs metric definition + possibly expanded premium extract; least coupled |

Alternate: G4 before G3 if partner premium code arrives first and topic dump slips — still keep G5 first.

---

# 4. What NOT to do

1. **Do not** cap ratios / gains / edge weights in the UI to hide outliers.
2. **Do not** EMA / smooth UMAP or time series to hide source jitter (remove existing G1 EMA after regen).
3. **Do not** hide countries (Taiwan lifetime ban) because one year is zero.
4. **Do not** footnote-away wrong ASJC (“Quantum ≈ Materials”) — fix the series.
5. **Do not** treat verification PASS as truth when tests don’t cover focus edges or static works.
6. **Do not** claim live World Bank / React / complete top-300 network.
7. **Do not** silently forward-fill GERD/H without an imputation flag.
8. **Do not** “fix” IITK–IITI by special-casing one pair in export.
9. **Do not** regenerate only `dashboard/` JS by hand-editing numbers.
10. **Do not** mix overview hub edges with full-network claims in viva script.

---

# Appendix A — G5 top-300 proof point (for partner ping)

From `collaboration_edges_full.csv` (IIT Kanpur ↔ IIT Indore):

| Year | Weight | In 202x_full.json? |
|------|--------|--------------------|
| 2015 | 24 | yes (above floor) |
| … | … | … |
| 2022 | 19 | yes |
| 2023 | 8 | **no** (slice min weight ≈ 15) |
| 2024 | 6 | **no** (slice min weight ≈ 17) |

Sum = 95. Detail/focus mode must show 8 and 6.

---

# Appendix B — Inventory note for partner reconciliation agent

If writing `SOURCE_RECONCILIATION_REPORT.md`, include at minimum:

- G5: `scripts/india_network/*`, `data/processed/institution_*.csv`, `dashboard/data/india_network/*`
- G1–G4: `CS661_Dataset/*` vs `dashboard/viz*_data.js` / `ridgeline_data.js`
- Explicit: **no topic-level OpenAlex raw locally for G3**
- Explicit: **`sjr_country_metrics.csv` is yearless** and poisons G1 H
)

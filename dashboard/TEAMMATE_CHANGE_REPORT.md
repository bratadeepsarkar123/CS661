Decision lock: see SEMANTICS_DECISION.md (same folder / raw_vault).

# TEAMMATE CHANGE REPORT — River → Pool → Tap

**Date:** 2026-07-12  
**Audience:** TAP owner (`app.js` / `index.html` / labels / filters)  
**Metaphor:** **RIVER** = vault CSVs (`CS661_Dataset/raw_vault/` + `READY_FOR_TEAM/`) · **POOL** = bundled `dashboard/*_data.js` · **TAP** = UI framing (your files)  
**Rule:** Pool is already corrected for G1–G4 metrics below. **Do not reinvent author-country Q1/Q4 in the pool.** Fix copy + filters in TAP only.

Canonical discrepancy log: `CS661_Dataset/raw_vault/POOL_VS_RIVER_DISCREPANCIES.md`  
Handoff CSVs: `CS661_Dataset/raw_vault/READY_FOR_TEAM/`

---

## 1. What happened (river vs what we claimed)

The dashboard **claimed** SCImago / OpenAlex / World Bank semantics, but several **pool** payloads had drifted from the **river** extracts (or used the wrong ontology):

| Graph | What we / FE claimed | What river actually is | What was wrong in the old pool |
|-------|----------------------|------------------------|--------------------------------|
| **G1** | Peer clustering on wealth, R&D, pubs, quality (UMAP) | `g1_features_panel.csv`: WB GDP/GERD + WB/OA docs + **SCImago Country Rank H** (lifetime-style stock, flat across years) | `H_Index` was yearless SJR stub scale (USA **53** vs true **3388**). UMAP `x,y` had been trained on that wrong H. UI credit still overstates “OpenAlex” for most years. |
| **G2** | “Global quality shift” Q1 vs Q4 | SCImago **journalrank** `Country` = **publisher country**, not author affiliation. `q1_q4_country_year.csv` has **uncapped** `ratio` (USA 2022 = **14.898**) | Old pool / `REBUILT` had **capped** ratios at 5.0 and some non-anchor drift. Any UI that implies *author-country* research output is semantically wrong for this series. |
| **G3** | Topic × country × year research volume | OpenAlex **concepts** (`topic_id_map.json`). Quantum = **`C58053490`** (“Quantum computer”) | Old pool used ASJC-like ids; Quantum = **`2500`** = Materials Science (**forbidden**). Counts will not match the old FE (expected). |
| **G4** | Collaboration premium (domestic vs international cites) | `collaboration_premium.csv` — **20 countries × years**; pool uses **2024** slice | Old pool had **111** undated countries with no river justification. |
| **G5** | India HE network | Pipeline + `india_outline.geojson` | Spot-check: outline / network JSON aligned — **no pool rewrite**. |

**Bottom line for viva:** River is the authority. Pool is now mostly aligned. Remaining TAP debt is **labels, credits, and hard-coded topic IDs** — not “re-download Q1/Q4 as author countries.”

---

## 2. What we already fixed in the POOL

Backups (do not delete): `*_BEFORE_POOLFIX.js` in `dashboard/`.  
Rebuild helper: `dashboard/_poolfix_rebuild.py`.  
UMAP regen helper: `dashboard/_regen_viz1_umap.py` · proof: `READY_FOR_TEAM/_notes/_umap_regen_proof.json`.

### G1 — `dashboard/viz1_data.js`

| Field | Before → After |
|-------|----------------|
| `H_Index` (USA 2022) | **53** → **3388** (joined from `g1_features_panel.csv`; 5966 rows updated; 52 left without panel H) |
| CHN / IND / GBR 2022 H | stub scale → **1595 / 1001 / 2183** |
| UMAP `x`,`y` | Old embedding on wrong H → **regenerated** 2026-07-12 from panel features (`log1p` GDP/docs/H + GERD; GERD ffill/bfill; per-year UMAP `n_neighbors=15`, `min_dist=0.1`, `random_state=42` + Procrustes year align). **4196 / 6022** rows got new coords; **1826** kept prior `x,y` (incomplete features after impute). USA 2022 xy ≈ `(-0.31, -11.78)` → `(6.04, 6.11)`. |
| Backup | `viz1_data_BEFORE_POOLFIX.js` (pre–H-fix snapshot; still the rollback for both H and pre-regen UMAP) |

### G2 — `dashboard/ridgeline_data.js`

| Field | Before → After |
|-------|----------------|
| Source | Drift / capped rebuild → **`q1_q4_country_year.csv`** (2705 country–years, 1999–2024) |
| `ratio` | Capped at **5.0** (e.g. USA/UK 2022) → **uncapped** (USA **14.898152**, UK **25.161841**) |
| Anchors USA/CHN/IND/GBR 2022 q1/q4/total | Exact match river |
| Argentina 1999 | q1=259,q4=1555,ratio≈0.167 → **q1=0, q4=303, ratio=0.0** (matches river) |
| Semantics | Still **publisher Country** |
| Backup | `ridgeline_data_BEFORE_POOLFIX.js` |

### G3 — `dashboard/viz3_data.js` (`window.CSV_DATA`)

| Field | Before → After |
|-------|----------------|
| Rows | ~48k dense legacy → **26 609** from `openalex_topic_country_year.csv` |
| Quantum `subfield_id` | **`2500`** (Materials Science) → **`C58053490`** |
| `topic_name` | Kept **dashboard labels** (`AI & Machine Learning`, `Quantum Computing`, …) so existing filter strings keep working |
| Year coverage | Legacy 1950–2025 dense → river extract (AI 1950–2024 full; most topics **2000–2024**; Infectious partial early years) |
| Backup | `viz3_data_BEFORE_POOLFIX.js` |

### G4 — `dashboard/viz4_data.js`

| Field | Before → After |
|-------|----------------|
| Countries | **111** undated → **20** from premium **year 2024** |
| USA domestic / intl / gain | 16.9 / 24.3 / 7.4 → **~3.0 / 6.3 / 3.3** |
| Backup | `viz4_data_BEFORE_POOLFIX.js` |

### G5 — `dashboard/data/india_network/*`

**No change** (outline byte-identical to river handoff).

### Not touched (TAP / report)

`app.js`, `index.html`, `style.css`, `WORKING.tex`, `india_network.js` logic.

---

## 3. What TEAMMATE must change in the TAP — checklist

Work only in TAP files. Pool already ships the corrected numbers / ids / uncapped ratios.

### G1

- [x] Update `VIZ_META[1].credit`: **World Bank (GDP, GERD, journal articles) · SCImago Country Rank (H-index; Documents fallback) · UMAP** — OpenAlex removed from G1 docs channel (2026-07-12).
- [ ] Re-check Plotly axis ranges / EMA smoother after UMAP regen (coords moved; EMA may still help leftover year flips).
- [ ] Tooltip: H is a **country quality stock** (flat across years in our panel), not a single-year H.

### G2 (critical)

- [ ] Any copy that implies **author affiliation / “where researchers publish from”** → rewrite to **publisher / journal country** (SCImago journalrank `Country`).
- [ ] Prefer wording like: “Q1 vs Q4 documents by **journal publisher country**.”
- [ ] Decide display policy for **uncapped** `ratio`: pool stores true `q1/q4` (UK 2022 ≈ 25). Optional TAP-only `Math.min(5, ratio)` for bars/labels — do **not** re-cap the pool file.
- [ ] Metric strings like “Total Q1 Journals Published” are OK if understood as **publisher-country doc sums**, not author counts.
- [ ] Read `READY_FOR_TEAM/_notes/G2_PUBLISHER_SCHEMA_NOTE.md` before changing filters.

### G3 (critical)

- [ ] Replace hard-coded `topicSubfields` ASJC numbers with OpenAlex concept ids from `topic_id_map.json`:

  | Topic | Old TAP id | Correct OpenAlex id |
  |-------|------------|---------------------|
  | AI & Machine Learning | 1702 | `C154945302` |
  | CRISPR & Genomics | 1308 | `C98108389` |
  | Infectious Diseases | 2725 | `C524204448` |
  | Data Science & Big Data | 1703 | `C2522767166` |
  | Renewable Energy | 2105 | `C188573790` |
  | Robotics & Automation | 2207 | `C34413123` |
  | Quantum Computing | **2500** | **`C58053490`** |

- [ ] Rename / restyle Quantum gradient key `g-materials` → something that is **not** Materials Science.
- [ ] Year credit: not “1950–2025” globally — priority window **2015–2024** complete; many topics start at **2000**; AI has 1950+.
- [ ] Do **not** filter on numeric `2500` / `1702` against pool — pool `subfield_id` is now `C…` strings. Filters on `topic_name` still work.

### G4

- [ ] UI should not imply 100+ countries: pool is **20 countries, year 2024**.
- [ ] Absolute cite levels differ from the old 111-country snapshot (expected).

### G5

- [ ] No pool action. Keep using existing network JSON + outline.

---

## 4. What is still wrong / optional next (pool)

| Item | Status | Notes |
|------|--------|-------|
| **G1 UMAP leftover rows** | Partial | **1826** viz1 rows still have old `x,y` (missing GDP/GERD/docs/H after impute). Majors 2015/2020/2022/2024 all regenerated. Optional: region-median GERD or drop those points from animation. |
| **G3 1950–1999 backfill** | **Skipped this pass** | Live OpenAlex probe **HTTP 429** (`dailyRemainingUsd: 0`, reset midnight UTC). Do **not** hammer the API. Resume later: `cd CS661_Dataset/raw_vault/04_openalex` → `python fetch_topics_full.py --years 1950-1999 --sleep 0.35`, then rebuild `viz3_data.js` from the CSV. Pending: Infectious **1972–1999**; Data / Renewable / Robotics / Quantum **1950–1999**. |
| **G4 expand beyond 20** | Open | Needs a documented extract — do not restore 111 without river. |
| **TAP label / id sync** | Open | Section 3 checklist (teammate). |

---

## 5. G2 publisher vs author — one paragraph for viva

Graph 2 is built from SCImago Journal Rank yearly exports by summing each journal’s `Total Docs` into Q1–Q4 buckets using **`Country` = the journal’s publisher country**, not the country of author affiliations. That means a Nature paper counts toward the United Kingdom (or whichever publisher country SJR lists), even if every author is in India; conversely, an Indian-published journal’s Q4 docs count for India regardless of foreign coauthors. We therefore describe G2 as a **publisher-country quality mix** (elite vs low-tier journal output hosted in that country), and we do **not** claim it measures where researchers themselves are based — that would require an author-affiliation microdata build we did not ship. The pool’s `ratio = q1/q4` is stored **uncapped** so viva numbers match the river CSV (e.g. USA 2022 ≈ 14.9); any on-screen cap at 5 is a display choice only.

---

## Quick file map

| Role | Path |
|------|------|
| This report (vault) | `CS661_Dataset/raw_vault/TEAMMATE_CHANGE_REPORT.md` |
| This report (dashboard copy) | `dashboard/TEAMMATE_CHANGE_REPORT.md` |
| Discrepancy + proof log | `CS661_Dataset/raw_vault/POOL_VS_RIVER_DISCREPANCIES.md` |
| River handoff | `CS661_Dataset/raw_vault/READY_FOR_TEAM/` |
| G2 schema note | `READY_FOR_TEAM/_notes/G2_PUBLISHER_SCHEMA_NOTE.md` |
| G3 extract status | `READY_FOR_TEAM/_notes/G3_EXTRACT_STATUS.md` (also `04_openalex/G3_EXTRACT_STATUS.md`) |

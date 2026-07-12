# Per-graph pool changelog (after raw-file consolidation)

**Date:** 2026-07-12  
**Audience:** You (viva / review) — plain language of what changed in the **pool** (dashboard data files) when we aligned them to the **river** (vault / `READY_FOR_TEAM` CSVs).  
**Not changed here:** TAP UI (`app.js`, `index.html`, `style.css`) — labels/filters are teammate debt unless noted.

**Metaphor:** RIVER = source CSVs · POOL = `dashboard/*_data.js` · TAP = UI framing.

**Locked G2 decision:** publisher-country Q1/Q4 (SCImago journalrank `Country`). **Not** author-affiliation join.

**Backups (do not delete):**  
`dashboard/viz1_data_BEFORE_POOLFIX.js`, `ridgeline_data_BEFORE_POOLFIX.js`, `viz3_data_BEFORE_POOLFIX.js`, `viz4_data_BEFORE_POOLFIX.js`.

---

## Summary table

| Graph | Title (short) | Pool file | Changed? | One-line what changed |
|-------|---------------|-----------|----------|------------------------|
| **G1** | Peer clusters (UMAP) | `viz1_data.js` | **Yes** | H-index fixed to SCImago stock; UMAP `x,y` regenerated for most rows |
| **G2** | Q1 vs Q4 ridgeline | `ridgeline_data.js` | **Yes** | Rebuilt from river; **uncapped** `ratio`; publisher-country semantics |
| **G3** | Topic × country × year | `viz3_data.js` | **Yes** | OpenAlex concept ids (Quantum = `C58053490`); thinner early years |
| **G4** | Collaboration premium | `viz4_data.js` | **Yes** | **20** countries, year **2024** only (was 111 undated) |
| **G5** | India HE network | `data/india_network/*` | **No** | Already matched river outline / network JSON |

---

### Graph 1 — Peer clustering (wealth, R&D, pubs, quality / UMAP)

- **Before (old pool):** Claimed a proper country quality H-index, but `H_Index` was on a wrong stub scale (USA 2022 **53** instead of SCImago stock **3388**). UMAP positions were trained on that bad H, so peer layout was misleading.
- **River used:** `READY_FOR_TEAM/g1_features_panel.csv` (World Bank GDP/GERD + docs + SCImago Country Rank H). Related: `scimago_country_rank_1996_2024.csv`.
- **After (new pool):** In `dashboard/viz1_data.js`, joined correct `H_Index` from the panel (~5966 rows; USA 2022 **3388**; CHN/IND/GBR 2022 **1595 / 1001 / 2183**). Regenerated UMAP `x,y` for **4196 / 6022** rows; **1826** sparse rows still keep old coords. Spot-check USA 2022 ≈ `(6.04, 6.11)` (was ~`(−0.31, −11.78)`). Backup: `viz1_data_BEFORE_POOLFIX.js`.
- **Still unchanged / teammate TAP:** Credit text may still overstate “OpenAlex” alone; should say WB + OpenAlex (late docs) + SCImago H + UMAP. Tooltip: H is a **stock** (flat across years in panel), not a single-year H. Plotly ranges / EMA may need a re-check after coord move.
- **Net effect for viva:** Clusters now sit on real SCImago H-index and mostly re-embedded UMAP — USA is no longer a tiny-H outlier for the wrong reason.

---

### Graph 2 — Q1 vs Q4 “quality mix” (ridgeline)

- **Before (old pool):** Numbers looked OK on USA/CHN/IND/GBR anchors in places, but **non-anchor rows drifted** (e.g. Argentina 1999) and **`ratio` was capped at 5.0** (USA/UK 2022 flattened). UI often implied *author-country* research, which this series is **not**.
- **River used:** `READY_FOR_TEAM/q1_q4_country_year.csv` (same panel as `country_year_publisher_quartile_docs_1999_2024.csv`). See `_notes/G2_PUBLISHER_SCHEMA_NOTE.md`.
- **After (new pool):** Replaced `dashboard/ridgeline_data.js` from river (**2705** country–years, 1999–2024) with **uncapped** `ratio`. USA 2022: q1 **530553**, q4 **35612**, total **834932**, ratio **14.898152** (exact river). Argentina 1999: **q1=0, q4=303, ratio=0** (was 259/1555/0.167). Backup: `ridgeline_data_BEFORE_POOLFIX.js`.
- **Still unchanged / teammate TAP:** Any copy saying authors / “where researchers publish from” must become **journal publisher country**. Optional display-only `min(5, ratio)` in TAP — **do not** re-cap the pool file. Chart scales will stretch for elite publishers (UK 2022 ratio ≈ **25**).
- **Net effect for viva:** G2 is honestly a **publisher-country** Q1/Q4 mix with true uncapped ratios matching the vault CSV — not an author-affiliation story.

---

### Graph 3 — Topic × country × year research volume

- **Before (old pool):** Used **ASJC-like** numeric subfield ids. Quantum was **`2500`** = Materials Science (**wrong / forbidden**). Legacy FE was denser (~48k rows, often 1950–2025) than the OpenAlex extract we actually have.
- **River used:** `READY_FOR_TEAM/openalex_topic_country_year.csv` + `topic_id_map.json` / `.csv`.
- **After (new pool):** Rebuilt `dashboard/viz3_data.js` (`window.CSV_DATA`) to **20 882** rows (**2000–2024 honesty window**). Quantum `subfield_id` = **`C58053490`**. Pre-2000 AI mega-concept / incomplete Infectious backfill **omitted** from tap (river CSV still full). See `docs/GRAPH3_DATA_ROOT_CAUSE.md`. Backup: `viz3_data_BEFORE_HONEST_TRIM.js` (+ earlier `viz3_data_BEFORE_POOLFIX.js`).
- **Still unchanged / teammate TAP:** Cross-topic absolute bar heights remain imperfect until AI re-extract uses `C119857082` Machine learning. Within-topic trends OK.
- **Net effect for viva:** Topic series is now real OpenAlex concepts (Quantum ≠ Materials Science); expect thinner pre-2000 coverage than the old fake-dense FE.

---

### Graph 4 — Collaboration premium (domestic vs international cites)

- **Before (old pool):** **111** undated countries with numbers that did **not** match any single year of the river premium file — **91** countries had no river justification.
- **River used:** `READY_FOR_TEAM/collaboration_premium.csv` (20 countries × years 2010–2024). Notes: `_notes/G4_PREMIUM_GAP.md`.
- **After (new pool):** Regenerated `dashboard/viz4_data.js` from premium **year 2024** only — **20** countries (`{name, region, domestic, international, gain}`). USA ≈ **3.0 / 6.3 / 3.3** (was 16.9 / 24.3 / 7.4). Russia renamed from “Russian Federation” where needed. Backup: `viz4_data_BEFORE_POOLFIX.js`.
- **Still unchanged / teammate TAP:** UI must not imply 100+ countries. Absolute cite levels differ from the old snapshot (expected). Do not restore 111 without a documented new extract.
- **Net effect for viva:** Smaller, honest 2024 premium chart grounded in the river CSV — not an inflated undated world list.

---

### Graph 5 — India higher-education collaboration network

- **Before (old pool):** Claimed pipeline + India outline for the network map.
- **River used:** `READY_FOR_TEAM/india_outline.geojson` (+ existing `dashboard/data/india_network/` yearly / all-years JSON).
- **After (new pool):** **No rewrite.** Outline byte-identical to river handoff; network JSON set present (manifest + years). Spot-check aligned.
- **Still unchanged / teammate TAP:** Label/footnote polish for static vs cumulative fields only (no pool action required for consolidation).
- **Net effect for viva:** G5 did not need a pool fix in this consolidation pass — data already matched the handoff.

---

## What this consolidation did *not* do

1. **No TAP edits** in this pass (`app.js` / HTML / CSS stay teammate-owned for publisher wording, topic ids, credits).
2. **No author-country rebuild for G2** — locked as publisher-country (see `SEMANTICS_DECISION.md`).
3. **G3 early-year backfill** still pending when OpenAlex budget allows (1950–1999 for several topics).
4. **G1:** 1826 UMAP leftover rows still on old coords until denser impute or drop.

---

## Proof anchors (spot-checked after fix)

| Check | Result |
|-------|--------|
| G1 USA 2022 `H_Index` | **3388** |
| G2 USA 2022 `ratio` | **14.898152** (uncapped) |
| G3 Quantum id | **`C58053490`** |
| G4 country count | **20** (2024) |
| G5 outline | Unchanged / matches river |

Canonical discrepancy log: `POOL_VS_RIVER_DISCREPANCIES.md` · Teammate TAP checklist: `TEAMMATE_CHANGE_REPORT.md` · Handoff folder: `READY_FOR_TEAM/`.

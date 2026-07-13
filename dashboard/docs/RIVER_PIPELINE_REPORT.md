# CS661 Dashboard — River Pipeline Report

**Date:** 2026-07-12  
**Focus:** Raw / background data first (**river**), not pool cleanup.  
**Live app:** `dashboard/`  
**Sample anchors used below:** United States & India, year **2022** (plus 2024 where the source switches).

Metaphor used throughout:

| Layer | Meaning | Typical location |
|-------|---------|------------------|
| **River** | Raw / background CSVs, APIs, PDFs | `CS661_Dataset/`, `raw_vault/`, NIRF scrapes |
| **Pool** | Bundled files the charts drink | `dashboard/*_data.js`, `dashboard/data/india_network/` |
| **Tap** | UI labels, filters, charts | `dashboard/app.js`, `graphs/g*/`, `india_network.js` |

---

## 1. What should happen (ideal)

One clean river feeds each metric. The pool is only a thin pack of that river for the browser. The tap draws charts and writes honest labels — it never invents H-index, GDP, R&D, or publication counts. If two graphs show the “same” label (e.g. H-index), they must drink from the **same river definition**, or the label must say they are different things.

---

## 2. What happens right now (G1–G5)

### Graph 1 — Peer clusters (UMAP bubbles)

| Layer | What |
|-------|------|
| **Shows** | Country bubbles over years; neighbors similar on wealth, R&D, pubs, quality |
| **Pool** | `dashboard/viz1_data.js` → `VIZ1_DATA` |
| **Tap** | `dashboard/graphs/g1/g1.js` (+ `app.js` shell) |
| **River (good path)** | `CS661_Dataset/raw_vault/READY_FOR_TEAM/g1_features_panel.csv` built from World Bank GDP/GERD/articles + SCImago Country Rank H (+ Documents fallback) |
| **River (stale path still on disk)** | `CS661_Dataset/master_dataset.csv` + `sjr_country_metrics.csv` still carry **wrong** H (USA **53**) |

**USA / India 2022 in live pool:**  
USA: H=**3388**, GDP PPP≈**77 861**, GERD≈**3.49%**, Docs≈**447 539** (WB articles)  
India: H=**1001**, GDP PPP≈**9 207**, GERD≈**0.65%** (forward-filled), Docs≈**200 488**

---

### Graph 2 — Q1 vs Q4 quality mix (bars)

| Layer | What |
|-------|------|
| **Shows** | Q1 vs Q4 document bars by country–year; ratio = q1/q4 |
| **Pool** | `dashboard/ridgeline_data.js` → `REAL_RIDGELINE_DATA` |
| **Tap** | `dashboard/graphs/g2/g2.js` |
| **River (chart numbers)** | SCImago **journalrank** XLS → `READY_FOR_TEAM/q1_q4_country_year.csv` (publisher **Country**, not author country) |
| **Sidebar H / GDP / R&D** | **Not from river** — hardcoded map + fake year growth inside `g2.js` |

**USA / India 2022 in live pool (chart):**  
USA: q1=**530 553**, q4=**35 612**, total=**834 932**, ratio≈**14.90**  
India: q1=**1 606**, q4=**15 095**, total=**48 309**, ratio≈**0.11**

**Same labels in G2 sidebar (invented):**  
USA 2022: H≈**1325**, GDP≈**97 054**, GERD=**2.74%** (fixed base, not WB)  
India 2022: H≈**306**, GDP≈**3 000**, GERD=**0.85%**

---

### Graph 3 — Topic frontiers

| Layer | What |
|-------|------|
| **Shows** | Topic × country × year publication volume (7 topics) |
| **Pool** | `dashboard/viz3_data.js` → `window.CSV_DATA` |
| **Tap** | `dashboard/graphs/g3/g3.js` |
| **River** | OpenAlex concepts → `READY_FOR_TEAM/openalex_topic_country_year.csv` + `topic_id_map.json` |

**USA / India 2022 AI & Machine Learning (pool, concept `C119857082`):**  
USA **41 530** · India **25 155** works  

Note: the river CSV also still contains a larger “mega AI” concept (`C154945302`) with much bigger counts (USA 2022 **111 017**). The live pool correctly prefers Machine learning `C119857082`.

---

### Graph 4 — Collaboration premium (dumbbell)

| Layer | What |
|-------|------|
| **Shows** | Domestic vs international **mean citations per paper**; gap = premium |
| **Pool** | `dashboard/viz4_data.js` → `VIZ4_BY_YEAR` (20 countries × 2010–2024) |
| **Tap** | `dashboard/graphs/g4/g4.js` (falls back to fake `data.js` only if pool missing) |
| **River** | `READY_FOR_TEAM/collaboration_premium.csv` (= `CS661_Dataset/collaboration_premium.csv`) from OpenAlex domestic/intl split |

**USA / India 2022:**  
USA: dom **3.932** / intl **12.833** / gain **8.901**  
India: dom **6.395** / intl **14.894** / gain **8.499**

---

### Graph 5 — India HE collaboration network

| Layer | What |
|-------|------|
| **Shows** | Map + network of Indian institutes; NIRF rank / funding / patents footnotes |
| **Pool** | `dashboard/data/india_network/{year}_*.json` + `india_network_data.js` |
| **Tap** | `india_network.js` via `graphs/g5/g5.js` (legacy fake `DATA.getIndiaNetwork` only if JSON not ready) |
| **River** | OpenAlex collab edges; NIRF PDFs/HTML; SCImago Institutions **2019** static %; outline GeoJSON — under `scripts/india_network/`, `CS661 Project/data/processed/`, vault `05_nirf/`, `08_scimago_institutions_india/` |

**Example:** IISc `total_works`=**87 588** (OpenAlex institution stock), `scimago_pct`=**1.63** (year **2019** by design), NIRF rank from mapped season.

---

## 3. Where the river is (exact paths)

### Canonical handoff (prefer this)

`CS661_Dataset/raw_vault/READY_FOR_TEAM/`

| File | Feeds |
|------|-------|
| `g1_features_panel.csv` | G1 features |
| `scimago_country_rank_1996_2024.csv` | G1 H-index + SCImago Documents |
| `q1_q4_country_year.csv` | G2 Q1/Q4 |
| `country_year_publisher_quartile_docs_1999_2024.csv` | G2 (same panel, clearer name) |
| `openalex_topic_country_year.csv` | G3 |
| `topic_id_map.json` / `.csv` | G3 IDs |
| `collaboration_premium.csv` | G4 |
| `raw_openalex_docs.csv` | G1 optional OA totals (not for bubble size) |
| `india_outline.geojson` | G5 outline |

### Deeper vault (source downloads)

| Folder | Content |
|--------|---------|
| `CS661_Dataset/raw_vault/01_world_bank/` | WB GDP, GERD, articles |
| `…/02_scimago_country/` | SCImago Country Rank year files + merged CSV |
| `…/03_scimago_journal_quartiles/` | Journalrank XLS → G2 aggregate |
| `…/04_openalex/` | OpenAlex topics + docs extracts |
| `…/05_nirf/` | NIRF rankings / funding / patents |
| `…/06_unesco_uis/` | UNESCO GERD (reference; not primary in live G1) |
| `…/07_oecd_msti/` | OECD MSTI GERD (reference) |
| `…/08_scimago_institutions_india/` | India institution quality |
| `…/11_geojson_india/` | India outline |

### Older / mixed “river” still sitting at dataset root (dangerous)

`CS661_Dataset/`

- `master_dataset.csv` — mixed panel; **H still stub 53**
- `sjr_country_metrics.csv` — **yearless stub** H / Q1% / Q4% (94 countries)
- `raw_worldbank.csv`, `raw_wb_publications.csv`, `raw_openalex_docs.csv` — real series pieces
- `collaboration_premium.csv` — real G4 river (also copied to READY_FOR_TEAM)
- `raw_oecd_msti.csv`, `raw_gerd_sectors.csv` — GERD enrichment, not wired as G1 primary

### G5 processed river (not inside `CS661_Dataset` top-level)

- `CS661 Project/data/processed/institution_master.csv`
- `…/collaboration_edges_full.csv`
- `…/institution_funding.csv`, `institution_patents.csv`
- Checkpoints under `data/checkpoints/*/data/raw/` and `…/processed/`

### Orphan / stub “data” that looks like a river but is tap fiction

- `dashboard/data.js` — hardcoded countries, fake topic growth, fake collab, fake India nodes  
- `dashboard/graphs/g2/g2.js` → `getCountryMetrics()` — hardcoded H/GDP/R&D  
- `dashboard/panel_data.js` — extra Q1/Q4-like ISO panel (loaded in HTML; **not** the G2 ridgeline source of truth)

---

## 4. Why numbers disagree for the same label

### H-index

| Place | Source + definition | USA 2022 | India 2022 |
|-------|---------------------|----------|------------|
| **G1 pool** | SCImago **Country Rank** cumulative H (flat across years in panel) | **3388** | **1001** |
| **River good** | `scimago_country_rank_1996_2024.csv` / `g1_features_panel.csv` | 3388 | 1001 |
| **River bad** | `sjr_country_metrics.csv` → still inside `master_dataset.csv` | **53** | **27** |
| **G2 sidebar** | Hardcoded base H + `+2` per year since 1999 (`g2.js`) | ≈**1325** | ≈**306** |
| **G5** | Institution **percentile / SIR**, not country H | n/a (e.g. IISc pct 1.63) | n/a |

**Why different:** Three different things were all called “H-index”: (1) real country H, (2) tiny yearless stub, (3) invented UI numbers.  
**Verdict:** **Different rivers + tap inventing.** G1 now drinks the good river; master/stub river still polluted; G2 tap invents.

---

### GDP per capita

| Place | Source + definition | USA 2022 | India 2022 |
|-------|---------------------|----------|------------|
| **G1** | World Bank `NY.GDP.PCAP.PP.CD` via panel | ≈**77 861** | ≈**9 207** |
| **G2 sidebar** | Hardcoded base GDP × `1.025^(year−1999)` | ≈**97 054** | ≈**3 000** |
| **data.js stub** | Separate fake GDP growth from 2010 (legacy) | not used by G1 | not used by G1 |

**Verdict:** **Same label, different rivers** — G1 = WB PPP; G2 sidebar = **tap inventing**.

---

### GERD / R&D (% of GDP)

| Place | Source + definition | USA 2022 | India 2022 |
|-------|---------------------|----------|------------|
| **G1** | World Bank `GB.XPD.RSDV.GD.ZS` | **3.487** | **0.646** (master empty 2022+ → forward fill) |
| **G2 sidebar** | Hardcoded constant `rd` (no year) | **2.74** | **0.85** |
| **Vault extras** | OECD MSTI, UNESCO UIS folders exist | not primary in live G1 | not primary |

Guide `CS661 Project/RD_Spending_Data_Guide.md` once recommended OECD > UIS > WB merge. Live G1 uses **WB only** (with fills).  
**Verdict:** **Partial pollution** — multiple GERD rivers on disk; live chart uses WB; G2 sidebar invents different numbers.

---

### “Publications” / documents / works

| Place | What it actually counts | USA 2022 | India 2022 |
|-------|-------------------------|----------|------------|
| **G1 bubble size** | WB scientific **journal articles** `IP.JRN.ARTC.SC` | ≈**447 539** | ≈**200 488** |
| **G1 SCImago Documents (same panel, not size when WB exists)** | SCImago country Documents | **751 197** | **286 865** |
| **OpenAlex country totals** (`raw_openalex_docs.csv`) | Broad OA **works** | **1 740 804** | **380 143** |
| **G2 bar `total`** | Sum of docs in journals whose **publisher** is in that country | **834 932** | **48 309** |
| **G3 topic count** | OpenAlex works with a **concept** (e.g. ML) | AI **41 530** | AI **25 155** |
| **G5 node `total_works`** | OpenAlex **institution** works (stock) | n/a | IISc **87 588** |

**Why different:** Five real measurement systems, one casual English word (“publications”).  
**Verdict:** **Different rivers** (mostly honest if labeled). Mixing them (e.g. old G1 WB→OpenAlex cliff) was pollution. Policy now: G1 size = WB else SCImago Documents; **never** OpenAlex for G1 size.

---

### Citations / “quality”

| Place | Definition | USA 2022-ish |
|-------|------------|--------------|
| **G4** | OpenAlex mean cites/paper, domestic vs international | dom **3.93** / intl **12.83** |
| **SCImago Country Rank** | Citations per document (country stock view) | **12.93** |
| **G2** | Not citations — Q1/Q4 **document counts** by publisher country | ratio **14.90** |
| **master `Q1_Percent`** | Yearless stub % from `sjr_country_metrics` | **47.97%** flat every year |

**Verdict:** **Different rivers.** G4 ≠ SCImago cites/doc ≠ G2 quality mix ≠ stub Q1%.

---

### Q1 / Q4 “quality”

| Place | Definition |
|-------|------------|
| **G2 pool** | Documents in Q1 vs Q4 journals by **publisher country** (year-varying) |
| **master / sjr stub** | Yearless **journal-share %** — wrong unit for G2 |

**Verdict:** **Different rivers.** Keep G2 journalrank aggregate; discard stub % as a G2 source.

---

## 5. Is the river polluted?

### **PARTIAL — YES**

Evidence:

1. **Two H-index rivers claim the same country label**  
   - Good: `scimago_country_rank_1996_2024.csv` / `g1_features_panel.csv` (USA 3388)  
   - Bad: `sjr_country_metrics.csv` → `master_dataset.csv` (USA 53; Ireland 111 > USA 53)

2. **Multiple “publications” rivers** without one naming standard (WB / SCImago Documents / OpenAlex works / publisher-quartile docs / institution works).

3. **GERD:** WB is live primary, but OECD + UNESCO still sit beside it; India 2022+ GERD empty in master → fills create a third “soft” series.

4. **G3 river CSV holds both mega-AI and Machine-learning concepts** under overlapping product names — pool picked one; river still dual.

5. **Tap pollution that pretends to be data** (not river, but users see it as numbers):  
   - `graphs/g2/g2.js` hardcoded H/GDP/R&D  
   - `data.js` fake countries / topics / collab / India (fallback / legacy)

6. **Good news:** For G1–G4, `READY_FOR_TEAM/` is largely a **cleaned handoff**. Live pools mostly match that handoff for core chart series. Pollution is worst in **old root CSVs + tap inventions**, not in every vault file.

---

## 6. What to keep vs discard (recommendation only — no file changes)

| Conflict | Keep | Discard / demote | Why |
|----------|------|------------------|-----|
| **Country H-index** | `scimago_country_rank_1996_2024.csv` → panel H | `sjr_country_metrics.csv` H; master H=53 | Stub scale is wrong institution/journal-ish, not Country Rank |
| **G1 GDP / GERD** | World Bank WDI series in panel | G2 hardcoded rd/gdp; optional OECD/UIS until a written merge rule exists | WB already powers G1; inventing in tap is worse than sparse GERD |
| **G1 publication size** | WB articles, else SCImago Documents | OpenAlex totals for bubble size | OA is ~3× larger → fake cliffs (`G1_TOTAL_DOCS_POLICY.md`) |
| **G2 Q1/Q4** | Publisher-country journalrank aggregate (`q1_q4_country_year.csv`) | master `Q1_Percent` / stub; author-country fantasy rebuild | Locked semantics (`SEMANTICS_DECISION.md`) |
| **G2 sidebar H/GDP/R&D** | Reuse G1 panel (same country–year) **after** river lock | `getCountryMetrics` invention | Same labels as G1 must share G1 river |
| **G3 topics** | Concept IDs in `topic_id_map.json` (Quantum `C58053490`, AI primary `C119857082`) | ASJC `2500`; mega-AI as default “AI & ML” | Wrong science / wrong scale |
| **G4 cites** | `collaboration_premium.csv` (20 countries × years) | `data.js` COLLAB_DATA; old 111-country undated FE | River is documented OpenAlex premium |
| **G5 works / NIRF / SIR** | Processed pipeline + static-2019 SIR footnotes | `DATA.getIndiaNetwork` demo growth | Real JSON already exists |
| **master_dataset.csv** | Keep only as archive / rebuild input after H fix | Do not treat as live G1 truth until stub H removed | Currently disagrees with READY_FOR_TEAM panel |

---

## 7. What NOT to do yet

1. **Do not “just join pools”** so G1 and G2 show the same H by copying JS objects. First lock **which river file owns H / GDP / GERD / pubs**.
2. **Do not delete or “clean” all pools** until those river choices are written down and accepted (especially: discard stub H; keep publisher-country G2; keep WB-not-OA for G1 size).
3. **Do not merge OECD + UNESCO + WB GERD** into G1 just because the spending guide suggested it — that is a new river design, not a pool patch.
4. **Do not rebuild G2 as author-country** without an explicit product decision (currently locked out).
5. **Do not dampen G3 Infectious spikes** or invent pre-1974 topic bars to make charts look smoother.
6. **Do not treat `data.js` / G2 `baseMetrics` as background data** — they are tap fiction.

---

## Short bottom line

The **background river is only partly clean**. The good channel is `CS661_Dataset/raw_vault/READY_FOR_TEAM/`. The polluted channel is still `master_dataset.csv` + `sjr_country_metrics.csv` (fake tiny H) plus several different real “publication” systems. On top of that, **Graph 2’s sidebar invents H-index, GDP, and R&D** that disagree with Graph 1 even when both panels say the same words.

**Next step (when you choose):** pick one river owner per metric label, demote stubs, then rebuild pools — not the other way around.

---

## Evidence pointers (for auditors)

| Claim | Where checked |
|-------|----------------|
| Live G1 USA 2022 H=3388, Docs≈447539 | `dashboard/viz1_data.js` |
| Live G2 USA 2022 ratio≈14.90 | `dashboard/ridgeline_data.js` |
| G2 invents H/GDP/R&D | `dashboard/graphs/g2/g2.js` lines 15–119 |
| Master still H=53 | `CS661_Dataset/master_dataset.csv` |
| Stub file | `CS661_Dataset/sjr_country_metrics.csv` |
| Good H river | `…/READY_FOR_TEAM/scimago_country_rank_1996_2024.csv` |
| G4 matches premium CSV | `viz4_data.js` ↔ `collaboration_premium.csv` |
| Prior audits | `dashboard/SOURCE_RECONCILIATION_REPORT.md` (partly outdated on pool H), `TEAM_HANDOFF_README.md`, `PER_GRAPH_POOL_CHANGELOG.md`, `raw_vault/POOL_VS_RIVER_DISCREPANCIES.md` |

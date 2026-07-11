# CS661 Dashboard — Source Reconciliation Report

**Date:** 2026-07-12  
**Workspace:** `C:\Users\brata\Downloads\CS661`  
**Primary local dataset:** `CS661_Dataset\`  
**Frontend payloads:** `dashboard\`  
**Helper scripts:** `dashboard/_recon_source_equality.py`, `dashboard/_recon_g1_g4_extra.py`, `dashboard/_recon_g5_spot.py`  
**Raw tool output:** `dashboard/_recon_source_equality_out.txt`, `dashboard/_recon_g1_g4_extra_out.txt`

---

## 1. Executive verdict

**Can we claim backend raw = frontend bundled = claimed external sources (SCImago / World Bank / OpenAlex / NIRF) today?**

### **NO.**

| Claim | Verdict |
|-------|---------|
| Frontend = local `CS661_Dataset` backend | **PARTIAL** — Graph 1 metrics largely match master/raw WB for overlapping years; Graphs 2–4 do **not** equal local candidates; Graph 5 matches a *different* pipeline (`data/processed` / `CS661 Project/data/processed`), not `CS661_Dataset`. |
| Frontend / local = official SCImago Country Rank | **NO** — country H-index in G1 is absurd vs public SCImago (USA H=53 vs ~1657); G2 Q1/Q4 counts have no year×country SCImago raw file; G5 SCImago % is a static 2019 SIR snapshot by design. |
| Frontend / local = live World Bank | **UNVERIFIED live** (API timed out from this environment). **Local equality holds:** `viz1` GDP/GERD = `raw_worldbank.csv` = `master_dataset.csv` where filled. Docs through ~2022 = `raw_wb_publications.csv` (WB scientific articles), **not** SCImago Documents / not OpenAlex. |
| Frontend = OpenAlex | **PARTIAL** — G1 2023–24 docs switch to OpenAlex totals; G3 topic series has **no** local OpenAlex topic dump; G5 `total_works` matches processed OpenAlex-derived master. |
| Frontend = NIRF | **G5 only** — not in `CS661_Dataset`; ranks/funding/patents from NIRF scrape pipeline with documented gaps. |

---

## 2. Inventory of `CS661_Dataset`

**No README** in the folder. 11 files:

| File | Size | Likely graph(s) | Role / schema |
|------|------|-----------------|---------------|
| `master_dataset.csv` | 920 KB | **G1** (primary), G2 candidate | 7340 rows; 259 countries; years **1996–2024**. Cols: `Country_Code`, `Country_Name`, `Year`, `GDP_Nominal`, `GDP_Per_Capita_Nominal`, `GDP_Per_Capita_PPP`, `PPP_Conversion_Scale`, `GERD_Percent_GDP`, `Researchers_Per_Million`, `GERD_Sector_*`, `Total_Docs`, `Citable_Docs`, `Citations_Per_Doc`, `H_Index`, `Q1_Percent`, `Q4_Percent` |
| `master_dataset_imputed.xlsx` | 953 KB | G1 imputed view | Same columns; fills some GERD/docs gaps (values **differ** from FE for 2024 GERD) |
| `raw_worldbank.csv` | 696 KB | **G1** | Country-year macro: GDP*, GERD%, researchers |
| `raw_wb_publications.csv` | 117 KB | **G1 docs** | `Country_Code`, `Year`, `WB_Pubs` (years ~1996–2022) |
| `raw_openalex_docs.csv` | 84 KB | **G1 docs (late years)** | `Country_Code`, `Year`, `Total_Docs_OA` (1996–2024) |
| `raw_gerd_sectors.csv` | 125 KB | G1 sectors | Gov / HE / Biz GERD shares |
| `raw_oecd_msti.csv` | **50.6 MB** | G1 GERD enrichment | OECD MSTI SDMX export (36 cols) |
| `sjr_country_metrics.csv` | 3 KB | **G1 H/Q%**, G2 candidate | **94 rows, NO Year** — `Q1_Percent`, `Q4_Percent`, `Citations_Per_Doc`, `H_Index`, `Num_Journals` |
| `collaboration_premium.csv` | 20 KB | **G4 candidate** | 300 rows; **20 countries**; years 2010–2024; domestic/intl avg citations + gain |
| `deep_dive_dataset_imputed.xlsx` | 18 KB | G1 deep-dive | Country-level averages (no year) |
| `merge_scimago_kaggle.py` | 2 KB | ETL stub | Expects **`scimago_country_rank.csv`** (Kaggle) — **FILE ABSENT** from this folder |

**Fill rates (`master_dataset.csv`):** GDP_PPP 95.1% · GERD 42.8% · Total_Docs 96.6% · H_Index / Q1% / Q4% **36.7%** (and those SJR fields are **year-static** once filled).

**Not in `CS661_Dataset`:** India network / NIRF / OpenAlex works / SCImago Institutions / topic-country OpenAlex series / full SCImago Country Rank year panel. Those live under `data/`, `data/checkpoints/`, `CS661 Project/data/`, `scripts/india_network/`.

---

## 3. Per-graph reconciliation

### Graph 1 — High-Dimensional Peer Clustering (`viz1_data.js` → `VIZ1_DATA`)

**UI credit (`app.js`):** “World Bank API · OpenAlex (t-SNE/UMAP Projection)”

#### Frontend fields used
`Country_Code`, `Country_Name`, `Year`, `GDP_Per_Capita_PPP`, `GERD_Percent_GDP`, `Total_Docs`, `H_Index`, `Region`, `x`, `y`

#### Local candidates
- `CS661_Dataset/master_dataset.csv` (+ imputed xlsx)
- `raw_worldbank.csv`, `raw_wb_publications.csv`, `raw_openalex_docs.csv`
- `sjr_country_metrics.csv` (yearless)
- Missing: `scimago_country_rank.csv` (referenced by merge script)

#### Claimed external sources
World Bank (`NY.GDP.PCAP.PP.CD`, `GB.XPD.RSDV.GD.ZS`, scientific articles), OpenAlex docs, SCImago (for H / quality — **implied by merge script / proposal**, not fully by UI credit)

#### Join keys
ISO-3 `Country_Code` + `Year`

#### Spot-check (FE vs master vs raw)

| Country | Year | GDP_PPP FE=master=rawWB? | GERD FE=master=rawWB? | Total_Docs provenance | H_Index |
|---------|------|--------------------------|------------------------|----------------------|---------|
| USA | 2015 | YES 56849.47 | YES 2.773 | = `WB_Pubs` 436908.38 (**≠** OA 981331) | 53 static |
| USA | 2020 | YES 64401.51 | YES 3.418 | = WB_Pubs 457586.9 | 53 |
| USA | 2022 | YES 77860.91 | YES 3.487 | = WB_Pubs 457335.25 (**≠** OA 1.74M) | 53 |
| USA | 2024 | YES 85809.90 | FE=3.447; **master GERD empty**; FE forward-filled from 2023 | = OA 1211879 | 53 |
| CHN | 2015/20/22 | YES | YES | = WB_Pubs | 39 static |
| CHN | 2024 | YES | FE filled; master empty | = OA | 39 |
| IND | 2015/20 | YES | YES | = WB_Pubs | 27 |
| IND | 2022/24 | YES GDP | GERD forward-filled 0.64558 (master empty 2022+) | 2022=WB_Pubs; 2024=OA | 27 |
| GBR / DEU | 2015/20/22 | YES | YES | = WB_Pubs | 48 / 36 |
| GBR / DEU | 2024 | YES GDP | FE filled; master empty | = OA | static |

**H_Index:** FE unique values equal `sjr_country_metrics.csv` exactly (USA 53, CHN 39, IND 27, GBR 48, DEU 36). **Ireland 2022 H=111 > USA 53** with ~9k docs — confirms this is **not** SCImago Country Rank H-index.

**External SCImago spot-check (web search of public country rank table, area filter in results):** USA H≈**1657**, China≈**608**, Ireland≈**256** (2022-era public pages). Local/FE USA **53** → **MISMATCH to SCImago Country Rank by orders of magnitude.** (Live `scimagojr.com` fetch returned 403 from this environment; search snippet used.)

**External World Bank:** live API **timed out**. Local chain FE=raw_worldbank is consistent; Wikipedia/WB summary tables for recent GDP PPP are in the same ballpark as FE 2024 (e.g. USA ~85.8k) but **year-exact live API equality was not proven**.

**Other FE issues:** 27/6022 rows with null `Country_Name`; UMAP `x,y` are derived (no raw equivalent).

#### Status: **PARTIAL**
- MATCH: FE ↔ master ↔ raw WB for GDP/GERD (when master filled); FE docs ↔ WB_Pubs (≤2022) or OA (2023–24).
- MISMATCH: H_Index / Q% vs real SCImago Country Rank; credit overstates OpenAlex for docs in most years; 2024 GERD is imputed/forward-filled beyond master CSV (and **≠** `master_dataset_imputed.xlsx` 2024 GERD).

---

### Graph 2 — Global Quality Shift (`ridgeline_data.js` → `REAL_RIDGELINE_DATA`)

**UI credit:** “SCImago SJR · Density Estimates”

#### Frontend fields
Per year key (`"1999"`…`"2024"`): `{ country, region, q1, q4, total, ratio }`  
Years: **1999–2024** (26); ~2610 country-year rows.

#### Local candidates
- `master_dataset.csv` `Q1_Percent` / `Q4_Percent` — **year-static**, from `sjr_country_metrics.csv` (journal-share %), **not** document counts
- **No** `scimago_country_rank.csv` with Documents / Q1–Q4 document counts by year

#### Claimed external
SCImago Journal & Country Rank (Scopus), country-year publication quality

#### Join keys
Country **name** (not ISO) + year string

#### Spot-check integrity + vs master

| Check | Result |
|-------|--------|
| `q1+q4 > total` | **569 / 2610** rows |
| `q4 > total` | **479** rows |
| `ratio` capped at 5 | **223** rows (`ratio = min(5, q1/q4)`) |
| USA 2022 | q1=530553, q4=35612, total=834932, ratio=5.0; FE q1/(q1+q4)=93.7% vs master Q1%=**47.97** (static) |
| UK 2022 | q1=530160 ≈ USA; master Q1%=52.65 |
| Master Q1% varies by year? | **No** — 0 countries with >1 distinct Q1_Percent |
| Taiwan present? | **Yes** in 2022 ridgeline (prior “Taiwan filter” is not a missing-country issue in bundled data) |

Document counts in ridgeline **cannot** be derived from local `Q1_Percent` (wrong unit + static). No local raw equals FE `q1`/`q4`/`total`.

#### Status: **NEEDS_PARTNER_FILES** (also **MISMATCH** vs only local SJR percents; internal integrity failures)

---

### Graph 3 — Top Research Topics (`viz3_data.js` → `window.CSV_DATA`)

**UI credit:** “OpenAlex (1950-2025)”

#### Frontend fields
CSV columns: `year`, `topic_name`, `subfield_id`, `country_name`, `country_code` (ISO-2), `publications_count`  
48219 rows; years **1950–2025**; 7 topics.

#### Local candidates
- `raw_openalex_docs.csv` — **country-year totals only** (`Total_Docs_OA`) — **no topics / ASJC / concepts**
- No other topic panel in `CS661_Dataset`

#### Claimed external
OpenAlex concepts / subfields (proposal: Concept 1702 = AI & ML, etc.)

#### Spot-check (FE only — no local topic raw)

| Country | Year | Topic | FE pubs | subfield_id |
|---------|------|-------|---------|-------------|
| US | 2015/20/22 | AI & Machine Learning | 13186 / 27451 / 22304 | 1702 |
| CN | 2022 | AI & ML | 31602 | 1702 |
| IN | 2022 | AI & ML | 10230 | 1702 |
| Quantum Computing (all) | — | — | 4397 rows | **`2500` only** |

**ASJC 2500 = Materials Science** (Scopus), not Quantum Physics (~3100s). Label/ID mismatch confirmed in bundled data.

#### Status: **NO_LOCAL_RAW** (+ labeling **MISMATCH** for Quantum/`2500`)

---

### Graph 4 — Collaboration Premium (`viz4_data.js` → `VIZ4_DATA`)

**UI credit:** “OpenAlex Citation Networks”

#### Frontend fields
`name`, `region`, `domestic`, `international`, `gain` — **111 countries**, **no year**  
All values **0.1 precision**; `gain == international - domestic` for **111/111**.

#### Local candidate
`collaboration_premium.csv` — 20 countries × 2010–2024 with `Domestic_Avg_Citations`, `International_Avg_Citations`, `Citation_Gain`

#### Spot-check equality (FE vs premium)

| Country | FE (dom/intl/gain) | premium 2022 | premium mean | Match any? |
|---------|-------------------|--------------|--------------|------------|
| United States | 16.9 / 24.3 / 7.4 | 3.932 / 12.833 / 8.901 | 13.20 / 22.53 / 9.33 | **NO** |
| United Kingdom | 16.2 / 23.8 / 7.6 | 7.057 / 14.657 / 7.600 | 12.55 / 23.95 / 11.40 | **NO** |
| Germany | 15.3 / 22.6 / 7.3 | 5.982 / 14.143 / 8.161 | 10.79 / 23.12 / 12.34 | **NO** |
| China | 13.0 / 18.3 / 5.3 | 13.366 / 19.193 / 5.827 | 13.06 / 26.41 / 13.35 | **NO** (near 2022 but gain/intl differ) |
| India | 9.5 / 15.7 / 6.2 | 6.395 / 14.894 / 8.499 | 11.31 / 20.38 / 9.07 | **NO** |

Overlap names: 19/20 premium countries (missing FE name for “Russian Federation”). **92 FE countries** have **zero** rows in `collaboration_premium.csv`.

Closest curious near-miss: USA FE domestic 16.9 ≈ premium **2015** domestic 16.609 (rounds to 16.6, not 16.9); intl FE 24.3 ≠ 2015 intl 27.611. Not a clean single-year slice.

#### Status: **MISMATCH** (local premium present but **does not** generate FE; FE looks like a rounded/synthetic cross-section)

---

### Graph 5 — India HE Network (`dashboard/data/india_network/*.json`)

**UI credit:** “NIRF India · ROR · SCImago”

#### Frontend fields (node / edge)
Nodes: `id`, `name`, `openalex_id`, `lat`/`lon`, `tier`, `is_hub`, `total_works`, `scimago_pct`, `scimago_year`, `nirf_rank`, `nirf_ranking_category`, …  
Edges: `source`, `target`, `weight`, `citation_weight`  
Manifest: years 2015–2024; `quality_year: 2019`; funding academic years 2017-18…2022-23; patents 2020–2022; NIRF seasons 2016–2024.

#### Local candidates (NOT in `CS661_Dataset`)
- `CS661 Project/data/processed/institution_master.csv` (120)
- `collaboration_edges_full.csv` (13236 year-edges)
- `institution_funding.csv`, `institution_patents.csv`
- `data/processed/institution_quality_static.csv` (SCImago 2019)
- Checkpoints under `data/checkpoints/*/data/raw/` (NIRF rankings/funding/patents, `scimago_india.csv`, OpenAlex caches via scripts)

#### Spot-checks

| Check | Result |
|-------|--------|
| `total_works` FE full vs `institution_master` | **120/120 MATCH** |
| IISc `scimago_pct` | FE **1.63** / year **2019** = `institution_quality_static.csv` |
| IITK–IITI edge weights in processed CSV | 2015–24: 24+2+4+3+5+11+13+19+8+6 = **95** |
| `all_years_full.json` | edge weight **95** present (top-300 cumulative; min weight in top300 = 88; rank 268) |
| `2023_full` / `2024_full` year slices | IITK–IITI **absent** (2023 w=8 < top300 min 15; 2024 w=6 < min 17) — by design |
| Overview payloads | 45 hub nodes / ≤40 edges (filtered view) |

#### External NIRF / OpenAlex / SCImago SIR
Not re-fetched live in this pass (NIRF PDFs / OpenAlex API / SCImago IR). Internal pipeline docs (`docs/GRAPH5_*`) state SCImago quality is **static 2019 by design**.

#### Status: **PARTIAL**
Strongest graph for **frontend = local processed pipeline**.  
**Not** in `CS661_Dataset`. True equality to live NIRF/OpenAlex/SCImago SIR still needs partner raw + ETL confirmation (files mostly exist under `data/` + scripts, but live external re-verification not done here).

---

## 4. Cross-graph inconsistencies

1. **Docs definitions disagree:** G1 `Total_Docs` ≈ WB scientific journal articles (then OA); G2 `total`/`q1`/`q4` are incompatible SCImago-like counts; G3 OpenAlex topic counts; G5 OpenAlex institution works — **four different “publication” concepts**.
2. **SCImago used three incompatible ways:** yearless tiny `sjr_country_metrics` (G1 H / master Q%); G2 document quartiles (source missing); G5 institution % 2019 static.
3. **H-index scale broken in G1** vs public SCImago Country Rank (and vs G5 institutional percentiles).
4. **OpenAlex credit on G1** is only true for late-year docs; most years are WB_Pubs.
5. **G4** does not equal `collaboration_premium.csv` despite that file being the obvious backend.
6. **G1 2024 GERD:** FE ≠ master CSV (empty) ≠ imputed xlsx (different fill) — multiple “backends.”
7. **Master Q1/Q4 % never change with year** but G2 animates year-varying quality — narrative conflict.

---

## 5. Exact partner file request checklist (copy-paste ready)

### Graph 1 — need true SCImago + confirm WB/OA series

```
ASK G1-A — SCImago Country Rank panel (REQUIRED)
Please send the Kaggle/SCImago export your merge_scimago_kaggle.py expects:

  Filename: scimago_country_rank.csv
  (or zip of yearly CSVs from https://www.scimagojr.com/countryrank.php)

  Required columns:
    Country, Year, Documents, Citable documents, Citations,
    Self-citations, Citations per document, H index
  Optional but useful:
    Region / Area filters used (we need ALL areas / country total, not a single subject area)

  Year range: 1996–2024 (or whatever you actually merged)
  Sample row:
    United States,2022,606654,584274,...,97.21,1657

  Also confirm: did H_Index in master/viz1 accidentally come from
  sjr_country_metrics.csv (journal-level / Num_Journals=5016, H=53)
  instead of country-rank H index?

ASK G1-B — World Bank indicator codes + download date
  Confirm indicators and snapshot date for:
    NY.GDP.PCAP.PP.CD  (GDP per capita PPP)
    GB.XPD.RSDV.GD.ZS  (GERD % GDP)
    IP.JRN.ARTC.SC     (or exact code behind raw_wb_publications.csv WB_Pubs)
  Prefer: original API JSON/CSV dumps + the notebook that built raw_worldbank.csv.

ASK G1-C — OpenAlex country-year totals
  Filename: raw_openalex_docs.csv is present — please send the script that built it
  (filter: type, authorship country credit, primary location, etc.)
  so we can reproduce Total_Docs_OA for USA/CHN/IND 2015,2020,2022,2024.
```

### Graph 2 — need SCImago Q1/Q4 **document counts** by country-year

```
ASK G2 — SCImago country-year quartile DOCUMENT counts (REQUIRED)
  We cannot rebuild ridgeline_data.js from sjr_country_metrics.csv
  (that file is yearless journal-share percentages).

  Need either:
    (1) scimago_country_quartile_docs_1999_2024.csv with columns:
        Country, ISO3, Year, Docs_Q1, Docs_Q2, Docs_Q3, Docs_Q4, Docs_Total
    OR
    (2) The notebook/script + intermediate tables that produced
        dashboard/ridgeline_data.js (REAL_RIDGELINE_DATA)

  Plus answers:
    - How is ratio defined? (we see min(5, q1/q4))
    - Why do 569 rows have q1+q4 > total?
    - GDP/Taiwan filters applied in ETL or only in UI?

  Sample row:
    United States,USA,2022,530553,...,834932
```

### Graph 3 — need OpenAlex topic extract

```
ASK G3 — OpenAlex topic-country-year extract (REQUIRED)
  Filename suggestion: openalex_topic_country_year.csv
  Columns:
    year, topic_name, openalex_concept_id OR subfield_id, asjc_code (if used),
    country_name, country_iso2, publications_count
  Topics (7): AI & Machine Learning, CRISPR & Genomics, Data Science & Big Data,
    Infectious Diseases, Quantum Computing, Renewable Energy, Robotics & Automation
  Years: 1950–2025

  CRITICAL: Quantum Computing is bundled with subfield_id=2500
  (ASJC Materials Science). Please send mapping table topic_name → concept/ASJC
  and confirm correct ID for Quantum (should not be 2500).

  Also send the ETL notebook (OpenAlex API query parameters).
```

### Graph 4 — need true premium series OR FE rebuild recipe

```
ASK G4 — Collaboration premium provenance (REQUIRED)
  We have collaboration_premium.csv (20 countries, 2010–2024) but
  viz4_data.js (111 countries, no year) does NOT match mean / 2022 / latest
  for USA, UK, Germany, China, India, etc.

  Please send ONE of:
    A) The exact script that wrote viz4_data.js, OR
    B) A country-level table matching FE columns:
         name, region, domestic, international, gain
       with methodology note (which years averaged? citation window?
       domestic = no foreign coauthor? OpenAlex vs Scopus?)

  If OpenAlex: works query filters + citation count field + year bounds.
  Sample expected FE-equal row for United States if intentional:
    United States, North America, 16.9, 24.3, 7.4
  — show how that row is computed from raw works.
```

### Graph 5 — mostly local; ask for raw SIR + NIRF PDF bundle confirmation

```
ASK G5 — Confirm raw bundle locations (HELPFUL, not blocking for internal match)
  Internal FE ↔ processed CSVs already match for total_works and scimago_pct.

  Please confirm / zip:
    1) OpenAlex works cache used for edges (2015–2024) + institution list (120)
    2) NIRF ranking CSVs/PDFs 2016–2024 + funding PDFs 2017-18…2022-23
       + Innovation patent PDFs 2020–2022
    3) scimago_india.csv / SIR 2019 extract behind institution_quality_static.csv
       (columns: institution name/idp, rank, percentile, q1_pct, year=2019)
    4) Explicit rule doc for top-300 edge filter (yearly vs cumulative)
       — we verified IITK–IITI cumulative 95 in all_years_full, absent in 2023/2024 slices

  CS661_Dataset does NOT contain G5 raw; point us at the canonical folder
  if different from data/checkpoints + CS661 Project/data/processed.
```

---

## 6. Recommended fix order

1. **P0 — Replace G1 H_Index (and master Q1/Q4 %)** with true SCImago Country Rank year panel; stop using `sjr_country_metrics.csv` for country H. Fixes Ireland>USA absurdity.
2. **P0 — Graph 2:** obtain quartile document counts; rebuild `ridgeline_data.js`; fix `q1+q4>total` and document ratio cap.
3. **P0 — Graph 4:** either regenerate `VIZ4_DATA` from `collaboration_premium.csv` (pick year or mean, document it) or replace premium CSV with the true 111-country source.
4. **P1 — Graph 3:** fix Quantum `subfield_id` 2500; land topic CSV in repo next to FE.
5. **P1 — Graph 1 docs labeling:** UI credit should say World Bank scientific articles + OpenAlex (2023–24), not “OpenAlex” alone.
6. **P2 — Graph 5:** already strongest; optional live NIRF/SIR spot audit; keep static-2019 footnote.
7. **P2 — Single source-of-truth folder:** put `scimago_country_rank.csv` + topic extract + G4 recipe beside `CS661_Dataset` and version the ETL notebooks.

---

## 7. What was NOT verified externally

| Source | Attempt | Outcome |
|--------|---------|---------|
| World Bank API `NY.GDP.PCAP.PP.CD` | `urllib` fetch | **Timeout** — no live numeric proof |
| SCImago countryrank.php | WebFetch | **403 Forbidden** — used web-search snippets for H-index scale only |
| OpenAlex API topic/works | Not called (no key / not required for local gap proof) | Topic FE unverified vs live OA |
| NIRF PDF re-scrape | Not re-run | Rely on existing pipeline files + docs |
| SCImago Institutions Rankings 2019 | Not re-fetched | Matched local `institution_quality_static.csv` only |

**Do not claim MATCH to external SCImago/WB/OpenAlex/NIRF beyond what is tabulated above.**

---

## Appendix — Status one-liners

| Graph | Status |
|-------|--------|
| G1 | **PARTIAL** — FE≈master≈raw WB for GDP/GERD/docs; H_Index = yearless SJR stub ≠ SCImago Country Rank |
| G2 | **NEEDS_PARTNER_FILES** — no local SCImago quartile docs; integrity failures vs own totals |
| G3 | **NO_LOCAL_RAW** — topic series absent from `CS661_Dataset`; Quantum ASJC 2500 mislabel |
| G4 | **MISMATCH** — `collaboration_premium.csv` ≠ `VIZ4_DATA`; 92 countries unexplained |
| G5 | **PARTIAL** — FE = processed pipeline (strong); not in `CS661_Dataset`; external live not re-verified |

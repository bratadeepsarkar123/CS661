# CS661 — Raw Data Acquisition Plan

**Date:** 2026-07-12  
**Workspace:** `C:\Users\brata\Downloads\CS661`  
**Owner:** Bratadeep Sarkar (must be able to re-download and archive all public raw)  
**Inputs consulted:** `SOURCE_RECONCILIATION_REPORT.md`, `PIPELINE_FIX_PLAN.md`, `CS661_Dataset/`, `data/raw/`, `data/processed/`, `CS661 Project/data/`, recon outs under `dashboard/_recon_*`  
**URL checks (2026-07-12):** SCImago SJR help + countryrank pages live; SCImago IR India CSV download links live; NIRF Overall 2023/2024 pages live; OpenAlex works API responded; World Bank API timed out from this environment (use browser / retry — endpoints below are official).

---

# 0. Operating rule

**Acquire → archive → verify → only then pipeline fix.**

1. Build a raw vault the user owns (dated downloads + checksums).
2. Spot-check vault vs frontend bundles (`viz1_data.js`, `ridgeline_data.js`, `viz3_data.js`, `viz4_data.js`, `data/india_network/*.json`).
3. Only after vault + verify: execute `PIPELINE_FIX_PLAN.md` (crafts / regen).
4. **Do not** regenerate graphs, re-UMAP, or rewrite ETL tonight until Phase B verify passes for that graph’s required raw.

---

# 1. Target raw vault layout

Canonical root (prefer this):

```
CS661_Dataset/raw_vault/
  01_world_bank/
  02_scimago_country/
  03_scimago_journal_quartiles/
  04_openalex/
  05_nirf/
  06_unesco_uis/
  07_oecd_msti/
  08_scimago_institutions_india/
  09_asjc_reference/
  10_mirrors_kaggle/          # optional; provenance-risk
  _copied_from_existing/      # hardlinks/copies of files already on disk
  MANIFEST.md
  CHECKSUMS.sha256
```

Alternate if you prefer repo-root ETL: `data/raw_vault/` with the same subfolders. Keep **one** vault; symlink the other.

## 1.1 What belongs in each folder

| Folder | Files to place | Log fields in `MANIFEST.md` |
|--------|----------------|-----------------------------|
| `01_world_bank/` | `API_NY.GDP.PCAP.PP.CD_*.csv` (or zip), `API_GB.XPD.RSDV.GD.ZS_*.csv`, `API_IP.JRN.ARTC.SC_*.csv`; optional JSON dumps | download_date, URL, indicator, years, sha256 |
| `02_scimago_country/` | One XLS/CSV per year: `scimago_country_rank_YYYY.xls` (+ merged `scimago_country_rank_1996_2024.csv`) | year, filter (All areas), URL with `year=` / `out=xls`, sha256 |
| `03_scimago_journal_quartiles/` | Yearly journal rank exports: `scimago_journal_rank_YYYY.xls` (Best Quartile column) — **needed only if rebuilding G2 from journals** | year, subject filter, sha256 |
| `04_openalex/` | `country_year_works_counts.csv` (API-built); optional topic extract; **do not** dump full 330GB snapshot unless needed | mailto/API key note, filter params, date |
| `05_nirf/` | Ranking HTML→CSV seasons 2016–2024; funding / patents institute PDFs or scraped CSVs | season, category (Overall/University/…), sha256 |
| `06_unesco_uis/` | STI bulk from UIS BDDS (only if filling GERD gaps / sectors) | dataset name, access date |
| `07_oecd_msti/` | MSTI CSV/SDMX — **already have** `CS661_Dataset/raw_oecd_msti.csv` → copy, don’t redownload unless stale | |
| `08_scimago_institutions_india/` | SIR India Research ranking CSV (year=2019 to match FE); optional later years | year, ranking=Research, country=IND |
| `09_asjc_reference/` | Elsevier ASJC list (xlsx/CSV) for G3 label truth | source URL, date |
| `10_mirrors_kaggle/` | Only if official SJR year loop fails; label **MIRROR** | Kaggle slug, upload date vs SJR portal date |
| `_copied_from_existing/` | Pointers/copies of current `CS661_Dataset/*` and `data/raw/*` | original path |

### MANIFEST.md template (copy into vault)

```markdown
# Raw vault manifest
Vault created: YYYY-MM-DD
Owner: Bratadeep Sarkar

| Path | Source product | URL | Downloaded | Bytes | SHA256 | Notes |
|------|----------------|-----|------------|-------|--------|-------|
| 01_world_bank/... | WDI NY.GDP.PCAP.PP.CD | ... | | | | |
```

PowerShell checksum helper:

```powershell
Get-ChildItem -Recurse -File CS661_Dataset\raw_vault |
  Get-FileHash -Algorithm SHA256 |
  ForEach-Object { "$($_.Hash)  $($_.Path)" } |
  Set-Content CS661_Dataset\raw_vault\CHECKSUMS.sha256
```

---

# 2. Per-graph acquisition matrix

**Legend — Already in `CS661_Dataset`?**  
`Y` = present and usable as raw-ish; `Partial` = related file but wrong grain/unit; `N` = missing; `Elsewhere` = under `data/` not `CS661_Dataset`.

| Graph | Metric/field in FE | Authoritative source | Exact URL / portal path | Free? | Download method | Target filename | Years needed | Join key | Already in CS661_Dataset? | Priority |
|-------|--------------------|----------------------|-------------------------|-------|-----------------|-----------------|--------------|----------|---------------------------|----------|
| **G1** | `GDP_Per_Capita_PPP` | World Bank WDI **GDP per capita, PPP (current international $)** | Product page: https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.CD · API CSV: `https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.CD?downloadformat=csv` · JSON: `...?format=json&per_page=20000&date=1996:2024` | Yes (CC-BY 4.0 WB) | API / bulk zip | `API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_*.csv` | 1996–2024 | ISO3 + Year | **Y** (`raw_worldbank.csv`) — re-download for ownership/date stamp | **P0 archive** |
| **G1** | `GERD_Percent_GDP` | World Bank WDI **R&D expenditure (% of GDP)** (UIS-sourced) | https://data.worldbank.org/indicator/GB.XPD.RSDV.GD.ZS · API: `.../GB.XPD.RSDV.GD.ZS?downloadformat=csv` | Yes | API / bulk | `API_GB.XPD.RSDV.GD.ZS_*.csv` | 1996–2023 (sparse 2024) | ISO3 + Year | **Y** | **P0 archive** |
| **G1** | `Total_Docs` (≤2022 in FE) | World Bank **Scientific and technical journal articles** | https://data.worldbank.org/indicator/IP.JRN.ARTC.SC · API: `.../IP.JRN.ARTC.SC?downloadformat=csv` | Yes | API / bulk | `API_IP.JRN.ARTC.SC_*.csv` | ~1996–2022 | ISO3 + Year | **Y** (`raw_wb_publications.csv`) | **P0 archive** |
| **G1** | `Total_Docs` (2023–24 in FE) | OpenAlex country-year works counts | Docs: https://developers.openalex.org/ · Example: `https://api.openalex.org/works?filter=authorships.countries:us,publication_year:2022&per_page=1` (use `meta.count`) · Snapshot overview: https://developers.openalex.org/download/overview | Yes (CC0); polite pool / API key recommended | API group_by / CLI (not full snapshot first) | `raw_openalex_docs.csv` (rebuild) | 1996–2024 | ISO3 + Year | **Y** (present; re-verify filters) | **P1** |
| **G1** | `H_Index` | **SCImago Journal & Country Rank — Country Rankings** (country H index; cumulative) | Portal: https://www.scimagojr.com/countryrank.php · Per year: `https://www.scimagojr.com/countryrank.php?year=2022` · Download: `...?year=2022&out=xls` · Help: https://www.scimagojr.com/help.php | Free for non-commercial (cite SCImago) | **Manual browser** year loop (bot 403 common) | `scimago_country_rank_YYYY.xls` → merge `scimago_country_rank.csv` | 1996–2024 | Country name → ISO3 + Year | **N** (expected by `merge_scimago_kaggle.py`; only yearless `sjr_country_metrics.csv` exists — **wrong metric**) | **P0** |
| **G1** | `x`,`y` (UMAP) | Derived — no public raw | N/A | N/A | Regenerate after metrics fixed | — | — | — | N | Later (Phase C) |
| **G2** | `q1`,`q4`,`total`,`ratio` | **Not a public SCImago country table.** Country Rank has Documents / Citable / Citations / H — **not** Q1–Q4 document counts. Quartiles are **journal**-level (SJR help). | Journal ranks: https://www.scimagojr.com/journalrank.php · `...?year=YYYY&out=xls` | Free non-commercial | Manual XLS / or reconstruct via journal×country (hard) | Ideal: `scimago_country_quartile_docs_1999_2024.csv` (partner) **or** rebuilt from journal quartile + OA/Scopus | 1999–2024 | Country name + Year | **N** | **P0 partner / reconstruct** |
| **G2** | (alt) quality as **%** | Country journal-share Q% (if you abandon document counts) | Same countryrank / journal exports; local `sjr_country_metrics.csv` is yearless journal-share stub | Free | Manual | Do **not** treat as FE q1 counts | — | ISO3 | **Partial** (wrong unit) | Only if redesign viz |
| **G3** | `publications_count` by topic×country×year | OpenAlex **topics** / concepts (prefer Topics API), not Scopus ASJC alone | https://api.openalex.org/works?filter=topics.id:T…,authorships.countries:…,publication_year:… · Topics: https://api.openalex.org/topics | Yes CC0 | API extract (custom 7 topics) | `openalex_topic_country_year.csv` | Prefer 2000–2024 (FE has 1950–2025) | ISO2 + year + topic_id | **N** (only totals in `raw_openalex_docs.csv`) | **P0** |
| **G3** | `subfield_id` / label truth | Scopus **ASJC** list (reference only) | https://service.elsevier.com/app/answers/detail/a_id/15181/supporthub/scopus/ · SciVal xlsx mirror often: `https://supportcontent.elsevier.com/RightNow%20Next%20Gen/SciVal/ASJC1.xlsx` | Free reference | Manual download | `ASJC_codes.xlsx` | N/A | code → name | **N** | **P1** (proves Quantum≠2500) |
| **G4** | `domestic`,`international`,`gain` | OpenAlex citation networks (domestic-only vs multi-country authorship) | OpenAlex works filters + `cited_by_count`; recipe must be written | Yes | API / snapshot subset | `g4_collab_premium_country.csv` | Window e.g. 2019–2023 or single 2022 | Country name / ISO | **Partial** — `collaboration_premium.csv` (20 countries × years) **≠** FE 111-country snapshot | **P0 define + expand** |
| **G5** | `nirf_rank`, funding, patents | **NIRF — National Institutional Ranking Framework** (MoE) | Home: https://www.nirfindia.org/ · Overall 2024: https://www.nirfindia.org/Rankings/2024/OverallRanking.html · Overall 2023: `.../2023/OverallRanking.html` · Pattern: `/Rankings/{YEAR}/{Category}Ranking.html` | Free public | Manual / existing scrapers in `scripts/india_network/` | `nirf_rankings_YYYY.csv`, funding/patent scrapes | Rankings 2016–2024; funding AYs 2017-18…2022-23; patents 2020–2022 | NIRF institute ID | **Elsewhere** — `data/raw/nirf_*.csv` (**do not redownload blindly**) | **P1 archive into vault** |
| **G5** | `total_works`, edges | OpenAlex institutions + works (India HE set) | https://api.openalex.org/institutions · works by `institutions.id` | Yes | API + existing cache | caches under `data/cache/openalex/` / parquet | 2015–2024 | OpenAlex institution id | **Elsewhere** (`data/processed/*`) | Parallel OK |
| **G5** | `scimago_pct` (static 2019) | **SCImago Institutions Rankings (SIR)** — India, Research | Portal: https://www.scimagoir.com/ · India Research: https://www.scimagoir.com/rankings.php?ranking=Research&country=IND · CSV: `https://www.scimagoir.com/getdata.php?ranking=Research&area=&sector=&country=IND&year=2019&top=0&format=csv&type=download` | Free non-commercial | Browser CSV | `scimago_india_2019.csv` | Snapshot **2019** (FE design) | Institution name / Idp | **Elsewhere** (`data/raw/scimago_india.csv`) | **P1 archive** |
| **G1/G5** | GERD sectors (optional) | UNESCO UIS STI bulk | https://uis.unesco.org/bdds · Data browser: https://databrowser.uis.unesco.org/ | Free | Bulk download | UIS STI zip | as available | ISO3 + Year | **Partial** (`raw_gerd_sectors.csv`) | **P2** only if claimed |
| **G1** | OECD GERD depth | OECD MSTI | SDMX CSV: `https://sdmx.oecd.org/public/rest/data/OECD.STI.STP,DSD_MSTI@DF_MSTI,/all?format=csvfilewithlabels` · (legacy stats.oecd.org may redirect) | Free | API | keep `raw_oecd_msti.csv` | 1981–2023 | country + year | **Y** (50.6 MB) | Skip redownload |

### G2 quartile document counts — honest verdict

| Question | Answer |
|----------|--------|
| Does SCImago Country Rank export Docs_Q1…Docs_Q4 by country-year? | **No.** Public country indicators: Documents, Citable documents, Citations, Self-citations, Citations/Doc, H index. |
| Where do quartiles live? | **Journal** rankings only (Best Quartile Q1–Q4 within subject category). |
| Can OpenAlex supply SJR Q1–Q4 docs? | **Not natively.** Would need join works→venue→external SJR quartile table. |
| Best public alternative | (A) Rebuild from yearly **journalrank** XLS + OpenAlex/Scopus affiliation counts (heavy); (B) Change G2 to plot **percentages** with clear labels; (C) Partner delivers the original `Docs_Q1/Q4/Total` panel used for `ridgeline_data.js`. |
| Partner ask | Required for bit-exact FE recovery; see §7. |

---

# 3. Step-by-step collection runbook

Execute this week. Check off in order.

### Prep

1. [ ] Create vault folders:
```powershell
$root = "C:\Users\brata\Downloads\CS661\CS661_Dataset\raw_vault"
1..10 | ForEach-Object { "{0:D2}_*" -f $_ }  # visual only
@(
  "01_world_bank","02_scimago_country","03_scimago_journal_quartiles",
  "04_openalex","05_nirf","06_unesco_uis","07_oecd_msti",
  "08_scimago_institutions_india","09_asjc_reference","10_mirrors_kaggle",
  "_copied_from_existing"
) | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $root $_) }
New-Item -ItemType File -Force -Path (Join-Path $root "MANIFEST.md")
```
2. [ ] Copy existing owned files into `_copied_from_existing` (no redownload):
```powershell
$src = "C:\Users\brata\Downloads\CS661"
$dst = Join-Path $src "CS661_Dataset\raw_vault\_copied_from_existing"
Copy-Item "$src\CS661_Dataset\raw_*.csv","$src\CS661_Dataset\master_dataset.csv","$src\CS661_Dataset\collaboration_premium.csv","$src\CS661_Dataset\sjr_country_metrics.csv" $dst
Copy-Item "$src\data\raw\nirf_*.csv","$src\data\raw\scimago_india.csv" (Join-Path $src "CS661_Dataset\raw_vault\05_nirf")
Copy-Item "$src\data\raw\scimago_india.csv" (Join-Path $src "CS661_Dataset\raw_vault\08_scimago_institutions_india\scimago_india_from_pipeline.csv")
Copy-Item "$src\CS661_Dataset\raw_oecd_msti.csv" (Join-Path $src "CS661_Dataset\raw_vault\07_oecd_msti\")
```

### World Bank (tonight — API / browser)

3. [ ] Download three indicator zips (browser or PowerShell). If API hangs, use the indicator page → **Download** → CSV:
```powershell
$wb = "C:\Users\brata\Downloads\CS661\CS661_Dataset\raw_vault\01_world_bank"
$codes = @("NY.GDP.PCAP.PP.CD","GB.XPD.RSDV.GD.ZS","IP.JRN.ARTC.SC")
foreach ($c in $codes) {
  $url = "https://api.worldbank.org/v2/country/all/indicator/${c}?downloadformat=csv"
  Invoke-WebRequest -Uri $url -OutFile (Join-Path $wb "$c.zip") -TimeoutSec 120
}
```
4. [ ] Unzip; record date in `MANIFEST.md`. Spot USA 2022 GDP PPP vs FE (~77860.91).

### SCImago Country Rank (tonight — **browser required**)

5. [ ] Open https://www.scimagojr.com/countryrank.php  
6. [ ] For each year **1996–2024**: set Year → **Download data** (`out=xls`). Save as `02_scimago_country/scimago_country_rank_YYYY.xls`.  
   - **Flag:** automated fetch often returns **403**; use a normal browser session. Do not hammer.  
   - Filter: all subject areas / all regions (country total).  
7. [ ] Optional mirror only if portal fails: Kaggle “SCImago country” dumps — store under `10_mirrors_kaggle/` and note **provenance risk** (may lag official portal). R package mirror of pooled SJR: https://github.com/ikashnitsky/sjrdata (`sjr_countries`) — still cite SCImago as source.
8. [ ] Merge years → `scimago_country_rank.csv` with columns at least: `Country, Year, Documents, Citable documents, Citations, Self-citations, Citations per document, H index`.

### SCImago journal ranks (only if rebuilding G2 without partner)

9. [ ] For years overlapping ridgeline (1999–2024): https://www.scimagojr.com/journalrank.php?year=YYYY → Download → `03_scimago_journal_quartiles/`.  
10. [ ] Stop before ETL craft — archive only.

### OpenAlex (sample tonight; full topic extract this week)

11. [ ] Register polite contact: mailto query param or OpenAlex API key (https://openalex.org/).  
12. [ ] Rebuild country-year counts (sample first):
```powershell
# Example: USA 2022 meta.count
Invoke-RestMethod "https://api.openalex.org/works?filter=authorships.countries:us,publication_year:2022&per_page=1"
```
13. [ ] Script loop ISO2 × years → `04_openalex/country_year_works_counts.csv`. Compare to `raw_openalex_docs.csv`.  
14. [ ] **Do not** download full quarterly snapshot (~330GB+) in this acquisition week unless API extract fails.  
15. [ ] Topic extract for 7 dashboard topics → `04_openalex/openalex_topic_country_year.csv` + `topic_id_map.csv` (Quantum must not map to Materials/ASJC 2500).

### ASJC reference

16. [ ] Download ASJC list from Elsevier Scopus Support (answer 15181) → `09_asjc_reference/`. Confirm code **2500 = Materials Science**.

### NIRF / SIR India (archive + optional refresh)

17. [ ] Confirm `data/raw/nirf_rankings_2016.csv` … `_2024.csv` exist → already copied in step 2.  
18. [ ] Optional refresh: open each `https://www.nirfindia.org/Rankings/{YEAR}/OverallRanking.html`, save HTML + scrape to CSV with existing `scripts/india_network/01*` tools.  
19. [ ] Re-download SIR India 2019 CSV from scimagoir.com link in matrix → compare to `data/raw/scimago_india.csv` (semicolon schema: Idp;Institution;…;Percentage).

### UNESCO UIS (optional P2)

20. [ ] Only if you need sector GERD beyond `raw_gerd_sectors.csv`: https://uis.unesco.org/bdds → Science, Technology and Innovation bulk → `06_unesco_uis/`.

### Close acquisition

21. [ ] Run SHA256 → `CHECKSUMS.sha256`.  
22. [ ] Fill `MANIFEST.md`.  
23. [ ] Zip vault for personal backup: `CS661_raw_vault_YYYYMMDD.zip` (your name on the archive).  
24. [ ] Proceed to §4 verification **before** any `PIPELINE_FIX_PLAN` crafts.

---

# 4. Verification protocol (after download, before ETL)

Use countries **USA, CHN, IND, GBR, DEU** × years **2015, 2020, 2022** (add 2024 where FE has OA/GERD fill).

### Tolerance rules

| Field | MATCH if |
|-------|----------|
| GDP PPP, GERD % | Relative error ≤ **1%** (or abs ≤ 0.02 for GERD points) vs vault WB |
| WB journal articles / OA docs | ≤ **1%** or ≤ 500 abs for large countries |
| SCImago Documents / H index | Exact match to downloaded year file (H is cumulative — expect USA H ≫ 1000, **not** 53) |
| G2 q1/q4/total | Only after quartile source exists; require `q1+q4 ≤ total` and uncapped ratio documented |
| G3 topic counts | Exact on extract; label/ID must match map |
| G4 gain | `gain = international − domestic` within 0.05; FE 0.1 grid may round |
| G5 works / edges / scimago_pct | Match `data/processed` already (FE = pipeline); vault vs NIRF HTML sample 5 institutes |

### Pass/fail template (copy per graph)

```
Graph: G_
Date:
Vault files used:

| Country | Year | FE field | FE value | Vault value | Source file | Δ% | PASS/FAIL |
|---------|------|----------|----------|-------------|-------------|-----|-----------|
| USA | 2015 | ... | | | | | |
| USA | 2020 | ... | | | | | |
| USA | 2022 | ... | | | | | |
| CHN | ... | | | | | | |
| IND | ... | | | | | | |
| GBR | ... | | | | | | |
| DEU | ... | | | | | | |

Integrity checks:
- [ ] No null Country_Name on verified rows
- [ ] Docs definition labeled (WB vs OA vs SJR)
Result: PASS / FAIL — blocker notes:
```

### Known FE anchors (from recon — for orientation, not “truth”)

| Check | FE today | Expected after true SJR |
|-------|----------|-------------------------|
| USA H_Index | 53 (static) | ~1657-class on public SCImago |
| USA 2022 GDP PPP | 77860.91 | ≈ vault WB |
| USA 2022 Total_Docs | ≈ WB_Pubs 457335 | ≠ OpenAlex ~1.7M |
| G2 USA 2022 | q1=530553, total=834932, ratio capped 5 | No local vault match yet |
| G5 IISc scimago_pct | 1.63, year 2019 | = `institution_quality_static` / SIR extract |

---

# 5. What cannot be recovered from the public web

| Artifact | Why not public | Recovery path |
|----------|----------------|---------------|
| G1 UMAP/`x,y` coordinates | Offline embedding; seed/hyperparams lost | **Regenerate** after country-year master fixed (no partner required) |
| G1 H from `sjr_country_metrics` | Not SCImago country H; looks like journal-level stub (`Num_Journals`) | **Replace** with Country Rank H; discard stub for country metrics |
| G2 `ridgeline_data.js` exact q1/q4 counts | No public country×year quartile **document** table; FE has integrity bugs (`q1+q4>total`, ratio cap) | **Partner** original extract/notebook **or** redesign metric + rebuild |
| G2 ratio cap policy / Taiwan filters | Transform choices in lost ETL | Document new policy in PIPELINE_FIX; don’t recreate silent caps |
| G3 topic×country series as bundled | No local OpenAlex topic dump; Quantum=`2500` is wrong ASJC | **Re-extract** from OpenAlex with new topic map; discard bad Quantum series |
| G4 `viz4_data.js` (111 countries, 0.1 grid) | Does not equal `collaboration_premium.csv`; likely hand-tuned/unknown window | **Partner** recipe **or** regenerate from OpenAlex with written formula; optionally shrink to 20-country honest coverage |
| G5 focus-edge UX / top-300 policy | Policy, not raw | Fix in ETL (PIPELINE_FIX Stage E) — raw already local |
| Partner notebooks (`merge` paths under `C:\Users\nikhi\...`) | Machine-local | Ask partner for scripts; rewrite paths to this vault |

---

# 6. Revised sequence (acquisition-first)

Replaces “start G5 crafts / graph regen now” with:

### Phase A — Vault fill (ordered by dependency)

| Order | Work | Effort | Blocks |
|-------|------|--------|--------|
| A1 | Folder + copy existing WB/OA/OECD/NIRF/SIR | **0.5–1 h** | Nothing |
| A2 | World Bank re-download 3 indicators (ownership) | **0.5–1 h** | G1 verify |
| A3 | SCImago country rank year loop 1996–2024 | **2–4 h** (manual) | G1 H, shared with G2 docs |
| A4 | OpenAlex country-year recount + topic extract plan | **0.5 day API** / longer if topics | G1 late docs, G3 |
| A5 | ASJC + SIR 2019 confirm | **30 min** | G3 labels, G5 quality |
| A6 | Journalrank years **only if** no partner G2 file | **2–4 h** | G2 reconstruct |
| A7 | MANIFEST + checksums + zip backup | **30 min** | Phase B |

### Phase B — Verify FE vs vault

| Order | Work | Effort |
|-------|------|--------|
| B1 | G1 GDP/GERD/docs vs WB/OA; H vs new SJR | **2–3 h** |
| B2 | G5 sample NIRF HTML + SIR vs processed (sanity) | **1–2 h** |
| B3 | G2: confirm still missing quartile docs → partner or redesign gate | **1 h** |
| B4 | G3/G4: confirm no false MATCH until extracts exist | **1 h** |

### Phase C — Then execute `PIPELINE_FIX_PLAN.md`

| Order | Work | Effort (from prior plan) |
|-------|------|---------------------------|
| C1 | **G5** honesty fixes (works labels, focus edges, gates) — raw mostly ready | **3–5 days** |
| C2 | G1 H replace + optional UMAP regen | **2–3 days** after A3/B1 |
| C3 | G2 rebuild when quartile source decided | **2–4 days** |
| C4 | G3 topic regen | **1–2 days** after extract |
| C5 | G4 formula regen | **1–2 days** |

### G5 parallel rule

**G5 can proceed partly in parallel** with Phase A for G1–G4:

- NIRF CSVs, `scimago_india.csv`, OpenAlex caches, and `data/processed/*` already exist.
- Safe parallel work: PIPELINE_FIX Stages D–F (year_works, focus partners, verification gates) using **existing** `data/` raw — after copying those files into the vault (A1).
- **Do not** wait for full SCImago country panel or G2 quartile recovery to polish G5.
- **Do** wait for vault MANIFEST entry for NIRF/SIR before claiming “we own the raw archive.”

---

# 7. Copy-paste partner ping (non-public pieces only)

```
Subject: CS661 — need non-public extracts only

We’re rebuilding a raw vault from official portals (World Bank, SCImago Country Rank,
OpenAlex API, NIRF, SIR). Please send only what we cannot re-download:

1) G2 — country-year quartile DOCUMENT counts used for ridgeline_data.js
   Columns: Country, ISO3, Year, Docs_Q1, Docs_Q2, Docs_Q3, Docs_Q4, Docs_Total
   Years: 1999–2024 (or whatever fed the FE)
   Plus the notebook that set ratio = min(5, q1/q4) and any Taiwan filters.

2) G3 — OpenAlex topic×country×year extract + topic_id mapping for the 7 topics
   (Quantum must not be ASJC/subfield 2500 / Materials Science).

3) G4 — script or table that produced viz4_data.js (111 countries).
   collaboration_premium.csv (20 countries) does not match the FE snapshot.

4) Optional: original scimago_country_rank.csv / Kaggle dump you merged
   (we’re also downloading yearly XLS from scimagojr.com ourselves).

Do NOT send: World Bank CSVs, NIRF ranking pages, or SIR India 2019 if you only
have what we can pull from nirfindia.org / scimagoir.com / data.worldbank.org.

Thanks — Bratadeep
```

---

# Appendix A — Inventory: do **not** redownload as if missing

### In `CS661_Dataset/` (keep; archive into vault)

| File | Role |
|------|------|
| `raw_worldbank.csv` | G1 GDP/GERD/researchers |
| `raw_wb_publications.csv` | G1 docs ≤2022 |
| `raw_openalex_docs.csv` | G1 docs late years |
| `raw_gerd_sectors.csv` | Sector shares |
| `raw_oecd_msti.csv` | OECD MSTI (~50 MB) |
| `master_dataset.csv` / imputed xlsx | Merged country-year |
| `collaboration_premium.csv` | G4 **candidate** (≠ FE) |
| `sjr_country_metrics.csv` | Yearless; **do not trust for country H** |
| `merge_scimago_kaggle.py` | Expects missing `scimago_country_rank.csv` |
| `deep_dive_dataset_imputed.xlsx` | Deep-dive averages |

### In `data/raw/` (G5 — archive, don’t blindly scrape again)

`nirf_rankings_2016.csv` … `2024.csv`, `nirf_research_projects*.csv`, `nirf_patents*.csv`, `scimago_india.csv`, `india_higher_education.csv`

### In `data/processed/` + `CS661 Project/data/processed/`

`institution_master.csv`, `collaboration_edges_full.csv`, funding/patents (± by year), `institution_quality_static.csv`, OpenAlex parquets — **pipeline outputs**, not substitute for vault raw, but G5 FE already matches these.

### Missing / must acquire

- `scimago_country_rank.csv` (yearly panel)
- G2 quartile document panel
- G3 topic-country-year extract
- Provenance for G4 111-country FE
- Fresh dated WB zips for personal ownership (even if numbers already match)

---

# Appendix B — License / terms notes (short)

| Source | Terms note |
|--------|------------|
| World Bank Open Data | Free; cite WB; CC-BY 4.0 typical for indicators |
| UNESCO UIS | Free for non-commercial research; cite UIS |
| OECD MSTI | Free via SDMX; cite OECD |
| SCImago SJR / SIR | Free for **non-commercial** use with citation to scimagojr.com / scimagoir.com |
| OpenAlex | CC0 |
| NIRF | Public MoE rankings; cite nirfindia.org; scraping for coursework OK — prefer HTML save |
| Elsevier ASJC list | Reference download from Support Center; not a Scopus subscription dump |
| Kaggle mirrors | Third-party; verify against official SJR before viva claims |

---

# Appendix C — Top 5 downloads to do tonight (highest leverage)

1. **SCImago Country Rank** XLS for key years 2015/2020/2022/2024 (then backfill) → fixes G1 H narrative.  
2. **World Bank** zip for `NY.GDP.PCAP.PP.CD`, `GB.XPD.RSDV.GD.ZS`, `IP.JRN.ARTC.SC` → owned G1 macro/docs.  
3. **Copy** existing `data/raw/nirf_*` + `scimago_india.csv` into vault → G5 ownership without re-scrape.  
4. **OpenAlex** USA/CHN/IND/GBR/DEU meta.count spot-check vs `raw_openalex_docs.csv`.  
5. **SIR India 2019 CSV** re-pull from scimagoir.com → confirm `scimago_pct` lineage.

Then stop. Verify. Partner-ping G2/G3/G4 holes. Only then run pipeline crafts.

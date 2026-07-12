# Report Section 2 Fact-Check — Domain Research and Data Acquisition

**Date:** 2026-07-12  
**Primary LaTeX:** `CS661 Project/CS661_Project_Report_Group10_Final.tex` (Abstract, Intro objectives, §Domain Research and Data Acquisition; related merge/PPP claims in §3 flagged)  
**Evidence:** `CS661_Dataset/`, `CS661_Dataset/raw_vault/`, `dashboard/viz1_data.js`, `dashboard/SOURCE_RECONCILIATION_REPORT.md`, `dashboard/RAW_DATA_ACQUISITION_PLAN.md`, computed CSV stats (Python)

---

## 1. Executive verdict

**Can Section 2 be presented as-is? NO.**

The World Bank subsection is mostly salvageable with tighter numbers. The **UNESCO UIS BDDS** and **OECD MSTI (as used in a tripartite hierarchical merge)** subsections are **not professor-safe**: they describe a planned strategy from `RD_Spending_Data_Guide.md`, not what the shipped dashboard actually uses. Abstract / Data Synthesis claims that list World Bank + UNESCO + OECD as equal acquisition pillars overclaim.

**Bottom line:** Graph 1 macro metrics come from **World Bank WDI extracts** (GERD %, GDP PPP, scientific articles) plus **OpenAlex** for late-year document totals, bundled statically into `viz1_data.js`. OECD MSTI exists as a large orphaned file. UNESCO BDDS was not archived. Sector GERD is a thin CSV unused by the FE.

---

## 2. Answers to the five green questions

### 1. What did we **actually** take from the World Bank?

| Indicator code | Meaning | Files |
|----------------|---------|--------|
| `GB.XPD.RSDV.GD.ZS` | R&D expenditure (% of GDP) | `CS661_Dataset/raw_worldbank.csv` → `GERD_Percent_GDP`; vault zip `01_world_bank/GB.XPD.RSDV.GD.ZS.zip` + `API_GB.XPD.RSDV.GD.ZS_*.csv` |
| `NY.GDP.PCAP.PP.CD` | GDP per capita, PPP (current international $) | `raw_worldbank.csv` → `GDP_Per_Capita_PPP`; vault `NY.GDP.PCAP.PP.CD.zip` |
| `IP.JRN.ARTC.SC` | Scientific and technical journal articles | `raw_wb_publications.csv` → `WB_Pubs` → FE `Total_Docs` (through ~2022) |
| *(also in raw)* | Researchers per million (WDI series; typically `SP.POP.SCIE.RD.P6`) | `raw_worldbank.csv` → `Researchers_Per_Million` (in master; **not** a viz1 bubble field) |
| *(also in raw)* | Nominal GDP / GDP per capita | `GDP_Nominal`, `GDP_Per_Capita_Nominal`; plus derived `PPP_Conversion_Scale` |

WB metadata confirms `GB.XPD.RSDV.GD.ZS` is **republished UIS** data (UNESCO is the upstream publisher of the GERD % series via WDI—not a separate BDDS download by this team).

### 2. What from UNESCO?

- **In the final Graph 1 pipeline: nothing as a separate UIS BDDS extract.**
- Vault `06_unesco_uis/` contains only `raw_gerd_sectors.csv` (copy of `CS661_Dataset/raw_gerd_sectors.csv`). MANIFEST note: *“confirm UIS provenance later.”*
- Columns are `GERD_Sector_Gov`, `GERD_Sector_HE`, `GERD_Sector_Biz` — **not** `GERD_HERD` / `GERD_BERD` / `GERD_GOVERD`.
- Country set matches OECD MSTI `REF_AREA` list exactly (49 codes including `OECD`, `EU27_2020`) — strong sign of OECD-lineage sector scrap, **not** a UIS BDDS bulk.
- **Not used** in `viz1_data.js` / `app.js` (zero `GERD_Sector` references).
- Indirect: World Bank GERD % **is** UIS-sourced at the publisher level (honest to say “UIS via World Bank WDI”).

### 3. Geographical coverage (non-null real values)

| Metric | Source file | Countries with ≥1 non-null (excl. WB regional aggregates where noted) |
|--------|-------------|------------------------------------------------------------------------|
| GERD % GDP | Official vault API CSV | **156** countries (217 meta “countries” with Region; 195 codes incl. aggregates have some GERD) |
| GERD % GDP | `raw_worldbank.csv` / master | **156** excl. aggregates; **193** if aggregates kept |
| GDP per capita PPP | Official API / raw | **203** excl. aggregates (raw: 247 codes incl. aggregates) |
| Scientific articles | `raw_wb_publications.csv` | **197** excl. aggregates (241 codes incl. aggregates); years 1996–2022 in project extract |
| FE viz1 panel | `viz1_data.js` | **213** countries, but GERD/GDP/docs are **fully filled** (imputation/forward-fill); only **156** ever have real master GERD |

“~170 countries” is a soft marketing round-up; **defensible number for GERD is ~156 countries**, with ~100–130 reporting in a typical recent year (not all 156 every year).

### 4. Temporal depth (real values, not imputed)

| Series | Min year with data | Max year with data | Notes |
|--------|--------------------|--------------------|-------|
| GERD % (`GB.XPD…`) | **1996** | **2024** (sparse) | Dense through ~2023; **only 30** codes non-null in 2024 in official zip |
| GDP PPP | **1990** in official zip; project extract from **1996** | **2024** | FE/master window 1996–2024 |
| Articles `IP.JRN…` | **1996** | **2022** in `raw_wb_publications.csv`; official zip has values through **2023** | FE uses WB pubs ≤2022, then OpenAlex 2023–24 |
| OECD MSTI file | **1995** | **2024** | **Not** back to 1981 in this dump; **not** merged into master GERD |
| FE viz1 years | 1996 | 2024 | Includes imputed GERD for many late years |

### 5. Key indicators — claimed vs actually used in FE

| Claimed (report) | In FE Graph 1 (`viz1_data.js`)? | Actual field / source |
|------------------|----------------------------------|------------------------|
| `GB.XPD.RSDV.GD.ZS` / GERD % GDP | **Yes** | `GERD_Percent_GDP` ← WB (`raw_worldbank`) + fill for gaps |
| `GERD_HERD` / `GERD_BERD` / `GERD_GOVERD` | **No** | Absent from FE |
| OECD absolute USD / PPP GERD | **No** | `raw_oecd_msti.csv` orphaned; master GERD == WB GERD 100% where both non-null |
| GDP (wealth) | **Yes** | `GDP_Per_Capita_PPP` = WB `NY.GDP.PCAP.PP.CD` (already PPP; not a custom LCU÷PPP pipeline on absolute GERD) |
| Publication volume | **Yes** | `Total_Docs` ← WB articles then OpenAlex |
| H-index / Q1 elite | **Yes (H)** / quality narrative | `H_Index` from yearless `sjr_country_metrics.csv` — **not** verified SCImago Country Rank H (see reconciliation) |
| UMAP coords | **Yes** | Derived `x`, `y` |
| Region | **Yes** | Categorical `Region` |

---

## 3. Full claim-by-claim table

| Claim (quote or paraphrase) | Verdict | Evidence (file + numbers) | Professor-safe rewrite |
|----------------------------|---------|---------------------------|------------------------|
| Abstract: “rigorous data acquisition … from the World Bank, UNESCO, and OECD” | **PARTIAL** | WB: yes (3 indicators + pubs). UNESCO BDDS: no archive. OECD file present but unused in master/FE GERD. | “…acquisition primarily from World Bank WDI (UIS-sourced GERD and macroeconomic series), supplemented by OpenAlex and SCImago-family bibliometrics; OECD MSTI was obtained for enrichment but not required for the Graph 1 GERD panel.” |
| Intro Data Synthesis: “merge … World Bank, OECD, UNESCO” and “OpenAlex, SCImago” | **PARTIAL / overclaim on OECD+UNESCO merge** | Master GERD = `raw_worldbank` GERD exactly (3140/3140 rows, max diff 0). No hierarchical OECD>UIS>WB script in repo. | Soften to: “aggregate and clean World Bank macroeconomic series with bibliometric sources (OpenAlex, SCImago-related metrics); explore OECD/UIS sector detail as optional enrichment.” |
| “Tripartite data sourcing strategy, merging datasets from the World Bank, UNESCO, and the OECD” | **FALSE** (as executed) | No merge script implementing OECD>UIS>WB; `SOURCE_RECONCILIATION_REPORT.md`; master↔WB GERD identity. Guide only: `RD_Spending_Data_Guide.md`. | “We evaluated three complementary public sources; the deployed country-year GERD panel is the World Bank WDI series.” |
| “World Bank API served as our primary, foundational source” | **TRUE** (for G1 GERD/GDP) | `raw_worldbank.csv`; FE equality in reconciliation. | Keep; clarify **static bundle**, not live runtime API. |
| WB “aggregates data from UNESCO UIS” for `GB.XPD.RSDV.GD.ZS` | **TRUE** | Vault `Metadata_Indicator_API_GB.XPD…csv`: SOURCE_ORGANIZATION = UNESCO UIS BDDS / databrowser. | Keep. |
| Coverage “approximately 170 countries” | **PARTIAL** | Official zip excl. aggregates: **156** countries with any GERD; ~108–130 in recent years; 193 codes if aggregates counted. | “About **156** countries have at least one GERD observation (roughly 110–130 in a typical recent year).” |
| Temporal depth “1996 to 2023” | **PARTIAL** | Real GERD from **1996**; some **2024** values (30 codes); FE shows through **2024** with fill. | “Primarily **1996–2023**, with sparse official 2024 updates; the dashboard window is 1996–2024.” |
| “Easiest bulk extraction via standard REST endpoints” | **TRUE** | Vault zips from `api.worldbank.org/.../downloadformat=csv` (2026-07-12). | Keep. |
| UNESCO BDDS STI dataset utilized | **FALSE** / **UNVERIFIABLE as done** | Only `raw_gerd_sectors.csv` in `06_unesco_uis/`; no BDDS zip; MANIFEST says confirm later. | Demote to: “UIS is the upstream publisher of WDI GERD; we did not retain a separate BDDS bulk for this release.” |
| Key indicators `GERD_HERD`, `GERD_BERD`, `GERD_GOVERD` extracted | **FALSE** | Sector file columns are `GERD_Sector_*`; FE unused; names from guide table only. | Delete, or: “Sector shares exist in an exploratory CSV (`GERD_Sector_Gov/HE/Biz`) and are not plotted in Graph 1.” |
| Advantage: differentiate state- vs corporate-funded research | **FALSE** for shipped product | No FE use of sectors. | Delete from Section 2 or mark as future work. |
| OECD MSTI accessed via SDMX API | **PARTIAL** | `raw_oecd_msti.csv` is SDMX-shaped (`STRUCTURE_ID` = `OECD.STI.STP:DSD_MSTI@DF_MSTI`); 50.6 MB, 173k rows — consistent with SDMX CSV export. | “We downloaded an OECD MSTI SDMX CSV (`raw_oecd_msti.csv`).” |
| Coverage “38 OECD members + ~15 partners (including China and India)” | **PARTIAL / FALSE on India** | 38 members + 9 non-members in file: ARG, BGR, CHN, HRV, ROU, RUS, SGP, TWN, ZAF. **`IND` absent.** | “38 OECD members plus partners such as China, Russia, Singapore, South Africa, Taiwan (India not in this extract).” |
| Temporal depth “dating back to 1981” | **FALSE** (this file) | `TIME_PERIOD` min/max = **1995–2024** for the dump on disk. | “Our MSTI extract covers **1995–2024**.” |
| OECD PPP conversions “critical for our normalization pipeline” | **FALSE** for FE GDP/GERD | FE `GDP_Per_Capita_PPP` is WB PPP indicator; master has no absolute GERD PPP from OECD; GERD never overridden by OECD. §3 PPP equations overclaim relative to G1. | “Wealth axis uses World Bank GDP per capita PPP (`NY.GDP.PCAP.PP.CD`). OECD PPP GERD series were not applied in the shipped Graph 1 panel.” |
| Hierarchical merge OECD → UNESCO → World Bank | **FALSE** | master GERD where WB null = **0** rows; FE/master = WB. | Delete; replace with single-source GERD statement. |
| OpenAlex: queried for institutions, pubs, concepts / discipline chronology | **PARTIAL** | Country-year totals: `raw_openalex_docs.csv`. Topic series in G3 has **no** matching local topic dump (reconciliation). Institution network is separate India pipeline. | Soften: “OpenAlex used for country-year work counts (and India HE / topic modules as applicable); full concept dumps not all archived under `CS661_Dataset`.” |
| SCImago for Q1% as primary Elite metric | **PARTIAL / risky** | Vault now has official country XLS 1996–2024. FE G1 H-index matches yearless stub (USA H=53 ≠ SCImago ~3388). G2 Q1/Q4 counts lack local raw. | “We use SCImago-family quality narratives; country H in the current Graph 1 bundle is **not** bit-equal to SCImago Country Rank and is under repair.” |
| NIRF scraped for faculty, funding, pubs | **TRUE** (India module) | Vault `05_nirf/` rankings 2016–2024, patents, research projects; `data/raw/nirf_*.csv`. | Keep for Module 5. |
| GeoJSON India boundaries acquired | **TRUE** | `dashboard/data/india_network/india_outline.geojson` (50,831 bytes); also under `CS661 Project/data/india_network/`. | Keep. |
| Dashboard uses “live” World Bank API | **FALSE** | `data.js` comment claims live; **no** `fetch`/`api.worldbank`. Runtime loads `viz1_data.js` static. Credit: “World Bank API · OpenAlex”. | “Bundled static extracts originally obtained from the World Bank API / WDI CSV downloads.” |

---

## 4. Recommended LaTeX replacement paragraphs

Copy-paste ready (honest, still strong):

```latex
\subsection{Macroeconomic Data: Sourcing R\&D Spending}
Acquiring historically deep, internationally comparable R\&D expenditure data is difficult because national statistical offices differ in coverage and reporting lags. Our Graph~1 country--year panel is built primarily from \textbf{World Bank World Development Indicators (WDI)}, downloaded via the World Bank bulk CSV API and archived under our raw vault. The WDI R\&D series republishes UNESCO Institute for Statistics (UIS) GERD estimates, which gives us global reach without requiring a separate UIS bulk ingest for the headline GERD percentage.

\subsubsection{The World Bank (WDI)}
We treat WDI as the foundational macroeconomic source for the dashboard:
\begin{itemize}
    \item \texttt{GB.XPD.RSDV.GD.ZS} --- Research and development expenditure (\% of GDP), stored as \texttt{GERD\_Percent\_GDP}.
    \item \texttt{NY.GDP.PCAP.PP.CD} --- GDP per capita, PPP (current international \$), stored as \texttt{GDP\_Per\_Capita\_PPP}.
    \item \texttt{IP.JRN.ARTC.SC} --- Scientific and technical journal articles, used for publication volume through the early 2020s (\texttt{Total\_Docs}), with OpenAlex filling the most recent years.
\end{itemize}
After excluding regional aggregates, about \textbf{156} countries have at least one non-missing GERD observation, typically beginning in \textbf{1996}. Coverage in any single recent year is closer to 100--130 countries; official 2024 GERD updates remain sparse. The interactive frontend consumes a \textbf{static} JavaScript bundle derived from these extracts (not a live browser call to the World Bank API).

\subsubsection{OECD MSTI (archived, not Graph~1 GERD authority)}
We also obtained the OECD Main Science and Technology Indicators (MSTI) as an SDMX CSV (\texttt{raw\_oecd\_msti.csv}, $\sim$50\,MB). The extract covers 38 OECD members and several partner economies (e.g., China, Russia, South Africa; India is not present in this file) for years \textbf{1995--2024}, including BERD/HERD/GOVERD and PPP-denominated GERD measures. \emph{This file was not used to override World Bank GERD in the shipped master or Graph~1 payload}; it remains available for future sector-level or absolute-spend analyses.

\subsubsection{UNESCO UIS}
Headline GERD percentages in our panel are UIS-origin data \emph{as redistributed by the World Bank}. We did not retain a separate UNESCO UIS Bulk Data Download Service (BDDS) Science, Technology and Innovation archive for this release. An exploratory sector-share table (\texttt{raw\_gerd\_sectors.csv}) exists but is not rendered in Graph~1.
```

Optional one-liner for Abstract / objective #1:

```latex
...including data acquisition from World Bank WDI (UIS-sourced GERD and GDP PPP), OpenAlex, and SCImago-related bibliometric sources, with OECD MSTI archived for optional enrichment...
```

---

## 5. Claims to DELETE or demote

| Claim | Action |
|-------|--------|
| Tripartite **merge** World Bank + UNESCO + OECD for maximum coverage | **DELETE** as executed fact; keep only as “evaluated sources” |
| UNESCO BDDS download of STI bulk | **DELETE** or demote to “not archived / not used” |
| Extracted indicators `GERD_HERD` / `GERD_BERD` / `GERD_GOVERD` | **DELETE** |
| Sector breakdown “crucial” for differentiating state vs corporate R&D in this project | **DELETE** (not in FE) |
| OECD back to **1981** | **DELETE** (file starts 1995) |
| Partners “including … **India**” in OECD extract | **DELETE** |
| OECD PPP “critical for our normalization pipeline” (implies custom absolute GERD PPP drove G1) | **DELETE / rewrite** — FE wealth axis is WB PPP GDP/capita |
| Hierarchical fill OECD → UNESCO → WB (`country_iso3`+`year`) | **DELETE** (§3 as well) |
| “Live” World Bank API in the running dashboard | **DELETE**; say static WDI-derived bundle |
| Abstract equal billing of UNESCO & OECD acquisition | **DEMOTE** |

---

## 6. What still needs SCImago agent / partner data (brief)

**Already in vault (do not block Section 2 macro rewrite):**  
`raw_vault/02_scimago_country/` — official XLS for **1996–2024** (29/29) + merged `scimago_country_rank_1996_2024.csv` (6570 rows). SIR India 2019 also present.

**Still needed / partner-dependent for bibliometric honesty elsewhere:**
- Rebuild Graph 1 `H_Index` from vault country H (USA ~3388 cumulative vs FE 53).
- Graph 2 Q1/Q4 **document counts** are not in Country Rank XLS — need partner panel or journal-rank reconstruction (`03_scimago_journal_quartiles/` still empty).
- Graph 3 topic×country raw OpenAlex extract; ASJC reference for Quantum≠2500.
- Graph 4: FE 111-country snapshot ≠ local `collaboration_premium.csv` (20 countries).

Section 2 bibliometric paragraphs should stay **light** until those are reconciled; do not claim bit-exact SCImago Country Rank H for the current Graph 1 bundle.

---

## Extra honesty checks (summary)

| Check | Result |
|-------|--------|
| Live WB API in dashboard? | **No** — static `viz1_data.js` |
| UNESCO BDDS proof? | **No** — thin sector CSV only |
| `raw_oecd_msti.csv` in viz1 merge? | **No** — orphaned relative to master GERD |
| “1996–2023” vs vault/FE | Real GERD from 1996; some 2024; FE to 2024 with imputation |
| “~170 countries” | Prefer **156** (excl. aggregates) |
| Custom PPP on absolute GERD? | **Not in FE**; `GDP_Per_Capita_PPP` is already WB PPP |

---

## Appendix — Computed stats (Python, 2026-07-12)

```
Official API GB.XPD.RSDV.GD.ZS: years with data 1996–2024; 156 countries excl. aggregates; ~108–130 / year recently; 30 in 2024
Official API NY.GDP.PCAP.PP.CD: 203 countries excl. aggregates; strong 1996–2024 coverage
Official API IP.JRN.ARTC.SC: 197 countries excl. aggregates; 1996–2023 in zip; project raw_wb_publications max year 2022
raw_worldbank GERD: 3140 non-null rows; master GERD identical to WB (100%)
raw_oecd_msti: 173333 rows; REF_AREA n=49; TIME 1995–2024; IND not present
raw_gerd_sectors: 49 codes (same as OECD areas); not in viz1
viz1_data.js: 6022 rows, 213 countries, 1996–2024; fields Country_Code, Country_Name, Year, Region, Total_Docs, H_Index, GERD_Percent_GDP, GDP_Per_Capita_PPP, x, y
```

**Provenance note:** Report Section 2 prose closely tracks `CS661 Project/RD_Spending_Data_Guide.md` (planned merge), not the executed ETL.

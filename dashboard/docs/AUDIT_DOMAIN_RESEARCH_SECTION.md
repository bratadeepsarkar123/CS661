# AUDIT — Domain Research and Data Acquisition (before → after)

**Date:** 2026-07-12  
**Mode:** AUDIT ONLY — no LaTeX rewrite in this pass.  
**Scope:** Pasted / draft claims for “Domain Research and Data Acquisition” (macro R&D spending + bibliometrics + India).  
**Live truth sources:** `RIVER_OWNERS.md`, `RIVER_PIPELINE_REPORT.md`, `RIVER_GERD_HIERARCHY.md`, `G3_*`, `G4_*`, `REPORT_EDITING_GUIDE.md`, `READY_FOR_TEAM/`, vault pools/scripts.  
**Also compared:** `CS661 Project/CS661_Project_Report_Group10_Final.tex` (partially updated; still not fully professor-safe).  
**Note:** Older `dashboard/REPORT_SECTION2_FACTCHECK.md` is partly stale. Prefer this audit + river docs.

**Executive verdict:** Do **not** ship the pasted draft as-is. Several macro claims still track the *planned* guide (`RD_Spending_Data_Guide.md`), not the locked live rivers. Fix Before → After using the table below, then edit the `.tex` yourself.

**Companion (same content, reading layout):** [`AUDIT_DOMAIN_RESEARCH_BEFORE_AFTER.md`](AUDIT_DOMAIN_RESEARCH_BEFORE_AFTER.md)

---

## How to read this table

1. **Before** = what the draft / pasted Domain Research text says *now* (quote or close paraphrase).  
2. **Is it OK?** = Keep / Fix / Partial / False / Outdated / Missing.  
3. **What is actually true** = reality in *this* project’s rivers, vaults, and dashboard.  
4. **After** = concrete sentence(s) you can later paste into the report (guidance only — not a full section rewrite).  
5. **Why / evidence** = one short line + file path.  
6. Rows labeled **MISSING** are live facts the draft omits; “Before” is empty / silent.  
7. When one paragraph mixes true and false, it is split into separate rows.

---

## Claim-by-claim table (Before → After)

| # | Topic (short) | What the draft says NOW (Before) | Is it OK? | What is actually true in our project | What the report SHOULD say (After) | Why / evidence (1 short line + path) |
|---|---------------|----------------------------------|-----------|--------------------------------------|------------------------------------|--------------------------------------|
| 1 | Two research domains | The project covers two domains: (1) macro R&D / GDP-style indicators and (2) bibliometric data (publications, citations, subjects). | **Keep** | Correct. Modules G1–G5 sit in those two buckets. | Keep: “We study two domains — country-level R&D/economy metrics, and publication/citation/network bibliometrics.” Optionally add: one metric → one data owner (river). | Live modules + metric map — `dashboard/docs/RIVER_OWNERS.md` |
| 2 | Three sources acquired (WB, UNESCO, OECD) | Macro data came from a tripartite acquisition: World Bank + UNESCO UIS + OECD MSTI; materials were collected for all three. | **Partial** | All three *archives* exist on disk. Only World Bank is the everyday live backbone for GERD % GDP; OECD fills *some* holes under a gate; UNESCO BDDS is reference, not the live GERD dial. | “We acquired World Bank WDI, UNESCO UIS BDDS, and OECD MSTI extracts. Live Module 1 GERD uses World Bank as base, with gated OECD hole-fill; UNESCO BDDS is acquired reference, not the live GERD series.” | Vault folders exist; live rule differs — `CS661_Dataset/raw_vault/01_world_bank/`, `06_unesco_uis/`, `07_oecd_msti/`; `RIVER_GERD_HIERARCHY.md` |
| 3 | Merge order OECD > UIS > World Bank | The dashboard is fed by a hierarchical merge: OECD preferred over UNESCO UIS over World Bank. | **False** | Planned in the old guide; **not** what we run. Live rule: **World Bank first**; UIS matches WB on overlaps (adds nothing); OECD only fills true missing years if the country passes an overlap gate. | Delete OECD>UIS>WB. Write: “GERD % GDP: World Bank base → OECD fills eligible missing country–years only → otherwise leave missing in the river → display may carry last official year forward (LOCF) in the pool.” | Design ≠ live — `RD_Spending_Data_Guide.md` vs `RIVER_GERD_HIERARCHY.md`; sources in `gerd_pct_gdp_hierarchical.csv` are only `WB`/`OECD` |
| 4 | Merge rule “still pending” | Final.tex / draft: OECD is not yet substituted; merge is pending an explicit written rule. | **Outdated** | The written gated merge rule exists and is implemented. Example: USA 2024 can come from OECD; India after 2020 is missing in the river and shown via LOCF in the pool. | “A gated merge rule is locked: WB base; OECD hole-fill only for eligible countries; UIS does not extend beyond WB. Display LOCF is tagged (e.g. India 2021–2024 from WB 2020).” | Rule + build — `RIVER_GERD_HIERARCHY.md`, `_build_gerd_hierarchy.py` |
| 5 | World Bank GERD indicator | Primary GERD % of GDP comes from World Bank indicator `GB.XPD.RSDV.GD.ZS`. | **Keep** | True as the **base** series. Data is a static WDI extract in the vault/panel — not a live browser call each time the dashboard opens. Upstream, this WDI series is published via UIS. | “Primary GERD (% of GDP) is World Bank WDI `GB.XPD.RSDV.GD.ZS` (static extract). This WDI series is UIS-origin upstream; our live file still treats WB as the operational base.” | WDI CSV + panel — `01_world_bank/`; `RIVER_OWNERS.md` |
| 6 | World Bank GDP PPP + articles | World Bank also supplies GDP PPP and scientific articles used in Module 1. | **Keep** | True. Codes: `NY.GDP.PCAP.PP.CD` (wealth) and `IP.JRN.ARTC.SC` (article counts for bubble size, with SCImago Documents as fallback). Bubble size must **never** use OpenAlex country totals. | “Module 1 also uses WB `NY.GDP.PCAP.PP.CD` (GDP per capita, PPP) and `IP.JRN.ARTC.SC` (scientific articles) for bubble size, with SCImago Documents as fallback — never OpenAlex country totals.” | Owners + sample USA size — `RIVER_OWNERS.md`; panel columns |
| 7 | “~170 countries” coverage | Macro GERD coverage is about ~170 countries. | **Partial / Fix** | Official GERD API (excluding aggregates): about **156** countries with ≥1 GERD value; recent years often ~80–130; 2024 is sparse (~30). “~170” is marketing from the guide. | Prefer: “About **156** countries have at least one GERD observation; typical recent years cover roughly **80–130**; 2024 is sparse.” | Recount vs guide — vault GERD extract; `RD_Spending_Data_Guide.md` “~170” |
| 8 | Years 1996–2023 | Temporal depth is 1996–2023. | **Partial / Fix** | Official GERD years among countries run **1996–2024** (2024 sparse). Dashboard fixed-effects / display window is **1996–2024** with LOCF where needed. | “Primarily **1996–2023**, with sparse official **2024**; the dashboard window is **1996–2024** with documented last-observation carry for display.” | Hierarchy + FE window — `RIVER_GERD_HIERARCHY.md`, `G2_CARRY_AND_GERD_FFILL.md` |
| 9 | UNESCO UIS BDDS downloaded | UNESCO UIS BDDS (bulk STI / R&D archives) were acquired. | **Keep** (acquisition) | True as of 2026-07-12: BDDS zips and fetch notes are on disk. This does **not** make UIS the live G1 GERD dial. | “UNESCO UIS BDDS archives are on disk (e.g. SCN-SDG / SCN-OPRI / SCIARCHIVE zips). They are acquired reference material; live headline GERD still follows the WB-based hierarchy.” | Fetch proof — `06_unesco_uis/README_FETCH.md` + zips |
| 10 | Exact names GERD_HERD / GERD_BERD / GERD_GOVERD | Extracted sector indicators are named `GERD_HERD`, `GERD_BERD`, `GERD_GOVERD`. | **False** | Our project CSV uses `GERD_Sector_Gov`, `GERD_Sector_HE`, `GERD_Sector_Biz`. Guide brochure names ≠ our columns. UIS archive uses its own label codes. | “Sector GERD columns in our extract are `GERD_Sector_Gov` / `_HE` / `_Biz` (HERD/BERD/GOVERD-*equivalents*). Do not claim the exact tokens `GERD_HERD`/`GERD_BERD`/`GERD_GOVERD` appear in our CSV.” | Column names — `raw_gerd_sectors.csv`; guide-only names in `RD_Spending_Data_Guide.md` |
| 11 | Sector R&D used in the product | Sector breakdown (gov / higher-ed / business) is used and is crucial for differentiating state vs corporate R&D in the shipped dashboard. | **False** | Front-end and G1 pool do not plot sector GERD. Live GERD owner is the hierarchical total % GDP series. | Demote: “Sector GERD was acquired for reference / future work; the shipped Module 1 charts use total GERD % GDP only.” | No FE use — `dashboard/app.js` / G1 pool; `RIVER_OWNERS.md` |
| 12 | UIS fills holes (e.g. India after 2020) | UNESCO UIS fills GERD gaps beyond World Bank (example: India 2021+). | **False** | On overlaps, UIS ≡ World Bank (match rate 1.0). UIS adds **zero** extra country–years. India’s river GERD ends at **2020**. | “UIS does not extend GERD coverage beyond World Bank on our overlaps. India official GERD in the river ends in 2020; later years on the chart are display LOCF, not new UIS values.” | Hierarchy proof — `RIVER_GERD_HIERARCHY.md` |
| 13 | OECD as gold-standard archive | OECD MSTI is the gold-standard / high-fidelity source for rich economies. | **Partial** | Fine as an **archive / reference** description. Live use is only **gated hole-fill**, not an equal third pillar for every country and field. | “OECD MSTI is a high-quality archive used as **reference + gated hole-fill** for eligible missing WB years — not a full live primary for all Module 1 fields.” | Extract + gate — `raw_oecd_msti.csv`; `RIVER_GERD_HIERARCHY.md` |
| 14 | OECD covers India as partner | OECD coverage: 38 members + ~15 partners **including China and India**. | **Fix** (India false) | Extract has **49** area codes; partners include China, Russia, Singapore, South Africa, Taiwan, etc. **`IND` (India) is absent.** | “38 OECD members plus several partners (e.g. China, Russia, Singapore, South Africa, Taiwan). **India is not in our OECD extract.**” | `REF_AREA` in `raw_oecd_msti.csv` — no `IND` |
| 15 | OECD data back to 1981 | OECD temporal depth goes back to 1981. | **False** (our dump) | On-disk extract `TIME_PERIOD` is **1995–2024**. “1981” is brochure text from the guide, not this file. | “Our OECD MSTI extract covers **1995–2024**.” | Min/max on disk — `raw_oecd_msti.csv` |
| 16 | OECD PPP critical for our pipeline | OECD PPP conversions are critical for our normalization pipeline. | **False** (shipped G1) | Module 1 wealth axis already uses World Bank GDP per capita PPP. We do not run a custom “absolute GERD × OECD PPP” normalization in live charts. | “PPP-aware wealth uses World Bank `NY.GDP.PCAP.PP.CD`. We do not apply a separate OECD-PPP GERD normalization step in shipped Module 1.” | Encoding guide — `REPORT_EDITING_GUIDE.md`; `RIVER_OWNERS.md` |
| 17 | OECD unused for live GERD | OECD is unused / “not substituted” into live GERD. | **Outdated** | OECD **is** used under the gate (e.g. USA 2024). Some countries are ineligible for conflict stitch (e.g. AUS, CAN, CHE, GBR, ISR, RUS, TUR). | “OECD **is** used for gated hole-fill on eligible countries (example: USA 2024). It is not a full stitch on every conflict country.” | Hierarchy samples — `RIVER_GERD_HIERARCHY.md` |
| 18 | OpenAlex roles (G3/G4/G5) | OpenAlex supplies institutions, publications, concepts / topic chronology (AI–Genomics style). | **Partial → Keep if scoped** | True for Module 3 (concepts), Module 4 (collab premium), Module 5 (institution network). **False** if implied for Module 1 bubble size. | “OpenAlex powers Module 3 topic chronology, Module 4 domestic vs international citation premium, and Module 5 institution networks. It does **not** set Module 1 country bubble size.” | Owners — `RIVER_OWNERS.md`; G3/G4/G5 docs |
| 19 | Vague “AI / Genomics” mega-topics | Chronology framed as broad AI / Genomics mega-topics (old mixed set / mega-AI). | **Fix / Outdated** | Live default is an **L3** set of **exactly 7** OpenAlex **concept** IDs (Infectious; Robotics; Quantum computer `C58053490`; CRISPR; Energy storage; Photovoltaics; Supervised learning `C136389625`). Mega-AI `C154945302` forbidden as primary; ASJC 2500 forbidden. Shared honesty window ~1974; no hard “field birth” floors. | Name the **7 live concept IDs** and L3 lane. Say mega-AI / ASJC 2500 are forbidden. Mention shared ~1974 window; no hard milestone floors. (Optional: L2 demo only on port 8085.) | Live set — `G3_L3_FIX_AND_L2_DEMO.md`, `g3_level_sets.json`, `G3_FLOORS_REVISED.md` |
| 20 | SCImago Q1–Q4 for Module 2 | SCImago Journal Rank publisher-country Q1–Q4 feeds Module 2. | **Keep** | True. Counts are by **publisher country**, not author nationality. | “Module 2 uses SCImago Journal Rank aggregates for **publisher-country** Q1–Q4 document mixes (not author nationality).” | `q1_q4_country_year.csv`; `SEMANTICS_DECISION.md`; `RIVER_OWNERS.md` |
| 21 | Module 2 = “brain drain” | Module 2 framed as measuring “brain drain.” | **Risky / Fix** | G2 is a **quality-mix / venue geography** metric (document counts by publisher country), not migration or brain-drain statistics. | Soften to “publisher-country quality mix / venue geography.” Use “brain drain” only as optional narrative, never as the metric’s definition. | Semantics — `SEMANTICS_DECISION.md` |
| 22 | SCImago H-index for Module 1 | SCImago Country Rank supplies Module 1 country H-index (and Documents fallback). | **Keep** (must appear) | Live H comes from Country Rank (e.g. USA H≈3388, India≈1001). Old stub master H=53 is quarantined. | “Module 1 country H-index comes from SCImago Country Rank (`scimago_country_rank_1996_2024.csv`). An old stub (H=53) is quarantined and must not be cited.” | Panel + quarantine — `RIVER_OWNERS.md`; Country Rank CSV |
| 23 | India NIRF | India higher-ed context uses an NIRF scrape. | **Keep** | True. Vault + G5 processed CSVs; note season/carry footnotes in G5 policy. | “Module 5 India context includes NIRF ranking extracts (with season / carry footnotes as documented).” | `05_nirf/`; `RIVER_PIPELINE_REPORT.md` G5 |
| 24 | India map GeoJSON + Leaflet | India map uses GeoJSON outline + Leaflet. | **Keep** | True in READY_FOR_TEAM / dashboard `data/india_network/` and Module 5. | “India map: `india_outline.geojson` rendered with Leaflet in Module 5.” | GeoJSON path + Module 5 FE |
| 25 | Live APIs in the browser | The dashboard calls live World Bank / OpenAlex APIs at runtime. | **False** | Runtime uses **static** bundled JS pools (`viz*_data.js`) rebuilt offline from extracts. | “Data were acquired via APIs/bulk downloads; the shipped dashboard loads **static** bundled extracts, not live API calls.” | No WB fetch in FE — `dashboard/app.js` / `viz*_data.js` |
| 26 | Abstract equal-bills all three sources | Abstract / objectives give equal billing to WB + UNESCO + OECD as if all equally feed the live product. | **Partial / Overclaim** | Acquisition of three sources ≠ three equal live pillars (see rows 2–4, 12–17). | Soften abstract when you rewrite Domain Research: emphasize WB backbone + gated OECD + UNESCO as acquired reference. | Same evidence as rows 2–4 |
| **M1** | **MISSING** — SCImago H owner | *(silent / understated in pasted draft)* | **Add** | SCImago Country Rank is the **sole** owner of Module 1 country H-index; stub quarantined. | Add an explicit sentence naming Country Rank as H owner and warning against stub H=53. | `RIVER_OWNERS.md`; Country Rank CSV |
| **M2** | **MISSING** — G1 bubble size policy | *(silent / understated)* | **Add** | Size = WB articles, else SCImago Documents; **never** OpenAlex country totals. | Add: “Bubble size: WB `IP.JRN.ARTC.SC`, else SCImago Documents; never OpenAlex country totals.” | `G1_TOTAL_DOCS_POLICY` / `RIVER_OWNERS.md` |
| **M3** | **MISSING** — GERD gate + LOCF | *(draft still says pending OECD>UIS>WB)* | **Add** | Full live story: WB base; UIS identity; OECD hole-fill if eligible; display LOCF tagged (India 2021–2024 = `LOCF:WB:y2020`). | Add a short “how GERD is built” paragraph with gate + LOCF (see After in rows 3–4). | `RIVER_GERD_HIERARCHY.md`, `G2_CARRY_AND_GERD_FFILL.md` |
| **M4** | **MISSING** — five “publications” meanings | *(often conflated)* | **Add** | G1 ≠ G2 ≠ G3 ≠ G4 ≠ G5 — one English word, five rivers. | Add one honesty line: each module’s “publications” means a different owned series; do not mix them. | `RIVER_OWNERS.md` (“Publications naming”) |
| **M5** | **MISSING** — G3 seven concept IDs | *(vague AI/Genomics only)* | **Add** | Exactly 7 live L3 concept IDs; shared ~1974 window; no hard floors; mega-AI / ASJC 2500 forbidden. | List the 7 IDs / topics (row 19 After). | `G3_L3_FIX_AND_L2_DEMO.md`, `g3_level_sets.json` |
| **M6** | **MISSING** — G4 = 73 countries | *(old unverified 111 risk)* | **Add** | Live collab premium: **73** countries × **2010–2024**; domestic vs international mean cites/paper. | “Module 4: OpenAlex collaboration premium for **73** countries, **2010–2024** (not 111).” | `G4_EXPAND_STATUS.md` |
| **M7** | **MISSING** — river / pool / tap | *(often missing in pasted draft)* | **Add** | Metaphor + `READY_FOR_TEAM/` clean handoff is the project’s data story. | Keep/extend Final intro: river (authoritative CSV) → pool (FE join) → tap (chart). | `RIVER_PIPELINE_REPORT.md`; `READY_FOR_TEAM/` |
| **M8** | **MISSING** — G2 publisher-country lock | *(weak / “brain drain”)* | **Add** | Q1/Q4 from journalrank aggregate by **publisher country**, not author-country fantasy. | Explicit publisher-country sentence (row 20 After). | `SEMANTICS_DECISION.md` |
| **M9** | **MISSING** — static bundle honesty | *(implies live APIs)* | **Add** | Acquisition online; runtime = JS pools. | Explicit static-bundle sentence (row 25 After). | `viz*_data.js` rebuild path |
| **M10** | **MISSING** — sectors unused by FE | *(draft implies sectors drive product)* | **Add** | If UNESCO sectors are mentioned, say FE does not plot them. | One demotion sentence (row 11 After). | `dashboard/app.js`; `RIVER_OWNERS.md` |

---

## Keep / Fix / Add (summary)

### Keep
- Two-domain framing (macro + bibliometrics).
- World Bank as operational backbone for GERD % (base), GDP PPP, and scientific articles (size).
- Honest credit that WB GERD % is UIS-origin via WDI — without claiming BDDS is the live feed.
- OpenAlex for Modules 3, 4, and 5 when scoped that way (not Module 1 size).
- SCImago Journal Rank → publisher-country Q1/Q4 for Module 2.
- SCImago Country Rank → H-index (+ Documents fallback) for Module 1.
- NIRF + India GeoJSON + Leaflet for Module 5.
- PPP wealth via WB GDP/capita PPP (do not revive custom OECD-PPP GERD pipeline).
- River vs pool language already started in Final.tex.

### Fix
- Delete live claim of **OECD > UIS > World Bank**; replace with **gated WB → OECD hole-fill + display LOCF**.
- Replace “merge pending” with “merge rule locked and gated.”
- Replace **~170** countries with **~156** (≥1 GERD); note sparse recent/2024 coverage.
- Replace OECD **1981** with extract years **1995–2024**.
- Remove **India** from OECD partners; `IND` absent in our extract.
- Rename or demote `GERD_HERD` / `GERD_BERD` / `GERD_GOVERD` to project column names / “equivalents.”
- Demote sector GERD to acquired reference (not shipped charts).
- Do not claim UIS fills India (or any) holes beyond WB.
- Soften OECD from equal live pillar / critical PPP pipeline to archive + gated fill.
- Soften Module 2 “brain drain” to publisher-country quality mix.
- Soften abstract equal-billing of WB+UNESCO+OECD.
- Replace vague AI/Genomics mega-topics with the **7** live L3 concept IDs.
- Say runtime data are **static bundles**, not live APIs.

### Add
- SCImago Country Rank as sole Module 1 H owner (+ stub quarantine).
- G1 bubble-size policy: WB articles → SCImago Documents; never OpenAlex.
- Full GERD hierarchy + LOCF paragraph (India `LOCF:WB:y2020` example).
- Five-module “publications” naming discipline.
- G3: seven concept IDs, ~1974 window, forbidden mega-AI / ASJC 2500.
- G4: **73** countries × **2010–2024** collaboration premium.
- River / pool / tap + `READY_FOR_TEAM/` handoff.
- G2 publisher-country semantics lock (if not already clear).
- Static-bundle honesty + sector-unused note if UNESCO sectors stay in the text.

---

## Suggested subsection outline (bullets only — no full prose)

Future rewrite structure (Domain Research only):

- **Opening:** river vs pool; two domains; one metric → one owner.
- **Macro — World Bank WDI:** three indicator codes; ~156 GERD countries; 1996–2024 window; static extracts.
- **Macro — GERD hierarchy:** WB first; UIS≡WB; OECD gated hole-fill; display LOCF; what is *not* done.
- **Macro — UNESCO UIS:** BDDS on disk; sector equivalents; unused in live charts; no India hole-fill beyond WB.
- **Macro — OECD MSTI:** 1995–2024 extract; partners without India; role under overlap gate.
- **Biblio — measurement units:** five “publications” rivers named honestly.
- **Biblio — OpenAlex:** G3 (7 L3 IDs); G4 (73×2010–2024); G5 institutions; not G1 size.
- **Biblio — SCImago:** Country Rank (H, Documents); Journal Rank quartiles (publisher-country).
- **India micro:** NIRF + GeoJSON/Leaflet.
- **Out of scope / deferred:** live API in browser; sector dashboards; author-country G2 rebuild.

---

## Final.tex vs pasted draft (status snapshot)

| Topic | Pasted draft (typical) | Current Final.tex | Still need? |
|-------|------------------------|-------------------|-------------|
| River/pool intro | Often missing | Present | Keep |
| OECD>UIS>WB / pending merge | Claimed | Softened but still “pending” + guide hierarchy | **Yes — gated hierarchy + LOCF** |
| ~170 / 1981 / India in OECD | Present | Still present | **Yes — fix numbers** |
| `GERD_HERD`/`BERD`/`GOVERD` names | Present | Still present | **Yes — rename or demote** |
| OpenAlex G3/G4/G5 + no OA for G1 size | Weak / missing | Largely present | Keep; add L3 IDs + G4=73 |
| SCImago Country Rank H | Often missing | Present | Keep |
| Publisher-country G2 | Weak | Present | Keep; avoid “brain drain” as metric name |
| NIRF + Leaflet | Present | Present | Keep |

---

## Evidence index (quick)

| Doc / artifact | Use for |
|----------------|---------|
| `dashboard/docs/RIVER_OWNERS.md` | Metric owners + forbidden sources |
| `dashboard/docs/RIVER_PIPELINE_REPORT.md` | River/pool/tap; USA/India samples |
| `dashboard/docs/RIVER_GERD_HIERARCHY.md` | Gated GERD + LOCF + India/USA proof |
| `dashboard/docs/G2_CARRY_AND_GERD_FFILL.md` | Display LOCF policy |
| `dashboard/docs/G3_L3_FIX_AND_L2_DEMO.md`, `g3_level_sets.json` | Live 7 L3 concepts |
| `dashboard/docs/G3_FLOORS_REVISED.md` | Shared 1974 window; no hard floors |
| `dashboard/docs/G4_EXPAND_STATUS.md` | 73 countries |
| `dashboard/docs/REPORT_EDITING_GUIDE.md` | Report ↔ live encoding |
| `CS661_Dataset/raw_vault/READY_FOR_TEAM/*` | Clean handoff CSVs |
| `CS661_Dataset/raw_vault/06_unesco_uis/README_FETCH.md` | UIS BDDS acquisition truth |
| `CS661 Project/RD_Spending_Data_Guide.md` | **Planned** strategy — not live truth |
| `CS661 Project/CS661_Project_Report_Group10_Final.tex` | Partially updated surface |

---

**Bottom line:** Keep the two-domain story and WB backbone. Rewrite UNESCO/OECD around **acquisition vs live ownership**, replace the hierarchical-merge fairy tale with **gated GERD + LOCF**, fix coverage/year/partner numbers, and add missing SCImago H / G1 size / G3 IDs / G4=73 / publications naming. Do not treat `REPORT_SECTION2_FACTCHECK.md` as final without reconciling to the 2026-07-12 river docs above.

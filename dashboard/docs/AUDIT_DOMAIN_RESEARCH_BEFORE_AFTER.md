# Domain Research audit — Before → After (easy read)

**Date:** 2026-07-12 · **Audit only** (no LaTeX rewrite)  
**Full table version:** [`AUDIT_DOMAIN_RESEARCH_SECTION.md`](AUDIT_DOMAIN_RESEARCH_SECTION.md)

**Verdict:** Do not ship the pasted draft as-is. Use each **After** block as paste-ready guidance when you edit the `.tex`.

---

## How to read this

For every claim:

| Column | Meaning |
|--------|---------|
| **Before** | What the draft says *now* |
| **Is it OK?** | Keep / Fix / False / Outdated / Partial / Add |
| **Actually true** | What our project really does |
| **After** | What the report *should* say (guidance you can paste later) |
| **Evidence** | One short proof + file path |

Rows labeled **MISSING** = live facts the draft left out.

---

## Claims 1–26 (from the draft)

### 1 — Two research domains
| | |
|--|--|
| **Before** | Two domains: macro R&D/GDP-style data + bibliometrics (pubs / citations / subjects). |
| **Is it OK?** | **Keep** |
| **Actually true** | Correct. Modules G1–G5 sit in those two buckets. |
| **After** | Keep: “We study two domains — country-level R&D/economy metrics, and publication/citation/network bibliometrics.” Optional: one metric → one data owner (river). |
| **Evidence** | Metric map — `dashboard/docs/RIVER_OWNERS.md` |

---

### 2 — Three sources acquired (WB + UNESCO + OECD)
| | |
|--|--|
| **Before** | Tripartite acquisition: World Bank + UNESCO UIS + OECD MSTI; materials collected for all three. |
| **Is it OK?** | **Partial** |
| **Actually true** | All three *archives* exist. Only World Bank is the everyday live GERD backbone; OECD fills *some* holes under a gate; UNESCO BDDS is reference, not the live GERD dial. |
| **After** | “We acquired World Bank WDI, UNESCO UIS BDDS, and OECD MSTI extracts. Live Module 1 GERD uses World Bank as base, with gated OECD hole-fill; UNESCO BDDS is acquired reference, not the live GERD series.” |
| **Evidence** | Vault folders + live rule — `01_world_bank/`, `06_unesco_uis/`, `07_oecd_msti/`; `RIVER_GERD_HIERARCHY.md` |

---

### 3 — Merge order OECD > UIS > World Bank
| | |
|--|--|
| **Before** | Dashboard fed by hierarchical merge: OECD preferred over UNESCO UIS over World Bank. |
| **Is it OK?** | **False** |
| **Actually true** | Planned in the old guide; **not** what we run. Live: **World Bank first**; UIS matches WB (adds nothing); OECD only fills true missing years if the country passes an overlap gate. |
| **After** | Delete OECD>UIS>WB. Write: “GERD % GDP: World Bank base → OECD fills eligible missing country–years only → otherwise leave missing in the river → display may carry last official year forward (LOCF) in the pool.” |
| **Evidence** | Design ≠ live — `RD_Spending_Data_Guide.md` vs `RIVER_GERD_HIERARCHY.md` |

---

### 4 — “Merge rule still pending”
| | |
|--|--|
| **Before** | OECD not yet substituted; merge pending an explicit written rule. |
| **Is it OK?** | **Outdated** |
| **Actually true** | Gated merge rule exists and is implemented (e.g. USA 2024 from OECD; India after 2020 missing in river, LOCF in pool). |
| **After** | “A gated merge rule is locked: WB base; OECD hole-fill only for eligible countries; UIS does not extend beyond WB. Display LOCF is tagged (e.g. India 2021–2024 from WB 2020).” |
| **Evidence** | `RIVER_GERD_HIERARCHY.md`, `_build_gerd_hierarchy.py` |

---

### 5 — World Bank GERD indicator
| | |
|--|--|
| **Before** | Primary GERD % of GDP from World Bank `GB.XPD.RSDV.GD.ZS`. |
| **Is it OK?** | **Keep** |
| **Actually true** | True as the **base** series. Static WDI extract — not a live browser API each page load. Upstream, this WDI series is UIS-origin. |
| **After** | “Primary GERD (% of GDP) is World Bank WDI `GB.XPD.RSDV.GD.ZS` (static extract). This WDI series is UIS-origin upstream; our live file still treats WB as the operational base.” |
| **Evidence** | `01_world_bank/`; `RIVER_OWNERS.md` |

---

### 6 — World Bank GDP PPP + articles
| | |
|--|--|
| **Before** | World Bank also supplies GDP PPP and scientific articles used in Module 1. |
| **Is it OK?** | **Keep** |
| **Actually true** | Codes `NY.GDP.PCAP.PP.CD` (wealth) and `IP.JRN.ARTC.SC` (bubble size), with SCImago Documents fallback. Size must **never** use OpenAlex country totals. |
| **After** | “Module 1 also uses WB `NY.GDP.PCAP.PP.CD` (GDP per capita, PPP) and `IP.JRN.ARTC.SC` (scientific articles) for bubble size, with SCImago Documents as fallback — never OpenAlex country totals.” |
| **Evidence** | `RIVER_OWNERS.md` |

---

### 7 — “~170 countries”
| | |
|--|--|
| **Before** | Macro GERD coverage ≈ ~170 countries. |
| **Is it OK?** | **Partial / Fix** |
| **Actually true** | About **156** countries with ≥1 GERD; recent years often ~80–130; 2024 sparse (~30). “~170” is guide marketing. |
| **After** | “About **156** countries have at least one GERD observation; typical recent years cover roughly **80–130**; 2024 is sparse.” |
| **Evidence** | Vault GERD recount vs `RD_Spending_Data_Guide.md` |

---

### 8 — Years 1996–2023
| | |
|--|--|
| **Before** | Temporal depth is 1996–2023. |
| **Is it OK?** | **Partial / Fix** |
| **Actually true** | Official GERD years **1996–2024** (2024 sparse). Dashboard window **1996–2024** with LOCF where needed. |
| **After** | “Primarily **1996–2023**, with sparse official **2024**; the dashboard window is **1996–2024** with documented last-observation carry for display.” |
| **Evidence** | `RIVER_GERD_HIERARCHY.md`, `G2_CARRY_AND_GERD_FFILL.md` |

---

### 9 — UNESCO UIS BDDS downloaded
| | |
|--|--|
| **Before** | UNESCO UIS BDDS (STI / R&D bulk archives) were acquired. |
| **Is it OK?** | **Keep** (acquisition only) |
| **Actually true** | Zips + fetch notes on disk (2026-07-12). Does **not** make UIS the live G1 GERD dial. |
| **After** | “UNESCO UIS BDDS archives are on disk. They are acquired reference material; live headline GERD still follows the WB-based hierarchy.” |
| **Evidence** | `06_unesco_uis/README_FETCH.md` + zips |

---

### 10 — Exact names GERD_HERD / BERD / GOVERD
| | |
|--|--|
| **Before** | Extracted indicators named `GERD_HERD`, `GERD_BERD`, `GERD_GOVERD`. |
| **Is it OK?** | **False** |
| **Actually true** | Our CSV uses `GERD_Sector_Gov`, `GERD_Sector_HE`, `GERD_Sector_Biz`. Guide names ≠ our columns. |
| **After** | “Sector GERD columns are `GERD_Sector_Gov` / `_HE` / `_Biz` (HERD/BERD/GOVERD-*equivalents*). Do not claim those exact `GERD_HERD` tokens appear in our CSV.” |
| **Evidence** | `raw_gerd_sectors.csv`; guide-only names in `RD_Spending_Data_Guide.md` |

---

### 11 — Sector R&D used in the shipped product
| | |
|--|--|
| **Before** | Sector breakdown is used and crucial for state vs corporate R&D in the dashboard. |
| **Is it OK?** | **False** |
| **Actually true** | Front-end / G1 pool do not plot sector GERD. Live GERD is total % GDP from the hierarchy. |
| **After** | “Sector GERD was acquired for reference / future work; shipped Module 1 charts use total GERD % GDP only.” |
| **Evidence** | No FE use — `dashboard/app.js`; `RIVER_OWNERS.md` |

---

### 12 — UIS fills holes (e.g. India after 2020)
| | |
|--|--|
| **Before** | UNESCO UIS fills GERD gaps beyond World Bank (e.g. India 2021+). |
| **Is it OK?** | **False** |
| **Actually true** | UIS ≡ WB on overlaps (match rate 1.0). Adds **zero** extra country–years. India river GERD ends **2020**. |
| **After** | “UIS does not extend GERD beyond World Bank on our overlaps. India official GERD in the river ends in 2020; later chart years are display LOCF, not new UIS values.” |
| **Evidence** | `RIVER_GERD_HIERARCHY.md` |

---

### 13 — OECD as gold-standard archive
| | |
|--|--|
| **Before** | OECD MSTI is gold-standard / high-fidelity for rich economies. |
| **Is it OK?** | **Partial** |
| **Actually true** | Fine as archive/reference. Live use = **gated hole-fill** only — not an equal third pillar for every country. |
| **After** | “OECD MSTI is a high-quality archive used as **reference + gated hole-fill** for eligible missing WB years — not a full live primary for all Module 1 fields.” |
| **Evidence** | `raw_oecd_msti.csv`; `RIVER_GERD_HIERARCHY.md` |

---

### 14 — OECD partners include India
| | |
|--|--|
| **Before** | 38 members + ~15 partners **including China and India**. |
| **Is it OK?** | **Fix** (India false) |
| **Actually true** | ~49 area codes; partners include China, Russia, Singapore, South Africa, Taiwan, etc. **`IND` absent.** |
| **After** | “38 OECD members plus several partners (e.g. China, Russia, Singapore, South Africa, Taiwan). **India is not in our OECD extract.**” |
| **Evidence** | `REF_AREA` in `raw_oecd_msti.csv` — no `IND` |

---

### 15 — OECD back to 1981
| | |
|--|--|
| **Before** | OECD temporal depth back to 1981. |
| **Is it OK?** | **False** (our dump) |
| **Actually true** | On-disk extract is **1995–2024**. “1981” is brochure text, not this file. |
| **After** | “Our OECD MSTI extract covers **1995–2024**.” |
| **Evidence** | `TIME_PERIOD` min/max — `raw_oecd_msti.csv` |

---

### 16 — OECD PPP critical for our pipeline
| | |
|--|--|
| **Before** | OECD PPP conversions are critical for our normalization pipeline. |
| **Is it OK?** | **False** (shipped G1) |
| **Actually true** | Wealth axis already uses WB GDP per capita PPP. No custom OECD-PPP GERD step in live charts. |
| **After** | “PPP-aware wealth uses World Bank `NY.GDP.PCAP.PP.CD`. We do not apply a separate OECD-PPP GERD normalization step in shipped Module 1.” |
| **Evidence** | `REPORT_EDITING_GUIDE.md`; `RIVER_OWNERS.md` |

---

### 17 — OECD unused for live GERD
| | |
|--|--|
| **Before** | OECD unused / “not substituted” into live GERD. |
| **Is it OK?** | **Outdated** |
| **Actually true** | OECD **is** used under the gate (e.g. USA 2024). Some countries are ineligible for conflict stitch. |
| **After** | “OECD **is** used for gated hole-fill on eligible countries (example: USA 2024). It is not a full stitch on every conflict country.” |
| **Evidence** | `RIVER_GERD_HIERARCHY.md` |

---

### 18 — OpenAlex roles (G3 / G4 / G5)
| | |
|--|--|
| **Before** | OpenAlex supplies institutions, publications, concepts / AI–Genomics chronology. |
| **Is it OK?** | **Partial → Keep if scoped** |
| **Actually true** | True for Modules 3, 4, 5. **False** if implied for Module 1 bubble size. |
| **After** | “OpenAlex powers Module 3 topic chronology, Module 4 domestic vs international citation premium, and Module 5 institution networks. It does **not** set Module 1 country bubble size.” |
| **Evidence** | `RIVER_OWNERS.md`; G3/G4/G5 docs |

---

### 19 — Vague “AI / Genomics” mega-topics
| | |
|--|--|
| **Before** | Chronology framed as broad AI / Genomics mega-topics (old mixed / mega-AI set). |
| **Is it OK?** | **Fix / Outdated** |
| **Actually true** | Live default = **7** L3 OpenAlex **concept** IDs (Infectious; Robotics; Quantum computer `C58053490`; CRISPR; Energy storage; Photovoltaics; Supervised learning `C136389625`). Mega-AI `C154945302` and ASJC 2500 forbidden. Shared window ~1974; no hard field-birth floors. |
| **After** | Name the **7 live concept IDs** and L3 lane. Forbid mega-AI / ASJC 2500. Mention shared ~1974 window; no hard milestone floors. |
| **Evidence** | `G3_L3_FIX_AND_L2_DEMO.md`, `g3_level_sets.json`, `G3_FLOORS_REVISED.md` |

---

### 20 — SCImago Q1–Q4 for Module 2
| | |
|--|--|
| **Before** | SCImago Journal Rank publisher-country Q1–Q4 feeds Module 2. |
| **Is it OK?** | **Keep** |
| **Actually true** | True. Counts by **publisher country**, not author nationality. |
| **After** | “Module 2 uses SCImago Journal Rank aggregates for **publisher-country** Q1–Q4 document mixes (not author nationality).” |
| **Evidence** | `q1_q4_country_year.csv`; `SEMANTICS_DECISION.md` |

---

### 21 — Module 2 = “brain drain”
| | |
|--|--|
| **Before** | Module 2 framed as measuring “brain drain.” |
| **Is it OK?** | **Risky / Fix** |
| **Actually true** | G2 is quality-mix / venue geography (publisher-country document counts), not migration stats. |
| **After** | Soften to “publisher-country quality mix / venue geography.” Use “brain drain” only as optional narrative, never as the metric definition. |
| **Evidence** | `SEMANTICS_DECISION.md` |

---

### 22 — SCImago H-index for Module 1
| | |
|--|--|
| **Before** | SCImago Country Rank supplies Module 1 H-index (and Documents fallback). |
| **Is it OK?** | **Keep** (must appear) |
| **Actually true** | Live H from Country Rank (e.g. USA ≈3388, India ≈1001). Stub H=53 quarantined. |
| **After** | “Module 1 country H-index comes from SCImago Country Rank. An old stub (H=53) is quarantined and must not be cited.” |
| **Evidence** | `RIVER_OWNERS.md`; `scimago_country_rank_1996_2024.csv` |

---

### 23 — India NIRF
| | |
|--|--|
| **Before** | India HE context uses an NIRF scrape. |
| **Is it OK?** | **Keep** |
| **Actually true** | Vault + G5 CSVs; note season/carry footnotes. |
| **After** | “Module 5 India context includes NIRF ranking extracts (with season / carry footnotes as documented).” |
| **Evidence** | `05_nirf/`; `RIVER_PIPELINE_REPORT.md` |

---

### 24 — India map GeoJSON + Leaflet
| | |
|--|--|
| **Before** | India map uses GeoJSON outline + Leaflet. |
| **Is it OK?** | **Keep** |
| **Actually true** | True in READY_FOR_TEAM / dashboard data + Module 5. |
| **After** | “India map: `india_outline.geojson` rendered with Leaflet in Module 5.” |
| **Evidence** | GeoJSON path + Module 5 FE |

---

### 25 — Live APIs in the browser
| | |
|--|--|
| **Before** | Dashboard calls live World Bank / OpenAlex APIs at runtime. |
| **Is it OK?** | **False** |
| **Actually true** | Runtime = **static** bundled JS pools rebuilt offline. |
| **After** | “Data were acquired via APIs/bulk downloads; the shipped dashboard loads **static** bundled extracts, not live API calls.” |
| **Evidence** | `viz*_data.js`; no WB fetch in `dashboard/app.js` |

---

### 26 — Abstract equal-bills WB + UNESCO + OECD
| | |
|--|--|
| **Before** | Abstract / objectives give equal billing as if all three equally feed the live product. |
| **Is it OK?** | **Partial / Overclaim** |
| **Actually true** | Three archives acquired ≠ three equal live pillars (see claims 2–4, 12–17). |
| **After** | Soften abstract: WB backbone + gated OECD + UNESCO as acquired reference. |
| **Evidence** | Same as claims 2–4 |

---

## MISSING (draft is silent — add these)

### M1 — SCImago H owner
| | |
|--|--|
| **Before** | *(silent / understated)* |
| **Is it OK?** | **Add** |
| **Actually true** | Country Rank is the **sole** Module 1 H owner; stub quarantined. |
| **After** | Explicit sentence: Country Rank owns H; do not cite stub H=53. |
| **Evidence** | `RIVER_OWNERS.md` |

---

### M2 — G1 bubble size policy
| | |
|--|--|
| **Before** | *(silent / understated)* |
| **Is it OK?** | **Add** |
| **Actually true** | Size = WB articles, else SCImago Documents; **never** OpenAlex country totals. |
| **After** | “Bubble size: WB `IP.JRN.ARTC.SC`, else SCImago Documents; never OpenAlex country totals.” |
| **Evidence** | `RIVER_OWNERS.md` / G1 size policy |

---

### M3 — GERD gate + LOCF
| | |
|--|--|
| **Before** | *(draft still says pending OECD>UIS>WB)* |
| **Is it OK?** | **Add** |
| **Actually true** | WB base; UIS identity; OECD hole-fill if eligible; display LOCF tagged (India 2021–2024 = `LOCF:WB:y2020`). |
| **After** | Short “how GERD is built” paragraph (see After in claims 3–4). |
| **Evidence** | `RIVER_GERD_HIERARCHY.md`, `G2_CARRY_AND_GERD_FFILL.md` |

---

### M4 — Five “publications” meanings
| | |
|--|--|
| **Before** | *(often conflated)* |
| **Is it OK?** | **Add** |
| **Actually true** | G1 ≠ G2 ≠ G3 ≠ G4 ≠ G5 — one English word, five rivers. |
| **After** | One honesty line: each module’s “publications” means a different owned series. |
| **Evidence** | `RIVER_OWNERS.md` (“Publications naming”) |

---

### M5 — G3 seven concept IDs
| | |
|--|--|
| **Before** | *(vague AI/Genomics only)* |
| **Is it OK?** | **Add** |
| **Actually true** | Exactly 7 live L3 concept IDs; ~1974 window; no hard floors; mega-AI / ASJC 2500 forbidden. |
| **After** | List the 7 IDs / topics (see claim 19 After). |
| **Evidence** | `G3_L3_FIX_AND_L2_DEMO.md`, `g3_level_sets.json` |

---

### M6 — G4 = 73 countries
| | |
|--|--|
| **Before** | *(old unverified 111 risk)* |
| **Is it OK?** | **Add** |
| **Actually true** | Live collab premium: **73** countries × **2010–2024**. |
| **After** | “Module 4: OpenAlex collaboration premium for **73** countries, **2010–2024** (not 111).” |
| **Evidence** | `G4_EXPAND_STATUS.md` |

---

### M7 — River / pool / tap
| | |
|--|--|
| **Before** | *(often missing in pasted draft)* |
| **Is it OK?** | **Add** |
| **Actually true** | Metaphor + `READY_FOR_TEAM/` clean handoff is the data story. |
| **After** | River (authoritative CSV) → pool (FE join) → tap (chart). |
| **Evidence** | `RIVER_PIPELINE_REPORT.md`; `READY_FOR_TEAM/` |

---

### M8 — G2 publisher-country lock
| | |
|--|--|
| **Before** | *(weak / “brain drain”)* |
| **Is it OK?** | **Add** |
| **Actually true** | Q1/Q4 by **publisher country**, not author-country fantasy. |
| **After** | Explicit publisher-country sentence (claim 20 After). |
| **Evidence** | `SEMANTICS_DECISION.md` |

---

### M9 — Static bundle honesty
| | |
|--|--|
| **Before** | *(implies live APIs)* |
| **Is it OK?** | **Add** |
| **Actually true** | Acquisition online; runtime = JS pools. |
| **After** | Explicit static-bundle sentence (claim 25 After). |
| **Evidence** | `viz*_data.js` |

---

### M10 — Sectors unused by FE
| | |
|--|--|
| **Before** | *(draft implies sectors drive product)* |
| **Is it OK?** | **Add** |
| **Actually true** | If UNESCO sectors are mentioned, FE does not plot them. |
| **After** | One demotion sentence (claim 11 After). |
| **Evidence** | `dashboard/app.js`; `RIVER_OWNERS.md` |

---

## Keep / Fix / Add (summary)

### Keep
- Two-domain framing (macro + bibliometrics).
- World Bank backbone: GERD % (base), GDP PPP, scientific articles (size).
- WB GERD is UIS-origin via WDI — without claiming BDDS is the live feed.
- OpenAlex for Modules 3, 4, 5 (not Module 1 size).
- SCImago Journal Rank → publisher-country Q1/Q4 (Module 2).
- SCImago Country Rank → H (+ Documents fallback) (Module 1).
- NIRF + India GeoJSON + Leaflet (Module 5).
- PPP wealth via WB GDP/capita PPP.
- River vs pool language already in Final.tex.

### Fix
- Delete **OECD > UIS > WB**; use **gated WB → OECD hole-fill + display LOCF**.
- Replace “merge pending” with “merge rule locked and gated.”
- **~170** → **~156** (≥1 GERD); note sparse recent/2024.
- OECD **1981** → extract **1995–2024**.
- Remove **India** from OECD partners.
- Rename/demote `GERD_HERD` / `BERD` / `GOVERD`.
- Demote sector GERD to reference (not shipped charts).
- Do not claim UIS fills India (or any) holes beyond WB.
- Soften OECD equal-pillar / critical-PPP claims.
- Soften Module 2 “brain drain.”
- Soften abstract equal-billing.
- Replace vague AI/Genomics with **7** live L3 concept IDs.
- Runtime = **static bundles**, not live APIs.

### Add
- SCImago Country Rank as sole Module 1 H owner (+ stub quarantine).
- G1 bubble-size policy (WB → SCImago Documents; never OpenAlex).
- Full GERD hierarchy + LOCF (India `LOCF:WB:y2020` example).
- Five-module “publications” naming discipline.
- G3: seven concept IDs, ~1974 window, forbidden mega-AI / ASJC 2500.
- G4: **73** countries × **2010–2024**.
- River / pool / tap + `READY_FOR_TEAM/`.
- G2 publisher-country lock (if unclear).
- Static-bundle honesty + sector-unused note if sectors stay in the text.

---

**Bottom line:** Keep two domains + WB backbone. Rewrite UNESCO/OECD as acquisition vs live ownership. Replace the merge fairy tale with gated GERD + LOCF. Fix numbers (156 / 1995–2024 / no India in OECD). Add SCImago H, G1 size policy, G3 IDs, G4=73, and publications naming before editing the report.

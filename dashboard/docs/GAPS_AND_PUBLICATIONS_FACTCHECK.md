# Gaps & publications — user-facing fact-check

**Date:** 2026-07-12  
**Scope:** Live dashboard under `dashboard/` (+ `READY_FOR_TEAM/` river).  
**Rule:** Only claims backed by code, pool files, or locked docs. Stale notes called out when they disagree with the live tap.

---

## 1. India GERD — which graph / what’s missing / what we do

### Which graph(s) and which UI part show GERD?

| Place | What the user sees | Role of GERD |
|-------|--------------------|--------------|
| **Graph 1 — Peer clusters** | UMAP bubbles; sidebar “Visual encodings”; hover / pinned detail | GERD is one of the **four UMAP inputs** (wealth · R&D · volume · quality). It is **not** a separate axis or bar. Tooltip: **R&D Spend (GERD)** with optional source tag `(WB)` / `(OECD)`, or **—** when null. |
| **Graph 2 — Quality mix** | Sidebar country card (and hover metrics) | Same GERD river as G1, joined **exact year** from `VIZ1_DATA`. Label: **R&D Spend (GERD)**. Bars themselves are **Q1/Q4 publisher docs**, not GERD. |
| **Graphs 3–5** | Topics / collab premium / India network | **No** country GERD (or H/GDP) labels. |

Credit line (G1): World Bank (GDP, GERD, journal articles) · SCImago Country Rank (H-index; Documents fallback) · UMAP.

Evidence: `graphs/g1/g1.js` encodings + tooltip; `graphs/g2/g2.js` `getCountryMetrics`; `docs/RIVER_OWNERS.md`; `docs/RIVER_GERD_HIERARCHY.md`.

### What is missing for India?

| Year | Live pool GERD | Source |
|------|----------------|--------|
| 2015–2020 | Real values (e.g. 2020 ≈ **0.64558%**) | World Bank (`GERD_Source: WB`) |
| **2021–2024** | **`null` → UI shows “—”** | No WB, no UIS beyond WB, **no OECD India rows** |

Proof: `docs/_river_to_pool_rebuild_proof.json` → `India_GERD_2015_2024`; live `viz1_data.js` India rows.

### What we are doing now (honest)

1. **Honest null** for India 2021–2024 (and any other true hole). No everlasting forward-fill of the last WB value.
2. **Gated hierarchy river** (`gerd_pct_gdp_hierarchical.csv`):
   - Prefer **WB** when present.
   - UNESCO UIS ≡ WB on overlaps and adds **zero** extra country–years → **cannot** fill India 2021+.
   - **OECD** may fill a *true* WB hole only if that country has **100%** WB∩OECD overlap within **0.05 pp** (USA 2024 is an example of eligible OECD fill). Conflict countries never get Frankenstein OECD stitches.
3. **G2** joins GERD **exact year only** — no prior-year GERD carry (so India 2022 sidebar GERD is “—”, not 2020’s 0.65%).
4. **Options considered / documented** (river-pipeline explorer + GERD docs):
   - Leave missing (**chosen**).
   - Optional later: DST / national series, or annotate “last known 2020”.
   - **Not chosen:** everlasting ffill of 0.64558% into 2021–2024 (old pool bandage).

---

## 2. Publications — why G1–G4 are different rivers

Casual English says “publications.” The dashboard measures **four different scientific objects**. Merging them into one column would mix incompatible units and invent cliffs.

| Graph | Honest name | What it counts | Why it exists |
|-------|-------------|----------------|---------------|
| **G1** | Country journal articles · documents | **World Bank** scientific & technical journal articles (`IP.JRN.ARTC.SC`), else **SCImago Country Rank Documents**. Author/country research **output volume**. | Peer layout needs one volume feature on a journal/document scale. |
| **G2** | Publisher-country journal documents (Q1/Q4) | Docs in journals whose **publisher** sits in that country (bookstore geography), split by quartile. | Prestige geography of the **publishing industry**, not where authors live. |
| **G3** | OpenAlex concept / topic works | Works tagged with locked OpenAlex concepts (e.g. ML `C119857082`, Infectious `C524204448`). | **Discipline race** — topic volume over time. |
| **G4** | OpenAlex domestic vs international paper sets | Mean **cites/paper** on domestic-only vs international coauthorship sets (plus paper counts in the premium split). | **Collaboration premium**, not a single “pubs” KPI. |

**G5** (for completeness): OpenAlex **institution** works stock on the India network — yet another unit; not comparable to G1 country totals.

### Why one “publications” column would be scientifically wrong

- **Scales differ by ~2–4×** for the same country–year (WB articles ≪ SCImago Documents ≪ OpenAlex works). Mixing WB→OpenAlex once caused a **fake ~3× cliff** for G1 size (`G1_TOTAL_DOCS_POLICY.md`).
- **Geography differs:** author country (G1) ≠ publisher country (G2) ≠ topic tagging (G3) ≠ collab filter (G4).
- **Question differs:** volume peers (G1) vs quality mix of publishers (G2) vs discipline race (G3) vs citation premium of collaboration (G4).

**Separate rivers + honest labels are legitimate.** Same English word must not force the same number.

Evidence: `docs/RIVER_OWNERS.md` “Publications naming”; `docs/RIVER_PIPELINE_REPORT.md` §Publications; `G1_TOTAL_DOCS_POLICY.md`.

---

## 3. Gap-filling fact check — G1 Tuvalu-style holes + all graphs

### 3.1 G1 — Tuvalu / microstate year holes (exact policy)

**What the user saw historically:** a year with WB articles = **0** (or empty) between years that had positive counts — classic example memory: “no 2005, had 2004 and 2006.”

**What the river shows today (Tuvalu / `TUV` in `g1_features_panel.csv`):**

| Year | WB_Pubs | SCImago_Documents | Panel `Total_Docs` | Notes |
|------|---------|-------------------|--------------------|-------|
| 2004 | 0.61 | 2.0 | 0.61 | WB present |
| **2005** | **0.0** | **1.0** | **1.0** | WB zero → treated as missing; **SCImago fills** |
| 2006 | 1.27 | 3.0 | 1.27 | WB present |
| **2011** | **0.0** | *(empty)* | *(empty)* | **True hole** — no positive WB and no SCImago; also no H in panel → **dropped from UMAP pool** |
| 2010 / 2012 | 0 / 0.04 | 1.0 / 1.0 | 1.0 / 0.04 | Adjacent years exist in pool |

So: **2005 is no longer a ghost gap** after zero-as-NA + SCImago coalesce. The remaining Tuvalu **interior hole in the live pool** is **2011** (and 2024 exists in panel via SCImago-only but may be filtered if UMAP features incomplete).

**Exact policies (code):**

| Layer | Policy | File |
|-------|--------|------|
| **Docs coalesce** | Prefer positive `Total_Docs` / `WB_Pubs`; else positive `SCImago_Documents`. **`≤ 0` treated as NA** so WB=0 does not block SCImago. **Never OpenAlex** for size. | `_regen_viz1_umap.py` `coalesce_docs` |
| **UMAP readiness** | Rows need GDP, GERD (for embedding — see caveat below), docs > 0, H. Incomplete rows **dropped** from regenerated coords (not invent GDP/H). | `_regen_viz1_umap.py` |
| **Display GERD** | Hierarchical river; true missing → **`null`**. **No everlasting GERD ffill** in pool rebuild. | `_river_to_pool_rebuild.py` `verify_g1` |
| **JS true-gap carry** | If a roster country has **no pool row** for year *Y*, tap may **carry last prior (x,y), H, GDP**; **`Total_Docs` forced to 0**; **GERD forced null**; marker drawn as **faint pin** (size ≈ 4, lower opacity), not real volume. | `graphs/g1/g1.js` `resolveViz1NodeForYear` |

**Interior year holes still in live `viz1_data.js` (examples):** Kiribati (8), Nauru (5), Aruba (3), Dominica/Somalia/São Tomé (2), Tuvalu **2011**, etc. Same class of sparse microstate / incomplete feature years.

**Known source-change cliff (not a hole fill):** USA (and many others) **2024** `Total_Docs` switches to **SCImago Documents** when WB WDI has no 2024 articles yet → can **step up** once vs 2023 WB. Documented as honest caveat, not OpenAlex inflation.

**Caveat (honest):** `_regen_viz1_umap.py` still **imputes GERD for UMAP embedding** (country ffill/bfill → region-year median → year median) so sparse countries can get coordinates. The **displayed** GERD in the pool after hierarchy rebuild is **not** that everlasting fill (India 2021+ cleared; proof `gerd_cleared: 3153`). Positions may still reflect imputed GERD at regen time — layout helper, not a claimed GERD observation.

### 3.2 Every analogous gap situation (G1–G5)

| # | Graph | Metric | What the gap looks like | What we do | Legit or risk? |
|---|-------|--------|-------------------------|------------|----------------|
| 1 | **G1** | `Total_Docs` (bubble size) | WB missing or **0** for a year; SCImago may still have docs | Zero-as-NA; coalesce **WB → SCImago**; never OA | **Legit** if labeled; risk if user thinks all years are WB |
| 2 | **G1** | `Total_Docs` | Both WB and SCImago empty (e.g. Tuvalu 2011) | No invented count; row often absent from pool; JS may show faint carried pin with docs=0 | **Legit** identity pin; risk if pin misread as “publishing” |
| 3 | **G1** | GERD % | WB ends / hole (India 2021–2024) | Honest **null** / “—”; OECD only if overlap-eligible; UIS cannot extend India | **Legit** |
| 4 | **G1** | GERD (UMAP only) | Sparse GERD for embedding | Temporary ffill/bfill/medians **inside UMAP regen only** | **Risk** if mistaken for published GERD — display path is separate |
| 5 | **G1** | Position (x,y) | Missing year mid-timeline | Carry prior UMAP coords; do **not** carry GERD or invent pubs | **Legit** for animation continuity; disclose as `_positionCarried` |
| 6 | **G1** | H-index | Flat stock across years in Country Rank extract | Same H carried in panel years where present | **Legit** as stock; not a yearly flow |
| 7 | **G2** | Q1/Q4 / total bars | Country–year absent from journalrank aggregate | No bar / zero from river — **no interpolation** | **Legit** |
| 8 | **G2** | Sidebar H / GDP | Exact VIZ1 year missing | **Nearest prior** VIZ1 row (LOCF-style); no invented growth | **Partial carry** — disclose; better than fake ×1.025 growth (removed) |
| 9 | **G2** | Sidebar GERD | Exact year missing (India 2021+) | **Exact year only** → “—” | **Legit** (stricter than H/GDP) |
| 10 | **G2** | Sidebar join | Country not in G1 (Cuba, Monaco, New Caledonia, Taiwan, Vatican) | Fail closed “—” | **Legit** |
| 11 | **G3** | Topic works | Pre-2000 incomplete / mega-AI retrospective tagging | Pool **honesty window** (shared complete primary years; AI pinned to ML `C119857082`); river may still hold more | **Legit** trim; do not invent early peers |
| 12 | **G3** | Infectious 2019→2020 | Huge real OpenAlex spike (e.g. India ~40×) | **Leave honest** — do **not** dampen or smooth | **Legit** as corpus fact; cross-topic absolute bars still imperfect (ontology levels) |
| 13 | **G3** | COVID UI note | User-facing annotation of spike | `TEAM_HANDOFF_README.md` still describes a COVID note; **modular `g3.js` / `index.html` currently have no `#covidInfectiousNote`** (stripped in modularization) | **Doc lag** — spike policy remains “don’t dampen”; UI note may need re-add |
| 14 | **G4** | Cites/paper premium | Only **20 countries × 2010–2024** in pool | No fill to 111 undated countries; stub `data.js` emptied | **Legit** sparse sample |
| 15 | **G4** | Year gaps inside sample | Missing country–year in CSV | No interpolation in rebuild — year absent from dumbbell | **Legit** |
| 16 | **G5** | Collab edges (year slice) | Weak pairs below **top-300** weight floor | Dropped from overview/year full JSON (e.g. IITK–IITI 2023 w=8 &lt; floor) | **By design clutter control**; risk if mistaken for “no collaboration” — focus/partner lists should use untruncated ≥2 when available |
| 17 | **G5** | Partner list empty | No edges with weight ≥ 2 | Explicit note | **Legit** |
| 18 | **G5** | NIRF funding / patents / rank | Metric years ≠ collaboration slider | **Mapped carry** to nearest available NIRF season/year + **footnotes** (“Funding data from another year…”) | **Legit carry with disclosure**; inventing would be wrong |
| 19 | **G5** | SCImago institute % | Only **2019** snapshot | Static across slider; note year | **Legit** static footnote |
| 20 | **G5** | Missing NIRF submission | No PDF / not ranked | “Unavailable” / — — **never fabricate** | **Legit** |

### 3.3 Short verdict on “do we still fill gaps?”

- **Still yes (with intent):** G1 docs coalesce (WB→SCImago; zero-as-NA); G1 JS position carry for missing years; G2 H/GDP prior-year join; G5 NIRF/SCImago **mapped** metrics with footnotes; G1 UMAP GERD impute for coordinates only.
- **Stopped / forbidden:** everlasting India GERD ffill; G2 invented H/GDP/GERD; OpenAlex for G1 bubble size; dampening G3 COVID Infectious spike; fabricating NIRF years.

---

## 4. One-line notes (report lag + H-index)

**Report lag:** Course-report wording (OECD / UNESCO / PPP / forward-fill story) is behind the live gated GERD hierarchy and pool proofs — update the LaTeX later from this doc and `RIVER_GERD_HIERARCHY.md`, not from older “WB + soft ffill” paragraphs.

**H-index for G1:** Confirmed — Graph 1 country H-index is the **SCImago Country Rank** river (e.g. USA 2022 **3388**, India **1001**), not the quarantined stub scale (~53 / ~27).

---

## Evidence index (primary)

| Topic | Paths |
|-------|--------|
| GERD hierarchy + India proof | `docs/RIVER_GERD_HIERARCHY.md`, `READY_FOR_TEAM/gerd_pct_gdp_hierarchical.csv`, `docs/_river_to_pool_rebuild_proof.json` |
| Owners / publication names | `docs/RIVER_OWNERS.md` |
| G1 docs / zero-as-NA | `dashboard/_regen_viz1_umap.py`, `G1_TOTAL_DOCS_POLICY.md` |
| G1 JS carry | `dashboard/graphs/g1/g1.js` (`resolveViz1NodeForYear`) |
| G2 join rules | `dashboard/graphs/g2/g2.js` (`getCountryMetrics`) |
| G3 honesty / COVID policy | `docs/GRAPH3_DATA_ROOT_CAUSE.md`, `TEAM_HANDOFF_README.md` (note: COVID UI strip may be absent in modular tap) |
| G5 mapping / footnotes | `docs/GRAPH5_DATA_PRESENTATION_POLICY.md`, `dashboard/india_network.js` |
| Explainer narrative | `docs/EXPLAINER_FINDINGS_AND_CHANGES.md` |

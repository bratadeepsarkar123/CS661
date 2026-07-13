# Explainer: What we found, what we changed

**Date:** 2026-07-12  
**Audience:** Anyone who wants the story in plain language (not the graded LaTeX course report).

---

## 1. What this doc is

This is a **plain-language explainer** of our investigation and fixes during the CS661 dashboard work.

It is **not** the course project report. That report lives here:

- `CS661 Project/CS661_Project_Report_Group10_Final.tex`

Think of this file as the “what happened in the chat / engineering pass” story. The `.tex` file is the formal write-up for the course. They overlap on facts, but this doc is meant to be readable and chronological.

### The river → pool → tap metaphor (used throughout)

| Layer | Meaning | Typical place |
|-------|---------|----------------|
| **River** | Raw / background data (CSVs, vault downloads) | `CS661_Dataset/`, `raw_vault/`, `READY_FOR_TEAM/` |
| **Pool** | Bundled files the charts drink in the browser | `dashboard/*_data.js`, `dashboard/data/india_network/` |
| **Tap** | UI labels, filters, charts, landing page | `app.js`, `graphs/g*/`, `style.css`, `index.html` |

**Rule we learned the hard way:** fix the **river owner** first, then rebuild the **pool**, then fix the **tap**. Joining two pools so they “agree” without locking the river just hides the lie.

---

## 2. Timeline of what happened (high level)

Rough chronological story of this work stream:

1. **Friend landing copy** — Landing-page wording / shell edits landed on the dashboard (hero text, gallery framing).
2. **Graphs broke** — Shared shell / script / CSS changes (or tangled edits across graphs) made visualizations unreliable.
3. **Revert** — Roll back the breakage so charts worked again; keep the project usable.
4. **Modular graphs** — Split each viz into `dashboard/graphs/g1` … `g5` (`gN.js` + `gN.css`) so editing one graph does not require rewriting the others. Shared chrome stays in `app.js` / `style.css`. See `dashboard/GRAPHS_LAYOUT.md`.
5. **River audit** — Ask the background-data question first: is the *river* clean, or only the *pool*? Documented in `dashboard/docs/RIVER_PIPELINE_REPORT.md`. Verdict: **partially polluted**.
6. **River / pool fix** — Quarantine stub H, lock owners per metric, stop Graph 2 inventing H/GDP/GERD, rebuild pools from `READY_FOR_TEAM/`. Documented in `RIVER_OWNERS.md` + `RIVER_TO_POOL_FIX.md`.
7. **G2 join all countries** — Graph 2 sidebar joins the same H/GDP/GERD as Graph 1 via `VIZ1_DATA` (ISO3 pins + aliases). Coverage **119/129 → 124/129 (96.1%)**. Five countries still unmatched (fail closed with “—”).
8. **Landing fonts / full-bleed** — Landing CSS only: Outfit + Plus Jakarta Sans, full-bleed shell (no max-width gutter). Cache-bust like `style.css?v=20260712-landing-fullbleed`. Chart modules left alone.
9. **Report `.tex` honesty pass** — Update `CS661_Project_Report_Group10_Final.tex` so Domain Research / Architecture claims match the live app (WB primary, publisher-country Q1/Q4, modular vanilla JS, etc.). Abstract / some contribution bullets still mention React (stale).
10. **GERD hierarchy work** — Build a gated OECD → UNESCO → WB river with an overlap consistency gate; stop everlasting forward-fill for India after last real WB year. **River + pool rebuild with proof exists** (`RIVER_GERD_HIERARCHY.md`, `gerd_pct_gdp_hierarchical.csv`, rebuild proof). Report prose still partly describes the older “WB + forward-fill only” story — see §6.

---

## 3. What we found (data)

### Metaphor reminder

If two charts say “H-index” but drink from different rivers (or invent numbers in the tap), users think the data is broken. Often the **label** was broken.

### Findings (facts from the river audit)

1. **River is only partly clean**  
   Good channel: `CS661_Dataset/raw_vault/READY_FOR_TEAM/`.  
   Polluted channel at dataset root: stub H / yearless quality metrics mixed into older master files.

2. **Graph 2 was inventing H / GDP / GERD**  
   The Q1/Q4 *bars* came from a real river (`q1_q4_country_year.csv`).  
   The *sidebar* used hardcoded `baseMetrics` + fake year growth inside `g2.js`.  
   Example (USA / India 2022, before fix): sidebar H ≈ **1325 / 306** vs Graph 1 SCImago H **3388 / 1001**.

3. **Stub H = 53 vs SCImago Country Rank ≈ 3388 (USA)**  
   `sjr_country_metrics` / old master `H_Index` used a tiny yearless stub scale (USA **53**, India **27**).  
   Real Country Rank H in the good panel: USA **3388**, India **1001**.  
   Same English word “H-index,” three different things (stub, invented UI, real Country Rank).

4. **Different “publications” definitions**  
   One casual word, several real measurement systems:
   - **G1 size:** World Bank scientific journal articles (else SCImago Documents)  
   - **G2 bars:** documents in journals whose **publisher** is in that country  
   - **G3:** OpenAlex works tagged with a **concept / topic**  
   - **G4:** OpenAlex domestic vs international paper sets (cites/paper)  
   - **G5:** OpenAlex **institution** works (stock)  
   Mixing them (e.g. WB → OpenAlex cliff for G1 size) was pollution. Policy now: G1 size = WB else SCImago Documents; **never** OpenAlex for G1 bubble size.

5. **India GERD World Bank gaps**  
   WB GERD for India stops around **2020** (last real ≈ **0.64558%**).  
   UNESCO UIS matches WB on overlaps and **does not** fill India 2021+. OECD has **no India** GERD % rows.  
   **User override (2026-07-12):** pool/UI applies **LOCF ffill** from 2020 → India 2021–2024 display **0.64558** tagged `LOCF:WB:y2020` (river CSV stays missing). See `G2_CARRY_AND_GERD_FFILL.md`.

6. **Browser MCP flaky ≠ data broken**  
   IDE browser automation (no-tab / lock races) failed sometimes. Join proofs were done with Node VM + HTTP smoke. Tool flakiness is not evidence that the river/pool is wrong.

---

## 4. What we changed

File-level bullets (what actually moved):

### Quarantine stubs

- `CS661_Dataset/_QUARANTINE/` — stub H CSV + master backup + README  
- `sjr_country_metrics.csv` moved out of the drinkable root path  
- Root `master_dataset.csv` stub quality columns renamed `*_STUB_YEARLESS_DO_NOT_USE` so accidental joins fail closed

### River ownership locked

- `dashboard/docs/RIVER_OWNERS.md` — one owner per metric label  
- Clean handoff stays `CS661_Dataset/raw_vault/READY_FOR_TEAM/`

### G2 join from VIZ1 (same H / GDP / GERD as G1)

- `dashboard/graphs/g2/g2.js` — removed invented `baseMetrics`; join from `VIZ1_DATA` (ISO3 + aliases + NFKD)  
- After join: USA / India 2022 H **3388 / 1001**, GDP ≈ **77861 / 9207**, GERD from VIZ1 (India recent years **null** after hierarchy)  
- Coverage proof: `dashboard/docs/_g2_g1_join_coverage.json` — **124 / 129** matched

### Pools rebuilt from owners

- Regenerated: `viz1_data.js`, `ridgeline_data.js`, `viz3_data.js`, `viz4_data.js`  
- Rebuild helper: `dashboard/_river_to_pool_rebuild.py`  
- Proof: `dashboard/docs/_river_to_pool_rebuild_proof.json`  
- G3 AI primary locked to Machine learning **`C119857082`** (not mega-AI `C154945302`); Quantum **`C58053490`**  
- `dashboard/data.js` stubs neutralized (empty + warn) so fake collab / India / topics cannot silently override  
- `panel_data.js` not loaded from `index.html`

### Modular graphs

- `dashboard/graphs/g1` … `g5` each with `gN.js` / `gN.css`  
- Layout contract: `dashboard/GRAPHS_LAYOUT.md`  
- Thin `app.js` orchestrator + shared `style.css`

### G3 honesty / UI-side cleanup

- Pool trimmed to a defendable honesty window (pre-2000 mega / incomplete backfill omitted from tap; river CSV can still hold more)  
- Topic IDs moved off forbidden ASJC-style numbers (Quantum is not Materials Science `2500`)  
- AI concept locked to **`C119857082`** in owners + rebuild guard

### Landing CSS only

- Fonts: Outfit (headings) + Plus Jakarta Sans (body) via Google Fonts in `index.html`  
- Full-bleed landing shell in `style.css` (shell itself has no max-width gutter)  
- Chart JS/CSS modules not rewritten for landing polish

### Report `.tex` honesty pass

- Primary file: `CS661 Project/CS661_Project_Report_Group10_Final.tex`  
- Details in §5 below

### GERD hierarchy (river + pool)

- Builder: `dashboard/_build_gerd_hierarchy.py`  
- River CSV: `READY_FOR_TEAM/gerd_pct_gdp_hierarchical.csv`  
- Docs: `dashboard/docs/RIVER_GERD_HIERARCHY.md`  
- Overlap gate: **0.05 pp**; UIS ≡ WB on overlaps; OECD fills holes only for countries with **100%** overlap match; no everlasting ffill  
- Pool proof shows India 2021–2024 GERD **null**; USA 2024 can take **OECD** when eligible

---

## 5. Project report (LaTeX) specifically

**File:** `CS661 Project/CS661_Project_Report_Group10_Final.tex`  
(Working sibling may also exist: `CS661_Project_Report_Group10_WORKING.tex` — Final is the honesty target.)

### Sections that were made more honest

| Area | What we corrected toward |
|------|---------------------------|
| **§ Domain Research and Data Acquisition** | River vs pool framing; **World Bank as live primary** for Module 1 GERD/GDP/articles; UNESCO/OECD as **acquired reference**, not silently equal live feeds |
| **SCImago** | Country Rank owns **H-index**; Journal Rank owns **publisher-country** Q1/Q4 (not author affiliation) |
| **OpenAlex** | Topics (G3), collab premium (G4), India network (G5); **not** G1 bubble size |
| **§ Data Preprocessing / Architecture** | Live panel path; static JS pools; pointer to `RIVER_OWNERS.md` / rebuild scripts |
| **Frontend** | **Modular vanilla JavaScript** shell (`graphs/g1`–`g5`); no React/Vite runtime in the live app |
| **Macro path language** | Softened “tripartite merge as executed” → acquisition vs what the live pool actually drinks |

### Claims that are still stale (do not treat as current engineering truth)

- **Abstract** still says “bespoke **React** and D3.js frontend”  
- **Objectives** still list **React.js** as the build stack  
- **Team Contributions** still mention React / Vite / React↔D3 bridging  
- Some macro paragraphs still describe **forward-fill** / “hierarchical merge not yet live” in places that predate (or lag) the gated GERD hierarchy river — prefer `RIVER_GERD_HIERARCHY.md` + rebuild proof for current GERD behavior  
- Older UNESCO/OECD detail bullets (e.g. HERD/BERD/GOVERD naming, “India in OECD extract,” “back to 1981”) may still overclaim relative to what is on disk; fact-check notes live in `dashboard/REPORT_SECTION2_FACTCHECK.md` (partly written *before* later H / hierarchy fixes — use with care)

**Bottom line for the report:** body sections on data architecture and frontend were pushed toward honesty; **abstract + contribution bullets still need a React → vanilla JS cleanup**.

---

## 6. Open / in progress

### GERD hierarchy (OECD → UNESCO → WB with overlap gate)

**Status: largely done in river + pool; report prose still catching up.**

Done (with proof):

- Overlap audit (WB vs UIS match rate **1.0**; WB vs OECD ≈ **0.96** with conflict countries blocked from Frankenstein stitch)  
- Hierarchical CSV written  
- Owners table updated to gated hierarchy (**no everlasting ffill**)  
- Pool rebuild: India 2022 GERD **`null`**; USA 2024 can be **OECD**-sourced when eligible  

Still open / follow-up:

- Keep **Final.tex** macro paragraphs aligned with gated OECD holes + **documented display LOCF** (see `G2_CARRY_AND_GERD_FFILL.md`)
- Do not invent GERD without a prior observation; LOCF tags must stay visible in `GERD_Source`

### Remaining unmatched G2 ↔ G1 countries (sidebar)

Fail closed (no invented H/GDP/GERD):

- Cuba  
- Monaco  
- New Caledonia  
- Taiwan  
- Vatican City State  

These have no matching row in G1 `VIZ1_DATA` under the current join rules (**5 / 129**). Status detail: [`G2_CARRY_AND_GERD_FFILL.md`](G2_CARRY_AND_GERD_FFILL.md).

### GERD display LOCF (user override 2026-07-12)

- Pool LOCF: **1066** country–years / **105** countries; India 2021–2024 = **0.64558** (`LOCF:WB:y2020`)
- H prior-year carry: **15** CY / **3** countries (`VEN`, `BTN`, `LBN`)
- GDP prior-year carry: **15** CY / **3** countries (same)

### G4 “111 countries” — why unverified, where backed data comes from

- **Old FE** (`viz4_data_BEFORE_POOLFIX.js`): undated 111-country snapshot. Most countries had **no** rows in `collaboration_premium.csv`; even the overlapping 20 did not match any single premium year → **unverified**, must not be revived as live data.
- **Backed data** comes from the **OpenAlex works API** (same recipe as `G4_RECOVERY_PLAN.md`): domestic `countries_distinct_count:1` vs international `>1`, population mean of `cited_by_count`, by country+year (2010–2024).
- **Live pool now:** **73 countries** (20 core river + 53 OpenAlex population-mean expand). Path: fetch → river CSV → `viz4_data.js`. Status: `dashboard/docs/G4_EXPAND_STATUS.md`. Runner: `scripts/expand_g4_openalex.py` (resumable cache). Do not revive the 111 snapshot.

### Other leftover risks (from river fix docs)

- G3 river CSV may still contain mega-AI rows; pool + rebuild guard must keep preferring **`C119857082`**  
- Old scripts may still *mention* quarantined stub paths; rebuild must refuse drinkable stub H at root  
- Some TAP copy (author-country wording on G2, etc.) may still need wording polish even when numbers are correct

---

## 7. Where to read more

| Doc | Path | What it is |
|-----|------|------------|
| This explainer | `dashboard/docs/EXPLAINER_FINDINGS_AND_CHANGES.md` | Plain-language story (you are here) |
| Root pointer | `EXPLAINER_FINDINGS_AND_CHANGES.md` (repo root) | Short pointer to this file |
| River audit | `dashboard/docs/RIVER_PIPELINE_REPORT.md` | Full river vs pool vs tap findings |
| Owners lock | `dashboard/docs/RIVER_OWNERS.md` | One owner per metric label |
| Fix log | `dashboard/docs/RIVER_TO_POOL_FIX.md` | Before/after + file list + G2 join coverage |
| GERD hierarchy / LOCF | `dashboard/docs/RIVER_GERD_HIERARCHY.md`, `G2_CARRY_AND_GERD_FFILL.md` | Overlap gate + India/USA proof + carry counts |
| Graph folders | `dashboard/GRAPHS_LAYOUT.md` | Modular `g1`–`g5` layout |
| Course report | `CS661 Project/CS661_Project_Report_Group10_Final.tex` | Graded LaTeX report |
| Section 2 fact-check | `dashboard/REPORT_SECTION2_FACTCHECK.md` | Earlier honesty audit of acquisition claims (historical; some pool facts superseded) |
| Simple graph deltas | `dashboard/GRAPH_CHANGES_EXPLAINED_SIMPLY.md` | Per-graph before/after in plain English |
| G4 expand status | `dashboard/docs/G4_EXPAND_STATUS.md` | Why 111 unverified; OpenAlex expand progress; resume commands |

---

## Short bottom line

We treated the dashboard like a water system: **river → pool → tap**. The river was only partly clean (stub H, mixed “publications,” soft India GERD fills). Graph 2’s tap was inventing the same words Graph 1 used honestly. We quarantined stubs, locked owners, rebuilt pools, joined G2 to G1, modularized graphs, polished landing CSS, and pushed the LaTeX report toward honesty — while leaving a few stale React lines and unmatched G2 countries as known leftovers.

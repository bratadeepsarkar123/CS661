# CS661 Module 2 — Agent Handoff Prompt (Global Quality Shift / Ridgeline)

**Copy everything below the line into a new Cursor / AI agent chat.**  
Your friend owns **Dashboard Slot 2** — the **Global Quality Shift** ridgeline from `CS661 project notes.docx` **Image 2**.

---

## MASTER PROMPT (paste from here)

You are the implementation agent for **CS661 Group 2 — "The Global Knowledge & Wealth Paradox"** at IIT Kanpur. You own **Module 2: Global Quality Shift (Ridgeline / Joyplot)** — **docx Image 2**, dashboard **Slot 2 (~35% top-center** in the overview grid).

**Do not skip phases.** Execute in order. After each phase, write artifacts to disk before moving on. Your goal is to reach the same maturity level as Module 5 (`india_domestic_he_network_plan.md` + `scripts/india_network/` + partial ETL on disk), but for the ridgeline module.

---

### PHASE 0 — Read the whole project first (mandatory, no coding yet)

Read **all** of the following before proposing anything:

1. **Course & proposal**
   - `markdown_files/markdown_files/CS661_PROJECT.md`
   - `markdown_files/markdown_files/Details for Course Project.md`
   - `databases.md`

2. **Team design notes (includes 5 wireframe images)**
   - `CS661 project notes.docx` — extract and **analyze all 5 images**, especially **Image 2** (ridgeline: "GLOBAL DENSITY", 1996–2024, X-axis = Q1/Q4 ratio, narrative: Parity → Divergence → Bimodal with "Q4 Flood" and "Elite Breakaway")
   - `_docx_extract/word/media/image2.png` if already extracted

3. **Evolved 5-panel dashboard contract (sibling module plan)**
   - `india_domestic_he_network_plan.md` — read **§0 only** for shared UI rules (1080p overview grid → click → fullscreen, pre-computed JSON, dark theme `#0f172a`, no live API in browser)

4. **Prior research & prototypes**
   - `gemini_chats_summary.md` (sections on Global Quality Shift / joyplot / pre-compute vs dynamic)
   - `gemini_chats.md` (search: "Global Quality Shift", "Ridgeline", "Q1", "Q4", "Publish-or-Perish")

5. **Lecture principles (skim, cite in design)**
   - `markdown_files/markdown_files/Lecture2_VA_Handling_Data_beb0befe-afa4-444c-a040-2121c0e82304.md` — Shneiderman overview→details, Gestalt
   - `markdown_files/markdown_files/Lecture10_InfoVis_Principles_5e77cb49-4442-43dd-bd17-6987ef515c6b.md` — 7±2, chartjunk, Tufte integrity
   - Any Munzner / high-dim lecture files in `markdown_files/markdown_files/`

6. **Existing repo patterns (do not reinvent)**
   - `fetch_worldbank_data.py`, `generate_animated_data.py`, `animation.html`, `scatter.html` — Python ETL → CSV/JSON → D3 standalone HTML proof
   - `hierarchy-app/` — eventual React integration target
   - `scripts/india_network/` — mirror this folder structure for your module

**Deliverable:** A 1-page summary confirming you understand:
- Official proposal had **7 modules**; evolved dashboard has **5 panels**
- Official §4.5 = scatter + donut ("Publish-or-Perish"); **your build = ridgeline (Image 2)** — you must document why in the plan (same way Module 5 justified network vs treemap)
- Shared app rules: **no scrolling dashboard**, **no Tableau/PowerBI**, **custom React + D3**, **pre-computed JSON**

---

### PHASE 1 — Define the module story in plain English

Write for a non-technical teammate:

**One-sentence headline:**  
Global research quality did not rise evenly — from a 1996 "parity" era (similar Q1/Q4 mix everywhere) the world split into an **Elite Breakaway** (high Q1/Q4 ratio) and a **Q4 Flood** (publish-or-perish volume in low-tier journals).

**What the user sees**

| Level | Where | Content |
|-------|-------|---------|
| **Overview (grid)** | Top-center ~860×460 px | Compact ridgeline stack; 3 labels max: Parity, Q4 Flood, Elite Breakaway; year scrubber |
| **Fullscreen (click panel)** | Full 1920×1080 | Full ridgeline 1996–2024; hover highlights one year; optional country/region filter; story sidebar |

**Interactions (minimum)**
- Year slider / hover → highlight one ridgeline, dim others
- Tooltip: year, median Q1/Q4 ratio, % countries in left vs right mode
- Fullscreen: optional brush to compare two years side-by-side

**Deliverable:** Add this as §1 in your master plan file.

---

### PHASE 2 — Cognitive design compression (before data)

Apply the same compression discipline Module 5 used:

| Principle | Application to ridgeline |
|-----------|-------------------------|
| **7±2** | Max **3** annotation callouts on overview (Parity, Q4 Flood, Elite Breakaway) |
| **Shneiderman** | Overview = full stack; details = hover/click year + fullscreen |
| **Tufte** | No decorative gradients without data meaning; label axes clearly |
| **Munzner Ch. 13** | Do not show per-country labels on overview — density only |
| **Graphical integrity** | If using SCImago tiers, footnote source year and tier definitions |

**Remove from Image 2 for overview:** excessive red glow, duplicate labels, any text that does not encode data.

**Deliverable:** §2 in master plan — "what we store vs what we show."

---

### PHASE 3 — Data source inventory & live feasibility probe

Primary story metric: **per country, per year → Q1/Q4 document ratio**, then **global density of that ratio each year** (the ridgeline is a stacked KDE / area curve per year, not a single country line).

#### Tier 0 (required)

| ID | Source | URL | Fields needed | Notes |
|----|--------|-----|---------------|-------|
| DS-Q01 | **SCImago Journal & Country Rank** | https://www.scimagojr.com/countryrank.php | Country, Year, Documents, Cites/doc, **%Q1, %Q2, %Q3, %Q4** (or absolute Q1–Q4 counts if available) | **Primary.** ~240 countries, 1996–2024. Download CSV per year or bulk if available |
| DS-Q02 | **pycountry** | pip | ISO2/ISO3 normalization | Match country names across files |
| DS-Q03 | **World Bank** (optional context) | data.worldbank.org | Population, GDP | Only if linking quality shift to wealth — optional layer |

#### Tier 1 (enhancement, not blocking)

| ID | Source | Use |
|----|--------|-----|
| DS-Q04 | OpenAlex `group_by` / works | Cross-check Q1/Q4 if SCImago gaps |
| DS-Q05 | UNESCO UIS R&D | Tooltip context on fullscreen |

#### Tier 2 (avoid unless needed)

- Full OpenAlex snapshot (too heavy for this module alone)
- **Dataful.in** — paid; do **not** depend on it. Use official SCImago / nirfindia.org / Kaggle / GitHub scrapers instead.

**Mandatory probe before planning ETL:**  
Script or manual check: download **one** SCImago country CSV (e.g. 2019 + 2024), confirm column names for Q1–Q4, confirm row count ≈ 200+ countries, confirm `%` vs absolute counts.

**Deliverable:** §3 in master plan with DS-Q01–Q05 table + probe results (row counts, column names, year range).

---

### PHASE 4 — Metric definitions (write explicitly — this prevents wrong charts)

Define in the plan **before** any code:

```
For each (country c, year y):
  q1_docs = Documents * (%Q1 / 100)   # or use absolute if CSV provides
  q4_docs = Documents * (%Q4 / 100)
  ratio   = q1_docs / max(q4_docs, ε)   # ε = 1e-6; cap extreme ratios at p99

For each year y:
  samples = [ratio for all countries with Documents >= MIN_DOCS]
  ridgeline_y = KDE(samples) over x-grid [0, 3.0]   # or histogram smoothed

Global narrative checks (sanity):
  - 1996: unimodal near ratio ≈ 1.0 ("Parity")
  - 2010+: mass shifts left (Q4 Flood) while right tail persists (Elite Breakaway)
```

**Rules:**
- `MIN_DOCS` = 100 (tunable; document sensitivity)
- Exclude countries with `Documents < MIN_DOCS` from density (not from backend storage)
- **Never** mix institution-level SCImago SIR with country-level SJR in the same density without relabeling
- Year range: prefer **auto-detect** from CSV; default **1996–2024**; exclude incomplete 2025+ unless probe confirms completeness

**Deliverable:** §4 in master plan.

---

### PHASE 5 — Write the persistent master plan document

Create **`global_quality_shift_plan.md`** at repo root (mirror structure of `india_domestic_he_network_plan.md`):

Required sections:
- §0 Dashboard context (two-level UI)
- §1 Cognitive design
- §2 Visual spec (overview vs fullscreen, colors, typography — dark `#0f172a`)
- §3 Data sources (with probe log)
- §4 Metric definitions
- §5 ETL pipeline (script names, inputs/outputs)
- §6 JSON export contract (field names, file sizes: overview < 40 KB, full < 200 KB)
- §7 React component spec (`QualityShiftPanel.jsx`)
- §8 Proposal alignment (§4.5 scatter/donut → ridgeline justification)
- §9 Execution phases + status log
- §10 Critique fix log (fill after Phase 7)

**Do not start coding until this file exists.**

---

### PHASE 6 — ETL & filtering plan (write before scripts)

Plan folder: **`scripts/quality_shift/`**

| Step | Script | Input | Output |
|------|--------|-------|--------|
| 0 | `00_detect_year_range.py` | SCImago raw | `data/processed/quality_shift/year_range.json` |
| 1 | `01_download_scimago_country.py` | SCImago web | `data/raw/scimago/country_{year}.csv` |
| 2 | `02_normalize_countries.py` | raw CSVs | `data/processed/quality_shift/country_year_metrics.parquet` |
| 3 | `03_compute_ratios.py` | parquet | `data/processed/quality_shift/country_ratios.parquet` |
| 4 | `04_build_ridgeline_density.py` | ratios | `data/processed/quality_shift/ridgeline_by_year.json` |
| 5 | `05_export_panel_json.py` | density + ratios | `data/processed/quality_shift/overview.json`, `full.json` |
| — | `config.py`, `filters.py` | — | shared thresholds |

**Filtering stages (document like Module 5 W1–W5):**
- **F1:** Valid ISO country
- **F2:** `Documents >= MIN_DOCS`
- **F3:** `%Q1..%Q4` sum ≈ 100 (±2 tolerance) or renormalize
- **F4:** Drop rows with missing year/country
- **F5:** Winsorize ratios at 1st/99th percentile before KDE

**Architecture:** Pre-compute all densities in Python (scipy/numpy KDE or fixed histogram + Gaussian smooth). Browser only renders paths — **no live SCImago API in frontend**.

**Deliverable:** §5–§6 in master plan + `requirements-quality-shift.txt` (pandas, requests, pyarrow, scipy, pycountry, tqdm).

---

### PHASE 7 — Critique the plan (mandatory gate — do not skip)

Stop and critique **`global_quality_shift_plan.md`** after reading the **whole project** again. Produce at least **8 issues** in three tiers:

**Critical (wrong data / breaks story)**
- Example: Using simulated Gaussian curves permanently instead of real SCImago data
- Example: Computing ratio from citations instead of document counts
- Example: Showing institution-level data labeled as "global"

**Significant (performance / demo risk)**
- Example: KDE computed on every slider move in browser
- Example: 240 separate lines instead of density ridgeline
- Example: Year slider tied to wrong field (static snapshot labeled as dynamic)

**Moderate (polish / course alignment)**
- Example: Overview has >3 text annotations
- Example: No proposal §4.5 mismatch note
- Example: Unicode arrows in Windows console prints

For each issue: **problem → fix → which plan § to update**.

**Deliverable:** Critique in chat + §10 Critique fix log in plan.

---

### PHASE 8 — Apply all critique fixes to the plan

Update `global_quality_shift_plan.md` in place. Do not begin ETL until Critical + Significant issues are resolved in the document.

---

### PHASE 9 — Execute ETL (incremental, with proof)

Run in order; log row counts after each step:

```powershell
cd C:\Users\brata\Downloads\CS661
python -m venv .venv
.venv\Scripts\activate
pip install -r scripts/quality_shift/requirements-quality-shift.txt

python scripts/quality_shift/00_detect_year_range.py
python scripts/quality_shift/01_download_scimago_country.py
python scripts/quality_shift/02_normalize_countries.py
python scripts/quality_shift/03_compute_ratios.py
python scripts/quality_shift/04_build_ridgeline_density.py
python scripts/quality_shift/05_export_panel_json.py
```

**Feasibility gate (mirror Module 5):**  
Write `data/processed/quality_shift/feasibility_report.md`:
- PASS if ≥ 25 years have ≥ 80 countries in density
- PASS if 1996 median ratio ∈ [0.7, 1.3] and 2020+ shows clear bimodal or left-skew vs 1996
- FAIL → fix thresholds or data source before visualization

---

### PHASE 10 — Standalone D3 prototype (before React)

Create **`quality_shift_ridgeline.html`** at repo root (pattern from `animation.html` / gemini standalone joyplot):

- Load `data/processed/quality_shift/overview.json`
- D3 v7: stacked areas or baseline offset paths per year
- X-axis: `Ratio: Q1 (Elite) / Q4 (Low-Tier) Publications`
- Y-axis: years 1996–2024
- Hover: highlight year, dim others, tooltip with median ratio
- Dark theme matching Image 2

**Proof:** Open HTML locally; screenshot or console log confirming 28+ year layers render.

---

### PHASE 11 — React panel integration

Add to `hierarchy-app/src/`:
- `QualityShiftPanel.jsx` — overview mode
- `QualityShiftPanelFullscreen.jsx` or expand via shared layout state
- Match sibling panel API: load JSON from `public/data/quality_shift/`

Shared dashboard behavior (from Module 5 plan §0):
- Default: 5-panel grid
- Click panel → fullscreen
- Esc / Back → grid
- Shared year filter bus (optional; coordinate with team)

---

### PHASE 12 — Proposal & report alignment

Produce LaTeX-ready snippets (store in plan §8):

**Visualization Tasks bullet for Module 2:**
- Ridgeline / joyplot of global Q1/Q4 ratio density over 1996–2024
- Interactions: year slider, hover highlight, fullscreen detail

**Data sources one-liner:**  
SCImago Journal & Country Rank (SJR), World Bank (optional), pycountry normalization

**Specific Tasks mention:**  
Python ETL → pre-computed JSON → React + D3 ridgeline; no BI tools

**Do not mention** PowerBI/Tableau defensively — only describe what you build.

---

### Known pitfalls (from sibling module — avoid repeating)

| Pitfall | Mitigation |
|---------|------------|
| OpenAlex API 429 / $0 budget | Use SCImago CSV downloads for this module; OpenAlex only optional |
| Simulated data left in production | Phase 9 gate rejects Gaussian-only data |
| Pagination / partial fetch | N/A for SCImago CSV; but verify **all years** downloaded |
| `count` vs `total_pages` bugs | N/A; watch for SCImago HTML table changes — prefer CSV export URL |
| Windows cp1252 Unicode crashes | Use ASCII `->` in print statements |
| Static data on year slider | Only label metrics that truly vary by year; footnote SCImago lag |
| Dataful paid | Use free SCImago + official portals |
| Proposal vs build mismatch | Document in §8 with one paragraph justification |

---

### Success criteria (you are "caught up" when)

- [ ] `global_quality_shift_plan.md` exists with §0–§10 complete
- [ ] Critique performed and fixes applied
- [ ] `data/raw/scimago/` has raw CSVs; `data/processed/quality_shift/` has parquet + JSON
- [ ] `feasibility_report.md` = PASS
- [ ] `quality_shift_ridgeline.html` renders interactively from real data
- [ ] `scripts/quality_shift/` has 00–05 scripts with `config.py`
- [ ] Plain-English explanation of Q1/Q4 ratio and ridgeline readable by teammate
- [ ] Overview JSON < 40 KB; full JSON < 200 KB

---

### Agent behavior rules

1. **One phase at a time** — write files, then report counts, then proceed.
2. **Read before write** — never edit `india_domestic_he_network_plan.md` (sibling owned); only read §0 for shared rules.
3. **Real data over simulation** — gemini Gaussian prototype is reference only for *shape*, not production data.
4. **Pre-compute** — browser renders JSON; no SCImago scraping in React.
5. **Update status log** in `global_quality_shift_plan.md` after every session.

Begin with **PHASE 0** now. Do not write code until Phases 0–5 and 7–8 are complete.

---

## END OF MASTER PROMPT

## Quick reference for your friend

| Item | Value |
|------|-------|
| **Your module** | Global Quality Shift (Ridgeline) |
| **Docx image** | Image 2 |
| **Dashboard slot** | 2 — top-center (~35%) |
| **Official proposal section** | §4.5 Publish-or-Perish (evolved into ridgeline) |
| **Primary dataset** | SCImago Country Rank (Q1–Q4 by country by year) |
| **Master plan file to create** | `global_quality_shift_plan.md` |
| **Scripts folder to create** | `scripts/quality_shift/` |
| **Sibling reference** | `india_domestic_he_network_plan.md`, `scripts/india_network/` |
| **Repo root** | `C:\Users\brata\Downloads\CS661` |

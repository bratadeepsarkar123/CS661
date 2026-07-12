# G2 / G4 Pipeline Status

**Date:** 2026-07-12 (overnight)  
**Owner:** Cursor (Pattern A implementer)  
**Live TAP:** `dashboard/` @ `http://127.0.0.1:8080`  
**Zip mirror:** `CS661 Project/` (pools + UI mirrored for deliverable)

ICM_RULES_CHECK=`five-layer-glass-box-sequential-review`

---

## 1. River → pool → tap (holes found)

| Graph | River (authority) | Pool hole (before) | Tap hole (before) | After |
|-------|-------------------|--------------------|-------------------|-------|
| **G2** | `q1_q4_country_year.csv` — SCImago **journalrank publisher Country** × Best Quartile, **uncapped** `ratio` (USA 2022 = **14.898**) | `CS661 Project/ridgeline_data.js` still had **capped** ratios (USA 5.0); `dashboard/` already poolfixed | Quality Guide overlapped tall bars (`margin.top` was 40 in Project); copy implied author-country; `OKABE` referenced without definition on live dashboard | Uncapped pool synced; **grouped/stacked bars** default; `margin.top=110` + guide at `top:1.5rem; right:2.5rem`; publisher-country wording; Okabe-Ito blue↔orange |
| **G4** | `collaboration_premium.csv` — **20 countries × 2010–2024** OpenAlex domestic vs intl mean cites | Project still had **111** undated countries; dashboard had single-year 2024 only | Dumbbell / muddy; no year play; no Esc drill-back | Multi-year `VIZ4_BY_YEAR`; **grouped horizontal bars**; year slider + play; region drill + Esc / ← Regions |
| **G3** (touched minimally) | `openalex_topic_country_year.csv`; Quantum = **`C58053490`** | Project pool still had ASJC-style **`2500`** | TAP hard-coded Quantum `2500` / `g-materials` | Pool synced from dashboard (1974–2024, Quantum id correct); TAP ids → OpenAlex `C…` |

**Policy locks honored:** G2 = publisher country, uncapped ratios in pool; G4 = top-20 / panel years from premium CSV (default cross-section still 2024 for flat `VIZ4_DATA`); Quantum ≠ ASJC 2500.

---

## 2. Coverage years

| Graph | Years on disk now | Notes |
|-------|-------------------|-------|
| G2 | **1999–2024** | Full SCImago journalrank rollup already in river; no invent |
| G4 | **2010–2024** | All 20 countries every year from `collaboration_premium.csv` |
| G3 (side fix) | **1974–2024** in tap pool | Pre-1974 / sparse topics still river-limited; no hammering OpenAlex overnight |

OpenAlex probe this session: HTTP 200, rate-limit remaining ~9.6k. Full G4 population-mean regen via API still expensive (must exhaust cursors); **not re-fetched** — river CSV is the honest source.

---

## 3. How to re-run fetches / rebuilds

### G2 pool (no live download required if XLS already in vault)

```powershell
cd C:\Users\brata\Downloads\CS661
python scripts\rebuild_g2_g4_project_pool.py
# copies uncapped ridgeline + multi-year viz4 into CS661 Project\
# then sync to live TAP:
Copy-Item "CS661 Project\ridgeline_data.js" dashboard\ridgeline_data.js -Force
Copy-Item "CS661 Project\viz4_data.js" dashboard\viz4_data.js -Force
```

Optional river rebuild from XLS:

```powershell
cd CS661_Dataset\raw_vault\03_scimago_journal_quartiles
python aggregate_g2_quartiles.py
```

### G4 pool

Same rebuild script emits `VIZ4_BY_YEAR` / `VIZ4_YEARS` / `VIZ4_DEFAULT_YEAR` from `CS661_Dataset/collaboration_premium.csv` (or `READY_FOR_TEAM/collaboration_premium.csv`).

To **extend** beyond 20 countries or refresh means: follow `CS661_Dataset/raw_vault/G4_RECOVERY_PLAN.md` (snapshot preferred; API needs full cursor exhaustion + backoff).

### G3 topic backfill (optional, rate-limit sensitive)

```powershell
cd CS661_Dataset\raw_vault\04_openalex
# Prefer sleep + API key from CS661\.env — never print the key
python fetch_topics_full.py --years 1950-1999 --sleep 0.35
# then rebuild viz3 via dashboard\_poolfix_rebuild.py G3 section
```

### Visual QA

```powershell
cd C:\Users\brata\Downloads\CS661\dashboard
python -m http.server 8080 --bind 127.0.0.1
python ..\scripts\_qa_g2_g4_playwright.py
# screenshots → docs\_qa_g2_g4\
```

---

## 4. UI proof (Playwright 2026-07-12)

| Check | Result |
|-------|--------|
| G2 chart family | Grouped bars (10 whitelist countries) |
| G2 Quality Guide vs bars | `overlap: false`; chart `translateY=110` |
| G2 Esc clears country | `China` → `null` |
| G4 chart family | Grouped horizontal bars (domestic orange / intl blue) |
| G4 drill | Region → `East Asia & Pacific` (CN/JP/KR) |
| G4 Esc | Back to `All` |
| Page errors | **0** |

Screenshots: `docs/_qa_g2_g4/01_g2_bars.png` … `06_g4_after_esc.png`

---

## 5. Navigation checklist

### G2
- [x] Year scrub + Play + speed
- [x] Grouped / Stacked
- [x] Continent / sort / factor sliders + Reset All
- [x] Click bar → select; Esc / clear → deselect
- [x] Back to Dashboard

### G4
- [x] Year scrub + Play (2010–2024)
- [x] Region aggregate → click drill to countries
- [x] Esc / ← Regions → All
- [x] Sort modes
- [x] Click country to pin/unpin highlight
- [x] Back to Dashboard

### G3 (filter-only)
- [x] Quantum OpenAlex id `C58053490` (not Materials `2500`)
- [x] Esc resets country filter toward GLOBAL when drilled

---

## 6. Files changed (primary)

| Path | Role |
|------|------|
| `dashboard/app.js` | Live TAP — G2 bars + guide margin, OKABE alias, G4 grouped bars + Esc |
| `dashboard/viz4_data.js` | Multi-year 20-country pool |
| `dashboard/ridgeline_data.js` | Uncapped G2 pool |
| `dashboard/index.html` | Cache-bust `?v=20260712g24b` |
| `CS661 Project/app.js` | Deliverable mirror — same G2/G4 intent |
| `CS661 Project/ridgeline_data.js` | Uncapped rebuild |
| `CS661 Project/viz4_data.js` | Multi-year rebuild |
| `CS661 Project/viz3_data.js` | Quantum id pool sync |
| `CS661 Project/index.html` | Cache-bust + G4 tags |
| `scripts/rebuild_g2_g4_project_pool.py` | Rebuild helper |
| `docs/_g2_g4_pool_rebuild_proof.json` | Anchor proof |
| `docs/G2_G4_PIPELINE_STATUS.md` | This file |

G1 motion code in `dashboard/app.js` left intact (EMA/rAF trails untouched).

---

## 7. Remaining blockers

1. **G4 >20 countries** — needs OpenAlex dump or multi-day API with exhausted cursors; do not restore 111-country snapshot.
2. **G3 1950–1973 / sparse topics** — optional backfill; watch 429 / USD budget.
3. **G2 SJR portal drift** — older years may differ slightly from live portal if SCImago revises history; river XLS is the owned snapshot.
4. **Two frontends** — keep `dashboard/` (live G1 polish) and `CS661 Project/` pools in sync when shipping the zip.

---

## 8. Numbering note

Proposal / TAP numbering: **G3 = topic bar race**, **G4 = collaboration premium**. Overnight brief mixed “G4 = topic race / Quantum”; Quantum fix was applied on **G3**, while **G4** received the collaboration bar restore + year panel.

# River → pool fix (2026-07-12)

**Owners table:** [`RIVER_OWNERS.md`](RIVER_OWNERS.md)  
**Audit guide:** [`RIVER_PIPELINE_REPORT.md`](RIVER_PIPELINE_REPORT.md)  
**Rebuild:** `dashboard/_river_to_pool_rebuild.py`  
**Verify:** `dashboard/_verify_river_fix.py`

## Before → after (USA / India 2022)

### H-index / GDP / GERD (same labels across G1 & G2 sidebar)

| Metric | Place | BEFORE (polluted) | AFTER (locked river) |
|--------|-------|-------------------|----------------------|
| H-index | G1 pool | 3388 / 1001 (already good SCImago) | **3388 / 1001** (unchanged, verified) |
| H-index | G2 sidebar | **~1325 / ~306** invented (`baseMetrics` + year growth) | **3388 / 1001** join from `VIZ1_DATA` |
| GDP PPP | G2 sidebar | **~97054 / ~3000** invented ×1.025^y | **~77861 / ~9207** World Bank via G1 |
| GERD % | G2 sidebar | **2.74 / 0.85** hardcoded | **3.487 / —** (India 2022 null — no ffill; USA WB via G1 hierarchical river) |

### Chart pools (already mostly clean; rebuilt to lock owners)

| Graph | BEFORE risk | AFTER |
|-------|-------------|-------|
| G1 | Stub H in `master`/`sjr` could re-poison rebuilds | Stub quarantined; pool synced from `g1_features_panel.csv` |
| G2 bars | Publisher Q1/Q4 OK | Rebuilt from `q1_q4_country_year.csv` (USA ratio **14.898**) |
| G3 | READY map still listed mega-AI primary | Pool AI = **`C119857082`** (USA 41530 / India 25155); Quantum **`C58053490`**; READY map synced |
| G4 | `data.js` COLLAB stub could override if pool missing | Stub returns `[]`; pool = all-year `collaboration_premium` (USA gain **8.901**) |
| G5 | Demo `getIndiaNetwork` growth | Stub returns empty; live JSON kept (23 files) |

## What changed (files)

### River quarantine
- `CS661_Dataset/_QUARANTINE/` — stub H CSV + master backup + README
- `CS661_Dataset/sjr_country_metrics.csv` → moved to quarantine
- `CS661_Dataset/master_dataset.csv` — stub quality columns renamed `*_STUB_YEARLESS_DO_NOT_USE`
- `CS661_Dataset/raw_vault/READY_FOR_TEAM/topic_id_map.json` — AI primary → `C119857082`

### Tap / pool
- `dashboard/graphs/g2/g2.js` — removed invented `baseMetrics`; join H/GDP/GERD from `VIZ1_DATA`; honest publication labels
- `dashboard/graphs/g1/g1.js` — honest “country journal articles” labels
- `dashboard/data.js` — COLLAB / India / topics / countries stubs neutralized (empty + warn)
- `dashboard/index.html` — stopped loading `panel_data.js`; cache-bust script tags
- `dashboard/panel_data.js` — quarantine header (not loaded)
- Pools regenerated: `viz1_data.js`, `ridgeline_data.js`, `viz3_data.js`, `viz4_data.js`
- Docs: `RIVER_OWNERS.md`, this file, rebuild proof JSON

## Proof samples

```
G2 getCountryMetrics United States H=3388 GDP=77861 GERD=3.48736 from=VIZ1:USA:2022
G2 getCountryMetrics India         H=1001 GDP=9207  GERD=0.64558 from=VIZ1:IND:2022
match G1 USA H === G2 USA H  → true
```

HTTP smoke: `http://127.0.0.1:8080/index.html` → 200.

## All-country G2↔G1 join (2026-07-12 follow-up)

| | Matched | Total G2 countries | % |
|--|---------|--------------------|---|
| **Before** (exact name + thin aliases) | 119 | 129 | **92.2%** |
| **After** (ISO3 pins + alias groups + NFKD) | 124 | 129 | **96.1%** |

**Still unmatched (no row in G1 `VIZ1_DATA` — fail closed “—”):**  
Cuba · Monaco · New Caledonia · Taiwan · Vatican City State

Spot-checks (2022 H equals G1): USA, India, China, Brazil, Germany, UK, Japan, South Korea, Russia, Nigeria, Egypt, Turkey, Iran, Vietnam, Slovakia, Kyrgyzstan, Palestine, Brunei, Czech Republic, Hong Kong — all OK.

Proof files: `docs/_g2_g1_join_coverage.json`, `node _verify_g2_g1_join.js`, `node _smoke_no_mcp.js`.

## Remaining risks

1. **Name-join gaps (mostly fixed 2026-07-12):** G2↔G1 sidebar join now uses ISO3 pins + alias groups + NFKD normalize. Coverage **119/129 → 124/129 (96.1%)**. Remaining unmatched (no G1 VIZ1 row): Cuba, Monaco, New Caledonia, Taiwan, Vatican City State — sidebar shows “—” (fail closed; no invention).
2. **India GERD:** Hierarchical river + overlap gate applied (`RIVER_GERD_HIERARCHY.md`). India 2021+ is **missing** (no OECD/UIS beyond WB 2020) — pool no longer forward-fills 0.64558. G2 exact-year join shows “—”.
3. **G3 river CSV** still contains mega-AI rows; pool filters them out — rebuild script pins `C119857082` and **refuses** forbidden mega-AI `C154945302` as primary.
4. **Old scripts** (`_poolfix_rebuild.py`, audits) may still *mention* `sjr_country_metrics.csv` paths; rebuild guard refuses drinkable stub H at root.
5. **Browser MCP** flaky (no-tab / lock races) — join proof via Node VM + Puppeteer HTTP smoke; MCP tool flaky ≠ data broken.

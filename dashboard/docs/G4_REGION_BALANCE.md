# G4 Region Balance

**Date:** 2026-07-12  
**Pool:** `dashboard/viz4_data.js`  
**River:** `CS661_Dataset/collaboration_premium.csv` (OpenAlex population means, 2010–2024)  
**Runner:** `scripts/expand_g4_openalex.py` (`--region-balance`, Europe lock)

## Rules applied

| Rule | Result |
|------|--------|
| **Europe** — do not increase or decrease | Locked at **21** ISOs (see list below) |
| **Oceania** — leave as-is | Locked at **2** (`AU`, `NZ`) |
| Other dashboard regions — target **8–12** | Fill up; do not cut if already >12 |
| Continental Africa / Americas / Asia | Bring each to **≥8** where possible |

Europe locked ISOs (unchanged):  
`BG CH CZ DE ES FI FR GB GR HR HU IE IT NL PL RO RS RU SE SI SK`

Europe cached but **excluded** from live pool (lock):  
`AT BE DK NO PT UA`

## Before / after (dashboard regions)

Live pool before this pass: **42** countries. After: **65**.

| Region | Before | After | Notes |
|--------|-------:|------:|-------|
| Europe | 21 | **21** | Locked — no adds/removes |
| Oceania | 2 | **2** | Locked as-is |
| East Asia & Pacific | 6 | **10** | In 8–12 |
| South Asia | 1 | **8** | In 8–12 |
| Latin America | 4 | **8** | In 8–12 |
| Middle East & Africa | 6 | **14** | >12 — filled for Africa ≥8; not cut |
| North America | 2 | **2** | Only `US`/`CA` in scheme; Americas filled via Latin America |
| **Total** | **42** | **65** | |

### Continent-style rollups (for the Africa / Asia / Americas brief)

| Continent | Before | After |
|-----------|-------:|------:|
| Europe | 21 | 21 (locked) |
| Oceania | 2 | 2 (locked) |
| Americas (NA + Latin America) | 6 | **10** |
| Africa (subset of ME&A) | 1 | **8** |
| Asia (EAP + South Asia; ME counted under ME&A UI) | 7 | **18** |

## Countries added (23)

### From existing expand cache (merge under Europe lock)

| ISO | Name | Region |
|-----|------|--------|
| `MX` | Mexico | Latin America |
| `PE` | Peru | Latin America |
| `TW` | Taiwan | East Asia & Pacific |
| `MY` | Malaysia | East Asia & Pacific |
| `PH` | Philippines | East Asia & Pacific |
| `VN` | Vietnam | East Asia & Pacific |
| `PK` | Pakistan | South Asia |
| `BD` | Bangladesh | South Asia |
| `ZA` | South Africa | Middle East & Africa |
| `EG` | Egypt | Middle East & Africa |
| `SA` | Saudi Arabia | Middle East & Africa |
| `MA` | Morocco | Middle East & Africa |
| `TN` | Tunisia | Middle East & Africa |

### Fresh OpenAlex fetch this pass (population means)

| ISO | Name | Region |
|-----|------|--------|
| `EC` | Ecuador | Latin America |
| `UY` | Uruguay | Latin America |
| `LK` | Sri Lanka | South Asia |
| `NP` | Nepal | South Asia |
| `AF` | Afghanistan | South Asia |
| `BT` | Bhutan | South Asia |
| `MV` | Maldives | South Asia |
| `KE` | Kenya | Middle East & Africa |
| `GH` | Ghana | Middle East & Africa |
| `ET` | Ethiopia | Middle East & Africa |

## After — country lists by region

- **Europe (21):** BG, CH, CZ, DE, ES, FI, FR, GB, GR, HR, HU, IE, IT, NL, PL, RO, RS, RU, SE, SI, SK  
- **Oceania (2):** AU, NZ  
- **East Asia & Pacific (10):** CN, HK, JP, KR, MY, PH, SG, TH, TW, VN  
- **South Asia (8):** AF, BD, BT, IN, LK, MV, NP, PK  
- **Latin America (8):** AR, BR, CL, CO, EC, MX, PE, UY  
- **Middle East & Africa (14):** AE, EG, ET, GH, IL, IR, KE, MA, NG, QA, SA, TN, TR, ZA  
- **North America (2):** CA, US  

## UI / integrity

- `VIZ4_META.n_countries` = **65**; years **2010–2024**  
- Fallback label in `dashboard/index.html` `#g4-country-count` → **65**  
- Cache-bust: `viz4_data.js?v=20260712-g4-region65`  
- Chart family unchanged: **dumbbell** (`graphs/g4/g4.js`)  
- G1–G3 / G5 not touched  
- Do **not** revive `viz4_data_BEFORE_POOLFIX.js`  

## Script flags used

```powershell
cd C:\Users\brata\Downloads\CS661
python scripts/expand_g4_openalex.py --rebuild-only
python scripts/expand_g4_openalex.py --region-balance --only EC,UY,LK,NP,AF,BT,MV,KE,GH,ET --max-new 10
```

`allowed_in_live_pool()` enforces Europe / Oceania locks on every merge.

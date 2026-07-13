# GERD hierarchical river (gated)

**Date:** 2026-07-12  
**Builder:** `dashboard/_build_gerd_hierarchy.py`  
**River CSV:** `CS661_Dataset/raw_vault/READY_FOR_TEAM/gerd_pct_gdp_hierarchical.csv`  
**Proof:** `READY_FOR_TEAM/_notes/gerd_hierarchy_proof.json`  
**Overlap audit:** `dashboard/_audit_gerd_overlap.py`

## WHY India GERD looked “complete” but was wrong

World Bank `GB.XPD.RSDV.GD.ZS` often lacks recent India (and other) years — reporting lag/holes. The pool used **everlasting forward-fill** after the last WB observation (India stuck at **0.64558%** for 2021–2024). That was a tap/pool bandage, not a second source.

## WHAT we do instead (with overlap gate)

Sources on disk:

| Priority intent | File |
|-----------------|------|
| OECD MSTI GERD % GDP | `07_oecd_msti/raw_oecd_msti.csv` — `MEASURE=G`, `UNIT_MEASURE=PT_B1GQ` |
| UNESCO UIS GERD % GDP | `06_unesco_uis/SCN-SDG_RD_Feb2026.zip` → `EXPGDP.TOT` |
| World Bank | `01_world_bank/API_GB.XPD.RSDV.GD.ZS_*.csv` |

### Overlap consistency gate (mandatory)

**Tolerance:** **0.05 percentage points**.

| Pair | Overlap *n* | Match within 0.05 pp | Match rate | Conflicts |
|------|-------------|----------------------|------------|-----------|
| **WB vs UIS** | 2467 | 2467 | **1.0000** | **0** |
| **WB vs OECD** | 1159 | 1117 | **0.9638** | **42** |
| **OECD vs UIS** | 1159 | 1117 | **0.9638** | **42** |

**Interpretation:**

- UIS `EXPGDP.TOT` is **identical** to WB on every overlapping cell in this vault. UIS also adds **zero** country–years beyond WB → **cannot fill India 2021+**.
- OECD disagrees on some countries. **Do not Frankenstein-stitch** OECD into those series.

### Merge rule (one consistent series per country)

1. **If WB exists for country+year → use WB** (label `WB`). UIS identity is noted in side columns; it is not a competing stitch.
2. **True WB holes:** fill with **OECD only if** that country has **100%** of WB∩OECD overlaps within 0.05 pp (**39** eligible countries).
3. **Ineligible OECD countries** (keep WB/UIS only — never OECD):  
   `AUS`, `CAN`, `CHE`, `GBR`, `ISR`, `RUS`, `TUR`
4. **OECD-only territories with no WB** (e.g. `TWN`): use OECD as the full series.
5. **Otherwise leave missing in the river CSV** — no LOCF written into `gerd_pct_gdp_hierarchical.csv`.

### Display LOCF (pool / UI — user override 2026-07-12)

After the gated hierarchy is joined into `viz1_data.js`, the pool applies **last-observation-carried-forward (LOCF)** per country for **display** so G1 and G2 stay aligned when later years have no WB/UIS/OECD cell (e.g. India 2021–2024 → **0.64558** from WB 2020, tagged `LOCF:WB:y2020`).

See [`G2_CARRY_AND_GERD_FFILL.md`](G2_CARRY_AND_GERD_FFILL.md) for counts and unmatched-5 status.

Conflict detail CSVs: `_notes/gerd_conflicts_wb_oecd.csv`, `_notes/gerd_conflict_summary_by_country.csv`.

### Conflict summary (WB vs OECD, max |Δ| pp)

| iso3 | n_conflicts | max_diff (pp) |
|------|-------------|-----------------|
| ISR | 7 | 0.613 |
| AUS | 12 | 0.200 |
| TUR | 2 | 0.138 |
| CAN | 1 | 0.125 |
| CHE | 4 | 0.118 |
| RUS | 15 | 0.089 |
| GBR | 1 | 0.077 |

## India proof (2015–2024)

| Year | River value | River source | Pool / UI (after LOCF) |
|------|-------------|--------------|-------------------------|
| 2015 | 0.69310 | WB (=UIS) | 0.69310 `WB` |
| 2016 | 0.66984 | WB | 0.66984 `WB` |
| 2017 | 0.66603 | WB | 0.66603 `WB` |
| 2018 | 0.66001 | WB | 0.66001 `WB` |
| 2019 | 0.65942 | WB | 0.65942 `WB` |
| 2020 | 0.64558 | WB | 0.64558 `WB` |
| 2021 | — | *missing* | **0.64558** `LOCF:WB:y2020` |
| 2022 | — | *missing* | **0.64558** `LOCF:WB:y2020` |
| 2023 | — | *missing* | **0.64558** `LOCF:WB:y2020` |
| 2024 | — | *missing* | **0.64558** `LOCF:WB:y2020` |

OECD has **no India** GERD % GDP rows. UIS stops at the same year as WB (2020). River stays honest-missing; **pool/UI LOCF** is the documented display policy.

## USA sample (OECD hole-fill works when eligible)

| Year | Value | Source |
|------|-------|--------|
| 2022 | 3.48736 | WB |
| 2023 | 3.44716 | WB |
| 2024 | 3.44486 | **OECD** (WB hole; USA overlap-eligible) |

## Cross-graph consistency

| Graph | Shared H / GDP / GERD |
|-------|------------------------|
| **G1** | Pool from panel + hierarchical GERD + **display LOCF**; H = SCImago only |
| **G2** | Sidebar joins H/GDP/GERD from `VIZ1_DATA` (GERD LOCF; H/GDP whole-row prior when exact year missing) |
| **G3** | OpenAlex topics only — no country GERD/H/GDP labels |
| **G4** | Collab cites/paper only — no GERD/H/GDP |
| **G5** | India institute network — no country GERD/H/GDP |

GDP PPP remains **World Bank only**. H-index remains **single SCImago Country Rank river**.

## Rebuild

```bash
python dashboard/_build_gerd_hierarchy.py
python dashboard/_river_to_pool_rebuild.py
```

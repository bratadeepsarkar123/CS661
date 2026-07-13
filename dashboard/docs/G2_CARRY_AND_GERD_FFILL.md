# G2 prior-year carry & GERD LOCF ffill

**Date:** 2026-07-12  
**User override:** India (and other) GERD gaps after last known observation should **forward-fill (LOCF)** for display — not show “—”.  
**Stats machine output:** [`_g2_carry_and_gerd_ffill_stats.json`](_g2_carry_and_gerd_ffill_stats.json)  
**Audit script:** `dashboard/_audit_g2_carry_and_gerd_ffill.py`  
**Pool rebuild:** `dashboard/_river_to_pool_rebuild.py` → `apply_gerd_locf`

---

## Policy (what changed)

| Layer | Behavior |
|-------|----------|
| **River** (`gerd_pct_gdp_hierarchical.csv`) | Unchanged — exact-year gated hierarchy only (WB / OECD hole-fill / UIS≡WB). No LOCF in the river CSV. |
| **Pool** (`viz1_data.js`) | After hierarchy join, **LOCF ffill** per country: missing later years carry the last non-null `GERD_Percent_GDP`. Tagged `GERD_Source = LOCF:<src>:yYYYY` (e.g. `LOCF:WB:y2020`). |
| **G2 tap** (`getCountryMetrics`) | Reads VIZ1; if GERD still null, also LOCF from last prior non-null VIZ1 GERD (belt-and-suspenders). H/GDP still use **whole-row prior** when the exact G1 year row is missing. |
| **G1 tap** | Same pool → India 2021–2024 GERD matches G2 (~0.64558). |

This is **last observation carried forward (LOCF)**, not a second source and not invented growth.

---

## India proof (user ask)

| Year | GERD % GDP | Source |
|------|------------|--------|
| 2015–2020 | real WB series | `WB` |
| 2020 | **0.64558** | `WB` (last real) |
| 2021–2024 | **0.64558** | `LOCF:WB:y2020` |

**India 2022 G2 sidebar:** ≈ **0.65%** (not “—”).

---

## H-index prior-year carry (G2 join)

**Rule:** if G2 year has **no** VIZ1 row for that ISO3, use nearest prior VIZ1 row’s `H_Index` (whole-row prior). No invented growth.

| Metric | Count |
|--------|------:|
| **Country–years** | **15** |
| **Countries** | **3** (`BTN`, `LBN`, `VEN`) |
| Matched G2 country–years (denom.) | 2612 / 2705 |

### By G2 year

| G2 year | H-carry CY |
|---------|----------:|
| 2012–2023 | 1 each (all `VEN`) |
| 2024 | 3 (`VEN`, `BTN`, `LBN`) |

### Full country breakdown

| Country | ISO3 | G2 years carried | H taken from | H value |
|---------|------|------------------|--------------|--------:|
| Venezuela | VEN | 2012–2024 (**13** CY) | 2011 | 306 |
| Bhutan | BTN | 2024 (**1**) | 2023 | 82 |
| Lebanon | LBN | 2024 (**1**) | 2023 | 353 |

**Why Venezuela:** VIZ1 drops out after 2011 (UMAP-ready / GDP completeness); G2 publisher bars continue → sidebar carries 2011 H.

---

## GDP prior-year carry (G2 join)

**Same whole-row prior rule** as H (same 15 country–years / same 3 countries).

| Metric | Count |
|--------|------:|
| **Country–years** | **15** |
| **Countries** | **3** (`BTN`, `LBN`, `VEN`) |

| Country | ISO3 | G2 years | GDP from year | GDP PPP (approx.) |
|---------|------|----------|---------------|------------------:|
| Venezuela | VEN | 2012–2024 | 2011 | ~21241 |
| Bhutan | BTN | 2024 | 2023 | ~16215 |
| Lebanon | LBN | 2024 | 2023 | ~12575 |

---

## GERD LOCF ffill (after change)

### Pool (authoritative)

| Metric | Count |
|--------|------:|
| **Country–years with `GERD_Source` starting `LOCF:`** | **1066** |
| **Countries** | **105** |

Recent-year volume (pool LOCF cells):

| Year | LOCF CY |
|------|--------:|
| 2015 | 38 |
| 2016 | 53 |
| 2017 | 48 |
| 2018 | 52 |
| 2019 | 49 |
| 2020 | 59 |
| 2021 | 58 |
| 2022 | 65 |
| 2023 | 63 |
| 2024 | 85 |

### Top examples

| Code | Year | GERD | Source tag |
|------|------|------|------------|
| IND | 2021–2024 | 0.64558 | `LOCF:WB:y2020` |
| AGO | 2024 | 0.03229 | `LOCF:WB:y2016` |
| ALB | 2024 | 0.19997 | `LOCF:WB:y2022` |
| AND | 2024 | 0.15818 | `LOCF:WB:y2022` |
| ARE | 2024 | 1.49469 | `LOCF:WB:y2021` |

---

## Unmatched 5 (no G1 VIZ1 row — fail closed)

Still **5 / 129** G2 countries with sidebar H/GDP/GERD = “—” (no invented metrics).

| Country | ISO3 | In panel? | In VIZ1? | Why no G1 row | Action this pass |
|---------|------|-----------|----------|---------------|------------------|
| **Cuba** | CUB | Yes | No | SCImago H + GERD exist; **GDP PPP empty all years** → UMAP `FEATURES` `dropna` drops CUB | Left unmatched |
| **Monaco** | MCO | Yes | No | H exists; GDP missing; GERD only 2004–2005 | Left unmatched |
| **New Caledonia** | NCL | Yes | No | H + docs; no GDP PPP; no GERD | Left unmatched |
| **Taiwan** | TWN | **No** | No | WB panel omits Taiwan. SCImago **H=784** exists; OECD GERD exists for `TWN`; no WB GDP in panel. Needs special ISO/name panel path | Left unmatched (special handling deferred — do not invent) |
| **Vatican City State** | VAT | **No** | No | Tiny SCImago H only; no panel / no GERD river | Left unmatched |

---

## Labels / publications ≠ G1

Left **by design**: G2 “Publisher journal docs” ≠ G1 WB/SCImago country articles. Sidebar tooltip already distinguishes them; no further label change required for this leftover pass.

---

## Verify commands

```bash
cd dashboard
python -c "from _river_to_pool_rebuild import assert_no_stub_h_sources, verify_g1; assert_no_stub_h_sources(); verify_g1()"
python _audit_g2_carry_and_gerd_ffill.py
```

Expect: India 2022 GERD `0.64558` / `LOCF:WB:y2020`; H carry CY = 15; GDP carry CY = 15; GERD LOCF pool CY = 1066.

Cache-bust: `viz1_data.js?v=20260712-gerd-locf`, `graphs/g2/g2.js?v=20260712-gerd-locf`.

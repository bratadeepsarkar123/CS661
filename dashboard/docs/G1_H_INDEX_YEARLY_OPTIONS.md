# G1 H-index: why flat, and can it vary by year?

**Date:** 2026-07-12  
**Status:** Investigation only (no pool/river rewrite in this note).

## Spot-check (live)

| Source | USA 2015 | USA 2022 | India 2015 | India 2022 |
|--------|----------|----------|------------|------------|
| `dashboard/viz1_data.js` | **3388** | **3388** | **1001** | **1001** |
| `g1_features_panel.csv` | **3388** | **3388** | **1001** | **1001** |
| `scimago_country_rank_1996_2024.csv` | **3388** | **3388** | **1001** | **1001** |

- Panel flag: `H_Index_Is_Cumulative=True`.
- **Documents** in the same SJR year files *do* change (USA 2015 Docs=730268 → 2022=751197; India 145097 → 286865). Only **H index** is identical across years.

Vault proof: all **243** countries in `02_scimago_country/scimago_country_rank_1996_2024.csv` have a **single** H value across 1996–2024 year files. MANIFEST already notes USA H=3388 “cumulative; identical across year files.”

## What the old “changing H” was

**Not** real yearly SCImago Country Rank H.

It was **G2 tap fiction** in legacy `CS661 Project/app.js` / old `g2.js`:

```js
const dy = year - 1999;
const hGrown = Math.round(match.h + dy * 2);  // USA base h=1279 → ~1325 in 2022
```

| Place | USA ~2022 | India ~2022 |
|-------|-----------|-------------|
| Invented G2 sidebar | ≈1325 (`1279 + 2×23`) | ≈306 (`260 + 2×23`) |
| Live SCImago stock (G1) | **3388** | **1001** |
| Quarantined yearless stub | **53** | **27** |

Separate bug (also fixed): yearless stub scale in `sjr_country_metrics` / master — wrong magnitude, still **not** year-varying.

Docs: `RIVER_PIPELINE_REPORT.md`, `RIVER_TO_POOL_FIX.md`, `RIVER_OWNERS.md`.

## Can we put “yearly H” in the river honestly?

### Option A — Re-read SCImago year XLS (already done)

- Vault has `scimago_country_rank_YYYY.xls` for **1996–2024**.
- **Does not help for H:** SCImago’s Country Rank export repeats the same **lifetime / cumulative** H in every year slice.
- Useful for year-varying **Documents / Citations / Rank**, not for animating H.

### Option B — OpenAlex “country H”

- OpenAlex exposes H-like metrics mainly at **author / institution** level, not a standard SCImago-style **country H** series.
- Computing country H yourself = aggregate all works + citations with an explicit window (e.g. papers ≤ Y, cites by cutoff T) → large API/dump job, new metric definition, **not** drop-in “SCImago H by year.”
- Do **not** slap OpenAlex totals onto G1 and call them H.

### Option C — Honest product choices (recommended framing)

1. **Keep flat stock H** (current): label tooltip/credit as *country quality stock (cumulative SCImago H)* — animation moves on GDP/GERD/docs/UMAP, not H size.
2. **Animate something that truly varies:** bubble size already uses year-varying docs; optional second encoding from SJR Documents / citations-per-doc.
3. **Only if product needs rising H:** define and compute a **windowed country H** (new river, new owner row, new credit text) — multi-day data engineering, not a panel join.

## Rebuild cost summary

| Goal | Effort | Honest? |
|------|--------|---------|
| “Make H move like before” via `base+2*dy` | Minutes | **No** — forbidden fiction |
| Expect yearly SJR XLS to yield rising H | 0 (already merged) | **No** — source is cumulative |
| Label H as stock + keep flat | Small TAP copy | **Yes** |
| True year-varying country H (custom window) | Large (OpenAlex/WoS pipeline + definitions) | **Yes**, if documented as *our* metric |

**Bottom line:** Purana yearly change **fake tha** (G2 `h + 2×(year−1999)`). Ab flat hai kyunki **SCImago Country Rank H itself is cumulative** in every year file we have — not because we forgot to join years.

---

## Implemented (2026-07-12): custom OpenAlex cohort H

See **[`G1_CUSTOM_YEARLY_H.md`](G1_CUSTOM_YEARLY_H.md)** — calendar-year cohort H (W=1) from OpenAlex works, labeled honestly (not SCImago). River: `READY_FOR_TEAM/country_year_h_openalex_cohort.csv`. Panel keeps `H_Index_SCImago` for audit; display/UMAP/G2 use yearly when present.

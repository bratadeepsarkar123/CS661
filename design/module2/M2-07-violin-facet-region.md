# M2-07 — Violin Facet Region

## Intent
**Geographic quality lens**: violins (mirrored KDE) of country-level Q1 share (or Q1/Q4 ratio) **faceted by world region** (7 regions from `data.js`). Shows whether quality shift is uniform or region-specific — e.g., Europe stable Q1 vs South Asia Q4 surge.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Regional Quality Mix         [⛶]   │
├─────────────────────────────────────┤
│ NA  ()   EU  ><   APAC ()           │
│ 3 violins: NA · EU · South Asia     │
│ x: Q1 share %  ·  y: density        │
├─────────────────────────────────────┤
│ Year: 2024 (fixed in overview)      │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year 1996 ────●──── 2024]  Metric: Q1%|Q1/Q4 ratio ▾     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  2×4 or 3×3 grid of violins, one per region (7 panels) │
│  Each violin: distribution of country values in region   │
│  Median line white 1px; IQR box `#475569` fill 0.3       │
│  Optional: overlay 1996 median as tick mark               │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: region | n_countries | median | p25 | p75       │
├──────────────────────────────────────────────────────────┤
│ *Synthetic demo; SCImago + REGIONS map from data.js      │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Violin fill | Region color from `REGIONS` at 0.35 opacity |
| Stroke | Region color 1px solid |
| Median | `#e2e8f0` 1.5px horizontal |
| Shared x-axis | 0–100% Q1 share (fullscreen bottom only) |
| Overview | 3 regions: North America, Europe, South Asia |

## Interaction (Shneiderman)
1. **Overview:** 2024 snapshot, 3 facets
2. **Zoom/filter:** year slider updates all violins
3. **Details-on-demand:** click facet → list countries in region + strip plot
4. **Compare:** toggle 1996 median ghost on each violin

## Data bindings
- ETL: join SCImago country tier % with region lookup (ISO → region)
- JSON schema: `{ years: [{ year, regions: [{ name, countries: [{ iso, q1_pct, ratio }], stats }] }] }`
- Target: `module2_region_violin.json`
- Placeholder: bootstrap from 18 `COUNTRIES` + `REGIONS` with synthetic Q1%

## Lecture alignment
- **7±2:** Seven region facets = category limit; one year control
- **Distribution honesty (L10):** Violin shows spread, not just mean
- **Geographic encoding (L15):** Region colors consistent with Module 1 scatter

## Risks
- Small regions (Oceania) have n=1–2 — show strip plot fallback + footnote
- Violin bandwidth per region with n<5 misleading — min n=3 to draw

## Implementation effort
Medium — violin KDE per region; region join in ETL

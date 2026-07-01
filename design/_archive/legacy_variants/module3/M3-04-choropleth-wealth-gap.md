# M3-04 — Choropleth Wealth Gap

## Intent
**World choropleth** (not India institutional map): color = ratio of R&D spend rank to Q1 output rank — red = under-performing wealth, blue = over-performing.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Wealth Gap Map               [⛶]   │
├─────────────────────────────────────┤
│ [Simplified world silhouettes]      │
│ diverging fill: spend rank − out rank │
│ 3 legend ticks: Under · Parity · Over│
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Projection: Natural Earth  Color ▾             │
├──────────────────────────────────────────────────────────┤
│ d3 geoPath world countries                               │
│ Hover country → tooltip ranks + raw metrics              │
│ Click country → focus fill + sidebar + dim others 40%    │
├──────────────────────────────────────────────────────────┤
│ Footnote: rank-based index; not causal; missing = grey   │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Under-perform | `#f97316` |
| Parity | `#334155` |
| Over-perform | `#38bdf8` |
| No data | `#1e293b` |
| Stroke | `#0f172a` 0.5px |

## Interaction
1. Overview: static map, no pan
2. Fullscreen: pan/zoom; click focus+context
3. Year slider recolors countries
4. Optional: switch to Gini choropleth layer

## Data bindings
- Natural Earth topojson + merged rank gap metric
- Pre-compute ranks in ETL per year
- JSON: `{ year, countries: [{ iso, gap, spend_rank, out_rank }] }`

## Lecture alignment
- **Geographic position (L2):** Used for world patterns, not India HE network
- **7±2:** Diverging 3-class legend on overview
- **Tufte:** No 3D globe; equal-area projection note

## Risks
- Rank index hard to interpret — strong tooltip
- Distinct from Module 5 — world scale, country polygons only

## Implementation effort
Medium (topojson + d3-geo)

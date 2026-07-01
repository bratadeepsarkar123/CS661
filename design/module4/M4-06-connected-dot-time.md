# M4-06 — Connected Dot Time

## Intent
**Temporal premium shift**: dumbbell pairs connecting **1996 vs 2024** (or configurable anchors) for domestic and international cites separately — four dots per country connected across time. Shows whether collaboration premium widened over decades.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Premium Over Time            [⛶]   │
├─────────────────────────────────────┤
│ USA  dom ●───●  intl ●────●         │
│      1996    2024                   │
│ IND  dom ●──●   intl ●────●         │
├─────────────────────────────────────┤
│ 2 countries · dual time dumbbells   │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Pair: [1996 vs 2024 ▾]  Metric: [dom|intl|both]  Sort ▾  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Per country row:                                        │
│    Domestic: dot_1996 ──connector── dot_2024 (indigo)    │
│    Intl:     dot_1996 ──connector── dot_2024 (cyan)      │
│  Or simplified: two dumbbells side-by-side per era       │
│  Hover → all four values + gain delta per era            │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: country | dom_96 | dom_24 | intl_96 | intl_24   │
├──────────────────────────────────────────────────────────┤
│ *Synthetic: extrapolate COLLAB_DATA with year multipliers  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| 1996 dots | Outlined ring (hollow) r=5px |
| 2024 dots | Filled r=5px |
| Domestic | `#6366f1`; International `#22d3ee` |
| Time connector | `#64748b` 2px solid between eras |
| Overview | USA + IND only |

## Interaction (Shneiderman)
1. **Overview:** 2 countries, fixed pair years
2. **Zoom/filter:** change anchor years; toggle dom/intl/both display
3. **Details-on-demand:** click row → sidebar timeline
4. **Sort:** by premium widening (gain_24 − gain_96)

## Data bindings
- M4-01 schema with full year range 1996–2024 per country
- ETL: compute mean cites domestic/intl for each year (heavy OpenAlex)
- Placeholder: scale 2024 `COLLAB_DATA` backward with decay factor per year

## Lecture alignment
- **Temporal honesty (L10):** Hollow vs filled distinguishes era encoding
- **7±2:** Two metrics (dom/intl) × two years — use toggles to reduce
- **Narrative:** Pairs with M2-05 dumbbell year pattern across modules

## Risks
- Four dots per row dense — default intl-only time pair in overview
- Synthetic back-projection misleading — footnote until real ETL

## Implementation effort
Medium–high — multi-year ETL + dual dumbbell layout

# M3-06 — Violin Income Tier

## Intent
**Distribution by wealth class**: violins of Q1 publication share (or cites/paper) across World Bank income groups — shows spread, not just averages.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Quality by Income Tier       [⛶]   │
├─────────────────────────────────────┤
│ Low  ╭──╮  Mid ╭─╮  High ╭───╮      │
│      │  │      │ │      │   │      │
│ violin silhouettes × 3 groups       │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Metric: Q1% | cites/paper  [Show boxplot ▾]    │
├──────────────────────────────────────────────────────────┤
│ 5 income groups (max) violins horizontal                 │
│ Overlay median tick; optional boxplot inner              │
│ Hover → KDE tooltip; click group → country strip plot    │
├──────────────────────────────────────────────────────────┤
│ KDE bins pre-computed (L15)                              │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Violin fill | `#6366f1` 30% |
| Stroke | `#94a3b8` |
| Median | white 2px tick |
| Selected group | `#38bdf8` fill 50%

## Interaction
1. Overview: 3 grouped violins (collapse lower tiers)
2. Fullscreen: five WB groups; click → strip plot of countries
3. Hover density path for percentile read
4. Sync year with global slider

## Data bindings
- Country-level Q1% tagged with WB income group
- ETL KDE per group-year → bin arrays
- JSON: `{ year, groups: [{ id, bins: [...], countries: [...] }] }`

## Lecture alignment
- **Distribution summarization (L15):** KDE bins in JSON
- **Compare distributions (L10):** Side-by-side violins
- **7±2:** Five groups max

## Risks
- Small groups → noisy KDE — min n countries per group
- Violin less familiar — median tick mandatory

## Implementation effort
Medium

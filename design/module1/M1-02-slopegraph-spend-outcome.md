# M1-02 — Slopegraph Spend→Outcome

## Intent
Show **long-run morphing** of the spend/outcome relationship: each country as two linked slopes (GERD % GDP and citations per paper) from 1996 baseline to selected year — narrative of convergence and breakaway.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Spend → Outcome Slopes       [⛶]   │
├─────────────────────────────────────┤
│ 1996 ════════════════════ 2024      │
│   ●───────●  USA (both up)          │
│   ●───●      IND (spend flat, out up)│
│  (8 countries, grey others)         │
├─────────────────────────────────────┤
│ Insight: "Output rose faster than   │
│ spend for South Asia since 2010"    │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [End year ●]  Compare axis: Spend | Output | Both        │
├──────────────────────────────────────────────────────────┤
│ Left axis 1996          Right axis 2024                  │
│   Spend lane (top half)                                  │
│   ●━━━━━━━━━━━━━━━━━━━━●  per country                    │
│   Output lane (bottom half)                              │
│   ●━━━━━━━━━━━━━━━━━━━━●                                 │
├──────────────────────────────────────────────────────────┤
│ Click country → both lanes highlight; peers dim 25%      │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Lines | `#64748b` default; selected `#3b82f6`; improving slope `#22c55e` |
| Nodes | 4px circles at endpoints; label right column only (top 20) |
| Lanes | Subtle `#1e293b` band separators |
| Overview | Max 8 labeled countries (7±2 + 1 spare) |

## Interaction
1. Overview: fixed end-year 2024, 8 preset countries (USA, CHN, IND, DEU, BRA, KOR, ZAF, GBR)
2. Fullscreen: country search adds to highlight set (max 12 lines)
3. Hover: tooltip with absolute delta spend % and cites/paper delta
4. Toggle: single combined slope vs dual-lane layout

## Data bindings
- UNESCO UIS + SCImago: extract 1996 and each year through 2024
- JSON: `{ baseline_year: 1996, snapshots: { "2024": [...] } }`
- Synthetic `data.js` lacks time series — ETL required

## Lecture alignment
- **Focus+context (L2/L10):** Highlight one country’s pair of slopes
- **Tufte (L10):** Direct labels on right; no redundant legend box
- **Trend encoding (L10):** Slope angle = rate of change (honest 1:1 scale per lane)

## Risks
- Dual-lane layout doubles vertical space — overview must stay single-lane
- Countries entering dataset mid-series need dashed “partial” endpoints

## Implementation effort
Medium

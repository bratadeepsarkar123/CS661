# M4-02 — Lollipop Gain Sorted

## Intent
**Gain-first story**: single dot per country at **citation gain** (intl − domestic) on horizontal axis, sorted descending. Drops domestic/intl dual-dot encoding for clarity when message is purely "who benefits most."

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Collaboration Gain           [⛶]   │
├─────────────────────────────────────┤
│ CHE  ────●  +8.8                    │
│ AUS  ───●   +7.9                    │
│ IND  ──●    +6.7                    │
│ x: citation gain (intl − dom)       │
├─────────────────────────────────────┤
│ Top 5 gains only                    │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Region ▾  Show: gain|log gain ▾                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Lollipop chart: stem from 0 to gain value               │
│  Dot r=6px colored by region; label at dot               │
│  Reference line at global median gain (dashed)             │
│  Hover → dom, intl, gain tooltip                         │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: full metrics for selected country               │
├──────────────────────────────────────────────────────────┤
│ *Synthetic COLLAB_DATA.gain precomputed                  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Stem | `#475569` 1.5px from 0 |
| Dot | Region color from `REGIONS` |
| Median line | `#fbbf24` dashed 1px |
| x-axis | Linear gain; label "Citations gained (intl − dom)" |
| Overview | 5 rows |

## Interaction (Shneiderman)
1. **Overview:** top 5 gains fixed
2. **Zoom/filter:** year; region; log scale toggle for wide spread
3. **Details-on-demand:** click → sidebar with dom/intl breakdown
4. **Brush:** x-axis brush to zoom gain range

## Data bindings
- Derive `gain = intl - domestic` in ETL from M4-01 schema
- Placeholder: `COLLAB_DATA.map(c => c.gain)` in `data.js`

## Lecture alignment
- **Tufte:** One dimension encoded once — no redundant dumbbell when gain suffices
- **7±2:** Minimal controls; region hue ≤7
- **Sorting:** Order by effect size — honest ranking

## Risks
- Hides absolute citation levels — tooltip must show dom/intl
- Negative gain rare — show if present, don't clip axis

## Implementation effort
Low — simpler than full dumbbell; same ETL

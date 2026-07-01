# M2-05 — Dumbbell Year Pairs

## Intent
**Before/after clarity** without full ridgeline: dumbbell chart comparing each country’s **Q1 share vs Q4 share** at anchor years **1996 vs 2024**. Left dot = Q1%, right dot = Q4%, connector shows gap. Sorted by Q4 gain — surfaces who flooded low-tier output.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Q1 vs Q4 Share Shift         [⛶]   │
├─────────────────────────────────────┤
│ USA  ●───────●  1996→2024           │
│ CHN  ●─────────●                    │
│ IND  ●──────────●  Q4 widened       │
│ ● Q1  ● Q4                          │
├─────────────────────────────────────┤
│ Top 5 countries by Q4 Δ               │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Pair: [1996 vs 2024 ▾]  Sort: Q4 Δ|Q1 Δ|name  Region ▾   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Horizontal dumbbells, one row per country (~60 shown)   │
│  Left cluster: 1996 Q1 (indigo) — Q4 (rose)            │
│  Right cluster: 2024 Q1 — Q4                           │
│  Connector: `#64748b` 2px between year pairs             │
│  Hover → country + exact % both years                   │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: country | Q1_96 | Q4_96 | Q1_24 | Q4_24 | ΔQ4   │
├──────────────────────────────────────────────────────────┤
│ *Synthetic demo; SCImago tier %; MIN_DOCS=100            │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Q1 dots | `#6366f1` r=5px |
| Q4 dots | `#fb7185` r=5px |
| Connectors | `#64748b` 2px; year-pair bridge `#475569` dashed |
| Row height | 22px; label `#cbd5e1` 11px left-aligned |
| Overview | Top 5 by Q4 delta only |

## Interaction (Shneiderman)
1. **Overview:** 5 rows, 1996→2024 pair fixed
2. **Zoom/filter:** change anchor years (presets: 1996/2010/2024); region filter
3. **Details-on-demand:** click row → sidebar + highlight
4. **Sort:** toggle Q4 gain vs Q1 gain vs alphabetical

## Data bindings
- ETL: SCImago `%Q1`, `%Q4` per country×year
- JSON schema: `{ pairs: [{ year_a, year_b, countries: [{ iso, q1_a, q4_a, q1_b, q4_b }] }] }`
- Target: `module2_dumbbell_pairs.json`
- Placeholder: synthetic tier % for 18 `COUNTRIES` in `data.js`

## Lecture alignment
- **Graphical integrity (L10):** Dots on common 0–100% x-axis; no dual axes
- **7±2:** One sort, one region filter, one year-pair selector
- **Comparison (L2):** Pair design matches proposal before/after narrative

## Risks
- Many countries → long scroll — default top 30 + search
- Q1+Q4 ≠ 100% (Q2/Q3 omitted) — footnote "pair shows extremes only"

## Implementation effort
Low–medium — D3 dumbbell pattern; lighter than KDE ridgeline

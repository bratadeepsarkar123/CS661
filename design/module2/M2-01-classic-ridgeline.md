# M2-01 — Classic Ridgeline

## Intent
Faithful implementation of proposal §4.2: stacked KDE ridgelines per year showing **global publication quality density**, with Q1 (elite) and Q4 (low-tier) curves overlaid on each row. Answers “How did the world’s journal-quality mix shift from parity toward bimodality?”

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Global Quality Shift         [⛶]   │
├─────────────────────────────────────┤
│ 1996 ═══Q1═══  ═══Q4═══             │
│ 2010 ═══Q1═══    ═Q4═               │
│ 2024 ══Q1══   ═══Q4 flood══         │
│ x: Quality proxy (Q1/Q4 ratio)      │
├─────────────────────────────────────┤
│ Q1 indigo · Q4 rose                 │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year 1996 ────●──── 2024]  Metric: ratio|index ▾       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Ridgeline rows: one band per year (1996–2024, step 2)   │
│  Each row: Q1 fill (indigo) + Q4 fill (rose), overlap OK │
│  Shared x-axis: country-level Q1/Q4 ratio KDE (0–3.0)    │
│  Hover row → year label + median ratio tooltip           │
│  Click row → lock highlight; others 30% opacity            │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: year | median ratio | Q1% global | Q4% global   │
├──────────────────────────────────────────────────────────┤
│ *Synthetic demo; SCImago SJR ETL → module2_ridgeline.json│
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Q1 curve | `#6366f1` fill 0.55, stroke `#818cf8` 1px |
| Q4 curve | `#fb7185` fill 0.55, stroke `#fda4af` 1px |
| Row labels | `#cbd5e1`, left margin, year only (no country names on overview) |
| Axes | `#94a3b8`; x ticks 0, 0.5, 1.0, 2.0, 3.0 |
| Row height | 48px overview; 56px fullscreen; overlap via negative y-offset |

## Interaction (Shneiderman)
1. **Overview:** latest 3 years only; no slider
2. **Zoom/filter:** year range slider; optional MIN_DOCS threshold (100+ papers)
3. **Details-on-demand:** hover row → tooltip; click → sidebar stats
4. **Focus+context:** selected year row full opacity; adjacent rows 60%; rest 25%

## Data bindings
- ETL: SCImago country CSV → per-country Q1/Q4 ratio per year → KDE bins in Python (Lecture 15)
- JSON schema: `{ years: [{ year, kde: [{ x, q1_density, q4_density }], stats: { median_ratio, q1_pct, q4_pct } }] }`
- Target file: `module2_ridgeline.json`
- Placeholder: `DATA.getRidgelineData()` in `dashboard/data.js` (synthetic bell curves 2010–2025)

## Lecture alignment
- **Graphical integrity (L10):** KDE pre-computed; area = density not volume — footnote clarifies
- **7±2 (L2):** Two hues (Q1/Q4), one year control, one sidebar
- **Overview→detail (L2):** Grid shows shape shift only; full year range in fullscreen

## Risks
- KDE bandwidth sensitivity — document kernel width in ETL; show histogram fallback toggle
- 240 countries × 29 years heavy in browser — ship pre-binned JSON only

## Implementation effort
Medium — D3 area + band scales; ETL + KDE pipeline is the heavy lift

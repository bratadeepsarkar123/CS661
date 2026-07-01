# M2-06 — Dot Plot Growth CAGR

## Intent
Static **growth lens**: dot plot of compound annual growth rate (CAGR) for publications 2000–2024 — who accelerated vs plateaued.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Publication Growth CAGR      [⛶]   │
├─────────────────────────────────────┤
│ CHN ●——————————→ 12%                │
│ IND ●——————→ 8%                     │
│ USA ●——→ 2%                         │
│ (6 countries, arrow length ∝ CAGR)  │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Window: 2000–24 ▾  Region filter  Sort CAGR ▾            │
├──────────────────────────────────────────────────────────┤
│ Vertical dot plot: y=country, x=CAGR %                   │
│ Arrow from 0 to dot; color region                        │
│ Reference line at global median CAGR                     │
├──────────────────────────────────────────────────────────┤
│ Click dot → inset line chart 1996–2024 raw volume        │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Dot | 6px filled circle |
| Arrow shaft | `#64748b` 2px |
| Positive CAGR | `#22c55e`; negative `#f97316` |
| Median line | `#475569` dashed |

## Interaction
1. Overview: top 3 positive + 3 mid CAGR
2. Fullscreen: sort/filter; click → inset line chart
3. Window selector recalculates from pre-computed JSON slices
4. Hover: show start/end counts used in CAGR

## Data bindings
- SCImago/OpenAlex yearly totals; CAGR computed in ETL
- JSON: `{ window, countries: [{ iso, cagr, series: [...] }] }`

## Lecture alignment
- **Graphical integrity:** CAGR formula in footnote; exclude years with zero start
- **Comparative viz (L10):** Shared x-axis CAGR across countries
- **Details-on-demand:** Inset line on click only

## Risks
- CAGR sensitive to start year — offer 1996 and 2010 windows
- Small countries volatile — min start pubs threshold

## Implementation effort
Low–medium

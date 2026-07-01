# M1-01 — Scatter Efficiency Frontier

## Intent
Answer “Which countries convert HE/R&D spend into measurable research outcomes?” with a single scatter + optional regression frontier — the core **expenditure vs outcomes** paradox from the project introduction.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ HE Spend vs Outcomes         [⛶]   │
├─────────────────────────────────────┤
│  ● USA   ● CHN                      │
│       ╲  frontier band              │
│  ● IND ● BRA                        │
│  x: GERD % GDP   y: cites / $1M GERD│
├─────────────────────────────────────┤
│ 3 labels: Over-perform · On-line ·  │
│ Under-perform (vs OLS)              │
├─────────────────────────────────────┤
│ *Synthetic demo; UNESCO+SCImago ETL │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year 1996 ────●──── 2024]  Region ▾  Metric ▾  [Search] │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Scatter ~60 countries, bubble area ∝ total publications│
│   Frontier: dashed OLS + 95% band (pre-computed coeffs)  │
│   Selected: white ring + sidebar metric table            │
│   Others: 35% opacity                                    │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: Country | GERD% | Pubs | Cites | Efficiency z   │
├──────────────────────────────────────────────────────────┤
│ Footnote: PPP-normalized GERD optional; missing = hollow │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Points | Region palette (max 6 regions, 7±2) from `data.js` REGIONS |
| Bubble area | `√(publications)` — Tufte lie factor |
| Frontier | `#64748b` dashed line; band `#334155` fill 0.15 |
| Over-perform | `#22c55e` stroke hint on label only (not fill flood) |
| Axes | `#94a3b8`, no grid on overview; light grid fullscreen only |

## Interaction (Shneiderman)
1. **Overview:** static latest year, no country labels (max 3 story callouts)
2. **Zoom/filter:** year slider + region dropdown
3. **Details-on-demand:** click/hover country → sidebar + highlight
4. **Focus+context:** selected country full opacity; others dimmed (L10 Munzner Ch.14)

## Data bindings
- ETL: join UNESCO `EXPGDP.TOT` + SCImago country-year metrics + WB GDP
- JSON schema: `{ year, countries: [{ iso, gerd_pct_gdp, pubs, cites, gdp_ppp, region, efficiency_z }] }`
- Replace synthetic `COUNTRIES` in `dashboard/data.js` when pipeline ready
- Pre-compute OLS coefficients per year in Python (not in browser)

## Lecture alignment
- **Graphical integrity (L10):** √ area for volume; footnote for missing GERD
- **7±2 (L2/L10):** One scatter, one year control, one region filter, one sidebar
- **Overview→detail (L2):** Grid shows frontier shape only; labels in fullscreen

## Risks
- GERD missing for ~30 countries some years — hollow points + exclude from frontier fit
- Comparing nominal vs PPP spend — toggle must be explicit in footnote

## Implementation effort
Medium — standard D3 scatter; ETL join is the heavy lift

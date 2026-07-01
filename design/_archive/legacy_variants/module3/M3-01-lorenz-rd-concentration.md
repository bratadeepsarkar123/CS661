# M3-01 — Lorenz R&D Concentration

## Intent
Single **Lorenz curve** answering “How unequal is global R&D ownership?” — cumulative population vs cumulative GERD share with Gini coefficient annotation.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ R&D Concentration            [⛶]   │
├─────────────────────────────────────┤
│ 1.0 ┤        ╱ equality            │
│     │      ╱                       │
│     │    ╱ Lorenz curve            │
│ 0.0 └────────────                  │
│ Gini ≈ 0.82 (2024)                 │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Compare years: overlay 1996 vs 2024           │
├──────────────────────────────────────────────────────────┤
│ Lorenz curve + diagonal equality line                    │
│ Hover point → tooltip: country at that cumulative step   │
│ Click to pin top 5 contributors at elbow                 │
├──────────────────────────────────────────────────────────┤
│ Sidebar: Gini table by year; top 10 cumulative share     │
│ Footnote: UNESCO UIS GERD; population WB                 │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Lorenz | `#38bdf8` 2px |
| Equality | `#475569` dashed |
| Fill between | `#1e3a5f` 15% opacity |
| Second year | `#f97316` if overlay |

## Interaction
1. Overview: latest year Gini only
2. Fullscreen: year slider; optional dual overlay
3. Hover along curve for country reveal
4. Focus+context: pin highlights segment; rest dim

## Data bindings
- UNESCO UIS GERD by country + WB population
- Sort countries by GERD; compute cumulative shares in ETL
- JSON: `{ year, gini, points: [{ pop_cum, gerd_cum, iso? }] }`

## Lecture alignment
- **Graphical integrity (Tufte):** Axes 0–1 labeled; Gini formula footnote
- **7±2:** One curve + one stat + one footnote on overview
- **Distribution (L15):** Pre-computed curve points

## Risks
- Population vs researcher denominator changes interpretation — pick one, document
- Missing GERD countries excluded — note n in footnote

## Implementation effort
Low–medium

# M1-03 — Small Multiples Lollipop

## Intent
Facet **~12 countries** in a grid of mini lollipop charts: horizontal bar = GERD % GDP, dot at tip = citations per publication — instant side-by-side efficiency comparison without overlap clutter.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ HE Efficiency Facets         [⛶]   │
├─────────────────────────────────────┤
│ [USA] [CHN] [IND] [DEU]             │
│  ████●   ██●   █●    ███●           │
│ [JPN] [KOR] [BRA] [GBR]             │
│  each: bar=spend  dot=outcome       │
├─────────────────────────────────────┤
│ Avg GERD 1.8% · Global median dot   │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Sort: Spend ▾ | Outcome | Region   [Year slider]         │
├──────────────────────────────────────────────────────────┤
│ 4×4 grid (16 facets) → scroll-free pagination (2 pages)  │
│ ┌──────┐ ┌──────┐   Each facet 120×80px                    │
│ │ IND  │ │ BRA  │   Bar max width normalized to global max │
│ │ ██●  │ │ █●   │   Dot color = above/below median outcome │
│ └──────┘ └──────┘                                         │
├──────────────────────────────────────────────────────────┤
│ Click facet → expands to hero lollipop + 5-peer comparison │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Bar | `#475569` fill |
| Dot | `#38bdf8` if outcome ≥ median else `#f97316` |
| Facet border | `#1e293b` 1px |
| Hero expand | 3× size with annotated values |

## Interaction
1. Overview: 8 facets, latest year
2. Fullscreen: sort reorders grid; click → hero + peer strip
3. Region filter reduces facet set
4. Brush on hero bar scrubs year locally (optional link to global year)

## Data bindings
- Same join as M1-01; add `global_median_cites_per_paper` per year in JSON
- Facet list: top 16 by publications or user region filter

## Lecture alignment
- **Small multiples (L10):** Same scale across facets — critical for comparison
- **7±2:** Overview shows 8 facets max
- **Integrity:** Shared x-scale documented in footnote

## Risks
- 16 facets still dense on 1080p — pagination or region filter required
- Normalizing bars to global max may shrink small economies — log toggle?

## Implementation effort
Low–medium

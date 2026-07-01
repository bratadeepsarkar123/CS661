# M1-04 — Parallel Coordinates HE

## Intent
Expose **multi-indicator country profiles** (GERD %, researchers/million, publications, citations, h-index) as brushable parallel axes — aligns with proposal t-SNE story but stays interpretable (no DR black box in UI).

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ HE Indicator Profiles        [⛶]   │
├─────────────────────────────────────┤
│ 5 vertical axes, 6 polylines        │
│ (one per region aggregate)            │
│ thick line = region mean              │
├─────────────────────────────────────┤
│ Brush one axis in fullscreen →      │
│ filter others (linked)              │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Normalize: MinMax | Z-score                    │
├──────────────────────────────────────────────────────────┤
│  GERD% — Researchers — Pubs — Cites — h-index            │
│    │        │          │       │        │                │
│    ╲────────╲─────────╲──────╲────────╲  ~50 countries   │
│    │        │          │       │        │                │
│  [brush handles on each axis]                            │
├──────────────────────────────────────────────────────────┤
│ Selected: 12 countries highlighted; rest 15% opacity       │
│ Sidebar: table of brushed set                            │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Lines | Region color, 1px default; brushed 2.5px white |
| Axes | `#64748b`; tick labels 10px |
| Brush | `#3b82f6` 20% fill |
| Overview | 6 regional mean polylines only |

## Interaction
1. Overview: regional aggregates (6 lines)
2. Fullscreen: axis brush filters country set (linked highlighting)
3. Click line → pin country to top z-order + sidebar
4. Double-click axis → reset brush

## Data bindings
- UNESCO UIS + WB + SCImago merged wide table
- Pre-normalize z-scores in ETL per year
- JSON: `{ axes: [...], countries: [{ id, values: [5 floats], region }] }`

## Lecture alignment
- **High-dim preprocessing (L2):** Normalize before display; footnote axes
- **Linked views (L10):** Brush = cross-filter within panel
- **7±2:** Five axes = upper working-memory bound

## Risks
- Hairball with 180 lines — cap at 50 countries or require brush to show any
- Parallel coords order affects perception — allow axis reorder in fullscreen only

## Implementation effort
Medium–high (brush logic)

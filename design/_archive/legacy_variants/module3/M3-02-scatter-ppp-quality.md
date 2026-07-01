# M3-02 — Scatter PPP vs Quality

## Intent
**Wealth paradox scatter**: x = GDP per capita (PPP), y = Q1 publication share — exposes rich countries with mediocre quality mix and inverse surprises.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Wealth vs Quality            [⛶]   │
├─────────────────────────────────────┤
│ Q1%                                 │
│   ● USA  ● LUX                      │
│        ● IND                        │
│ ─────────── PPP GDP                 │
│ 3 zones: High $ · Mid · Low $       │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Size: population | pubs  Region ▾  [Search]    │
├──────────────────────────────────────────────────────────┤
│ ~60 countries; bubble area ∝ √(population)               │
│ Quadrant guides at median PPP and median Q1% (dashed)    │
│ Click country → sidebar: PPP, Q1%, Gini if available     │
├──────────────────────────────────────────────────────────┤
│ Selected full opacity; others 30%                        │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Points | Region colors (6 max) |
| Quadrants | `#334155` 0.3 opacity bands (optional toggle off default) |
| Median lines | `#64748b` dashed |
| Labels | Overview none; fullscreen top 12 by pubs

## Interaction
1. Overview: 12 dots no labels, 3 zone text labels
2. Fullscreen: search, region filter, click focus
3. Hover tooltip with PPP and Q1 count
4. Year slider animates point positions

## Data bindings
- World Bank `NY.GDP.PCAP.PP.KD` + SCImago Q1/(Q1..Q4)
- JSON per year arrays
- Synthetic `data.js` has gdp2010 — replace with PPP series

## Lecture alignment
- **Planar position (L2):** Strongest encodings on x,y
- **Lie factor (Tufte):** √ area for population
- **Focus+context (L10):** Selection dims peers

## Risks
- Q1 share noisy for small publishers — min pub threshold
- Luxembourg-style outliers compress mid — log x-axis toggle

## Implementation effort
Medium

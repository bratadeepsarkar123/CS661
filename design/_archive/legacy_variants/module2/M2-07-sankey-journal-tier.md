# M2-07 — Sankey Journal Tier

## Intent
**Flow diagram**: countries (left) → Q1/Q2/Q3/Q4 tiers (right) sized by publication volume — production funnel without geographic map.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Pub Flow by Tier             [⛶]   │
├─────────────────────────────────────┤
│ USA ═══╗                            │
│ CHN ═══╬══► Q1 Q2 Q3 Q4              │
│ IND ═══╝   (aggregated ribbons)     │
├─────────────────────────────────────┤
│ Global Q4 share ↑ since 2010        │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Countries: top 12 ▾  Min flow: 1%              │
├──────────────────────────────────────────────────────────┤
│ d3-sankey layout                                         │
│ Left nodes: countries; right nodes: 4 tiers              │
│ Hover ribbon → highlight path + count tooltip            │
│ Click country → isolate incoming ribbons; dim others     │
├──────────────────────────────────────────────────────────┤
│ SCImago Q classification footnote                        │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Ribbons | Tier color at destination node |
| Country nodes | `#94a3b8` bars |
| Tier nodes | Q1 `#3b82f6` … Q4 `#475569` |
| Opacity | 0.6 default; 0.95 focused path |

## Interaction
1. Overview: 3-country aggregate flows
2. Fullscreen: country filter; click focus path
3. Year transition morphs ribbon widths (interpolate)
4. Toggle absolute vs % of country output

## Data bindings
- SCImago country-year tier counts
- Sankey links: `{ source: iso, target: tier, value }`
- Pre-layout optional but prefer client d3-sankey for flexibility

## Lecture alignment
- **Flow integrity:** Ribbon width = count (linear)
- **7±2:** 4 tier targets + ≤12 sources
- **Focus+context:** Path isolation on click

## Risks
- Ribbon crossing clutter — limit to top 12 countries
- Sankey layout instability — cache node positions per year

## Implementation effort
Medium–high

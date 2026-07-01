# M4-06 — Arc World Flows

## Intent
**Great-circle arc map** on muted world basemap: origin→host student flows as arcs — geographic drama distinct from Module 5 India node-link institutional map.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ World Mobility Arcs          [⛶]   │
├─────────────────────────────────────┤
│ [dark world outline]                │
│  CHN ~~~~> USA                      │
│  IND ~~~~> GBR                      │
│ 3 arcs, width ∝ flow                │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Top flows: 15 ▾  [Origin filter ▾]             │
├──────────────────────────────────────────────────────────┤
│ Natural Earth basemap `#1e293b` fill                     │
│ Arc height ∝ flow; color by origin region                │
│ Hover arc → tooltip; click → lock arc + dim others       │
│ Click country dot → all arcs incident highlighted        │
├──────────────────────────────────────────────────────────┤
│ Footnote: arc count capped; not all bilateral pairs shown  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Basemap | `#1e293b` land, `#0f172a` ocean |
| Arcs | Region color, 1–4px width linear scale |
| Country dots | 3px at endpoints on hover |
| Locked arc | white 1px glow stroke (subtle)

## Interaction
1. Overview: top 3 flows only
2. Fullscreen: filters; click focus arc
3. Year transition retargets arcs
4. Pan/zoom map (d3 zoom)

## Data bindings
- Bilateral flow matrix top-N pairs per year
- Country centroids from Natural Earth
- JSON: `{ year, flows: [{ from_iso, to_iso, value, from_latlon, to_latlon }] }`

## Lecture alignment
- **Position (L2):** Geo used for mobility, not institutional network
- **7±2:** Overview 3 arcs
- **Chartjunk:** No animated particles on overview

## Risks
- Arc overlap clutter — top-N cap + origin filter
- Distinct from M5: no institution nodes/edges/tiers

## Implementation effort
Medium–high

# M4-08 — Stacked Brain Drain Index

## Intent
**Regional aggregate**: stacked bars of net mobility index (inbound − outbound per capita) by world region over time — macro brain drain/gain without bilateral detail.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Net Mobility by Region       [⛶]   │
├─────────────────────────────────────┤
│ ▓▓ Asia                               │
│ ▓▓ Europe                             │
│ ░░ Africa                             │
│ stacked positive/negative per region  │
│ single year 2024 snapshot             │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Normalize: per 100k pop | absolute  ▶ Play     │
├──────────────────────────────────────────────────────────┤
│ Horizontal stacked bars per region OR small multiples     │
│ Positive segment = net importer; negative = net exporter  │
│ Hover segment → countries in region contributing          │
├──────────────────────────────────────────────────────────┤
│ Click region → drill to country-level stacked bar         │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Net positive | `#22c55e` |
| Net negative | `#f97316` |
| Zero line | `#475569` |
| Drill-down | fade non-selected regions 30%

## Interaction
1. Overview: 5 regions one year
2. Fullscreen: play years; click drill to countries
3. Normalize toggle per capita
4. Esc drill-up from country to region

## Data bindings
- Aggregate UIS in/out by region; population from WB for per capita
- JSON: `{ years: [...], regions: [{ id, net, countries: [...] }] }`
- Index = (in - out) / population * 100k

## Lecture alignment
- **7±2:** Five regions on overview
- **Integrity:** Per capita footnote; missing pop excludes country
- **Overview→detail:** Drill hierarchy

## Risks
- Regional aggregation masks India→USA story — drill-down required
- Per capita sensitive to population estimates

## Implementation effort
Medium

# M4-04 — Stream Inbound Share

## Intent
Track **% of tertiary students who are internationally mobile** in major host nations over time — policy-relevant “internationalization” trend.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Inbound Share Trend          [⛶]   │
├─────────────────────────────────────┤
│ 25% ┤     ╱ USA                     │
│     │   ╱                           │
│ 10% ┤ ╱ AU                           │
│     └──────── years                 │
│ 3 countries max lines               │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Countries multi-select (max 8)  Metric ▾       │
├──────────────────────────────────────────────────────────┤
│ Line chart: y = mobile / tertiary enrollment %           │
│ Hover vertical rule + multi-tooltip                      │
│ Click line → focus; others 25% opacity                 │
├──────────────────────────────────────────────────────────┤
│ Toggle: inbound share | outbound share | net ratio       │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Lines | 8-color restrained palette |
| Axis | `#64748b`; y capped 0–40% unless outlier |
| Highlight | 3px stroke white outline |
| Grid | horizontal ticks only fullscreen

## Interaction
1. Overview: 3 preset hosts
2. Fullscreen: country picker
3. Metric toggle recolors same selection
4. Global year slider = vertical cursor

## Data bindings
- UIS `MOBILE.IN` / `ENR.TER` per host country
- JSON time series per country
- Missing years = gap in line (not zero)

## Lecture alignment
- **Time series integrity:** Break lines for missing
- **7±2:** 3 lines overview
- **Tufte:** Direct line labels at end

## Risks
- Enrollment denominator revisions — UIS vintage footnote
- Small countries volatile percentages — smooth optional off

## Implementation effort
Low–medium

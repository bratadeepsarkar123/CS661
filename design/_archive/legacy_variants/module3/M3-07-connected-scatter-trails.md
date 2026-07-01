# M3-07 — Connected Scatter Trails

## Intent
**Gapminder-style** animated scatter: PPP GDP vs total publications with country trails 1996–2024 — motion reveals inequality dynamics.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Wealth–Output Trails         [⛶]   │
├─────────────────────────────────────┤
│ pubs                                │
│   ╱ trails CHN, IND                 │
│  ● USA                              │
│ ─────── PPP GDP                     │
│ ▶ static end frame                  │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ▶ Play  [Year ●]  Trails: 8 countries ▾  [Search]       │
├──────────────────────────────────────────────────────────┤
│ Scatter x=log PPP, y=log pubs                            │
│ Trails fade 1996→current; head = current year dot        │
│ Bubble area ∝ population (optional off default)          │
├──────────────────────────────────────────────────────────┤
│ Click country → isolate trail; others ghost 10%          │
│ Sidebar: start vs end values + CAGR                      │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Trail | Region color, opacity gradient old→new |
| Head dot | white 1px stroke |
| Playhead | vertical year label |
| Background | `#0f172a`, axes `#64748b`

## Interaction
1. Play animates year; pause freezes
2. Scrub year slider moves head along trails
3. Click focus trail; search adds country
4. Overview: no play, 6 trails max

## Data bindings
- WB PPP + SCImago pubs time series per country
- JSON: `{ countries: [{ iso, series: [{ year, ppp, pubs, pop }] }] }`
- Log transforms pre-applied optional fields

## Lecture alignment
- **Temporal trajectory (L2/L10):** Trails show path not just point
- **Focus+context:** Isolate one trail
- **Tufte:** sqrt pop scaling if enabled

## Risks
- Overplotting — default 8 trails; user adds more
- Log axes need footnote for general audience

## Implementation effort
Medium–high (animation)

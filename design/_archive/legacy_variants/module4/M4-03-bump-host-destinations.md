# M4-03 — Bump Host Destinations

## Intent
**Rank animation** of top host countries by total inbound international students — which destinations rise/fall in the global mobility market.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Host Country Rankings        [⛶]   │
├─────────────────────────────────────┤
│ 1 ─── USA                           │
│ 3 ─── GBR ↑                         │
│ 5 ─── AUS ↓                         │
│ (top 5 rank lines, end labels)      │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ▶ Play  [Year scrub ●]  Show top 10 ▾                    │
├──────────────────────────────────────────────────────────┤
│ Bump chart ranks 1–15 over 1996–2024                     │
│ Click country → trail highlight + inbound count sidebar   │
├──────────────────────────────────────────────────────────┤
│ Footnote: UNESCO UIS MOBILE.IN aggregation               │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Lines | Categorical palette 10 colors |
| Rank axis | inverted 1 at top |
| Labels | country name at line head |
| Ghost trail | selected country full history faint line

## Interaction
1. Play rank race (fullscreen)
2. Scrub year
3. Click focus country
4. Overview static 2024 ranks

## Data bindings
- UIS inbound mobile students by host country-year
- Pre-ranked frames JSON like M1-05 bump pattern

## Lecture alignment
- **Temporal rank (L10):** Value in tooltip not line slope confusion
- **7±2:** Overview 5 lines
- **Focus+context:** Trail isolate

## Risks
- Definition changes in UIS mobile student — document indicator code
- Brexit/US policy shifts need annotation, not decoration

## Implementation effort
Medium

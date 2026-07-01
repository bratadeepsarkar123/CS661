# M4-01 — Chord Student Flows

## Intent
**Circular chord diagram** of bilateral tertiary student flows among top ~12 countries — compact “who sends students where” without geographic map duplication.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Student Flow Chord           [⛶]   │
├─────────────────────────────────────┤
│        CHN                            │
│    USA ═══╬═══ GBR                   │
│        IND                            │
│ (6 arc segments, top flows only)    │
├─────────────────────────────────────┤
│ Top flow: CHN→USA                   │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Top N countries: 12 ▾  Min flow threshold    │
├──────────────────────────────────────────────────────────┤
│ d3 chord layout; ribbon width ∝ mobile students          │
│ Hover ribbon → origin→dest + count tooltip               │
│ Click country arc → highlight all incident ribbons       │
├──────────────────────────────────────────────────────────┤
│ Others dim 15%; selected arc bright                      │
│ Footnote: UNESCO UIS inbound/outbound where bilateral est.│
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Arc fill | Region palette, 12 max colors |
| Ribbons | Source color at 50% opacity |
| Highlight | opacity 0.9 + white arc stroke |
| Background | `#0f172a`

## Interaction
1. Overview: aggregated top 3 flows as text + mini chord
2. Fullscreen: hover/click focus+context
3. Year morphs ribbon widths (interpolate)
4. Threshold slider hides small flows

## Data bindings
- UNESCO UIS mobile student indicators; bilateral matrix from UIS or OECD where available
- JSON: `{ year, matrix: [[n]], labels: [iso], flows: [{ from, to, value }] }`
- If bilateral sparse: use regional aggregates with footnote

## Lecture alignment
- **Flow width (L2):** Linear width = student count
- **7±2:** 12 nodes max
- **Not Module 5:** No India lat/lon node map

## Risks
- Bilateral data gaps — regional fallback documented
- Chord readability — limit N and threshold

## Implementation effort
Medium–high

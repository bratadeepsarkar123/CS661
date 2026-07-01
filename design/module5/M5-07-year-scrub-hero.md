# M5-07 — Year Scrub Hero

## Intent
Make **temporal change** the hero narrative: scrubbing 2015→2024 shows edge emergence/dissolution (Domestic HE network growth post-2015).

## Layout
```
┌────────────────────────────────────────────┐
│  ◀  2015  2016  2017 … 2024  ▶             │
│  ════════════●═════════════════  slider    │
├────────────────────────────────────────────┤
│  Map: edges animate opacity/width by year   │
│  New edges this year: brief green flash     │
├────────────────────────────────────────────┤
│  Stat strip: |E| hubs, Σ weight, Δ vs prior │
└────────────────────────────────────────────┘
```

## Animation spec
- Transition 400ms ease between year payloads
- Edge enters: stroke from 0 → target width; optional one-time `#22c55e` flash
- Node enters: scale 0 → 1 if first appearance in tier set

## Visual system
- Year label large (24px) top-center
- Play/pause auto-scrub (3s/year) for kiosk demo mode

## Interaction
- Slider + arrow keys
- Selecting node **freezes** year until deselect
- Compare mode: hold Shift to overlay prior year edges (ghost)

## Data bindings
- Preload all `overview_YYYY.json` (10 files ~300KB total) or fetch on demand
- Precompute `delta_edges_YYYY.json` optional for performance

## Lecture alignment
- **Overview→detail:** Grid shows 2015 vs 2024 side-by-side mini spark maps
- Strong fit for “how domestic collaboration evolved” report section

## Risks
- Animation may distract — default paused on grid overview
- 10 JSON loads — batch or embed in single manifest

## Implementation effort
Medium–high

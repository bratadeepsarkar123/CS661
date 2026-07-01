# M5-06 — Search-First Command

## Intent
Solve **discoverability** for 80 non-hub nodes: search is the primary control; map stays sparse until user commits a query.

## Layout (initial state)
```
┌────────────────────────────────────────────┐
│  🔍 Search 120 institutions…               │
│  [premier ▼] [state ▼] [year ▼]            │
├────────────────────────────────────────────┤
│  Map: hubs only + faint state silhouettes  │
│  (state nodes at 10% opacity, no labels)   │
├────────────────────────────────────────────┤
│  “Type to reveal institutions” placeholder │
└────────────────────────────────────────────┘
```

## After search / selection
- FlyTo institution, full ego network, card panel slides in from right
- Recent searches (max 5, localStorage)

## Visual system
- Search bar: prominent, `#1e293b` field, 48px height in fullscreen
- Keyboard: `/` focuses search, `Esc` clears selection

## Interaction
- Autocomplete with tier badge prefix `[P]` / `[S]`
- Empty search → hub-only map (performance friendly)
- **7±2:** search + 3 filters + map + card

## Data bindings
- Build lightweight `institution_index.json` (id, name, tier, lat, lon) for fast search without full metrics

## Lecture alignment
- **Overview→detail:** Grid shows search mock + 3 hub names as hints
- Supports demo: type “IIT Kanpur” → instant story

## Risks
- Hides geography until interaction — include “Show all” toggle

## Implementation effort
Medium (index file + UX)

# M2-05 — Bar Race Topics

## Intent
**Animated horizontal bar race** of top-10 OpenAlex research concepts by global publication count — flagship “field momentum” viz from proposal §4.3.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Top Research Topics          [⛶]   │
├─────────────────────────────────────┤
│ AI/ML        ████████████ 1         │
│ Oncology     ████████ 2             │
│ COVID-19     ██████ 3                 │
│ (top 5 bars, static year 2024)      │
├─────────────────────────────────────┤
│ ▶ icon greyed in thumbnail          │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ▶ Play  Pause  [Speed ▾]  [Year scrub ●]  Top 10       │
├──────────────────────────────────────────────────────────┤
│ Bars reorder with transition; rank numbers left          │
│ Long labels truncate with ellipsis; full in tooltip      │
├──────────────────────────────────────────────────────────┤
│ Click bar → sidebar sparkline 1996–2024 for topic          │
│ Focus: selected bar full opacity; others 40%             │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Bars | 10 distinct hues from restrained palette (no neon) |
| Rank badge | `#1e293b` circle, 10px |
| Bar height | 28px; gap 6px |
| Value label | Right-aligned inside bar if width > 80px |

## Interaction
1. Play/pause year animation (fullscreen)
2. Scrub year slider
3. Click topic → sparkline + freeze rank history overlay
4. Speed: 500ms / 900ms / 1500ms per year step

## Data bindings
- OpenAlex concepts aggregated globally by year (proposal: 7 topics × 75 years expandable to top-10)
- JSON: `{ frames: [{ year, topics: [{ id, name, count, rank }] }] }`
- Current `data.js` has mock topic arrays — replace entirely

## Lecture alignment
- **Overview→detail (L2):** Overview top 5 only
- **7±2:** Ten bars fullscreen; five overview
- **Trend/time-series (L10):** Animation shows temporal change

## Risks
- Label collision during transitions — D3 axis trick or long pause on year
- Concept name length — ellipsis + tooltip mandatory

## Implementation effort
Medium (known pattern; many libraries reference)

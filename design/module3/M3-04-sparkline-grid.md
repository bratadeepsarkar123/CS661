# M3-04 — Sparkline Grid

## Intent
**Accessibility / reduced-motion** alternative to bar race: grid of **10 mini sparklines** (volume over time), no animation. Each cell = one topic; y = volume trend 2010–2024. Best for users with `prefers-reduced-motion` or overview cells that must not flash.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Topic Trends (static)        [⛶]   │
├─────────────────────────────────────┤
│ AI      ___/‾‾‾   Genomics ___/‾    │
│ Energy  __/‾‾    Quantum  _/‾‾‾     │
│ 2×2 sparklines, no motion           │
├─────────────────────────────────────┤
│ Sorted by 2024 volume               │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Sort: 2024 vol|CAGR|name  Field filter ▾  [Year ●]       │
├──────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────┐ ┌──────────┐                   │
│ │ AI       │ │ Genomics │ │ Energy   │  5×2 grid         │
│ │ ~~~~~/‾‾ │ │ ~~~~/‾‾  │ │ ~~~~/‾   │  sparklines       │
│ │ 142k→310k│ │ rank #2  │ │ +18%/yr  │  end labels       │
│ └──────────┘ └──────────┘ └──────────┘                   │
├──────────────────────────────────────────────────────────┤
│ Year scrubber: vertical line across all sparklines       │
├──────────────────────────────────────────────────────────┤
│ *Synthetic TOPICS; no animation by design                │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Sparkline stroke | Field color 1.5px; fill gradient 0.15 opacity |
| Panel | `#1e293b` 1px border; title `#e2e8f0` 12px |
| End dot | Latest year r=3px field color |
| Overview | 4 topics; fullscreen 10 |
| Scrubber line | `#fbbf24` 1px vertical shared |

## Interaction (Shneiderman)
1. **Overview:** 4 sparklines, no controls
2. **Zoom/filter:** field filter; sort metric
3. **Details-on-demand:** click panel → enlarge + volume table all years
4. **Scrubber:** drag year → dot on each sparkline + value tooltip

## Data bindings
- Full time series per topic from M3-01 JSON (all years, not just top-10 snapshots)
- Placeholder: loop `getTopicsForYear(y)` for y in 2010..2024 client-side

## Lecture alignment
- **Accessibility:** WCAG — no flashing; motion-free default
- **7±2:** Ten panels but one sort + one filter + scrubber
- **Small multiples (Tufte):** Same time axis, comparable slopes

## Risks
- Less engaging than race — use as explicit "accessible mode" toggle on M3-01
- Sparkline scale per panel hides cross-topic magnitude — optional shared y-scale toggle

## Implementation effort
Low — mini line charts; no transition logic

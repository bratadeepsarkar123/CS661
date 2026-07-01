# M3-07 — Scrubber Hero

## Intent
**Temporal control as hero element**: large year scrubber (slider + labels) drives bar positions — chart secondary to scrubbing UX. Matches Module 5 year-scrub pattern (M5-07) for cross-panel consistency.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Research Topics              [⛶]   │
├─────────────────────────────────────┤
│ [2010 ═══════●══════ 2024]          │
│ AI ████████  Genomics ██████        │
│ (bars update with slider preview)   │
├─────────────────────────────────────┤
│ Year scrubber dominant                │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ┌──────────────────────────────────────────────────────┐ │
│ │  2010 ════════════●════════════════════════ 2024     │ │
│ │       2015    2020    COVID    2024                  │ │
│ └──────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Large horizontal bars (rank 1–10) below scrubber        │
│  Scrubber drag → immediate bar update (no play required) │
│  Optional ▶ play moves scrubber head automatically       │
│  Milestone ticks: 2010, 2015, 2020, 2022, 2024         │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Hero year display: 48px `#e2e8f0` centered above bars    │
├──────────────────────────────────────────────────────────┤
│ *Synthetic TOPICS; sync APP.year global if wired         │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Scrubber track | `#334155` h=8px; thumb `#6366f1` r=12px + white ring |
| Milestone ticks | `#64748b` 2px; label `#94a3b8` 10px |
| Hero year | `#e2e8f0` 48px bold; subtitle rank-1 topic |
| Bars | Standard M3-01 styling; height 32px for legibility |
| Scrubber zone | 20% of fullscreen height minimum |

## Interaction (Shneiderman)
1. **Overview:** mini scrubber (read-only or 3-step snap: 2010/2020/2024)
2. **Zoom/filter:** drag scrubber = primary interaction; keyboard ←/→ year step
3. **Details-on-demand:** hover bar while scrubbing → freeze tooltip
4. **Play:** animates scrubber head; pause on user drag

## Data bindings
- Same M3-01 JSON; client caches all year slices for instant scrub
- Preload all years on fullscreen enter (small payload ~15 years × 10 topics)
- Placeholder: precompute array from `getTopicsForYear()` loop

## Lecture alignment
- **7±2:** One hero scrubber + bars + optional play = 3 controls
- **Consistency:** Align scrubber chrome with Module 5 M5-07
- **Direct manipulation (L2):** Slider linked 1:1 to data year

## Risks
- Play + scrub conflict — pause play on manual scrub
- Global APP.year sync may fight local scrub — document ownership

## Implementation effort
Medium — UX polish on scrubber; data preload pattern

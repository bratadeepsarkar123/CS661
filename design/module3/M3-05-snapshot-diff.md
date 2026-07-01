# M3-05 — Snapshot Diff

## Intent
**Static overview cell** hero: side-by-side horizontal bars for **2010 vs 2024** top-10 topics. Shows decade shift without animation — ideal for grid thumbnail and print-friendly slides.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Topics: 2010 vs 2024         [⛶]   │
├─────────────────────────────────────┤
│         2010    │    2024           │
│ AI      ████    │  ██████████  ↑    │
│ Genomics █████  │  ████████         │
│ Δ labels: AI +180%, Quantum new     │
├─────────────────────────────────────┤
│ Mirror bars, shared topic rows      │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Pair: [2010 vs 2024 ▾]  Sort: 2024 vol|biggest Δ|name    │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Butterfly / back-to-back bars per topic (top 10 union)   │
│  Left = year A volume (indigo); Right = year B (cyan)    │
│  Center column: topic names; Δ% badge color-coded        │
│  New in 2024: dashed bar + "NEW" tag                     │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: topic | vol_2010 | vol_2024 | Δ% | rank change  │
├──────────────────────────────────────────────────────────┤
│ *Synthetic TOPICS; module3_topics.json                   │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Year A bars | `#6366f1` |
| Year B bars | `#22d3ee` |
| Δ badge | Positive `#22c55e`, negative `#fb7185`, neutral `#94a3b8` |
| Center gutter | 120px topic labels `#e2e8f0` |
| Overview | Top 5 topics by 2024 volume |

## Interaction (Shneiderman)
1. **Overview:** fixed 2010/2024 pair, 5 rows
2. **Zoom/filter:** change year pair presets (2010/2020/2024)
3. **Details-on-demand:** click row → sidebar + highlight
4. **Sort:** biggest volume change vs latest rank

## Data bindings
- Two slices from M3-01 JSON at years 2010 and 2024
- Union of top-10 both years (may be >10 rows) — cap display at 12 with footnote
- Placeholder: `getTopicsForYear(2010)` vs `getTopicsForYear(2024)`

## Lecture alignment
- **Tufte:** Static comparison avoids motion distraction
- **7±2:** Two hues (years), one sort, one pair selector
- **Overview→detail (L2):** Thumbnail delivers decade story in one glance

## Risks
- Topics in 2010 top-10 but not 2024 need "dropped" indicator
- Union >10 rows — sort by max volume, footnote remainder

## Implementation effort
Low — dual bar chart; no animation

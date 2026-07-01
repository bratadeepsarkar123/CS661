# M3-03 — Stream Topic Share

## Intent
**Composition view** of top-10 topic volume: stacked stream/area showing each topic’s **share of top-10 total** over time. Answers "Is AI growing at the expense of biomedicine?" without rank motion.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Topic Share Mix              [⛶]   │
├─────────────────────────────────────┤
│ ▓▓ AI ▒▒ Genomics ░░ Energy ~~~     │
│ stream 2010→2024 compressed         │
├─────────────────────────────────────┤
│ AI share ↑ post-2022 callout        │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Stack: [% of top-10|absolute volume]  [Year ●]           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Stacked area, x = year, y = 0–100% (normalized)       │
│  10 layers max; colors by field (7 hue groups)           │
│  Hover → topic + share + absolute volume               │
│  Click layer → isolate; reorder legend by latest share   │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: topic rank table for scrubbed year              │
├──────────────────────────────────────────────────────────┤
│ *Synthetic TOPICS; module3_topics.json                 │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Layers | 10 distinct hues grouped by 7 fields (reuse field palette) |
| Stroke | `#0f172a` 0.5px between layers |
| Baseline | Zero baseline (not silhouette) — % must sum to 100 |
| Overview | 3 labeled layers: AI, Genomics, Renewable Energy |

## Interaction (Shneiderman)
1. **Overview:** static stream, no scrubber
2. **Zoom/filter:** toggle absolute vs normalized y
3. **Details-on-demand:** hover → tooltip; click → lock layer
4. **Year scrubber:** vertical line + sidebar sync

## Data bindings
- ETL: from M3-01 volumes → compute `share = volume / sum(top10 volumes)`
- JSON schema: extend M3-01 with `share_pct` per topic×year
- Placeholder: client-side normalize from `getTopicsForYear()`

## Lecture alignment
- **Lie factor (L10):** Toggle absolute vs % mandatory
- **7±2:** One stack mode, one year control, field-grouped colors
- **Part-to-whole (L15):** Normalized stack sums to 100%

## Risks
- Topics outside top-10 invisible — footnote "composition of top-10 only"
- 10 colors exceeds 7±2 — group by field in legend

## Implementation effort
Low–medium — D3 stack; same data as M3-01

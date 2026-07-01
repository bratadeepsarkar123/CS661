# M2-03 — Streamgraph Quality

## Intent
Single-canvas **composition view**: stacked area showing global share of publications in Q1, Q2, Q3, Q4 over time (1996–2024). Complements ridgeline by answering “what fraction of output is top-tier vs bottom-tier?” without per-year density rows.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Quality Tier Mix             [⛶]   │
├─────────────────────────────────────┤
│ ▓▓ Q1 ▒▒ Q2 ░░ Q3 ░ Q4             │
│ ~~~~~~~~~~~~~~~~ stream 1996→2024   │
│ Q4 share ↑ visibly after 2010       │
├─────────────────────────────────────┤
│ 4 tiers · silhouette stack          │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Stack: [silhouette|expand|zero]  [Year ●]  Tiers: 4 ▾   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Streamgraph / stacked area, x = year, y = % share (100) │
│  Layers: Q1 (indigo) Q2 (cyan) Q3 (amber) Q4 (rose)      │
│  Hover band → tier name + % + absolute docs (tooltip)    │
│  Click tier → isolate layer; others 25% opacity            │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: tier table for selected year (Q1–Q4 % + counts) │
├──────────────────────────────────────────────────────────┤
│ *Synthetic demo; SCImago global aggregates               │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Q1–Q4 palette | `#6366f1`, `#22d3ee`, `#fbbf24`, `#fb7185` (4 tiers = within 7±2) |
| Baseline | **Silhouette** (wiggle) for readable mid-chart shape |
| Stroke | `#0f172a` 0.5px between layers |
| Overview | Q1 + Q4 labels only; middle tiers unlabeled |

## Interaction (Shneiderman)
1. **Overview:** static stream, no play button
2. **Zoom/filter:** year brush on x-axis; tier legend toggle
3. **Details-on-demand:** hover → tooltip with % and doc count
4. **Stack mode:** silhouette default; expand for absolute volume honesty

## Data bindings
- ETL: aggregate SCImago country rows → global Q1–Q4 counts per year → normalize to %
- JSON schema: `{ series: [{ year, q1, q2, q3, q4, total_docs }] }`
- Target: `module2_quality_stream.json` (or extend `module2_ridgeline.json`)
- Placeholder: derive synthetic tier shares from `getRidgelineData()` integrals

## Lecture alignment
- **Lie factor (L10):** Silhouette vs expand toggle — user must see % vs absolute
- **7±2:** Four tier colors, one stack mode, one year scrubber
- **Composition (L15):** Part-to-whole readable in single view

## Risks
- Silhouette distorts absolute volume — mandatory expand mode + footnote
- Q2/Q3 middle tiers visually dominated — use consistent tier order (Q1 top)

## Implementation effort
Low–medium — standard D3 stack; simpler ETL than per-country KDE

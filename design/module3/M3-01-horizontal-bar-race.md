# M3-01 — Horizontal Bar Race (Recommended)

## Intent
Proposal §4.3 default: **animated horizontal bar chart race** showing top-10 research topics by publication volume per year (2010–2024). Classic "racing bars" narrative — AI rises, infectious diseases spike 2020–2022 — driven by OpenAlex concept aggregates.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Top Research Topics          [⛶]   │
├─────────────────────────────────────┤
│ AI        ████████████████  #1      │
│ Genomics  ██████████████            │
│ Energy    ████████████              │
│ ... (static frame, latest year)     │
├─────────────────────────────────────┤
│ ▶ Play in fullscreen                │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ▶ Play/Pause  [Year 2010 ────●──── 2024]  Speed: 1×▾     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Horizontal bars, rank 1–10, length ∝ volume             │
│  Smooth tween between years (300ms); bars swap rank      │
│  Rank badge left; topic name + volume label right        │
│  Color by field category (≤7 hues)                       │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Footer: current year large; leader topic + Δ rank        │
├──────────────────────────────────────────────────────────┤
│ *Synthetic TOPICS in dashboard/data.js                   │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Bars | Field palette: CS `#6366f1`, Biomed `#fb7185`, Eng `#22d3ee`, etc. (max 7) |
| Bar height | 28px; gap 4px; label `#e2e8f0` 13px |
| Rank badge | `#334155` circle, `#cbd5e1` number |
| Overview | No animation; final year frame only |
| Tween | d3.interpolateNumber on bar width; FLIP on y-position |

## Interaction (Shneiderman)
1. **Overview:** static top-10 for APP.year; no play
2. **Zoom/filter:** year scrubber + play/pause; speed 0.5×/1×/2×
3. **Details-on-demand:** hover bar → field, volume, rank history spark
4. **Reduced motion:** respect `prefers-reduced-motion` → jump frames, no tween

## Data bindings
- ETL: OpenAlex concepts aggregated by year → top-10 per year in Python
- JSON schema: `{ years: [{ year, topics: [{ id, name, field, volume, rank }] }] }`
- Target: `module3_topics.json`
- Placeholder: `DATA.getTopicsForYear(year)` + `TOPICS` array in `data.js`

## Lecture alignment
- **7±2:** Ten bars visible but **7 field colors** max; one play, one scrubber
- **Motion honesty (L10):** Bar length = volume only; rank change not extra encoding
- **Overview→detail (L2):** Thumbnail static; motion in fullscreen only

## Risks
- Bar race criticized as chartjunk — justify with temporal rank story + static alt (M3-04)
- OpenAlex concept drift — footnote concept ID versioning

## Implementation effort
Medium — D3 join + transition; ETL aggregation straightforward

# M3-02 — Bump Rank Trails

## Intent
Emphasize **rank volatility** over volume: bump chart with lines tracking each topic’s rank (1–10) across years. Better than bar race when the story is "who entered/exited the top 10" rather than absolute growth.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Topic Rank Trails            [⛶]   │
├─────────────────────────────────────┤
│  1 ────╲  AI climbs                 │
│  5 ──╱──╲──                          │
│ 10 ──────── Blockchain enters       │
│ x: year   y: rank (1=top)           │
├─────────────────────────────────────┤
│ 5 lines only in overview            │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ▶ Play  [Year ●]  Show: top 10|all tracked ▾             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Bump chart: x = year, y = rank (inverted 1 at top)      │
│  One polyline per topic; color = field category          │
│  End labels at latest year; hover → topic + rank path    │
│  Crossings highlighted (optional subtle glow)            │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: topic | best rank | worst rank | years in top10 │
├──────────────────────────────────────────────────────────┤
│ *Synthetic TOPICS; OpenAlex ETL → module3_topics.json  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Lines | 2px stroke; field colors; opacity 0.85 |
| Rank axis | 1–10 ticks; `#94a3b8`; inverted scale |
| End labels | `#e2e8f0` 11px; collision offset ±8px |
| Overview | 5 highest-volatility topics only |
| Grid | horizontal rank lines `#334155` 0.5px |

## Interaction (Shneiderman)
1. **Overview:** 5 lines, fixed 2010–2024 span
2. **Zoom/filter:** year scrubber moves vertical cursor; play animates cursor
3. **Details-on-demand:** hover line → highlight + dim others 20%
4. **Focus:** click topic → isolate line + rank table

## Data bindings
- Same as M3-01: pre-computed rank per topic per year
- Derive rank from volume sort in ETL (not stored separately in OpenAlex)
- Placeholder: compute ranks client-side from `getTopicsForYear()` for each year

## Lecture alignment
- **7±2:** Limit labeled lines to 10; field legend ≤7 colors
- **Tufte:** Rank is ordinal — y-axis clearly labeled inverted
- **Comparison (L2):** Crossings show competitive dynamics without bar length bias

## Risks
- Line spaghetti if >10 topics — strict top-10 filter
- Rank ties — deterministic tie-break by volume then name

## Implementation effort
Medium — bump chart layout + label collision; shares ETL with M3-01

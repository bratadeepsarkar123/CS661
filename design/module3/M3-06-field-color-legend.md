# M3-06 — Field Color Legend

## Intent
Bar race (M3-01 substrate) with **explicit OpenAlex field encoding**: bars colored by field category (≤7 hues), legend always visible, field filter toggles. Emphasizes disciplinary structure of rising topics — CS vs Biomed vs Engineering.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Topics by Field              [⛶]   │
├─────────────────────────────────────┤
│ ■ CS ■ Biomed ■ Eng ■ Physics …     │
│ AI ████████  Genomics ██████        │
│ (bars colored by cat from TOPICS)   │
├─────────────────────────────────────┤
│ Legend: 6 fields max                │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Fields: [all|CS|Biomed|Eng|…]  ▶ Play  [Year ●]         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Horizontal bar race OR static bars for selected year    │
│  Color = field (NOT unique per topic) — max 7 hues       │
│  Legend pinned top-right; click swatch → filter field    │
│  Bar label: topic name + field abbreviation in muted text│
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Sidebar: field summary — count in top10, total volume    │
├──────────────────────────────────────────────────────────┤
│ *Synthetic TOPICS.cat; OpenAlex field IDs in ETL         │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Field palette | CS `#6366f1`, Biomed `#fb7185`, Eng `#22d3ee`, Physics `#a78bfa`, Chemistry `#fbbf24`, Earth `#34d399`, Multi `#64748b` |
| Legend | Horizontal strip; active field full opacity; inactive 30% |
| Bar stroke | Same hue, darker 1px when selected |
| Overview | Legend + 4 bars spanning ≥3 fields |

## Interaction (Shneiderman)
1. **Overview:** legend + snapshot bars; no filter
2. **Zoom/filter:** click legend → show only topics in field (re-rank within filter)
3. **Details-on-demand:** hover → field full name + OpenAlex concept ID
4. **Play:** optional; field filter persists during animation

## Data bindings
- ETL: map OpenAlex concept → field (top-level domain); store `field_id`, `field_name`
- JSON schema: topics include `field` enum (≤7 values enforced in ETL)
- Placeholder: `TOPICS[].cat` in `data.js` (6 categories today)

## Lecture alignment
- **7±2 (L2/L10):** **Seven field colors max** — critical constraint
- **Categorical color:** Consistent field hues across Modules 1–3
- **Integrity:** Field assignment documented in ETL metadata

## Risks
- Topics spanning multiple fields — assign primary field in ETL + footnote
- Colorblind — add field abbreviation text on bar

## Implementation effort
Low — M3-01 + legend/filter layer; field mapping in ETL

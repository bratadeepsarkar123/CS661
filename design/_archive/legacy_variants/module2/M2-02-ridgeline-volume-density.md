# M2-02 — Ridgeline Volume Density

## Intent
**Distribution-first** view of publication volume: each year a KDE ridge showing how countries cluster in output (not geography) — reuses quality-shift pipeline geometry for **volume** lens.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Publication Density Shift    [⛶]   │
├─────────────────────────────────────┤
│ 1996 ≈ ~~~~  single broad ridge     │
│ 2024 ≈ ~~~    ~~~~  bimodal hint    │
│ 3 labels: Parity · Mid · Heavy tail │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year hover scrub]  Metric: log pubs | raw pubs          │
├──────────────────────────────────────────────────────────┤
│ Ridgeline stack 1996→2024 (vertical time)                │
│ Each row = KDE of country pub counts for that year         │
│ Hover row → highlight + sidebar: top 5 countries in band   │
├──────────────────────────────────────────────────────────┤
│ Pre-computed bins only (L15); no raw country list in browser│
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Ridge fill | `#6366f1` → `#22d3ee` gradient by era (2 stops only) |
| Stroke | `#94a3b8` 1px ridge outline |
| Highlight row | `#f8fafc` outline |
| Overview | 2 silhouette ridges + 3 text labels |

## Interaction
1. Overview: static 1996 vs 2024 inset
2. Fullscreen: hover scrubs highlight row; click pins year
3. Optional play sweeps highlight downward
4. Log toggle remaps x-axis (pre-computed second bin set)

## Data bindings
- Follow `global_quality_shift_agent_handoff.md` KDE pattern but x = publication count
- SCImago country-year totals → scipy KDE → compact bins JSON
- `{ years: [{ year, bins: [{ x, density }], top_countries: [...] }] }`

## Lecture alignment
- **Distribution summarization (L15):** Bins only in payload
- **Focus+context (L10):** Hover row dims others
- **No chartjunk:** No red/blue glow on overview (lecture plan §6)

## Risks
- Confusion with Q1/Q4 quality ridgeline — title must say “volume”
- KDE bandwidth affects story — document bandwidth in footnote

## Implementation effort
Medium (reuse Module 2 handoff scripts)

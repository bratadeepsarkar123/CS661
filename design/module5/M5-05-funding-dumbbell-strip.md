# M5-05 — Funding Dumbbell Strip

## Intent
Connect Module 5 to the **wealth paradox**: premier vs state **funding per student** (or total funding where student count missing) as a dumbbell chart under the map.

## Layout
```
┌────────────────────────────────────────────┐
│           [Hub map — minimal]              │
├────────────────────────────────────────────┤
│ Funding gap (NIRF 2024, n=116 reported)   │
│                                             │
│  Premier ●━━━━━━━━━━━━━━━━━━━━● State      │
│         ₹X avg              ₹Y avg          │
│                                             │
│  [institution dots on dumbbell by tier]     │
├────────────────────────────────────────────┤
│ Patents: separate small bar (42 reported)   │
└────────────────────────────────────────────┘
```

## Visual system
- Dumbbell line: `#64748b`
- Premier dots: `#3b82f6`; State dots: `#a855f7`
- Institutions with `funding_status !== reported` → hollow grey dots, excluded from averages

## Interaction
- Hover dot → map highlight + tooltip name
- Click dot → select node on map (sync)
- Toggle metric: total funding vs funding/student (if AISHE enrollment joined later)

## Data bindings
- Requires `_full_*.json` with `funding_total`, `funding_status`
- Tier averages computed client-side excluding non-reported

## Lecture alignment
- **Graphical integrity:** Missing = not plotted, not zero
- **Overview:** Grid cell shows dumbbell only (no map) for faster load

## Risks
- Only 116/120 funding — footnote must dominate visually
- Student denominator may be incomplete — label metric clearly

## Implementation effort
Medium

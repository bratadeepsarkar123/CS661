# M4-05 — Top-8 Overview Strip

## Intent
**Overview readability** first: grid cell and optional fullscreen default show **only top 8 countries by citation gain** — remaining countries behind "show all" expand. Prevents dumbbell clutter in 35% dashboard slot.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Collaboration Premium        [⛶]   │
├─────────────────────────────────────┤
│ 1 CHE ●────●  +8.8                  │
│ 2 AUS ●────●  +7.9                  │
│ …                                   │
│ 8 IND ●───●   +6.7                  │
├─────────────────────────────────────┤
│ Top 8 by gain · 2024                │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Show: [top 8|top 15|all 60]  [Year ●]  Sort: gain ▾      │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Dumbbell strip (M4-01 style) for selected count         │
│  Rank number left column `#64748b`                       │
│  "Show all" expands with vertical scroll                 │
│  Sticky header: axis + legend                            │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Footer stat: median gain top-8 vs global median          │
├──────────────────────────────────────────────────────────┤
│ *Synthetic COLLAB_DATA sorted by gain                   │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Rank column | 24px wide; `#94a3b8` 10px |
| Dumbbell | M4-01 spec; row height 26px |
| Expand CTA | `#6366f1` text button "Show all 17 countries" |
| Overview | Exactly 8 rows — no scroll |
| Divider | `#334155` between rank 8 and rest when expanded |

## Interaction (Shneiderman)
1. **Overview:** locked top 8; no interaction
2. **Zoom/filter:** year; expand count preset
3. **Details-on-demand:** click row → sidebar
4. **Collapse:** return to 8 after expand

## Data bindings
- M4-01 JSON; client sorts by `gain` desc, slices(0, 8)
- Placeholder: `getCollabData()` sorted in render

## Lecture alignment
- **7±2:** Eight rows ≈ within cognitive limit for overview
- **Overview→detail (L2):** Thumbnail readable; full set on demand
- **Tufte:** Rank numbers reduce search time

## Risks
- Arbitrary cut at 8 — footnote total country count
- India/US narrative may fall out of top 8 some years — allow pin countries toggle

## Implementation effort
Low — M4-01 + slice + expand UI

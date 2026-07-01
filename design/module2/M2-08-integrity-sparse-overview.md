# M2-08 — Integrity Sparse Overview

## Intent
**Tufte / grader honesty** variant: overview cell shows **only 3 annotated milestones** (1996 Parity, 2010 Breakaway, 2024 Q4 Flood) as minimal spark-density strips + prominent footnotes — no dense ridgeline in thumbnail. Full chart deferred to fullscreen with data caveats upfront.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Global Quality Shift         [⛶]   │
├─────────────────────────────────────┤
│ 1996 ▁▂▃  "Parity"                  │
│ 2010 ▁▂▃▂ "Breakaway begins"        │
│ 2024 ▁▃▅  "Q4 flood"                │
├─────────────────────────────────────┤
│ ⚠ SCImago tier = journal proxy only │
│ ⚠ Missing countries omitted ≠ zero  │
│ ⚠ Synthetic demo until ETL lands    │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ┌─ Data integrity panel (expanded) ─────────────────────┐│
│ │ Sources: SCImago SJR 1996–2024 · MIN_DOCS=100        ││
│ │ Known gaps: pre-1999 sparse · country name drift     ││
│ │ Synthetic: dashboard/data.js getRidgelineData()       ││
│ └──────────────────────────────────────────────────────┘│
├──────────────────────────────────────────────────────────┤
│ Full ridgeline OR dumbbell (implementer picks M2-01/05)  │
│ Footnote bar pinned bottom — never collapsible           │
├──────────────────────────────────────────────────────────┤
│ [Year ●]  Download: methodology one-pager (optional MD)  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Milestone strips | `#64748b` fill minimal; Q1/Q4 hint only on fullscreen |
| Footnote text | `#94a3b8` 11px; warning icon `#fbbf24` |
| Integrity panel | `#1e293b` border `#475569`; padding 12px |
| Chart area | 60% height; integrity panel 25%; footnote 15% |

## Interaction (Shneiderman)
1. **Overview:** zero controls — read-only milestones + footnotes
2. **Zoom/filter:** fullscreen only; integrity panel always visible
3. **Details-on-demand:** click milestone → jump year in full chart
4. **No animation** in overview — static integrity-first

## Data bindings
- Same ETL as M2-01; emphasize `metadata` block in JSON:
  `{ _meta: { source, min_docs, missing_policy, synthetic: true, etl_date } }`
- Placeholder flag: read from `data.js` until `module2_ridgeline.json` replaces

## Lecture alignment
- **Tufte (L10):** Lead with limitations; missing data ≠ zero explicit
- **Academic integrity:** Matches CS661 grading emphasis on source citation
- **7±2:** Overview = 3 milestones + 3 footnote lines — no control clutter

## Risks
- Sparse overview may look "empty" to teammates — pair with M2-02 in presentation
- Duplicate footnote content with Module 5 — unify footnote CSS across panels

## Implementation effort
Low — mostly layout + copy; chart is borrowed from M2-01 or M2-05

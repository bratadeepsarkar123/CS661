# M5-08 — Integrity Footnote First

## Intent
**Tufte-maximalist** variant for academic grading: lead with data limitations and methodology; map is secondary proof.

## Layout
```
┌────────────────────────────────────────────┐
│ DATA INTEGRITY (always expanded)           │
│ • 120 institutions (OpenAlex ROR)          │
│ • Domestic edge: both authors IN inst IN   │
│ • NIRF funding: 116/120 (4 unranked 2024)  │
│ • NIRF patents: 42/120 (Innovation PDF)    │
│ • SCImago quality: static 2019 snapshot    │
│ • Tier avgs: ~40k affiliated institutions  │
├────────────────────────────────────────────┤
│ Map (compact 60% height) — hub edges only  │
├────────────────────────────────────────────┤
│ Two metrics only: domestic works + degree  │
│ (no funding/patents on main canvas)        │
└────────────────────────────────────────────┘
```

## Visual system
- Integrity panel: `#1e293b` box, monospace labels, 12px
- Map deliberately small — avoids “chartjunk map” criticism
- Link “View funding/patents (full data)” → modal with `_full` JSON fields

## Interaction
- Expand/collapse integrity (default expanded in fullscreen)
- Export verification checklist link → `verification_report.md` static HTML mirror

## Data bindings
- Static copy from `nirf_coverage_gaps.md` + verification counts
- Map uses overview JSON only

## Lecture alignment
- **Graphical integrity:** Literally the first thing you see
- Best if grader cares about honest missing-data handling

## Risks
- Less visually impressive for general audience
- Pairs well with M5-03 for “integrity header + fisheye map” hybrid

## Implementation effort
Low

## Hybrid note
Recommended merge: **M5-08 header + M5-03 map** = production candidate

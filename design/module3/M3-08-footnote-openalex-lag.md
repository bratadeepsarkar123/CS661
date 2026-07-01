# M3-08 — Footnote OpenAlex Lag

## Intent
**Academic integrity** variant: minimal bar race or static bars with **prominent OpenAlex metadata caveats** — concept lag, English bias, pre-2024 ingestion delays. Leads with limitations like M2-08 / M5-08 for grader trust.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Top Research Topics          [⛶]   │
├─────────────────────────────────────┤
│ AI ████████  Genomics ██████        │
│ (3 bars only — chart de-emphasized) │
├─────────────────────────────────────┤
│ ⚠ OpenAlex concepts ≠ keywords      │
│ ⚠ 2024 data incomplete until T+6mo  │
│ ⚠ Synthetic demo (data.js TOPICS)   │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ┌─ Methodology & caveats (always expanded) ────────────┐ │
│ │ Source: OpenAlex works API · concept aggregation     │ │
│ │ Lag: latest year may under-count by 5–15%            │ │
│ │ Language: English-heavy concept labels               │ │
│ │ Synthetic: TOPICS in dashboard/data.js until ETL    │ │
│ └──────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────┤
│ Compact bar race (M3-01) OR sparkline grid (M3-04)       │
│ Chart height ≤50% viewport; footnote panel ≥25%          │
├──────────────────────────────────────────────────────────┤
│ Link: OpenAlex concept version date · ETL script path    │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Caveat panel | `#1e293b`; border `#475569`; icon `#fbbf24` |
| Chart | Muted bars `#64748b` default; field color on hover only |
| Footnote | `#94a3b8` 11px; never hidden behind collapse |
| Overview | 3 bars + 3 caveat lines — chart secondary |

## Interaction (Shneiderman)
1. **Overview:** read-only; no play; caveats dominate
2. **Zoom/filter:** fullscreen chart optional; caveats pinned
3. **Details-on-demand:** click caveat → expand ETL methodology
4. **Reduced motion:** default M3-04 sparklines behind caveats

## Data bindings
- M3-01 JSON + `_meta: { openalex_snapshot, concept_version, synthetic, lag_note }`
- Placeholder: `synthetic: true` flag from `data.js` until `module3_topics.json`

## Lecture alignment
- **Tufte / integrity (L10):** Source and lag disclosed before interpretation
- **CS661 grading:** Matches proposal emphasis on data provenance
- **7±2:** Overview intentionally sparse — integrity over spectacle

## Risks
- Panel feels negative — balance with one positive insight callout
- Duplicate caveat text across modules — centralize in shared `_config/footnotes.md`

## Implementation effort
Low — layout + copy; chart borrowed from M3-01 or M3-04

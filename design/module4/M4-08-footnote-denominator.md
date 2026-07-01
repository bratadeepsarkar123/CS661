# M4-08 — Footnote Denominator

## Intent
**Tufte integrity** variant: lead with **paper-count denominator footnote** and methodology panel; chart (dumbbell or lollipop) secondary. Emphasizes that means are over heterogeneous paper sets — domestic-only vs intl co-auth definitions matter.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Collaboration Premium        [⛶]   │
├─────────────────────────────────────┤
│ USA ●────●  IND ●───●               │
│ (2 dumbbells only — chart minimal)  │
├─────────────────────────────────────┤
│ ⚠ Mean cites over n papers shown    │
│ ⚠ Domestic = no foreign institution │
│ ⚠ Synthetic COLLAB_DATA until ETL   │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ┌─ Denominator & definitions (expanded, pinned) ────────┐ │
│ │ Domestic papers: all authors same country as lead     │ │
│ │ Intl papers: ≥1 co-author different country           │ │
│ │ Denominator: show n_dom, n_intl in sidebar always     │ │
│ │ Missing: excluded countries ≠ zero premium              │ │
│ │ Source: OpenAlex · Synthetic: data.js COLLAB_DATA      │ │
│ └──────────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────────┤
│ Compact M4-01 dumbbell (≤50% height) OR M4-02 lollipop   │
│ Every row label includes n: "IND (n_dom=12k, n_intl=8k)" │
├──────────────────────────────────────────────────────────┤
│ Footnote bar: never collapsible; links to ETL script      │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Definition panel | `#1e293b`; `#475569` border; 25% min height |
| Chart | Muted `#64748b` connectors; color on hover |
| n labels | `#94a3b8` 10px appended to country name |
| Warning icon | `#fbbf24` on overview footnotes |
| Overview | 2 rows + 3 footnote lines |

## Interaction (Shneiderman)
1. **Overview:** read-only; footnotes dominate
2. **Zoom/filter:** fullscreen chart optional; definitions pinned
3. **Details-on-demand:** click footnote term → expand definition
4. **Toggle:** show/hide n labels on chart rows

## Data bindings
- M4-01 JSON + `_meta: { domestic_def, intl_def, min_n, synthetic: true }`
- Require `n_dom`, `n_intl` in every country row (placeholder integers)
- Placeholder: add fake n to `COLLAB_DATA` in spec until ETL

## Lecture alignment
- **Tufte (L10):** Denominator disclosure before mean interpretation
- **Graphical integrity:** Matches CS661 emphasis on citation metric caveats
- **7±2:** Overview sparse — integrity over data ink in chart

## Risks
- n labels clutter rows — default sidebar only; toggle for labels
- Align definitions with OpenAlex API — document in `_meta`

## Implementation effort
Low — M4-01 + copy panel + n display; ETL must supply counts

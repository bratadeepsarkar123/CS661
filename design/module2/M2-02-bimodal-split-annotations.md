# M2-02 — Bimodal Split Annotations (Recommended)

## Intent
Same ridgeline substrate as M2-01, but **narrative-first**: three annotated eras — **Parity** (1996), **Breakaway** (~2010), **Q4 Flood** (2024) — with callout brackets and short labels matching the team docx wireframe (Image 2). Best for grader-facing story clarity.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Global Quality Shift         [⛶]   │
├─────────────────────────────────────┤
│ ┌─ Parity ─┐                        │
│ 1996  ▁▂▃ single peak ~1.0          │
│ ┌─ Breakaway ─┐  ┌─ Q4 Flood ─┐     │
│ 2010  ▁▂▃▂▁ bimodal    2024 ▁▃▅ flood│
├─────────────────────────────────────┤
│ Elite ↑ · Mass-market journals ↑↑   │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Era: [Parity|Breakaway|Q4 Flood|All]  [Year ●]          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Ridgeline (subset or full) + vertical era bands         │
│  Annotated callouts (max 3):                             │
│    • "1996: unimodal near ratio 1.0"                     │
│    • "2010+: right tail = elite breakaway"               │
│    • "2024: Q4 flood — low-tier volume surge"            │
│  Optional: ghost curve of 1996 overlaid on 2024 row      │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Narrative strip: 1-sentence era summary (editable copy)  │
├──────────────────────────────────────────────────────────┤
│ *Synthetic demo; SCImago; MIN_DOCS=100 footnote          │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Era bands | Parity `#334155` 0.2, Breakaway `#475569` 0.25, Flood `#64748b` 0.3 |
| Q1 / Q4 curves | Same as M2-01 |
| Callout text | `#e2e8f0` 13px; leader lines `#64748b` 1px dashed |
| Ghost overlay | 1996 curve on 2024 row: `#94a3b8` stroke 1.5px, no fill |

## Interaction (Shneiderman)
1. **Overview:** three milestone years only with era labels
2. **Zoom/filter:** era toggle jumps year slider to era anchor years
3. **Details-on-demand:** click callout → expand footnote panel
4. **Compare:** toggle "Show 1996 ghost on current year"

## Data bindings
- Same as M2-01: `module2_ridgeline.json`
- Additional metadata: `eras: [{ id, label, year_start, year_end, anchor_year, blurb }]`
- Placeholder: hard-code three era objects in spec; wire to JSON when ETL ready

## Lecture alignment
- **Tufte (L10):** Annotations replace chartjunk; no 3D; data-ink ratio high
- **7±2:** Three era labels + one slider + one narrative strip = 5 elements
- **Storytelling (L2):** Overview delivers thesis; fullscreen supplies evidence

## Risks
- Over-annotation clutters ridgeline — cap at 3 callouts; hide on overview
- Era boundaries subjective — footnote "era bands are interpretive guides"

## Implementation effort
Medium — M2-01 base + annotation layer + era UI

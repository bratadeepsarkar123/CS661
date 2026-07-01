# M3-05 — Waterfall Gap Decomposition

## Intent
**Analytic waterfall** showing how much of the global output gap between high- and low-income groups is “explained” by GERD, researchers, and institutional scale — descriptive decomposition only.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Output Gap Waterfall         [⛶]   │
├─────────────────────────────────────┤
│ Low ──► +GERD ──► +Researchers ──► │
│       High output bar               │
│ 3 step labels only                  │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Compare groups: High vs Low income ▾           │
├──────────────────────────────────────────────────────────┤
│ Waterfall bars: start gap → factor contributions → end   │
│ Hover segment → % of total gap + absolute delta          │
│ Click segment → table of country drivers in that bucket  │
├──────────────────────────────────────────────────────────┤
│ Footnote: Oaxaca-style decomposition pre-computed; not causal│
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Positive contrib | `#22c55e` |
| Negative | `#f97316` |
| Total bars | `#475569` |
| Connectors | thin `#64748b` lines

## Interaction
1. Overview: 3-step simplified waterfall
2. Fullscreen: full 5-factor waterfall
3. Click segment → country table
4. Toggle income group pairing

## Data bindings
- Python decomposition on grouped aggregates (WB income + UIS + SCImago)
- JSON: `{ year, start, end, steps: [{ name, value, drivers: [...] }] }`
- No client-side regression

## Lecture alignment
- **Graphical integrity:** Label each bar absolute value
- **Overview→detail:** Overview collapses factors
- **7±2:** Max 5 waterfall steps

## Risks
- Decomposition method contested — footnote methodology
- Synthetic data cannot support — ETL required

## Implementation effort
High (stats + viz)

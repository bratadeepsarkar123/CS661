# M2-06 — Heatmap Tier×Year

## Intent
**Compact overview** of global quality structure: heatmap with rows = quality tier (Q1–Q4), columns = years (1996–2024), cell color = global share of publications in that tier. Best for dashboard grid cell where vertical space is limited.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Tier Share Heatmap           [⛶]   │
├─────────────────────────────────────┤
│ Q1 ░░▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │
│ Q2 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒   │
│ Q3 ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │
│ Q4 ░░░░▒▒▒▓▓████████████████████   │
│     96      10      18      24     │
├─────────────────────────────────────┤
│ Darker = higher global tier share   │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Normalize: [global %|by row|by col]  [Year ●] highlight   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Heatmap 4×29 cells (+ optional 5-year column groups)    │
│  Color: sequential indigo → rose (or tier-fixed hues)    │
│  Click cell → sidebar: tier, year, share, doc count      │
│  Column hover → vertical guide line for that year        │
│                                                          │
├──────────────────────────────────────────────────────────┤
│ Optional row sparkline: tier trend mini-chart right edge │
├──────────────────────────────────────────────────────────┤
│ *Synthetic demo; SCImago global tier aggregates          │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Cell fill | Sequential `#1e3a5f` (low) → `#6366f1` (Q1 high) / `#881337` (Q4 high) |
| Or tier-fixed | Q1 indigo scale, Q4 rose scale per row |
| Grid lines | `#334155` 0.5px |
| Labels | Row Q1–Q4; col every 4th year on overview |
| Cell size | Overview min 4px; fullscreen 12px+ |

## Interaction (Shneiderman)
1. **Overview:** full heatmap, no click
2. **Zoom/filter:** normalize mode; year scrubber highlights column
3. **Details-on-demand:** click cell → sidebar breakdown
4. **Brush:** drag on x to zoom year range

## Data bindings
- ETL: sum SCImago docs by tier×year globally (or filter region)
- JSON schema: `{ matrix: [{ tier, values: [{ year, share_pct, docs }] }] }`
- Target: `module2_tier_heatmap.json`
- Placeholder: synthetic 4×16 matrix from streamgraph derivation

## Lecture alignment
- **7±2:** Four rows, one normalize toggle, one year highlight
- **Tufte:** No pseudo-3D; cell value in tooltip not flooded on overview
- **Overview density (L2):** Entire 29-year story in one thumbnail

## Risks
- Color scale misread as absolute volume — footnote + docs in tooltip
- Row normalization hides Q4 flood — default global % normalization

## Implementation effort
Low — D3 heatmap; trivial ETL aggregation

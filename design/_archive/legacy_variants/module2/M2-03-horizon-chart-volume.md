# M2-03 — Horizon Chart Volume

## Intent
Compare **top 8 publishing countries** with mirrored horizon bands — packs 30 years × 8 series into one panel without line spaghetti.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Publishing Horizons          [⛶]   │
├─────────────────────────────────────┤
│ USA ═══╪═══ mirrored blue bands     │
│ CHN ═══╪═══                         │
│ IND ═══╪═══  (3 countries shown)    │
├─────────────────────────────────────┤
│ Band height ∝ pub volume            │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ Countries: pick 8 ▾  [Year range 1996–2024]            │
├──────────────────────────────────────────────────────────┤
│ 8 horizon rows, shared x-time                             │
│ Hover band → vertical rule + tooltip count              │
│ Click row → expand row 2× height, others compress       │
├──────────────────────────────────────────────────────────┤
│ Footnote: SCImago + OpenAlex reconciled where available  │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Band color | Single hue per country `#38bdf8` variants (lightness steps) |
| Mirror axis | `#334155` horizontal midline per row |
| Expanded row | `#3b82f6` saturated |

## Interaction
1. Overview: 3 countries fixed
2. Fullscreen: country picker (max 8); click row focus
3. Linked year cursor across rows on hover
4. Sync global year slider to vertical cursor line

## Data bindings
- SCImago/OpenAlex yearly pub totals per country
- JSON time series arrays per country
- Normalize each row independently (horizon convention)

## Lecture alignment
- **Small multiples (L10):** Shared time axis
- **7±2:** Max 8 horizons
- **Tufte:** Band area ∝ value within row only — footnote per-row scale

## Risks
- Cross-row comparison distorted by independent scales — tooltip shows raw
- Horizon unfamiliar to graders — one-line explainer in overview

## Implementation effort
Medium

# M2-08 — Calendar Heatmap Output

## Intent
**Year × country** heatmap of publication intensity (log-scaled) — compact pattern discovery for production surges and stagnation.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Publication Heatmap          [⛶]   │
├─────────────────────────────────────┤
│      '20 '22 '24                    │
│ USA  ░░███                          │
│ CHN  ░████                          │
│ IND  ░░██                           │
│ (8 rows × 12 year cols max)         │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year range]  Region ▾  Color: linear | log              │
├──────────────────────────────────────────────────────────┤
│ ~30 countries × 29 years grid                            │
│ Hover cell → tooltip pubs + YoY Δ                        │
│ Click row → highlight row timeline sparkline below       │
│ Click col → vertical year marker across rows             │
├──────────────────────────────────────────────────────────┤
│ Color scale: `#0f172a` → `#38bdf8` (5 steps)             │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Cell | 12×12px rounded 2px |
| Missing | `#1e293b` |
| Row/col highlight | `#334155` overlay |
| Color scale | Sequential blue; colorblind-safe alt toggle

## Interaction
1. Overview: 8 countries, last 12 years
2. Fullscreen: region filter; row/col focus
3. Sync global year slider to column highlight
4. Double-click cell → jump to M2-05 bar race that year (cross-panel hook optional)

## Data bindings
- SCImago/OpenAlex matrix country×year
- JSON: `{ countries: [...], years: [...], values: [[int]] }`
- Precompute log transform optional second matrix

## Lecture alignment
- **Matrix overview (L10):** Overview limits rows/cols (7±2 rows)
- **Tufte:** No fake 3D; legend with numeric breaks
- **Linked views:** Year slider highlights column

## Risks
- Heatmaps hide magnitude differences within cell — tooltip essential
- Many countries — virtual scroll or region filter required

## Implementation effort
Low–medium

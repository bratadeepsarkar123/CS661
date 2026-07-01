# M4-02 — Sankey Region→Host

## Intent
**Sankey pipeline**: origin regions (Asia, Europe, etc.) flow into top host countries — macro mobility funnel for overview-friendly storytelling.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Mobility Pipelines           [⛶]   │
├─────────────────────────────────────┤
│ Asia ═══╗                            │
│ EU   ═══╬══► USA · GBR · AUS         │
│ Africa══╝   (3 hosts)               │
├─────────────────────────────────────┤
│ USA hosts 22% intl mobile (2024)    │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ [Year ●]  Host count: 8 ▾  Origin: regions | top countries│
├──────────────────────────────────────────────────────────┤
│ Three-column sankey: Origin → (optional hub) → Host       │
│ Hover path highlight; click host → filter origins only    │
├──────────────────────────────────────────────────────────┤
│ Sidebar: host rank table + YoY Δ                          │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Origin nodes | `#64748b` |
| Host nodes | `#38bdf8` |
| Ribbons | gradient origin→host |
| Labels | host names always; origin on hover overview

## Interaction
1. Overview: 3 hosts, 3 origins
2. Fullscreen: expand hosts; toggle origin granularity
3. Click host focus paths
4. Year transition animates ribbon widths

## Data bindings
- UIS aggregate by region + host country
- OECD supplement for OECD hosts
- JSON sankey links per year

## Lecture alignment
- **Overview→detail (L2):** Overview 3×3 flows
- **Chartjunk (L10):** No gradient glow — flat fills
- **7±2:** Three origin groups on overview

## Risks
- Region aggregation hides bilateral detail — link to M4-07 heatmap
- Data lag for recent years — footnote vintage

## Implementation effort
Medium

# M5-01 — Hub Corridor Minimal

## Intent
Fastest path to “I understand India’s domestic HE network in 10 seconds.” Overview shows only hub-to-hub edges; detail is optional.

## Layout (overview grid cell)
```
┌─────────────────────────────────────┐
│ India Domestic HE Network    [⛶]   │
├─────────────────────────────────────┤
│  [Leaflet India, muted basemap]     │
│   ● premier hub  ● state hub        │
│   ─── edge weight 2–5  ─── 6+       │
├─────────────────────────────────────┤
│ Tier strip: Premier ████  State ██   │
│ (avg domestic works only)           │
├─────────────────────────────────────┤
│ *120 institutions; tier avgs over   │
│  ~40k affiliated; NIRF gaps noted   │
└─────────────────────────────────────┘
```

## Fullscreen (on ⛶)
- Left 70%: same map, click hub → side card (name, tier, domestic works, degree)
- Right 30%: ranked hub list (top 15 by degree), no funding/patents in overview mode

## Visual system
| Element | Spec |
|---------|------|
| Background | `#0f172a` |
| Premier | `#3b82f6` fill, white stroke |
| State | `#a855f7` fill, white stroke |
| Edges | `#64748b`, width ∝ log(weight), max 3px |
| Basemap | Carto dark matter, opacity 0.35 |

## Interaction
1. Default: hub edges only (~40–60 visible)
2. Click hub: highlight ego network (all nodes, dim non-ego 25% opacity)
3. No year slider in overview cell; year fixed to latest in thumbnail

## Data bindings
- `india_network_overview_YYYY.json`
- `hubIds`, `edges` filtered hub∩hub

## Lecture alignment
- **7±2:** One map, one tier strip, one footnote
- **Tufte:** Footnote always visible; no 3D; edge width encodes weight only

## Risks
- Hides 60+ non-hub nodes until click — mitigated by search in fullscreen only

## Implementation effort
Low — closest to current code minus extra panels

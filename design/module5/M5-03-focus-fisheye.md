# M5-03 — Focus Fisheye (Recommended)

## Intent
Implement Munzner Ch.14 **focus+context**: selected institution stays sharp; full network remains visible but dimmed. Matches post-audit `india_network.js` behavior.

## Layout
```
┌────────────────────────────────────────────┐
│ [Year 2015 ────●──── 2024]  [Search…]      │
├────────────────────────────────────────────┤
│                                            │
│     Map: all 120 nodes                     │
│     Selected: full opacity + pulse ring    │
│     Neighbors (ego): full opacity          │
│     Others: 25% node, 8% edge opacity      │
│                                            │
├────────────────────────────────────────────┤
│ Card: IIT Delhi | premier | deg 34         │
│ Domestic works 1,204 | Funding reported    │
├────────────────────────────────────────────┤
│ Footnote: SCImago 2019 static; NIRF gaps   │
└────────────────────────────────────────────┘
```

## Edge drawing rules
| State | Edges shown |
|-------|-------------|
| No selection | Hub ∩ hub only, opacity 0.7 |
| Selected | **All** tier-filtered edges; ego edges 0.85, others 0.08 |

## Visual system
- Node radius: `4 + 2*log(degree)` capped at 14px
- Selected: 2px white ring + subtle CSS pulse (1.5s)
- Tier colors unchanged

## Interaction (Shneiderman)
1. **Overview:** hub map + year label
2. **Zoom/filter:** tier toggle premier/state/both
3. **Details-on-demand:** click node → card + ego highlight
4. **Search:** fuzzy match on `display_name`, flyTo + select

## Data bindings
- Year slices `india_network_overview_YYYY.json` / `_full_YYYY.json`
- Lazy-load full JSON only when user opens funding/patents tab in card

## Lecture alignment
- **7±2:** Map + year + search + card + footnote = 5 controls
- **Tufte:** Mandatory footnote on tier averages (~40k affiliated)

## Risks
- Clutter at “both tiers + no selection” — hub filter essential

## Implementation effort
Low–medium (current codebase baseline)

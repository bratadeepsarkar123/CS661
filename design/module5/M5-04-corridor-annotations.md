# M5-04 — Corridor Annotations

## Intent
Tell a **geographic story**: NCR, Bengaluru, Mumbai-Pune, Chennai-Hyderabad corridors as annotated ribbons over the hub map.

## Layout
```
┌────────────────────────────────────────────┐
│  Map with semi-transparent corridor bands  │
│  ┌─ NCR Knowledge Corridor ─────────┐      │
│  │  (label + arrow to hub cluster)  │      │
│  └──────────────────────────────────┘      │
│  Similar: Bengaluru, Mumbai-Pune, South    │
├────────────────────────────────────────────┤
│  Corridor stats (on band hover):            │
│  # institutions, internal edge share %      │
└────────────────────────────────────────────┘
```

## Corridor definitions (static GeoJSON in repo)
| ID | Approx bbox / cities | Hubs included |
|----|---------------------|---------------|
| NCR | Delhi NCR | IITD, JNU, DU, … |
| BLR | Karnataka | IISc, IISC, … |
| MUM-PUN | Maharashtra | IITB, … |
| SOUTH | TN+TS+AP | IITM, IIT-H, … |

## Visual system
- Corridors: `fill: tier-neutral #475569 @ 15% opacity`, dashed border
- Hubs inside corridor: slightly larger nodes when corridor toggled on
- **No fifth color** — corridors are grey overlays

## Interaction
- Toggle corridors (max 2 visible at once — 7±2)
- Click corridor label → filter map to institutions in bbox
- Click hub → standard ego view (M5-03 rules)

## Data bindings
- Precompute `corridor_membership.json` from lat/lon
- Edge share = internal edges / all edges touching corridor nodes

## Lecture alignment
- **Overview→detail:** Grid shows one corridor highlighted; fullscreen all four
- Supports project narrative: “knowledge corridors vs periphery”

## Risks
- Arbitrary bbox boundaries — document methodology in footnote

## Implementation effort
Medium (needs corridor GeoJSON + stats script)

# M5-02 — Split Tier Panels

## Intent
Make the **premier vs state funding/quality gap** impossible to miss — docx-style dual columns (Lecture 2/10 fullscreen pattern).

## Layout (fullscreen only; overview shows static split screenshot)
```
┌──────────────────┬──────────────────┐
│ PREMIER (n≈60)   │ STATE (n≈60)     │
│ mini-map zoom    │ mini-map zoom    │
│ NCR + south hubs │ regional hubs    │
├──────────────────┼──────────────────┤
│ Avg domestic     │ Avg domestic     │
│ works: 847       │ works: 124       │
│ Median funding*  │ Median funding*  │
│ Patents avail*   │ Patents avail*   │
└──────────────────┴──────────────────┘
* footnote: NIRF 116/120 funding; 42/120 patents
```

## Overview grid cell
- Static composite image OR simplified side-by-side bars (domestic works only)
- Badge: “Open fullscreen for funding split”

## Visual system
- Same two tier colors; panels separated by 1px `#334155` divider
- No third color for “gap” — use **position** (left vs right) not redundant hue

## Interaction
- Click institution in either panel → sync highlight on both maps if cross-tier edge exists
- Toggle “Show cross-tier edges only” filter

## Data bindings
- Overview JSON for maps; **full JSON** for funding/patents in fullscreen
- `funding_status`, `patent_status` → “— (unranked)” not zero

## Lecture alignment
- **Overview→detail:** Grid = aggregate bars; fullscreen = split maps
- **Graphical integrity:** Missing NIRF shown as status, not 0

## Risks
- Two maps = 2× render cost; use simplified node set per panel

## Implementation effort
Medium

# M1-05 — Bump Chart ROI Rank

## Intent
Animate **efficiency rank** (citations per million PPP-adjusted GERD) over 1996–2024 — dramatic “who climbed the leaderboard” story tied to expenditure effectiveness.

## Layout

**Overview grid cell**
```
┌─────────────────────────────────────┐
│ Efficiency Rank Race         [⛶]   │
├─────────────────────────────────────┤
│ 1 ─── CHN ↑↑                        │
│ 5 ─── IND ↑                         │
│10 ─── BRA →                         │
│ (top 10 lines, end labels only)     │
├─────────────────────────────────────┤
│ ▶ Play disabled in thumbnail        │
└─────────────────────────────────────┘
```

**Fullscreen**
```
┌──────────────────────────────────────────────────────────┐
│ ▶ Play  [Speed]  [Year scrub ●]  Top N: 10 ▾           │
├──────────────────────────────────────────────────────────┤
│ Rank 1 ─────────────────────────────                     │
│ Rank 2 ─────────────────────────────                     │
│  ... animated country labels move vertically             │
│ Rank 10 ────────────────────────────                     │
├──────────────────────────────────────────────────────────┤
│ Click country → freeze rank trail + sidebar history      │
└──────────────────────────────────────────────────────────┘
```

## Visual system
| Element | Spec |
|---------|------|
| Lines | Interpolate rank; color by region |
| Labels | Country ISO right-aligned at line head |
| Rank axis | Inverted y (1 at top) |
| Trail | Selected country: faint ghost line full history |

## Interaction
1. Play/pause rank animation (fullscreen)
2. Scrub year — updates ranks without full replay
3. Click country — focus trail; others 20% opacity
4. Top N selector: 10 / 15 / 20

## Data bindings
- Compute `efficiency = cites / (gerd_ppp_million + ε)` per country-year
- Rank within available set; store `{ year, ranks: [{ iso, rank, value }] }`
- Animation frames pre-bundled in JSON for smooth playback

## Lecture alignment
- **Time series (L10):** Rank stable encoding; value in tooltip only
- **Chartjunk (L10):** No flags/icons on overview
- **Overview→detail:** Overview static final frame

## Risks
- Rank volatility with missing data — require min 3 years presence to enter
- Small countries jump ranks — footnote sample size threshold

## Implementation effort
Medium (animation timing)

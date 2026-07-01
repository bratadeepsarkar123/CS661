# M1-08 — Diverging Bar Residual

## Intent
Highlight **over- and under-performers** vs a model: residual = observed citation impact minus expected given GERD spend.

## Layout
```
┌─────────────────────────────────────┐
│ Spend-adjusted performance     [⛶]  │
├─────────────────────────────────────┤
│  CHN  ████████▌ +2.1σ               │
│  KOR  ██████▌   +1.4σ               │
│  IND  ◀████     -1.2σ               │
│  ... (top 8 |residual|)             │
├─────────────────────────────────────┤
│ Model: cites ~ GERD + researchers    │
└─────────────────────────────────────┘
```

**Fullscreen:** full ranked list (~60 countries with data), sort toggle, click → metric breakdown.

## Visual system
- Positive residuals: `#22c55e` bars right
- Negative: `#f97316` bars left
- Zero line: `#64748b` 2px
- Bar length = z-score capped at ±3

## Interaction
- Sort: residual | name | GERD
- Click bar → focus+context dim others (L10)

## Data bindings
- Pre-compute regression + residuals in Python per year
- JSON: `{ country, residual_z, predicted, observed, gerd }`

## Lecture alignment
- Tufte: label the model in footnote; missing = excluded not zero
- Best **overview thumbnail** when grid cell is small (readable bars)

## Risks
- Model choice affects narrative — document OLS vs robust regression in report

## Implementation effort
Medium

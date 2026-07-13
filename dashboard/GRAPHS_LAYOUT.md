# Dashboard graph layout

Per-graph folders so editing one visualization does not require touching another.

```
dashboard/
  index.html          # shell + landing + script/link order
  style.css           # SHARED: landing, panel chrome, page-wide colors
  app.js              # SHARED: routing, controls chrome, helpers
  graphs/
    g1/  g1.css  g1.js   # UMAP peer clustering
    g2/  g2.css  g2.js   # Global quality shift
    g3/  g3.css  g3.js   # Research topics
    g4/  g4.css  g4.js   # Collaboration premium
    g5/  g5.css  g5.js   # India network shell
  india_network.js    # G5 Leaflet engine (kept at root; safe)
  *_data.js / data/   # pools — do not merge
```

## Load order

1. Shared CSS (`style.css`) then `graphs/gN/gN.css`
2. Vendor (D3, Leaflet, Plotly, Chart.js)
3. Data pools (`viz*_data.js`, `india_network_data.js`, …)
4. `india_network.js` (G5 engine)
5. Thin `app.js` orchestrator (shared palette + routing)
6. `graphs/gN/gN.js`

## Editing rule

Change graph N only under `graphs/gN/`. Do not put graph-only CSS/JS back into `style.css` / `app.js`.

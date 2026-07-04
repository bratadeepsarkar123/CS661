# hierarchy-app (local / untracked)

This Vite app is **not** the canonical Graph 5 data source. The pipeline publishes network JSON here:

- **Canonical:** `dashboard/data/india_network/` (synced by `09b_export_year_slices.py` from `public/india_network/`)

The built bundle fetches `/india_network/2024_overview.json` (see `dist/assets/*.js`). Serve data from `public/india_network/` in dev or copy into `dist/india_network/` for static preview.

## Sync command (PowerShell, from repo root)

```powershell
New-Item -ItemType Directory -Force -Path hierarchy-app/public/india_network | Out-Null
Copy-Item -Recurse -Force dashboard/data/india_network/* hierarchy-app/public/india_network/
```

After sync, rebuild if needed: `cd hierarchy-app; npm run build` (copies `public/` into `dist/`).

**Note:** `hierarchy-app/dist/india_network/` may contain stale slices (e.g. 2026-06-30) if not rebuilt — prefer sync + build over editing `dist/` by hand.

Do not commit `node_modules/` or full app artifacts unless explicitly requested; only this README is intended for git when documenting the fork.

# G3 L3 fix + L2 broader demo

**Date:** 2026-07-12  
**Scope:** Graph 3 only. G1 / G2 / G4 / G5 untouched.

---

## A) Live L3 set fix

**Problem:** Live Lane C had two Quantum topics (`Quantum computer` + `Quantum information`).

**Change:**

| Action | Concept | ID |
|--------|---------|-----|
| **Keep** | Quantum computer | `C58053490` |
| **Remove from live** | Quantum information | `C169699857` (stays in river) |
| **Add** | Supervised learning | `C136389625` (OpenAlex **level=3**, verified API) |

### New live 7 (`L3_college_cross_domain`)

1. Infectious disease — `C524204448`  
2. Robotics — `C34413123`  
3. Quantum computer — `C58053490`  
4. CRISPR — `C98108389`  
5. Energy storage — `C73916439`  
6. Photovoltaics — `C542589376`  
7. **Supervised learning** — `C136389625`

### Fetch / rebuild

| Step | Result |
|------|--------|
| Fetch `Supervised learning` 1974–2024 | **51/51**, 1433 rows, 9 empty years, **0 errors** |
| Rebuild `dashboard/viz3_data.js` | 17387 pool rows; year_min=1974 |
| `g3.js` / `g3.css` / cache-bust `?v=20260712-l3-sl` | done |
| Mega-AI / ASJC | not used |

---

## B) L2 broader demo (separate localhost)

**Lane B** = one OpenAlex level broader than L3 (mid-college). Served **separately** so main dashboard stays L3.

| Item | Value |
|------|--------|
| Path | `demos/g3-l2-broader/` |
| Port | **8085** |
| URL | http://127.0.0.1:8085 |
| Main G3 | http://127.0.0.1:8080 (unchanged L3) |

### L2 seven

| Topic | ID | Level |
|-------|-----|------:|
| Renewable energy | `C188573790` | 2 |
| Climate change | `C132651083` | 2 |
| Epidemiology | `C107130276` | 2 |
| Sustainable development | `C552854447` | 2 |
| Deep learning | `C108583219` | 2 |
| Automation | `C115901376` | 2 |
| Internet of Things | `C81860439` | 2 |

### Fetch status (L2 missing six)

| Metric | Value |
|--------|------:|
| Queued / fetched | **306 / 306** |
| Rows this run | **24407** |
| Empty year pairs | **6** |
| Errors | **0** |
| Auth | KeyPool from `.env` (values never printed) |

Renewable energy was already in the river.

### Start commands

```powershell
python -m http.server 8080 --directory dashboard
python -m http.server 8085 --directory demos/g3-l2-broader
```

See also `demos/g3-l2-broader/README.md`.

---

## Files touched

- `dashboard/viz3_data.js`, `graphs/g3/g3.js`, `graphs/g3/g3.css`, `index.html` (cache-bust)
- `dashboard/_river_to_pool_rebuild.py` (Lane C allowlist → Supervised learning)
- `dashboard/docs/g3_level_sets.json`
- `CS661_Dataset/.../topic_id_map.json` + river CSV
- `demos/g3-l2-broader/` (standalone demo + `_rebuild_l2_viz3.py`)

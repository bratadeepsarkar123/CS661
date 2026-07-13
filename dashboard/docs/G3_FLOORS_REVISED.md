# G3 honesty floors revised (soft shared 1974 window)

**Date:** 2026-07-12  
**Scope:** Graph 3 only. G1 / G2 / G4 / G5 untouched.  
**Bug class:** Same as AI 1980 — hard milestone floors zeroed continuous OpenAlex concept series, creating fake `n/a → spike` cliffs in the race.

**Policy:** Honesty = UI labeling (retrospective OpenAlex concepts). Do **not** delete real river volume to force a “field birth” narrative. Mega-AI `C154945302` still forbidden as primary.

**Audit script:** `docs/_audit_g3_all_floors.py` → `_audit_g3_all_floors.json`  
**Rebuild:** `_river_to_pool_rebuild.py` → `viz3_data.js`

---

## Per-topic decision table

| Topic | Concept ID | Old floor | Raw global (year before floor) | Raw global (at floor) | Pool before (year before) | Action | New floor |
|-------|------------|----------:|-------------------------------:|----------------------:|--------------------------:|--------|----------:|
| Infectious Diseases | `C524204448` | 1974 | 135 (1973) | 117 (1974) | outside scrubber / matched | **keep** | **1974** |
| Renewable Energy | `C188573790` | 1974 | 51 (1973) | 58 (1974) | outside scrubber / matched | **keep** | **1974** |
| AI & Machine Learning | `C119857082` | 1974 (was 1980) | 3182 (1979)* | 3396 (1980)* | matches river | **verify OK** | **1974** |
| Robotics & Automation | `C34413123` | 1980 | **14** (1979) | **11** (1980) | **0 (n/a)** | **soften → 1974** | **1974** |
| Quantum Computing | `C58053490` | 1994 | **62** (1993) | **80** (1994) | **0 (n/a)** | **soften → 1974** | **1974** |
| Data Science & Big Data | `C2522767166` | 2001 | **5883** (2000) | **6534** (2001) | **0 (n/a)** | **soften → 1974** | **1974** |
| CRISPR & Genomics | `C98108389` | 2012 | **269** (2011) | **386** (2012) | **0 (n/a)** | **soften → 1974** | **1974** |

\*AI already softened earlier the same day; pool 1979=3182 / 1980=3396 still matches raw.

---

## Cliff windows (raw = pool after rebuild)

### CRISPR `C98108389` (old floor 2012)

| Year | Raw global | Pool AFTER |
|-----:|-----------:|-----------:|
| 2005 | 92 | 92 |
| 2006 | 111 | 111 |
| 2007 | 124 | 124 |
| 2008 | 136 | 136 |
| 2009 | 155 | 155 |
| 2010 | 192 | 192 |
| **2011** | **269** | **269** (was n/a) |
| **2012** | **386** | **386** |
| 2013 | 736 | 736 |
| 2014 | 1125 | 1125 |
| 2015 | 1886 | 1886 |

Old cliff: pool 0 → 386. Real river step: +117 (+43%).

### Data Science `C2522767166` (old floor 2001)

| Year | Raw global | Pool AFTER |
|-----:|-----------:|-----------:|
| 1995 | 3270 | 3270 |
| 1996 | 3647 | 3647 |
| 1997 | 4045 | 4045 |
| 1998 | 4208 | 4208 |
| 1999 | 4740 | 4740 |
| **2000** | **5883** | **5883** (was n/a) |
| **2001** | **6534** | **6534** |
| 2002 | 9901 | 9901 |

Old cliff: pool 0 → 6534. Real river step: +651 (+11%).

### Quantum `C58053490` (old floor 1994)

| Year | Raw global | Pool AFTER |
|-----:|-----------:|-----------:|
| 1989 | 40 | 40 |
| 1990 | 29 | 29 |
| 1991 | 53 | 53 |
| 1992 | 82 | 82 |
| **1993** | **62** | **62** (was n/a) |
| **1994** | **80** | **80** |
| 1995 | 102 | 102 |

Old cliff: pool 0 → 80. Real river step: +18 (+29%). Continuous from 1974 (global 20).

### Robotics `C34413123` (old floor 1980)

| Year | Raw global | Pool AFTER |
|-----:|-----------:|-----------:|
| 1974 | 2 | 2 |
| 1975 | 7 | 7 |
| 1976 | 3 | 3 |
| 1977 | 8 | 8 |
| 1978 | 7 | 7 |
| **1979** | **14** | **14** (was n/a) |
| **1980** | **11** | **11** |

Old cliff: pool 0 → 11 (tiny but still fake n/a). Softened for consistency.

### AI `C119857082` (already 1974)

| Year | Raw global | Pool |
|-----:|-----------:|-----:|
| 1974 | 2267 | 2267 |
| 1979 | 3182 | 3182 |
| 1980 | 3396 | 3396 |

---

## Rebuild proof anchors (2026-07-12)

```
honesty_1974:
  Infectious Diseases: 117
  Renewable Energy: 58
  AI & Machine Learning: 2267
  Robotics & Automation: 2
  Quantum Computing: 20
  Data Science & Big Data: 550
  CRISPR & Genomics: 1

pre_cliff_globals:
  AI_1979: 3182 / AI_1980: 3396
  Robotics_1979: 14
  Quantum_1993: 62
  DataScience_2000: 5883
  CRISPR_2011: 269 / CRISPR_2012: 386
```

Pool rows: **28048**. Mega-AI `C154945302` absent. Cache-bust: `?v=20260712-g3-floors-1974`.

---

## What we did *not* do

- Did not invent counts.
- Did not switch AI primary to mega-AI.
- Did not change G1 / G2 / G4 / G5.
- Did not claim 1974 CRISPR bars mean gene-editing Cas9 papers existed then — UI disclaimer carries that honesty.

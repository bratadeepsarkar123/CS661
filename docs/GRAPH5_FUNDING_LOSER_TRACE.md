# Graph 5 — Duplicate Funding Trace & NIRF Loser Review

**Generated:** 2026-07-07  
**Runtime evidence:** `debug-e78b43.log` (session `e78b43`), `institution_funding.csv`, `nirf_funding_by_institute.csv`, `nirf_research_projects.csv`

---

## Executive summary

| Area | Finding |
|------|---------|
| **Duplicate clusters** | **2 remaining** (post-join fixes) — `bhu_campus_family` (206.94 cr × 3) and `coincidental_rounding` (19.84 cr × 2); informational PASS in verification |
| **NIRF losers** | **14** accepted gaps — see `nirf_match_losers.csv` and `GRAPH5_GAP_ASSESSMENT.md` |
| **Historical join bugs** | 6 clusters at audit time — **3 join bugs fixed** (`2effa39`, `f15e208`); clusters A–C below are historical |

### Remaining duplicate clusters (2026-07-08)

| Amount (₹ cr) | Institutes | Classification |
|---------------|------------|----------------|
| 206.94 | IIT BHU Varanasi, Banaras Hindu University, Institute of Medical Sciences | **Legitimate** — shared NIRF Overall row `IR-O-U-0500` (38 projects) |
| 19.84 | Panjab University, NIT Durgapur | **Coincidental** — distinct IDs; raw amounts differ by ~₹0.02 cr |

Dashboard export tags: `funding_duplicate_cluster` = `bhu_campus_family` | `coincidental_rounding`.

---

## Duplicate funding clusters — traced

### 🔴 Cluster A: ₹197.08 cr — **JOIN BUG** (critical)

| Institute | Match score | Verdict |
|-----------|-------------|---------|
| All India Institute of Medical Sciences | 1.0 | ✅ Correct — raw `IR-D-N-15`, 1970827533 INR |
| Indian Institute of Science | 0.788 | ❌ **Wrong** — fuzzy-matched AIIMS; IISc not in `nirf_funding_by_institute` |
| Institute of Medical Sciences (Varanasi) | 0.853 | ❌ **Wrong** — fuzzy-matched AIIMS substring |

**Root cause:** `08_join_nirf_funding.py` accepts fuzzy match at **≥0.78**. "Indian Institute of Science" / "Institute of Medical Sciences" overlap token-wise with "All India Institute of Medical Sciences".

**Fix:** Raise threshold for medical/IIT institutes OR require distinguishing-token overlap with funding row name. IISc should show `null` or its own PDF row if scraped.

---

### 🔴 Cluster B: ₹35.37 cr — **JOIN BUG**

| Institute | Match score | Verdict |
|-----------|-------------|---------|
| IIT Bhilai | 1.0 | ✅ Correct — PDF `IR-E-U-0946`, 353703993 INR |
| IIT (BHU) Varanasi | 0.875 | ❌ **Wrong** — matched Bhilai; BHU has `IR-E-U-0701` in NIRF |

**Fix:** IIT campus token must match (`varanasi` vs `bhilai`). BHU needs own PDF scrape / funding row.

---

### 🔴 Cluster C: ₹12.24 cr — **JOIN BUG**

| Institute | Match score | Verdict |
|-----------|-------------|---------|
| IIT Dharwad | 1.0 | ✅ Correct — PDF `IR-E-U-0899` |
| IIT (ISM) Dhanbad | 0.9 | ❌ **Wrong** — matched Dharwad; Dhanbad has `IR-E-U-0205` |

**Fix:** Distinguish `dhanbad` vs `dharwad` tokens in funding join.

---

### 🟡 Cluster D: ₹19.84 cr — **Coincidental (likely OK)**

| Institute | Raw source |
|-----------|------------|
| Panjab University | `IR-O-U-0078`, 198419807 INR |
| NIT Durgapur | `IR-E-U-0577`, 198400199 INR |

Amounts differ in raw by ~0.01 cr but round to same ₹19.84 cr. **Not a join error** — verify in UI footnote if needed.

---

### 🟡 Cluster E: ₹18.53 cr — **Alias / same entity**

| Institute | Source |
|-----------|--------|
| Christian Medical College, Vellore | `IR-D-C-29209` |
| Christian Medical College | Same row — name variant |

**Fix:** Add `FUNDING_NAME_ALIASES` entry; display one canonical name.

---

### 🟡 Cluster F: ₹0.62 cr — **Entity confusion**

| Institute | Source |
|-----------|--------|
| Central University of Rajasthan | `IR-P-U-0392` — correct |
| University of Rajasthan | 0.852 fuzzy match to Central's row |

**Fix:** University of Rajasthan needs distinct NIRF row if ranked; else accept `null`.

---

## NIRF match losers — review (22)

### Reason breakdown

| Reason | Count |
|--------|-------|
| `no_fuzzy_match` | 20 |
| `id_blocked_by_uniqueness` | 2 |

### ✅ Accept gap (not in NIRF 2024 or no close row)

| Institute | Notes |
|-----------|-------|
| IIT Goa | Not in `nirf_rankings.csv` 2024 |
| Guru Nanak Dev University | Best sim 0.71 — below threshold |
| Dr. Hari Singh Gour University | Sim 0.64 |
| IACS Kolkata | Sim 0.53 — distinct research institute |
| G.S. Science, Arts And Commerce College | College-tier; not in master NIRF set |

### 🔧 Add override / improve matcher (clear NIRF row exists)

| Institute | NIRF row in CSV | ID | Action |
|-----------|-----------------|-----|--------|
| **SRM Institute of Science and Technology** | S.R.M. Institute of Science and Technology | `IR-O-U-0473` | Override — blocked by Madras false candidate |
| **GLA University** | G. L. A. University | `IR-P-U-0513` | Override — punctuation/spacing |
| **Thapar Institute** | Thapar Institute of Engineering and Technology | `IR-E-I-1480` | Override — name variant |
| **University of Rajasthan** | (distinct from Central Univ Rajasthan) | Search Pharmacy/Overall | Separate ID from `IR-P-U-0392` |
| **Mangalore University** | Mangalore University may exist | — | Improve matcher; don't match Bangalore Univ |

### ⚠️ Review manually (similar name, wrong best match in trace)

| Institute | Issue |
|-----------|-------|
| IIT Goa | Fuzzy picks IIT Ropar (0.94) — misleading; Goa not ranked |
| KIIT, GITAM, SASTRA, Shivaji | Private univs — may need NIRF 2024 scrape check |
| Saveetha, Pondicherry, Presidency | Below or near threshold — check `01b` gaps JSON |

### Blocked by uniqueness (2)

| Loser | Blocked by | Real NIRF row for loser? |
|-------|------------|--------------------------|
| SRM Institute of Science and Technology | IIT Madras (`IR-O-U-0456`) | **Yes** — `IR-O-U-0473` S.R.M. |
| University of Rajasthan | Central University of Rajasthan | **Maybe** — different entities in Jaipur |

---

## Fix applied (2026-07-07)

**Root cause:** `extract_distinguishing_tokens` stripped all tokens for IISc/IIT names via `NAME_STOP_TOKENS`; fuzzy join at ≥0.78 matched wrong institutes. PDF scrape rows were also dropped when master short names failed `funding_row_id_name_valid`.

**Changes:** `funding_campus_compatible()`, `FUNDING_NAME_ALIASES`, removed 0.78 fallback, `01e` uses NIRF canonical names, relaxed validation for aliased master names.

**Post-fix dashboard values (`2024_full.json`):**

| Institute | Before (corrupt) | After |
|-----------|------------------|-------|
| IISc | 197.08 (AIIMS) | **534.77** |
| IIT BHU Varanasi | 35.37 (Bhilai) | **206.94** |
| IIT Dhanbad | 12.24 (Dharwad) | **30.54** |
| AIIMS | 197.08 | 197.08 ✓ |
| IIT Delhi | — | 333.41 ✓ |
| IIT Madras | — | 592.22 ✓ |

Verification: **18/18 PASS**

---

## Re-run trace

```bash
python scripts/india_network/_debug_trace_funding_losers.py
```

Logs append to `debug-e78b43.log`.

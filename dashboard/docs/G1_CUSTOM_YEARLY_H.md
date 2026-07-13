# G1 custom yearly H: OpenAlex calendar-year cohort H

**Date:** 2026-07-12  
**Status:** Canonical custom metric (not SCImago).  
**River:** `CS661_Dataset/raw_vault/READY_FOR_TEAM/country_year_h_openalex_cohort.csv`  
**Owner row:** [`RIVER_OWNERS.md`](RIVER_OWNERS.md)

---

## Exact definition (locked)

**Country–year cohort H, window W = 1 (calendar year):**

For country \(C\) (ISO3) and year \(Y\):

1. Take all OpenAlex **works** with at least one authorship country = \(C\) (filter `authorships.countries:{ISO2}`) and `publication_year = Y`.
2. Let \(c_i\) be each work’s `cited_by_count` (**citation stock as of the OpenAlex extract / API pull date** — not cites received only in year \(Y\)).
3. Sort \(c_{(1)} \ge c_{(2)} \ge \cdots \ge c_{(N)}\).
4. Define
   \[
   H_{\text{cohort}}(C,Y) = \max\{ h : c_{(h)} \ge h \}
   \]
   (classic Hirsch h-index on that cohort). If \(N=0\), \(H=0\).

**Method label in CSV:** `openalex_cohort_W1_cited_by_count_stock`

This is **not** SCImago Country Rank H, **not** a lifetime / cumulative country H, and **not** the old G2 fiction `base + 2×(year−1999)`.

### Why W=1 (not W=5 trailing)

- Tractable API cost (one publication year per cell).
- Clear semantics: “among papers **published in year Y** with an author in C, what is the h-index of that cohort’s current citation stock?”
- Still **year-varying** (smoke: USA 2010 ≠ USA 2020).

A future **W=5 trailing** variant would use `publication_year` in \([Y-4, Y]\) and should get a new method label (`…_W5_…`) and a new river column — do not silently swap.

---

## What this is / is not

| Claim | Truth |
|-------|--------|
| SCImago yearly H | **No** — SCImago Country Rank repeats the same cumulative H in every year XLS (see [`G1_H_INDEX_YEARLY_OPTIONS.md`](G1_H_INDEX_YEARLY_OPTIONS.md)). |
| OpenAlex official “country H” | **No** — we compute it ourselves from works. |
| Lifetime quality stock | **No** — cohort of pubs in year \(Y\) only. |
| Fair across years without caveat | **No** — older cohorts have had more calendar time to accumulate cites (see Limitations). |
| G2 `h + 2×dy` animation | **Forbidden** — never revive. |

---

## Panel / pool columns

| Column | Meaning |
|--------|---------|
| `H_Index_SCImago` | Cumulative SCImago Country Rank H (flat across years). Audit / stock. |
| `H_Index_Yearly` | OpenAlex cohort H for that country–year (`W=1`). |
| `H_Index` | **Display / UMAP / G2 join field** = `H_Index_Yearly` when present; else `H_Index_SCImago` (partial coverage fallback — document coverage %). |

UI copy must say **“OpenAlex cohort H (pubs in year Y)”** for the yearly value, not “SCImago H”.

---

## Limitations (must stay visible)

1. **Citation stock, not same-age cites.** `cited_by_count` is total cites as of extract. A 2010 paper has ~15 more years of citation accumulation than a 2020 paper. Cohort H can **fall** for mature systems even when research quality does not (e.g. USA 2010 vs 2020 in smoke checks).
2. **Author-country filter.** Fractional / multi-country authorship is not de-duplicated beyond OpenAlex’s country tag on authorships; a work can count toward multiple countries.
3. **OpenAlex coverage / type mix.** All work types in the filter unless further restricted; not identical to SCImago “citable documents.”
4. **Partial roster.** If fetch is incomplete, uncovered country–years keep SCImago stock in `H_Index` — mixed scale until coverage is full. Check `method` / coverage notes in the river CSV and status script.
5. **API / budget.** Rate limits (HTTP 429) → key rotate + resume; never invent values.

---

## How it is computed (engineering)

- Script: `scripts/fetch_country_year_h_openalex.py`
- Status / resume: `scripts/status_country_year_h_openalex.py`
- Merge into panel + viz1: `scripts/merge_yearly_h_into_g1.py` (then `_regen_viz1_umap.py` when UMAP must re-embed)
- Cache: `CS661_Dataset/raw_vault/04_openalex/h_cohort_cache/{ISO3}_{YEAR}.json`
- Fetch strategy: works sorted `cited_by_count:desc`, `select=cited_by_count`, paginate until `c_{(k)} < k`; stop early — no need to download the full long tail.
- Keys: repo-root `.env` (`OPENALEX_API_KEY`, `_2`, `_3`, or `OPENALEX_API_KEYS`). **Never log key material.**

---

## Smoke expectations

| Cell | Expectation |
|------|-------------|
| USA 2010 vs USA 2020 | **Different** H (typically 2010 higher under stock cites). |
| IND 2010 vs IND 2020 | **Different** H. |
| USA ≫ small country same year | Order-of-magnitude sanity (not SCImago magnitudes). |

---

## Related

- Flat SCImago investigation: [`G1_H_INDEX_YEARLY_OPTIONS.md`](G1_H_INDEX_YEARLY_OPTIONS.md)
- River ownership: [`RIVER_OWNERS.md`](RIVER_OWNERS.md)

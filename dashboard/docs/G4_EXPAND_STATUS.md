# G4 Expand Status

**Updated:** 2026-07-12 21:39 India Standard Time
**Live pool countries:** 73 (core20=20, expanded=+53)
**Years:** 2010–2024
**Credits remaining (last check):** 7884
**Stop reason:** completed_targets

## API keys

Keys live only in repo-root `.env` (gitignored): `OPENALEX_API_KEY`, `OPENALEX_API_KEY_2`, `OPENALEX_API_KEY_3`, and/or `OPENALEX_API_KEYS`. The expand script rotates on HTTP 429 / low daily credits. **Never** commit keys or paste them into docs/JS/zips.

## Why the old 111 was unverified

The old FE (`viz4_data_BEFORE_POOLFIX.js`) was an **undated snapshot** of 111 countries. Most of those countries have **zero rows** in `collaboration_premium.csv`. Even for the overlapping 20, FE scalars do not match any single premium year. It must **not** be revived as live data.

## Where backed data comes from

OpenAlex Works API (same recipe as `G4_RECOVERY_PLAN.md`):

- Domestic: `institutions.country_code:{ISO2},countries_distinct_count:1,publication_year:{Y}`
- International: `...countries_distinct_count:>1...`
- Metric: **population** mean of `cited_by_count` (all work types)
- Method: `group_by=cited_by_count` + high-cite tail; full cursor if residual gap

## Completed expanded countries (full 2010–2024)

- `AE` — United Arab Emirates
- `AF` — Afghanistan
- `AR` — Argentina
- `AT` — Austria
- `BD` — Bangladesh
- `BE` — Belgium
- `BG` — Bulgaria
- `BT` — Bhutan
- `CL` — Chile
- `CO` — Colombia
- `CR` — Costa Rica
- `CZ` — Czechia
- `DK` — Denmark
- `EC` — Ecuador
- `EG` — Egypt
- `ET` — Ethiopia
- `FI` — Finland
- `GH` — Ghana
- `GR` — Greece
- `HK` — Hong Kong
- `HR` — Croatia
- `HU` — Hungary
- `IE` — Ireland
- `IL` — Israel
- `KE` — Kenya
- `LK` — Sri Lanka
- `LU` — Luxembourg
- `MA` — Morocco
- `MV` — Maldives
- `MX` — Mexico
- `MY` — Malaysia
- `NG` — Nigeria
- `NO` — Norway
- `NP` — Nepal
- `NZ` — New Zealand
- `PE` — Peru
- `PH` — Philippines
- `PK` — Pakistan
- `PT` — Portugal
- `QA` — Qatar
- `RO` — Romania
- `RS` — Serbia
- `SA` — Saudi Arabia
- `SG` — Singapore
- `SI` — Slovenia
- `SK` — Slovakia
- `TH` — Thailand
- `TN` — Tunisia
- `TW` — Taiwan
- `UA` — Ukraine
- `UY` — Uruguay
- `VN` — Vietnam
- `ZA` — South Africa

## Still missing / pending from expand list

*(none — expand candidate list for this session is complete.)*

Toward the old unverified 111: many remaining countries still need overnight/API or OpenAlex dump regen. Do **not** fill gaps from `viz4_data_BEFORE_POOLFIX.js`.

```powershell
# Continue expanding more ISO codes by appending to EXPAND in scripts/expand_g4_openalex.py
# then:
python scripts/expand_g4_openalex.py --max-new 20
```


- River (live): `CS661_Dataset/collaboration_premium.csv`
- River (READY_FOR_TEAM): `CS661_Dataset/raw_vault/READY_FOR_TEAM/collaboration_premium.csv`
- Expanded copy: `CS661_Dataset/raw_vault/READY_FOR_TEAM/collaboration_premium_expanded.csv`
- Cache (resume): `CS661_Dataset/raw_vault/g4_expand_cache.json`
- Pool: `dashboard/viz4_data.js`

## How to continue overnight

```powershell
cd C:\Users\brata\Downloads\CS661
python scripts/expand_g4_openalex.py
# optional: limit how many NEW countries to attempt this run
python scripts/expand_g4_openalex.py --max-new 15
```

Script resumes from `g4_expand_cache.json`. When daily OpenAlex credits reset (see `resets_in_seconds` on `/rate-limit`), re-run until pending countries reach `{have}/{years}` = full. Then pool rebuild is automatic at end of run.

## Integrity rules

- Do **not** load `viz4_data_BEFORE_POOLFIX.js` as live data.
- Do **not** invent means; only cache-backed population rows enter the river.
- Incomplete countries (partial years) stay in cache only — not in live pool.


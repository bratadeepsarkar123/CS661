# Module 5 verification checklist

Generated: 2026-07-08T03:51:23.578803+00:00
**23/23 passed**

- [PASS] institution_master rows + geo: 120 rows, 100% with lat/lon
- [PASS] collaboration_edges weight>=2: 13236 edge rows
- [PASS] edge endpoints in master (domestic IN institutions): all endpoints in institution_master
- [PASS] overview size: 32466 bytes
- [PASS] full size: 412790 bytes (cap 1953 KB)
- [PASS] SCImago static year footnote: SCImago research impact % snapshot (2019 data); static across year slider
- [PASS] overview payload edge integrity: 0 orphan edges (nodes=45, edges=40)
- [PASS] full payload edge integrity: 0 orphan edges (nodes=120, edges=300)
- [PASS] year slice manifest: 10 years listed in manifest.json
- [PASS] campus coordinate stacks: max stack=1, out_of_india=0
- [PASS] domestic_works.parquet non-empty: 108705 rows, 1252 KB
- [PASS] NIRF funding coverage: 104 / 120 institutions with research_funding_cr
- [PASS] funding ID/name corruption guard: no suspect funding
- [PASS] major IIT funding present: all major IITs funded
- [PASS] duplicate funding value clusters: no duplicate funding values
- [PASS] positive domestic co-auth test: IIT Kanpur ↔ IIT Delhi edge weight=234 in collaboration_edges_full.csv
- [PASS] negative foreign co-auth test: foreign co-auth work W3044674088 correctly excluded from domestic_works
- [PASS] temporal edge variance (2015 vs 2022): 2015 weight sum=7184, 2022 weight sum=20139
- [PASS] year-aware funding variance (2020 vs 2023 JSON): 103 institutes with different funding 2020 vs 2023 slices (e.g. Indian Institute of Science: 525.722 vs 534.773 cr)
- [PASS] year-aware NIRF rank variance (2020 vs 2023 JSON): 95 institutes with different NIRF rank 2020 vs 2023 slices (e.g. University of Delhi: #18 vs #22)
- [PASS] 2024 slice is true calendar year: 2024_full.json year field=2024
- [PASS] NIRF coverage gap report: funding 104/120, patents 55/120
- [PASS] AISHE xlsx validation: optional file missing
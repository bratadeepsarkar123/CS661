# Module 5 verification checklist

Generated: 2026-07-01T03:20:50.494707+00:00
**11/11 passed**

- [PASS] institution_master rows + geo: 120 rows, 100% with lat/lon
- [PASS] collaboration_edges weight>=2: 13236 edge rows
- [PASS] edge endpoints in master (domestic IN institutions): all endpoints in institution_master
- [PASS] overview size: 29878 bytes
- [PASS] full size: 102972 bytes
- [PASS] SCImago static year footnote: SCImago research impact % snapshot (2019 data); static across year slider
- [PASS] domestic_works.parquet non-empty: 108705 rows, 1252 KB
- [PASS] NIRF funding coverage: 116 / 120 institutions with research_funding_cr
- [PASS] positive domestic co-auth test: IIT Kanpur ↔ IIT Delhi edge weight=234 in collaboration_edges_full.csv
- [PASS] negative foreign co-auth test: foreign co-auth work W3044674088 correctly excluded from domestic_works
- [PASS] temporal edge variance (2015 vs 2022): 2015 weight sum=7184, 2022 weight sum=20139
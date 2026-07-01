# Module 5 verification checklist

Generated: 2026-07-01T04:42:51.670168+00:00
**15/15 passed**

- [PASS] institution_master rows + geo: 120 rows, 100% with lat/lon
- [PASS] collaboration_edges weight>=2: 13236 edge rows
- [PASS] edge endpoints in master (domestic IN institutions): all endpoints in institution_master
- [PASS] overview size: 29493 bytes
- [PASS] full size: 102535 bytes
- [PASS] SCImago static year footnote: SCImago research impact % snapshot (2019 data); static across year slider
- [PASS] overview payload edge integrity: 0 orphan edges (nodes=45, edges=40)
- [PASS] full payload edge integrity: 0 orphan edges (nodes=80, edges=200)
- [PASS] year slice manifest: 10 years listed in manifest.json
- [PASS] campus coordinate stacks: max stack=1, out_of_india=0
- [PASS] domestic_works.parquet non-empty: 108705 rows, 1252 KB
- [PASS] NIRF funding coverage: 116 / 120 institutions with research_funding_cr
- [PASS] positive domestic co-auth test: IIT Kanpur ↔ IIT Delhi edge weight=234 in collaboration_edges_full.csv
- [PASS] negative foreign co-auth test: foreign co-auth work W3044674088 correctly excluded from domestic_works
- [PASS] temporal edge variance (2015 vs 2022): 2015 weight sum=7184, 2022 weight sum=20139
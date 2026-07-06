# NIRF Data Acquisition Log

**Internal team memory — not for dashboard.**

Marathon started: 2026-07-07T21:31:26Z

## Sections
- Live nirfindia.org probes
- Wayback Machine (2016–2017 rankings)
- PDF CDN season probes (Innovation / Overall / Engineering)
- data.gov.in / government portals
- NIRF press / MoE releases
- Third-party mirrors (reference only)
- Common Crawl / Internet Archive bulk search
- Manual CSV drops

| Timestamp (UTC) | Method | Source/URL | Script | Rows | Status | Why failed | Next retry |
|-----------------|--------|------------|--------|------|--------|------------|------------|
| 2026-07-07T21:31:26Z | Marathon start | run_acquisition_marathon.py | run_acquisition_marathon.py | 0 | partial | — | — |
| 2026-07-07T21:31:42Z | Live nirfindia.org ranking probe | nirfindia.org/Rankings/{2015..2025}/OverallRanking.html | scrape_nirf_press.py | 0 | partial | 404 years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025] | Wayback for 2016-2017; live for 2018+ |
| 2026-07-07T21:31:44Z | NIRF press / discovery | https://www.nirfindia.org/ | scrape_nirf_press.py | 10 | success | — | — |
| 2026-07-07T21:31:45Z | NIRF press / discovery | https://www.nirfindia.org/Rankings/ | scrape_nirf_press.py | 0 | fail | fetch failed | — |
| 2026-07-07T21:31:47Z | NIRF press / discovery | https://www.nirfindia.org/News/ | scrape_nirf_press.py | 0 | fail | fetch failed | — |
| 2026-07-07T21:31:49Z | NIRF press / discovery | https://www.nirfindia.org/PressRelease/ | scrape_nirf_press.py | 0 | fail | fetch failed | — |
| 2026-07-07T21:31:50Z | NIRF press / discovery | https://www.nirfindia.org/sitemap.xml | scrape_nirf_press.py | 347 | success | — | — |
| 2026-07-07T21:31:52Z | NIRF press / discovery | https://www.nirfindia.org/robots.txt | scrape_nirf_press.py | 0 | fail | fetch failed | — |
| 2026-07-07T21:31:53Z | NIRF press / discovery | https://www.education.gov.in/en/nirf | scrape_nirf_press.py | 0 | fail | fetch failed | — |
| 2026-07-07T21:31:56Z | NIRF press / discovery | https://pib.gov.in/Search.aspx?Search=NIRF | scrape_nirf_press.py | 0 | fail | fetch failed | — |
| 2026-07-07T21:35:56Z | Wayback Machine | nirfindia.org/Rankings/2016/ | wayback_nirf_rankings.py | 0 | fail | Overall: no CDX snapshots; University: no CDX snapshots; College: no CDX snapshots; Research: no CDX snapshots; Engineering: no CDX snapshots; Management: no CDX snapshots; Pharmacy: no CDX snapshots; Medical: no CDX snapshots; Dental: no CDX snapshots; Law: no CDX snapshots; Architecture: no CDX snapshots; Agriculture: no CDX snapshots; Innovation: no CDX snapshots | Try Internet Archive bulk search or alternate snapshot dates |
| 2026-07-07T21:39:20Z | Wayback Machine | nirfindia.org/Rankings/2017/ | wayback_nirf_rankings.py | 0 | fail | Overall: snapshots exist but parse=0; University: snapshots exist but parse=0; College: snapshots exist but parse=0; Research: no CDX snapshots; Engineering: no CDX snapshots; Management: snapshots exist but parse=0; Pharmacy: no CDX snapshots; Medical: no CDX snapshots; Dental: no CDX snapshots; Law: no CDX snapshots; Architecture: no CDX snapshots; Agriculture: no CDX snapshots; Innovation: no CDX snapshots | Try Internet Archive bulk search or alternate snapshot dates |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2015/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2016/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2017/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2018/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2019/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2020/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2021/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2022/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2023/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn/2024/pdf/ | probe_nirf_cdn.py | 0 | fail | No PDFs >500B for sample IDs | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:47:47Z | PDF CDN probe | nirfpdfcdn aggregate | probe_nirf_cdn.py | 0 | partial | — | — |
| 2026-07-07T21:47:50Z | data.gov.in search | data.gov.in?q=NIRF | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:47:52Z | data.gov.in search | data.gov.in?q=National Institutional Ranking Framework | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:47:54Z | data.gov.in search | data.gov.in?q=MHRD university | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:47:55Z | data.gov.in search | data.gov.in?q=Ministry of Education higher education | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:47:57Z | data.gov.in search | data.gov.in?q=R&D expenditure university | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:47:59Z | data.gov.in search | data.gov.in?q=patents granted university India | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:48:01Z | data.gov.in search | data.gov.in?q=UGC research projects | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:48:03Z | data.gov.in search | data.gov.in?q=AISHE | probe_data_gov.py | 0 | fail | No packages in CKAN search | Try manual portal browse; RTI for institute-level funding |
| 2026-07-07T21:48:03Z | data.gov.in search | data.gov.in aggregate | probe_data_gov.py | 0 | fail | All queries returned 0 | Metadata saved for manual review; no institute-level NIRF CSV found automatically |
| 2026-07-07T21:48:11Z | Common Crawl index | index.commoncrawl.org/nirfindia.org/nirfpdfcdn | run_acquisition_marathon.py | 0 | fail | No indexed nirfpdfcdn URLs in recent collections (or API limit) | Download CC index for full URL list; cross-check CDN probe |
| 2026-07-07T21:48:11Z | Third-party mirror | https://www.shiksha.com/university/ranking | run_acquisition_marathon.py | 0 | fail | Aggregator; institute ID mapping unreliable; legal/attribution unclear for ingestion | Manual spot-check only; do not ingest without IR-* ID crosswalk |
| 2026-07-07T21:48:11Z | Third-party mirror | https://www.careers360.com/university/ranking | run_acquisition_marathon.py | 0 | fail | Category/year coverage incomplete; no IR-* IDs | Manual spot-check only; do not ingest without IR-* ID crosswalk |
| 2026-07-07T21:48:11Z | Third-party mirror | https://dataful.in/datasets/19320/ | run_acquisition_marathon.py | 0 | partial | Used by 01_download_sources; IDs unreliable for funding join | Manual spot-check only; do not ingest without IR-* ID crosswalk |
| 2026-07-07T21:48:12Z | Funding cross-ref on disk | data/raw/nirf_research_projects*.csv | run_acquisition_marathon.py | 6 | fail | 2023-24 academic year absent from all scraped PDF seasons | Probe 2025 ranking season PDFs when published; re-run 01e on new CDN |
| 2026-07-07T21:48:15Z | Internet Archive bulk search | archive.org?q=collection:web AND nirfindia.org AND Rankings AND 2016 | run_acquisition_marathon.py | 0 | fail | No IA items matching 2016 ranking query | Use wayback CDX per-category URLs (primary path) |
| 2026-07-07T21:52:34Z | Wayback Machine | nirfindia.org/Rankings/2017/ | wayback_nirf_rankings.py | 500 | success | — | — |
| 2026-07-07T21:58:48Z | Marathon start | run_acquisition_marathon.py | run_acquisition_marathon.py | 0 | partial | — | — |
| 2026-07-07T21:59:06Z | PDF CDN probe | nirfpdfcdn/2019/pdf/ | probe_nirf_cdn.py | 20 | success | — | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:59:06Z | PDF CDN probe | nirfpdfcdn/2020/pdf/ | probe_nirf_cdn.py | 20 | success | — | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:59:06Z | PDF CDN probe | nirfpdfcdn/2021/pdf/ | probe_nirf_cdn.py | 22 | success | — | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:59:06Z | PDF CDN probe | nirfpdfcdn/2022/pdf/ | probe_nirf_cdn.py | 20 | success | — | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:59:06Z | PDF CDN probe | nirfpdfcdn/2023/pdf/ | probe_nirf_cdn.py | 21 | success | — | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:59:06Z | PDF CDN probe | nirfpdfcdn/2024/pdf/ | probe_nirf_cdn.py | 24 | success | — | Expand sample IDs; GET full Innovation PDF for patent year columns |
| 2026-07-07T21:59:07Z | Legacy PDF CDN | nirfpdfcdn/2016/IR16-*.pdf | probe_legacy_cdn.py | 0 | fail | Legacy flat PDF path 404 or not in wayback HTML | Parse funding tables from legacy PDFs if Overall contains sponsored research |
| 2026-07-07T22:00:03Z | Legacy PDF CDN | nirfpdfcdn/2017/IR17-*.pdf | probe_legacy_cdn.py | 40 | success | — | Parse funding tables from legacy PDFs if Overall contains sponsored research |
| 2026-07-07T22:00:30Z | Pipeline integration | scripts/india_network pipeline | run_acquisition_marathon.py | 0 | partial | — | — |
| 2026-07-07T22:05:05Z | Pipeline integration | scripts/india_network pipeline | run_acquisition_marathon.py | 0 | partial | — | — |
| 2026-07-07T22:09:31Z | Live nirfindia.org | nirfindia.org/Rankings/2016/ | wayback_nirf_rankings.py | 500 | success | — | — |
| 2026-07-07T22:11:55Z | Pipeline integration | scripts/india_network pipeline | run_acquisition_marathon.py | 0 | partial | — | — |

---

## Final coverage summary (2026-07-08 marathon)

| Metric | Year / range | Source | Status | Rows recovered this run |
|--------|--------------|--------|--------|-------------------------|
| **NIRF ranks** | 2015 | nirfindia.org live + Wayback CDX | **tried-failed** | 0 — not published |
| **NIRF ranks** | 2016 | Live GET `Rankings/2016/` | **have** | **500** (`nirf_rankings_2016.csv`) |
| **NIRF ranks** | 2017 | Wayback + live IR17 parser | **have** | **500** (`nirf_rankings_2017.csv`) |
| **NIRF ranks** | 2018–2024 | Prior pipeline + live | **have** | 0 new (already on disk) |
| **Funding** | 2017-18 … 2022-23 | PDF CDN 2021–2024 seasons | **have** | 0 new |
| **Funding** | 2023-24 | All scraped PDF seasons | **tried-failed** | 0 — absent from PDFs |
| **Funding** | pre-2017-18 | Legacy flat CDN 2017 | **tried-failed** | 0 — PDFs exist (~6KB) but no parseable tables |
| **Patents** | 2020–2022 | Innovation PDF 2024 CDN only | **have** | 0 new |
| **Patents** | 2019–2023 CDN | `probe_nirf_cdn.py` GET | **tried-failed** | Innovation 404 on 2019–2023; Overall/Engineering OK |
| **Patents** | pre-2020 | All methods | **tried-failed** | No Innovation PDF path |
| **data.gov.in** | all queries | CKAN API | **tried-failed** | 0 institute-level CSV |
| **Third-party** | Shiksha, Careers360 | Reference only | **not ingested** | 0 |
| **Common Crawl / IA bulk** | nirfpdfcdn | Index APIs | **tried-failed** | 0 indexed hits in sample |

**Verification after integration:** 23/23 PASS (`10_verification_checklist.py`)

**Re-run tomorrow:**
```bash
python scripts/india_network/acquisition/run_acquisition_marathon.py --integrate
```

**Key scripts:** `acquisition/wayback_nirf_rankings.py`, `probe_nirf_cdn.py`, `probe_legacy_cdn.py`, `probe_data_gov.py`, `scrape_nirf_press.py`, `run_acquisition_marathon.py`

**Machine-readable log:** `data/logs/nirf_acquisition_attempts.json`  
**Coverage:** `data/logs/nirf_historical_coverage.json`

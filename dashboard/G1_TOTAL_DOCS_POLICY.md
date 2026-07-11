# Why World Bank article counts ≪ OpenAlex works

Graph 1 bubble size (`Total_Docs`) must use **one** publication definition across years.

| Source | What it counts | Typical USA scale |
|--------|----------------|-------------------|:|
| **World Bank** `IP.JRN.ARTC.SC` | Scientific & technical **journal articles** (narrow, curated flow) | ~430–470k / year |
| **SCImago Country Rank** `Documents` | Indexed **documents** in the SCImago/Scopus country view (broader than WB journals, still “documents”) | ~750k / year for USA |
| **OpenAlex** country works | Nearly all scholarly **works** (articles, preprints, books, datasets, etc.) | ~1.2–1.7M / year for USA |

Mixing WB (≤2022) with OpenAlex (2023–24) caused a fake ~3× cliff for most countries — not real growth.

**Policy now:** `Total_Docs` = WB whenever present; else SCImago Documents; **never** OpenAlex. `OA_Docs` may remain as a side column for research, but it does not feed bubble size or UMAP.

**Honest caveat:** When WB ends (no 2024 WDI value yet), 2024 bubbles use SCImago Documents. SCImago sits above WB for many countries, so **2023→2024** can still step up once — that is a known source change (WB→SCImago), not OpenAlex inflation. Prefer extending WB when WDI publishes 2024.

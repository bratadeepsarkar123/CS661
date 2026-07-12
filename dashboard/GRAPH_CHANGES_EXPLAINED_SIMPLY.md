# Graph changes explained simply

**Date:** 2026-07-12  
**Audience:** Anyone confused about “why did the dashboard numbers move?”  
**No code changes in this document** — explanation only.

**One metaphor (used once):** Think of the vault CSVs as a **river** (source of truth), the bundled `dashboard/*_data.js` files as a **pool** (what the charts drink from), and the HTML/labels/filters as a **tap** (how the UI frames what you see). We fixed the pool so it matches the river. The tap (wording and some filters) is still partly your teammate’s job.

---

## TL;DR for the whole dashboard

1. Four of five charts got **corrected data files**; Graph 5 was already fine.
2. Old pools often **looked polished but measured the wrong thing** (wrong H-index scale, capped ratios, Quantum = Materials Science, 111 fake countries).
3. After refresh, numbers and layouts will **look different** — that is honesty, not breakage of the river.
4. Some UI labels/filters may still **speak the old story** until the teammate updates the tap.
5. For viva: **river = authority**; pool is now mostly aligned; leftover work is mostly wording and topic IDs in the UI.

---

### Graph 1 — Peer clusters (UMAP)

**In one sentence:** Countries as bubbles over time, placed so neighbors look similar on wealth, R&D, publication volume, and research quality (H-index).

**What was it before?**  
We told people each country had a real SCImago-style quality H-index. The pool file disagreed: USA’s H for 2022 was **53** (a tiny stub scale), not the real SCImago country stock (**3388**). China / India / UK 2022 were on that same wrong scale. Bubble positions (`x`, `y`) came from a UMAP run trained on that bad H, so “who sits near whom” was misleading.

**How did it function then?**  
You scrubbed a year slider; Plotly drew bubbles that drifted and clustered. A user reasonably thought: “I’m seeing peer groups on true quality + wealth + pubs.” In reality, quality was on the wrong yardstick, so the map of peers was skewed (USA looked like a tiny-H outlier for the wrong reason).

**What is it now?**  
`H_Index` is joined from the real features panel (~5966 rows fixed). USA 2022 = **3388**; China / India / UK 2022 = **1595 / 1001 / 2183**. UMAP `x,y` was regenerated for **4196 of 6022** rows; **1826** sparse rows still keep old coordinates. Spot-check: USA 2022 moved from about `(−0.31, −11.78)` to about `(6.04, 6.11)`.

**How is it functioning now?**  
Same slider and bubble chart, but clusters will **look different** after refresh. That is expected: we fixed the feature that drove the layout, then re-embedded. Some years/countries with incomplete inputs may still sit on leftover old coords. Credits may still over-say “OpenAlex” alone.

**Why we changed it:**  
A “quality” number of 53 for the USA was not the SCImago stock we claimed. Leaving bad H in place kept peer neighborhoods wrong. Fixing H without moving UMAP would still leave a map trained on the lie. So we corrected the numbers and re-ran the layout for most points.

**What your teammate still must fix in the UI (tap):**
- Credit line: World Bank (GDP, GERD, journal articles) · SCImago Country Rank (H-index; Documents fallback) · UMAP — OpenAlex is **not** used for G1 bubble size (see `G1_TOTAL_DOCS_POLICY.md`)
- Tooltip: H is a **country quality stock** (flat across years in our panel), not a single-year H
- Re-check Plotly axis ranges / smoothing after the coordinate move

---

### Graph 2 — Q1 vs Q4 quality mix (ridgeline)

**In one sentence:** For each country–year, how much of the journal output hosted there is top-tier (Q1) versus bottom-tier (Q4), via the Q1/Q4 ratio.

**What was it before?**  
The pool had ~country–year Q1/Q4 counts that looked OK for big anchors (USA, China, India, UK) in places, but **`ratio` was capped at 5.0** (so USA/UK 2022 were flattened to look less extreme than they are). Some non-anchor rows drifted (e.g. Argentina 1999 was wrong). UI copy often sounded like **author country** (“where researchers publish from”).

**Simple analogy — publisher country vs author country:**  
**Bookstore location vs customer home address.** Graph 2 counts books by **which country’s bookstore published them** (SCImago journal `Country`), not by **where the shoppers live**. A Nature paper can count toward the UK even if every author is in India; an Indian-published Q4 journal counts for India even if coauthors are abroad. This chart is about **where elite vs low-tier journals are hosted**, not where authors live.

**How did it function then?**  
Year slider + ridgeline / bars of Q1 vs Q4 (and a ratio). Users thought they were seeing “research quality by country of researchers.” Caps hid how extreme elite publisher countries really are (true UK 2022 ratio ≈ **25**, not 5).

**What is it now?**  
Rebuilt from the river CSV: **2705** country–years, 1999–2024, **uncapped** `ratio`. USA 2022: q1 **530553**, q4 **35612**, total **834932**, ratio **14.898152**. Argentina 1999: **q1=0, q4=303, ratio=0** (was wrongly 259/1555/0.167). UK 2022 ratio ≈ **25.16**.

**How is it functioning now?**  
Same chart chrome; bars/ridges will stretch higher for elite publisher countries. If labels still say “authors” or “researchers’ countries,” the **picture is right for publisher country but the words are still wrong** until the tap is updated. Optional on-screen cap at 5 is a display choice only — the pool must stay uncapped.

**Why we changed it:**  
We needed the dashboard numbers to match the vault CSV exactly, including true ratios. Capping in the data file lied about how Q1-heavy some publisher countries are. We also locked the meaning: this series is publisher-country journal output, not a rebuilt author-affiliation story we never shipped.

**What your teammate still must fix in the UI (tap):**
- Rewrite any author / “where researchers publish from” copy → **journal publisher country**
- Prefer: “Q1 vs Q4 documents by journal publisher country”
- If bars look too tall, optional display-only `min(5, ratio)` — **do not** re-cap the pool file
- Read the G2 publisher schema note before changing filters

---

### Graph 3 — Topic × country × year research volume

**In one sentence:** How much research volume each country produces over time in selected topics (AI, Quantum, CRISPR, etc.).

**What was it before?**  
Old pool used **ASJC-like** numeric subfield IDs. Quantum was coded **`2500`**, which in that scheme means **Materials Science** — wrong and forbidden for a “Quantum Computing” chart. The old front-end felt denser (~**48k** rows, often 1950–2025) than the OpenAlex extract we actually have.

**How did it function then?**  
Topic picker + country/year views (bars/bubbles/heat depending on the viz). A user selecting “Quantum Computing” was, under the hood, filtering a Materials Science–style id. Early years looked fuller than our real OpenAlex pull justified.

**What is it now?**  
Rebuilt to **26 609** rows from OpenAlex concepts. Quantum id = **`C58053490`**. Dashboard-friendly `topic_name` labels kept (`AI & Machine Learning`, `Quantum Computing`, …) so name-based filters still work. Coverage: AI **1950–2024**; Quantum and most others mainly **2000–2024**; some early Infectious / other topics still thin (API limits).

**How is it functioning now?**  
Topic **names** still work. Hard-coded numeric filters like **`2500` / `1702`** against the new pool will break or miss data. Pre-2000 will look thinner than the old fake-dense series — that is the real extract, not a regression of the river. Quantum gradient keys named like “materials” are still misleading until renamed.

**Why we changed it:**  
Calling Materials Science “Quantum” is a factual error, not a style choice. We aligned the pool to real OpenAlex concept IDs and the extract we can defend. Thinner early years beat inventing dense history we did not fetch.

**What your teammate still must fix in the UI (tap):**
- Replace hard-coded ASJC numbers with OpenAlex `C…` ids (Quantum **`C58053490`**, AI `C154945302`, etc.)
- Rename Quantum styling keys away from “materials”
- Year credit: do not claim full 1950–2025 for every topic
- Prefer `topic_name` or new ids — not numeric `2500`

---

### Graph 4 — Collaboration premium (domestic vs international cites)

**In one sentence:** For each country, how much higher average citations are for international vs domestic collaboration (the “premium”).

**What was it before?**  
The pool showed **111** countries with **no year attached**. Those numbers did **not** match any single year of our real collaboration-premium CSV. **91** of those countries had **no river justification at all**. USA looked like domestic / intl / gain ≈ **16.9 / 24.3 / 7.4**. People could think this was a complete “agreed company” world list — it wasn’t; it was an unjustified undated snapshot.

**How did it function then?**  
Bars or paired values comparing domestic vs international mean cites and a gain. Users thought they were seeing a broad, authoritative multi-country premium ranking. Absolute levels and country count were inflated relative to what we can source.

**What is it now?**  
**20** countries, **year 2024 only**, rebuilt from `collaboration_premium.csv`. USA ≈ **3.0 / 6.3 / 3.3** (domestic / international / gain). Russia naming cleaned where needed. Smaller list, dated, matchable to the vault.

**How is it functioning now?**  
Same chart type, fewer countries, lower absolute cite levels than the old 111-country picture. If the UI still implies “100+ countries” or an undated world census, that framing is outdated even though the pool is honest.

**Why we changed it:**  
**20 countries for 2024 is MORE honest than 111 undated.** The 111 were not “agreed company data” — most had no backing file, and the values didn’t line up with any year of the real premium extract. Shrinking the chart to what we can prove beats a impressive-looking fake globe.

**What your teammate still must fix in the UI (tap):**
- Do not imply 100+ countries; say **20 countries, 2024**
- Expect absolute cite levels to differ from the old snapshot (expected)
- Do not restore 111 without a documented new extract

---

### Graph 5 — India higher-education collaboration network

**In one sentence:** A map/network of Indian HE institutions and their collaboration links over years.

**What was it before?**  
Claimed pipeline data plus India outline for the network map — and the pool already matched that story on spot-check.

**How did it function then?**  
Year / network views over India with institution nodes and edges; outline geo for the map. Users saw the India HE collaboration graph as designed.

**What is it now?**  
**Essentially unchanged.** Outline is byte-identical to the river handoff; network JSON set (manifest + yearly / all-years) was already present and aligned. No pool rewrite in this consolidation pass.

**How is it functioning now?**  
Same as before for pool purposes. Any remaining polish is label/footnote wording (static vs cumulative fields), not a data-file swap.

**Why we changed it:**  
We didn’t — there was nothing to consolidate. Graph 5 already matched the handoff, so leaving it alone avoided pointless churn.

**What your teammate still must fix in the UI (tap):**  
Nothing for pool. Optional label/footnote polish for static vs cumulative fields only.

---

## What this consolidation did *not* do

- No tap edits required of you from this doc (`app.js` / HTML / CSS remain teammate-owned for the checklist above).
- No author-country rebuild for Graph 2 (locked as publisher-country).
- Graph 3 early-year backfill still pending when OpenAlex budget allows.
- Graph 1: 1826 UMAP leftover rows may still sit on old coords until denser impute or drop.

## Proof anchors (after the pool fix)

| Check | Result |
|-------|--------|
| G1 USA 2022 `H_Index` | **3388** |
| G2 USA 2022 `ratio` | **14.898152** (uncapped) |
| G3 Quantum id | **`C58053490`** |
| G4 country count | **20** (2024) |
| G5 outline | Unchanged / matches river |

**Related files:** `PER_GRAPH_POOL_CHANGELOG.md` · `SEMANTICS_DECISION.md` · `TEAMMATE_CHANGE_REPORT.md` · `POOL_VS_RIVER_DISCREPANCIES.md` · handoff folder `READY_FOR_TEAM/`

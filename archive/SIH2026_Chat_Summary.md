# SIH 2026 — Problem-Statement Selection: Chat Summary

**Team:** 6 people — **1 full-stack developer + 5 members** (non-coders).
**Hard constraint:** software only; **no intensive model training**; no proprietary dataset collection; no hardware.
**Source data:** `SIH2026_All_Problem_Statements.doc` — 226 entries = 192 real statements (155 Software, 37 Hardware) + 34 AICTE "Student Innovation" open-idea placeholders (ignored).
**Date:** 2026-08-23.

**Deliverables produced (Claude artifacts):**
- The One-Developer Filter (criteria) — https://claude.ai/code/artifact/29900616-9e5f-46bf-8daa-27c105cd76f2
- Twelve, Three, One (first screen, from PDFs/titles) — https://claude.ai/code/artifact/8e82fd94-5651-44c9-90bd-a6b24eecb7e7
- **SIH 2026 Shortlist Dossier (final, full deep-dives)** — https://claude.ai/code/artifact/8349f8f3-c64f-4f1c-9aad-f2cdcfca1138

---

## 1. The core idea

With **one developer**, the real budget is **surface area, not difficulty**. One good dev can build one hard thing well; what kills a 1-dev team is *breadth* (many screens, roles, integrations). So the filter is: **pick statements where the value sits in one core engine + a thin UI**, not "a complete system for X."

The no-training constraint is not a weakness — it is a **filter that points at two statement shapes SIH 2026 rewards**: **rules/compliance engines** and **optimisation**. Both are engineering, not ML. A rules engine proves itself clause-by-clause; a solver returns a proof of optimality. Those survive judge questioning; "the model said so" / "the LLM said so" does not.

---

## 2. What to look for in a PS (the criteria we built)

1. **Is the hard part one module?** (concentrated value, not a platform)
2. **Can a 70%-built version still demo?** (graceful degradation, not all-or-nothing)
3. **Does the output prove itself?** (optimality proof / standards conformance / verifiable calc — not an accuracy % you can't defend without an ML specialist)
4. **Does the domain need an expert nobody has?** (weather, DSP, orbital, clinical → drop)
5. **What fraction of work is non-code?** (rules/circulars/standards = load-bearing work your 5 members can own — actively hunt for this)
6. **Does the data exist, or are you inventing it?** (proprietary corpus you'll never get → dead; statement that enumerates its own inputs → synthetic data is valid method)
7. **Does it demo offline on one laptop?** (no live gov API, no multi-service deploy, no device)
8. **How crowded is it?** (500-team cap per PS; unglamorous compliance/optimisation = thin crowds)
9. **Does the sponsor actually want it?** (specific, operational statement = engaged mentor)
10. **Can you explain the problem in 60 seconds?**
11. **Does the dev already know the stack?** (no learning a new language/framework)

**Instant no:** needs hardware; needs sponsor-only data; core is training a model from scratch; reads as "build us a portal/ERP/management system"; needs a live system you can't access; needs specialist domain knowledge nobody has.

---

## 3. Three lenses added during the chat

**Data → Intelligence → Decision → Action pipeline.** Every PS fits it, so it's a *diagnostic*, not a filter. Ask **which stage carries the cost**:
- DATA = grind that scales with headcount → want it handed to you
- INTELLIGENCE = fine if pretrained/API, fatal if train-your-own
- **DECISION = solvers/rules/scoring/simulation → small code, high cleverness → your target**
- ACTION = a plan/report/dispatch → cheap to build, huge for the pitch (and where teams bluff — make it real)

**The 5 SIH-2026 "patterns" verdict (from the DecodeX slides):**
- Agents → **build here** (orchestration is engineering)
- Multimodal → **conditional** (off-the-shelf models only)
- Domain-specific models (fine-tuned LLMs/LSTMs/GNNs) → **reject** (exactly what you can't do)
- Data fusion → **conditional** (deterministic overlay/rules yes; learned fusion no; cap at 3 sources)
- Edge AI → **reject** (quantisation/RAM budgets = specialist + hardware)
- Real-world systems (Pattern 5) → **build here** — its own "decision engine" box is rules/scoring/optimisation/simulation, none of which need training.

**Conclusion:** you can sit dead-centre of what SIH rewards while training almost nothing.

---

## 4. The 9 gates (binary — fail any = out)

- **G1** needs a model trained on data you'd collect
- **G2** needs hardware / edge / RAM-latency-power budget
- **G3** core depends on sponsor-only data
- **G4** domain needs an expert nobody has
- **G5** reads as portal / ERP / management system (breadth)
- **G6** can't demo offline on one laptop
- **G7** forces the dev to learn a new language/framework
- **G8** all-or-nothing (no graceful degradation)
- **G9** problem takes >1 minute to explain

## 5. The scorecard (weighted, /220 in the criteria version; /100 rubric in the dossier)

Bent hard toward narrowness. Key weights (criteria version): narrow surface area ×5, decision-layer ×5, full-chain-visible ×4, self-proving output ×4, real demo moment ×4, non-code work for members ×3, low domain barrier ×3, data obtainable/synthesisable ×3, low crowding ×2, sponsor seriousness ×2, dev knows stack ×2. Topic appeal is deliberately excluded (it's what makes a PS crowded).

Dossier rubric (/100): Impact 20 · Innovation 15 · Feasibility 15 · Low dataset dependency 10 · Low training requirement 10 · Demo potential 10 · Deployment potential 10 · Scalability 5 · Team-skill accessibility 5.

---

## 6. The funnel

**192 statements → 155 software → 34 survive the 9 gates → 8 deep-dived → 3 recommended → 1 winner.**
Of the 121 software statements cut: **52 on training burden alone**, 33 breadth, 12 domain-expert, 9 vague (Maharashtra one-liners), 6 sponsor-only data, 5 hardware-in-disguise, 4 new-stack/CAD.

---

## 7. The 8 shortlisted statements (final ranking)

| Rank | PS | Title | Class | Score | Verdict |
|---|---|---|---|---|---|
| 1 | **34** | Legal Metrology packaged-commodity compliance | B | 90 | **YES — winner** |
| 2 | **27** | Automatic block planning — Indian Railways | A | 87 | YES — highest ceiling |
| 3 | **35** | NAWI test-report generation (OIML R-76) | A | 82 | YES — safest to finish |
| 4 | **191** | Hazard red zones & relocation (GIS) | B | 82 | YES — best-looking demo |
| 5 | **100** | GeM bid compliance verification | B | 80 | YES — twin of the winner |
| 6 | **155** | Multi-vendor network compliance auditor | B | 75 | MAYBE — domain-heavy |
| 7 | **99** | Material-code harmonisation across CPSEs | C | 73 | MAYBE — needs real matching |
| 8 | **117** | Sovereign agentic AI workbench (MRPL) | D-eq | 61 | **NO — drop it** |

Class key: A = no ML · B = pretrained/API only · C = small classical model on obtainable data · D/E = training required (cut).

### Why the winner (PS 34)
- Rules engine built from the **Legal Metrology (Packaged Commodities) Rules, 2011** — proves itself clause by clause.
- **Zero data barrier** — you shoot the packet corpus yourself with a phone; that's valid method because the rules define the inputs.
- **Non-coders on the critical path** — 2 members encode the rulebook (the actual product); this is the only shortlisted PS where the 5 members are load-bearing, not adjacent.
- **Demo that defeats "is this rehearsed?"** — hand a judge your phone: "pick any product here or paste any product URL." Live scan → per-clause verdict + generated inspection notice. No other team's demo runs on an object the judge chose.
- Differentiator most teams miss: **Rule 9 font-height check** (glyph height vs package size) from bounding-box geometry; and an **e-commerce batch mode** (the impact/deployment argument).
- One real risk: **extraction on glossy/curved packaging** — test on 200 real packets in week 1; if it stalls, switch to PS 27.

### The runners-up
- **PS 27** — highest ceiling (CP-SAT, provably optimal, weight-slider + minimal-conflict-set demo) but **all risk sits in the one developer's head**; take it only if that person is strong at and enjoys optimisation. Note: it names 5 internal railway systems (TMS/SMMS/TDMS/COA/BDMS) you can't access → use a parameterised scenario generator.
- **PS 35** — the safety pick; near-pure calculation + document generation faithful to OIML R-76; lowest difficulty (4/10), a *complete* build is near-guaranteed.
- **PS 191** — best visual demo (live hazard map + carrying-capacity gate + re-ranking); free public GIS data; risk is a GIS learning curve + defensible carrying-capacity formula.
- **PS 100** — the winner's twin (document rules engine over GeM statutory checks); same non-coder leverage; manage gov-portal access with a documented adapter layer (some live, some realistic mocks).

### Why PS 117 is a NO
Doesn't strictly need training, so it passes the training gate — but fails on **surface area + infrastructure**: it's five projects in one title (open-weight LLM serving + multi-model routing + full agentic loop + multimodal OCR/vision + local KB), needs real GPU hardware, may not run offline at the venue, and "the agent did it" doesn't prove itself. A platoon's project, not a 1-dev team's.

---

## 8. Final recommendation

**Pick PS 34. Hold PS 35 as the fallback. Consider PS 27 only if the developer is an optimisation enthusiast.**

The team decision is: **ambition (27) vs balance (34) vs safety (35)** — decide which failure you fear more, an unfinished brilliant thing or a finished modest one. **The developer holds the veto** (they build it). If two teams from your institute enter, take **34 and 100** (both compliance, non-overlapping sponsors) — don't self-compete.

**Week 1, whatever you pick:**
1. **Prove the risky stage immediately** — 34: extraction on 200 real packets · 27: a tiny CP-SAT model solving correctly · 191: one district's layers into PostGIS · 99: measure matching precision. If it doesn't work early, switch while switching is cheap.
2. **Fix the bus factor** — push 2 of the 5 members into narrow code lanes now (one on React front-end, one on Python/data). Not to make them developers — only so the single point of failure isn't literally one person by December.

**Member roles (non-negotiable for a strong finish):** domain researcher (owns the rulebook/standard), test-data/synthetic-data builder, pitch & demo owner, judge-question prep & docs, UI mockups. At the finale a team that presents well with 70% beats a silent team with 90%.

---

## 9. Data notes & corrections (carry forward)

- **Universe = 192 statements (155 software).** The Word file's 34 extra entries (26193–26226) are AICTE "Student Innovation" placeholders — not real statements.
- **The Category (Software/Hardware) column is reliable** (0 mismatches vs the PDFs). **The Theme column is corrupt — ignore it** (e.g. a dementia platform tagged "Space Technology," a Bitcoin tool tagged "Transportation").
- **The circulating DecodeX pattern deck cites several wrong PS numbers.** Verify every number on the official portal before it reaches your own slides:
  - SIH26185 = helmet-mounted conformal antenna (Hardware), **not** urban flood prediction (that's 85).
  - Thunderstorm/lightning nowcasting = **72**, not 68 (68 = WeatherGPT).
  - GeM procurement analytics = **100**, not 95 (95 = a monitoring app).
  - PS 162 = industrial fire detection, **not** a defence LLM.
- **Crowding is live data** — every PS read 0/500 registrations because the list was captured early. Re-check registration counts on the portal ~1 week before the 20 Sept 2026 deadline; the low-crowding advantage on 34/27/35/155 is an assumption until then.
- Four statements are tagged Hardware but read as pure software (87, 88, 96, 109) — none survive the gates anyway, so it costs nothing here, but don't lean on the Type column blindly.

---

## 10. Where the analysis could be wrong

- The scorecard rewards narrowness and provability, so it **systematically undervalues ambition**. If SIH 2026 judging rewards visible AI sophistication over defensible correctness, PS 34 places mid-table and the ISRO/MoES statements we cut were the right bets. That's the trade you make with one developer — the correct trade, but a trade.
- PS 34's soft spot is the extraction stage: if it doesn't hit ~80% on judge-chosen packets, the demo that makes it a winner is also what sinks it. Test early; switch to PS 27 if it stalls.

# SIH PROJECT — SESSION HANDOFF

**Paste this file into a new Claude Code session to restore full context.**
Working folder: `C:\Users\manug\Downloads\SIH\`
Last updated: end of session 1.

---

## 1. WHO / WHAT

A student team (4–6 people) is preparing for **Smart India Hackathon**. I am helping them choose a problem statement and plan the build.

**Hard constraint, stated by the user and applied throughout:**
> "We want to build a technically impressive software solution, but we do NOT want a project that requires collecting a huge proprietary dataset or training a deep-learning model from scratch."

**Comfortable using:** LLM APIs, open-source pretrained models, RAG, vector DBs, OCR, NLP APIs, pretrained CV, optimisation / constraint programming / OR, GIS & map APIs, small classical ML, full-stack, cloud, microservices, rule engines, simulation, public government APIs.

**Additional filter added later:** software statements only — no hardware.

---

## 2. WHERE THINGS STAND (read this first)
The work happened in two phases, and **phase 2 invalidated phase 1's specific conclusions**:

| Phase | What | Status |
|---|---|---|
| 1 | Deep analysis of **SIH 2025** statements (139 total, 105 software) | **Historical.** Method still valid, verdicts obsolete |
| 2 | User supplied **SIH 2026** statements (192 total, 155 software) | **Current.** Segregated only — not yet screened |

**None of the eight SIH 2025 statements analysed appear in SIH 2026.** The 2025 winner (PS 65, KMRL train induction) does not exist in the 2026 list. Do not recommend it.

### ⏭ THE PENDING TASK

Run the phase-1 method across the **155 SIH 2026 software statements**:
1. Classify every one on the A–E training-intensity ladder (§4).
2. Cut Class D/E.
3. Score the survivors on the 100-point rubric (§5).
4. Produce a top 3 and a single winner, with the same brutal-honesty standard.

Source data is ready at `source/sih2026.tsv` (pipe-delimited: `num|organisation|title|category`, all 192 rows, validated).

---

## 3. FILES

| File | What it is |
|---|---|
| `SIH_Dossier.html` | The full deliverable, standalone HTML |
| `SIH_Full_Analysis.md` | Same content as Markdown (~49,500 words) |
| `source/part01.md` … `part10.md` | The document split into parts; edit these, not the outputs |
| `source/build.py` | Converts `part[0-9][0-9].md` → styled `sih_dossier.html`. Run it after editing any part |
| `source/classify.py` | The SIH 2025 training-intensity classifier (105 statements). **Template for the 2026 pass** |
| `source/sih2026.tsv` | All 192 SIH 2026 statements, validated |
| `source/SIH2025_Problem_Statements.xlsx` | Original 2025 sheet |

**Published artifact (private, same URL on republish):**
`https://claude.ai/code/artifact/143919d8-a699-4739-a7fc-69d675ba611e`

To update it: edit a part file → `python source/build.py` → publish `sih_dossier.html` **passing that URL as `url`**, or the update creates a separate artifact.
Favicon in use: 🚇📋 (keep it stable). Title: *SIH Shortlist Dossier*.

**Dependencies:** `pip install openpyxl markdown`

---

## 4. METHOD — the training-intensity ladder

Every software statement gets exactly one class:

| Class | Meaning | Verdict |
|---|---|---|
| **A** | No AI/ML required — rules, optimisation, engineering, integration | Target zone |
| **B** | Pretrained models, APIs or RAG are sufficient | Target zone |
| **C** | A small classical model on obtainable tabular data | Acceptable |
| **D** | Significant custom model training required | Cut |
| **E** | Training *plus* unobtainable data, or hardware / specialist science | Cut |

**Calibration rules learned in phase 1:**
- Class is about *training burden*, not quality. Plenty of Class A statements (ERP portals, gamified education apps) are trivially buildable and impossible to win with. Screen for **winnability**, not buildability.
- Where a statement can be read at different ambition levels, assume the sane reading (pretrained detection = B, training your own detector = D).
- 2025 result for comparison: of 105 software statements, **81 passed (37 A / 31 B / 13 C), 24 failed**. The constraint is far less restrictive than it feels.

---

## 5. METHOD — the 100-point rubric

| Criterion | Weight |
|---|---|
| Problem Impact | 20 |
| Innovation Potential | 15 |
| Technical Feasibility | 15 |
| Low Dataset Dependency | 10 |
| Low Model Training Requirement | 10 |
| SIH Demo Potential | 10 |
| Real-world Deployment Potential | 10 |
| Scalability | 5 |
| Team Skill Accessibility | 5 |

Per statement, the full analysis covers 22 sections: problem understanding · what it really requires (mandatory / implied / optional / misreadings) · proposed solution · AI-ML classification · dataset requirements + risk rating · architecture (text diagram) · tech stack with per-choice justification · MVP (must/should/nice) · advanced features · innovation analysis vs. what competitors will build · demo strategy with a named WOW moment · 12–15 predicted judge questions with strong/weak answers · failure modes · difficulty ratings 1–10 · team roles · time estimates · cost · security & privacy · prototype-vs-production · score calculation · brutal assessment ending in YES/MAYBE/NO.

---

## 6. TRANSFERABLE FINDINGS (these survive the 2025→2026 change)

**The single most important insight.** The no-training constraint is not a limitation — it is a *filter that points at optimisation problems*. Statements phrased as "AI-based scheduling / allocation / planning" are usually constraint-programming problems where **OR-Tools CP-SAT** gives provably optimal, fully explainable answers in seconds with no data and no hallucination. In the 2025 field this put optimisation statements in the top three slots. LLM/RAG statements are easier to start and much harder to finish convincingly, because *"the LLM said so"* collapses under judge questioning while *"the solver proved it"* does not.

**Patterns that scored well:**
- Statements that enumerate their own decision variables — synthetic data then becomes correct methodology, not a workaround.
- A verifiable claim (a solver's optimality proof, a model trained on real public outcome data, machine-checkable standards conformance) beats an unverifiable accuracy number.
- Infeasibility handling — returning the *minimal conflicting constraint set* — impresses judges more than producing an answer.
- Interactive trade-offs (drag a weight slider, watch KPIs move) are the most effective demo device found.

**Patterns that scored badly:**
- The core feature depending on a confidential corpus (this alone killed one statement).
- Commodity pipelines (upload PDF → chunk → embed → chat) where differentiation has to be manufactured.
- Crowded statements — anything where the naive version is easy attracts dozens of teams.
- API-only projects with no demoable client (technically excellent, hackathon-fatal).

**Recurring judge questions to prepare for, whatever the statement:**
"Where is the AI?" · "Where did your data come from?" · "How accurate is it, and how do you know?" · "What happens when it's wrong?" · "Would the sponsor actually deploy this?" · "What does it cost at scale?" · "Prompt injection?" · "What's the weakest part?" (never answer "nothing").

---

## 7. SIH 2026 — WHAT'S KNOWN SO FAR

192 statements · **155 software, 37 hardware** · IDs `SIH26001`–`SIH26192` · 500-team cap each · deadline 20 September 2026.

**Software concentration by organisation:** Ministry of Earth Sciences 27 (almost all weather/ocean forecasting) · NTRO 22 (almost all cyber/forensics) · ISRO 10 · MHA 10 · Rural Development 9 · Maharashtra 9 · Consumer Affairs 8 · Social Justice 7 · BEL 5 · Egreen Quanta 5 · rest ≤4. **MoES + NTRO alone are 32% of the software field.**

**Data-quality warnings — carry these forward:**
- The **Theme column in the source is misaligned and must not be used** (a dementia platform is tagged *Space Technology*, a land-record system *MedTech*, onion grading *Fitness & Sports*). It has been dropped from `sih2026.tsv`.
- Four statements are tagged **Hardware but read as pure software** — verify on the SIH portal before excluding: **87** (Cooperative ERP), **88** (Governance chatbot), **96** (Digital heritage archive), **109** (Bovine mastitis predictive modelling).
- Reverse error: **114** and **116** (Autodesk Forma / Revit) are tagged Software but are CAD modelling exercises. Out of scope regardless of label.

**Early observations, not yet a screen** — statements that look like the low-training / high-ceiling profile the method rewards, worth checking first: **27** (Railways automatic block planning — optimisation), **6** (freight forecasting + vessel chartering — OR), **119** (indigenous optimisation solver — MRPL), **62** (polar expedition logistics — OR), **16/17** (land acquisition monitoring and delay prediction), **34/35/36** (legal metrology compliance and test-report generation — rules engines), **99/100** (material-code harmonisation, GeM bid compliance), **149/150/164** (NTRO forensic and cryptographic tooling — engineering, no training). The MoES weather block (70–86) is mostly Class C/D — heavy geoscience ML — and should be treated with suspicion despite its size.

---

## 8. WORKING PREFERENCES

- **Default to compact.** The user initially asked for maximum depth, then said: *"talk about same topics but not in that depth."* Cover the same topics, less length.
- **Do not flatter the shortlist.** The user explicitly asked not to be agreed with blindly. Disagreeing with their ranking, and cutting statements from it, is expected and was well received.
- Deliverables go to the artifact (same URL) plus a Markdown copy in this folder.
- Tables and ranked verdicts land better than prose walls.
- Everything must be cost-realistic: the team is building on free tiers, so prefer local embeddings, self-hosted stacks, and free map tiles over billed APIs.

---

## 9. SUGGESTED OPENING MESSAGE FOR THE NEW SESSION

> Read `C:\Users\manug\Downloads\SIH\HANDOFF.md`. Then run the pending task in §2: classify all 155 SIH 2026 software statements in `source/sih2026.tsv` on the A–E ladder, cut D and E, score the survivors on the rubric in §5, and give me a top 3 and one winner. Keep it compact.

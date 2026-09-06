---
---

# PART 3 — CROSS-STATEMENT COMPARISON

## Master comparison table

| PS | Problem | Impact /20 | Innovation /15 | AI Difficulty | Data Risk | Dev Risk | Demo /10 | **Score /100** | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| **65** | Train Induction Planning — KMRL | 16 | 14 | Medium-High (CP-SAT modelling) | **LOW** | MED–HIGH | 9 | **87** | **YES — winner** |
| **70** | NEP Timetable Generation — J&K | 16 | 10 | Medium (CP-SAT, well-trodden) | **LOW** | MEDIUM | 9 | **87** | **YES — safest** |
| **33** | PM Internship Allocation — MCA | 17 | 9 | Medium (matching + flow) | LOW | MEDIUM | 8 | **85** | YES — with discipline |
| **64** | Document Overload — KMRL | 15 | 9 | Low (all off-the-shelf) | LOW–MED | MEDIUM | 8 | **82** | YES — if UI/full-stack is your strength |
| **125** | DPR Quality & Risk — MDoNER | 17 | 12 | Medium (LLM + small tabular ML) | **MEDIUM** | MED–HIGH | 8 | **79** | MAYBE — needs a data owner |
| **54** | RTRWH Assessment — Jal Shakti | 17 | 9 | Low (pretrained CV only) | MEDIUM | MEDIUM | 9 | **79** | MAYBE — great app, thin core |
| **26** | NAMASTE ↔ ICD-11 TM2 — Ayush | 15 | 10 | **Very Low** (barely any AI) | **LOW** | MED (HIGH demo risk) | 5 | **77** | MAYBE — best engineering, worst stage |
| **121** | R&D Proposal Evaluation — Coal | 11 | 8 | Low | **HIGH** | MED (HIGH outcome risk) | 6 | **66** | **NO — drop** |

## Score components side by side

| Criterion (weight) | PS 65 | PS 70 | PS 33 | PS 64 | PS 125 | PS 54 | PS 26 | PS 121 |
|---|---|---|---|---|---|---|---|---|
| Impact (20) | 16 | 16 | **17** | 15 | **17** | **17** | 15 | 11 |
| Innovation (15) | **14** | 10 | 9 | 9 | 12 | 9 | 10 | 8 |
| Feasibility (15) | 12 | **15** | 14 | 14 | 11 | 13 | 12 | 13 |
| Low data dependency (10) | 9 | **10** | 9 | 9 | 7 | 6 | 9 | 5 |
| Low training (10) | **10** | **10** | **10** | **10** | 8 | 9 | **10** | 9 |
| Demo (10) | 9 | 9 | 8 | 8 | 8 | 9 | 5 | 6 |
| Scalability (5) | **5** | 4 | **5** | 4 | 4 | 4 | 4 | 4 |
| Deployment (10) | 9 | 8 | 8 | 8 | **9** | 8 | **9** | 6 |
| Team accessibility (5) | 3 | **5** | **5** | **5** | 3 | 4 | 3 | 4 |
| **TOTAL** | **87** | **87** | **85** | **82** | **79** | **79** | **77** | **66** |

## Patterns worth noticing

1. **The optimisation statements swept the top.** PS 65, 70 and 33 take the top three because constraint programming and matching theory give provable answers with zero data — a perfect fit for your stated constraint, and a category most SIH teams handle badly.
2. **Impact and score are only loosely coupled.** PS 54 and PS 125 tie PS 33 on impact (17) and still finish two tiers lower, because impact is only 20% of the picture and both carry real data cost.
3. **Demo potential is where PS 26 dies.** It is otherwise a top-four project. A 5/10 on a 10-point criterion is a 4-point swing that pushes it below two projects it is technically superior to. That is a fair reflection of hackathon reality, not an injustice.
4. **Your two lowest-innovation top picks (PS 64 and PS 33) are also the two most-picked statements at SIH.** That combination — easy to build, crowded field — is the classic way a good team finishes mid-table.
5. **Every statement here passes your no-training constraint** except in the mild sense that PS 125 wants a small tabular model — which is a feature, not a violation, because it is the only project with a genuinely verifiable predictive claim.

---

# PART 4 — FINAL RECOMMENDATION

## TOP 3

### 🥇 1. PS 65 — AI-Driven Train Induction Planning & Scheduling (KMRL)

**Why choose it.** It is the rare statement where the hardest part is *interesting* rather than tedious. Six named decision variables, a physical yard to model, conflicting objectives to reconcile, and a nightly decision that currently runs on one person's memory. It needs no real data because the statement defines its own variable space, so synthetic generation is methodologically correct rather than a workaround. And unlike the crowded statements, comparatively few teams will attempt it, and fewer still will model stabling geometry.

**Biggest advantage:** the demo. A depot map, a live re-solve, and an override that instantly prices its own consequences is the most tangible thing you can put in front of a judge — abstract optimisation made physical.

**Biggest risk:** the CP-SAT model itself. If nobody on your team is willing to spend day one and day two inside a solver, this becomes a sorted table with a nice map, and the whole advantage evaporates.

**Recommended architecture:** React + TypeScript with a Canvas yard map → FastAPI → separate optimisation service running OR-Tools CP-SAT via Celery → PostgreSQL with versioned plans and an append-only audit log → Redis for caching and job brokering → LLM API used *only* to render structured reason objects as prose. No vector DB. No Kafka. No Kubernetes.

**Recommended MVP:** synthetic generator for 25 trainsets → rule engine with machine-readable reasons → CP-SAT assignment across service/standby/IBL under FC, job-card, cleaning and branding constraints with mileage balancing → ranked list with per-trainset explanations → **depot yard map with shunt-move counting in the objective** → what-if override with KPI delta → emergency re-plan.

**Best demo strategy:** open on the night-shift spreadsheet, generate the plan in under ten seconds with the constraint count on screen, then spend your best ninety seconds on the override that quantifies its own cost. Close by switching to a 40-trainset two-depot scenario and re-solving live. Have the "where is the AI?" answer memorised — you will be asked it, and answering it confidently is itself a differentiator.

---

### 🥈 2. PS 70 — NEP-2020 Timetable Generation (J&K)

**Why choose it.** It is the lowest-variance strong option on your list. No data risk at all, a mature problem class with excellent tooling, a demo that any judge understands in five seconds, and a real institutional pain that every Indian college currently feels. A competent team executing this reliably lands in the top tier.

**Biggest advantage:** certainty. Almost nothing can go catastrophically wrong. You will have a working timetable on day one and spend the rest of your time making it excellent rather than making it work.

**Biggest risk:** the crowd, and the resulting section-level trap. Timetabling is among the most-attempted SIH problem types, so a competent-but-ordinary version disappears. And if you schedule *sections* rather than individual student baskets, you have missed the NEP point entirely — which one sharp question will expose.

**Recommended architecture:** Next.js frontend with a custom CSS-grid component pivoting the same data across master/faculty/room/student views → FastAPI → CP-SAT via Celery → PostgreSQL → optional local embeddings for faculty–course matching and an LLM for natural-language constraint entry with mandatory user confirmation.

**Recommended MVP:** full entity setup → 2,000 synthetic student baskets from a realistic preference model → section auto-splitting → CP-SAT generation → master grid **plus per-student view** → NEP credit-compliance report → three scenarios with a KPI comparison → drag-to-edit with instant validation → minimum-disruption re-planning.

**Best demo strategy:** state the instance size early (2,000 students, 214 courses), solve in seconds, then **invite a judge to name any student ID** and show that student's clean, credit-validated week. Follow with a live run of your independent verifier, and close on the quality metrics — student idle hours down, faculty load equity up, room utilisation up — because "feasible" is the floor and everyone else stops there.

---

### 🥉 3. PS 33 — Smart Allocation Engine, PM Internship Scheme (MCA)

**Why choose it.** The highest real-world impact on your list, and genuinely respectable algorithms underneath — capacitated stable matching plus quota-constrained optimisation is real computer science, not a similarity score. The fairness dimension gives you something to say that is both technically precise and socially meaningful, which is a strong combination in front of a government panel.

**Biggest advantage:** the algorithm-comparison moment. Showing naive greedy versus stable matching versus quota-constrained optimisation, with the trade-offs quantified, instantly separates you from every team that built a recommender.

**Biggest risk:** the field. This is likely the most-attempted statement on your shortlist, and the naive version is easy enough that dozens of teams will have something demoable. If your team drifts toward "top-5 matches per candidate," you become indistinguishable from them.

**Recommended architecture:** Next.js three-portal frontend with a Leaflet/MapLibre national heatmap → FastAPI → local sentence-transformers for skill embeddings → **pgvector ANN retrieval for sparse top-K candidate–opportunity pairs** (this is the scale insight) → capacitated Gale–Shapley plus OR-Tools min-cost flow → PostgreSQL with versioned, reproducible allocation runs → LLM for resume parsing and explanation prose only.

**Recommended MVP:** 50,000+ synthetic candidates with realistic geographic and preference skew → real NCO taxonomy, real aspirational-districts list, real geography → embeddings and sparse retrieval → stable matching with hard fairness quotas → fairness audit report → per-candidate explanations with counterfactuals → national heatmap → algorithm comparison panel.

**Best demo strategy:** open with two identically skilled candidates, one invisible to today's process. Establish scale, then allocate 84,000 candidates in under a minute. Spend your peak on the three-algorithm comparison with quantified trade-offs, then show a rejected candidate receiving actionable guidance, and close with the quota slider that prices a policy change before it is announced.

---

## 🏆 THE ONE OVERALL WINNER: PS 65 — AI-Driven Train Induction Planning (KMRL)

**Why it beats the other seven.**

**Against PS 70 (tied on score, 87):** the tiebreak is competition and ceiling. Timetabling is one of the most-attempted SIH problem types; depot induction planning is not. Both are data-free optimisation projects, but PS 65 has a higher innovation score (14 vs 10) because modelling a physical yard with LIFO stabling and shunt costs is materially harder and rarer than scheduling classes into slots. When two projects score equally, choose the one where fewer teams can reach your level.

**Against PS 33:** PS 33 has higher impact but lower innovation and a far more crowded field. Its algorithms are excellent, but the naive version is easy enough that you would spend the pitch differentiating yourself from lookalikes rather than explaining your work.

**Against PS 64:** PS 64 is the easiest to build and the hardest to win with. Its base pipeline is commodity; you would have to manufacture every differentiator. PS 65's differentiation is structural — it lives in the problem itself.

**Against PS 125:** PS 125 has the higher innovation ceiling but pays for it with MEDIUM data risk, PDF table extraction grind, and complete dependence on one person doing disciplined data work from hour one. PS 65 achieves comparable depth with LOW data risk.

**Against PS 54:** better demo aesthetics, worse technical core. PS 54's engine is arithmetic; PS 65's is a constraint solver.

**Against PS 26:** PS 26 is arguably the more professional artefact and the more deployable one, but a 5/10 demo score at a hackathon is close to disqualifying. PS 65 gives you comparable engineering credibility *with* a demo that performs.

**Against PS 121:** not competitive on any axis.

**The decisive argument.** Your stated constraint — no proprietary data, no deep-learning training — is not a limitation you are working around. It is a filter, and it points directly at problems where mathematics beats data. PS 65 is the purest expression of that on your list: a hard, real, well-specified decision problem with six named variables, zero data dependency, a physical system to model, provable answers, natural explainability, and a visual demo. You will not be competing against fifty other teams; you will be competing against a handful, most of whom will build a ranked table and call it AI.

**Conditions on this recommendation — read them before committing.**

1. **Someone must own the solver from hour one.** Ideally two people pairing on it. If CP-SAT is not producing a valid assignment by the end of day two, switch to PS 70 while the switch is still cheap.
2. **Build the yard model, not a bay label.** Shunt-move counting inside the objective is the difference between winning and placing.
3. **Prepare the "where is the AI?" answer** and deliver it before the question is asked.
4. **Do not scope-creep into crew rostering, IoT telemetry or energy optimisation.** Put them on a roadmap slide and move on.

**If any of those four conditions fails, switch to PS 70.** It scores identically, is materially easier, and its only real weakness — a crowded field — is one you can overcome with the per-student verification demo. That is your fallback, and it is a genuinely good one.

---

## One-page decision aid

| If your team's strength is… | Choose | Because |
|---|---|---|
| Algorithms / OR / mathematical modelling | **PS 65** | Highest ceiling, lowest competition, best demo |
| Balanced, wants low risk | **PS 70** | Same score, easier build, universally legible |
| Social impact + solid CS | **PS 33** | Highest impact, real algorithms, crowded field |
| Full-stack execution + UI polish | **PS 64** | Highest floor; you must manufacture differentiation |
| Data wrangling + ML rigour | **PS 125** | Highest innovation ceiling; needs a dedicated data owner |
| Mobile + GIS + human-centred design | **PS 54** | Beautiful, cheap, humane; thinnest technical core |
| Specifications, standards, backend rigour | **PS 26** | Most deployable, most professional; demo risk is real |
| — | ~~PS 121~~ | Drop it. Choose PS 125 instead for the same skills at ten times the impact |

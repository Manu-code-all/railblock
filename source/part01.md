# SIH 2025 — Deep Evaluation of 8 Shortlisted Problem Statements

**Prepared for:** a 4–6 person software team
**Source sheet:** `Problem Statements.xlsx` (139 statements: 105 Software, 34 Hardware)
**Hard constraint honoured throughout:** *no proprietary dataset collection, no deep-learning training from scratch.*

---

## PART 0 — EXECUTIVE SUMMARY (read this page even if you read nothing else)

### 0.1 Overall ranking (weighted score /100, calculation shown in each section 20)

| Rank | PS | Title (short) | Score | Verdict |
|---|---|---|---|---|
| 1 | **PS 65** | AI-Driven Train Induction Planning — KMRL | **87** | YES — winner |
| 2 | **PS 70** | NEP-2020 Timetable Generation — J&K | **87** | YES — safest strong pick |
| 3 | **PS 33** | Smart Allocation Engine — PM Internship | **85** | YES — highest impact, most crowded |
| 4 | **PS 64** | Document Overload — KMRL | **82** | YES — easiest to build, hardest to differentiate |
| 5 | **PS 125** | DPR Quality & Risk Prediction — MDoNER | **79** | MAYBE — highest ceiling, real data work |
| 6 | **PS 54** | On-spot RTRWH & Recharge Assessment | **79** | MAYBE — beautiful demo, thin tech core |
| 7 | **PS 26** | NAMASTE ↔ ICD-11 TM2 EMR integration | **77** | MAYBE — best engineering, worst demo |
| 8 | **PS 121** | Auto-Evaluation of R&D Proposals — Coal | **66** | NO — drop it |

### 0.2 Where I disagree with your tiering

You put **PS 65 in Tier A. That is your biggest mistake.** PS 65 is the single best statement on your list: it needs zero real data (all six decision variables are enumerated in the statement itself, so synthetic data is *defensible*, not a cop-out), it has genuine algorithmic depth that 90% of teams cannot replicate, it produces a gorgeous depot-visualisation demo, and KMRL is an active sponsor that actually wants the artefact. **Promote it to Tier S.**

You put **PS 121 in Tier A. Drop it entirely.** It is PS 125's weaker twin — same document-scoring shape, one-third the impact, and a corpus (past NaCCER/CMPDI R&D proposals) that is confidential and genuinely unobtainable. It fails your own constraint harder than anything else on the list.

**PS 26 is under-rated by everyone including you** — it is the most professionally impressive thing on the list and the one real government deployment candidate. It is also demo-hostile. Choose it only if you accept that risk consciously.

**Competition warning from the sheet itself:** 7 of your 8 picks sit in *Smart Automation* — the largest theme (32 of 139 statements). PS 33, PS 64 and PS 70 are the three statements most SIH teams historically converge on. PS 65, PS 125 and PS 26 are where the thin crowds are.

### 0.3 Category winners

| Question | Answer | One-line reason |
|---|---|---|
| **Best project overall** | **PS 65 (Train Induction)** | Deep algorithms + zero data risk + unbeatable demo + low competition |
| **Fastest to implement** | **PS 64 (KMRL Documents)** | A competent team has a working RAG pipeline in 24 hours |
| **Maximum innovation** | **PS 125 (DPR Risk)** | Nobody else will do real cost-overrun modelling on MoSPI data |
| **Minimum AI/ML dependency** | **PS 26 (NAMASTE/ICD-11)**, then **PS 70** | PS 26 is pure standards engineering; PS 70 is pure constraint programming |
| **Highest-risk project** | **PS 121 (Coal R&D)** — data does not exist. Runner-up: **PS 26**, for demo risk |
| **I would personally choose** | **PS 65**, with **PS 70** as the fallback if nobody on the team enjoys optimisation |

### 0.4 The one strategic insight

Your constraint ("no training, no proprietary data") is not a limitation — it is a *filter that points at optimisation problems*. Every statement that says "AI-based scheduling / allocation / planning" is secretly a constraint-programming problem where OR-Tools CP-SAT gives you provably optimal, fully explainable answers in seconds, with no data and no hallucination. That is why **PS 65, PS 70 and PS 33 occupy the top three slots.** LLM/RAG statements (64, 125, 121) are easier to start and much harder to finish convincingly, because "the LLM said so" collapses under judge questioning while "the solver proved it" does not.

---

## HOW TO READ THE REST

Each of the 8 statements gets the full 22-section treatment. Statements are presented in my ranked order, not yours — best first, so that if you stop reading you have already read the important ones.

Scoring weights used throughout: Impact 20 · Innovation 15 · Feasibility 15 · Low Dataset Dependency 10 · Low Training Requirement 10 · Demo Potential 10 · Deployment Potential 10 · Scalability 5 · Team Skill Accessibility 5.


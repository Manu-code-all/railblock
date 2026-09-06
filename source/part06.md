---
---

# ⑤ PS 125 — AI-Powered DPR Quality Assessment & Risk Prediction System for MDoNER
**Organisation:** Ministry of Development of North Eastern Region · **Category:** Software · **Theme:** Smart Automation
**Score: 79/100 · Recommendation: MAYBE — highest innovation ceiling, real data work required**

## 1. Problem Understanding

A **Detailed Project Report (DPR)** is the document on which an infrastructure project is sanctioned. For a road, bridge, water-supply scheme or tourism facility in the North East, a DPR typically runs 150–500 pages and must contain: project justification and need assessment, technical feasibility and design, detailed cost estimates built from Schedule-of-Rates items, land-acquisition status, statutory clearances (environmental, forest, wildlife — acutely relevant in the North East), a financial analysis (IRR, NPV, cost–benefit), an implementation schedule, an O&M plan, and risk/mitigation sections.

MDoNER receives DPRs from eight state governments and implementing agencies. Appraisal today is manual: an officer or an empanelled consultant reads the document and forms a judgement. Three failures follow:

1. **Slow.** Weeks per DPR, and the North East pipeline is large.
2. **Inconsistent.** Two appraisers apply different standards; the same weakness passes in one DPR and fails another.
3. **Backward-looking only.** Appraisal checks whether the document is *complete*, not whether the project is *likely to overrun*. And overrun is the actual problem — Indian infrastructure projects routinely finish late and over budget, and the warning signs are usually visible in the DPR: optimistic schedules, unresolved land acquisition, missing clearances, cost estimates far from comparable-project benchmarks.

**Users:** MDoNER appraisal officers, state implementing agencies (who could self-check before submitting), and consultants. **Beneficiaries:** the region — faster sanctions, fewer stalled projects, better use of a large annual budget.

**Success:** upload a DPR, get within minutes a completeness scorecard against a defined checklist, a quality assessment with specific page-cited gaps, a benchmarked cost sanity check, and a data-driven risk score for cost and time overrun with the drivers named — all as a reviewable draft appraisal note that a human officer edits and signs.

## 2. What the Statement REALLY Requires

**Mandatory**
- Assess DPR quality and completeness automatically.
- Predict risk (cost overrun, delay, and implementation risk).
- Produce something an appraisal officer can act on.

**Implied**
- **A defined, defensible appraisal rubric.** You cannot score quality without stating the standard. Ground it in real guidance — DPR preparation guidelines, appraisal checklists used for centrally sponsored schemes, and standard SoR-based costing practice — and make the rubric visible and editable. Teams that invent an arbitrary 100-point scale will be asked "who decided these weights?" and have no answer.
- **Risk prediction needs historical outcomes.** This is the crux of the statement and the place teams will cheat by asking an LLM to "predict risk," producing a confident number with no basis. Do not do this.
- **Extraction from complex PDFs** — cost tables, Gantt schedules, clearance annexures. Tables, not prose, carry the decisive information.
- **Benchmarking against comparable projects** — a ₹/km figure means nothing alone and everything in context.
- **Explainability is mandatory in an appraisal context** — a score without page-cited evidence is unusable, because the officer must justify a rejection to a state government.
- **Human-in-the-loop by design.** The system drafts; the officer decides.

**Optional:** multi-language, portal integration, post-sanction monitoring, geospatial verification of project sites.

**Misunderstanding to avoid:** believing "AI risk prediction" means an LLM opinion. It means a model trained on real project outcomes — and the good news is that such data exists publicly.

## 3. Proposed Solution

**Product concept:** *"DPR Sentinel"* — an appraisal co-pilot that turns a 300-page DPR into a structured, evidence-cited scorecard plus a benchmarked, data-driven overrun risk assessment.

**Core modules**
1. **Document Understanding** — PDF parsing with layout awareness, OCR fallback, table extraction, section identification against a canonical DPR structure.
2. **Structured Extraction** — project type, sector, location, total cost, cost breakdown by head, timeline and milestones, land-acquisition status, clearance status per statute, funding pattern, IRR/NPV, contractor/agency details. LLM structured output with schema validation, each field carrying a page citation.
3. **Completeness Engine** — checklist evaluation against the rubric: present / partial / absent, with the evidence location or the specific absence.
4. **Quality Engine** — beyond presence: is the cost estimate itemised or a lump sum? Is the schedule broken into dependent milestones or a single bar? Are risks specific or boilerplate? Are clearances *obtained* or merely "applied for"? These distinctions separate a real appraisal from a checkbox.
5. **Benchmarking Engine** — compare unit costs (₹/km, ₹/sqm, ₹ per household served) and durations against comparable historical projects; flag deviations with percentile context.
6. **Risk Prediction Model** — a gradient-boosted model trained on **public historical project data** (see §5) predicting probability of cost overrun and time overrun, with SHAP attributions naming the drivers.
7. **Appraisal Note Generator** — a draft note with scores, evidence citations, benchmark comparisons, risk assessment and specific queries to raise with the submitting agency.
8. **Officer Workspace** — side-by-side DPR viewer and scorecard, accept/override every finding with a reason, export the final note.
9. **Portfolio Dashboard** — all DPRs under appraisal, risk distribution, common deficiency patterns by state and sector (which is itself a policy insight: "62% of submitted DPRs lack forest clearance evidence").

**Journey:** state agency uploads DPR → parsed and extracted in minutes → scorecard with cited gaps → benchmark comparison → risk score with drivers → officer reviews side by side, overrides two findings → note exported → agency receives specific, evidence-based queries instead of a vague rejection.

## 4. AI/ML Requirement

**Classification: B/C — pretrained models and APIs for the document work; a *small* classical ML model for risk, trained on public tabular data. No deep learning, no training from scratch.**

| Component | Technique | Why |
|---|---|---|
| PDF parsing & layout | **PyMuPDF, pdfplumber, Unstructured.io**; **Camelot/Tabula** for tables | Tables carry the cost data — this is the hardest extraction problem here |
| OCR fallback | **Tesseract/PaddleOCR** | Some DPRs are scanned |
| Section identification | **Embeddings + heading heuristics** | DPR structures vary by state; rigid regex fails |
| Field extraction | **LLM structured output with JSON schema + page citations** | No labelled corpus exists; zero-shot extraction is the right tool |
| Completeness/quality scoring | **Rule engine over extracted fields + LLM assessment for qualitative criteria, each with cited evidence** | Rules where objective, LLM only where judgement is genuinely needed — and always cited |
| Benchmarking | **Statistics over a historical project table** (percentiles by sector and terrain) | Simple and unarguable |
| **Risk prediction** | **Gradient boosting (LightGBM/XGBoost) on public historical project data + SHAP** | This is the statement's real ML content: small, tabular, interpretable, trainable in seconds |
| Draft note generation | **LLM over structured findings** | Presentation of computed results only |

**Critical architectural discipline:** the LLM extracts and phrases; **rules and the ML model decide**. If a judge can find any path where an LLM's free-form opinion becomes a score, you lose the section-4 argument.

## 5. Dataset Requirements — read this carefully, it decides the project

| Dataset | Why | Public? | Obtainable? | Synthetic? | Mock OK? |
|---|---|---|---|---|---|
| Sample DPRs | Input documents | **Partly — yes.** Many state PWDs, urban local bodies, DPR consultants and tender portals publish DPRs as PDFs; NE state and NEC project documents appear on government sites | Yes, with effort | Partly | Real ones are much better |
| **Historical project cost/time outcomes** | **Risk model training** | **YES — this is the key** | **Yes** | No need | Use real |
| DPR appraisal guidelines/checklists | The rubric | **Yes** — scheme guidelines and standard appraisal formats are published | Yes | — | Use real |
| Schedule of Rates | Cost sanity checks | **Yes** — state PWD SoRs are published | Yes | — | Use real |
| Benchmark unit costs by sector | Comparison | Partly — derivable from the historical outcome data | Yes | — | Derive |

**The unlock:** the Ministry of Statistics & Programme Implementation publishes regular **project implementation status reports on centrally monitored infrastructure projects**, listing for each project its sector, original cost, revised/anticipated cost, original commissioning schedule, anticipated commissioning date, and reasons cited for delay. That is a real, sizeable, public tabular dataset containing exactly the label you need: *did this project overrun, and by how much?* Supplement it with sector-wise project listings from state portals, PMGSY road data, and the India Investment Grid.

Build your risk model on that. Features: sector, project size band, state/terrain, funding pattern, original duration, agency type, and DPR-derived flags (land acquisition unresolved, clearances pending, lump-sum costing, unit cost deviation from benchmark). Then say on stage: *"Our risk model is trained on N real government-recorded infrastructure projects with known cost and time outcomes — not on our opinion."* That single sentence is the difference between this project and every other document-scoring project at SIH.

**Honest caveat you should state yourself:** MoSPI data covers large central-sector projects, which are not a perfect proxy for MDoNER's smaller North-Eastern projects. Handle it by reporting risk as a calibrated probability band with the reference population named, and by treating the model as a prior that DPR-derived flags adjust. Stating this limitation before a judge finds it is worth more than hiding it.

**Biggest data risk:** obtaining enough genuine DPR PDFs to prove extraction works across varied formats. Mitigation: gather 10–15 real ones early (day 1 task for the domain person), and synthesise variants for volume.

**Dataset Risk: MEDIUM** — but uniquely, it is *reducible by effort*, and the effort is a differentiator rather than a liability.

## 6. Technical Architecture

```
State Agency (submitter) / MDoNER Appraisal Officer / Senior Reviewer
        |
        v
Next.js frontend
  |-- Upload + processing status
  |-- Side-by-side DPR viewer & scorecard (citation jump-to-page)
  |-- Benchmark comparison charts
  |-- Risk panel with SHAP driver bars
  +-- Portfolio dashboard
        |
        v
FastAPI Gateway
        |
   +----+-------------+------------------+-------------------+
   v                  v                  v                   v
Parsing Svc      Extraction Svc     Scoring Svc         Risk Svc
(PDF, OCR,       (LLM structured    (rule engine +      (LightGBM model,
 tables, layout,  output + schema    quality criteria    SHAP, benchmark
 sections)        + page citations)  + evidence links)   percentiles)
   |                  |                  |                   |
   v                  v                  v                   v
Object store    PostgreSQL (+pgvector)     Redis/Celery      Model registry
(original PDFs)  extracted fields,          async pipeline    (versioned model
                 scores, citations,                           + training data
                 historical project table                     snapshot)
        |
        v
   Report generator (PDF appraisal note)  -  Audit log  -  Monitoring
```

**Note the model registry.** Versioning the risk model *and the data snapshot it was trained on* is what makes a prediction defensible months later. It costs an afternoon and it is a strong answer to "how do we audit a score from last year?"

## 7. Recommended Tech Stack

| Layer | Choice | Why here |
|---|---|---|
| Frontend | **Next.js + TypeScript + Tailwind** | Document-heavy review UI |
| Viewer | **PDF.js with citation highlighting and jump-to-page** | Every finding must be one click from its evidence |
| Charts | **Recharts / Plotly** | Benchmark distributions and SHAP bars |
| Backend | **Python + FastAPI** | Document + ML ecosystem |
| Table extraction | **Camelot + pdfplumber**, with **Unstructured.io** as a general fallback | Cost tables are the crux; use tools built for tables |
| LLM | **Claude API** — long context and reliable structured output with citations | Extraction and note drafting |
| ML | **LightGBM + SHAP + scikit-learn** | Small tabular data, interpretable, trains in seconds |
| Database | **PostgreSQL** (+pgvector for section matching) | Structured findings + similarity search over comparable projects |
| Async | **Celery + Redis** | A 300-page DPR takes minutes |
| Reports | **WeasyPrint / ReportLab** | Officers need a signable PDF note |
| Deploy | **Docker Compose** | ₹0 |

## 8. MVP for SIH

**MUST HAVE**
1. DPR upload + parsing + table extraction + section identification.
2. Structured field extraction with page citations.
3. Completeness scorecard against a documented, real-guideline-based rubric.
4. Quality assessment for at least 6–8 substantive criteria with cited evidence.
5. **Risk model trained on real public historical project data**, with probability output.
6. SHAP-based driver explanation for each risk score.
7. Side-by-side viewer: finding → highlighted evidence in the PDF.

**SHOULD HAVE**
8. Benchmarking against comparable projects with percentile context.
9. Draft appraisal note export (PDF).
10. Officer override with reason, captured in the audit trail.
11. Portfolio dashboard with deficiency patterns by state/sector.

**NICE TO HAVE**
12. Comparable-project retrieval by embedding similarity. 13. Geospatial verification of the project site. 14. Multi-DPR comparison. 15. Submitter self-check portal.

**Finish before presenting:** MUST + 8 and 9. Item 5 is the whole reason to pick this statement — if the risk model is not trained on real data, choose a different problem statement.

## 9. Advanced Features

- **Real-data risk model with named drivers** — "68% probability of >20% cost overrun; drivers: land acquisition unresolved (+22pp), unit cost 41% above the sector median for hill terrain (+15pp), single-milestone schedule (+9pp)."
- **Benchmark percentile positioning** — show this DPR's ₹/km against the distribution of comparable NE road projects.
- **Evidence-cited findings throughout**, with jump-to-page.
- **Deficiency pattern analytics across the portfolio** — an actual policy output: which states systematically omit which sections.
- **Self-check portal for submitting agencies** — turns a gatekeeper into a quality-improvement tool, which is a far better adoption story.
- **Model and data versioning** for auditability.
- **Calibration display** — show that predicted probabilities match observed frequencies on held-out data. Almost no SIH team will show a calibration curve, and it is the single most credible slide you can put in front of a technical judge.
- **Officer feedback loop** — overrides feed rubric refinement.

## 10. Innovation Analysis

1. **A risk model trained on real, public, government-recorded project outcomes** — this is genuine, verifiable ML, and virtually no competing team will do it.
2. **Rules and models decide; LLMs only extract and phrase** — a clean, defensible division most teams cannot articulate.
3. **Evidence-cited scoring** — every finding one click from its page.
4. **Benchmarking with percentile context** rather than isolated numbers.
5. **Calibration reporting** — honest probability communication.
6. **Portfolio-level deficiency analytics** — value to the ministry beyond individual appraisals.

**What competitors will build:** upload a PDF, ask an LLM "is this DPR good and how risky is it?", print an invented score out of 100 and a risk percentage with no basis. The first judge question — "where does 73% come from?" — ends that project.

## 11. SIH Demo Strategy (8 minutes)

| # | Stage | Time | Screen | Say |
|---|---|---|---|---|
| 1 | Problem | 0:45 | A 340-page real DPR scrolling fast; "weeks of manual appraisal" | "Every sanctioned project starts here. So does every overrun." |
| 2 | Upload | 0:30 | Drop a real DPR; pipeline stages tick through: 340 pages, 47 tables, 12 sections identified | — |
| 3 | Completeness | 0:50 | Scorecard: 11/15 sections complete; "Forest clearance: applied for, not obtained — page 212" — click, PDF jumps and highlights | "Every finding points at a page. An officer can defend this to a state government." |
| 4 | Quality | 0:50 | Substantive findings: lump-sum costing on 3 heads; schedule has 1 milestone, not 14; risk section is boilerplate | "Presence isn't quality. This is where manual appraisal is inconsistent — ours isn't." |
| 5 | Benchmark | 0:50 | ₹/km plotted against the distribution for comparable hill-terrain road projects — this DPR sits at the 91st percentile | "41% above the median for comparable terrain. That's a question worth asking before sanction." |
| 6 | **WOW** | 1:40 | Risk panel: 68% probability of >20% cost overrun; SHAP bars naming drivers. Then the provenance slide: *"trained on N real central-sector projects with recorded cost and schedule outcomes"* plus a calibration curve | "This number isn't an opinion. It comes from a model trained on real government project outcomes — and here's the calibration proving it's honest." |
| 7 | Human loop | 0:50 | Officer overrides one finding with a reason; draft appraisal note generated and exported | "The system drafts. The officer decides. Every override is logged." |
| 8 | Portfolio | 0:45 | Dashboard: 62% of DPRs from one state lack clearance evidence | "Now the ministry can fix the cause, not just the symptom." |

**WOW moment: stage 6 — the risk score plus its data provenance and calibration curve.** It converts your project from "an LLM said so" into "a model measured it," which is the entire game in this statement.

## 12. Judge Questions (15)

| # | Question | Testing | Strong answer | Avoid |
|---|---|---|---|---|
| 1 | "Where does the risk number come from?" | **The decisive question** | "A gradient-boosted model trained on real central-sector project records with original vs revised cost and original vs actual commissioning dates. We report probability with a calibration curve on held-out projects, and SHAP attributions naming each driver." | "The AI analyses the DPR and estimates risk." |
| 2 | "That dataset is central-sector projects, not MDoNER's smaller ones." | Whether you know your own limitation | "Correct, and we say so on the slide. We use it as a prior over sector, size band and terrain, adjusted by DPR-derived flags, and we report the reference population explicitly. With MDoNER's own historical data the model retrains in minutes — the pipeline is built for that." | Pretending the populations match. |
| 3 | "Who defined your quality rubric?" | Domain credibility | "It's derived from published DPR guidelines and standard appraisal checklists, and it's fully visible and editable in the UI with per-criterion weights, because appraisal standards are the ministry's to set, not ours." | "We designed a 100-point scale." |
| 4 | "How accurate is your table extraction on real DPRs?" | Engineering honesty | "We tested on N real DPRs from state portals. Native-PDF tables extract reliably; scanned and merged-cell tables are harder, so we flag low-confidence extractions for officer verification rather than scoring on data we're unsure of." | "It works." |
| 5 | "What if the LLM hallucinates an extracted figure?" | Safety | "Every extracted field carries a page citation the officer can click, extraction is schema-constrained, and numeric fields are cross-checked against totals in the document — an internal inconsistency is itself a flagged finding rather than a silent error." | "We use a good model." |
| 6 | "Could this reject a good project?" | Consequence awareness | "It can't reject anything — it produces a draft note with cited findings that an officer accepts or overrides, and every override is logged. It's designed to make appraisal consistent and fast, not autonomous." | "It's accurate enough." |
| 7 | "States might game the checklist." | Adversarial thinking | "Which is partly the point — a state that adds a genuine milestone schedule and resolves land acquisition to score better has made the project better. The gameable parts are the presence checks; the ungameable parts are benchmarked unit costs and clearance status, which are verified against external references." | "They can't game it." |
| 8 | "Where do you get DPRs to test on?" | Data honesty | "State PWD and urban-body portals, tender documents, and NE project sites publish them. We built our test set from N real ones covering roads, water supply and buildings, then synthesised format variants for volume." | "We made a sample DPR." |
| 9 | "How long does a 400-page DPR take?" | Practicality | "Two to four minutes end to end, asynchronous. Against weeks of manual appraisal, and the officer's reading time drops because findings are pre-located." | "It's fast." |
| 10 | "Cost per DPR?" | Economics | "LLM extraction on a 400-page document costs a few rupees, and it's a one-time cost per DPR. Parsing and the risk model are free. At MDoNER's volume this is a rounding error against the value of catching one overrun early." | "Depends on usage." |
| 11 | "Security — DPRs contain commercially sensitive costing." | Governance | "RBAC by role and state, encrypted storage, signed URLs, full access audit, and an on-premise model path for deployment so documents needn't leave the ministry's boundary. In the prototype we're explicit that we use an API." | "It's secure." |
| 12 | "What if the model is systematically biased against certain states?" | Fairness | "We check exactly that — we report predicted-vs-actual overrun rates disaggregated by state and sector on held-out data, and terrain is an explicit feature so hill projects aren't penalised for being hill projects. If disparity appears, it's visible rather than hidden." | "The model is objective." |
| 13 | "How would MDoNER adopt this?" | Deployment | "Shadow appraisal first — run it alongside the manual process for a quarter, compare findings, and measure how often the system caught something the officer didn't and vice versa. Then it becomes a first-pass tool with officers on top." | "They'd deploy it." |
| 14 | "What happens as guidelines change?" | Maintainability | "The rubric is configuration with versioning, so an appraisal from last year can be reproduced under the rules that applied then. Same for the risk model — the model and its training snapshot are versioned together." | "We'd update the code." |
| 15 | "What's the weakest part?" | Self-awareness | "The transfer gap between our training population and MDoNER's project profile, and table extraction on poor scans. Both are visible in the UI as confidence indicators rather than hidden behind a confident number." | "Nothing." |

## 13. Failure Modes & Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Table extraction fails on real DPRs | **High** | High | Multiple extractors with fallback; confidence flags; officer verification queue |
| Risk model has too little data / poor calibration | Medium | High | Use the largest public source; report calibration honestly; wide probability bands |
| LLM hallucinated fields | Medium | High | Schema constraints, page citations, internal-consistency cross-checks |
| Rubric seen as arbitrary | Medium | High | Derive from published guidelines; make weights visible and editable |
| Can't obtain enough real DPRs | Medium | Medium | Start collection on day 1; synthesise variants |
| Section identification breaks on varied formats | High | Medium | Embedding-based matching, not regex; graceful "section not found" reporting |
| Processing too slow to demo | Medium | Medium | Pre-process demo DPRs; ingest one live for theatre only |
| Judges question AI judging government projects | Medium | Medium | Human-in-the-loop framing throughout; the system never decides |

## 14. Development Difficulty

| Dimension | Rating |
|---|---|
| Frontend | 6/10 |
| Backend | 7/10 |
| AI/ML | 6/10 — LLM extraction plus a small tabular model |
| **Data** | **8/10** — real DPR collection + public outcome dataset assembly is the heavy lift |
| Integration | 4/10 |
| Deployment | 4/10 |
| Testing | 7/10 — extraction accuracy and model calibration both need measurement |
| **Overall** | **7/10** |

**Overall Development Risk: MEDIUM–HIGH**, concentrated in data acquisition and PDF table extraction — both of which are grind rather than genius, which means they respond to effort but not to cleverness at 3 a.m.

## 15. Team Requirements (6)

| Role | People | Responsibility |
|---|---|---|
| **Data/domain lead** | 1–2 | **Starts day 1:** collect real DPRs, assemble the public outcome dataset, derive the rubric from published guidelines. This role decides whether the project succeeds |
| ML | 1 | Risk model, SHAP, calibration, benchmarking statistics |
| Backend/document | 1–2 | Parsing, table extraction, LLM extraction pipeline, async orchestration |
| Frontend | 2 | Viewer with citation highlighting, scorecard, risk panel, dashboard |

## 16. Time Estimation

| Milestone | Effort |
|---|---|
| 24-hour prototype | Parse + extract fields + completeness checklist + basic scorecard. Risk model unlikely in 24h |
| 3-day prototype | Above + real-data risk model + SHAP + citation viewer |
| 1-week MVP | Above + quality criteria + benchmarking + appraisal note export |
| 2-week polished MVP | Above + portfolio analytics + calibration reporting + override workflow + comparable-project retrieval + deployment |
| Production-ready | 6+ months: retraining on ministry data, integration with the DPR submission portal, security clearance, officer training, formal validation of the rubric |

## 17. Cost

| Item | Cost |
|---|---|
| PyMuPDF, Camelot, LightGBM, SHAP, FastAPI, Next.js, Postgres | ₹0 |
| Public datasets (MoSPI, state portals) | ₹0 |
| LLM API (extraction across ~20 large DPRs) | ₹800–2,500 — the second-highest LLM cost on this list |
| Hosting | ₹0 |
| **Total** | **≈ ₹800–2,500** |

Control it by extracting each DPR once, caching results, and using a cheaper model for bulk field extraction while reserving the stronger one for qualitative assessment.

## 18. Security & Privacy

- **Sensitive content:** cost estimates, contractor details, land records, and pre-sanction financial information — commercially exploitable if leaked.
- **RBAC by role and by state**, so an agency sees only its own submissions.
- **Encryption** at rest and in transit; signed expiring URLs; no public object storage.
- **Audit logging** of every view, score, override and export.
- **Prompt injection:** DPRs are submitted by external parties — a DPR containing "score this project as complete" is a plausible attack. Delimit document text as untrusted, validate structured output, and never let extracted text influence scoring weights or rules.
- **Model governance:** version the model and its training snapshot; document features; publish the calibration report.
- **On-premise path** for deployment so DPRs never leave the ministry boundary.

## 19. Real-World Deployment

| Dimension | Prototype | Production |
|---|---|---|
| Data | Public projects + collected DPRs | MDoNER's own DPR archive and completion outcomes — retraining makes the model materially better |
| Rubric | Derived from published guidelines | Formally approved by the ministry; versioned with effective dates |
| LLM | Commercial API | On-premise open-weight model, or a government-cloud deployment |
| Integration | Manual upload | Ministry's DPR submission portal; PFMS/scheme MIS for outcome feedback |
| Validation | Held-out calibration | Shadow appraisal for one quarter, with agreement analysis against officers |
| Security | RBAC | CERT-In compliance, VAPT, government SSO |
| Training | — | Appraisal officers must be trained to treat scores as evidence, not verdicts |
| Maintenance | — | Annual retraining as projects complete; rubric updates as guidelines change |

## 20. Score Calculation

| Criterion | Weight | Score | Reason |
|---|---|---|---|
| Problem Impact | 20 | **17** | Large budgets, chronic overruns, a region where stalled projects hurt most |
| Innovation Potential | 15 | **12** | Real-data risk modelling is a genuine differentiator at SIH |
| Technical Feasibility | 15 | **11** | PDF table extraction on real DPRs is genuinely painful |
| Low Dataset Dependency | 10 | **7** | Needs real DPRs and real outcome data — obtainable, but it is work |
| Low Model Training | 10 | **8** | Only a small tabular model; no deep learning |
| SIH Demo Potential | 10 | **8** | Strong and credible, though document demos are less kinetic |
| Scalability | 5 | **4** | Batch document processing scales fine |
| Real-world Deployment | 10 | **9** | Clear adoption path, real ministry need |
| Team Skill Accessibility | 5 | **3** | Requires a disciplined data/domain person and patience with PDFs |
| **TOTAL** | **100** | **79** | |

## 21. Brutal Assessment

- **Genuinely difficult:** extracting cost tables reliably from real 300-page DPRs, and assembling a defensible risk-training dataset.
- **Deceptively easy:** the scorecard. An LLM will happily produce a plausible-looking 100-point score in an afternoon, and it will be worthless the moment a judge asks where the number came from.
- **What could kill it:** starting data collection on day 3. If you have no real DPRs and no outcome dataset by day 2, this project degenerates into exactly the competitor project you were trying to beat.
- **What could impress judges:** the calibration curve and the data-provenance slide. That combination signals a team that understands what a prediction *is*, which is rare at any hackathon.
- **What could make judges reject it:** an unexplained risk percentage, or an arbitrary rubric.
- **Worth choosing?** Only if one team member genuinely enjoys data work and will own it from hour one. With that person, this has the highest ceiling on your list after PS 65. Without them, it is the most likely to collapse into mediocrity.
- **Would I personally choose it?** **MAYBE** — a strong yes with the right data person, a firm no without one.

---
---

# ⑥ PS 54 — On-spot Assessment of Rooftop Rainwater Harvesting & Artificial Recharge Potential
**Organisation:** Ministry of Jal Shakti (CGWB) · **Category:** Software · **Theme:** Smart Automation
**Score: 79/100 · Recommendation: MAYBE — beautiful demo, thin technical core unless you add the geospatial layer**

## 1. Problem Understanding

India's groundwater is over-extracted across large parts of the country, and rooftop rainwater harvesting (RTRWH) with artificial recharge (AR) is one of the few interventions an individual household can make. Many states now mandate it for new buildings, and subsidies exist. Yet uptake is poor, for a practical reason: **an ordinary citizen cannot find out what to build.**

To size an RTRWH system you must know local rainfall, the roof's catchment area and material, the number of dwellers, the local aquifer type and its recharge capacity, the depth to the water table, and the soil's infiltration behaviour. From these you compute harvestable volume, then choose a recharge structure — a recharge pit, a trench, a shaft, a dug well or a recharge borewell — and size it. Today that assessment requires a site visit by someone from the Central Ground Water Board or a consultant. That does not scale to crores of households.

**Users:** homeowners, RWAs, small builders, panchayat and municipal officials, and CGWB field staff. **Beneficiaries:** the household (water security, lower bills, subsidy access) and the aquifer.

**What's wrong today:** no accessible tool exists that combines *location-specific hydrogeology* with *building-specific parameters* to produce a concrete, buildable recommendation with dimensions and costs. Generic online calculators ask for rainfall and roof area and return a volume — which tells a homeowner nothing about what to actually dig.

**Success:** a citizen opens an app at their house, the app knows where they are, auto-detects their roof, asks two or three questions, and returns: harvestable litres per year, the recommended structure type given the local aquifer and water-table depth, its dimensions, an estimated cost, expected payback, and how to apply for the applicable subsidy.

## 2. What the Statement REALLY Requires

**Mandatory**
- On-spot (i.e. mobile, at the location) assessment for a general public user.
- Determine RTRWH feasibility.
- Recommend the **type and size** of recharge structure — not just a water volume.
- Use local parameters: rainfall, aquifer, groundwater depth, roof area, dwellers.
- Provide cost estimation and cost–benefit.

**Implied**
- **"On-spot" means genuinely mobile and low-friction** — GPS, camera, offline tolerance, and a language the user reads. A desktop form is a misreading of the statement.
- **The recommendation must be defensible engineering**, grounded in CGWB's published design methodology rather than invented formulas. Getting the hydrology right is the credibility core.
- **Aquifer-awareness changes the answer.** A recharge borewell is right in one hydrogeological setting and wrong in another; recommending the same pit everywhere means you haven't solved the problem.
- **The average user does not know their roof area.** Asking for it in square metres guarantees garbage input — which is precisely why automatic roof detection is not a gimmick here but the fix for the biggest usability failure.
- **Aggregation matters as much as individual assessment.** A panchayat needs to see the ward-level potential; that view is what turns an app into a policy instrument.

**Optional:** AR/photo estimation, IoT integration, community leaderboards, contractor marketplace.

**Misunderstanding to avoid:** treating this as a calculator. If the entire product is `rainfall × area × runoff coefficient`, you have built a spreadsheet with a logo, and a judge will say so.

## 3. Proposed Solution

**Product concept:** *"JalDhara"* — a mobile-first, offline-capable, multilingual assessment app that auto-detects your rooftop from satellite imagery, combines it with local hydrogeology, and returns a buildable, costed recharge design.

**Core modules**
1. **Location & Roof Capture** — GPS fix; satellite/aerial basemap centred on the user; **automatic building-footprint detection**, with a draw/adjust fallback; area computed in m².
2. **Building Parameters** — roof material (affects runoff coefficient), number of dwellers, open space available for a structure, existing well or borewell presence, with visual pickers rather than text fields.
3. **Hydrogeology Lookup** — for the coordinates: annual and monsoon rainfall, principal aquifer type, depth to water table, and soil infiltration category, from preloaded CGWB/IMD-derived datasets.
4. **Feasibility & Sizing Engine** — deterministic hydrology: harvestable volume = area × rainfall × runoff coefficient × collection efficiency; first-flush allowance; then structure selection via a decision tree over aquifer type, water-table depth, available space and soil, followed by dimensioning per CGWB design guidance.
5. **Cost & Benefit** — material and excavation cost estimates by structure type and size; water-value savings; payback period; applicable state subsidy with a link to the scheme.
6. **Visual Output** — a scale diagram of the recommended structure, a bill of materials, and a step-by-step construction guide with images.
7. **Report & Share** — a PDF assessment the user can take to a mason, a contractor or a subsidy office.
8. **Offline Mode** — district-level hydrogeology packs cached on-device; assessments queue and sync when connectivity returns.
9. **Aggregation Dashboard** — for panchayat/municipal officials: assessments by ward, total potential recharge, adoption tracking, priority areas.

**Journey:** a homeowner in a water-stressed block opens the app → grants location → sees their own roof outlined automatically on the map → confirms it (or drags a corner) → picks roof type and dwellers from icons → gets, in seconds: "Your roof can harvest 1,42,000 litres a year. Your area sits on an alluvial aquifer with the water table at 18 m and sandy-loam soil. Recommended: a recharge shaft, 1.5 m diameter × 12 m deep with a filter chamber. Estimated cost ₹38,000. Payback 4.2 years. Your state offers a 50% subsidy — here's the form." → downloads the PDF → shows it to a mason.

## 4. AI/ML Requirement

**Classification: A/B — mostly no AI; one high-value pretrained computer-vision component. Zero training.**

Be honest about this and turn it into a strength: the hydrology *must* be deterministic, because a homeowner is going to dig a hole based on the answer.

| Component | Technique | Why |
|---|---|---|
| Volume & sizing calculations | **Deterministic formulas from CGWB guidance** | Engineering, not prediction. A learned model here would be indefensible |
| Structure selection | **Decision tree / rule engine over aquifer, water table, space, soil** | Transparent and matched to published practice |
| **Roof footprint detection** | **Pretrained segmentation — SAM, or a pretrained building-footprint model; or open building-footprint datasets covering India** | The one genuine AI component, and it solves the real usability problem. No training required |
| Roof material inference (optional) | **Pretrained image classifier on a user photo** | Sets the runoff coefficient without asking |
| Multilingual UI + voice | **Translation APIs / on-device TTS-STT; Bhashini for Indian languages** | Accessibility for the actual user base |
| Conversational guidance (optional) | **LLM API constrained to computed results** | Explains the recommendation; must never alter the numbers |

**Do NOT** predict groundwater levels with a neural network, or let an LLM compute the structure size. Both invite the question "what happens when it's wrong and someone builds it?"

## 5. Dataset Requirements

| Dataset | Why | Public? | Obtainable? | Synthetic? | Mock OK? |
|---|---|---|---|---|---|
| Rainfall (annual/monsoon normals) | Volume calculation | **Yes** — IMD normals, district-level | Yes | — | Use real |
| Principal aquifer map | Structure selection | **Yes** — CGWB aquifer mapping is published, and India-WRIS serves layers | Yes, with effort | — | Use real; pre-extract to district/block level |
| Depth to water table | Structure selection & depth | **Yes** — CGWB Ground Water Year Book and monitoring-well data | Yes, with effort | Partial | Use real where available, interpolate elsewhere |
| Soil/infiltration category | Sizing | **Yes** — NBSS&LUP soil maps, FAO soil data | Yes | — | Use real |
| Building footprints | Roof detection | **Yes** — open building-footprint datasets cover India, plus OSM | Yes | — | Use real |
| Satellite basemap | Visual + detection | Free tiles available | Yes | — | Use free tiles |
| Cost rates (materials, excavation) | Cost estimate | **Yes** — state PWD Schedules of Rates | Yes | Yes | Use real SoR items |
| Subsidy schemes | Actionability | **Yes** — state scheme pages | Yes | — | Use real for 3–4 states |

**Strategy that de-risks everything:** do **not** depend on live government WMS/API calls during the demo. Those services are slow and occasionally down, and a failed tile request in minute four of your pitch is unrecoverable. Instead, **pre-extract the layers you need into your own database at district/block granularity** and ship that. Then say on stage: "We pre-process public CGWB and IMD datasets into a queryable store — which is also what makes the app work offline in the villages that need it most." A weakness becomes an architectural decision.

**Biggest data risk:** water-table depth has genuinely sparse spatial coverage, so any point estimate is an interpolation. Handle it by showing a value *with its confidence and nearest-observation distance*, and by recommending conservative designs where uncertainty is high.

**Dataset Risk: MEDIUM** — everything is public, but the extraction and cleaning work is real and easy to underestimate.

## 6. Technical Architecture

```
Homeowner (mobile) / RWA / Panchayat official (web)
        |
        v
React Native or PWA (offline-first, multilingual)
  |-- Map + auto-detected roof polygon (editable)
  |-- Icon-based parameter entry
  |-- Result: structure diagram, BoM, cost, payback
  +-- Offline queue + sync
        |
        v
FastAPI Gateway
        |
   +----+--------------+------------------+------------------+
   v                   v                  v                  v
Geo Svc            Roof Detect Svc    Assessment Svc     Report Svc
(PostGIS spatial   (footprint lookup  (hydrology formulas,(PDF, BoM,
 queries: aquifer,  + SAM/pretrained   structure decision  construction
 rainfall, WT,      segmentation on    tree, sizing,       guide)
 soil, SoR rates)   the map tile)      cost, payback)
   |                   |                  |
   v                   v                  v
PostgreSQL + PostGIS        Object store (tiles, reports)
(pre-extracted CGWB/IMD/soil layers,
 assessments, aggregation views)
        |
        v
Free map tiles (OSM/MapLibre) - Bhashini/translation - optional LLM explanation
        |
        v
Panchayat aggregation dashboard (ward-level potential, adoption tracking)
```

## 7. Recommended Tech Stack

| Layer | Choice | Why here |
|---|---|---|
| Mobile | **React Native (Expo)** or a **PWA** | "On-spot" requires GPS and camera; a PWA is faster to build and installs without a store, which matters for rural distribution. Choose PWA if the team is web-strong |
| Maps | **MapLibre GL + OpenStreetMap / free satellite tiles** | Zero cost and no API-key risk on stage. **Avoid Google Maps billing** |
| Spatial backend | **PostgreSQL + PostGIS** | The whole product is point-in-polygon lookups against pre-extracted layers; PostGIS is exactly right and free |
| Backend | **Python + FastAPI** | GIS + CV ecosystem, and rasterio/GeoPandas for the ingestion pipeline |
| Roof detection | **Pretrained building-footprint data (primary) + SAM segmentation on the tile (fallback)** | Lookup first because it's instant and accurate; segmentation covers gaps |
| Offline | **Service worker + IndexedDB; district data packs** | Rural connectivity is the real constraint |
| PDF | **WeasyPrint** with a scale structure diagram (SVG) | The output must survive being handed to a mason |
| i18n | **i18next + Bhashini APIs** | Hindi, regional languages, and voice for low-literacy users |
| Deploy | **Docker Compose → free-tier VM; static PWA on a free host** | ₹0 |

## 8. MVP for SIH

**MUST HAVE**
1. Mobile UI with GPS location and map.
2. **Automatic roof-footprint detection** with manual adjust; area computed.
3. Pre-extracted hydrogeology database (rainfall, aquifer, water table, soil) for at least 2–3 states at block granularity.
4. Deterministic feasibility and volume calculation per CGWB methodology.
5. **Structure-type selection driven by local hydrogeology**, with dimensions.
6. Cost estimate and payback.
7. PDF assessment report with a scale diagram and bill of materials.

**SHOULD HAVE**
8. Offline mode with district data packs.
9. Multilingual UI (at least 3 languages) + voice input.
10. Panchayat aggregation dashboard.
11. Confidence display on interpolated water-table values.

**NICE TO HAVE**
12. Roof-material inference from a photo. 13. Subsidy scheme linkage per state. 14. Contractor/mason directory. 15. Community adoption map and impact counter. 16. AR overlay of the structure.

**Finish before presenting:** MUST + 8, 9, 10. Item 2 is the demo; item 5 is the credibility; item 10 is what elevates it from a consumer utility to a government tool.

## 9. Advanced Features

- **Auto roof detection** — the difference between a form and a product.
- **Aquifer-driven differentiation** — demo two locations 200 km apart, same roof, *different recommended structures*. That single comparison proves the whole thesis.
- **Uncertainty made visible** — water-table confidence and nearest-observation distance, with conservative designs where data is sparse.
- **Offline-first** — the households that need this most have the worst connectivity.
- **Voice + regional languages** — real accessibility for the actual user.
- **Buildable output** — dimensioned diagram, bill of materials, SoR-based costing. Not a number; a plan.
- **Panchayat aggregation** — ward-level potential recharge, adoption tracking, priority mapping.
- **Cumulative impact counter** — litres of recharge potential assessed across all users; a genuinely motivating public metric.
- **Subsidy linkage** — the last mile that turns intent into action.

## 10. Innovation Analysis

1. **Computer vision removing the hardest input.** Nobody knows their roof area; the app knows it.
2. **Hydrogeology-driven recommendation**, not a universal formula — two users get different structures for a reason you can explain.
3. **Offline-first architecture** designed around rural reality rather than demo convenience.
4. **Buildable output** — dimensions, materials, cost, subsidy — instead of a volume figure.
5. **Uncertainty communication** — rare in citizen apps and exactly right when someone will dig based on the answer.
6. **Individual → community aggregation**, turning household actions into a planning dataset.

**What competitors will build:** a form with rainfall and roof area, one formula, one generic pit recommendation, and a bar chart. Weaknesses: manual area entry, no aquifer awareness, no structure design, no offline mode, no aggregation.

**The honest risk:** even done well, the technical core is arithmetic plus a lookup. Your differentiation is CV + GIS + offline + accessibility. If you strip those, this becomes the weakest project on your list. If you build them, it becomes the most *humane* one, and it demos beautifully.

## 11. SIH Demo Strategy (8 minutes)

| # | Stage | Time | Screen | Say |
|---|---|---|---|---|
| 1 | Problem | 0:45 | Groundwater-stress map of India; a citizen asking "what do I build?" | "The scheme exists. The subsidy exists. What doesn't exist is an answer a homeowner can act on." |
| 2 | On-spot | 0:40 | Phone in hand, GPS lock, satellite view of an actual house | "On-spot means on a phone, at the house." |
| 3 | **WOW #1** | 0:50 | Roof outline appears automatically over the building; area 148 m² | "Nobody knows their roof area. That's why every existing calculator fails at question one." |
| 4 | Input | 0:30 | Three icon taps: roof type, dwellers, open space | "Three taps. No jargon." |
| 5 | Result | 1:10 | Harvestable 1,42,000 L/yr; alluvial aquifer, water table 18 m, sandy loam → **recharge shaft, 1.5 m × 12 m**; scale diagram; ₹38,000; payback 4.2 yrs | "Not a number — a design, with dimensions and a bill of materials." |
| 6 | **WOW #2** | 1:00 | Jump to a second location in hard-rock terrain with a shallow water table. Same roof, same rainfall — **different recommended structure** with the reason shown | "Same roof, different ground, different answer. That's the difference between a calculator and an assessment." |
| 7 | Reality | 0:50 | Switch the phone to airplane mode and run a full assessment offline | "The villages that need this have the worst connectivity. So it works without any." |
| 8 | Access | 0:35 | Switch to a regional language; voice input | — |
| 9 | Scale | 0:50 | Panchayat dashboard: ward-level assessments, aggregate recharge potential, priority wards | "One household saves water. A panchayat plans an aquifer." |

**WOW moments: stage 3 (the roof detecting itself) and stage 6 (two locations, two different structures).** Stage 7's airplane-mode moment is the credibility clincher and takes ten seconds.

## 12. Judge Questions (14)

| # | Question | Testing | Strong answer | Avoid |
|---|---|---|---|---|
| 1 | "Isn't this just a calculator?" | **The decisive question** | "The arithmetic is deliberately deterministic, because someone digs a hole based on the answer. The engineering is everywhere else: automatic roof detection, point-in-polygon hydrogeology, a structure-selection decision tree grounded in CGWB design guidance, offline district packs, and panchayat aggregation. A calculator asks you for the roof area — we're solving the problem that you don't know it." | "We use AI to calculate it." |
| 2 | "Where does your hydrogeology data come from?" | Data credibility | "Published CGWB aquifer mapping and groundwater monitoring, IMD rainfall normals, and NBSS&LUP soil data — pre-extracted into PostGIS at block granularity so lookups are instant and work offline." | "We estimated it." |
| 3 | "How accurate is roof detection?" | CV honesty | "We use open building-footprint data as the primary source, which is accurate for most established buildings, and pretrained segmentation as a fallback for gaps and new construction. The user can always adjust the polygon, and we show the computed area so an error is visible and correctable in one drag." | "It's very accurate." |
| 4 | "What if the water-table value is wrong?" | Uncertainty | "Monitoring wells are sparse, so any point value is interpolated — and we say so in the UI with a confidence indicator and the distance to the nearest observation. Where confidence is low we recommend the more conservative structure. We'd rather show uncertainty than hide it." | "Our data is accurate." |
| 5 | "Would CGWB endorse these designs?" | Domain credibility | "The methodology follows CGWB's published design guidance for recharge structures, and the parameters are configurable so CGWB can adjust coefficients per region. We'd want their validation before public release, and the architecture assumes it." | "We designed our own formulas." |
| 6 | "Where is the AI?" | Architecture honesty | "In the one place it belongs: computer vision to detect rooftops, which removes the input users can't provide. The hydrology is deliberately deterministic — a probabilistic estimate of how deep to dig would be irresponsible. Using AI selectively is a design decision, not a limitation." | Overclaiming AI. |
| 7 | "Who would use this? Rural users have basic phones." | Adoption realism | "Three channels: a PWA that installs without an app store and runs offline, regional languages with voice input for low-literacy users, and an assisted mode where a panchayat worker or CSC operator runs assessments on a citizen's behalf. The panchayat dashboard is designed for exactly that." | "Everyone has smartphones now." |
| 8 | "Cost to run at national scale?" | Economics | "Very low — free map tiles, self-hosted PostGIS, no per-query paid APIs, and building-footprint data ingested once. That's a deliberate choice: a scheme meant for crores of households can't be built on per-call billing." | "We'd use Google Maps." |
| 9 | "How do you handle the cost estimate?" | Practicality | "From state PWD Schedules of Rates for the actual line items — excavation, filter media, masonry — so it's regionally accurate and updatable, not a national guess." | "We estimated typical costs." |
| 10 | "What if there isn't enough open space?" | Domain depth | "The decision tree handles it — with limited space we recommend a shaft or borewell recharge rather than a pit or trench, and if nothing is feasible we say so plainly rather than recommending something that won't fit." | "We'd suggest a smaller pit." |
| 11 | "Privacy — you're collecting home locations." | Governance | "Assessments are anonymous by default; no login is required to get a result. Aggregation is done at ward level, never at household level in the public dashboard, and precise coordinates are stored only if the user opts in for subsidy assistance." | "It's just a location." |
| 12 | "How does this scale beyond your 3 states?" | Scalability | "The layers are national — CGWB aquifer mapping, IMD rainfall and soil data all cover India. Extending is an ingestion job per state, not a code change, and we built the pipeline to be re-run." | "We'd add more data." |
| 13 | "What stops someone building it wrong?" | Consequence | "The report is a design brief, not a construction certificate — it includes a step-by-step guide and explicitly recommends verification by a local mason or CGWB officer for large installations. We're closing an information gap, not replacing site engineering." | "The design is correct." |
| 14 | "Why offline? Everyone has data." | Whether you know your user | "Not in the blocks with the worst groundwater stress. Offline isn't a nice-to-have here; it's the difference between a demo and a deployment — which is why we cache district packs on device and queue assessments for sync." | "It's a bonus feature." |

## 13. Failure Modes & Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Government WMS/API slow or down mid-demo | **High** | Fatal | Pre-extract all layers into your own PostGIS — never call them live |
| Roof detection misses a building | Medium | Medium | Footprint data primary, segmentation fallback, manual adjust always available |
| Water-table data sparse/stale | High | Medium | Confidence display, conservative defaults, interpolation with visible caveats |
| Map tile provider throttles | Medium | High | Self-host or cache tiles for demo areas |
| Perceived as a calculator | **High** | High | Lead with the two-locations comparison; foreground CV, GIS and offline |
| Cost estimates unrealistic | Medium | Medium | Base on real SoR line items and cite the source |
| Offline sync bugs | Medium | Medium | Keep the offline scope narrow — cached read data plus a queued write |

## 14. Development Difficulty

| Dimension | Rating |
|---|---|
| Frontend/mobile | 7/10 — offline PWA plus map interaction |
| Backend | 5/10 |
| AI/CV | 5/10 — pretrained only |
| **Data/GIS** | **7/10** — layer extraction and cleaning is the real work |
| Integration | 5/10 |
| Deployment | 4/10 |
| Testing | 5/10 |
| **Overall** | **6/10** |

**Overall Development Risk: MEDIUM** — the risk is front-loaded in GIS data preparation, which is tedious and must start on day 1.

## 15. Team Requirements (6)

| Role | People | Responsibility |
|---|---|---|
| GIS/data | 1–2 | **Day 1:** extract and clean CGWB/IMD/soil layers into PostGIS; SoR cost rates |
| Mobile/frontend | 2 | PWA, map, roof polygon interaction, offline, i18n |
| Backend | 1 | FastAPI, PostGIS queries, assessment engine, PDF |
| CV | 1 (can overlap) | Footprint lookup + segmentation fallback |
| Domain | 1 (overlaps) | CGWB methodology, structure decision tree, validation, demo script |

## 16. Time Estimation

| Milestone | Effort |
|---|---|
| 24-hour prototype | Map + manual roof polygon + one district's data + calculation + result screen |
| 3-day prototype | Above + auto roof detection + structure decision tree + cost + PDF report |
| 1-week MVP | Above + 2–3 states of data + offline mode + multilingual + panchayat dashboard |
| 2-week polished MVP | Above + voice + subsidy linkage + confidence display + polish + deployment |
| Production-ready | 4–6 months: CGWB validation of the methodology, national data coverage, app-store release, accessibility audit, integration with state subsidy portals |

## 17. Cost

| Item | Cost |
|---|---|
| PostGIS, FastAPI, MapLibre, React/RN, SAM or footprint data | ₹0 |
| Map tiles (OSM/free satellite) | ₹0 — **do not use billed Google Maps** |
| Public datasets (CGWB, IMD, soil, SoR) | ₹0 |
| Translation/voice (Bhashini free tier) | ₹0 |
| Hosting | ₹0 |
| **Total** | **≈ ₹0** — the cheapest project on this list |

## 18. Security & Privacy

- **Sensitive data:** precise home locations and building footprints — combined, that is household-identifying information.
- **Anonymous by default:** no account needed for an assessment; store coordinates only with explicit opt-in.
- **Aggregate only at ward level** in any public or official dashboard; never expose household points.
- **Encryption** in transit; minimal retention; clear deletion path.
- **Consent language in the user's own language**, not an English wall of text.
- **API security:** rate limiting on the assessment endpoint; no PII in URLs.
- **Offline data on device** is public reference data only — no personal data cached beyond the user's own queued assessments.

## 19. Real-World Deployment

| Dimension | Prototype | Production |
|---|---|---|
| Coverage | 2–3 states, block granularity | National, with an automated refresh pipeline as CGWB publishes updates |
| Validation | CGWB published methodology | Formal CGWB endorsement of coefficients and structure-selection logic — essential before public advice |
| Distribution | PWA link | App stores + CSC/panchayat assisted mode + integration into state water portals |
| Integration | — | State subsidy portals, Jal Shakti dashboards, Atal Bhujal-type scheme reporting |
| Accessibility | 3 languages | Full Indian-language coverage, voice-first flows, accessibility audit |
| Infra | One VM | Autoscaled read-heavy service with tile caching and a CDN |
| Maintenance | — | Annual data refresh; SoR rates update yearly; structure guidance follows CGWB revisions |

## 20. Score Calculation

| Criterion | Weight | Score | Reason |
|---|---|---|---|
| Problem Impact | 20 | **17** | Water security, mass public reach, aligned with active national schemes |
| Innovation Potential | 15 | **9** | The CV + GIS + offline combination is good; the core computation is arithmetic |
| Technical Feasibility | 15 | **13** | Very achievable; GIS prep is the main effort |
| Low Dataset Dependency | 10 | **6** | All public, but extraction and cleaning is substantial and easy to underestimate |
| Low Model Training | 10 | **9** | Pretrained CV only |
| SIH Demo Potential | 10 | **9** | Maps, auto-detected roofs and an offline moment demo beautifully |
| Scalability | 5 | **4** | Read-heavy and cacheable; national coverage is an ingestion effort |
| Real-world Deployment | 10 | **8** | Genuinely deployable; CGWB validation is the gate |
| Team Skill Accessibility | 5 | **4** | Needs a GIS-comfortable person |
| **TOTAL** | **100** | **79** | |

## 21. Brutal Assessment

- **Genuinely difficult:** extracting and cleaning national hydrogeology layers into a queryable form, and making offline mode actually work.
- **Deceptively easy:** the assessment itself. The formula is a few lines. That is precisely the trap — a working "calculator" on day one will make you feel finished while you have built the least valuable part.
- **What could kill it:** relying on live government geospatial services during the demo, or shipping without auto roof detection — the app then looks like every online rainwater calculator.
- **What could impress judges:** the roof detecting itself, two locations yielding two different structures, and the airplane-mode assessment.
- **What could make judges reject it:** "where's the technical depth?" — a fair question if you skip the CV and GIS layers.
- **Worth choosing?** Yes if your team is strong on mobile/GIS and wants a project with visible human impact and near-zero data risk. It is the friendliest, most humane statement on your list and the cheapest to build.
- **Would I personally choose it?** **MAYBE.** Excellent demo, high social impact, but the lowest algorithmic ceiling of the six statements above it. Against strong optimisation projects it can read as "a very good app" rather than "a hard problem solved."

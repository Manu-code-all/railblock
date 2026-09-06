---
---

# ① PS 65 — AI-Driven Train Induction Planning & Scheduling, KMRL
**Organisation:** Government of Kerala (Kochi Metro Rail Limited) · **Category:** Software · **Theme:** Smart Automation
**Score: 87/100 · Recommendation: YES — this is my pick**

## 1. Problem Understanding

**Teach it to a team that has never seen it.** Every night between roughly 21:00 and 23:00, a small group of KMRL supervisors decides what each trainset does tomorrow. Each trainset lands in exactly one of three buckets:

- **Revenue service** — it carries passengers tomorrow morning, and it needs a turn-out order and a stabling position that lets it exit the depot on time.
- **Standby** — parked ready, used if something fails in service.
- **Inspection Bay Line (IBL) / maintenance** — held back for work.

The decision is not one-dimensional. Six interacting variables have to be reconciled simultaneously:

1. **Fitness Certificates (FC).** Three independent departments — Rolling-Stock, Signalling, Telecom — each issue a validity window per trainset. If *any* of the three has expired, the train legally cannot enter revenue service. These windows live in different systems and expire at awkward hours.
2. **Job-card status.** Open/closed work orders from IBM Maximo. An open safety-critical job card blocks service; a cosmetic one may not.
3. **Branding priorities.** Advertiser wraps are sold with *contractual exposure hours*. If a wrapped trainset sits in the depot for a week, KMRL is in breach and owes make-good. Branding therefore pulls toward running specific trainsets.
4. **Mileage balancing.** Bogies, brake pads and HVAC units wear per kilometre. If the same four trainsets always run, they hit overhaul thresholds together and you lose a quarter of the fleet at once. Kilometres must be *equalised across the fleet* — which pulls directly against branding.
5. **Cleaning & detailing slots.** Deep cleaning needs a specific bay, a crew and a window. Night manpower is limited.
6. **Stabling geometry.** The depot is a physical yard of stabling lines. If tomorrow's first train out is parked behind three others, you must *shunt* — each shunt costs time, energy, a driver, and risks the morning turn-out. Bad geometry is how a plan that looks fine on paper causes an 06:00 delay.

**Who experiences the problem:** the depot supervisor and the Operations Control Centre. **Intended user:** depot planning staff and rolling-stock engineers. **Beneficiary:** the daily ridership, plus KMRL finance — unplanned withdrawals and branding penalties cost real money.

**Existing workflow:** messages from three departments, a Maximo export, a hand-maintained spreadsheet, and one experienced supervisor's memory — executed under time pressure, at night, in under two hours.

**What's wrong with it:** it does not scale (the fleet is heading from ~25 toward 40 trainsets across two depots), it is undocumented (when the supervisor retires the knowledge leaves), it optimises nothing (it finds *a* feasible answer, not a good one), it has no audit trail, and it cannot answer "what happens if trainset 12's telecom certificate expires at 04:00?"

**What success looks like:** a ranked, explained induction list produced in seconds, every constraint checked, conflicts flagged before they bite, and instant re-planning when reality changes. KMRL's stated ambition is to hold punctuality ≥99.5% while the fleet nearly doubles.

## 2. What the Statement REALLY Requires

**Mandatory**
- Ingest the six variable families and produce a nightly decision per trainset: service / standby / IBL.
- Reconcile *conflicting* objectives, not merely filter on constraints.
- Explain each decision — the statement explicitly asks for reasoning, not a black box.
- Flag conflicts and rule violations *before* they cause a service failure.
- Handle heterogeneous, siloed inputs (Maximo exports, spreadsheets, manual entries).

**Implied — this is where you win, because most teams miss all six**
- **Stabling geometry is a routing problem, not a label.** "Bay 4, position 3" implies shunt-move counting. Most teams will store a bay number and stop. Model the yard as a graph of LIFO stabling lines and *count the shunts*.
- **The output has a time dimension.** Turn-out order matters: the 05:45 departure must be physically reachable at 05:45.
- **Certificates expire mid-plan.** A trainset valid at 23:00 may be invalid at 04:00. Validity must be checked against *tomorrow's service window*, not against now.
- **Mileage balancing is longitudinal.** A one-night greedy choice is wrong; you need a 7–30 night horizon for fleet variance to actually converge.
- **The system must degrade gracefully.** If a train fails at 05:00, someone needs a new plan in under a minute — changing as little as possible.
- **The "learning" the statement mentions** is best delivered as parameter tuning and failure-risk scoring, not as a neural planner.

**Optional / nice-to-have:** IoT telemetry, energy optimisation, crew rostering, multi-depot expansion, supervisor mobile app.

**The most common misunderstanding:** teams read "AI-Driven" and build a model that predicts a schedule. That is wrong on every axis — unexplainable, untrainable without data, and strictly worse than a solver. The correct reading is *decision support with an optimisation core and ML at the edges*.

## 3. Proposed Solution

**Product concept:** *"Nightly Induction Copilot"* — turns six siloed data streams into one ranked, explained, simulatable induction plan, on a live depot map.

**Core modules**
1. **Ingestion & Normalisation** — connectors for Maximo job cards (CSV/REST), three FC department feeds, branding contracts, mileage logs, cleaning roster, yard occupancy. Everything lands in one canonical `TrainsetState` snapshot with per-source freshness tracking.
2. **Rule & Eligibility Engine** — deterministic hard constraints: expired FC ⇒ ineligible; open safety job card ⇒ ineligible; mileage past threshold ⇒ forced IBL. Emits a machine-readable *why*.
3. **Optimisation Engine (the heart)** — a CP-SAT model assigning each trainset to {service, standby, IBL}, giving service trains a turn-out slot, IBL trains a bay, and everything a stabling position — minimising a weighted multi-objective cost.
4. **Yard / Shunting Model** — depot as a graph of LIFO stabling lines; computes the shunt moves an assignment implies and feeds that cost back into the objective.
5. **Explainability Layer** — per-trainset rationale: *"TS-07 → Standby. Telecom FC expires 04:20, before the 05:45 turn-out. Branding exposure deficit 6.2h — schedule tomorrow."*
6. **What-If Simulator** — override any decision or inject a failure; the solver re-runs and shows the delta.
7. **Risk Module (light ML, optional)** — gradient-boosted model over job-card history estimating probability of unplanned withdrawal; used as a *soft cost*, never a hard gate.
8. **Audit & Reporting** — every plan versioned, every override attributed; KPI dashboard (punctuality proxy, mileage variance σ, branding SLA compliance, shunt-move count).

**User roles:** Depot Supervisor (generate/approve) · Rolling-Stock Engineer (constraints and thresholds) · Branding Officer (exposure targets) · OCC Controller (read-only + emergency re-plan) · Admin.

**End-to-end journey**
1. **21:00** — the system auto-pulls the day's data; the ingestion dashboard shows freshness per source and flags anything stale.
2. Supervisor opens *Tonight's Plan*. Pre-flight shows three alerts: "TS-04 Signalling FC expires in 6h", "TS-11 open job card J-4471 (brake) — safety critical", "TS-19 branding deficit 11h".
3. Supervisor clicks **Generate**. Solver runs, target < 10 s.
4. Output: colour-coded ranked induction list; depot map with every trainset in its assigned position; total shunt count for the night; objective breakdown chart.
5. Supervisor disagrees, drags TS-14 from Standby to Service. The system re-solves the remainder instantly and warns: *"Feasible, but shunt moves 6 → 9 and mileage σ worsens 4%."*
6. Supervisor approves. The plan is frozen, versioned, exported (PDF + CSV) and pushed to the crew view.
7. **05:00** — TS-03 fails. The controller clicks **Emergency Re-plan**; a new plan arrives in seconds under a minimum-disruption constraint.

**Inputs:** trainset master; FC records (3 types × validity windows); job cards; branding contracts + accumulated exposure; cumulative mileage per component; cleaning slots + crew availability; yard topology; tomorrow's service requirement (N trains, turn-out times).
**Processing:** normalise → validate → CP-SAT solve → explain → simulate.
**Outputs:** induction list, stabling plan, shunt schedule, conflict report, KPI deltas, audit record.
**Alerts:** FC expiring within 48h; branding SLA breach risk; mileage divergence beyond σ threshold; infeasible plan — reported with the *minimal conflicting constraint set*.
**Dashboard:** fleet heatmap, mileage-variance trendline, branding exposure vs contract, shunt-moves-per-night trend, plan-vs-actual punctuality.

## 4. AI/ML Requirement

**Classification: B — AI may be used, but pretrained/API models plus optimisation are entirely sufficient. Zero training from scratch.**

The intellectual core is **operations research, not machine learning**, and you should say so proudly on stage. The constraints are legal and hard (an expired fitness certificate is not a probability); the output must be auditable; there is no historical dataset to learn from; and a solver returns a *proof of optimality*, which is stronger evidence than any model's confidence score.

| Component | Technique | Why |
|---|---|---|
| Eligibility gating | **Rule engine** (deterministic) | Safety constraints must never be probabilistic |
| Induction assignment | **CP-SAT (OR-Tools)** | Multi-objective integer assignment under rich constraints — exactly its domain |
| Stabling / shunt minimisation | **Graph model integrated into CP-SAT**, or local-search post-pass | LIFO yard structure is combinatorial |
| Mileage balancing | **Rolling-horizon objective term** | Variance minimisation is an objective, not a prediction |
| Failure-risk score | **Classical ML — LightGBM/XGBoost** on job-card history | Tabular, small, SHAP-interpretable. Optional |
| Explanation prose | **LLM API as a renderer only** | Converts the solver's structured reason object into a sentence. It must never *decide* |
| Natural-language Q&A ("why is TS-7 on standby?") | **LLM + tool-calling over your own API** | Cheap differentiator, low risk |

**Explicitly do NOT:** train a neural scheduler, let an LLM produce the plan, or reach for reinforcement learning. All three are unexplainable, undemonstrable in a hackathon, and will be dismantled in Q&A.

## 5. Dataset Requirements

| Dataset | Why needed | Public? | Obtainable? | Synthetic OK? | Mock OK for SIH? |
|---|---|---|---|---|---|
| Trainset master (25→40) | Entity backbone | Partly | Yes | Yes | Yes |
| Fitness certificate records | Hard constraint | No | No | **Yes — trivially** | Yes |
| Maximo job cards | Hard/soft constraint | No | No | **Yes** — CMMS schema is standard | Yes |
| Branding contracts + exposure | Objective term | No | No | Yes | Yes |
| Cumulative mileage per component | Objective term | No | No | Yes | Yes |
| Cleaning roster + crew | Constraint | No | No | Yes | Yes |
| Depot yard topology (Muttom) | Shunt modelling | Approximately, via imagery/published layouts | Roughly | Yes | Yes |
| Timetable / service requirement | Demand side | **Yes — KMRL publishes it** | Yes | — | Use the real one |

**This statement's superpower:** it *enumerates every variable itself*. That makes a well-built synthetic generator the accepted methodology rather than a cop-out. Build a **parameterised scenario generator** (fleet size, FC-expiry distribution, job-card arrival rate, branding mix, yard size) and you can demo 25 trainsets *and* 40 *and* a two-depot future state. That is more impressive than real data, because it proves scalability.

**Biggest data risk:** getting yard topology subtly wrong so your shunt model doesn't match KMRL's reality. **Mitigation:** make topology *configurable* through a yard editor in the UI — then a wrong assumption is a settings change, not a design flaw, and you can say exactly that on stage.

**Dataset Risk: LOW.**

## 6. Technical Architecture

```
Depot Supervisor / RS Engineer / OCC Controller
        |  (browser, RBAC)
        v
React + TypeScript SPA
  |-- Plan Console (ranked list, drag-to-override)
  |-- Depot Yard Map (Canvas/SVG, animated shunts)
  |-- What-If Simulator
  +-- KPI Dashboard
        |  HTTPS / JWT
        v
FastAPI Gateway  <--------->  WebSocket channel (live solve progress)
        |
        +----------------+------------------+-------------------+
        v                v                  v                   v
  Ingestion Svc    Rule Engine Svc    Optimisation Svc     Explain Svc
  (connectors,     (eligibility,      (OR-Tools CP-SAT,    (reason object
   validation,      hard gates,        multi-objective,     -> LLM text,
   normalise)       conflict sets)     yard/shunt model)    NL Q&A)
        |                |                  |                   |
        v                v                  v                   v
   PostgreSQL  <---  Redis (cache + Celery broker)  --->   LLM API
   (state, plans,        long solves run async,
    audit, versions)     progress streamed back
        |
        v
  External: Maximo REST/CSV export - FC department feeds - KMRL timetable - S3/MinIO for plan PDFs
        |
        v
  Observability: OpenTelemetry -> Prometheus + Grafana; append-only structured audit log
```

**Component notes**
- **Optimisation as its own service** — solves are CPU-bound and bursty; isolating them lets you scale that container independently and keeps the API responsive. Run through Celery so a 60-second solve never holds an HTTP connection open.
- **Redis** caches the nightly normalised snapshot and brokers solve jobs, and backs the WebSocket progress feed. CP-SAT emits improving solutions as it works — streaming them makes the demo feel alive.
- **PostgreSQL, not a document store** — the domain is relational and audit-critical. Use versioned/temporal rows so any past plan is reconstructible.
- **No vector database.** Do not add one for decoration; a judge will ask why and you will have no answer.
- **Append-only audit log** with user, timestamp, before/after and KPI delta for every override. This is what makes it government-deployable rather than a toy.

## 7. Recommended Tech Stack

| Layer | Choice | Why *this* problem needs it |
|---|---|---|
| Frontend | **React + TypeScript + Vite** | Six interacting entities make types genuinely valuable; Vite keeps hackathon iteration fast |
| Visualisation | **Canvas (Konva) or D3 for the yard; Recharts for KPIs** | The yard map is the demo centrepiece — you need real drawing control, not a chart library |
| Backend | **Python + FastAPI** | Non-negotiable: OR-Tools' best-supported binding is Python and the solver *is* the product. Async FastAPI keeps the WebSocket feed clean |
| Optimisation | **Google OR-Tools CP-SAT** | Integer assignment, reified constraints, multi-objective, proof of optimality, and infeasibility cores. A genetic algorithm gives you none of the last three — which are exactly what impresses judges |
| Task queue | **Celery + Redis** | Solves must be async and cancellable |
| Database | **PostgreSQL 16** | Relational, transactional, temporal-friendly, free |
| Migrations | **SQLAlchemy 2.0 + Alembic** | Your schema will change nightly during the build |
| Risk model (optional) | **LightGBM + SHAP** | Trains in seconds on tabular data; SHAP gives per-trainset explanations |
| LLM | **Claude API (Sonnet-class)** for explanation rendering and NL Q&A | Touches presentation and query only, never decisions — a defensible architecture story |
| Auth | **JWT + server-side RBAC** | Simple, sufficient, demonstrable |
| Deploy | **Docker Compose → single VM (free tier); Render/Railway for a public backup link** | Near-zero cost, reproducible |
| Monitoring | **Prometheus + Grafana**, or structured logs if time-poor | Optional for MVP, strong on the production-readiness slide |

**Deliberately rejected — and say so if asked, it shows judgement:** MongoDB (the domain is relational), Kafka (there is no streaming volume at 40 trainsets), Kubernetes (over-engineering), custom neural networks (see §4).

## 8. MVP for SIH

**MUST HAVE** — without these there is no project
1. Domain model + synthetic scenario generator for 25 trainsets.
2. Rule engine producing eligibility plus machine-readable reasons.
3. CP-SAT model: assign service/standby/IBL under FC, job-card and cleaning-capacity constraints, balancing mileage and honouring branding exposure.
4. Ranked induction list UI with per-trainset explanation.
5. Conflict/alert panel including infeasibility explanation.
6. One-click generate in under 10 seconds.

**SHOULD HAVE** — these are what beat the other teams
7. Depot yard map with stabling positions and **shunt-move count inside the objective**.
8. What-if override → instant re-solve with KPI delta.
9. Emergency re-plan under a minimum-disruption constraint.
10. KPI dashboard (mileage σ, branding SLA, punctuality proxy).

**NICE TO HAVE**
11. LightGBM failure-risk score with SHAP. 12. Natural-language Q&A over the plan. 13. Scale demo at 40 trainsets / two depots. 14. Crew mobile read-only view. 15. Maximo-format CSV import demo.

**Finish before the presentation:** all MUST plus 7, 8 and 9. **Item 7 is the highest-leverage thing on this list** — real shunt counting is what separates you from a team that produced a sorted table.

## 9. Advanced Features (differentiators)

- **Infeasibility explanation.** CP-SAT assumption literals let you return the *minimal set of conflicting constraints*: "No feasible plan — 18 trains required, 16 hold valid FCs, cleaning-bay capacity blocks 2 more." Almost no other team will have this, and it is the most sophisticated thing you can put on screen.
- **Live objective weights.** A slider labelled *Branding ↔ Mileage Balance*; drag it and watch the plan and the yard rearrange. Judges instantly grasp that this is a real optimiser.
- **Shunt-move animation** — play the night's yard movements.
- **Rolling-horizon convergence chart** — simulate 30 nights and show fleet mileage σ falling. Proof the balancing objective *works*, not a claim that it does.
- **Digital-twin scenario library** — "normal night", "monsoon, 3 withdrawn", "festival service", "fleet of 40". One click, re-solve.
- **Two-level explainability** — structured reason objects for machines, LLM prose for humans, with a toggle.
- **Immutable audit trail** with override attribution and per-override KPI impact.
- **Accessibility that matches reality** — the plan gets read at 06:00 on a phone under depot lighting: high-contrast mode, large touch targets, offline PDF export.
- **Constraint editor** so KMRL staff can add a rule without a developer.

## 10. Innovation Analysis

**"What makes this more than a CRUD app?"**

1. **It decides, with a proof.** CRUD retrieves stored records; this returns a mathematically optimal assignment together with its optimality gap.
2. **It models the physical world.** Shunt minimisation over a LIFO track graph is a genuine combinatorial subproblem that virtually nobody will attempt.
3. **It prices trade-offs.** Interactive objective weights make the *cost of a preference* visible — which is what planners actually need and no dashboard provides.
4. **It explains impossibility.** Returning minimal conflict sets is harder than returning an answer, and it is the mark of a serious system.
5. **It optimises longitudinally.** Mileage variance converging over 30 simulated nights, shown live.
6. **It exercises architectural restraint.** Using AI only where it belongs is itself a differentiator in a field of teams over-applying LLMs.

**What other teams will build:** a dashboard listing trainsets, a rule-based filter, a hand-written greedy or genetic ranker, and an LLM prompt saying "given this data, suggest an induction plan." Their weaknesses: no optimality, no yard geometry, no infeasibility handling, hallucinated reasoning, no answer to "what happens when two constraints conflict?"

**How you are better:** a solver instead of heuristics, a modelled yard instead of a bay label, explanations instead of assertions, simulation instead of a static plan, and a live scale-up to 40 trainsets on stage.

## 11. SIH Demo Strategy (8 minutes)

| # | Stage | Time | On screen | Say |
|---|---|---|---|---|
| 1 | Problem | 0:45 | Night depot photo + spreadsheet + message-thread mock-up | "Every night, one person decides this in two hours from three message threads and a spreadsheet. The fleet is about to double." |
| 2 | Ingestion | 0:45 | Data-freshness dashboard, six source cards, three red alerts | "Six systems, one snapshot. Two fitness certificates expire before tomorrow's first service." |
| 3 | User action | 0:20 | Click **Generate Tonight's Plan** | — |
| 4 | Processing | 0:30 | Live solver progress, objective value dropping, "17,842 constraints · optimal in 4.2s" | "This is a constraint solver, not a guess. Seventeen thousand constraints, provably optimal." |
| 5 | Result | 1:30 | Ranked list + yard map filling in; hover a train → explanation | "TS-07 is standby because its Telecom certificate expires at 04:20 — before turn-out." |
| 6 | **WOW** | 1:30 | Drag TS-14 Standby→Service. Instant re-solve. Toast: *"Feasible. Shunt moves 6→9 (+3 driver movements). Mileage σ worsens 4%. Branding SLA still met."* Then drag the Branding↔Mileage slider and watch the plan and yard rearrange live | "The supervisor stays in control — but now they can see the price of every decision." |
| 7 | Robustness | 0:45 | Inject TS-03 failure at 05:00 → Emergency re-plan → minimum-disruption diff highlighted | "Reality breaks the plan. We recover in four seconds, changing as little as possible." |
| 8 | Impact & scale | 1:00 | 30-night mileage-σ convergence chart, then switch to **40 trainsets / 2 depots** and re-solve live | "Same model, forty trainsets, two depots — seven seconds. That's KMRL's 2027 fleet." |
| 9 | Close | 0:35 | Architecture slide + audit log | "Deterministic where safety demands it, optimised where money is, explained everywhere." |

**The WOW moment is stage 6 — the override that instantly quantifies its own cost.** It converts an abstract optimiser into something a judge can feel. Rehearse it until it is flawless, and run every scenario from preloaded local data so nothing depends on the venue's network.

## 12. Judge Questions (15)

| # | Question | What's being tested | Strong answer | Weak answer to avoid |
|---|---|---|---|---|
| 1 | "Where is the AI? This is rules and a solver." | Whether you understand your own architecture | "Deliberate. Safety constraints must be deterministic and auditable — an expired fitness certificate is not a probability. The intelligence is combinatorial optimisation over 17,000 constraints, plus ML for failure-risk scoring and an LLM for explanation. A neural planner here would be unexplainable and unsafe." | "We can add deep learning later." |
| 2 | "You have no real KMRL data. What does this prove?" | Data honesty | "The statement enumerates all six variable families, so we built a generator matching those semantics — which let us validate at 25, 40 and two-depot scale, something real data wouldn't allow. Every input is schema-mapped to Maximo and the FC registers; swapping in live feeds is a connector change, not a redesign." | "We used dummy data because we couldn't get real data." |
| 3 | "How accurate is it?" | Whether you know what 'accurate' means here | "Accuracy is the wrong metric for a solver — feasibility and optimality are. We report 100% hard-constraint satisfaction, verified by an independent checker; the objective value against the solver's proven bound; and against a simulated 30-night baseline we cut mileage variance by X% and shunt moves by Y%." | "About 90%." |
| 4 | "What if the solver takes too long?" | Engineering realism | "CP-SAT is anytime. We cap at 30 seconds and take the best incumbent with its optimality gap shown. At fleet size 40 we're around 7 seconds. If it ever degrades we fall back to a warm-started greedy and label the plan 'heuristic'." | "It's fast." |
| 5 | "What if no feasible plan exists?" | Depth | "We solve with assumption literals and return the minimal conflicting constraint set — 'need 18, only 16 have valid FCs, cleaning capacity blocks 2' — then offer relaxations ranked by cost." | "It shows an error." |
| 6 | "Would a supervisor actually trust this?" | Adoption realism | "It never auto-commits. It proposes, explains in plain language, and every override is accepted, logged and priced in KPI terms. A copilot with an audit trail is how planning tools actually get adopted." | "The AI is better than humans." |
| 7 | "How do you integrate with Maximo?" | Integration realism | "Two paths: Maximo's REST API where available, and a scheduled CSV export otherwise — which is how most Indian metro deployments actually run. Ingestion normalises both into one canonical state with per-source freshness monitoring." | "We'll just call their API." |
| 8 | "Security — this touches safety-critical operations." | Government seriousness | "Four RBAC roles enforced server-side, short-lived JWTs, TLS everywhere, an append-only audit log, and read-only integration with Maximo in v1 — which removes the largest risk class entirely. The LLM receives no PII and no decision authority." | "We have login." |
| 9 | "What does it cost to run?" | Feasibility | "The prototype is effectively free — everything is open-source and self-hosted; the only paid element is a few hundred rupees of LLM calls for explanation text, and that's optional. Production is one modest VM plus Postgres; the solver is CPU-bound and runs once a night." | "Cloud is cheap." |
| 10 | "How does it scale to 40 trainsets and two depots?" | Scalability | "That's the combinatorially harder question, so we tested it live in the demo. The model is parameterised by fleet and yard topology; two depots are two subproblems sharing a fleet-mileage objective. Forty trainsets solves in about seven seconds." | "It's microservices, so it scales." |
| 11 | "Mileage balancing conflicts with branding. Who decides?" | Domain understanding | "KMRL does — through configurable objective weights exposed as a slider with live KPI impact. We don't bury the trade-off in a magic constant; we surface its price." | "The AI balances them." |
| 12 | "What if the LLM hallucinates an explanation?" | LLM risk awareness | "It can't affect a decision — it renders a structured reason object the solver produced, and we show that raw object alongside the prose. If the API is unavailable we fall back to templated text. The system is fully functional with the LLM switched off." | "We use a good model." |
| 13 | "Has anyone from KMRL validated this?" | Honesty | "No, and we'd rather say so. We validated against the statement's own constraint definitions and published KMRL fleet and timetable data — and we built a yard-topology editor precisely so their real layout can be corrected in the UI rather than in code." | Inventing a validation. |
| 14 | "Why not reinforcement learning?" | Technical judgement | "RL needs a simulator and millions of episodes to approximate what CP-SAT proves exactly, and it can neither explain itself nor guarantee constraint satisfaction. For a safety-regulated nightly decision that's a strictly worse trade." | "RL is too complex for us." |
| 15 | "What breaks first in production?" | Maturity | "Data freshness. A stale fitness-certificate feed means optimising on a lie — so we monitor freshness per source, hard-block generation on stale safety data, and require explicit supervisor acknowledgement to proceed." | "Nothing, it's robust." |

## 13. Failure Modes & Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Solver slow / no solution on stage | Medium | Fatal | Time cap + anytime incumbent; pre-warmed scenarios; rehearse offline |
| Over-constrained model → infeasible | High during build | High | Soft constraints with penalties by default; hard only for legal/safety; infeasibility cores |
| Yard/shunt model diverges from reality | Medium | Medium | Configurable topology editor; state the assumption openly |
| Synthetic data looks unrealistic | Medium | Medium | Derive distributions from published metro maintenance practice; show the generator's parameters openly |
| LLM API down mid-demo | Medium | Low | Cached explanations + templated fallback; demo runs fully offline |
| Weights produce nonsense plans | Medium | Medium | Sane defaults, bounded weight ranges, regression tests over the scenario library |
| Team can't learn CP-SAT in time | Medium | Fatal | Start the solver on day 1, not day 5; assign two people |
| Judges dismiss it as "not AI" | Medium | High | Pre-empt in the pitch (demo stage 4); memorise Q1's answer |
| Scope creep into rostering/IoT | High | High | Freeze scope after MUST + 7/8/9; everything else goes on a roadmap slide |

## 14. Development Difficulty

| Dimension | Rating |
|---|---|
| Frontend | 7/10 — the yard map is real work |
| Backend | 6/10 |
| AI / Optimisation | **8/10** — CP-SAT modelling is the hard skill |
| Data | 3/10 — synthetic |
| Integration | 4/10 — mocked connectors |
| Deployment | 3/10 |
| Testing | 6/10 — you need an independent constraint checker |
| **Overall** | **7/10** |

**Overall Development Risk: MEDIUM–HIGH** — concentrated almost entirely in one place (the solver model). That is *good* risk: you will know by day 2 whether you have it, not day 6.

## 15. Team Requirements (6 people)

| Role | People | Responsibility |
|---|---|---|
| **Optimisation lead** | 1–2 | CP-SAT model, objectives, infeasibility cores. **Starts day 1.** |
| Backend | 1 | FastAPI, Postgres schema, Celery, ingestion connectors, rule engine |
| Frontend | 2 | One on the yard map + plan console (the hardest UI), one on dashboard + simulator |
| Data & domain | 1 | Scenario generator, KMRL research, KPI definitions, judge prep, demo script |
| DevOps/QA | shared | Docker Compose, deployment, independent constraint verifier |

**If you are four:** fold DevOps into backend and let the domain person take frontend #2. Never fold away the second optimisation person — pair-program the model instead.

## 16. Time Estimation

| Milestone | Realistic effort |
|---|---|
| 24-hour prototype | Domain model + generator + CP-SAT with FC/job-card/mileage constraints + plain ranked list. Achievable; no yard map |
| 3-day prototype | Above + branding and cleaning constraints + explanations + basic yard map + alerts |
| 1-week MVP | Above + shunt cost in the objective + what-if override with KPI delta + emergency re-plan + dashboard |
| 2-week polished MVP | Above + infeasibility cores + weight sliders + 30-night simulation + 40-train scale demo + risk model + deployment |
| Production-ready | 4–6 months with KMRL: real integrations, validation against historical nights, security audit, staff training, change management |

## 17. Cost

| Item | Prototype cost |
|---|---|
| OR-Tools, FastAPI, React, PostgreSQL, Redis, Docker | ₹0 |
| LLM API (explanations, a few thousand calls) | ₹200–800, and optional |
| Hosting | ₹0 — free-tier VM, or a laptop for the demo |
| Maps/GIS | ₹0 — the yard is custom SVG, not a map service |
| OCR | Not needed |
| **Total** | **≈ ₹0–800** |

Keep it free: run everything in Docker Compose locally for the demo, cache LLM explanations, and use free-tier hosting only for a public backup link.

## 18. Security & Privacy

**Sensitive data:** maintenance records (commercially sensitive), branding contract values (confidential), staff rosters (personal data), operational safety state (safety-critical).

- **AuthN:** short-lived JWT + refresh; SSO against KMRL's directory in production.
- **AuthZ:** RBAC — Supervisor (generate/approve), Engineer (constraints), Commercial (branding only), OCC (read + emergency re-plan), Admin. Enforced server-side per endpoint, never in the UI alone.
- **Encryption:** TLS 1.3 in transit; disk encryption at rest with column-level encryption for contract values.
- **Data minimisation:** store crew availability as counts, not named individuals, in v1.
- **Audit logging:** append-only and tamper-evident (hash-chained), covering every plan, override and constraint change.
- **API security:** rate limiting, Pydantic validation, no raw SQL, locked CORS.
- **Prompt injection:** the LLM receives *only* structured JSON reason objects your own code produced — never raw external documents — and its output is rendered as text, never parsed back into decisions. That closes the injection surface almost entirely; say exactly this if asked.
- **Data leakage:** LLM calls carry trainset IDs and constraint codes, never contract values or personal names.
- **Integration safety:** read-only against Maximo in v1.

## 19. Real-World Deployment: prototype vs production

| Dimension | SIH prototype | Production at KMRL |
|---|---|---|
| Data | Synthetic generator | Live Maximo + three FC feeds + mileage telemetry, with reconciliation and freshness SLAs |
| Infrastructure | Docker Compose on one VM | On-prem or government cloud (operational data may not be allowed to leave), HA Postgres, backups, DR |
| Security | JWT + RBAC | SSO against KMRL AD, CERT-In-aligned audit, VAPT clearance, ISO 27001 alignment |
| Compliance | — | Metro Railways (O&M) Act obligations, CMRS-facing audit evidence, safety-case sign-off |
| Validation | Constraint checker on synthetic scenarios | Shadow mode for 60–90 nights: the system proposes, humans decide, deltas measured before any reliance |
| Scale | 25–40 trainsets | 40+ across two depots, extensible to Water Metro |
| Monitoring | Logs | Prometheus/Grafana, alerts on stale feeds, solve-time SLO |
| Training | — | Supervisor training, printed fallback procedure, defined manual-override path |
| Maintenance | — | Constraints as versioned configuration; a named owner for objective weights |

**The honest line for judges:** "Shadow-mode operation is the deployment path. No metro should hand nightly induction to software on day one — but a system that proposes and explains while humans decide earns trust within a quarter."

## 20. Score Calculation

| Criterion | Weight | Score | Reason |
|---|---|---|---|
| Problem Impact | 20 | **16** | Real, funded, safety- and revenue-relevant; KMRL-specific but generalises to every Indian metro |
| Innovation Potential | 15 | **14** | Yard geometry + multi-objective + infeasibility cores is genuinely rare at SIH |
| Technical Feasibility | 15 | **12** | Achievable, but CP-SAT modelling is a real skill hurdle |
| Low Dataset Dependency | 10 | **9** | Synthetic data is methodologically defensible here |
| Low Model Training | 10 | **10** | Zero training required |
| SIH Demo Potential | 10 | **9** | Yard map plus live re-solve is outstanding |
| Scalability | 5 | **5** | Demonstrated on stage at 40 trainsets |
| Real-world Deployment | 10 | **9** | Active sponsor with a stated need |
| Team Skill Accessibility | 5 | **3** | Requires at least one person who enjoys optimisation |
| **TOTAL** | **100** | **87** | |

## 21. Brutal Assessment

- **Genuinely difficult:** the CP-SAT model — encoding stabling geometry and shunt counting without exploding the search space, and tuning multi-objective weights so plans stay sane.
- **Deceptively easy:** the ranked list. You will have a plausible-looking table by hour 10 and mistake it for the project. It isn't. The table is the commodity; the yard, the trade-offs and the infeasibility handling are the project.
- **What could kill it:** treating the solver as a week-2 task. If CP-SAT isn't running by end of day 2, pivot. Second killer: scope creep into crew rostering or IoT.
- **What could impress judges:** the override that prices its own consequences, the infeasibility core, the live 40-trainset scale-up.
- **What could make judges reject it:** failing to answer "where is the AI?" in one confident sentence, or a yard model that is obviously cosmetic.
- **Worth choosing?** Yes — and its low pick rate relative to PS 64/70/33 is a strategic bonus.
- **Would I personally choose it?** **YES.**

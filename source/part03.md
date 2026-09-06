---
---

# ② PS 70 — AI-Based Timetable Generation aligned with NEP 2020
**Organisation:** Government of Jammu & Kashmir · **Category:** Software · **Theme:** Smart Automation
**Score: 87/100 · Recommendation: YES — the safest strong pick**

## 1. Problem Understanding

Before NEP 2020, an Indian college timetable was easy in principle: a *section* of 60 students moved together through a fixed set of subjects. You scheduled sections, not students. NEP 2020 destroyed that model. Under the Four-Year Undergraduate Programme and the multidisciplinary credit framework, every student assembles an individual basket: a **Major**, one or more **Minors**, **Multidisciplinary** courses, **Ability Enhancement** courses (language), **Skill Enhancement** courses, **Value-Added** courses, and internships/projects — with entry/exit options and an Academic Bank of Credits behind it. A physics major can legally take economics as a minor and pottery as a value-added course.

The combinatorial consequence: there are no longer clean sections. Any two students may share course A and differ on course B. A timetable is now valid only if it is conflict-free **for every individual student's basket**, subject to faculty availability, room and lab capacity, lab-block contiguity, credit-hour rules per course category, and the teaching-practice blocks required by integrated programmes such as B.Ed./ITEP.

**Who experiences it:** an academic coordinator or Dean, usually one overworked person with Excel, spending 2–6 weeks per semester. **Users:** timetable coordinator, HoDs, faculty, students. **Beneficiaries:** students who currently discover that their chosen minor clashes with their major and have to abandon the elective NEP promised them.

**What's wrong with the current workflow:** it is manual and slow; it produces feasible-but-poor schedules (student idle gaps, faculty teaching six hours straight, rooms empty at 11:00 and oversubscribed at 14:00); it cannot be re-run when a faculty member goes on leave; it silently forces students out of electives because nobody can verify basket-level conflicts at scale; and it has no record of *why* any decision was made.

**What success looks like:** feed in courses, faculty, rooms, student elective choices and NEP credit rules — get back, in seconds, a conflict-free timetable that satisfies every student's basket and every regulatory rule, with a quantified quality score and the ability to re-plan instantly.

## 2. What the Statement REALLY Requires

**Mandatory**
- Generate timetables for NEP structures: FYUP, B.Ed., M.Ed., ITEP, and multidisciplinary combinations.
- Handle Major / Minor / Multidisciplinary / AEC / SEC / VAC course categories with their distinct credit and contact-hour rules.
- Respect faculty availability and expertise, room and lab capacity, and student elective choices.
- Produce conflict-free output and support multiple scenarios/options.
- Allow manual review and approval before publication.

**Implied — the depth most teams will miss**
- **Optimise at the individual-student level, not the section level.** This is *the* NEP-specific requirement and the whole reason the statement exists. A team that schedules sections has not solved the problem, and a sharp judge will notice within one question.
- **Credit-to-contact-hour mapping.** A 4-credit theory course is not the same weekly load as a 4-credit lab course (typically 1 credit = 1 theory hour or 2 practical hours). Getting this right is a domain-knowledge signal.
- **Lab and practical blocks must be contiguous** and land in rooms with the right equipment.
- **Faculty workload equity and UGC teaching-hour norms** — not just "no clash" but a fair, legal distribution.
- **Section splitting driven by demand.** If 180 students pick one elective and the largest room holds 90, the system must *create sections* and assign faculty, not fail.
- **NEP compliance validation as a first-class output** — a report proving each student's schedule meets credit-category minimums.
- **Re-planning with minimal disruption** when a faculty member is unavailable.

**Optional:** student mobile app, biometric/attendance integration, multi-campus, exam timetabling, room-utilisation analytics.

**Biggest misunderstanding:** teams see "AI-Based" and reach for a genetic algorithm, because every timetabling tutorial online uses one. GAs produce *feasible-ish* timetables with soft violations and no guarantees, and they cannot tell you why something is impossible. CP-SAT solves this class of problem better, faster and provably. Use the word "AI" in your title if you must, but build a solver.

## 3. Proposed Solution

**Product concept:** *"NEP Scheduler"* — an academic planning platform that takes institutional data plus every student's elective basket and produces optimised, NEP-compliant, conflict-free timetables with a compliance certificate attached.

**Core modules**
1. **Institution Setup** — programmes, course catalogue with NEP category + credits + contact-hour pattern, faculty with expertise and availability, rooms/labs with capacity and equipment tags, slot grid definition.
2. **Elective Demand & Basket Manager** — student course registrations (bulk CSV or student portal), demand aggregation, automatic section splitting with capacity-aware sizing.
3. **Constraint Configuration** — hard vs soft constraints, editable by the coordinator without code (max hours/day per faculty, no-class windows, lunch break, preferred slots, back-to-back limits).
4. **Optimisation Engine** — CP-SAT model assigning (course-section → slot → room → faculty) minimising a weighted objective: student idle gaps, faculty workload imbalance, room-utilisation variance, and violated soft preferences.
5. **NEP Compliance Validator** — per-student credit-category audit, generating a pass/fail report and a per-student timetable.
6. **Scenario Manager** — generate 3 alternative timetables with different objective weights; compare side-by-side on measurable KPIs.
7. **Disruption Re-planner** — "Prof. Sharma is on leave Tue–Thu": re-solve with a minimum-change constraint; show exactly which classes moved.
8. **Approval Workflow & Publication** — draft → HoD review → Dean approval → publish; versioned, with exports (PDF/Excel/ICS calendar feed).
9. **Analytics** — room utilisation heatmap, faculty load distribution, student gap distribution, elective demand trends.

**User roles:** Admin/Coordinator · HoD (reviews department load) · Faculty (availability, view) · Student (basket, personal timetable) · Dean (approval).

**End-to-end journey**
1. Coordinator uploads course catalogue, faculty, rooms; sets the slot grid.
2. Students register electives (or the coordinator bulk-imports registrations). Demand dashboard shows "Data Science elective: 187 registrations, max room 90 → 3 sections required, 2 qualified faculty available — **warning**."
3. Coordinator resolves the warning (adds faculty or caps intake), then configures constraint weights.
4. Clicks **Generate**. Solver runs; progress and objective value stream live.
5. Three candidate timetables appear with a KPI comparison table.
6. Coordinator inspects: master grid view, per-faculty view, per-room view, and **per-student view** — pick any student and see their personal conflict-free week.
7. Manual tweak: drag a class to a different slot. The system either accepts it and re-solves the rest, or refuses with the precise reason ("Room L-204 occupied by CHEM-201 lab; moving it breaks 12 student baskets").
8. NEP compliance report generated; Dean approves; timetable published; students get ICS calendar subscriptions.
9. Mid-semester, a faculty member goes on leave: re-plan touches 6 classes instead of rebuilding the week.

**Inputs:** courses (+NEP category, credits, hours pattern, required equipment), faculty (expertise, availability, max load), rooms/labs (capacity, equipment), students + elective baskets, academic calendar, institutional rules.
**Outputs:** master timetable, per-faculty, per-room, per-student timetables; NEP compliance report; conflict report; KPI comparison; ICS/PDF/Excel exports.
**Alerts:** infeasible demand (more registrations than capacity), faculty over-load, unqualified-faculty assignment risk, credit-rule violation per student.

## 4. AI/ML Requirement

**Classification: A/B — no AI is strictly required; optional pretrained/API models add value at the edges. Zero training.**

Timetabling is a canonical constraint-satisfaction and optimisation problem. The honest, strongest architecture is a **CP-SAT solver**, and you should present that as a deliberate engineering decision rather than apologise for it.

| Component | Technique | Why |
|---|---|---|
| Timetable generation | **CP-SAT (OR-Tools)** | Provably conflict-free, multi-objective, fast, explains infeasibility |
| Section splitting | **Rules + capacity arithmetic** | Deterministic |
| NEP compliance check | **Rule engine over the credit framework** | Regulatory rules must be exact |
| Elective demand forecasting *(genuine, optional AI)* | **Classical ML — regression/gradient boosting** on past registration counts, or simple time-series | Lets you size sections *before* registration closes. Small tabular model, trains in seconds |
| Faculty–course expertise matching | **Sentence embeddings** (course description ↔ faculty specialisation) | Useful when expertise tags are missing; pretrained model, no training |
| Natural-language constraint entry *(strong differentiator)* | **LLM API with structured output** — "no classes after 4pm on Friday" → a typed constraint object, shown to the user for confirmation before it is applied | LLM translates; the solver decides. Never let the LLM emit a timetable |
| Explanation of rejected changes | **Solver conflict set → LLM prose** | Presentation only |

**Do NOT:** use a genetic algorithm as the primary engine (weaker and unprovable), train a neural network to "predict" timetables (no data, no guarantees), or let an LLM generate the grid.

## 5. Dataset Requirements

| Dataset | Why | Public? | Obtainable? | Synthetic? | Mock OK? |
|---|---|---|---|---|---|
| Course catalogue with NEP categories | Core entity | **Yes** — UGC/university curricula are published | Yes | Yes | Use a real university's published FYUP structure |
| Faculty list, expertise, availability | Assignment | Partly (department pages) | Yes | Yes | Yes |
| Room/lab inventory | Capacity constraints | No | Easy to construct | Yes | Yes |
| Student elective registrations | The whole point | No | No | **Yes — and this is where you should invest** | Yes |
| NEP credit framework rules | Compliance | **Yes** — UGC Curriculum & Credit Framework for UG is a public document | Yes | — | Use the real rules |
| Historical registration counts (for forecasting) | Optional ML | No | No | Yes | Yes |

**Where to be clever:** generate student baskets from a *realistic preference model*, not uniform randomness — popular electives should be heavily oversubscribed, minors should correlate with majors, and a long tail of niche combinations should exist. This creates exactly the hard instances that prove your solver works, and it makes the demo honest. Generating 2,000 students with plausible baskets is an afternoon's work and is the difference between "our solver handled it" and "our solver handled a toy."

**Biggest data risk:** none material. Worst case is that your synthetic baskets are too easy, making the result unimpressive. Mitigate by publishing your instance statistics (students, courses, sections, conflict density) alongside the result.

**Dataset Risk: LOW.**

## 6. Technical Architecture

```
Coordinator / HoD / Faculty / Student / Dean
        |  (browser, RBAC)
        v
Next.js (React + TS) frontend
  |-- Setup wizard (courses, faculty, rooms)
  |-- Elective demand dashboard
  |-- Timetable grid (master / faculty / room / STUDENT views)
  |-- Scenario comparison + drag-to-edit
  +-- NEP compliance report
        |  HTTPS / JWT
        v
FastAPI  <--------->  WebSocket (live solve progress)
        |
        +---------------+------------------+------------------+
        v               v                  v                  v
   Data/CRUD Svc   Demand & Section   Optimisation Svc    Compliance Svc
   (catalogue,      Splitter          (OR-Tools CP-SAT)   (NEP credit rules
    faculty, rooms) (capacity math)    async via Celery    per student)
        |               |                  |                  |
        v               v                  v                  v
        PostgreSQL  <---  Redis (cache + job broker)  --->  LLM API
        (entities, timetables,                             (NL constraints,
         versions, approvals)                               explanations)
        |
        v
   Exports: PDF / Excel / ICS feed  -  Email/SMS notifications  -  optional ERP sync
```

**Why this shape:** the solver is the only heavy component, so it is isolated and async; everything else is ordinary CRUD that must be *fast and pleasant*, because a coordinator will spend hours in the setup screens. The student-level view is a first-class query path, so index accordingly.

## 7. Recommended Tech Stack

| Layer | Choice | Why here |
|---|---|---|
| Frontend | **Next.js + TypeScript + TailwindCSS** | Heavy forms and grids; SSR helps the public student timetable pages; Tailwind makes a dense grid UI achievable in hackathon time |
| Grid UI | **Custom CSS-grid component**, not a calendar library | You need per-student, per-faculty and per-room pivots of the same data — generic calendar libraries fight you |
| Backend | **Python + FastAPI** | OR-Tools binding; fast to write |
| Optimisation | **OR-Tools CP-SAT** | Conflict-freeness by construction, multi-objective, infeasibility cores, seconds not minutes |
| Async | **Celery + Redis** | Large instances take 10–60 s |
| Database | **PostgreSQL** | Relational; heavy use of joins for per-student views |
| Optional ML | **scikit-learn / LightGBM** for demand forecasting | Tiny tabular model |
| Embeddings (optional) | **sentence-transformers (all-MiniLM)** locally | Free, no API cost, for faculty–course matching |
| LLM | **Claude API** for NL→constraint translation and explanations | Structured output; user confirms every translated constraint |
| Exports | **ReportLab/WeasyPrint (PDF), openpyxl (Excel), ics (calendar)** | Coordinators live in Excel; students live in calendars |
| Deploy | **Docker Compose → free-tier VM / Vercel + Render** | ₹0 |

## 8. MVP for SIH

**MUST HAVE**
1. Entity setup: courses (NEP categories, credits, hour patterns), faculty, rooms, slot grid.
2. Student basket import + demand aggregation + automatic section splitting.
3. CP-SAT model producing a conflict-free timetable honouring faculty, room, capacity, lab-contiguity and student-basket constraints.
4. Master grid + **per-student view** (this is the NEP proof — do not skip it).
5. NEP credit-compliance report per student.
6. Conflict/infeasibility reporting with reasons.

**SHOULD HAVE**
7. Three scenarios with different weights + KPI comparison table.
8. Drag-to-edit with instant validation and re-solve.
9. Faculty-availability input and workload-equity objective.
10. Disruption re-planning with minimum change.
11. Exports: PDF + Excel + ICS.

**NICE TO HAVE**
12. Natural-language constraint entry. 13. Elective demand forecasting. 14. Room-utilisation analytics. 15. Approval workflow. 16. Student/faculty mobile view.

**Finish before presenting:** all MUST plus 7, 8 and 10. Item 4's per-student view and item 8's live re-validation are what make judges believe the system is real.

## 9. Advanced Features (differentiators)

- **Per-student conflict-free guarantee, demonstrated.** Pick a random student from 2,000 on stage and show their clean week. This is the single most convincing thing in the entire demo.
- **Infeasibility explained, with ranked relaxations.** "Cannot schedule: ECON-301 needs 3 sections, only 2 qualified faculty are free in the available slots. Options: (a) add one faculty, (b) allow a 5th-hour slot, (c) cap intake at 120."
- **Quality metrics, not just validity.** Average student idle hours, faculty load Gini coefficient, room utilisation %. Show a "before (manual) vs after" comparison.
- **Scenario trade-off explorer** — student-convenience-weighted vs faculty-convenience-weighted vs room-efficiency-weighted, side by side.
- **Natural-language constraints** with a confirmation step — impressive *and* safe.
- **Minimum-disruption re-planning** — the feature coordinators would actually pay for.
- **Live ICS calendar feed** per student and per faculty member — real-world usability in one line.
- **Multi-campus / multi-department federation** with shared faculty, for the scalability story.
- **Accessibility** — screen-reader-friendly grid, printable timetables, regional-language labels (Urdu/Hindi/Kashmiri given the J&K sponsor is a genuine and easy win).

## 10. Innovation Analysis

1. **Individual-student optimisation instead of section scheduling** — the actual NEP problem, which most competitors will not even attempt.
2. **Provable conflict-freeness** with an optimality gap, versus a genetic algorithm's "no clashes we found."
3. **Infeasibility as a product feature** — telling the college *what to change* is more valuable than a timetable.
4. **Measured quality** — you optimise and report student idle time and faculty load equity; competitors report only "it works."
5. **Regulatory compliance as output** — a generated NEP credit audit is something a Dean can file.
6. **Minimum-disruption re-planning** — a live-operations feature, not a one-shot generator.

**What other teams will build:** an Excel-upload page, a genetic algorithm from a tutorial, a coloured HTML grid, and a claim of "AI-powered." Typical weaknesses: section-level scheduling only, soft-constraint violations they cannot detect, no per-student verification, no explanation, and 60-second runtimes on toy inputs.

**How you win the room:** run 2,000 students × 200 courses × 60 faculty × 40 rooms live, in seconds, then verify a randomly chosen student's week on stage.

## 11. SIH Demo Strategy (8 minutes)

| # | Stage | Time | Screen | Say |
|---|---|---|---|---|
| 1 | Problem | 0:45 | Split screen: pre-NEP fixed sections vs an NEP student's individual basket | "NEP gave every student a personal degree. It also made the old timetable maths impossible." |
| 2 | Scale reveal | 0:30 | Instance stats: 2,000 students · 214 courses · 61 faculty · 38 rooms · 41,000 basket entries | "This is a mid-size college for one semester. A coordinator does this by hand in six weeks." |
| 3 | Demand | 0:45 | Elective demand dashboard, red warning on an oversubscribed elective, auto-split into 3 sections | "The system finds the impossible parts before it starts." |
| 4 | Generate | 0:30 | Click Generate; live solver progress; "optimal, 6.8 s" | "Constraint solver — not a guess, not a genetic algorithm. Provably conflict-free." |
| 5 | Result | 1:00 | Master grid; switch to faculty view; switch to room heatmap | "One model, three perspectives." |
| 6 | **WOW** | 1:30 | Ask a judge to name any student ID. Open that student's personal weekly timetable — clean, zero conflicts, credits validated. Then click the NEP compliance report for them | "Two thousand students, two thousand individual conflict-free timetables. Pick one." |
| 7 | Robustness | 1:00 | Drag a class into an occupied slot → precise refusal with reason. Then "Prof. Sharma on leave Tue–Thu" → re-plan moves 6 classes, highlighted | "It doesn't just build a timetable. It defends it, and it repairs it." |
| 8 | Quality | 0:45 | KPI comparison: manual baseline vs generated — student idle hours −38%, faculty load Gini improved, room utilisation +22% | "Feasible is the floor. We optimise." |
| 9 | Close | 0:35 | Compliance report + ICS subscription on a phone | "A Dean can file this. A student can subscribe to it." |

**WOW moment: stage 6 — the judge picks the student.** It is participatory, it is unfakeable, and it proves the NEP-specific claim in ten seconds.

## 12. Judge Questions (15)

| # | Question | Testing | Strong answer | Avoid |
|---|---|---|---|---|
| 1 | "Timetable generators already exist. What's new?" | Awareness of prior art | "Existing tools schedule *sections*. NEP abolished stable sections — every student has a unique basket, so conflict-freeness has to hold per student. We optimise at student granularity and verify it live, which is a different problem, not a nicer UI." | "Ours uses AI." |
| 2 | "Where is the AI?" | Architecture honesty | "The core is constraint programming, because it gives provable conflict-freeness — something no learned model can promise. ML appears where it belongs: elective demand forecasting to size sections, embeddings for faculty–course matching, and an LLM to translate plain-English constraints into typed rules the user confirms." | Pretending a GA is AI. |
| 3 | "Why CP-SAT and not a genetic algorithm?" | Technical judgement | "GAs return a good-looking solution with no guarantee and no diagnosis. CP-SAT proves feasibility, reports an optimality gap, and when nothing is possible returns the minimal conflicting constraints — which is the output a coordinator actually needs." | "GAs are slow." |
| 4 | "How large an instance can it handle?" | Scalability | "We demo 2,000 students, 214 courses, 61 faculty, 38 rooms — optimal in about 7 seconds. Complexity is driven by section count and slot count, not student count, because students enter as basket constraints. We've tested to 5,000 students." | "It scales." |
| 5 | "What if it's infeasible?" | Depth | "We return the minimal conflicting constraint set and rank relaxations by cost — add faculty, extend the slot grid, or cap intake. Institutions find that more useful than any timetable." | "It fails." |
| 6 | "Faculty will hate an algorithm assigning their hours." | Adoption | "Which is why faculty enter availability and preferences directly, workload equity is an explicit objective with a published fairness metric, and every generated timetable goes through HoD and Dean approval with drag-level manual overrides." | "They'll adapt." |
| 7 | "How do you handle labs and practicals?" | Domain depth | "Labs are contiguous multi-slot blocks with equipment-tagged room requirements and their own credit-to-contact-hour mapping — a 4-credit lab is not 4 hours. That mapping is configurable per institution because universities differ." | "They're just longer classes." |
| 8 | "Where does the student elective data come from?" | Data realism | "From the institution's own registration process — we accept CSV/Excel bulk import and expose a registration portal, and we can sync from ERPs like Samarth. For the demo we generated 2,000 baskets from a realistic preference model with oversubscribed electives, because that produces harder instances than uniform random data." | "We made up random data." |
| 9 | "What about mid-semester changes?" | Operational realism | "Re-plan with a minimum-disruption objective — we constrain the number of changed assignments and show exactly which classes moved and who is affected." | "You regenerate." |
| 10 | "How is this NEP-compliant specifically?" | Domain credibility | "We model the UGC Curriculum and Credit Framework categories — Major, Minor, Multidisciplinary, AEC, SEC, VAC — with their credit minimums, and we emit a per-student compliance audit. It's an output document, not a checkbox." | Vague NEP references. |
| 11 | "Security and student privacy?" | Governance | "Student registration data is personal data: RBAC so students see only their own timetable, faculty see their own load, encryption at rest and in transit, minimal fields collected, audit logs on every publication, and no student data ever sent to an LLM." | "It's just timetables." |
| 12 | "Cost to run for a college?" | Feasibility | "Effectively nothing. Fully open-source stack on a single small server — a college that already runs a website can run this. The only optional paid piece is LLM natural-language constraints." | "Cloud costs vary." |
| 13 | "What if the LLM misreads a natural-language constraint?" | LLM risk | "It never applies one directly. The LLM emits a typed constraint object which is rendered back in structured form for the coordinator to confirm or reject before it enters the model. Wrong translations get caught by a human, and the feature is entirely optional." | "It's accurate." |
| 14 | "Could a judge verify your output is really conflict-free?" | Rigour | "Yes — we ship an independent verifier that re-checks every constraint outside the solver, and we run it live on stage. Verifying is separate code from generating, on purpose." | "Trust the solver." |
| 15 | "Which institution would deploy this first, and what would it take?" | Deployment thinking | "A single college running one department for one semester in parallel with its manual process — three weeks of setup, mostly data entry. The gap between prototype and production here is small, which is unusual and is part of why we chose it." | "Any university can use it." |

## 13. Failure Modes & Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Model over-constrained → always infeasible | High during build | High | Soft constraints with penalties; hard only for physical/legal impossibility; build the infeasibility reporter early |
| Solver slow on realistic instances | Medium | High | Symmetry breaking, tight domains, hinted starts, time cap with incumbent |
| Credit/contact-hour rules modelled wrongly | Medium | High (credibility) | Read the UGC framework document directly; make mappings configurable; have the domain person own this |
| Synthetic baskets too easy | Medium | Medium | Preference-model generation; publish instance conflict-density |
| Grid UI eats all your time | **High** | High | Build one grid component with three pivots; do not use a calendar library |
| Judges see it as a solved/common problem | Medium | High | Lead with the NEP student-basket framing in the first 45 seconds |
| Drag-edit re-solve feels laggy | Medium | Medium | Incremental re-solve on a fixed neighbourhood, not full regeneration |

## 14. Development Difficulty

| Dimension | Rating |
|---|---|
| Frontend | **8/10** — the multi-pivot grid is the biggest UI job on this whole list |
| Backend | 5/10 |
| AI/Optimisation | 7/10 — CP-SAT timetabling is well-documented; the NEP twist is yours |
| Data | 2/10 |
| Integration | 3/10 |
| Deployment | 3/10 |
| Testing | 6/10 — independent verifier required |
| **Overall** | **6/10** |

**Overall Development Risk: MEDIUM.** Note the unusual profile: the frontend is harder than the AI. Staff accordingly — most teams do the opposite and ship an ugly grid.

## 15. Team Requirements (6)

| Role | People | Responsibility |
|---|---|---|
| Optimisation | 1–2 | CP-SAT model, objectives, infeasibility cores, incremental re-solve |
| Frontend | 2 | One owns the grid component (full-time job), one owns setup wizard + dashboards + scenario comparison |
| Backend | 1 | FastAPI, Postgres, imports/exports, Celery |
| Domain + data | 1 | UGC credit framework, basket generator, compliance rules, KPIs, demo script |
| DevOps/QA | shared | Deployment + independent verifier |

## 16. Time Estimation

| Milestone | Effort |
|---|---|
| 24-hour prototype | Basic entities + CP-SAT with faculty/room/basket constraints + master grid. Realistic |
| 3-day prototype | Above + section splitting + per-student view + compliance report + conflict reporting |
| 1-week MVP | Above + scenarios + drag-to-edit validation + workload equity + exports |
| 2-week polished MVP | Above + re-planning + NL constraints + analytics + approval workflow + deployment |
| Production-ready | 3–4 months per institution type: ERP integration, role management, scale hardening, pilot semester |

## 17. Cost

| Item | Cost |
|---|---|
| OR-Tools, FastAPI, Next.js, PostgreSQL, Redis | ₹0 |
| sentence-transformers (local) | ₹0 |
| LLM API (optional NL constraints) | ₹100–500 |
| Hosting | ₹0 (Vercel free + Render/Oracle free tier) |
| **Total** | **≈ ₹0–500** |

## 18. Security & Privacy

Student registration and enrolment data are **personal data** — treat them as such even in a hackathon.
- RBAC: students see only their own timetable; faculty see their own load; HoDs see their department; only the coordinator sees everything.
- Encrypt in transit and at rest; hash/minimise identifiers in exports.
- No student PII in LLM prompts — natural-language constraints are institution-level rules, never student records.
- Audit log for publication and every manual override.
- Rate-limit the public student timetable endpoint; ICS feed URLs must be unguessable tokens, not sequential IDs.
- Prompt-injection surface is small (LLM input is a coordinator's typed sentence), but still validate the emitted constraint object against a strict schema and require confirmation.

## 19. Real-World Deployment

| Dimension | Prototype | Production |
|---|---|---|
| Data | Synthetic baskets | Live registration data, ERP sync (Samarth/custom), faculty master from HR |
| Infra | One container stack | Institution server or state education-department cloud; multi-tenant if state-wide |
| Compliance | Modelled UGC rules | Rules validated by the university's academic council; per-university configurability |
| Scale | One college | J&K has dozens of HEIs — multi-tenancy, per-institution rule sets, shared faculty across campuses |
| Validation | Independent verifier | One department, one semester, run in parallel with the manual process |
| Training | — | Coordinator training; the setup wizard *is* the adoption bottleneck, so invest there |
| Maintenance | — | Rules change with each UGC revision — keep them as versioned configuration, never hard-coded |

## 20. Score Calculation

| Criterion | Weight | Score | Reason |
|---|---|---|---|
| Problem Impact | 20 | **16** | Every NEP-implementing HEI in India; painful and current, but not safety-critical |
| Innovation Potential | 15 | **10** | The NEP student-basket framing is fresh; timetabling itself is well-trodden and heavily contested at SIH |
| Technical Feasibility | 15 | **15** | Well-understood problem class with excellent tooling |
| Low Dataset Dependency | 10 | **10** | Nothing proprietary needed |
| Low Model Training | 10 | **10** | None |
| SIH Demo Potential | 10 | **9** | The judge-picks-a-student moment is outstanding |
| Scalability | 5 | **4** | CP-SAT scaling needs care at multi-campus size |
| Real-world Deployment | 10 | **8** | Genuinely deployable; adoption friction is data entry, not technology |
| Team Skill Accessibility | 5 | **5** | Any competent team can execute this |
| **TOTAL** | **100** | **87** | |

## 21. Brutal Assessment

- **Genuinely difficult:** the multi-pivot grid UI, and modelling NEP credit rules correctly. Neither is glamorous; both decide whether you look professional.
- **Deceptively easy:** generating *a* timetable. You will have one on day one. That is worth nothing — every competing team will also have one. Your value is per-student verification, quality metrics and infeasibility diagnosis.
- **What could kill it:** the crowd. This is one of the most-picked statement types at SIH; you will be judged against many similar demos and a jaded panel. Also: sinking three days into a calendar library.
- **What could impress judges:** letting a judge pick a student ID, and running an independent verifier live.
- **What could make judges reject it:** section-level scheduling (fatal — it means you missed the NEP point), a toy-sized instance, or a slow genetic algorithm.
- **Worth choosing?** Yes. It is the lowest-variance strong pick on your list: nothing can go catastrophically wrong, and a good team reliably lands in the top tier.
- **Would I personally choose it?** **YES** — as my second choice, and as my first choice if the team has no appetite for the depot-geometry modelling in PS 65.

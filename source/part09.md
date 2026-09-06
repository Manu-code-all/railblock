---
---

# PART 5 — FULL-FIELD SCREEN: ALL 105 SOFTWARE STATEMENTS

Parts 0–4 evaluated the eight statements you had already shortlisted. This part does the job you actually asked for: screen **every software statement in the sheet** for model-training intensity, then check whether anything outside your shortlist beats it.

**It does.** One statement you missed — **PS 22, Ministry of Railways** — scores within a point of the winner and has higher impact than anything on your list.

## The training-intensity ladder

Every one of the 105 software statements is placed in one of five classes.

| Class | Meaning | Verdict | Count |
|---|---|---|---|
| **A** | No AI/ML required — rules, optimisation, engineering, integration | **Target zone** | 37 |
| **B** | Pretrained models, APIs or RAG are sufficient | **Target zone** | 31 |
| **C** | A small classical model on obtainable tabular data | **Acceptable** | 13 |
| **D** | Significant custom model training required | Cut | 10 |
| **E** | Training *plus* unobtainable data, or hardware / specialist science | Cut | 14 |

**81 of 105 pass. 24 fail.** Your constraint is far less restrictive than it feels — the real filter is not "which statements avoid training" but "which of the 81 are worth winning with."

Two calibration notes. First, class is about *training burden*, not quality: PS 82 (student ERP) is Class A and still a bad choice, because no-AI-needed and worth-building are different questions. Second, several statements can be read at different ambition levels — PS 44 is Class B if you use pretrained detection and signal optimisation, Class D if you decide to train your own vehicle detector. **Where a statement is ambiguous, the class below assumes the sane reading.**

## The cut — 24 statements that fail your constraint

| PS | Class | Statement | Why it fails |
|---|---|---|---|
| **4** | D | Image based breed recognition for cattle and buffaloes of India | Fine-grained breed classification needs a large India-specific labelled cattle image corpus. |
| **5** | D | Image based Animal Type Classification for cattle and buffaloes | Same corpus problem as 4; coarser classes but still custom vision training. |
| **36** | D | AI-Driven Unified Data Platform for Oceanographic Fisheries and Molecular Biod… | eDNA / molecular biodiversity analysis is specialist bioinformatics, not app development. |
| **56** | E | AI-Based Rockfall Prediction and Alert System for Open-Pit Mines | Rockfall prediction needs geotechnical sensor histories and slope monitoring you cannot obtain. |
| **63** | E | Software other than a circuit breaker that can be used to detect and turn off … | Line-break detection is a signal-physics and hardware problem wearing a software label. |
| **76** | E | Research and develop a design on autonomous small precision focused machine fo… | Machine design. Not a software deliverable. |
| **77** | E | Students are tasked with designing a 4-story commercial office building using … | Revit/BIM coursework. Not software engineering. |
| **78** | E | AI-powered monitoring of crop health soil condition and pest risks using multi… | Hyperspectral crop analytics needs hyperspectral capture and heavy training. |
| **99** | E | Instruments in observational Astronomy | Scope undefined; instrument-building, not software. |
| **101** | D | AI-Driven Next-Generation Firewall for Dynamic Threat Detection and Zero Trust… | A learned firewall needs labelled network traffic at scale and cannot be demoed honestly. |
| **102** | D | Mitigating National Security Risks Posed by Large Language Models (LLMs) in AI… | Research brief, not a buildable deliverable in hackathon time. |
| **103** | E | Automated Optical Inspection (AOI) based IC marking to identify fake marking | IC die imaging is proprietary and hardware-bound. |
| **104** | E | Self-Healing Computing Elements | Systems research with no demonstrable hackathon artefact. |
| **110** | E | LunaBot: Autonomous Navigation of Robot for Lunar Habitats | Lunar SLAM and robotics. Simulation-heavy, far outside the constraint. |
| **111** | E | Enhancing OpenAI’s GPT-OSS with Multimodal Vision Capabilities extensible to I… | Explicitly asks you to extend a multimodal model. Training is the deliverable. |
| **112** | E | Optical-Guided Super-Resolution for Thermal IR Imagery | Super-resolution on thermal IR is deep-learning training from scratch. |
| **113** | D | Transformer based end-to-end Web Application Firewall (WAF) pipeline | End-to-end transformer WAF requires training on request corpora you cannot obtain. |
| **115** | D | Neural Net based Android Application for Real-Time Fish Catch Identification, … | Fine-grained fish species recognition needs a labelled catch corpus. |
| **117** | D | To develop AI/ML based models to predict time-varying patterns of the error bu… | GNSS clock/ephemeris error modelling is specialist time-series geodesy. |
| **118** | E | Use of measurements from the mobile phones (low cost preferred) to provide a s… | Sensor fusion for autonomous navigation from phone-grade hardware. |
| **119** | D | Short term forecast of gaseous air pollutants (ground-level O3 and NO2) using … | Air-quality forecasting from satellite and reanalysis is heavy geoscience ML. |
| **129** | E | AI-Based Dynamic Contact Resistance Measurement (DCRM) Analysis for EHV Circui… | DCRM waveform corpora are proprietary utility data. |
| **130** | E | AI-Driven Frequency Response Analysis for Transformer Diagnostics via Unified … | FRA traces are proprietary utility data. |
| **131** | D | Development of AI/ML enabled Digital Twin for EHV 400/220 kV Substation | A substation digital twin needs SCADA histories and deep power-systems knowledge. |


## The survivors — 81 statements that pass


### Class A — no AI/ML required at all

| PS | Statement | Note |
|---|---|---|
| **6** | Development of a Digital Farm Management Portal for Implementing Biosecurity… | Compliance workflow, rules and records. No ML anywhere in the core. |
| **7** | Development of a Digital Farm Management Portal for Monitoring Maximum Resid… | MRL/AMU thresholds are a rule engine over a livestock register. |
| **8** | Disaster Preparedness and Response Education System for Schools and Colleges | Content, drills and scoring. No ML. |
| **9** | Gamified Environmental Education Platform for Schools and Colleges | Gamification and content. No ML. |
| **11** | Smart Curriculum Activity &amp; Attendance App | CRUD plus scheduling. No ML. |
| **13** | Real-Time Public Transport Tracking for Small Cities | GTFS, GPS ingestion and ETA arithmetic. No ML needed. |
| **17** | Digital Platform for Centralized Alumni Data Management and Engagement | Directory, events, engagement. Pure CRUD. |
| **18** | Telemedicine Access for Rural Healthcare in Nabha | Scheduling, records and low-bandwidth video. No ML. |
| **19** | Digital Learning Platform for Rural School Students in Nabha | Content delivery and offline sync. No ML. |
| **22** | Maximizing Section Throughput Using AI-Powered Precise Train Traffic Control | Train precedence and crossing decisions are a pure constraint-programming problem. The statement itself names OR. |
| **23** | Ayur Sutra- Panchakarma Patient Management and therapy scheduling Software | Panchakarma therapy scheduling is resource-constrained scheduling: therapists, rooms, protocol order. |
| **24** | Comprehensive Cloud-Based Practice Management &amp; Nutrient Analysis Software f… | Nutrient arithmetic against a food-composition table plus practice CRUD. |
| **26** | Develop API code to integrate NAMASTE and or the International Classificatio… | Terminology interoperability and FHIR conformance. Barely any AI at all. |
| **27** | Develop a blockchain-based system for botanical traceability of Ayurvedic he… | Ledger, geotagging and custody events. No ML. |
| **28** | Smart Classroom &amp; Timetable Scheduler | Timetabling = CP-SAT. Weaker, less specific sibling of 70. |
| **32** | Development of a Smart Digital Platform to Promote Eco &amp; Cultural Tourism in… | Content platform and itineraries. No ML. |
| **39** | Blockchain-Based Supply Chain Transparency for Agricultural Produce | Ledger and custody events. No ML. |
| **42** | Gamified Learning Platform for Rural Education | Content and gamification. No ML. |
| **46** | AR-Based Cultural Heritage Preservation Platform | AR content and 3D assets. No ML. |
| **50** | Digitize and Showcase Monasteries of Sikkim for Tourism and Cultural Preserv… | Digitisation, 360 media, catalogue. No ML. |
| **60** | Gamified Platform to Promote Sustainable Farming Practices | Gamification and tracking. No ML. |
| **65** | AI-Driven Train Induction Planning &amp; Scheduling for Kochi Metro Rail Limited… | Six-variable nightly assignment under conflicting objectives. CP-SAT, no training. |
| **67** | Digital Health Record Management System for migrant workers in Kerala aligne… | Health records, portability and consent. Standards work, not ML. |
| **70** | AI-Based Timetable Generation System aligned with NEP 2020 for Multidiscipli… | NEP timetabling at individual-student granularity. CP-SAT, zero data. |
| **72** | Centralised Digital Platform for Comprehensive student activity record in HE… | Records platform. Pure CRUD. |
| **80** | Remote classroom for rural colleges | Low-bandwidth classroom delivery. No ML. |
| **82** | ERP-based Integrated Student Management system | ERP. Pure CRUD. |
| **84** | Develop computer programs (in any language preferably Python) to identify th… | Kolam grammar is computational geometry and L-systems. Elegant, tiny audience. |
| **94** | Identification of Infrastructure, Amenities, and Service Gaps in SC-Majority… | Gap analysis over Census / Mission Antyodaya style public data. GIS and rules. |
| **95** | Digital Mechanism for Beneficiary Identification under Grant- in-Aid (GIA) C… | Eligibility rules over a beneficiary register. |
| **96** | Mapping of Implementing and Executing Agencies across PM- AJAY Components | Registry and mapping. Pure CRUD. |
| **97** | Modalities for implementation of Direct Benefit Transfer (DBT) under Central… | Workflow and payment-rail integration. No ML. |
| **105** | Designing an Efficient Algorithm for Coordinated Swarm Engagement among Auto… | Swarm engagement is multi-agent algorithms plus simulation. No data, no training. |
| **106** | Temple &amp; Pilgrimage Crowd Management (Somnath, Dwarka, Ambaji, Pavagadh) | Crowd flow simulation plus darshan slot optimisation. Queueing theory, not ML. |
| **120** | Quantum Secure Email Client Application | Post-quantum crypto integration. Zero AI, zero data, pure engineering. |
| **124** | Secure closed group communication platform over exisiting public mobile comm… | End-to-end encrypted group messaging. Protocol engineering, no ML. |
| **138** | Cybersecurity Framework for Rural Digital Banking | Framework and controls. Vague, closer to policy than product. |

### Class B — pretrained models, APIs or RAG are sufficient

| PS | Statement | Note |
|---|---|---|
| **2** | Smart Tourist Safety Monitoring &amp; Incident Response System using AI Geo-Fenc… | Geofencing rules + anomaly heuristics + a ledger. No training. Very heavily picked. |
| **10** | Smart Crop Advisory System for Small and Marginal Farmers | Advisory can be retrieval over public agri-advisories; yield claims are where teams overreach. |
| **12** | Automated Attendance System for Rural Schools | Pretrained face/QR recognition; the hard part is privacy, not modelling. |
| **16** | Automated Student Attendance Monitoring and Analytics System for Colleges | Pretrained recognition plus analytics. Crowded and low-ceiling. |
| **29** | Authenticity Validator for Academia | OCR plus registry verification plus a ledger; optional forgery heuristics. |
| **31** | Crowdsourced Civic Issue Reporting and Resolution System | Routing rules plus optional pretrained image tagging. Extremely crowded. |
| **33** | AI-Based Smart Allocation Engine for PM Internship Scheme | Embeddings for skill semantics, then stable matching and constrained optimisation. |
| **34** | AI-Based Internship Recommendation Engine for PM Internship Scheme | Recommendation sibling of 33 — strictly the weaker framing of the same problem. |
| **35** | Integrated Platform for Crowdsourced Ocean Hazard Reporting and Social Media… | Pretrained multilingual classification over posts, plus geospatial hotspotting. |
| **43** | AI-Driven Public Health Chatbot for Disease Awareness | RAG over public health advisories. Commodity. |
| **44** | Smart Traffic Management System for Urban Congestion | Pretrained detection on traffic video plus signal-timing optimisation; simulation is the safer core. |
| **49** | Real life solutions for Waste Management | Routing, rules, optional pretrained waste image tagging. Statement is vague. |
| **54** | Designing and development of an application for on spot assessment of Roof T… | Pretrained segmentation for rooftops; the hydrology is deliberately deterministic. |
| **55** | Development of an AI-driven ChatBOT for INGRES as a virtual assistant | RAG plus natural-language-to-query over the public INGRES groundwater database. |
| **58** | AI-Powered Mobile Platform for Democratizing Sports Talent Assessment | Pretrained pose estimation (MediaPipe/MoveNet) plus rule-based rep counting. |
| **59** | AI-Powered Personal Farming Assistant for Kerala Farmers | Retrieval over public advisories plus optional pretrained pest imagery. |
| **61** | AI-Based Farmer Query Support and Advisory System | RAG over Kisan Call Centre style advisory corpora. |
| **64** | Document Overload at Kochi Metro Rail Limited (KMRL)-An automated solution | OCR, multilingual embeddings, RAG. Everything off the shelf. |
| **71** | Development of a Digital Mental Health and Psychological Support System for … | Screening instruments plus a guarded LLM layer. Sensitive, crowded. |
| **73** | One-Stop Personalized Career &amp; Education Advisor | Embeddings plus rules over a career taxonomy. Crowded. |
| **83** | Language Agnostic Chatbot | Translation and LLM APIs. Commodity. |
| **92** | Loan Utilization Tracking via Mobile | OCR on receipts plus rules; optional anomaly heuristics. |
| **98** | Transliterations tool for street signs | Pretrained OCR plus transliteration. Small, cute, low impact. |
| **109** | Enhancing farmer productivity through innovative technology solutions | Umbrella statement; whatever you build will be retrieval or rules. |
| **114** | Conversational SIEM Assistant for Investigation and Automated Threat Reporti… | RAG plus natural-language-to-query over security logs. |
| **116** | MAITRI : An AI Assistant for Psychological &amp; Physical Well-Being of Astronau… | Guarded LLM assistant. Buildable, but impossible to validate. |
| **121** | AI/ML based Auto Evaluation of R&amp;D proposals received at NaCCER, CMPDI Ranch… | Embeddings and rules — but the duplication corpus is confidential and unobtainable. |
| **123** | AI enabled cyber incident &amp; safety web portal for defence. | Portal, workflow and triage. Optional LLM classification. |
| **134** | Intelligent Recommendation System for Personalized Individual Development Pl… | Embeddings over competency frameworks. Low ceiling. |
| **135** | Smart Helpdesk Ticketing Solution for IT Services | LLM classification and routing. Commodity. |
| **136** | AI-based UFDR (Universal Forensic Extraction Device Report) Analysis Tool | UFDR parsing, pretrained NER, entity graph, natural-language querying. No training. |

### Class C — a small classical model on obtainable tabular data

| PS | Statement | Note |
|---|---|---|
| **1** | Smart Community Health Monitoring and Early Warning System for Water-Borne D… | Outbreak prediction needs longitudinal health + water-quality data that is thin and partly sensor-dependent. |
| **30** | AI-Based Crop Recommendation for Farmers | Small tabular model over public soil/rainfall/yield data; claims outrun the data fast. |
| **38** | AI-Powered Crop Yield Prediction and Optimization | Public district yield data supports a small tabular model; anything finer needs data you lack. |
| **66** | Development of a travel related software app that can be installed on mobile… | Trip-chain and mode inference from phone sensors needs a modest labelled set. |
| **79** | Accelerating High-Fidelity Road Network Modelling for Indian Traffic Simulat… | Road-network modelling with some learned components; MATLAB-centric and specialised. |
| **81** | AI-based drop-out prediction and counselling system | Dropout prediction is a small tabular classifier; the data is synthetic or institutional. |
| **85** | Blockchain-Based Blue Carbon Registry and MRV System | The MRV half needs remote-sensing analysis; the registry half is a ledger. |
| **93** | Beneficiary Credit Scoring with Income Verification Layer for Direct Digital… | Credit scoring is a small tabular model, but the training data is exactly what you lack. |
| **100** | Real-Time AI/ML-Based Phishing Detection and Prevention System. | Feature-based classifier on public phishing corpora. Small and trainable. |
| **125** | Al-Powered DPR Quality Assessment and Risk Prediction System for MDoNER | LLM extraction plus a small tabular overrun model on public project-outcome records. |
| **132** | Predicting Project Costs and Timeline | Same shape as 125: small tabular model, public project data possible. |
| **133** | Forecasting materials demand with machine learning for supply chain planning… | Demand forecasting plus inventory optimisation; needs their consumption history. |
| **139** | Hybrid Renewable Energy Generation Solution | Hybrid generation sizing is optimisation plus small forecasting models. |
---

## Best of the survivors

81 statements pass the training filter. Most are still not worth choosing — CRUD portals, gamified education apps, crop advisories and civic-reporting clones make up the bulk of Class A and B, and they are simultaneously the easiest to build and the most heavily picked. Ranking the survivors on *winnability* rather than *buildability* gives this:

| Rank | PS | Statement | Class | Score | Note |
|---|---|---|---|---|---|
| 1 | **65** | KMRL train induction | A | **87** | Deep-dived in Part 1 |
| 2 | **70** | NEP timetable | A | **87** | Deep-dived in Part 1 |
| 3 | **22** | **Railway section throughput** | **A** | **86** | **Missed by your shortlist — analysed below** |
| 4 | **33** | PM internship allocation | B | 85 | Deep-dived |
| 5 | **64** | KMRL documents | B | 82 | Deep-dived |
| 6 | **136** | UFDR forensic analysis | B | 81 | Missed — see below |
| 7 | **125** | DPR quality & risk | C | 79 | Deep-dived |
| 8 | **54** | Rooftop rainwater | B | 79 | Deep-dived |
| 9 | **35** | Ocean hazard reporting | B | 78 | Missed — see below |
| 10 | **26** | NAMASTE / ICD-11 | A | 77 | Deep-dived |
| 11 | **106** | Temple crowd management | A | 76 | Missed — see below |
| 12 | **55** | INGRES groundwater chatbot | B | 76 | Missed — pairs with PS 54 |
| 13 | **23** | Panchakarma scheduling | A | 74 | Under-picked scheduling problem |
| 14 | **124** | Secure group comms (MoD) | A | 74 | Zero AI, pure protocol engineering |
| 15 | **120** | Quantum-secure email (ISRO) | A | 73 | Zero AI, weak demo |
| 16 | **94** | Adarsh Gram gap analysis | A | 72 | GIS + public data, obscure |
| 17 | **114** | Conversational SIEM (ISRO) | B | 72 | Needs security domain |
| 18 | **105** | Drone swarm engagement | A | 71 | No data at all; simulation demo, harsh judges |
| 19 | **121** | Coal R&D proposals | B | 66 | Deep-dived — still a no |
| — | 82, 72, 17, 42, 31, 43, 73 | ERP / records / gamified / civic / chatbots | A–B | 45–60 | Easy to build, impossible to win with |

Scores 1–2 and 4–5, 7–8, 10, 19 come from the full 22-section analyses in Parts 1–3. Ranks 3, 6, 9, 11–18 are rapid screens against the same rubric — directionally reliable, not equally deep.

## Four statements your shortlist should have contained

**PS 22 — Maximizing Section Throughput (Ministry of Railways).** The big miss. Full treatment below.

**PS 136 — UFDR Analysis Tool (MHA).** Forensic extraction reports from seized phones run to tens of thousands of records; investigators read them manually. Parse the report, run pretrained NER, build an entity-and-timeline graph, answer natural-language questions over it. No training. Architecturally it is PS 64 with a graph, but the domain is far more compelling and the field is thinner — most teams see "forensic" and skip it. Its one real risk is corpus: genuine UFDR files contain real evidence and are unobtainable, so you synthesise against the documented format and say so. **Take this over PS 64** if you like the document-intelligence shape and want a less crowded room.

**PS 35 — Ocean Hazard Reporting & Social Media Analytics (MoES/INCOIS).** Crowdsourced hazard reports plus pretrained multilingual classification over social posts, fused into geospatial hotspots for the tsunami warning centre. Strong impact, good map demo, no training. Main risk is social-media API access, which is now restricted and expensive — mitigate with cached corpora and say so plainly.

**PS 106 — Temple & Pilgrimage Crowd Management (Gujarat).** Crowd-flow simulation plus darshan slot-allocation optimisation across four sites. Queueing theory and OR, zero data dependency, and a genuinely dramatic demo — watch a crowd surge form, then re-allocate slots and watch it dissolve. Under-rated, and the closest thing on the list to PS 65's profile at lower difficulty.

Also worth knowing: **PS 55 pairs with PS 54.** Both are Ministry of Jal Shakti groundwater statements. The CGWB/India-WRIS research you do for one is most of the domain work for the other, so if you pick either, you get a cheap second submission.

---

# PS 22 — Maximizing Section Throughput Using AI-Powered Precise Train Traffic Control

**Organisation:** Ministry of Railways · **Category:** Software · **Theme:** Transportation & Logistics · **Class A** · **Score 86/100**

**1. The problem.** A railway *section* is the stretch between two major stations, divided into block sections that only one train may occupy at a time. A section controller decides, continuously and under pressure, which train goes first: hold the passenger express or let the freight clear, cross two trains at loop A or loop B, which train takes which platform. Today this is done by an experienced human with a train graph, a phone and memory. It does not scale, it is not optimised, it cannot be replayed, and when a train runs late the recovery decisions are pure improvisation. Users are section controllers and divisional operations; beneficiaries are every passenger and every tonne of freight on Indian Railways. Success means a controller sees an optimised, explained precedence plan in seconds, can ask "what if I hold this freight eight minutes," and gets a new plan the moment reality breaks the old one.

**2. What it really requires.** Mandatory: model block-section occupancy and headway, decide precedence and crossings, maximise throughput while respecting priorities, re-optimise under disruption, and explain decisions. Implied and mostly missed: **conflict-free means physically conflict-free in continuous time**, not "no two trains in the same row of a table"; loop and platform capacity are hard constraints; train priority is a policy input, not a hardcoded constant; the objective is multi-part (throughput, weighted delay, priority adherence) and the weights belong to Railways; and re-optimisation must be *minimum-disruption*, because a plan that changes everything is a plan a controller will not use. The classic misreading is treating this as timetable *generation*; it is real-time timetable *repair*.

**3. Solution.** A controller decision-support console: ingest section topology, today's timetable and live train positions → CP-SAT model over train-to-block-to-time assignments → output a precedence plan rendered as a live **train graph** (time on one axis, distance on the other, one line per train) with conflicts resolved → per-decision explanation → what-if overrides → disruption injection with minimum-change re-solve → KPI panel (throughput, average weighted delay, priority adherence, loop utilisation). Roles: controller, divisional supervisor, read-only observer.

**4. AI/ML.** **Class A.** Constraint programming is the entire engine, and the statement itself points at operations research. ML appears only optionally — a small tabular model estimating run-time variability per train type, used as a soft buffer. An LLM renders structured reasons as prose and answers "why did TR-1042 wait?" It must never produce the plan. Do not attempt reinforcement learning here; you cannot validate it and cannot explain it.

**5. Data.** Section topology, block lengths and loop positions — approximable from public railway maps and published section data. Timetables — **public**. Train priorities and headway rules — published operating principles. Live positions — synthesised. **Dataset risk: LOW**, for the same reason as PS 65: the physics and the rules are the specification, so a parameterised generator is the correct methodology. Biggest risk is getting headway and block semantics subtly wrong; mitigate by making topology and headway configurable and stating the assumption.

**6. Architecture.** React + TypeScript with a Canvas train-graph renderer → FastAPI → optimisation service running OR-Tools CP-SAT under Celery → PostgreSQL for topology, plans, versions and audit → Redis for caching and job brokering → WebSocket streaming of solver progress → LLM API for explanation text only. No vector DB, no Kafka.

**7. Stack.** Python/FastAPI (OR-Tools binding is the deciding factor), OR-Tools CP-SAT, Celery + Redis, PostgreSQL, React + Canvas for the graph, Recharts for KPIs, Docker Compose. Identical to PS 65 — which is exactly why the two are strategically linked.

**8. MVP.** Must have: section topology model, synthetic scenario generator, CP-SAT precedence and crossing model with block occupancy and headway, train-graph visualisation, per-decision explanations, conflict/infeasibility reporting. Should have: what-if override with KPI delta, disruption injection with minimum-change re-solve, priority-weight configuration. Nice to have: multi-section handover, freight pathing, throughput comparison against a manual baseline.

**9–10. Differentiators.** Continuous-time block occupancy rather than slotted tables; minimum-disruption repair; infeasibility cores that name the conflicting constraints; configurable objective weights showing the price of a policy; a measured throughput gain against a simulated manual baseline. Competitors will build a train-list dashboard, a greedy or genetic ranker, and an LLM that "suggests" precedence — none of which survives the question "prove no two trains occupy the same block."

**11. Demo.** Open on a controller's train graph. Generate the optimised plan — lines resolve, conflicts vanish, solve time and constraint count on screen. **WOW moment:** delay one train by twenty minutes and watch the graph repair itself in seconds, with a toast quantifying the cost (`3 trains re-sequenced · weighted delay +4.2 min · throughput unchanged`). Close on the throughput comparison against the manual baseline.

**12. Judge questions.** The five that matter: *"Where is the AI?"* — constraint programming, deliberately, because block occupancy is a safety constraint not a probability. *"Is it really conflict-free?"* — yes, verified by an independent checker run live. *"Does it match real Railways operating rules?"* — headway and priority are configurable inputs, and we state which assumptions we made. *"What about live signalling integration?"* — read-only ingestion in v1; we never write to signalling, which removes the entire safety-certification class of risk. *"Would a controller trust it?"* — it proposes, they approve, every override is logged and priced.

**13. Failure modes.** Solver too slow at realistic train counts (cap time, take the anytime incumbent, show the optimality gap); over-constrained model that is always infeasible (soft constraints by default, infeasibility cores); train graph consuming the whole build (start it day 2, it is the demo); domain error in block/headway semantics (configurable, stated openly).

**14. Difficulty.** Frontend 8 (the train graph is the hardest single UI on this whole list) · Backend 6 · Optimisation **9** · Data 3 · Integration 4 · Deployment 3 · Testing 7 · **Overall 8/10. Development risk: HIGH**, concentrated in the solver and the graph.

**15–17. Team, time, cost.** Six people: two on CP-SAT from hour one, one on the train-graph renderer full-time, one on the rest of the frontend, one backend, one domain and demo. 24h gets a basic precedence model on a toy section; three days adds the train graph; one week adds disruption repair; two weeks polishes. Cost ≈ ₹0–800, everything open-source with optional LLM explanations.

**18–19. Security and deployment.** Operational rail data is safety-sensitive: RBAC, TLS, append-only audit of every plan and override, read-only integration with signalling and TMS, no PII anywhere near the LLM. Production would need on-premise or government-cloud deployment, integration with the real control system, and — critically — a shadow-mode period where the system proposes while controllers decide, before any reliance.

**20. Score.** Impact 19/20 · Innovation 13/15 · Feasibility 10/15 · Low data 9/10 · Low training 10/10 · Demo 10/10 · Scalability 4/5 · Deployment 9/10 · Team accessibility 2/5 → **86/100.**

**21. Brutal assessment.** Genuinely difficult: continuous-time block occupancy in CP-SAT, and the train graph. Deceptively easy: a table of trains with a precedence column, which you will have by hour eight and which proves nothing. What could kill it: Railways judges know this domain cold and will find a shallow model in one question — and the field is larger than for PS 65, because Ministry of Railways statements attract crowds. What could impress: the self-repairing train graph, which is the single best visual on the entire software list. **Worth choosing? Yes — but it is the higher-ceiling, higher-variance sibling of PS 65.**

---

# REVISED VERDICT

## Final ranking, full software field

| Rank | PS | Score | Verdict |
|---|---|---|---|
| 1 | **PS 65 — KMRL train induction** | **87** | **Winner. Unchanged.** |
| 2 | PS 70 — NEP timetable | 87 | Safest strong pick |
| 3 | **PS 22 — Railway section throughput** | **86** | Highest ceiling, highest variance |
| 4 | PS 33 — PM internship allocation | 85 | Highest impact, most crowded |
| 5 | PS 64 — KMRL documents | 82 | Highest floor, lowest ceiling |

## Why PS 65 still wins, now that PS 22 is on the board

PS 22 beats PS 65 on impact (19 vs 16) and demo (10 vs 9). PS 65 beats PS 22 on feasibility (12 vs 10), team accessibility (3 vs 2), and — decisively — on **competition**. Three arguments settle it:

1. **Scope you can actually finish.** PS 65 is a discrete nightly assignment over ~25 objects. PS 22 is continuous-time scheduling with block occupancy and headway constraints. Both need CP-SAT; only one is completable to a high standard in the time you have.
2. **The field.** Ministry of Railways statements draw large crowds. PS 65 does not. Against equal scores, choose the room with fewer strong teams.
3. **Judge risk.** Railways judges know section control intimately and will expose a shallow model instantly. KMRL judges will too — but PS 65's six variables are fully enumerated in the statement, so the target you must hit is written down for you. PS 22's is not.

**PS 22 is the right pick only if** you have two people who have already used CP-SAT or a similar solver, and you are optimising for the highest possible ceiling rather than the best expected outcome. If both are true, take it — it is the more impressive problem.

## The strategic play

PS 65 and PS 22 are the *same engineering investment*: OR-Tools CP-SAT, FastAPI, a Canvas visualisation, multi-objective weights, minimum-disruption re-solve, infeasibility cores. Build that competence once and both statements are open to you, and PS 70 and PS 106 come nearly free as well. That is four viable submissions off one core skill — which is the strongest argument in this entire document for pointing your team at constraint programming rather than at another RAG pipeline.

**Decision, in one line: build PS 65. Keep PS 22 as the stretch option and PS 70 as the fallback, and start the solver on day one regardless of which you pick.**

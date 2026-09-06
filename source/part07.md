---
---

# ⑦ PS 26 — NAMASTE & ICD-11 TM2 Integration into EMR Systems (EHR Standards for India)
**Organisation:** Ministry of Ayush · **Category:** Software · **Theme:** MedTech / HealthTech
**Score: 77/100 · Recommendation: MAYBE — the best engineering on the list, and the worst demo**

## 1. Problem Understanding

This statement is not about AI at all. It is about **medical terminology interoperability**, and understanding that is the whole battle.

When a doctor records a diagnosis in an electronic health record, the diagnosis must be stored as a *code* from a controlled vocabulary, not as free text — otherwise nothing downstream works: insurance claims, disease surveillance, research, or analytics. Modern biomedicine uses **ICD-11** (the WHO's classification). India's traditional medicine systems — Ayurveda, Siddha and Unani — have their own standardised terminology, **NAMASTE**, published by the Ministry of Ayush, covering several thousand disorder terms.

WHO's ICD-11 includes **Traditional Medicine Module 2 (TM2)**, which provides codes for traditional-medicine conditions inside the international classification. So there are now two vocabularies that must speak to each other:

- An Ayurvedic practitioner records a NAMASTE term.
- The health system, insurers and international reporting need an ICD-11 code (TM2, and often a biomedical ICD-11 code alongside).

Without a mapping and an API, Ayush clinical activity is invisible to national health analytics and insurance. **Dual coding** — recording both the NAMASTE term and the corresponding TM2 (and where relevant biomedicine) code on the same problem-list entry — is the goal.

The statement asks for a **FHIR R4-compliant terminology micro-service** that: ingests the NAMASTE terminology and publishes it as a FHIR `CodeSystem`; retrieves ICD-11 TM2 and Biomedicine content via the WHO ICD API and publishes a `ConceptMap`; exposes an **auto-complete value-set lookup** so a clinician typing "Amavata" gets candidate codes; provides a **translate** operation between systems; accepts a **FHIR Bundle** encounter upload carrying dual-coded conditions; and does all of this under India's EHR Standards — meaning **ABHA-linked OAuth 2.0 authentication, consent handling, version tracking and audit trails**.

**Users:** EMR vendors and their developers (the direct consumers of the API), and through them Ayush practitioners. **Beneficiaries:** patients, insurers, the Ministry of Ayush and national health analytics.

**Why it matters:** without this layer, a huge volume of Indian healthcare activity is unmeasurable and uninsurable. It is a small piece of software with disproportionate systemic consequence.

## 2. What the Statement REALLY Requires

**Mandatory — and unusually precise for an SIH statement**
- Ingest NAMASTE terminology → generate a **FHIR R4 `CodeSystem`**.
- Fetch ICD-11 TM2 (and Biomedicine) via the **WHO ICD API** → generate a **`ConceptMap`** between NAMASTE and TM2.
- **Auto-complete value-set lookup** endpoint for clinical search.
- **Translate** operation (NAMASTE ↔ TM2 / biomedicine codes).
- Accept a **FHIR `Bundle`** upload of an encounter with dual-coded `Condition` resources.
- **ABHA-linked OAuth 2.0**, consent, versioning, and audit trails per India's EHR Standards.

**Implied**
- **Correctness is the deliverable.** A FHIR resource is either valid against the specification or it is not, and it is machine-checkable. This is unusual and it is your advantage: you can *prove* correctness rather than claim quality.
- **Version management** — ICD-11 has releases and NAMASTE has updates; a ConceptMap must be versioned so historical records remain interpretable.
- **Mapping is semantically hard.** Ayurvedic disorder concepts do not map one-to-one onto TM2 categories. You must express *equivalence type* (`equivalent`, `wider`, `narrower`, `relatedto`, `inexact`) rather than pretending every mapping is exact — FHIR ConceptMap has fields for precisely this, and using them correctly is a strong signal of understanding.
- **You need a demonstrable consumer.** An API alone cannot be demoed. Build a small EMR-like front end that consumes your own service.
- **Audit and consent are not decoration** — they are the compliance core, and a health-sector judge will check.

**Optional:** analytics dashboards, SNOMED CT/LOINC semantics, insurance-claim generation, morbidity reporting.

**Misunderstanding to avoid:** treating this as a search box over a CSV. Without genuine FHIR resource conformance, ABHA-style OAuth and versioned ConceptMaps, you have built a lookup table and missed the statement entirely.

## 3. Proposed Solution

**Product concept:** *"AYUSH-Bridge"* — a FHIR R4 terminology micro-service plus a reference EMR client that demonstrates dual coding end to end.

**Core modules**
1. **Terminology Ingestion** — parse the NAMASTE terminology release; normalise codes, display names, transliterations and definitions across Ayurveda, Siddha and Unani.
2. **FHIR CodeSystem Publisher** — emit a conformant `CodeSystem` resource with proper metadata, versioning and hierarchy, plus `ValueSet` definitions for clinical use.
3. **WHO ICD-11 Client** — authenticate to the WHO ICD API, fetch TM2 and Biomedicine entities, cache locally with release-version pinning.
4. **Mapping Engine** — candidate generation using multilingual embeddings over term definitions, plus lexical matching on transliterations; each candidate presented for **curator review** with a required equivalence type. Curated mappings are published as a versioned `ConceptMap`.
5. **Terminology API** — FHIR-style operations: `$lookup`, `$validate-code`, `$expand` (auto-complete), `$translate`, plus a plain REST search endpoint for EMR vendors who are not FHIR-native.
6. **Encounter Ingest** — accept a FHIR `Bundle` (Patient, Encounter, Condition with dual codings), validate every resource against R4 profiles, persist, and return an `OperationOutcome` on failure.
7. **Security & Compliance** — OAuth 2.0 with ABHA-style token flow, scope-based authorisation, consent artefact per encounter, immutable audit log of every terminology access and data write, ISO 22600-style access policy.
8. **Reference EMR Client** — a small clinical UI: search a condition, see NAMASTE and TM2 codes appear together, save the encounter, view the resulting Bundle.
9. **Analytics View** — morbidity distribution by NAMASTE/TM2 code, which is the *reason* this whole layer exists and makes the value legible in one chart.

**Journey:** a practitioner types "Amavata" → auto-complete returns the NAMASTE code with its mapped TM2 candidates and equivalence type → selects → the condition is stored dual-coded → the encounter is submitted as a FHIR Bundle with a consent artefact → the audit log records it → the analytics view shows Ayush morbidity now visible in ICD-11 terms alongside biomedical data.

## 4. AI/ML Requirement

**Classification: A — essentially no AI required. Optional embedding assistance for mapping candidate generation. Zero training.**

| Component | Technique | Why |
|---|---|---|
| Terminology ingestion & FHIR generation | **Deterministic code** | It's a specification, not a prediction |
| Auto-complete | **Trigram/full-text search + prefix indexes** | Fast, exact, and clinicians expect deterministic behaviour |
| **Mapping candidate generation** | **Multilingual sentence embeddings over term definitions + lexical similarity** | The one genuinely useful ML touch: it proposes, a human curates |
| Translate operation | **Lookup over the curated ConceptMap** | Must be deterministic — a clinical code cannot be generated probabilistically |
| Clinical documentation assist (optional) | **LLM over free text → suggested codes, always requiring confirmation** | A real value-add, but never auto-applied |

**The line to hold:** an LLM may *suggest* a code; only a curated ConceptMap may *assign* one. In a clinical context, a hallucinated diagnosis code is a patient-safety and insurance-fraud issue, and saying this crisply is one of the strongest answers you can give any judge.

## 5. Dataset Requirements

| Dataset | Why | Public? | Obtainable? | Synthetic? | Mock OK? |
|---|---|---|---|---|---|
| NAMASTE terminology | Core | **Yes** — published by the Ministry of Ayush | Yes | No need | Use real |
| **ICD-11 TM2 + Biomedicine** | Core | **Yes** — WHO ICD API, free with registration; also downloadable | Yes | No need | **Use the real API** |
| FHIR R4 specification & profiles | Conformance | **Yes** | Yes | — | Use real |
| India EHR Standards | Compliance | **Yes** — published by MoHFW | Yes | — | Use real |
| ABHA/ABDM sandbox | Auth | **Yes** — sandbox exists, registration required and can take time | Probably | **Yes — mock the flow** | Mock, and say so |
| Patient encounters | Demo data | No (PHI) | No | **Yes — must be synthetic** | Yes |
| Existing NAMASTE↔TM2 mappings | Ground truth | Partial | Limited | Partly | Curate a subset yourself |

**This is the lowest data risk on your entire list.** Both terminologies are public, the WHO API is free and real, and the only synthetic element is patient data — which *must* be synthetic for privacy reasons anyway, so it costs you nothing in credibility.

**Biggest risk:** ABDM sandbox access timing. **Mitigation:** implement a fully standards-correct OAuth 2.0 flow against a local authorisation server that mirrors ABHA's token structure and scopes, and state plainly that swapping the issuer URL is the only change needed for the real sandbox. That is an honest, complete answer.

**Second risk:** mapping quality. Ayurvedic nosology is not a relabelling of biomedical disease; forcing exact mappings would be wrong. **Mitigation:** curate a high-quality subset (150–300 terms) with explicit equivalence types and honest `inexact`/`relatedto` labels, and say clearly that full mapping is expert clinical work — which is true and is what the Ministry itself would do.

**Dataset Risk: LOW.**

## 6. Technical Architecture

```
EMR Vendor system / Ayush Practitioner (reference client) / Administrator-Curator
        |
        v
Reference EMR client (React)          Curator console (React)
  |-- Condition search + dual code       |-- Mapping review queue
  |-- Encounter form                     |-- Equivalence type assignment
  +-- Bundle viewer                      +-- ConceptMap version publish
        |   OAuth 2.0 (ABHA-style) Bearer token
        v
API Gateway (FastAPI)  --  OAuth2 / scopes / consent check / audit interceptor
        |
   +----+---------------+------------------+--------------------+
   v                    v                  v                    v
Terminology Svc     Mapping Svc        FHIR Svc            Audit/Consent Svc
($lookup,           (candidate gen     (Bundle validate,   (immutable log,
 $expand,            via embeddings,    Condition/Encounter consent artefacts,
 $validate-code,     curation,          persist,            access records)
 $translate)         ConceptMap ver.)   OperationOutcome)
   |                    |                  |                    |
   v                    v                  v                    v
PostgreSQL (CodeSystem, ConceptMap versions, concepts, encounters, audit)
   |                              |
   v                              v
Redis cache (hot lookups)   WHO ICD-11 API (cached, version-pinned)
        |
        v
   Analytics view (morbidity by code)  -  OpenAPI docs  -  Conformance statement
```

**Design points that matter here**
- **Version everything.** CodeSystem, ValueSet and ConceptMap all carry versions; historical encounters resolve against the version in force when they were recorded.
- **Cache the WHO API aggressively and pin the release** — you must not depend on network conditions during a demo, and clinical systems must not silently change meaning when WHO publishes an update.
- **The audit interceptor is cross-cutting** — every terminology access and every write is logged with subject, purpose and timestamp.
- **Publish a FHIR CapabilityStatement.** It is a small thing that tells a health-IT judge instantly that you know the ecosystem.

## 7. Recommended Tech Stack

| Layer | Choice | Why here |
|---|---|---|
| Backend | **Python + FastAPI**, or **Java + HAPI FHIR** | FastAPI is faster to build and lets you hand-craft conformant resources. **HAPI FHIR** gives you a battle-tested FHIR server and validator for free — if anyone on the team knows Java, this is a serious advantage and an instant credibility signal |
| FHIR validation | **`fhir.resources` (Python) or HAPI's validator** | Conformance must be machine-verified, not asserted |
| Database | **PostgreSQL** | Terminology hierarchies, versioned maps, audit — all relational |
| Search/auto-complete | **PostgreSQL trigram + full-text**, optionally OpenSearch | Sub-100ms prefix search on a few thousand terms needs nothing exotic |
| Embeddings (mapping aid) | **`multilingual-e5` / LaBSE locally** | Handles transliterated Sanskrit/Tamil/Urdu terms; free |
| Cache | **Redis** | Hot lookups and WHO API responses |
| Auth | **OAuth 2.0 — Authlib, or Keycloak as the authorisation server** | Keycloak makes the ABHA-style flow realistic and demonstrable with little code |
| Frontend | **React + TypeScript** | Two small clients: reference EMR and curator console |
| Docs | **OpenAPI/Swagger + a FHIR CapabilityStatement** | EMR vendors are your users; the docs *are* the product surface |
| Deploy | **Docker Compose** | ₹0 |

## 8. MVP for SIH

**MUST HAVE**
1. NAMASTE ingestion → valid FHIR R4 `CodeSystem` (validated, not just generated).
2. WHO ICD-11 API integration for TM2 + Biomedicine, cached and version-pinned.
3. Curated `ConceptMap` (150–300 terms) with **explicit equivalence types**, versioned.
4. `$lookup`, `$expand` (auto-complete), `$translate`, `$validate-code` endpoints.
5. FHIR `Bundle` ingest with validation and `OperationOutcome` on error.
6. OAuth 2.0 with ABHA-style scopes + consent artefact + immutable audit log.
7. **Reference EMR client** demonstrating dual coding end to end.

**SHOULD HAVE**
8. Curator console with embedding-assisted mapping suggestions.
9. Version management demo — two ConceptMap versions, historical resolution.
10. Analytics view: morbidity by NAMASTE/TM2 code.
11. Published CapabilityStatement + OpenAPI docs.

**NICE TO HAVE**
12. Biomedical double-coding (TM2 + biomedicine on one condition). 13. LLM-assisted coding from clinical free text with confirmation. 14. Insurance claim (FHIR Claim) generation. 15. SNOMED CT/LOINC semantic alignment.

**Finish before presenting:** MUST + 9 and 10. Item 7 is not optional — without a client, there is nothing to show.

## 9. Advanced Features

- **Live FHIR validation on stage** — paste a Bundle, show it validating; then break one field and show the `OperationOutcome`. Correctness you can *prove* beats accuracy you claim.
- **Honest equivalence typing** — displaying `wider`/`inexact` rather than forcing false equivalence demonstrates real understanding of both medical systems.
- **Version-aware resolution** — show an encounter recorded under ConceptMap v1 still resolving correctly after v2 is published.
- **Embedding-assisted curation** with a human in the loop — AI where it belongs.
- **Consent and audit demonstrated**, not described — click through a consent artefact and show the resulting audit entry.
- **Analytics payoff** — Ayush morbidity data appearing in an ICD-11-coded national view. This is the *why* of the entire project and takes one chart.
- **Developer experience** — a live Swagger console judges can call. An API product's UX is its documentation.
- **Offline-capable terminology cache** for low-connectivity clinics.

## 10. Innovation Analysis

1. **Genuine standards conformance** — machine-validated FHIR R4 resources, which almost no SIH team will attempt and none will fake successfully.
2. **Semantically honest mapping** with equivalence types instead of forced one-to-one pairs.
3. **Version-aware terminology** so historical records stay interpretable.
4. **Compliance built in** — OAuth 2.0, consent artefacts, immutable audit — rather than bolted on.
5. **Human-curated, AI-assisted mapping**, with a clear line between suggestion and assignment.
6. **A real integration target** — this is a component ABDM-connected EMR vendors could actually adopt.

**What competitors will build:** a CSV of NAMASTE terms in a database, a search box, a hardcoded mapping table, and a claim of "FHIR-compliant" with resources that would fail validation. Weaknesses: no real WHO API integration, no ConceptMap semantics, no OAuth, no versioning, no audit.

**The uncomfortable truth:** your differentiation is *correctness*, which is invisible unless you make it visible. Live validation and a working WHO API call are how you make it visible. If you cannot make correctness visual in the first three minutes, this project loses to a flashier one that is technically inferior — and you must decide, before choosing it, whether you are willing to accept that.

## 11. SIH Demo Strategy (8 minutes)

| # | Stage | Time | Screen | Say |
|---|---|---|---|---|
| 1 | Problem | 1:00 | An Ayurvedic prescription beside a hospital claim form; the claim is rejected | "Crores of Ayush consultations happen every year. To insurance, to surveillance, to national health data — almost none of them exist, because there's no code." |
| 2 | Standards | 0:45 | Diagram: NAMASTE ↔ your service ↔ ICD-11 TM2, with FHIR R4 and ABHA labelled | "This isn't an app. It's the missing translation layer between two medical worlds." |
| 3 | Live WHO call | 0:40 | Hit the WHO ICD-11 API live; TM2 entities return | "That's the World Health Organization's live API, not a copy we pasted." |
| 4 | Clinical use | 1:20 | Reference EMR: type "Amavata" → auto-complete shows the NAMASTE code **and** the mapped TM2 code with equivalence type `wider` | "One search, dual coded — and we tell the clinician the mapping is broader, not identical, because Ayurvedic and biomedical concepts genuinely aren't the same thing." |
| 5 | **WOW** | 1:30 | Save the encounter → the FHIR Bundle appears → run it through a **standards validator live: PASS**. Then delete a required field and re-run: **FAIL with OperationOutcome** | "This isn't 'FHIR-inspired'. Any FHIR system in the world can consume this, and here's the validator proving it." |
| 6 | Compliance | 0:50 | OAuth token with ABHA-style scopes; consent artefact; the audit entry the request just created | "Authentication, consent and audit, per India's EHR Standards — the three things that decide whether health software is deployable." |
| 7 | Versioning | 0:45 | Publish ConceptMap v2; show an encounter from v1 still resolving under v1 | "Medical vocabularies change. Patient records can't." |
| 8 | Payoff | 0:45 | Analytics: Ayush morbidity distribution rendered in ICD-11 terms | "This chart has never existed at national scale. That's what the translation layer buys." |

**WOW moment: stage 5 — live FHIR validation passing, then failing on demand.** It is the only way to make correctness visible, and it is genuinely impressive to anyone who knows the ecosystem. **Risk: it lands hardest with a health-IT judge and may fall flat with a generalist.** Stage 8's analytics chart is your insurance for that case, so do not cut it.

## 12. Judge Questions (14)

| # | Question | Testing | Strong answer | Avoid |
|---|---|---|---|---|
| 1 | "Where's the AI in this?" | **The decisive risk** | "Deliberately minimal. A diagnosis code cannot be generated probabilistically — a hallucinated code is an insurance-fraud and patient-safety issue. AI assists mapping *curation* through multilingual embeddings that propose candidates; a human assigns the equivalence type. The hard part here isn't intelligence, it's interoperability, and that's what the statement asks for." | Inventing an AI component to sound impressive. |
| 2 | "Is this actually FHIR-compliant?" | The core claim | "Yes, and it's machine-verifiable — we validate against R4 profiles in the demo, and we publish a CapabilityStatement. Compliance here is provable, not claimed, which is unusual and it's why we chose the statement." | "Yes, we followed the spec." |
| 3 | "How accurate are your NAMASTE↔TM2 mappings?" | Domain honesty | "We curated 240 mappings with explicit equivalence types, and roughly a third are `wider` or `inexact` rather than `equivalent` — because Ayurvedic nosology isn't a relabelling of biomedical disease. Full mapping is expert clinical work; our contribution is the infrastructure plus an AI-assisted curation workflow that makes expert review efficient." | "Our mappings are 95% accurate." |
| 4 | "What if a mapping is clinically wrong?" | Patient safety | "Every mapping carries its equivalence type and is surfaced to the clinician, who selects rather than accepts silently. Mappings are versioned and attributable, so a correction is traceable, and nothing is auto-applied to a patient record." | "Our mapping is correct." |
| 5 | "Did you integrate with the real ABDM/ABHA sandbox?" | Honesty | "We implemented the OAuth 2.0 flow with ABHA-style scopes and consent artefacts against a local authorisation server, because sandbox onboarding takes longer than a hackathon. The issuer URL is configuration — pointing it at the real sandbox is a config change, not a rewrite. We'd rather show you a correct flow than claim access we don't have." | Claiming integration you don't have. |
| 6 | "Would an EMR vendor actually adopt this?" | Adoption | "That's exactly who we built for — a standards-conformant micro-service with OpenAPI docs, a plain REST path for non-FHIR-native systems, and no requirement to change their data model. They add a lookup call and a second coding on the Condition resource." | "Vendors would integrate it." |
| 7 | "What happens when WHO updates ICD-11?" | Maturity | "We pin the release version and cache it, so meaning never changes underneath existing records. A new release produces a new ConceptMap version, and historical encounters keep resolving against the version in force when they were recorded." | "We fetch live data." |
| 8 | "Patient data security?" | Health-sector rigour | "All demo patient data is synthetic — real PHI has no place in a hackathon. Architecturally: OAuth 2.0 with scoped access, consent artefacts per encounter, immutable audit of every terminology access and write, encryption in transit and at rest, and role-based access aligned to ISO 22600." | "We hash the data." |
| 9 | "How fast is auto-complete?" | Engineering | "Sub-50ms — trigram-indexed prefix search over a few thousand terms with a Redis cache. Clinicians abandon a search box above about 200ms, so this was a design constraint, not an afterthought." | "It's fast enough." |
| 10 | "What about Siddha and Unani, not just Ayurveda?" | Coverage | "All three are in the NAMASTE terminology and all three are ingested; the CodeSystem carries the system of medicine as a property, and search can filter on it." | Only handling Ayurveda. |
| 11 | "Could an LLM just do this mapping automatically?" | Judgement | "It could propose candidates — which is exactly how we use it. It should not assign them. A confident wrong mapping between two medical traditions has consequences for treatment and reimbursement, and there's no ground truth for the model to have learned from." | "Yes, we could automate it fully." |
| 12 | "What's your test coverage / how do you know it works?" | Rigour | "Resource-level validation against the R4 spec on every generated resource, contract tests on each API operation, and a round-trip test — code in, translate, translate back, verify. Conformance testing is the natural fit for a standards project." | "We tested manually." |
| 13 | "Who maintains the mappings long term?" | Deployment realism | "The Ministry of Ayush, through the curator console — that's why we built curation as a product surface rather than a script. Our system's job is to make expert review efficient and versioned, not to replace the experts." | "The AI keeps it updated." |
| 14 | "Why should this win over a flashier project?" | Your weak point — prepare it | "Because it's the one on this list a ministry could deploy next quarter. It's built to a published specification, it's machine-verifiably correct, it integrates a live WHO API, and it unlocks national visibility for a system of medicine that currently has none. It's less spectacular and more finished." | Getting defensive. |

## 13. Failure Modes & Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Demo is boring / judges don't grasp the value** | **High** | **Fatal** | Lead with the rejected insurance claim; end with the analytics chart; make validation visual |
| WHO API rate limits or auth issues | Medium | High | Cache aggressively, pin a release, keep a local snapshot fallback |
| ABDM sandbox access not granted in time | High | Medium | Standards-correct local OAuth server; state the swap honestly |
| FHIR spec learning curve eats the week | **High** | High | Use HAPI FHIR or `fhir.resources` rather than hand-rolling; assign one person to FHIR on day 1 |
| Mapping quality challenged by a domain expert | Medium | Medium | Honest equivalence types; curated subset; explicit scope statement |
| Resources fail validation late in the build | Medium | High | Validate continuously from day 1, in CI |
| Generalist judges undervalue standards work | **High** | High | The analytics payoff slide + the insurance-claim framing |

## 14. Development Difficulty

| Dimension | Rating |
|---|---|
| Frontend | 4/10 — two small clients |
| Backend | 7/10 |
| AI | 2/10 — embeddings only |
| Data | 3/10 — everything public |
| **Integration** | **8/10** — WHO API, FHIR conformance, OAuth flows |
| Deployment | 4/10 |
| Testing | 7/10 — conformance testing is the point |
| **Overall** | **6/10** |

**Overall Development Risk: MEDIUM** technically — but **HIGH presentation risk**, which is a different and more dangerous thing at a hackathon.

## 15. Team Requirements (5–6)

| Role | People | Responsibility |
|---|---|---|
| **FHIR/standards lead** | 1–2 | **Day 1:** read the R4 terminology module, build CodeSystem/ConceptMap generation and validation. This role is the project |
| Backend/integration | 1 | WHO ICD API client, caching, OAuth/Keycloak, audit |
| Frontend | 1–2 | Reference EMR client + curator console |
| Domain/medical | 1 | NAMASTE↔TM2 curation, equivalence types, clinical framing, demo narrative |

Note the unusual shape: **fewer frontend people and no ML person**, but one person who is comfortable reading a specification document for two days. If nobody on your team enjoys that, do not pick this statement.

## 16. Time Estimation

| Milestone | Effort |
|---|---|
| 24-hour prototype | NAMASTE ingest + CodeSystem + auto-complete + basic search UI. FHIR validity unlikely to be complete |
| 3-day prototype | Above + WHO API integration + curated ConceptMap + `$translate` + Bundle ingest |
| 1-week MVP | Above + OAuth/consent/audit + reference EMR client + validation passing |
| 2-week polished MVP | Above + curator console + versioning + analytics + CapabilityStatement + docs |
| Production-ready | 3–4 months, but with an unusually short gap: real ABDM onboarding, expert-curated full mapping (the long pole — clinical, not technical), security audit, EMR vendor pilots |

## 17. Cost

| Item | Cost |
|---|---|
| FastAPI / HAPI FHIR, PostgreSQL, Redis, Keycloak, React | ₹0 |
| WHO ICD-11 API | **₹0** — free with registration |
| NAMASTE terminology | ₹0 — published |
| Local embeddings | ₹0 |
| Hosting | ₹0 |
| **Total** | **≈ ₹0** — tied with PS 54 as the cheapest |

## 18. Security & Privacy — the strictest section in this report

This is healthcare. Treat every shortcut as disqualifying.

- **No real patient data, ever, at any stage.** All demo data synthetic. State this unprompted.
- **OAuth 2.0 with scoped access** aligned to ABHA token structure; short-lived tokens; no long-lived API keys.
- **Consent artefact per encounter**, stored, referenced from the record, and revocable — consent is a first-class resource, not a checkbox.
- **Immutable audit log** of every terminology access and every data write: who, what, when, for what purpose. Health audits require purpose, not just identity.
- **Encryption** in transit (TLS 1.3) and at rest; encrypted backups.
- **Data minimisation** — the terminology service does not need patient demographics to translate a code, so it should not receive them. Design the API so PHI never touches the terminology path.
- **RBAC/ABAC** aligned to ISO 22600 as the statement requires: practitioner, curator, administrator, vendor-integration.
- **No PHI to any LLM.** The embedding model touches terminology definitions only, and runs locally.
- **Versioned, attributable mappings** — a clinical decision made under v1 must remain explicable after v2.
- **Prompt-injection surface is minimal** by design, precisely because the LLM sees only terminology text; say so, because it demonstrates you thought about it.

## 19. Real-World Deployment

| Dimension | Prototype | Production |
|---|---|---|
| Auth | Local OAuth server mirroring ABHA | Real ABDM/ABHA onboarding, gateway registration, health-ID linkage |
| Mappings | 150–300 curated | Full terminology, curated by Ayush clinical experts — the long pole, and it's clinical work, not engineering |
| Hosting | Docker Compose | Government cloud / NIC, HA, DR — health data localisation applies |
| Compliance | Standards-aligned | Formal EHR Standards conformance, DPDP compliance, security audit, ABDM certification |
| Integration | Reference client | Pilot with real EMR vendors; a plain-REST adapter path for legacy systems |
| Versioning | Demonstrated | Governed release process synchronised with WHO ICD releases and NAMASTE updates |
| Support | — | Developer portal, sandbox, versioned API deprecation policy — you're serving developers, not end users |

**Note how short this gap is.** Of all eight statements, this has the smallest distance between the hackathon artefact and something deployable — which is a genuine argument in its favour and worth saying explicitly.

## 20. Score Calculation

| Criterion | Weight | Score | Reason |
|---|---|---|---|
| Problem Impact | 20 | **15** | Systemically important, but indirect — the beneficiaries are downstream of the API |
| Innovation Potential | 15 | **10** | Novel and rarely attempted, but "correctness" reads as less innovative than it is |
| Technical Feasibility | 15 | **12** | Achievable, with a steep specification learning curve |
| Low Dataset Dependency | 10 | **9** | Both terminologies public; WHO API free |
| Low Model Training | 10 | **10** | None |
| SIH Demo Potential | 10 | **5** | **The killer.** APIs and JSON don't perform on stage without deliberate effort |
| Scalability | 5 | **4** | A terminology service scales trivially |
| Real-world Deployment | 10 | **9** | The shortest prototype-to-production distance on this list |
| Team Skill Accessibility | 5 | **3** | Needs someone who will read the FHIR spec properly |
| **TOTAL** | **100** | **77** | |

## 21. Brutal Assessment

- **Genuinely difficult:** FHIR R4 conformance done properly, and semantically honest mapping between two different medical epistemologies.
- **Deceptively easy:** the search box. You will have auto-complete over NAMASTE terms in three hours and it will look like progress. It is 5% of the statement.
- **What could kill it:** the demo. This is the only statement on your list where a technically superior project can lose to a weaker one purely on presentation. Also: underestimating the FHIR learning curve and hand-rolling resources that fail validation on day six.
- **What could impress judges:** live FHIR validation, a live WHO API call, and honest `inexact` equivalence types — the last one signals genuine domain respect to any medical judge.
- **What could make judges reject it:** "FHIR-compliant" resources that are not; no working demo client; or a panel that never grasps why terminology mapping matters.
- **Worth choosing?** It is the most *professional* project on your list and the one most likely to actually be used. It is also the one most likely to be under-scored by a non-specialist panel.
- **Would I personally choose it?** **MAYBE.** Choose it if (a) someone on the team genuinely enjoys specifications, and (b) you accept that you are optimising for real-world value over stage impact. If you want to *win*, PS 65 or PS 70 gives you better odds.

---
---

# ⑧ PS 121 — AI/ML-based Auto-Evaluation of R&D Proposals at NaCCER, CMPDI Ranchi
**Organisation:** Ministry of Coal · **Category:** Software · **Theme:** Smart Automation
**Score: 66/100 · Recommendation: NO — drop this from your shortlist**

## 1. Problem Understanding

The Ministry of Coal funds research through a Science & Technology grant programme, administered via CMPDI, Ranchi, with the National Coal Research Centre involved in evaluation. Researchers and institutions submit proposals; a committee evaluates them for relevance to coal-sector priorities, technical merit, budget reasonableness, duplication with existing or past work, and the credibility of the proposing team. The process is slow, involves scarce expert time, and is inconsistent across evaluators.

The ask: automate a first-pass evaluation so expert committees see pre-screened, pre-scored proposals with the routine checks already done.

**Users:** CMPDI/NaCCER programme officers and evaluation committee members. **Beneficiaries:** researchers (faster decisions) and the coal sector (better-allocated research funding).

**Why it matters:** it matters, but modestly. The volume of proposals is small compared with the national schemes in PS 33 or PS 125, and the beneficiary population is narrow.

## 2. What the Statement REALLY Requires

**Mandatory:** ingest proposal documents; evaluate against defined criteria; score and rank; assist the committee's decision.
**Implied:** a defensible evaluation rubric grounded in the programme's actual criteria; duplication detection against past funded projects; budget reasonableness checks; explainability, because a rejected researcher may formally contest a decision; and human-in-the-loop, because peer review cannot be delegated to software.
**Optional:** reviewer assignment/matching, plagiarism detection, portfolio-gap analysis.

**Misunderstanding to avoid:** believing an LLM can assess *technical merit* in coal science. It cannot, and neither can you validate whether it did.

## 3. Proposed Solution

**Product concept:** a proposal triage and duplication-screening system, honestly scoped: it does the mechanical work — completeness, compliance, budget norms, duplication — and refuses to pretend it can judge scientific merit.

**Core modules:** document ingestion and extraction (PI, institution, objectives, methodology, budget heads, duration, deliverables); completeness and compliance checks against submission guidelines; **duplication detection via embedding similarity against a corpus of past and ongoing projects**; budget norm checking (head-wise limits, manpower/equipment ratios, cost per deliverable); relevance scoring against a published list of coal-sector research priorities; reviewer-matching by expertise embedding; a committee dashboard with side-by-side comparison; and an evaluation-note generator with cited evidence.

**Journey:** proposal uploaded → extracted → completeness and budget checks flagged → similarity search surfaces three related past projects with overlap highlighted → relevance mapped to stated priority areas → suitable reviewers suggested → committee reviews a pre-populated evaluation sheet and scores merit themselves.

## 4. AI/ML Requirement

**Classification: B — pretrained models and rules suffice. No training. But note that the most valuable component (duplication detection) is the one most dependent on unavailable data.**

| Component | Technique | Why |
|---|---|---|
| Extraction | LLM structured output | No labelled corpus |
| Completeness/compliance | Rule engine | Objective |
| Budget norms | Rules + arithmetic | Objective, and genuinely useful |
| **Duplication detection** | **Embeddings + similarity search over past proposals** | The single most valuable feature — and it needs a corpus you cannot obtain |
| Relevance to priorities | Embedding similarity to published priority areas + LLM justification | Reasonable |
| Reviewer matching | Embeddings over publications/expertise | Reasonable |
| Technical merit | **Nothing — do not attempt** | Neither an LLM nor your team can assess coal-science merit, and you cannot validate any score you produce |

## 5. Dataset Requirements — and why this statement fails your constraint

| Dataset | Why | Public? | Obtainable? | Synthetic? | Mock OK? |
|---|---|---|---|---|---|
| **Past R&D proposals submitted to the programme** | **Duplication detection — the core feature** | **No** | **No — these are confidential submissions** | Poorly (you cannot synthesise a realistic corpus of coal-research proposals) | Weakly |
| Past funded project abstracts | Duplication (partial substitute) | **Partly** — some project titles and abstracts appear in annual reports and CMPDI listings | Limited, thin | — | Partial |
| Coal-sector research priorities | Relevance scoring | Partly — some priority documents are published | Yes | — | Use real |
| Evaluation rubric | Scoring | Partly | Partly | — | Approximate |
| Budget norms | Budget checks | Partly | Partly | Yes | Yes |
| Historical funding decisions | Any predictive component | **No** | **No** | No | No |

**This is the disqualifying problem.** The feature with the highest value — telling a committee "this proposal substantially overlaps with a project you funded in 2019" — requires a corpus of past proposals that is confidential and that you have no path to obtaining. Synthesising it is not viable either: you cannot invent 500 plausible coal-research proposals with realistic technical overlap without domain expertise your team does not have.

Compare with PS 125, which has essentially the same architecture but where the equivalent dataset (project cost and schedule outcomes) **is public**. That single difference is why one scores 79 and the other 66.

**Dataset Risk: HIGH.**

## 6–7. Architecture & Stack (abbreviated — it mirrors PS 125)

The architecture is PS 125's with the risk model replaced by similarity search: Next.js frontend → FastAPI → parsing service, LLM extraction service, rules/scoring service, embedding similarity service → PostgreSQL + pgvector → Celery/Redis → object storage → audit log. Stack: Python/FastAPI, PyMuPDF, LLM API for extraction, `all-MiniLM` or `e5` embeddings locally, PostgreSQL with pgvector, React/Next.js, Docker Compose. Every technology choice justified for PS 125 applies here for the same reasons; nothing about this statement requires a distinct architecture, which is itself telling — **you would be building PS 125's system against a weaker dataset for a smaller audience.**

## 8. MVP for SIH

**MUST HAVE:** ingestion and extraction; completeness/compliance checks; budget norm validation; duplication similarity search against whatever corpus you can assemble; relevance mapping to published priority areas; committee dashboard with evidence citations.
**SHOULD HAVE:** reviewer matching; evaluation-note generation; side-by-side comparison; override with reason and audit.
**NICE TO HAVE:** portfolio-gap analysis; plagiarism checks; historical trend analytics.

## 9. Advanced Features

Duplication with highlighted overlapping passages; budget anomaly detection against norms; reviewer conflict-of-interest detection (same institution, recent co-authorship); portfolio-gap analysis showing which priority areas are under-funded; a transparent, editable rubric; and a deliberate, prominent **"merit is not scored by this system"** statement — which, handled confidently, converts your biggest limitation into evidence of judgement.

## 10. Innovation Analysis

Honest assessment: **low**. Duplication detection via embeddings is standard; rule-based compliance checking is standard; the reviewer-matching component is the most interesting piece and it is a small one. There is no equivalent here to PS 125's real-outcome risk model — no verifiable predictive component, and no dataset to build one on.

**What competitors will build:** exactly what you would build, and there will be fewer of them because few teams pick this statement. Low competition is the only strategic argument in its favour, and it is not enough.

## 11. SIH Demo Strategy (6 minutes, abbreviated)

Problem (proposal backlog, scarce expert time) → upload a proposal → extraction and compliance flags → **duplication hit against a past project with overlapping text highlighted** (the one genuinely satisfying moment) → budget anomaly flagged → relevance mapped to priority areas → reviewer suggestions with conflict-of-interest flags → committee sheet pre-populated → the honest closing statement that merit remains human.

**WOW moment:** the duplication hit — **which only lands if you have a credible corpus.** Without one, the demo has no peak, and that is the practical argument against choosing this statement.

## 12. Judge Questions (12, condensed)

| # | Question | Strong answer | Avoid |
|---|---|---|---|
| 1 | "Can AI really evaluate research merit?" | "No, and we don't claim it. We automate completeness, compliance, budget norms, duplication and reviewer matching. Merit stays with the committee. Overclaiming here would be indefensible." | "Our model scores technical merit." |
| 2 | "Where's your corpus of past proposals?" | *This is the question that ends the project.* The only honest answer: "We couldn't obtain one — they're confidential. We used published project titles and abstracts, which is a much thinner substitute." | Claiming a corpus you don't have. |
| 3 | "How accurate is duplication detection?" | "Embedding similarity with a human-reviewed threshold; we surface candidates with highlighted overlapping passages rather than making a call, and we report recall on a small hand-built test set." | "It catches all duplicates." |
| 4 | "What if you flag a legitimate follow-up study as duplicate?" | "We flag, we don't reject — with passages highlighted so the officer judges in seconds. Follow-on work is normal in research, and the system is explicitly a screening aid." | "Our threshold is tuned." |
| 5 | "Would researchers accept algorithmic screening?" | "They're screened on objective criteria only — completeness, budget norms, overlap — all of which are contestable with evidence. Nothing subjective is automated." | "It's more objective than humans." |
| 6 | "How does this differ from a plagiarism checker?" | "Semantic overlap rather than textual — it catches a proposal restating past work in new words, which a plagiarism checker misses. That's the useful part." | "It's similar." |
| 7 | "Confidentiality of proposals?" | "RBAC, encryption, audit, and an on-premise LLM path — unpublished research is commercially and academically sensitive, and a leak would be serious." | "It's just documents." |
| 8 | "Volume — how many proposals a year?" | The honest answer is *a modest number*, which invites "is automation worth it?" Best response: "Value is in consistency and expert-time savings, not throughput — but yes, this is a smaller-scale problem than a national scheme." | Inflating the volume. |
| 9 | "Prompt injection via proposals?" | "Proposals are untrusted external submissions — text is delimited, outputs schema-validated, and no extracted text influences scoring rules." | "Not a concern." |
| 10 | "Could this generalise beyond coal?" | "Yes — DST, DBT, ICMR and similar grant programmes share the structure. Frankly, the general version is more valuable than the coal-specific one." | Pretending coal specificity is a strength. |
| 11 | "What's your evaluation rubric based on?" | "Published programme guidelines where available; some criteria we had to approximate, and we say which." | Inventing weights silently. |
| 12 | "What's the weakest part?" | "The corpus. Duplication detection is the most valuable feature and the one we could least support with real data." | "Nothing." |

## 13. Failure Modes

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **No corpus for duplication** | **High** | **Fatal to the core feature** | Published abstracts only — a genuinely weak substitute |
| Rubric seen as arbitrary | High | High | Ground in published guidelines; be explicit about approximations |
| Judges object to AI evaluating research | Medium | High | Scope merit out loudly and early |
| Extraction failures on varied formats | Medium | Medium | Multiple parsers, confidence flags |
| Demo has no peak | **High** | High | No good mitigation — this is intrinsic |

## 14. Development Difficulty

Frontend 5 · Backend 6 · AI 5 · **Data 8** · Integration 4 · Deployment 3 · Testing 5 · **Overall 6/10**. **Overall Development Risk: MEDIUM technically, HIGH in outcome** — you can build it and still have nothing compelling to show.

## 15. Team Requirements

Same shape as PS 125 with 4–5 people: one document/backend, one embeddings/ML, two frontend, one domain. The domain role is harder here than in PS 125 because coal-sector research is genuinely specialised and the reference material is thin.

## 16. Time Estimation

24h: extraction + compliance checks. 3 days: + duplication + budget checks + dashboard. 1 week: + reviewer matching + note generation + overrides. 2 weeks: + analytics + polish. Production: 3–4 months, but blocked on CMPDI providing the historical corpus — which is an organisational decision, not an engineering task.

## 17. Cost

₹0 for open-source components and local embeddings; ₹300–1,000 in LLM API for extraction; ₹0 hosting. **Total ≈ ₹300–1,000.** Cost is not a differentiator here.

## 18. Security & Privacy

Unpublished research proposals are highly sensitive — they contain novel ideas before publication, and a leak could constitute research theft. Requirements: strict RBAC (committee members see only assigned proposals), conflict-of-interest enforcement in access control, encryption at rest and in transit, comprehensive audit, an on-premise LLM path (arguably mandatory — sending unpublished proposals to a third-party API is difficult to defend), retention limits, and prompt-injection defences since proposals are external submissions.

## 19. Real-World Deployment

Requires CMPDI to supply the historical proposal corpus (the blocker), formal approval of the rubric, on-premise deployment for confidentiality, integration with the existing submission process, committee training, and a defined appeal path for screened-out proposals. The prototype-to-production gap is dominated by an organisational data-sharing decision you cannot influence.

## 20. Score Calculation

| Criterion | Weight | Score | Reason |
|---|---|---|---|
| Problem Impact | 20 | **11** | Real but narrow — small proposal volume, specialised audience |
| Innovation Potential | 15 | **8** | Standard techniques; no verifiable predictive component |
| Technical Feasibility | 15 | **13** | Easy to build |
| Low Dataset Dependency | 10 | **5** | The core feature depends on a confidential corpus |
| Low Model Training | 10 | **9** | Pretrained only |
| SIH Demo Potential | 10 | **6** | No natural peak without a corpus |
| Scalability | 5 | **4** | Fine, but low volume makes scale moot |
| Real-world Deployment | 10 | **6** | Blocked on an organisational data decision |
| Team Skill Accessibility | 5 | **4** | Accessible, but the domain is obscure |
| **TOTAL** | **100** | **66** | |

## 21. Brutal Assessment

- **Genuinely difficult:** duplication detection without a corpus. That is not a hard problem; it is an impossible one under your constraints.
- **Deceptively easy:** the whole thing. You will build it comfortably and it will be unremarkable.
- **What could kill it:** the second judge question. "Where are the past proposals?" has no good answer.
- **What could impress judges:** honest scoping — refusing to score merit is genuinely mature. But maturity alone does not win hackathons.
- **What could make judges reject it:** claiming AI evaluation of research quality, or a duplication feature with nothing to compare against.
- **Is it worth choosing?** **No.** It is PS 125's architecture applied to a smaller problem with a worse dataset. If this problem shape appeals to you, choose PS 125 — you get the same skills, ten times the impact, and a public dataset that makes your central claim defensible.
- **Would I personally choose it?** **NO.** This is the clearest cut on your list.

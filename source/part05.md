---
---

# ④ PS 64 — Document Overload at Kochi Metro Rail Limited: an Automated Solution
**Organisation:** Government of Kerala (KMRL) · **Category:** Software · **Theme:** Smart Automation
**Score: 82/100 · Recommendation: YES — easiest to build, hardest to stand out**

## 1. Problem Understanding

KMRL runs on documents. Every day it receives engineering drawings, maintenance job cards, incident reports, vendor invoices and purchase orders, regulatory directives from the Commissioner of Metro Rail Safety and the Ministry of Housing & Urban Affairs, environmental impact studies, safety circulars, HR policies, legal opinions and board minutes. They arrive through incompatible channels — email attachments, SharePoint, WhatsApp PDFs from field staff, scanned paper, Maximo exports — and in **two languages, English and Malayalam, often mixed inside the same document**.

The statement names five consequences, and it is worth learning them because they are the vocabulary of your pitch:

1. **Information latency** — managers skim long documents to find the paragraph that concerns them, and decisions are delayed.
2. **Siloed awareness** — Engineering acts on a change that Procurement and HR only learn about weeks later, after the budget and rosters were already set.
3. **Compliance exposure** — a regulatory directive gets buried, a deadline passes, and the organisation is exposed during an audit.
4. **Knowledge attrition** — when staff move on, the institutional context behind decisions disappears with them.
5. **Duplicated effort** — multiple departments independently summarise the same document.

**Users:** department heads, engineers, procurement officers, HR, legal, and the compliance function. **Beneficiaries:** the whole organisation, and ultimately passengers, since safety directives that are read on time are safety directives that are acted on.

**Existing workflow:** documents land in an inbox or a shared drive; someone reads them; important ones get forwarded; nothing is indexed; search is Ctrl+F inside individual files.

**What success looks like:** rapid, trustworthy, *traceable* snapshots of long documents, delivered to exactly the people whose work they affect, searchable across the whole corpus in either language, with regulatory obligations tracked to their deadlines — and with every claim linked back to its source paragraph so nobody has to trust a summary blindly.

## 2. What the Statement REALLY Requires

**Mandatory**
- Ingest documents from heterogeneous channels and formats, including scans.
- Handle **English and Malayalam**, including mixed-language documents.
- Produce accurate summaries with **traceability to the source** — the statement is explicit that trust matters.
- Route information to the right roles/departments.
- Make the corpus searchable and reduce duplicated reading effort.

**Implied — the differentiators**
- **Role-aware, not one-size-fits-all summarisation.** The same tender document should yield a cost-and-terms summary for Procurement and a specifications summary for Engineering. This is the single best differentiating idea available in this statement.
- **Compliance obligations must become tracked objects with deadlines**, not sentences in a summary. Extract "submit X by DD/MM" into a task with an owner and an alert.
- **Cross-document linkage** — an invoice relates to a purchase order relates to a job card relates to a vendor contract. Building that graph turns a search tool into a knowledge base.
- **Contradiction and supersession detection** — circular of March supersedes circular of January; a system that flags this is doing something no one else will.
- **Trust must be engineered, not asserted** — citations, confidence signals, and an obvious path to the original page.
- **Access control at the document level.** Legal opinions and board minutes must not surface in an engineer's search results. Most teams will forget this entirely, and it is exactly what a government judge will ask about.
- **Scanned-document quality varies** — a WhatsApp photo of a printed circular is a realistic input, not an edge case.

**Optional:** drawing/CAD understanding, workflow approvals, mobile app, voice queries, integration with Maximo/SharePoint.

**Misunderstanding to avoid:** building a generic "chat with your PDF" app. That is the commodity outcome, and roughly two-thirds of teams choosing this statement will land there.

## 3. Proposed Solution

**Product concept:** *"KMRL DocuMind"* — a bilingual document intelligence layer that ingests everything, understands who each document affects, and delivers role-specific, cited briefings plus tracked compliance obligations.

**Core modules**
1. **Multi-channel Ingestion** — email connector (IMAP), folder/SharePoint watcher, WhatsApp-export importer, manual upload, Maximo export parser. Deduplication by content hash.
2. **Document Processing Pipeline** — file-type detection → text extraction (native PDF text where available) → **OCR fallback for scans, with Malayalam support** → layout/table extraction → language detection per block → chunking that respects section structure.
3. **Classification & Metadata Extraction** — document type (circular / invoice / job card / drawing / minutes / legal), issuing authority, dates, referenced document IDs, monetary values, deadlines, affected assets or stations.
4. **Role-Aware Summarisation** — for each department whose interests the document touches, generate a targeted summary answering that department's standing questions, every claim carrying a citation to page and paragraph.
5. **Routing Engine** — rules plus classification decide which roles receive which document, at what priority; notifications by email/in-app, with escalation on unread safety-critical items.
6. **Bilingual Search & RAG Q&A** — hybrid search (BM25 keyword + vector semantic) over both languages, so a Malayalam query retrieves relevant English documents and vice versa; answers cite sources and refuse when evidence is absent.
7. **Compliance Tracker** — extracted obligations become tracked items with deadline, owner, source citation and status; a calendar and an escalation ladder sit on top.
8. **Knowledge Graph** — entities (vendors, assets, stations, contracts, projects) and relations linking documents; visualised, and used to answer "show me everything about the Aluva escalator contract."
9. **Admin & Access Control** — document-level and category-level permissions, audit trail of every access.

**End-to-end journey:** a Malayalam safety circular arrives as a scanned PDF by email → OCR extracts it → classified as *Regulatory / Safety*, issuer CMRS, containing an obligation due in 14 days → Engineering and Safety receive role-specific summaries in English and Malayalam with citations → the obligation appears in the compliance tracker with an owner → three days before the deadline it escalates → six months later an auditor searches "escalator inspection" in Malayalam and finds it in two seconds with a full provenance trail.

**Inputs:** documents of any format, in either language, from any channel.
**Outputs:** role-specific cited summaries; routed notifications; searchable corpus; compliance obligations with deadlines; entity knowledge graph; audit trail.
**Dashboard:** inbox by role, compliance calendar with risk flags, document-volume analytics, unread safety-critical alerts, corpus coverage stats.

## 4. AI/ML Requirement

**Classification: B — pretrained models and APIs are entirely sufficient. No training.**

| Component | Technique | Why |
|---|---|---|
| OCR (English) | **Tesseract / PaddleOCR / docTR** | Mature, free |
| **OCR (Malayalam)** | **Tesseract `mal` + PaddleOCR; cloud OCR (Google Vision / Azure Document Intelligence) as the accuracy fallback** | This is your one real technical risk — see §5 |
| Layout & table extraction | **PyMuPDF, pdfplumber, Unstructured.io** | Free, effective on native PDFs |
| Language detection | **fastText / langdetect** | Trivial |
| Classification | **Zero/few-shot with an LLM**, upgraded to embedding-based k-NN once you have exemplars | No labelled corpus exists — zero-shot is the honest choice, and few-shot exemplars cost nothing |
| Embeddings | **Multilingual model — `multilingual-e5` or `LaBSE`** (both handle Malayalam) | Cross-lingual retrieval is the requirement; a monolingual English model would silently fail |
| Summarisation | **LLM API with role-specific prompts + enforced citations** | Exactly what LLMs are good at |
| RAG Q&A | **Hybrid retrieval (BM25 + vector) → reranking → grounded generation with refusal** | Hybrid beats pure vector on identifiers, dates and document numbers, which dominate this corpus |
| Entity/relation extraction | **LLM structured output + rules** | No training data |
| Contradiction/supersession | **Embedding similarity to find candidates + LLM comparison + explicit "supersedes" reference extraction** | Rare and impressive |

**Do NOT** fine-tune a summarisation model or train a document classifier from scratch — you have no labelled KMRL corpus, and zero-shot performance is already adequate. Be ready to say why fine-tuning would be worse: no data, no eval set, and no ability to update when document types change.

## 5. Dataset Requirements

| Dataset | Why | Public? | Obtainable? | Synthetic? | Mock OK? |
|---|---|---|---|---|---|
| KMRL internal documents | The corpus | **No** | **No** | Yes | Yes — but build them carefully |
| Regulatory circulars (CMRS/MoHUA/Kerala Govt) | Realistic regulatory inputs | **Yes — genuinely public** | Yes | — | **Use real ones** |
| Malayalam text/documents | Bilingual proof | **Yes** — Kerala government gazettes and circulars are published in Malayalam | Yes | — | **Use real ones** |
| Invoices / POs / job cards | Format variety | No | Templates are standard | Yes | Yes |
| Engineering drawings | Format variety | Partly | Sample CAD/PDF drawings exist publicly | — | Yes |
| Org chart / roles | Routing | No | Trivial to construct | Yes | Yes |

**Do this and you beat most teams instantly:** build the demo corpus from **real published Kerala government and metro-safety circulars in Malayalam and English**, mixed with synthetic invoices and job cards. Then print a few, photograph them at an angle with a phone, and feed those in. A demo that ingests a genuinely crooked phone photo of a genuine Malayalam circular and answers a question about it with a citation is worth more than any architecture slide.

**Biggest data risk: Malayalam OCR accuracy on poor scans.** Malayalam is a complex script with extensive conjunct characters, and open-source OCR degrades badly on low-quality images. **Mitigations:** (a) prefer native PDF text extraction whenever available — many government circulars are digital, not scanned; (b) use a cloud OCR fallback for scans and measure the difference openly; (c) display an OCR confidence score per document and flag low-confidence extractions for human verification rather than pretending they are fine. Judges reward measured honesty here far more than a claimed accuracy figure.

**Dataset Risk: LOW–MEDIUM** (low for corpus availability, medium for Malayalam OCR quality).

## 6. Technical Architecture

```
Dept Head / Engineer / Procurement / Legal / Compliance Officer
        |
        v
Next.js frontend
  |-- Role inbox (documents routed to me)
  |-- Document viewer with citation highlighting (side-by-side original + summary)
  |-- Bilingual search + RAG chat
  |-- Compliance calendar
  +-- Knowledge graph explorer
        |  HTTPS / JWT / RBAC
        v
FastAPI Gateway
        |
        +----------------+------------------+------------------+
        v                v                  v                  v
  Ingestion Svc    Processing Svc      Intelligence Svc    Compliance Svc
  (IMAP, folder,   (OCR, layout,       (classify, summarise (obligation
   upload, dedupe)  language detect,    per role, extract    extraction,
                    chunk)              entities, RAG)       deadlines, alerts)
        |                |                  |                  |
        v                v                  v                  v
   Object store    Celery + Redis      Qdrant / pgvector    PostgreSQL
   (MinIO/S3:      (async pipeline,    (multilingual        (metadata, roles,
    originals)      retry, DLQ)         embeddings)          obligations, audit)
                                              |
                                              v
                                        LLM API (summaries, extraction, RAG)
                                        + Cloud OCR fallback
        |
        v
  Notifications (email / in-app / SMS)  -  Audit log  -  Monitoring
```

**Notes**
- **The async pipeline is the backbone.** OCR + LLM calls on a 200-page document take minutes. Celery with retries and a dead-letter queue is not optional; a synchronous design will fail live.
- **Hybrid search, not vector-only.** This corpus is full of document numbers, dates and vendor names where BM25 outperforms embeddings. Combine and rerank.
- **A vector DB is genuinely justified here** (unlike in PS 65/70) — say so explicitly, because knowing *when* a vector DB is unnecessary is what makes its use here credible.
- **Document-level ACLs enforced at query time**, filtering before retrieval so restricted content never enters an LLM prompt for an unauthorised user. This is a real security property, not a UI check.

## 7. Recommended Tech Stack

| Layer | Choice | Why here |
|---|---|---|
| Frontend | **Next.js + TypeScript + Tailwind** | Document viewer, inbox, chat — heavy UI, fast iteration |
| PDF viewer | **PDF.js with a highlight overlay** | Citation highlighting is the trust mechanism; you need programmatic control |
| Backend | **Python + FastAPI** | The entire document/ML ecosystem is Python |
| Async | **Celery + Redis** | Long, failure-prone pipelines |
| OCR | **PaddleOCR / Tesseract (`eng`+`mal`)**, with **Google Vision or Azure Document Intelligence** as fallback | Free by default, accurate when it matters |
| Parsing | **PyMuPDF + pdfplumber + Unstructured.io** | Native text first — faster, cheaper, more accurate than OCR |
| Embeddings | **`multilingual-e5-base` or LaBSE, run locally** | Cross-lingual Malayalam↔English retrieval, zero per-call cost |
| Vector DB | **Qdrant** (or pgvector if you want one datastore) | Payload filtering for ACLs is first-class in Qdrant, which matters for permission-aware retrieval |
| Keyword search | **PostgreSQL full-text or OpenSearch** | Hybrid retrieval |
| LLM | **Claude API** — long context suits multi-page documents; strong at structured extraction and at citing | Summaries, extraction, RAG answers |
| Storage | **MinIO/S3** | Originals must be retained for provenance |
| Database | **PostgreSQL** | Metadata, obligations, RBAC, audit |
| Deploy | **Docker Compose** | ₹0 |

## 8. MVP for SIH

**MUST HAVE**
1. Multi-format ingestion (PDF native + scanned, DOCX, images) with dedupe.
2. OCR pipeline with **working Malayalam** and per-document confidence display.
3. Classification + metadata extraction (type, issuer, dates, references).
4. **Role-aware summarisation with citations** to page/paragraph.
5. Routing to roles + role inbox.
6. Hybrid bilingual search with **cross-lingual retrieval demonstrated** (Malayalam query → English document).
7. RAG Q&A with citations and explicit refusal when the corpus lacks an answer.

**SHOULD HAVE**
8. Compliance obligation extraction → deadline tracker with alerts.
9. Document-level access control with an audit trail.
10. Side-by-side viewer highlighting the exact cited passage in the original.
11. Cross-document linking (invoice ↔ PO ↔ job card).

**NICE TO HAVE**
12. Contradiction/supersession detection. 13. Knowledge graph visualisation. 14. Email/WhatsApp connectors live. 15. Mobile view. 16. Drawing/CAD metadata extraction.

**Finish before presenting:** MUST + 8, 9, 10. Item 10 (highlight the cited sentence in the original scan) is the cheapest trust-building feature in this entire report and takes half a day.

## 9. Advanced Features

- **Role-aware summarisation shown side by side** — the same document, three departments, three genuinely different summaries, on one screen. This is your strongest visual argument.
- **Citation highlighting into the original scan**, including for OCR'd Malayalam — visually striking and instantly credible.
- **Compliance obligations as tracked objects** with owners, deadlines and escalation. This converts a reading tool into a risk-management tool.
- **Supersession detection** — "This March circular supersedes clause 4 of the January circular you are currently following."
- **Confidence and provenance surfaces** — OCR confidence, retrieval confidence, and an explicit "insufficient evidence in the corpus" answer. Refusing to answer is a feature; demo it deliberately.
- **Permission-aware retrieval** — filter before retrieval so restricted documents cannot leak into a prompt.
- **Knowledge graph** over vendors, assets, stations and contracts.
- **Bilingual output** — summaries available in the reader's preferred language regardless of source language.
- **Zero-retention / on-premise LLM option** for sensitive categories, with the architecture supporting a locally hosted open-weight model.

## 10. Innovation Analysis

1. **Role-aware summarisation** rather than a single generic summary — the difference between a tool and a product.
2. **True cross-lingual retrieval**, demonstrated live in both directions.
3. **Obligations extracted into a tracked workflow with deadlines**, not left as prose.
4. **Provenance-first design** — every sentence traceable to a highlighted region of the original scan.
5. **Permission-aware RAG** — access control enforced inside retrieval, which almost no hackathon RAG app does.
6. **Supersession/contradiction detection** across the corpus.

**What competitors will build:** upload a PDF, chunk it, embed it, chat with it. Weaknesses: English-only (or Malayalam claimed but untested), no roles, no routing, no citations or fake ones, no access control, no compliance tracking, and no answer to "what if the model is wrong?"

**Be honest with yourself:** this statement has the lowest innovation ceiling of your top four, because the base pipeline is a solved commodity. Everything above is you *manufacturing* differentiation. That is achievable, but it means the pitch must foreground roles, citations, Malayalam and compliance from the first minute — never "we built a RAG system."

## 11. SIH Demo Strategy (8 minutes)

| # | Stage | Time | Screen | Say |
|---|---|---|---|---|
| 1 | Problem | 0:45 | A wall of mixed documents: Malayalam circular, invoice, drawing, WhatsApp PDF | "Thousands of pages a day, two languages, five channels, and one buried safety deadline." |
| 2 | Ingest | 0:45 | Drag in a **phone photo of a real Malayalam circular**, taken at an angle | "This is how documents actually arrive at KMRL." |
| 3 | Processing | 0:40 | Live pipeline: OCR (confidence 94%) → language: Malayalam → type: Safety Circular → issuer: CMRS → 1 obligation, due in 14 days | "Everything after this is grounded in what we extracted, and we show you how confident we were." |
| 4 | **WOW #1** | 1:20 | Same document, three role summaries side by side — Engineering, Procurement, Safety — each with different content, each sentence carrying a citation chip. Click a chip; the original scan opens with the exact Malayalam sentence highlighted | "One document. Three departments. Three different answers — and every one of them is traceable to the page it came from." |
| 5 | **WOW #2** | 1:00 | Type a query **in Malayalam**; results include English documents. Then ask a question the corpus cannot answer and show the system refuse | "Cross-lingual search, and a system that knows what it doesn't know." |
| 6 | Compliance | 1:00 | Compliance calendar; the obligation from stage 3 sits there with an owner and an escalation timer; show an overdue item escalating | "This is the failure mode that costs metros money — a deadline nobody read." |
| 7 | Security | 0:45 | Log in as an Engineer; the legal opinion is absent from search results *and* absent from the RAG context | "Access control is enforced inside retrieval, not just hidden in the UI." |
| 8 | Impact | 0:35 | Analytics: 1,240 documents, 96% auto-routed, average time-to-awareness 4h → 3min | — |

**WOW moment: stage 4 — three role-specific summaries with clickable citations that highlight Malayalam text in a photographed scan.** It hits language, roles and trust in one screen.

## 12. Judge Questions (15)

| # | Question | Testing | Strong answer | Avoid |
|---|---|---|---|---|
| 1 | "How is this different from ChatGPT with a PDF?" | The core risk | "Three ways. It's role-aware — the same document produces different summaries for Engineering and Procurement. It's permission-aware — access control is enforced inside retrieval, so restricted documents never enter a prompt. And it's obligation-aware — deadlines become tracked tasks with owners. A chat interface does none of that." | "We use RAG." |
| 2 | "How accurate is Malayalam OCR?" | Whether you tested honestly | "We measured it. On native digital PDFs we extract text directly, so accuracy is effectively 100%. On clean scans, open-source OCR gives us roughly 90–95% character accuracy; on poor phone photos it degrades, so we display per-document confidence and route low-confidence documents for human verification instead of pretending. A cloud OCR fallback closes most of the gap." | "It works fine." |
| 3 | "What if the LLM hallucinates a summary?" | The obvious attack | "Every sentence carries a citation, and clicking it highlights the source region in the original — a hallucinated claim has nowhere to point. We also constrain generation to retrieved context and return 'insufficient evidence' rather than guessing. We demo that refusal on purpose." | "We use a good model." |
| 4 | "A safety directive gets summarised wrong and someone gets hurt. Who's responsible?" | Governance maturity | "Which is why the system never replaces the document. Summaries are an index into the original, always one click away, and safety-critical categories require acknowledgement of the source document, not the summary. We reduce time-to-awareness; we don't remove the human from the loop." | "Our accuracy is high." |
| 5 | "Where does the data go? These are government documents." | Sovereignty | "In the prototype, to a commercial LLM API. For deployment, the architecture supports a locally hosted open-weight model on KMRL infrastructure for sensitive categories, with the same pipeline — because embeddings and OCR already run locally. Category-based routing decides what may leave the boundary." | "The API is secure." |
| 6 | "How do you handle 200-page engineering documents?" | Engineering realism | "Hierarchical processing — section-aware chunking, per-section summaries, then a synthesis pass, all asynchronous with retries. We use long-context models where a whole section must be reasoned over at once, and we cache aggressively because the same document is read by several departments." | "We split it into chunks." |
| 7 | "What about tables and drawings?" | Format realism | "Tables are extracted structurally with pdfplumber and preserved as tables, not flattened to text — critical for invoices and BOQs. Drawings are handled by metadata and title-block extraction; full CAD understanding is out of scope and we'd rather say so than overclaim." | Claiming drawing comprehension. |
| 8 | "Cost at KMRL's real volume?" | Economics | "Embeddings and OCR run locally at zero marginal cost. LLM cost is per new document, not per query, because summaries are generated once and cached — so cost scales with intake, not usage. At a few thousand pages a day that's a modest monthly figure, and an on-premise model removes it entirely." | "Cloud is cheap." |
| 9 | "Prompt injection — a vendor sends a PDF containing instructions." | Security depth | "A real attack, and we treat document text as untrusted data. It's delimited and never merged into the instruction section of a prompt; outputs are schema-validated; the model has no tools and no write access; and routing/permissions are decided by our code, never by anything the document says. Worst case is a bad summary, not a bad action." | "LLMs don't do that." |
| 10 | "How do you handle mixed-language documents?" | Domain detail | "Language detection runs per block, not per document, so a Malayalam circular with English annexures is handled correctly. Retrieval is cross-lingual via a multilingual embedding model, so the query language and the document language don't have to match." | "We translate everything to English." |
| 11 | "Who decides routing rules?" | Adoption | "KMRL does — routing is configurable rules over document type, issuer and extracted entities, editable by an administrator without a developer. Classification proposes; rules decide. That keeps it auditable." | "The AI decides." |
| 12 | "How does search stay fast at a million documents?" | Scale | "Hybrid retrieval with an ANN index; vector search is sub-linear, keyword search is inverted-index. The heavy work is at ingestion, which is asynchronous and horizontally scalable. Query-time cost is roughly flat in corpus size." | "It's fast now." |
| 13 | "What about existing systems — SharePoint, Maximo?" | Integration | "We're an intelligence layer, not a replacement — read-only connectors ingest from them and we link back to the source system. Not asking a government body to migrate its document repository is a major adoption advantage." | "They'd migrate to us." |
| 14 | "How do you evaluate summary quality without ground truth?" | Rigour | "We built a small human-annotated evaluation set from public circulars — key facts each summary must contain — and we measure fact recall and citation validity, which is checkable automatically: does every citation actually point at supporting text? Citation validity is the metric that matters most for trust." | "It looks good." |
| 15 | "What is the single biggest weakness?" | Self-awareness | "Malayalam OCR on poor-quality scans. We've mitigated it with native-text extraction, a cloud fallback and confidence flagging, but on a bad photograph of a degraded photocopy, we surface uncertainty rather than claim accuracy. We'd rather be honestly uncertain than confidently wrong." | "There isn't one." |

## 13. Failure Modes & Mitigations

| Failure | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Malayalam OCR poor on scans | **High** | High | Native text first; cloud fallback; confidence flags; human verification queue |
| Hallucinated summaries | Medium | Severe (safety) | Citation enforcement, retrieval grounding, refusal path, original always one click away |
| LLM API latency/outage on stage | Medium | High | Pre-processed demo corpus; cached summaries; local fallback model |
| Prompt injection via documents | Medium | High | Untrusted-data delimiting, schema validation, no tool access, code-side routing |
| Restricted documents leaking into answers | Medium | Severe | Pre-retrieval ACL filtering, tested explicitly |
| Cost blow-up on large corpora | Medium | Medium | Summarise once and cache; local embeddings; batch processing |
| Looks like every other RAG demo | **High** | High | Foreground roles, Malayalam, citations and compliance in the first 90 seconds |
| Pipeline failures on odd formats | High | Medium | Retries, dead-letter queue, visible per-document status |

## 14. Development Difficulty

| Dimension | Rating |
|---|---|
| Frontend | 7/10 — the citation-highlighting viewer is real work |
| Backend | 7/10 — async pipeline with retries |
| AI | 5/10 — all off-the-shelf, orchestration is the skill |
| Data | 5/10 — corpus assembly and Malayalam samples take time |
| Integration | 5/10 |
| Deployment | 4/10 |
| Testing | 6/10 — citation-validity checking |
| **Overall** | **6/10** |

**Overall Development Risk: MEDIUM** — the build risk is low, the *differentiation* risk is high. That is an unusual and dangerous profile: you will feel successful early and still lose.

## 15. Team Requirements (6)

| Role | People | Responsibility |
|---|---|---|
| Pipeline/backend | 2 | Ingestion, OCR, Celery orchestration, storage, connectors |
| AI/RAG | 1–2 | Chunking, embeddings, hybrid retrieval, prompts, citation enforcement, evaluation |
| Frontend | 2 | Document viewer with highlighting (one — this is a full job), inbox/search/compliance UI (one) |
| Domain/data | 1 | Corpus assembly, Malayalam samples, routing rules, evaluation set, demo script |

## 16. Time Estimation

| Milestone | Effort |
|---|---|
| 24-hour prototype | Ingest → extract → embed → search → summarise with citations. Very achievable |
| 3-day prototype | Above + Malayalam OCR + classification + role-aware summaries + role inbox |
| 1-week MVP | Above + compliance extraction + tracker + ACLs + citation-highlighting viewer |
| 2-week polished MVP | Above + cross-document linking + supersession detection + connectors + evaluation harness + deployment |
| Production-ready | 4–6 months: real connectors, on-prem model deployment, security clearance, retention policy, migration of the historical corpus |

## 17. Cost

| Item | Cost |
|---|---|
| Tesseract/PaddleOCR, multilingual embeddings (local), Qdrant, FastAPI, Next.js, Postgres, MinIO | ₹0 |
| LLM API (summaries + extraction, demo corpus of a few hundred documents) | ₹500–2,000 — the highest LLM cost of any statement here |
| Cloud OCR fallback (free tier covers ~1,000 pages/month) | ₹0 in demo |
| Hosting | ₹0 |
| **Total** | **≈ ₹500–2,000** |

Keep it low: pre-process the demo corpus once and cache every summary; never generate live on stage except for the one document you ingest theatrically.

## 18. Security & Privacy

**Sensitive content:** legal opinions, board minutes, vendor contracts and pricing, incident reports, personnel matters. This is the highest document-sensitivity of any statement on your list except PS 26.

- **Document-level and category-level ACLs, enforced pre-retrieval.** The retrieval query itself must be permission-filtered so restricted content cannot reach an LLM prompt for an unauthorised user. Demonstrate this.
- **RBAC** by department and seniority; separate handling for a "restricted" category that never leaves on-premise processing.
- **Encryption** at rest (originals in object storage) and in transit; signed, expiring URLs for document access.
- **Audit logging** of every document view, search and answer — who saw what, when. Government audits ask exactly this.
- **Prompt injection:** treat all document text as untrusted; delimit it, validate structured outputs against schemas, give the model no tools, and never let document content determine routing or permissions.
- **Data leakage to third-party LLMs:** classify before sending; restricted categories route to a locally hosted model. Make this a configuration, not a code change.
- **Retention:** defined lifecycle for originals and derived artefacts; deletion must cascade to embeddings, or you have a leak in your vector store — a subtle point that will impress a security-minded judge.

## 19. Real-World Deployment

| Dimension | Prototype | Production |
|---|---|---|
| Ingestion | Manual upload + a few connectors | Live IMAP/Exchange, SharePoint, Maximo, scanning stations, WhatsApp Business API |
| Corpus | A few hundred documents | Years of backlog — a migration project in its own right, with prioritised back-indexing |
| LLM | Commercial API | On-premise open-weight model for restricted categories; API for the rest, governed by classification |
| Security | RBAC + ACLs | Government SSO, CERT-In compliance, VAPT, DPDP-aligned retention, full audit |
| Infra | Docker Compose | Kerala state data centre or NIC cloud; GPU nodes if hosting a local model |
| Accuracy | Demo-level | Human-in-the-loop verification queue for low-confidence extractions; periodic sampling audits |
| Change management | — | Departments must trust summaries — expect a parallel-running period where originals are still circulated |
| Maintenance | — | Routing rules and document taxonomies evolve; they must stay configuration, not code |

## 20. Score Calculation

| Criterion | Weight | Score | Reason |
|---|---|---|---|
| Problem Impact | 20 | **15** | Real organisational pain with compliance and safety consequences; generalises to every PSU |
| Innovation Potential | 15 | **9** | Base pipeline is commodity; differentiation must be manufactured through roles, language and compliance |
| Technical Feasibility | 15 | **14** | Everything is off-the-shelf |
| Low Dataset Dependency | 10 | **9** | Public circulars + synthetic documents suffice |
| Low Model Training | 10 | **10** | None |
| SIH Demo Potential | 10 | **8** | Strong visuals, but a familiar genre to jaded judges |
| Scalability | 5 | **4** | Ingestion cost grows with corpus; query side scales well |
| Real-world Deployment | 10 | **8** | Highly deployable as a layer over existing systems |
| Team Skill Accessibility | 5 | **5** | Any competent full-stack team can execute |
| **TOTAL** | **100** | **82** | |

## 21. Brutal Assessment

- **Genuinely difficult:** Malayalam OCR on realistic scans, citation *validity* (not just citation display), and permission-aware retrieval done properly.
- **Deceptively easy:** the whole pipeline. You will have upload→summarise→chat working on day one and feel finished. You will not be finished; you will be identical to everyone else.
- **What could kill it:** commoditisation. If your demo opens with "we built a RAG system," the panel has already scored you. Second killer: Malayalam claimed but not actually working — judges from Kerala will test it in Malayalam.
- **What could impress judges:** three role-specific summaries side by side; a citation click that highlights Malayalam text inside a photographed scan; a compliance deadline escalating; and the refusal-to-answer moment.
- **What could make judges reject it:** hallucination with no traceability; no access control; English-only in practice.
- **Worth choosing?** Yes, if — and only if — the team commits to the differentiators rather than the pipeline. It is the highest-floor, lowest-ceiling option in your top four.
- **Would I personally choose it?** **MAYBE.** It is the safest to *build* and the hardest to *win* with. If your team's strength is full-stack execution and UI polish rather than algorithms, this is your best statement; otherwise PS 65 or PS 70 gives you more headroom.

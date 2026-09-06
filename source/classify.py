# -*- coding: utf-8 -*-
"""Classify all 105 software statements by ML-training intensity."""
import openpyxl, io, os, collections

# A = no AI needed (rules / optimisation / engineering / integration)
# B = pretrained models, APIs, RAG sufficient
# C = small classical ML on obtainable tabular data
# D = significant custom model training required
# E = training PLUS unobtainable data, or hardware / specialist science
CLS = {
1:("C","Outbreak prediction needs longitudinal health + water-quality data that is thin and partly sensor-dependent."),
2:("B","Geofencing rules + anomaly heuristics + a ledger. No training. Very heavily picked."),
4:("D","Fine-grained breed classification needs a large India-specific labelled cattle image corpus."),
5:("D","Same corpus problem as 4; coarser classes but still custom vision training."),
6:("A","Compliance workflow, rules and records. No ML anywhere in the core."),
7:("A","MRL/AMU thresholds are a rule engine over a livestock register."),
8:("A","Content, drills and scoring. No ML."),
9:("A","Gamification and content. No ML."),
10:("B","Advisory can be retrieval over public agri-advisories; yield claims are where teams overreach."),
11:("A","CRUD plus scheduling. No ML."),
12:("B","Pretrained face/QR recognition; the hard part is privacy, not modelling."),
13:("A","GTFS, GPS ingestion and ETA arithmetic. No ML needed."),
16:("B","Pretrained recognition plus analytics. Crowded and low-ceiling."),
17:("A","Directory, events, engagement. Pure CRUD."),
18:("A","Scheduling, records and low-bandwidth video. No ML."),
19:("A","Content delivery and offline sync. No ML."),
22:("A","Train precedence and crossing decisions are a pure constraint-programming problem. The statement itself names OR."),
23:("A","Panchakarma therapy scheduling is resource-constrained scheduling: therapists, rooms, protocol order."),
24:("A","Nutrient arithmetic against a food-composition table plus practice CRUD."),
26:("A","Terminology interoperability and FHIR conformance. Barely any AI at all."),
27:("A","Ledger, geotagging and custody events. No ML."),
28:("A","Timetabling = CP-SAT. Weaker, less specific sibling of 70."),
29:("B","OCR plus registry verification plus a ledger; optional forgery heuristics."),
30:("C","Small tabular model over public soil/rainfall/yield data; claims outrun the data fast."),
31:("B","Routing rules plus optional pretrained image tagging. Extremely crowded."),
32:("A","Content platform and itineraries. No ML."),
33:("B","Embeddings for skill semantics, then stable matching and constrained optimisation."),
34:("B","Recommendation sibling of 33 — strictly the weaker framing of the same problem."),
35:("B","Pretrained multilingual classification over posts, plus geospatial hotspotting."),
36:("D","eDNA / molecular biodiversity analysis is specialist bioinformatics, not app development."),
38:("C","Public district yield data supports a small tabular model; anything finer needs data you lack."),
39:("A","Ledger and custody events. No ML."),
42:("A","Content and gamification. No ML."),
43:("B","RAG over public health advisories. Commodity."),
44:("B","Pretrained detection on traffic video plus signal-timing optimisation; simulation is the safer core."),
46:("A","AR content and 3D assets. No ML."),
49:("B","Routing, rules, optional pretrained waste image tagging. Statement is vague."),
50:("A","Digitisation, 360 media, catalogue. No ML."),
54:("B","Pretrained segmentation for rooftops; the hydrology is deliberately deterministic."),
55:("B","RAG plus natural-language-to-query over the public INGRES groundwater database."),
56:("E","Rockfall prediction needs geotechnical sensor histories and slope monitoring you cannot obtain."),
58:("B","Pretrained pose estimation (MediaPipe/MoveNet) plus rule-based rep counting."),
59:("B","Retrieval over public advisories plus optional pretrained pest imagery."),
60:("A","Gamification and tracking. No ML."),
61:("B","RAG over Kisan Call Centre style advisory corpora."),
63:("E","Line-break detection is a signal-physics and hardware problem wearing a software label."),
64:("B","OCR, multilingual embeddings, RAG. Everything off the shelf."),
65:("A","Six-variable nightly assignment under conflicting objectives. CP-SAT, no training."),
66:("C","Trip-chain and mode inference from phone sensors needs a modest labelled set."),
67:("A","Health records, portability and consent. Standards work, not ML."),
70:("A","NEP timetabling at individual-student granularity. CP-SAT, zero data."),
71:("B","Screening instruments plus a guarded LLM layer. Sensitive, crowded."),
72:("A","Records platform. Pure CRUD."),
73:("B","Embeddings plus rules over a career taxonomy. Crowded."),
76:("E","Machine design. Not a software deliverable."),
77:("E","Revit/BIM coursework. Not software engineering."),
78:("E","Hyperspectral crop analytics needs hyperspectral capture and heavy training."),
79:("C","Road-network modelling with some learned components; MATLAB-centric and specialised."),
80:("A","Low-bandwidth classroom delivery. No ML."),
81:("C","Dropout prediction is a small tabular classifier; the data is synthetic or institutional."),
82:("A","ERP. Pure CRUD."),
83:("B","Translation and LLM APIs. Commodity."),
84:("A","Kolam grammar is computational geometry and L-systems. Elegant, tiny audience."),
85:("C","The MRV half needs remote-sensing analysis; the registry half is a ledger."),
92:("B","OCR on receipts plus rules; optional anomaly heuristics."),
93:("C","Credit scoring is a small tabular model, but the training data is exactly what you lack."),
94:("A","Gap analysis over Census / Mission Antyodaya style public data. GIS and rules."),
95:("A","Eligibility rules over a beneficiary register."),
96:("A","Registry and mapping. Pure CRUD."),
97:("A","Workflow and payment-rail integration. No ML."),
98:("B","Pretrained OCR plus transliteration. Small, cute, low impact."),
99:("E","Scope undefined; instrument-building, not software."),
100:("C","Feature-based classifier on public phishing corpora. Small and trainable."),
101:("D","A learned firewall needs labelled network traffic at scale and cannot be demoed honestly."),
102:("D","Research brief, not a buildable deliverable in hackathon time."),
103:("E","IC die imaging is proprietary and hardware-bound."),
104:("E","Systems research with no demonstrable hackathon artefact."),
105:("A","Swarm engagement is multi-agent algorithms plus simulation. No data, no training."),
106:("A","Crowd flow simulation plus darshan slot optimisation. Queueing theory, not ML."),
109:("B","Umbrella statement; whatever you build will be retrieval or rules."),
110:("E","Lunar SLAM and robotics. Simulation-heavy, far outside the constraint."),
111:("E","Explicitly asks you to extend a multimodal model. Training is the deliverable."),
112:("E","Super-resolution on thermal IR is deep-learning training from scratch."),
113:("D","End-to-end transformer WAF requires training on request corpora you cannot obtain."),
114:("B","RAG plus natural-language-to-query over security logs."),
115:("D","Fine-grained fish species recognition needs a labelled catch corpus."),
116:("B","Guarded LLM assistant. Buildable, but impossible to validate."),
117:("D","GNSS clock/ephemeris error modelling is specialist time-series geodesy."),
118:("E","Sensor fusion for autonomous navigation from phone-grade hardware."),
119:("D","Air-quality forecasting from satellite and reanalysis is heavy geoscience ML."),
120:("A","Post-quantum crypto integration. Zero AI, zero data, pure engineering."),
121:("B","Embeddings and rules — but the duplication corpus is confidential and unobtainable."),
123:("B","Portal, workflow and triage. Optional LLM classification."),
124:("A","End-to-end encrypted group messaging. Protocol engineering, no ML."),
125:("C","LLM extraction plus a small tabular overrun model on public project-outcome records."),
129:("E","DCRM waveform corpora are proprietary utility data."),
130:("E","FRA traces are proprietary utility data."),
131:("D","A substation digital twin needs SCADA histories and deep power-systems knowledge."),
132:("C","Same shape as 125: small tabular model, public project data possible."),
133:("C","Demand forecasting plus inventory optimisation; needs their consumption history."),
134:("B","Embeddings over competency frameworks. Low ceiling."),
135:("B","LLM classification and routing. Commodity."),
136:("B","UFDR parsing, pretrained NER, entity graph, natural-language querying. No training."),
138:("A","Framework and controls. Vague, closer to policy than product."),
139:("C","Hybrid generation sizing is optimisation plus small forecasting models."),
}

wb = openpyxl.load_workbook(r'C:\Users\manug\Downloads\Problem Statements.xlsx', data_only=True)
ws = wb['Sheet1']
rows = [r for r in ws.iter_rows(min_row=3, values_only=True) if r[0]]
sw = {int(r[0]): (str(r[1]).strip(), str(r[2]).strip(), str(r[4]).strip())
      for r in rows if str(r[3]).strip().lower() == 'software'}

missing = sorted(set(sw) - set(CLS))
extra = sorted(set(CLS) - set(sw))
assert not missing, f"unclassified: {missing}"
assert not extra, f"not software: {extra}"

counts = collections.Counter(CLS[n][0] for n in sw)
print("TOTAL SOFTWARE:", len(sw))
for c in "ABCDE":
    print(f"  Class {c}: {counts[c]:>3}")
print("  PASS (A/B/C):", counts['A']+counts['B']+counts['C'])
print("  CUT  (D/E)  :", counts['D']+counts['E'])

SHORT = {
 22:"Train section throughput", 65:"KMRL train induction", 70:"NEP timetable",
 136:"UFDR forensic analysis", 33:"PM internship allocation", 64:"KMRL documents",
 125:"DPR quality & risk", 54:"Rooftop rainwater", 26:"NAMASTE / ICD-11",
 35:"Ocean hazard reporting", 106:"Temple crowd management", 55:"INGRES chatbot",
 23:"Panchakarma scheduling", 124:"Secure group comms", 120:"Quantum-secure email",
 94:"Adarsh Gram gap analysis", 114:"Conversational SIEM", 105:"Drone swarm algorithm",
 84:"Kolam grammar", 121:"Coal R&D proposals",
}

def esc(s):
    return s.replace("|", "\\|").replace("&", "&amp;")

out = []
out.append("## The cut: 46 software statements that fail your constraint\n")
out.append("| PS | Class | Statement | Why it fails |")
out.append("|---|---|---|---|")
for n in sorted(sw):
    c, why = CLS[n]
    if c in "DE":
        title = sw[n][1]
        title = title[:78] + ("…" if len(title) > 78 else "")
        out.append(f"| **{n}** | {c} | {esc(title)} | {esc(why)} |")

out.append("\n\n## The survivors: 59 statements that pass\n")
for c, label in [("A", "Class A — no AI/ML required at all"),
                 ("B", "Class B — pretrained models, APIs or RAG are sufficient"),
                 ("C", "Class C — a small classical model on obtainable tabular data")]:
    out.append(f"\n### {label}\n")
    out.append("| PS | Statement | Note |")
    out.append("|---|---|---|")
    for n in sorted(sw):
        if CLS[n][0] != c:
            continue
        title = sw[n][1]
        title = title[:76] + ("…" if len(title) > 76 else "")
        out.append(f"| **{n}** | {esc(title)} | {esc(CLS[n][1])} |")

io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen_tables.md"),
        "w", encoding="utf-8").write("\n".join(out))
print("\nwrote screen_tables.md")

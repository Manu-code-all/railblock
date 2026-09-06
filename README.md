# RailBlock

**SIH2026027 · Automatic Block Planning for Indian Railways**
Team **Anomaly** · Galgotias University

Three maintenance departments — Engineering (P.Way), Signalling & Telecom, and
Traction (OHE) — all need traffic-free "blocks" on the same railway sections
to do their work. Planned by hand, requests clash, windows go to waste, and
when something genuinely can't fit, nobody can say exactly why.

RailBlock takes every department's requests and the corridor's timetable and
uses **Google OR-Tools' CP-SAT constraint solver** to return one conflict-free
plan it *proves* is optimal — or, when the requests genuinely can't all fit,
the exact, irreducible set that's fighting, with the arithmetic. No machine
learning, no historical data: there isn't a dataset to train on, and a
proof beats a prediction for a safety-adjacent scheduling problem.

## What's in this repo

| | |
|---|---|
| [`prototype/`](prototype/) | The working system — CP-SAT solver, SQLite persistence, and two interfaces: the original Streamlit app and a React frontend. **Start here to run it.** |
| [`docs/`](docs/) | The five planning documents — problem, architecture, security, frontend spec, feature tickets. |
| [`team/`](team/) | Prep packages for the four non-coding team members (domain rules, real corridor data, pitch, testing). |
| [`deck/`](deck/) | The submitted SIH idea-presentation deck. |
| [`video/`](video/) | The MVP video script and final export. |
| [`HANDOFF.md`](HANDOFF.md) | Full project handoff — team, decisions, bugs fixed, open items. |

## Run it

```bash
cd prototype
pip install -r requirements.txt
python -m railblock.seed
streamlit run app.py
```

That's the original interface. For the newer React frontend instead, run the
API (`python -m uvicorn api.main:app --port 8001`) and `prototype/web`
(`npm install && npm run dev`) side by side — see
[`prototype/web/README.md`](prototype/web/README.md). Both interfaces read
and write the same database.

See [`prototype/README.md`](prototype/README.md) for the full walkthrough —
loading real corridor data, running the test suite, and the terminal CLI.

## Status

The engine and both interfaces are complete (tickets T01–T21, T26, T27 —
solver, persistence, submission, solving, explanation, conflict resolution,
publishing, export, activity log, a React frontend, and real login with
server-side authorisation). What's left is reserved on purpose for the team's
technical member to finish live on the internal hackathon day: hardening,
adding a couple of extra domain rules, deploying, and fixing anything the
test pass turns up. Full detail in
[`docs/05-feature-tickets.md`](docs/05-feature-tickets.md).

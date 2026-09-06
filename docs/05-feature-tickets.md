# 05 · Feature Ticket List

**RailBlock** · Version 1.2 · 6 September 2026
Internal hackathon: **7 September**

> **Technical member:** the tickets marked **`SUNDAY`** are yours. Everything
> above them should be working when you arrive. Read
> `02-technical-architecture.md` first — twenty minutes, and it will save you an
> hour of reading code.

Priority: **P0** demo breaks without it · **P1** materially better · **P2** nice to have.

---

## DONE — built and tested

| # | Ticket | Notes |
|---|---|---|
| T01 | CP-SAT constraint model — sections, windows, durations, deadlines, crews | `model.py`, 17 tests |
| T02 | Independent verification of a finished plan | `verify()` |
| T03 | Minimal conflict extraction via deletion filter | CP-SAT's own answer was not minimal |
| T04 | Priority slider — urgency vs train-path protection | Measurable: 7 days/0 daytime windows → 2 days/6 |
| T05 | Gantt rendering with windows behind blocks | `chart.py` |
| T06 | Terminal interface | `cli.py` |
| T07 | Three demo scenarios incl. an irreducible 3-way conflict | `scenarios.py` |
| T08 | **SQLite persistence** — requests, plans, blocks, activity | `store.py` |
| T09 | **`to_scenario()`** — database into the solver, solver unchanged | The only coupling point |
| T10 | **Database seeder** | `python -m railblock.seed` |
| T11 | **Explanation engine** — why is this block here | `explain.py` |
| T12 | Role selector and department view | Streamlit sidebar picker; superseded in the React app by real login (T26) |
| T13 | Submit a request form | Validation per `04-frontend-specification.md` §3.1 |
| T14 | Controller plan view | Result strip, Gantt, verification banner — every value computed, none hard-coded |
| T15 | **CSV import for corridor and requests** | `railblock/load.py` — per-row validation, names file/row/fix |
| T16 | **Explanation panel in the UI** | Pick a block, see reasons and the windows considered |
| T17 | **Conflict view with defer-and-resolve** | Names the irreducible set, defers and re-solves without leaving the screen |
| T18 | Publish and view block orders | Publishing marks requests `planned`, order visible from department view |
| T19 | Export the block order | CSV, grouped by day and section |
| T20 | Activity log page | Newest first, filterable by actor |
| T21 | Empty and error states | Every state in §4 of the frontend spec |
| T26 | **React frontend** (`web/` + `api/`) | Full feature parity with the Streamlit app, built for presentation quality — see `web/README.md` |
| T27 | **Real login, server-side authorisation, login rate limiting** | Replaces the role dropdown in the React app; see `03-security-and-access.md` |

The Streamlit app (`app.py`) and the React app (`web/`) both still work, read
and write the same database, and can be run side by side — the React app is
what gets demoed; Streamlit is the fallback if anything about the newer app
doesn't hold up.

---

## SUNDAY — technical member

### T22 · `SUNDAY` · Review and harden · **P0**
Read the architecture doc, then look hardest at:
- The objective weights in `model.py` — are urgency and uptime balanced sensibly?
- The `store.py` schema — anything that will bite us mid-demo?
- Caching — Streamlit's `st.cache_data`, and the React app's client-side
  re-fetch after every mutation. Is anything stale after a write, in either app?
- The auth model (`api/main.py`) — demo-scale on purpose (§1 of the security
  doc); is there anything there that would embarrass us if a judge tried it?

*Deliverable: a short list of what you changed and why, for the Q&A.*

### T23 · `SUNDAY` · Add the top domain rules · **P1**
Member 1's worksheet (`team/1-domain/rules-worksheet.md`) ends with the top three
missing rules. Add whichever are tractable, **with a test each**.

Most likely candidate: adjacent-section clearance — forbid concurrent blocks on
neighbouring sections. It extends the existing `AddNoOverlap` pattern.

*Done when:* the new constraint has a test, and `verify()` checks it too.

### T24 · `SUNDAY` · Deploy · **P2**
The React app (`web/`) plus the FastAPI backend (`api/`), anywhere with a URL —
that's the one to put in front of judges. Streamlit Community Cloud remains the
fallback if the two-service deploy costs too much time. A judge opening it on
their own phone is worth more than any slide.

*If it costs more than an hour, drop it and demo locally.*

### T25 · `SUNDAY` · Fix from the bug log · **P0**
`team/4-test/bug-log.md`. Demo-breaking first.

---

## Order of work

**Wed 3 Sep – Sat 6 Sep** — T01 through T21 built and verified, then, once the
Streamlit UI wasn't presentation-quality, T26 (React frontend) and T27 (real
login) on top. Everything above this line is done.
**Sun 7 Sep** — T22, T25, T23, T24 in that order

## If time runs out

Cut in this order: **T24** (deploy) → **T20** (activity page) → **T19** (export)
→ **T23** (extra rules).

**Never cut T16 or T17.** The explanation and the conflict resolution are the two
things no other team will have, and they are why we got this far.

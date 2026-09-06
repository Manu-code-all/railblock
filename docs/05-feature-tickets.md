# 05 · Feature Ticket List

**RailBlock** · Version 1.0 · 3 September 2026
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

---

## TO BUILD BEFORE SUNDAY — Manu, with help

### T12 · Role selector and department view · **P0**
Sidebar role picker; each department sees only its own requests.

*Done when:* switching role changes the list; a department cannot see another's
requests; the choice survives navigation.

### T13 · Submit a request form · **P0**
Per `04-frontend-specification.md` §3.1, with the validation listed there.

*Done when:* a submitted request persists across a restart, appears for the
controller, and is written to the activity log.

### T14 · Controller plan view · **P0**
All requests, Solve, result strip, Gantt, verification banner.

*Done when:* result strip shows solver status, block count, measured solve time
and `verify()` violations — every value computed, none hard-coded.

### T15 · CSV import for corridor and requests · **P0**
Reads `sections.csv`, `windows.csv`, `requests.csv` in the format Member 2 is
filling in (`team/2-data/`). `windows.csv` uses a repeating-day format
(`days = 0-6`) that expands to individual windows.

*Blocks Member 2's package — build this early.*

*Done when:* `python -m railblock.load team/2-data/corridor-1` replaces the
corridor, and the app runs on it with no code change.

### T16 · Explanation panel in the UI · **P1**
Surface `explain.py` — pick a block, see reasons and the windows considered.

*Done when:* every scheduled block explains itself and the reasoning matches the
chart.

### T17 · Conflict view with defer-and-resolve · **P1**
Per §3.3. Name the conflicting requests, show the arithmetic, allow deferring one
and re-solving in place.

*Done when:* the overloaded corridor names exactly its irreducible set, and
deferring one produces a valid plan without leaving the screen.

### T18 · Publish and view block orders · **P1**
Publish a draft; departments see the live order filtered to them.

*Done when:* publishing marks its requests `planned` and the order is visible
from a department view.

### T19 · Export the block order · **P1**
CSV download, grouped by day and section.

### T20 · Activity log page · **P2**
Newest first, filterable by actor.

### T21 · Empty and error states · **P1**
Every state in §4 of the frontend spec. No bare tracebacks.

---

## SUNDAY — technical member

### T22 · `SUNDAY` · Review and harden · **P0**
Read the architecture doc, then look hardest at:
- The objective weights in `model.py` — are urgency and uptime balanced sensibly?
- The `store.py` schema — anything that will bite us mid-demo?
- Streamlit caching — is anything stale after a write?

*Deliverable: a short list of what you changed and why, for the Q&A.*

### T23 · `SUNDAY` · Add the top domain rules · **P1**
Member 1's worksheet (`team/1-domain/rules-worksheet.md`) ends with the top three
missing rules. Add whichever are tractable, **with a test each**.

Most likely candidate: adjacent-section clearance — forbid concurrent blocks on
neighbouring sections. It extends the existing `AddNoOverlap` pattern.

*Done when:* the new constraint has a test, and `verify()` checks it too.

### T24 · `SUNDAY` · Deploy · **P2**
Streamlit Community Cloud, or anything with a URL. A judge opening it on their
own phone is worth more than any slide.

*If it costs more than an hour, drop it and demo locally.*

### T25 · `SUNDAY` · Fix from the bug log · **P0**
`team/4-test/bug-log.md`. Demo-breaking first.

---

## Order of work

**Wed 3 Sep** — T15 first (unblocks Member 2), then T12
**Thu 4 Sep** — T13, T14
**Fri 5 Sep** — T16, T17, then load Member 2's real corridor
**Sat 6 Sep** — T18, T19, T21, freeze, rehearse, brief the technical member
**Sun 7 Sep** — T22, T25, T23, T24 in that order

## If time runs out

Cut in this order: **T24** (deploy) → **T20** (activity page) → **T19** (export)
→ **T23** (extra rules).

**Never cut T16 or T17.** The explanation and the conflict resolution are the two
things no other team will have, and they are why we got this far.

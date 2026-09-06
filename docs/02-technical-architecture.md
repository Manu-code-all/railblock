# 02 · Technical Architecture

**RailBlock** · Version 1.1 · 6 September 2026

> **If you are the technical member arriving on hackathon day, read this file
> first, then `05-feature-tickets.md`. Everything else is background.**

**There are two frontends now, both talking to the same solver and the same
database.** The Streamlit app (`app.py`) is what §1 below was originally
written for, and it still works. Once the demo needed to look presentation-
ready, a second interface was built: a React + TypeScript app (`prototype/web/`)
behind a FastAPI backend (`prototype/api/main.py`) that wraps the exact same
`railblock` package — `model.py` and `store.py` did not change for it. **The
React app is what gets demoed**; Streamlit is the fallback. See
`prototype/web/README.md` for that stack specifically; everything below still
describes the shared engine underneath both.

---

## 1. Shape of the system

```
   Department accounts             Section controller
   (login required)                       │
            │                             │
            ▼                             ▼
   ┌──────────────────────┐   ┌──────────────────────┐
   │  React app (web/)     │   │  Streamlit (app.py)  │   presentation
   │  — what gets demoed   │   │  — fallback           │
   └──────────────────────┘   └──────────────────────┘
            │                             │
            ▼                             │
   ┌──────────────────────┐               │
   │  FastAPI (api/)       │               │
   │  login · sessions     │◀── both call ─┘
   │  server-side authz    │
   └──────────────────────┘
            │                             │
            ▼                             ▼
   ┌────────────────┐            ┌──────────────────┐
   │   store.py     │◀──────────▶│    explain.py    │   application
   │  (SQLite)      │            │  (reasoning)     │
   └────────────────┘            └──────────────────┘
            │                             ▲
            │  to_scenario()              │
            ▼                             │
   ┌──────────────────────────────────────────────┐
   │        model.py — CP-SAT solver              │   domain
   │        solve() · verify() · conflict         │
   └──────────────────────────────────────────────┘
                        │
                        ▼
              Google OR-Tools CP-SAT
```

Three layers, and the important property is that **the domain layer knows
nothing about the database or the UI**. `model.py` takes a `Scenario` dataclass
and returns a `Solution`. It was written before the database existed and did not
change when the database — or the second frontend, or the login system — was
added. Both `app.py` and `api/main.py` are consumers of the same `railblock`
package; neither is privileged, and the domain layer cannot tell which one
called it.

## 2. Modules

| File | Responsibility | Status |
|---|---|---|
| `railblock/model.py` | Constraint model, `solve()`, `verify()`, minimal-conflict extraction | Stable — 17 tests |
| `railblock/scenarios.py` | Three built-in demo scenarios | Stable |
| `railblock/chart.py` | Gantt rendering (matplotlib, no UI dependency) | Stable |
| `railblock/cli.py` | Terminal interface | Stable |
| `railblock/store.py` | SQLite persistence, `to_scenario()` bridge | New, tested |
| `railblock/seed.py` | Populate the database from a scenario | New, tested |
| `railblock/explain.py` | Why is this block here | New, tested |
| `railblock/load.py` | CSV import for a real corridor, row-level validation | Stable |
| `app.py` | Streamlit UI — fallback interface | Stable, full feature parity |
| `api/main.py` | FastAPI layer over `railblock` — login, sessions, every JSON endpoint the React app calls | Stable |
| `web/` | React + TypeScript + Tailwind UI — what gets demoed | Stable, full feature parity |
| `test_railblock.py` | 17 checks over the solver | Passing |

## 3. The solver — the part that matters

**Decision variables.** For each request: a boolean "is it scheduled", an
integer start time, and one boolean per candidate window ("is it in this one").

**Constraints.**
- The block sits wholly inside exactly one traffic-free window on its section
- `AddNoOverlap` over all intervals on each section
- `AddCumulative` per department, capacity = crew count
- End time ≤ end of the deadline day

**Objective.** Maximise `10000 × priority × scheduled`, so placing work always
dominates. Two smaller terms then decide *how* the accepted work is placed:
urgency (penalise finishing an urgent job late) and uptime (penalise spending
disruptive daytime windows). A slider from 0.0 to 1.0 moves weight between them.

### Two modes

- **optimise** — every request optional. Always returns a plan; drops what does
  not fit.
- **strict** — every request mandatory via CP-SAT *assumption literals*. If
  infeasible, we recover which assumptions caused it.

### The conflict minimisation — do not remove this

`SufficientAssumptionsForInfeasibility()` returns *a* sufficient set, which in
practice was **every request in the batch**. Technically correct, operationally
useless.

`_minimal_conflict()` runs a deletion filter: drop each request in turn, re-solve
with the rest forced, and if it is still infeasible that request was never part
of the problem. What survives is irreducible — remove any single member and the
plan solves.

This is the single most important piece of logic in the project. The demo's best
moment depends on it entirely.

### Verification

`verify()` re-walks the finished plan and re-tests every rule from scratch —
independent of the solver. It exists so that no one has to take the solver's
word for it, and the UI reports its result as "rule violations".

## 4. Data model

SQLite, file at `prototype/railblock.db`. Plain `sqlite3` from the standard
library — no ORM, no extra dependency.

| Table | Holds |
|---|---|
| `sections` | Track sections — id, name |
| `windows` | Traffic-free windows — section, start, end, disruption cost |
| `requests` | Block requests — dept, section, title, duration, priority, deadline, status, submitter |
| `plans` | A solve result — solver status, timing, urgency, draft/published, conflict list |
| `plan_blocks` | The blocks in a plan — request, section, start, end, window |
| `activity` | Append-only audit log — timestamp, actor, action, detail |

**Time representation:** minutes from Monday 00:00. Day *n* spans
`n×1440` to `(n+1)×1440`. There is no calendar-date handling anywhere, which is
deliberate — a planning horizon is relative, and dates would add timezone
problems for no demo value.

**Request status:** `pending` → `planned` (when a plan is published) or
`deferred` (when the controller drops it to resolve a conflict). Deferred
requests are excluded from the next solve.

## 5. The bridge

```python
scenario = store.to_scenario(days=7)      # database  → dataclasses
solution = solve(scenario, urgency=0.5)   # dataclasses → plan
problems = verify(scenario, solution)     # independent re-check
pid      = store.save_plan(solution, ...) # plan → database
```

`to_scenario()` is the only coupling point between storage and the solver. If
you change the schema, that function is what has to keep working — nothing in
`model.py` should ever import `store`.

## 6. Key decisions and why

| Decision | Reason |
|---|---|
| CP-SAT, no ML | Produces a proof. No training data, no accuracy to defend, no drift. |
| SQLite, no ORM | One file, zero setup, inspectable with any viewer. A learner can read every query. |
| Streamlit, not React | Four days. The engine is the differentiator; UI framework work buys nothing here. |
| Minutes-from-Monday | Avoids all date and timezone handling. |
| Solver never imports storage | Keeps the domain testable in isolation — all 17 tests run without a database. |
| Deletion filter for conflicts | CP-SAT's own answer was not minimal. See §3. |
| `verify()` duplicates the rules | On purpose. An independent check is worth the duplication. |

## 7. Known limitations

- **In the React app**, roles require a real login (hashed passwords, server-
  issued sessions, server-side authorisation) — but the accounts are a
  handful of shared demo logins, not individual staff identities. **In the
  Streamlit fallback**, roles are still selected from a dropdown, not
  authenticated at all. See `03-security-and-access.md` for exactly where
  each stands.
- Single corridor at a time; no multi-division support.
- No live railway system integration; corridor data comes from CSV or the seeder.
- Block durations are given, never estimated.
- Streamlit re-runs the whole script on every interaction; solves are cached with
  `st.cache_data` keyed on `(scenario, strict, urgency)`.

## 8. Running it

```
cd prototype
pip install -r requirements.txt
python -m railblock.seed        # corridor + 18 requests + 4 demo accounts
```

**The React app (what gets demoed)** — two processes:

```
python -m uvicorn api.main:app --port 8001     # terminal 1
cd web && npm install && npm run dev            # terminal 2
```

Login with `controller` / `railblock2026` (or any of the three department
accounts — see `web/README.md`).

**The Streamlit fallback:**

```
streamlit run app.py
```

```
pytest                                    # 17 checks
python -m railblock.cli B                # solve in the terminal
python -m railblock.cli C --strict       # the conflict answer
```

## 9. Where to extend

| You want to | Go to |
|---|---|
| Add a railway rule | `model.py` — `_build()`, then add a test |
| Change what drives the plan | `model.py` — the objective section |
| Add a screen (React) | `web/src/views/`, wire it into `App.tsx` |
| Add a screen (Streamlit fallback) | `app.py` / `pages/` |
| Add or change an API endpoint | `api/main.py` — reuses `store.py`/`model.py`, never duplicates their logic |
| Change what is stored | `store.py` — `SCHEMA` and `to_scenario()` |
| Improve the reasoning shown | `explain.py` |
| Change the chart | `chart.py` (Streamlit) or `web/src/components/Gantt.tsx` (React) |

**Rule of thumb:** if a change makes `model.py` import anything from `store.py`,
Streamlit, or `api/main.py`, it is the wrong change.

# 04 · Frontend Specification

**RailBlock** · Version 1.0 · 3 September 2026
Streamlit multi-page app. This is the spec the UI is built to.

---

## 1. Principles

**One question per screen.** A department planner asks "what have I asked for?"
A controller asks "does this plan work, and why?" Do not merge them.

**Every claim on screen must be verifiable.** "Proven optimal" appears only when
the solver returns `OPTIMAL`. "0 rule violations" comes from `verify()`, not from
assuming success. Never print a number the system did not compute.

**Never state a solve time in words.** The figure varies run to run; show the
measured value and let it speak.

**Degrade honestly.** If a solve fails, say what failed and what to do next.
Never a blank screen or a stack trace.

## 2. Global layout

**Sidebar** — always visible:
- Role selector: `Engineering (P.Way)` · `Signalling & Telecom` · `Traction (OHE)` · `Section controller`
- Corridor name and planning horizon
- Live counts: pending requests, published plan number

**Main area** — the current page.

**Theme** — pinned light in `.streamlit/config.toml` so it renders identically on
any machine, with Streamlit's Deploy button and menu hidden. Do not remove that
file; it is what keeps the demo consistent on a borrowed laptop.

**Palette** — matches the submitted deck:

| | Hex |
|---|---|
| Navy (primary) | `#1F3864` |
| Engineering | `#2E6DA4` |
| Signalling & Telecom | `#1E8449` |
| Traction | `#CA8A04` |
| Traffic-free window | `#E8EDF3` |
| Good / verified | `#1E8449` |
| Conflict / error | `#C0392B` |

Department colours are used consistently in the Gantt, in tables and in badges.
A viewer should learn them once.

## 3. Screens

### 3.1 Department view — *"My requests"*
**Who:** the three department roles.

**Shows**
- Their own requests only, newest first: id, work, section, duration, priority, deadline, status
- Status as a coloured badge: `pending` grey · `planned` green · `deferred` amber
- The published block order filtered to their department, if one exists

**Actions**
- **Submit a request** — form: section (dropdown, from database), work title (text), duration in minutes (number, 30–480), priority (1–5), deadline day (0 to horizon−1)
- **Withdraw** — only while `pending`

**Validation**
- Title required, trimmed, max 80 characters
- Duration a multiple of 15, within bounds
- Deadline within the horizon
- Warn, but allow, if no window on that section is long enough — the explanation screen will then say exactly why it could not be placed

**On submit:** confirmation naming the new id, list refreshes, activity logged.

### 3.2 Controller view — *"Plan the corridor"*
**Who:** section controller. The primary screen.

**Shows**
- All pending requests, grouped by department, with a count per department
- Result strip once solved: **Result** · **Blocks scheduled** · **Solved in** · **Rule violations**
- The Gantt: sections down the side, time across, blocks coloured by department, traffic-free windows as pale bands behind them
- Verification banner: green when `verify()` returns clean, listing what was re-checked; red with the specific violations otherwise

**Controls**
- **Priority slider** 0.00–1.00, labelled `◀ protect service` / `clear urgent ▶`
- **Every request is mandatory** toggle — strict mode
- **Solve** and **Publish block order**

**Behaviour**
- Solving is cached on `(corridor, requests, strict, urgency)` so moving the slider back and forth is instant
- Publishing marks the plan live and its requests `planned`, and is confirmed before it happens

### 3.3 Conflict view
Replaces the Gantt when strict mode returns infeasible.

**Shows**
- **No valid plan** · number of requests in conflict · time to prove it
- The explanation in plain words, with the arithmetic: *"All 3 need Phulera – Jaipur. Together that is 270 minutes, but the longest window available to them is 240."*
- A row per conflicting request: id, work, department, section, duration, priority
- A note that these are irreducible — deferring any one makes the rest solvable

**Actions**
- **Defer** on each row → marks it `deferred`, excludes it from the next solve, re-solves in place

This is the strongest sequence in the demo. It must not be buried behind a tab.

### 3.4 Explanation panel
Reached by picking a block from the plan.

**Shows**
- Headline: *"R004 runs day 0, 13:00–15:00 on Bandikui – Alwar"*
- The reasons, as a list — why that window, what fixed the start time, how much
  slack before the deadline, whether a daytime window was spent
- **Windows considered** — every window on that section with a verdict:
  `chosen` · `was also possible` · `only 0 min free — held by R010` ·
  `opens after the day-3 deadline` · `only 180 min long, the job needs 210`

Every line is derived from the plan by `explain.py`. Nothing is templated
optimism — if the reasoning cannot be established, the panel says so.

### 3.5 Block orders
**Shows** the published plan grouped by day and section: time, department,
section, work, request id.

**Actions** — export as CSV; export as a printable order.

### 3.6 Activity log
Append-only, newest first: timestamp, actor, action, detail. Filterable by
actor. This is the auditability story, so it should look plain and factual.

## 4. Empty, loading and error states

| State | Show |
|---|---|
| No corridor loaded | "No corridor loaded. Run `python -m railblock.seed`, or import a corridor from CSV." |
| No requests yet | "No requests yet. Departments submit from their own view." |
| Solving | Spinner with "Solving…" — solves are sub-second, so no progress bar |
| Solver failed | The exception message, plus what to try next. Never a bare traceback. |
| No published plan | "No block order published yet." |

## 5. Accessibility and demo robustness

- Colour is never the only signal — department is always also written in text,
  and status badges carry a word, not just a colour
- Readable at 1280×720, since that is the recording and projection size
- Everything reachable in **at most two clicks from the sidebar** — a judge
  should never watch someone hunt for a screen
- No horizontal scrolling on the main area at 1280 wide

## 6. Out of scope

Real login screens, user management, mobile layout, dark theme, animation,
multi-language. None of it is being scored on 7 September.

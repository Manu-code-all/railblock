# 01 · Product Requirements Document

**RailBlock — Automatic Block Planning for Indian Railways**
Team Anomaly · Galgotias University · SIH 2026 · PS SIH2026027
Version 1.0 · 3 September 2026 · Internal hackathon 7 September 2026

---

## 1. The problem

Indian Railways takes track out of service to maintain it. Three departments
need those possessions:

| Department | Code | Work |
|---|---|---|
| Engineering (P.Way) | `ENGG` | Track, ballast, welds, level crossings |
| Signalling & Telecom | `S&T` | Point machines, axle counters, interlocking |
| Traction (OHE) | `TRD` | Overhead wires, masts, feeders |

Each department raises its block requests **independently**, with no visibility
of the others. The consequences are routine:

- Two departments book the same section on the same night. One is cancelled on
  the morning — after the crew has already travelled to site.
- Approved traffic-free windows go unused because nobody matched work to them.
- Maintenance slips, track health degrades, trains are delayed anyway.

This is not a forecasting problem. Every input is known in advance. It is a
**coordination problem**, and it is currently solved by hand, department by
department, on spreadsheets.

## 2. What we are building

A single planner that ingests all three departments' requests plus the corridor
timetable and returns **one conflict-free block schedule that is provably
optimal** under the stated constraints. When the requests genuinely cannot all
fit, it returns the **minimal set of requests that are in conflict** rather than
an unhelpful "no solution".

**Non-goal, stated deliberately:** we train no machine-learning model and use no
historical data. Constraint programming produces a proof, not a prediction. That
is the product decision the whole system rests on.

## 3. Users

| User | Needs to |
|---|---|
| **Department planner** (×3) | Submit block requests, see their status, withdraw one |
| **Section controller** | See all requests, generate a plan, understand why it looks that way, resolve conflicts, publish the block order |
| **Field supervisor** *(read-only)* | Read the published block order for their section |

The controller is the primary user. Everything else feeds them or consumes their
output.

## 4. App flow — start to finish

1. **Log in.** A department account or the controller account, from the
   landing page (React app) or a role picker (Streamlit fallback).
2. **A department submits a request** — section, work, duration, priority,
   deadline day — and sees it appear immediately with a `pending` status.
3. **The controller solves the corridor.** One action. CP-SAT returns a
   schedule in well under a second, shown as a Gantt chart with an
   independent verification banner.
4. **If everything can't fit**, switching on "every request is mandatory"
   shows the exact irreducible conflicting set with the arithmetic, and a
   **Defer** button that re-solves in place without leaving the screen.
5. **Any block can explain itself** — pick a request, see which windows were
   considered and why the others were ruled out.
6. **The controller publishes.** The plan becomes the live block order.
   Departments immediately see their own slice of it; the order exports as
   CSV.
7. **Every step above is on the record** — an append-only, filterable
   activity log ties each action to the account that took it.

## 5. Functional requirements

### Must have — the system is not credible without these

| # | Requirement |
|---|---|
| F1 | A department planner can submit a request: section, work title, duration, priority, deadline |
| F2 | Requests persist across restarts |
| F3 | The controller sees all requests from all three departments in one place |
| F4 | The controller can generate a plan, and the system states whether it is proven optimal |
| F5 | The plan is shown as a Gantt chart, coloured by department, with the traffic-free windows visible |
| F6 | The system independently re-verifies its own plan against every rule and reports violations |
| F7 | When no plan exists, the system names the minimal conflicting set and explains the arithmetic |
| F8 | For any scheduled block, the system explains why it is at that time, in that window |
| F9 | The controller can publish a plan; it becomes the live block order |
| F10 | Every action is written to an activity log with actor and timestamp |

### Should have

| # | Requirement |
|---|---|
| F11 | Corridor and requests can be loaded from CSV, so real data replaces demo data |
| F12 | The published block order exports as a file a department could actually receive |
| F13 | A priority control trades finishing urgent work sooner against protecting train paths |
| F14 | On conflict, the controller can defer one of the named requests and re-solve in place |

### Out of scope for 7 September — say so plainly if asked

- Live integration with TMS, BDMS, SMMS or the real eBlock system
- Individual staff identities — the React app has real login and server-side
  authorisation, but against a handful of shared demo accounts, not a real
  staff directory (see `03-security-and-access.md`)
- Multi-division or network-wide planning
- Estimating block durations from history
- Mobile app for field staff

## 6. Constraints the solver enforces

| Constraint | Meaning |
|---|---|
| Section exclusivity | One department may hold a track section at a time |
| Window containment | A block must sit wholly inside one traffic-free window on its own section |
| Duration | Each request has a fixed length in minutes |
| Deadline | Each request must finish by the end of its stated day |
| Crew capacity | A department cannot run more concurrent blocks than it has crews |
| Priority weighting | 1 routine … 5 safety-critical; decides what is dropped when not everything fits |
| Disruption cost | Daytime windows cost train paths; night windows do not |

Member 1's rules worksheet (`team/1-domain/`) identifies which real Block
Working rules we do **not** yet model. The top three from that list are the
first candidates for extension.

## 7. Success criteria for the internal round

1. A judge can submit a request and watch it appear in the controller's plan.
2. The system says **proven optimal** and reports **zero rule violations**.
3. A judge can pick any block and get a truthful explanation of why it is there.
4. The overloaded corridor names its three conflicting requests with the
   arithmetic, and deferring one produces a valid plan.
5. Real corridor data from public timetables, not invented data.
6. Nothing is claimed that is not built.

## 8. What makes this defensible

Most entries produce an answer and a confidence score. Ours produces a **proof**.
When a judge asks "how do you know this is right?", the answer is not "our model
scored 94%" — it is "the solver proved no better schedule exists, and here is a
separate checker that re-tested the finished plan against every rule from
scratch."

The conflict explanation is the second differentiator. "These three requests need
270 minutes of a 240-minute window — defer any one" is something a controller can
act on. "No feasible solution" is not.

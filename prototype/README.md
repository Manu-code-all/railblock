# RailBlock — working prototype

Automatic Block Planning for Indian Railways · SIH 2026 · PS SIH2026027
Team **Anomaly**, Galgotias University

Three maintenance departments — Engineering, S&T and Traction — each ask for
possession of track sections. Today they ask independently, so blocks clash and
windows go to waste. RailBlock takes all three departments' demands plus the
timetable and returns **one conflict-free plan that the solver proves is
optimal** — or, when the demands genuinely cannot all fit, the exact set of
requests that are fighting.

No model training. No historical data. Google OR-Tools CP-SAT.

---

## Setup

```
pip install -r requirements.txt
```

## Run the demo

```
streamlit run app.py
```

Opens at `http://localhost:8501`. Pick a scenario in the sidebar, drag the
priority slider, watch the corridor re-plan.

## Run it in the terminal

```
python -m railblock.cli A              # small division
python -m railblock.cli B              # full corridor
python -m railblock.cli C --strict     # the conflict answer
python -m railblock.cli B --urgency 1.0
```

## Run the checks

```
python test_railblock.py
```

17 checks. Every claim the demo makes is asserted here — that the plan breaks
no rule, that the slider is a real trade-off, that the conflict set is minimal
and that deferring any one member of it makes the plan solvable.

---

## The three scenarios

| | Scenario | What it shows |
|---|---|---|
| **A** | Jaipur division, 3 sections, 8 requests, 5 days | The basic plan. Everything fits. Solves in ~40 ms. |
| **B** | Jaipur–Gurgaon corridor, 6 sections, 18 requests, 7 days | It scales. Still proven optimal, ~120 ms. |
| **C** | One section, one night, three urgent jobs | **The conflict answer.** Turn on "every request is mandatory". |

Scenario C is built so that the clash is genuinely three-way: SEC-A has a
single 240-minute window and R01, R02, R03 each need 90 minutes. *Any two fit.*
All three need 270 and cannot. So no pair is the problem — the solver has to
identify the trio, and it does, while correctly leaving the two unrelated
requests on SEC-B out of the answer.

---

## What the solver actually does

**Decides** — for each request, whether to schedule it and when to start.

**Subject to** — the block must sit wholly inside one traffic-free window on
its own section; no two blocks may hold the same section at once; each
department has a limited number of crews; each request has a deadline.

**Maximising** — the weighted value of the work scheduled, then, as a
tie-break, the balance the planner chose with the slider.

The slider is not decoration. On scenario B:

| Priority slider | Days used | Disruptive daytime windows |
|---|---|---|
| Protect service (0.0) | 7 | 0 |
| Balanced (0.5) | 3 | 2 |
| Clear urgent work (1.0) | 2 | 6 |

Both ends produce fully valid plans. The slider decides *which* valid plan —
finish sooner by spending daytime paths, or protect train service and take
the whole week.

---

## Why it proves rather than predicts

A trained model gives you an answer and an accuracy figure you have to defend.
CP-SAT returns `OPTIMAL`, which means it has proved no better plan exists
under the stated constraints. When no plan exists, it proves that instead —
and `SufficientAssumptionsForInfeasibility` plus a deletion filter turns
"infeasible" into "these three requests, and here is the arithmetic".

That distinction is the whole pitch: an operations controller can act on
*"R01, R02 and R03 need 270 minutes of a 240-minute window — defer one"*.
Nobody can act on *"87% confidence"*.

`verify()` re-checks the solver's own output from scratch against every rule,
so the demo never asks anyone to take the solver's word for it.

---

## Layout

```
prototype/
├── app.py                  Streamlit demo
├── test_railblock.py       17 checks
├── requirements.txt
└── railblock/
    ├── model.py            constraint model, solve(), verify(), conflict minimisation
    ├── scenarios.py        the three demo scenarios
    ├── chart.py            Gantt rendering
    └── cli.py              terminal interface
```

---

## Not built yet

Honest scope, so nothing here is oversold:

- No connection to live TMS / BDMS / SMMS — scenarios are parameterised, which
  the problem statement supports since it enumerates its own inputs.
- Single-user local app; no auth, no persistence, no multi-division rollout.
- Block durations are given, not estimated from history.

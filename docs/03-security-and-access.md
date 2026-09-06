# 03 · Security & Access

**RailBlock** · Version 1.0 · 3 September 2026

This document exists for two reasons. Judges evaluating a system for a
government operator will ask how it is secured, and we should be able to answer
precisely rather than vaguely. And the honest answer — that this is a
demonstrator with role selection rather than authentication — is one we would
rather state ourselves than have found.

---

## 1. What is actually built

**Roles are selected, not enforced.** The user picks a role from a dropdown.
There are no accounts, no passwords, no sessions, no server-side authorisation.
Anyone with the URL can act as any department or as the controller.

| Control | Built | Reality |
|---|---|---|
| Authentication | No | No login exists |
| Authorisation | Partial | The UI hides actions by role; nothing enforces it |
| Audit logging | **Yes** | Every submission, solve and publish is recorded with actor and timestamp |
| Input validation | Partial | Form-level bounds on duration, priority, deadline |
| Transport security | No | Runs on `localhost` over HTTP |
| Data at rest | No | Unencrypted SQLite file |

The audit log is real and worth pointing at: every action is written to an
append-only table, so the plan can always be traced to who requested what and
who published it.

**Why we stopped there.** Four days, and authentication adds nothing a judge is
scoring. What matters is that we know exactly what is missing and can say how it
would be closed.

## 2. The roles, as designed

| Role | Can | Cannot |
|---|---|---|
| Department planner (ENGG / S&T / TRD) | Submit and withdraw their own requests; view published block orders | See or edit another department's requests; generate or publish plans |
| Section controller | View all requests; generate plans; defer requests; publish block orders | Submit requests on a department's behalf |
| Field supervisor | Read the published block order | Anything else |

The separation is enforced in the UI only. On a real deployment it would move
server-side.

## 3. What production would require

Ordered as we would actually build it.

**1 — Authentication.** Integrate with Indian Railways' existing directory
rather than inventing accounts. Railway staff already have identities; a new
credential store would be both a burden and a liability.

**2 — Server-side authorisation.** Every action re-checked against the caller's
role at the API boundary, not in the interface. The current UI-only separation is
convenience, not security.

**3 — Transport and storage.** HTTPS throughout; PostgreSQL with encryption at
rest, replacing the SQLite file.

**4 — Tamper-evident audit.** The log already captures the right events. Making
it append-only at the database level, with retention rules, would make it
evidential — which matters if a block order is ever disputed after an incident.

**5 — Integration security.** Any link to TMS, BDMS or SMMS is read-only,
authenticated service-to-service, over the railways' own network. A planning tool
should never be able to write into an operational safety system.

## 4. Safety boundary — the important one

RailBlock is a **planning aid, not a safety system**. It proposes a schedule that
a human controller reviews and publishes. It does not authorise possession, does
not communicate with signalling, and cannot place track into or out of service.

That boundary is deliberate and should stay. Block authorisation is a safety-of-
line function with its own established procedure, and an optimiser has no
business inside it. The correct output of this system is a *proposed block
order*; a human still signs it.

If asked "what if the solver gets it wrong?" — the plan is verified
independently, every constraint is stated and auditable, and a controller
approves before anything is issued. Three layers, none of which is the model
being trusted.

## 5. Privacy

The system holds no personal data. Requests carry a department and a submitter
identifier (a role account such as `p.way.jaipur`), not individuals. Corridor
and timetable data is public. Nothing here would be subject to personal-data
protection rules, which is worth saying if asked.

## 6. If a judge asks

> **"How is this secured?"**
> Today it is a demonstrator: roles are selected rather than authenticated,
> because in four days that was not where the value was. What is real is the
> audit log — every request, solve and publication is recorded with who and when.
> For deployment the first step is authenticating against the railways' existing
> staff directory and moving authorisation server-side, and we would keep the
> system firmly on the planning side of the safety boundary — it proposes a block
> order, a controller still signs it.

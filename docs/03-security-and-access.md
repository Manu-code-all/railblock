# 03 · Security & Access

**RailBlock** · Version 1.1 · 6 September 2026

This document exists for two reasons. Judges evaluating a system for a
government operator will ask how it is secured, and we should be able to answer
precisely rather than vaguely. And the honest answer about exactly where our
security model stops is one we would rather state ourselves than have found.

---

## 1. What is actually built

**There is a real login**, added once the demo needed to show four separate
department portals rather than one shared screen with a role dropdown.
Accounts are real rows in the database — not hardcoded strings — and
passwords are never stored in the clear: each is hashed with PBKDF2-HMAC-SHA256
(200,000 iterations, a random salt per account, stdlib `hashlib` — no extra
dependency to risk installing the night before a demo). A successful login
issues an opaque session token; the client holds only that token, never the
password, and the token is what every subsequent request carries.

**Authorisation is enforced server-side, not just hidden in the UI.** The
department on a submitted request comes from the session that made the call,
not from anything the client claims — so logging in as Engineering makes it
impossible to submit, withdraw, or defer as another department, even by
calling the API directly rather than clicking through the interface. Solving,
deferring, and publishing are rejected with a 403 for anyone who isn't logged
in as the controller. This was verified directly against the API, not assumed.

| Control | Built | Reality |
|---|---|---|
| Authentication | **Yes** | Real accounts, hashed passwords, server-issued session tokens |
| Authorisation | **Yes, server-side** | Every mutating endpoint checks the session's role itself, not the client's claim |
| Brute-force protection | **Yes** | `/login` locks a username out for 60s after 5 failed attempts |
| Audit logging | **Yes** | Every submission, solve and publish is recorded with actor and timestamp |
| Input validation | Partial | Form-level bounds on duration, priority, deadline |
| Transport security | No | Runs on `localhost` over HTTP |
| Data at rest | No | Unencrypted SQLite file |

The audit log is real and worth pointing at: every action is written to an
append-only table, so the plan can always be traced to who requested what and
who published it — and now that action is tied to an authenticated account, not
just a self-reported name.

**Where this still falls short of production**, deliberately: the accounts are
a handful of shared demo logins we created for the demo (`p.way.jaipur`,
`snt.jaipur`, `ohe.jaipur`, `controller`), not individual staff identities;
there is no password reset flow, no 2FA, and no transport encryption (this
runs over plain HTTP on localhost). Two-factor authentication was left out on
purpose — with four shared demo accounts whose credentials are shown on the
login screen itself so any judge can try every role, an OTP step would add
friction without adding real protection. Those are the next things to close,
not gaps we've hidden.

**One more honest note on the session token.** It's held in the browser's
`localStorage`, which is simple and works regardless of how the frontend and
API end up deployed — but it means a cross-site-scripting bug anywhere on the
page could read it, where an `httpOnly` cookie could not. We chose
`localStorage` deliberately for the demo: cookies bring their own sharp edges
(domain and `SameSite` rules that are easy to get wrong under deployment
pressure), and this page has no third-party scripts or user-generated content
to make XSS a realistic risk tonight. It is the right next hardening step
before this ever left a demo, not before tomorrow.

## 2. The roles, as designed

| Role | Can | Cannot |
|---|---|---|
| Department planner (ENGG / S&T / TRD) | Submit and withdraw their own requests; view published block orders | See or edit another department's requests; generate or publish plans |
| Section controller | View all requests; generate plans; defer requests; publish block orders | Submit requests on a department's behalf |
| Field supervisor | Read the published block order | Anything else |

The department/controller split above is enforced server-side (§1). The field
supervisor role remains UI-only — it was never wired into the login system,
since a read-only viewer has nothing to protect against.

## 3. What production would require

Ordered as we would actually build it.

**1 — Real staff identities.** Replace our handful of demo accounts with
Indian Railways' existing directory. Railway staff already have identities;
a bespoke credential store for four shared logins is a demo convenience, not
something to carry into deployment.

**2 — Harden the session model further.** Login attempts are already rate-
limited; what's still missing is token expiry, moving the session token to an
`httpOnly` cookie, and individual accounts instead of one shared password per
role. What's built proves the *shape* of real authentication; production
needs its remaining edges hardened.

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
> There's a real login — hashed passwords, server-issued session tokens — and
> authorisation is enforced on the server, not just hidden in the interface: an
> Engineering account cannot submit, withdraw, or defer as another department,
> even by calling the API directly. What's demo-scale is the account list
> itself — a handful of shared logins we created, rather than individual staff
> identities — and there's no transport encryption yet since this runs on
> localhost. For deployment, the real step is swapping our demo accounts for
> the railways' existing staff directory and adding HTTPS. And regardless of
> any of that, we'd keep the system firmly on the planning side of the safety
> boundary — it proposes a block order, a controller still signs it.

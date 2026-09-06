# RailBlock — React frontend

A second, more polished interface for the same system. This does not replace
`app.py` (the Streamlit app) — both talk to the same database and the same
solver, and either can be used for the demo. This one exists because the
Streamlit look wasn't cutting it for presentation; `app.py` stays as the
proven fallback.

**Nothing about the solver or storage changed.** `api/main.py` is a thin
FastAPI layer over the existing `railblock` package — same `model.py`,
`store.py`, `explain.py`. This frontend just talks to that API over JSON
instead of Python calling Python in-process the way Streamlit does.

## Run it

Two processes, both from `prototype/`:

```bash
# Terminal 1 — the API (wraps railblock, same DB as app.py)
python -m uvicorn api.main:app --port 8001

# Terminal 2 — the frontend
cd web
npm install
npm run dev -- --port 5174
```

Open `http://localhost:5174`. If port 8001 or 5174 is already taken by
something else on your machine, change the port in `web/vite.config.ts`
(the `proxy` target) and in `api/main.py` (`allow_origins` in the CORS
middleware) to match.

The database must already be seeded — same as for the Streamlit app:

```bash
python -m railblock.seed
```

That also creates four demo accounts, one per department plus the controller,
all sharing the password `railblock2026` (printed by the seed command, and
shown on the login screen itself under "Demo accounts"):

| Username | Role |
|---|---|
| `p.way.jaipur` | Engineering (P.Way) |
| `snt.jaipur` | Signalling & Telecom |
| `ohe.jaipur` | Traction (OHE) |
| `controller` | Section controller |

## Login is real, not decorative

This isn't the Streamlit app's sidebar role-picker reskinned. Passwords are
hashed (PBKDF2-HMAC-SHA256, stdlib `hashlib`, no extra dependency) and a
successful login issues a session token that the client carries on every
request afterward. More importantly, **the server enforces it**: which
department a submitted request belongs to comes from the session that made
the call, not from anything the client claims, so an Engineering login cannot
submit, withdraw, or defer as another department even by calling the API
directly. Solving, deferring and publishing all require a controller session.
See [`docs/03-security-and-access.md`](../../docs/03-security-and-access.md)
for exactly where this model does and doesn't reach production-grade.

## Stack

- **Vite + React + TypeScript** — the app itself
- **Tailwind CSS v4** — styling, via `@tailwindcss/vite`
- **Framer Motion** — the tab-switch transition and animated underline
- **lucide-react** — icons

No component library was pulled in beyond that. A UI kit like Kokonut UI
distributes components through the shadcn CLI rather than as an npm package,
which means fetching from an external registry at build time — a fragile
dependency to add the night before a hackathon. Every component here is
hand-built with Tailwind instead, so there's nothing that can fail to
resolve on a borrowed laptop with a bad connection.

## Layout

```
web/src/
├── api.ts             typed fetch client — attaches the session token to
│                      every request, holds it in localStorage
├── types.ts           TS types mirroring the API's JSON shapes
├── App.tsx            session state, sidebar, the three controller tabs
├── components/
│   ├── Sidebar.tsx    signed-in identity + log out, no role picker
│   ├── Gantt.tsx       hand-drawn SVG timeline — no charting library
│   └── Pill.tsx        status badges, department tags
└── views/
    ├── Login.tsx       the landing page — username + password
    ├── DepartmentView.tsx
    ├── ControllerView.tsx   solve, conflict + defer, explain panel, publish
    ├── BlockOrders.tsx
    └── ActivityLog.tsx
```

Feature parity with the Streamlit app is complete: submit/withdraw, solve
(optimise or strict), the irreducible-conflict view with defer-and-resolve,
the explanation panel, publish, CSV export, and the activity log — now behind
a real login rather than a role dropdown.

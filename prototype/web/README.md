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
├── api.ts            typed fetch client for every endpoint in api/main.py
├── types.ts           TS types mirroring the API's JSON shapes
├── App.tsx             role state, sidebar, the three controller tabs
├── components/
│   ├── Sidebar.tsx
│   ├── Gantt.tsx       hand-drawn SVG timeline — no charting library
│   └── Pill.tsx        status badges, department tags
└── views/
    ├── DepartmentView.tsx
    ├── ControllerView.tsx   solve, conflict + defer, explain panel, publish
    ├── BlockOrders.tsx
    └── ActivityLog.tsx
```

Feature parity with the Streamlit app is complete: submit/withdraw, solve
(optimise or strict), the irreducible-conflict view with defer-and-resolve,
the explanation panel, publish, CSV export, and the activity log.

"""
RailBlock HTTP API.

A thin FastAPI layer over the existing `railblock` package — the solver
(model.py), storage (store.py) and explanation engine (explain.py) are used
exactly as they are for the Streamlit app. Nothing about them changes; this
just gives a React frontend something to talk to over JSON instead of
Python calling Python in-process.

    uvicorn api.main:app --reload --port 8000

Run from prototype/, same as the Streamlit app.
"""
from __future__ import annotations

import csv
import io
import time
from dataclasses import asdict
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from railblock import explain as explain_mod
from railblock import solve, store, verify
from railblock.model import DAY
from railblock.scenarios import DEPT_NAME, small_division

app = FastAPI(title="RailBlock API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    store.init_db()
    # Pay CP-SAT's one-time warm-up cost now, not on the first real request.
    solve(small_division(), time_limit=5.0)


def _horizon() -> int:
    ws = store.windows()
    return max((w.day for w in ws), default=6) + 1


def _section_name(sid: str) -> str:
    return next((s.name for s in store.sections() if s.id == sid), sid)


# ══════════════════════════════════════════════════════════════════
#  Auth — a real login, enforced server-side, not just hidden in the UI
#
#  The client holds an opaque bearer token, nothing else. Every mutating
#  endpoint below trusts the *session's* department, never one the client
#  claims in the request body — so logging in as Engineering makes it
#  impossible to submit, withdraw or defer as another department, even by
#  calling the API directly.
# ══════════════════════════════════════════════════════════════════
class LoginBody(BaseModel):
    username: str
    password: str


def current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Log in to continue.")
    user = store.get_session(authorization.removeprefix("Bearer ").strip())
    if not user:
        raise HTTPException(401, "Session expired — log in again.")
    return user


def require_controller(user: dict = Depends(current_user)) -> dict:
    if user["dept"] is not None:
        raise HTTPException(403, "Only the section controller can do this.")
    return user


def require_department(user: dict = Depends(current_user)) -> dict:
    if user["dept"] is None:
        raise HTTPException(403, "Departments only — the controller does not submit requests.")
    return user


_LOGIN_ATTEMPT_LIMIT = 5
_LOGIN_WINDOW_SECONDS = 60
_failed_logins: dict[str, list[float]] = {}


def _check_login_rate_limit(username: str) -> None:
    now = time.monotonic()
    recent = [t for t in _failed_logins.get(username, [])
             if now - t < _LOGIN_WINDOW_SECONDS]
    _failed_logins[username] = recent
    if len(recent) >= _LOGIN_ATTEMPT_LIMIT:
        raise HTTPException(
            429, f"Too many failed attempts for '{username}'. "
                 f"Wait a minute and try again.")


@app.post("/api/login")
def login(body: LoginBody):
    _check_login_rate_limit(body.username)
    user = store.verify_login(body.username, body.password)
    if not user:
        _failed_logins.setdefault(body.username, []).append(time.monotonic())
        raise HTTPException(401, "Wrong username or password.")
    _failed_logins.pop(body.username, None)
    token = store.create_session(user["username"])
    return {"token": token, **user}


@app.post("/api/logout")
def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        store.delete_session(authorization.removeprefix("Bearer ").strip())
    return {"ok": True}


@app.get("/api/me")
def me(user: dict = Depends(current_user)):
    return user


# ══════════════════════════════════════════════════════════════════
#  Requests / models
# ══════════════════════════════════════════════════════════════════
class NewRequest(BaseModel):
    section: str
    title: str
    duration: int
    priority: int
    deadline_day: int


class SolveParams(BaseModel):
    strict: bool = False
    urgency: float = 0.5


class ExplainParams(SolveParams):
    rid: str


# ══════════════════════════════════════════════════════════════════
#  Corridor / meta
# ══════════════════════════════════════════════════════════════════
@app.get("/api/windows")
def windows(user: dict = Depends(current_user)):
    return [asdict(w) for w in store.windows()]


@app.get("/api/meta")
def meta(user: dict = Depends(current_user)):
    sections = store.sections()
    windows = store.windows()
    pub = store.published_plan()
    return {
        "sections": [asdict(s) for s in sections],
        "sectionCount": len(sections),
        "windowCount": len(windows),
        "days": _horizon(),
        "pendingCount": len(store.list_requests(status="pending")),
        "published": pub,
    }


# ══════════════════════════════════════════════════════════════════
#  Requests
# ══════════════════════════════════════════════════════════════════
@app.get("/api/requests")
def list_requests(status: Optional[str] = None, user: dict = Depends(current_user)):
    # A department account only ever sees its own requests, enforced here —
    # not just hidden in the UI. The controller sees everything.
    dept = user["dept"]
    return store.list_requests(dept=dept, status=status)


@app.post("/api/requests")
def submit_request(body: NewRequest, user: dict = Depends(require_department)):
    if not body.title.strip():
        raise HTTPException(400, "Give the work a title.")
    if body.section not in {s.id for s in store.sections()}:
        raise HTTPException(400, f"'{body.section}' isn't a section in this corridor.")
    if body.duration <= 0:
        raise HTTPException(400, "Duration must be a positive number of minutes.")
    if not 1 <= body.priority <= 5:
        raise HTTPException(400, "Priority must be between 1 (routine) and 5 (safety-critical).")
    if body.deadline_day < 0:
        raise HTTPException(400, "Deadline day can't be before the corridor's first day.")
    windows = [w for w in store.windows() if w.section == body.section]
    longest = max((w.length for w in windows), default=0)
    rid = store.add_request(
        dept=user["dept"], section=body.section, title=body.title.strip(),
        duration=body.duration, priority=body.priority,
        deadline_day=body.deadline_day, submitted_by=user["username"])
    warning = None
    if longest < body.duration:
        warning = (f"No window on this section is longer than {longest} "
                   f"minutes, so it cannot be placed as it stands.")
    return {"id": rid, "warning": warning}


@app.delete("/api/requests/{rid}")
def withdraw_request(rid: str, user: dict = Depends(require_department)):
    row = next((r for r in store.list_requests(dept=user["dept"]) if r["id"] == rid), None)
    if row is None:
        raise HTTPException(404, "That request isn't yours to withdraw.")
    store.delete_request(rid, user["username"])
    return {"ok": True}


@app.post("/api/requests/{rid}/defer")
def defer_request(rid: str, user: dict = Depends(require_controller)):
    store.set_status([rid], "deferred", user["username"])
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════
#  Solving
# ══════════════════════════════════════════════════════════════════
def _solve(params: SolveParams):
    days = _horizon()
    sc = store.to_scenario(days=days)
    sol = solve(sc, strict=params.strict, urgency=params.urgency)
    return sc, sol


def _solution_json(sc, sol):
    violations = verify(sc, sol) if sol.ok else []
    payload = {
        "status": sol.status,
        "ok": sol.ok,
        "provenOptimal": sol.proven_optimal,
        "blocks": [
            {**asdict(b), "sectionName": _section_name(b.section)}
            for b in sol.blocks
        ],
        "unscheduled": [
            {**asdict(sc.request(rid)),
             "sectionName": _section_name(sc.request(rid).section)}
            for rid in sol.unscheduled
        ],
        "conflict": [
            {**asdict(sc.request(rid)),
             "sectionName": _section_name(sc.request(rid).section),
             "deptName": DEPT_NAME.get(sc.request(rid).dept, sc.request(rid).dept)}
            for rid in sol.conflict
        ],
        "conflictText": None,
        "solveTimeMs": sol.solve_time * 1000,
        "violations": violations,
        "requestCount": len(sc.requests),
        "days": sc.days,
    }
    if not sol.ok:
        from railblock.model import explain_conflict
        payload["conflictText"] = explain_conflict(sc, sol.conflict)
    return payload


@app.post("/api/solve")
def run_solve(params: SolveParams, user: dict = Depends(require_controller)):
    sc, sol = _solve(params)
    if not sc.requests:
        raise HTTPException(409, "No requests to plan.")
    return _solution_json(sc, sol)


@app.post("/api/explain")
def run_explain(params: ExplainParams, user: dict = Depends(require_controller)):
    sc, sol = _solve(SolveParams(strict=params.strict, urgency=params.urgency))
    why = explain_mod.explain(sc, sol, params.rid)
    return {
        "request": why.request,
        "scheduled": why.scheduled,
        "headline": why.headline,
        "reasons": why.reasons,
        "alternatives": [asdict(a) for a in why.alternatives],
    }


# ══════════════════════════════════════════════════════════════════
#  Plans
# ══════════════════════════════════════════════════════════════════
@app.post("/api/plans")
def create_plan(params: SolveParams, user: dict = Depends(require_controller)):
    days = _horizon()
    sc = store.to_scenario(days=days)
    sol = solve(sc, strict=params.strict, urgency=params.urgency)
    if not sol.ok:
        raise HTTPException(409, "Solution is infeasible — cannot save a plan.")
    pid = store.save_plan(sol, days, params.urgency, params.strict, user["username"])
    return {"id": pid}


@app.post("/api/plans/{pid}/publish")
def publish_plan(pid: int, user: dict = Depends(require_controller)):
    try:
        store.publish_plan(pid, user["username"])
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {"ok": True}


@app.get("/api/plans/published")
def published(user: dict = Depends(current_user)):
    pub = store.published_plan()
    if not pub:
        return {"plan": None, "blocks": []}
    blocks = sorted(store.plan_blocks(pub["id"]),
                    key=lambda b: (b["start"], b["section"]))
    for b in blocks:
        b["sectionName"] = _section_name(b["section"])
        b["deptName"] = DEPT_NAME.get(b["dept"], b["dept"])
        b["day"] = b["start"] // DAY
    return {"plan": pub, "blocks": blocks}


@app.get("/api/export/csv")
def export_csv(user: dict = Depends(current_user)):
    pub = store.published_plan()
    if not pub:
        raise HTTPException(404, "No block order published yet.")
    blocks = sorted(store.plan_blocks(pub["id"]),
                    key=lambda b: (b["start"], b["section"]))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Day", "Time", "Section", "Department", "Work", "Request"])
    for b in blocks:
        s, e = b["start"] % DAY, b["end"] % DAY
        w.writerow([
            b["start"] // DAY, f"{s // 60:02d}:{s % 60:02d}-{e // 60:02d}:{e % 60:02d}",
            _section_name(b["section"]), DEPT_NAME.get(b["dept"], b["dept"]),
            b["title"], b["request_id"],
        ])
    buf.seek(0)
    return StreamingResponse(
        buf, media_type="text/csv",
        headers={"Content-Disposition":
                 f"attachment; filename=block_order_plan_{pub['id']}.csv"})


# ══════════════════════════════════════════════════════════════════
#  Activity
# ══════════════════════════════════════════════════════════════════
@app.get("/api/activity")
def activity(limit: int = 200, user: dict = Depends(require_controller)):
    return store.activity(limit=limit)

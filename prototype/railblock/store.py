"""
Storage for RailBlock.

The prototype held everything in memory, so every reload lost the work.
This gives the system a real database: departments submit block requests
that persist, a controller solves and publishes a plan, and every action
is written to an activity log.

Plain sqlite3 from the standard library — no extra dependency, one file
on disk, and easy to inspect with any SQLite viewer.

The bridge to the solver is `to_scenario()`, which turns whatever is in
the database into the same `Scenario` object `model.solve()` already
takes. Nothing in the solver had to change.
"""
from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
from typing import Iterable

from .model import DAY, Request, Scenario, Section, Window

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(HERE), "railblock.db")

DEPTS = ["ENGG", "S&T", "TRD"]
STATUSES = ["pending", "planned", "deferred"]


# ══════════════════════════════════════════════════════════════════
#  Connection
# ══════════════════════════════════════════════════════════════════
@contextmanager
def connect(path: str | None = None):
    con = sqlite3.connect(path or DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    finally:
        con.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS sections (
    id      TEXT PRIMARY KEY,
    name    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS windows (
    id          TEXT PRIMARY KEY,
    section     TEXT NOT NULL REFERENCES sections(id),
    start       INTEGER NOT NULL,      -- minutes from Monday 00:00
    end         INTEGER NOT NULL,
    disruption  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS requests (
    id            TEXT PRIMARY KEY,
    dept          TEXT NOT NULL,
    section       TEXT NOT NULL REFERENCES sections(id),
    title         TEXT NOT NULL,
    duration      INTEGER NOT NULL,    -- minutes
    priority      INTEGER NOT NULL,    -- 1 routine .. 5 safety critical
    deadline_day  INTEGER NOT NULL,
    status        TEXT NOT NULL DEFAULT 'pending',
    submitted_by  TEXT NOT NULL,
    submitted_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS plans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT NOT NULL,
    created_by  TEXT NOT NULL,
    days        INTEGER NOT NULL,
    urgency     REAL NOT NULL,
    strict      INTEGER NOT NULL,
    status      TEXT NOT NULL DEFAULT 'draft',   -- draft | published
    solver      TEXT NOT NULL,                   -- OPTIMAL / INFEASIBLE / ...
    solve_ms    REAL NOT NULL,
    conflict    TEXT NOT NULL DEFAULT '[]'       -- JSON list of request ids
);

CREATE TABLE IF NOT EXISTS plan_blocks (
    plan_id     INTEGER NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    request_id  TEXT NOT NULL,
    dept        TEXT NOT NULL,
    section     TEXT NOT NULL,
    title       TEXT NOT NULL,
    start       INTEGER NOT NULL,
    end         INTEGER NOT NULL,
    priority    INTEGER NOT NULL,
    window_id   TEXT NOT NULL,
    PRIMARY KEY (plan_id, request_id)
);

CREATE TABLE IF NOT EXISTS activity (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    at      TEXT NOT NULL,
    actor   TEXT NOT NULL,
    action  TEXT NOT NULL,
    detail  TEXT NOT NULL DEFAULT ''
);
"""


def init_db(path: str | None = None) -> None:
    with connect(path) as con:
        con.executescript(SCHEMA)


def reset_db(path: str | None = None) -> None:
    """Wipe everything. Used by the seed script and the tests."""
    p = path or DB_PATH
    if os.path.exists(p):
        os.remove(p)
    init_db(p)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ══════════════════════════════════════════════════════════════════
#  Activity log — every change is recorded
# ══════════════════════════════════════════════════════════════════
def log(actor: str, action: str, detail: str = "", path=None) -> None:
    with connect(path) as con:
        con.execute(
            "INSERT INTO activity (at, actor, action, detail) VALUES (?,?,?,?)",
            (_now(), actor, action, detail))


def activity(limit: int = 100, path=None) -> list[dict]:
    with connect(path) as con:
        rows = con.execute(
            "SELECT * FROM activity ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]


# ══════════════════════════════════════════════════════════════════
#  Corridor: sections and traffic-free windows
# ══════════════════════════════════════════════════════════════════
def set_corridor(sections: Iterable[Section], windows: Iterable[Window],
                 path=None) -> None:
    """Replace the corridor definition. Requests are left alone."""
    with connect(path) as con:
        con.execute("DELETE FROM windows")
        con.execute("DELETE FROM sections")
        con.executemany("INSERT INTO sections (id, name) VALUES (?,?)",
                        [(s.id, s.name) for s in sections])
        con.executemany(
            "INSERT INTO windows (id, section, start, end, disruption) "
            "VALUES (?,?,?,?,?)",
            [(w.id, w.section, w.start, w.end, w.disruption) for w in windows])


def sections(path=None) -> list[Section]:
    with connect(path) as con:
        return [Section(r["id"], r["name"])
                for r in con.execute("SELECT * FROM sections ORDER BY id")]


def windows(path=None) -> list[Window]:
    with connect(path) as con:
        return [Window(r["id"], r["section"], r["start"], r["end"],
                       r["disruption"])
                for r in con.execute("SELECT * FROM windows ORDER BY start")]


# ══════════════════════════════════════════════════════════════════
#  Requests
# ══════════════════════════════════════════════════════════════════
def next_request_id(path=None) -> str:
    with connect(path) as con:
        n = con.execute("SELECT COUNT(*) c FROM requests").fetchone()["c"]
    return f"R{n + 1:03d}"


def add_request(dept: str, section: str, title: str, duration: int,
                priority: int, deadline_day: int, submitted_by: str,
                path=None) -> str:
    rid = next_request_id(path)
    with connect(path) as con:
        con.execute(
            "INSERT INTO requests (id, dept, section, title, duration, "
            "priority, deadline_day, status, submitted_by, submitted_at) "
            "VALUES (?,?,?,?,?,?,?,'pending',?,?)",
            (rid, dept, section, title, duration, priority, deadline_day,
             submitted_by, _now()))
    log(submitted_by, "submitted request",
        f"{rid} · {title} · {section} · {duration} min · P{priority}", path)
    return rid


def list_requests(dept: str | None = None, status: str | None = None,
                  path=None) -> list[dict]:
    q = "SELECT * FROM requests"
    where, args = [], []
    if dept:
        where.append("dept = ?")
        args.append(dept)
    if status:
        where.append("status = ?")
        args.append(status)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY priority DESC, id"
    with connect(path) as con:
        return [dict(r) for r in con.execute(q, args)]


def get_request(rid: str, path=None) -> dict | None:
    with connect(path) as con:
        r = con.execute("SELECT * FROM requests WHERE id = ?", (rid,)).fetchone()
    return dict(r) if r else None


def delete_request(rid: str, actor: str, path=None) -> None:
    with connect(path) as con:
        con.execute("DELETE FROM requests WHERE id = ?", (rid,))
    log(actor, "withdrew request", rid, path)


def set_status(rids: Iterable[str], status: str, actor: str,
               path=None) -> None:
    rids = list(rids)
    if not rids:
        return
    with connect(path) as con:
        con.executemany("UPDATE requests SET status = ? WHERE id = ?",
                        [(status, r) for r in rids])
    log(actor, f"marked {status}", ", ".join(rids), path)


# ══════════════════════════════════════════════════════════════════
#  The bridge to the solver
# ══════════════════════════════════════════════════════════════════
def to_scenario(days: int, name: str = "Live corridor",
                crews: dict[str, int] | None = None,
                only: Iterable[str] | None = None,
                path=None) -> Scenario:
    """Build a Scenario from what is currently in the database.

    `only` restricts to specific request ids; by default every request
    that has not been deferred is included.
    """
    secs = sections(path)
    wins = [w for w in windows(path) if w.day < days]

    rows = list_requests(path=path)
    if only is not None:
        keep = set(only)
        rows = [r for r in rows if r["id"] in keep]
    else:
        rows = [r for r in rows if r["status"] != "deferred"]

    reqs = [Request(id=r["id"], dept=r["dept"], section=r["section"],
                    title=r["title"], duration=r["duration"],
                    priority=r["priority"], deadline_day=r["deadline_day"])
            for r in rows]

    return Scenario(name=name, days=days, sections=secs, windows=wins,
                    requests=reqs, crews=crews or {d: 2 for d in DEPTS})


# ══════════════════════════════════════════════════════════════════
#  Plans
# ══════════════════════════════════════════════════════════════════
def save_plan(solution, days: int, urgency: float, strict: bool,
              created_by: str, path=None) -> int:
    """Store a solved plan as a draft and return its id."""
    with connect(path) as con:
        cur = con.execute(
            "INSERT INTO plans (created_at, created_by, days, urgency, "
            "strict, status, solver, solve_ms, conflict) "
            "VALUES (?,?,?,?,?,'draft',?,?,?)",
            (_now(), created_by, days, urgency, int(strict),
             solution.status, solution.solve_time * 1000,
             json.dumps(solution.conflict)))
        pid = cur.lastrowid
        con.executemany(
            "INSERT INTO plan_blocks (plan_id, request_id, dept, section, "
            "title, start, end, priority, window_id) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            [(pid, b.request, b.dept, b.section, b.title, b.start, b.end,
              b.priority, b.window) for b in solution.blocks])
    log(created_by, "solved a plan",
        f"plan #{pid} · {solution.status} · {len(solution.blocks)} blocks",
        path)
    return pid


def publish_plan(pid: int, actor: str, path=None) -> None:
    """Make a plan the live block order and mark its requests planned."""
    with connect(path) as con:
        con.execute("UPDATE plans SET status = 'draft' WHERE status = 'published'")
        con.execute("UPDATE plans SET status = 'published' WHERE id = ?", (pid,))
        rids = [r["request_id"] for r in con.execute(
            "SELECT request_id FROM plan_blocks WHERE plan_id = ?", (pid,))]
        con.executemany("UPDATE requests SET status = 'planned' WHERE id = ?",
                        [(r,) for r in rids])
    log(actor, "published block order",
        f"plan #{pid} · {len(rids)} blocks now live", path)


def list_plans(limit: int = 25, path=None) -> list[dict]:
    with connect(path) as con:
        return [dict(r) for r in con.execute(
            "SELECT p.*, (SELECT COUNT(*) FROM plan_blocks b "
            "WHERE b.plan_id = p.id) AS blocks "
            "FROM plans p ORDER BY p.id DESC LIMIT ?", (limit,))]


def plan_blocks(pid: int, path=None) -> list[dict]:
    with connect(path) as con:
        return [dict(r) for r in con.execute(
            "SELECT * FROM plan_blocks WHERE plan_id = ? ORDER BY start",
            (pid,))]


def published_plan(path=None) -> dict | None:
    with connect(path) as con:
        r = con.execute(
            "SELECT * FROM plans WHERE status = 'published' "
            "ORDER BY id DESC LIMIT 1").fetchone()
    return dict(r) if r else None

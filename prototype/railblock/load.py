"""
Load a corridor from CSV into the database.

Member 2 fills in three spreadsheets — sections, windows and requests — and
this turns them into the live corridor. Nothing else in the system changes:
every screen, the solver and the block orders all run on whatever was loaded
last.

    python -m railblock.load ../team/2-data/corridor-1
    python -m railblock.load ../team/2-data/corridor-2 --check

`--check` validates and reports without writing anything, which is what to run
while the spreadsheets are still being filled in.

The files are written by hand, so every error message names the file, the row
and what to do about it.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from dataclasses import dataclass

from . import store
from .model import DAY, Section, Window

DEPTS = {"ENGG", "S&T", "TRD"}
SUBMITTER = {"ENGG": "p.way", "S&T": "snt", "TRD": "ohe"}

MIN_DURATION, MAX_DURATION = 15, 480
MAX_DAYS = 14


@dataclass
class Corridor:
    sections: list[Section]
    windows: list[Window]
    requests: list[dict]
    days: int


class LoadError(Exception):
    """Carries every problem found, not just the first."""

    def __init__(self, problems: list[str]):
        self.problems = problems
        super().__init__(f"{len(problems)} problem(s) in the CSV files")


# ══════════════════════════════════════════════════════════════════
#  Small parsers
# ══════════════════════════════════════════════════════════════════
def parse_hhmm(text: str, where: str) -> int:
    """'01:00' -> 60 minutes past midnight."""
    t = text.strip()
    if ":" not in t:
        raise ValueError(f"{where}: '{text}' should look like 01:00")
    hh, _, mm = t.partition(":")
    try:
        h, m = int(hh), int(mm)
    except ValueError:
        raise ValueError(f"{where}: '{text}' should look like 01:00") from None
    if not (0 <= h <= 24 and 0 <= m < 60):
        raise ValueError(f"{where}: '{text}' is not a real time")
    return h * 60 + m


def parse_days(text: str, where: str) -> list[int]:
    """'0-6' -> [0..6]   '0,2,4' -> [0,2,4]   '3' -> [3]"""
    t = text.strip()
    if not t:
        raise ValueError(f"{where}: days is empty — use 0-6 for every day")
    out: list[int] = []
    for part in t.split(","):
        part = part.strip()
        try:
            if "-" in part:
                a, _, b = part.partition("-")
                lo, hi = int(a), int(b)
                if lo > hi:
                    raise ValueError
                out.extend(range(lo, hi + 1))
            else:
                out.append(int(part))
        except ValueError:
            raise ValueError(
                f"{where}: cannot read days '{text}' — use 0-6, or 0,2,4, "
                f"or a single number") from None
    bad = [d for d in out if not 0 <= d < MAX_DAYS]
    if bad:
        raise ValueError(
            f"{where}: day {bad[0]} is outside 0–{MAX_DAYS - 1}")
    return sorted(set(out))


def _read_csv(folder: str, name: str, required: list[str],
              problems: list[str]) -> list[dict]:
    path = os.path.join(folder, name)
    if not os.path.exists(path):
        problems.append(f"{name}: file not found in {folder}")
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        problems.append(f"{name}: no rows — only the header line was found")
        return []
    missing = [c for c in required if c not in (rows[0].keys() or [])]
    if missing:
        problems.append(
            f"{name}: missing column(s) {', '.join(missing)} — "
            f"the header row must stay exactly as in the template")
        return []
    return rows


# ══════════════════════════════════════════════════════════════════
#  Reading a corridor folder
# ══════════════════════════════════════════════════════════════════
def read_corridor(folder: str) -> Corridor:
    problems: list[str] = []

    # ── sections ──────────────────────────────────────────────
    srows = _read_csv(folder, "sections.csv", ["id", "name"], problems)
    sections: list[Section] = []
    seen: set[str] = set()
    for i, r in enumerate(srows, start=2):
        sid = (r.get("id") or "").strip()
        name = (r.get("name") or "").strip()
        where = f"sections.csv row {i}"
        if not sid:
            problems.append(f"{where}: id is empty")
            continue
        if " " in sid:
            problems.append(f"{where}: id '{sid}' must not contain spaces")
            continue
        if sid in seen:
            problems.append(f"{where}: id '{sid}' is used more than once")
            continue
        seen.add(sid)
        sections.append(Section(sid, name or sid))

    valid = {s.id for s in sections}

    # ── windows ───────────────────────────────────────────────
    wrows = _read_csv(folder, "windows.csv",
                      ["section", "days", "start", "end"], problems)
    windows: list[Window] = []
    max_day = 0
    for i, r in enumerate(wrows, start=2):
        where = f"windows.csv row {i}"
        sec = (r.get("section") or "").strip()
        if sec not in valid:
            problems.append(
                f"{where}: section '{sec}' is not listed in sections.csv")
            continue
        try:
            days = parse_days(r.get("days", ""), where)
            start = parse_hhmm(r.get("start", ""), where)
            end = parse_hhmm(r.get("end", ""), where)
        except ValueError as e:
            problems.append(str(e))
            continue
        if end <= start:
            problems.append(
                f"{where}: end {r.get('end')} is not after start "
                f"{r.get('start')} — overnight windows are not supported, "
                f"split them into two rows")
            continue
        try:
            disruption = int((r.get("disruption") or "0").strip() or 0)
        except ValueError:
            problems.append(f"{where}: disruption must be a whole number")
            continue

        for d in days:
            max_day = max(max_day, d)
            windows.append(Window(
                id=f"W{d}-{sec}-{start}", section=sec,
                start=d * DAY + start, end=d * DAY + end,
                disruption=disruption))

    # ── requests ──────────────────────────────────────────────
    rrows = _read_csv(folder, "requests.csv",
                      ["dept", "section", "title", "duration_min",
                       "priority", "deadline_day"], problems)
    requests: list[dict] = []
    for i, r in enumerate(rrows, start=2):
        where = f"requests.csv row {i}"
        dept = (r.get("dept") or "").strip().upper()
        if dept == "S&T " or dept == "SNT":
            dept = "S&T"
        if dept not in DEPTS:
            problems.append(
                f"{where}: dept '{r.get('dept')}' must be one of "
                f"{', '.join(sorted(DEPTS))}")
            continue
        sec = (r.get("section") or "").strip()
        if sec not in valid:
            problems.append(
                f"{where}: section '{sec}' is not listed in sections.csv")
            continue
        title = (r.get("title") or "").strip()
        if not title:
            problems.append(f"{where}: title is empty")
            continue

        def _int(field, lo, hi):
            raw = (r.get(field) or "").strip()
            try:
                v = int(float(raw))
            except ValueError:
                raise ValueError(
                    f"{where}: {field} '{raw}' is not a number") from None
            if not lo <= v <= hi:
                raise ValueError(
                    f"{where}: {field} is {v}, must be between {lo} and {hi}")
            return v

        try:
            duration = _int("duration_min", MIN_DURATION, MAX_DURATION)
            priority = _int("priority", 1, 5)
            deadline = _int("deadline_day", 0, MAX_DAYS - 1)
        except ValueError as e:
            problems.append(str(e))
            continue

        requests.append(dict(dept=dept, section=sec, title=title,
                             duration=duration, priority=priority,
                             deadline_day=deadline))
        max_day = max(max_day, deadline)

    # ── whole-corridor sanity ─────────────────────────────────
    if sections and not windows:
        problems.append(
            "windows.csv: no usable windows — the corridor cannot be planned")
    for s in sections:
        if not any(w.section == s.id for w in windows):
            problems.append(
                f"sections.csv: '{s.id}' has no windows in windows.csv, so "
                f"nothing can ever be scheduled on it")

    if problems:
        raise LoadError(problems)

    return Corridor(sections, windows, requests, days=max_day + 1)


# ══════════════════════════════════════════════════════════════════
#  Writing it into the database
# ══════════════════════════════════════════════════════════════════
def load_folder(folder: str, keep_requests: bool = False,
                actor: str = "data.import") -> dict:
    c = read_corridor(folder)
    store.init_db()

    # Requests carry a foreign key to sections, so they have to go before
    # the corridor can be replaced.
    if keep_requests:
        new_ids = {s.id for s in c.sections}
        orphans = sorted({r["section"] for r in store.list_requests()
                          if r["section"] not in new_ids})
        if orphans:
            raise LoadError([
                f"--keep-requests was given, but existing requests sit on "
                f"section(s) {', '.join(orphans)}, which the new corridor "
                f"does not have. Drop --keep-requests to replace them."])
    else:
        with store.connect() as con:
            con.execute("DELETE FROM plan_blocks")
            con.execute("DELETE FROM plans")
            con.execute("DELETE FROM requests")

    store.set_corridor(c.sections, c.windows)

    for r in c.requests:
        store.add_request(
            dept=r["dept"], section=r["section"], title=r["title"],
            duration=r["duration"], priority=r["priority"],
            deadline_day=r["deadline_day"],
            submitted_by=SUBMITTER.get(r["dept"], "unknown"))

    store.log(actor, "imported corridor",
              f"{os.path.basename(folder)} · {len(c.sections)} sections · "
              f"{len(c.windows)} windows · {len(c.requests)} requests")

    return dict(folder=folder, sections=len(c.sections),
                windows=len(c.windows), requests=len(c.requests),
                days=c.days)


# ══════════════════════════════════════════════════════════════════
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="railblock.load",
        description="Load a corridor from CSV files into the database.")
    ap.add_argument("folder", help="folder holding the three CSV files")
    ap.add_argument("--check", action="store_true",
                    help="validate only, write nothing")
    ap.add_argument("--keep-requests", action="store_true",
                    help="keep existing requests instead of replacing them")
    a = ap.parse_args(argv)

    if not os.path.isdir(a.folder):
        print(f"  no such folder: {a.folder}")
        return 2

    try:
        if a.check:
            c = read_corridor(a.folder)
            print(f"  {a.folder}")
            print(f"  looks good — {len(c.sections)} sections, "
                  f"{len(c.windows)} windows, {len(c.requests)} requests, "
                  f"{c.days} day horizon")
            print("  nothing was written (--check)")
            return 0

        r = load_folder(a.folder, keep_requests=a.keep_requests)
        print(f"  loaded {r['folder']}")
        print(f"    sections  {r['sections']}")
        print(f"    windows   {r['windows']}")
        print(f"    requests  {r['requests']}")
        print(f"    horizon   {r['days']} days")
        print(f"  database: {store.DB_PATH}")
        return 0

    except LoadError as e:
        print(f"  {len(e.problems)} problem(s) found — nothing was written:\n")
        for p in e.problems:
            print(f"    - {p}")
        print("\n  Fix these in the spreadsheets and run again.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Populate the database with a starting corridor and a set of requests.

    python -m railblock.seed            # corridor + 18 requests
    python -m railblock.seed --empty    # corridor only, no requests
    python -m railblock.seed --small    # the 3-section division

Wipes whatever was there, so it is safe to re-run before a demo.
"""
from __future__ import annotations

import argparse

from . import store
from .scenarios import full_corridor, small_division

SUBMITTER = {"ENGG": "p.way.jaipur", "S&T": "snt.jaipur", "TRD": "ohe.jaipur"}

# Demo accounts — one per department, plus the controller. Real accounts,
# real hashed passwords (see store.create_user), just a shared password so
# anyone on the team can log in as any role during rehearsal and demo.
DEMO_PASSWORD = "railblock2026"
DEMO_ACCOUNTS = [
    ("p.way.jaipur", "ENGG", "Engineering (P.Way)"),
    ("snt.jaipur", "S&T", "Signalling & Telecom"),
    ("ohe.jaipur", "TRD", "Traction (OHE)"),
    ("controller", None, "Section controller"),
]


def seed(scenario, with_requests: bool = True) -> None:
    store.reset_db()
    store.set_corridor(scenario.sections, scenario.windows)
    for username, dept, display_name in DEMO_ACCOUNTS:
        store.create_user(username, DEMO_PASSWORD, dept, display_name)
    store.log("system", "seeded corridor",
              f"{len(scenario.sections)} sections, "
              f"{len(scenario.windows)} windows, {scenario.days} days")

    if not with_requests:
        return

    for r in scenario.requests:
        store.add_request(
            dept=r.dept, section=r.section, title=r.title,
            duration=r.duration, priority=r.priority,
            deadline_day=r.deadline_day,
            submitted_by=SUBMITTER.get(r.dept, "unknown"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Seed the RailBlock database.")
    ap.add_argument("--empty", action="store_true",
                    help="corridor only, no requests")
    ap.add_argument("--small", action="store_true",
                    help="use the 3-section division instead of the corridor")
    a = ap.parse_args()

    sc = small_division() if a.small else full_corridor()
    seed(sc, with_requests=not a.empty)

    print(f"  seeded from: {sc.name}")
    print(f"  database:    {store.DB_PATH}")
    print(f"  sections:    {len(store.sections())}")
    print(f"  windows:     {len(store.windows())}")
    print(f"  requests:    {len(store.list_requests())}")
    print(f"  days:        {sc.days}")
    print(f"  accounts:    {', '.join(u for u, _, _ in DEMO_ACCOUNTS)} "
         f"(password: {DEMO_PASSWORD})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

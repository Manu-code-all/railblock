"""
RailBlock command line — the fastest way to show the solver working.

    python -m railblock.cli A
    python -m railblock.cli C --strict
    python -m railblock.cli B --urgency 1.0
"""
from __future__ import annotations

import argparse
import sys

from .model import DAY, explain_conflict, solve, verify
from .scenarios import ALL, DEPT_NAME, load


def _unicode_ok() -> bool:
    """Windows consoles often run cp1252, which cannot draw box rules."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")   # Python 3.7+
        return True
    except Exception:
        pass
    enc = getattr(sys.stdout, "encoding", None) or "ascii"
    try:
        "═–·".encode(enc)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


UNI = _unicode_ok()
BAR = ("═" if UNI else "=") * 74
DASH = ("─" if UNI else "-") * 74
TO = "–" if UNI else "-"


def hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="railblock",
        description="Coordinated maintenance block planning (CP-SAT).")
    ap.add_argument("scenario", nargs="?", default="A",
                    choices=[k for k in ALL] + [k.lower() for k in ALL],
                    help="A = small division, B = full corridor, C = overloaded")
    ap.add_argument("--strict", action="store_true",
                    help="every request must be scheduled; report the "
                         "minimal conflicting set if that is impossible")
    ap.add_argument("--urgency", type=float, default=0.5,
                    help="0.0 protect train service .. 1.0 clear urgent work early")
    args = ap.parse_args(argv)

    sc = load(args.scenario)

    print(BAR)
    print(f"  RailBlock  ·  {sc.name}")
    print(BAR)
    print(f"  Sections   {len(sc.sections)}       "
          f"Windows  {len(sc.windows)}       "
          f"Requests {len(sc.requests)}")
    print(f"  Horizon    {sc.days} days   "
          f"Crews    " + ", ".join(f"{d}:{sc.crews_for(d)}" for d in sc.depts))
    print(f"  Mode       {'STRICT (all requests mandatory)' if args.strict else 'OPTIMISE (schedule what fits)'}")
    print(f"  Urgency    {args.urgency:.2f}")
    print(DASH)

    sol = solve(sc, strict=args.strict, urgency=args.urgency)

    # ── Infeasible: name the culprits ────────────────────────────
    if not sol.ok:
        print(f"  STATUS     {sol.status}   ({sol.solve_time:.3f}s)")
        print(DASH)
        if sol.conflict:
            print("  These requests CANNOT COEXIST:")
            print()
            for rid in sol.conflict:
                r = sc.request(rid)
                print(f"    {rid}  {r.dept:5}  {sc.section_name(r.section):22}"
                      f"  {r.duration:3d} min  P{r.priority}")
                print(f"          {r.title}")
            print()
            why = explain_conflict(sc, sol.conflict)
            import textwrap
            for ln in textwrap.wrap(why, 70):
                print(f"  {ln}")
            print()
            print("  This is the answer that matters: not 'no solution',")
            print("  but exactly which requests are fighting, and why.")
        else:
            print("  No solution and no assumption set "
                  "(try --strict to get the conflict set).")
        print(BAR)
        return 1

    # ── Feasible: print the plan ─────────────────────────────────
    verdict = "PROVEN OPTIMAL" if sol.proven_optimal else "feasible"
    print(f"  STATUS     {sol.status}  -  {verdict}   ({sol.solve_time:.3f}s)")
    print(f"  Scheduled  {len(sol.blocks)} of {len(sc.requests)} requests")
    print(DASH)

    for d in range(sc.days):
        today = [b for b in sol.blocks if b.day == d]
        if not today:
            continue
        print(f"\n  DAY {d}")
        for b in sorted(today, key=lambda x: x.start):
            print(f"    {hhmm(b.start % DAY)}{TO}{hhmm(b.end % DAY)}  "
                  f"{b.dept:5} {sc.section_name(b.section):22} "
                  f"P{b.priority}  {b.title}")

    if sol.unscheduled:
        print(f"\n  NOT SCHEDULED ({len(sol.unscheduled)})")
        for rid in sol.unscheduled:
            r = sc.request(rid)
            print(f"    {rid}  {r.dept:5} {r.title}  "
                  f"({r.duration} min, P{r.priority}, due day {r.deadline_day})")

    # ── Independent re-check ─────────────────────────────────────
    print()
    print(DASH)
    problems = verify(sc, sol)
    if problems:
        print("  VERIFICATION FAILED:")
        for p in problems:
            print(f"    ! {p}")
        print(BAR)
        return 2

    print(f"  VERIFIED   {len(sol.blocks)} blocks re-checked independently:")
    print("             no section double-booked, every block inside a")
    print("             traffic-free window, no deadline missed, crew")
    print("             limits respected.")
    print(BAR)
    return 0


if __name__ == "__main__":
    sys.exit(main())

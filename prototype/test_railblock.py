"""
Checks for RailBlock.

Every claim the demo makes on camera is asserted here, so "the solver
proves it" is something you can run in front of a judge rather than
something you assert.

    python -m pytest test_railblock.py -v
    python test_railblock.py            # runs without pytest too
"""
from __future__ import annotations

import itertools
from dataclasses import replace

from railblock import DAY, scenarios, solve, verify
from railblock.model import explain_conflict


# ══════════════════════════════════════════════════════════════════
#  Claim: the plans we produce are legal
# ══════════════════════════════════════════════════════════════════
def test_small_division_is_valid():
    sc = scenarios.small_division()
    sol = solve(sc)
    assert sol.proven_optimal
    assert verify(sc, sol) == []


def test_full_corridor_is_valid():
    sc = scenarios.full_corridor()
    sol = solve(sc)
    assert sol.proven_optimal
    assert verify(sc, sol) == []


def test_every_request_fits_when_there_is_room():
    """Scenarios A and B are designed to be fully satisfiable."""
    for build in (scenarios.small_division, scenarios.full_corridor):
        sc = build()
        sol = solve(sc)
        assert len(sol.blocks) == len(sc.requests), sc.name
        assert sol.unscheduled == []


def test_blocks_sit_inside_traffic_free_windows():
    sc = scenarios.full_corridor()
    sol = solve(sc)
    wins = {w.id: w for w in sc.windows}
    for b in sol.blocks:
        w = wins[b.window]
        assert w.section == b.section
        assert w.start <= b.start and b.end <= w.end


def test_no_section_is_double_booked():
    sc = scenarios.full_corridor()
    sol = solve(sc)
    for s in sc.sections:
        on = sorted((b for b in sol.blocks if b.section == s.id),
                    key=lambda b: b.start)
        for a, c in zip(on, on[1:]):
            assert c.start >= a.end, f"{a.request} overlaps {c.request}"


def test_deadlines_are_respected():
    sc = scenarios.full_corridor()
    sol = solve(sc)
    for b in sol.blocks:
        r = sc.request(b.request)
        assert b.end <= (r.deadline_day + 1) * DAY


def test_crew_limits_are_respected():
    sc = scenarios.small_division()
    sol = solve(sc)
    for dept in sc.depts:
        on = [b for b in sol.blocks if b.dept == dept]
        cap = sc.crews_for(dept)
        for t in {b.start for b in on}:
            live = sum(1 for b in on if b.start <= t < b.end)
            assert live <= cap, f"{dept}: {live} concurrent, cap {cap}"


# ══════════════════════════════════════════════════════════════════
#  Claim: the priority slider is a real trade-off, not decoration
# ══════════════════════════════════════════════════════════════════
def test_slider_changes_the_plan():
    sc = scenarios.full_corridor()
    protect = solve(sc, urgency=0.0)
    urgent = solve(sc, urgency=1.0)

    def span(s):
        return max(b.day for b in s.blocks)

    def daytime(s):
        wins = {w.id: w for w in sc.windows}
        return sum(1 for b in s.blocks if wins[b.window].disruption > 0)

    # Clearing work urgently finishes sooner...
    assert span(urgent) < span(protect)
    # ...by spending disruptive daytime windows that the other end avoids.
    assert daytime(urgent) > daytime(protect)
    assert daytime(protect) == 0
    # Both remain fully valid plans.
    assert verify(sc, protect) == [] and verify(sc, urgent) == []


# ══════════════════════════════════════════════════════════════════
#  Claim: the conflict set is minimal, and it is right
# ══════════════════════════════════════════════════════════════════
def test_overloaded_scenario_is_infeasible_in_strict_mode():
    sc = scenarios.overloaded()
    sol = solve(sc, strict=True)
    assert not sol.ok
    assert sol.status == "INFEASIBLE"


def test_conflict_set_is_exactly_the_three_culprits():
    sc = scenarios.overloaded()
    sol = solve(sc, strict=True)
    assert sol.conflict == ["R01", "R02", "R03"]
    # The two requests on the other section are not implicated.
    assert "R04" not in sol.conflict and "R05" not in sol.conflict


def test_conflict_set_is_irreducible():
    """No proper subset of the conflict is itself infeasible.

    This is what makes the answer useful: every request named is load
    bearing, so the planner knows the argument is genuinely three-way.
    """
    sc = scenarios.overloaded()
    core = solve(sc, strict=True).conflict
    for pair in itertools.combinations(core, len(core) - 1):
        subset = replace(sc, requests=[r for r in sc.requests if r.id in pair])
        assert solve(subset, strict=True).ok, f"{pair} should be satisfiable"


def test_dropping_any_one_culprit_makes_it_solvable():
    """The demo says 'defer any one of these' — check that is true."""
    sc = scenarios.overloaded()
    for drop in solve(sc, strict=True).conflict:
        trimmed = replace(sc, requests=[r for r in sc.requests if r.id != drop])
        sol = solve(trimmed, strict=True)
        assert sol.ok, f"dropping {drop} should solve"
        assert len(sol.blocks) == len(trimmed.requests)
        assert verify(trimmed, sol) == []


def test_conflict_explanation_names_the_section_and_the_numbers():
    sc = scenarios.overloaded()
    sol = solve(sc, strict=True)
    why = explain_conflict(sc, sol.conflict)
    assert "Phulera" in why
    assert "270" in why          # what the three requests need
    assert "240" in why          # what the window can give


# ══════════════════════════════════════════════════════════════════
#  Claim: optimise mode degrades gracefully instead of failing
# ══════════════════════════════════════════════════════════════════
def test_optimise_mode_still_returns_a_plan_when_overloaded():
    sc = scenarios.overloaded()
    sol = solve(sc)                       # not strict
    assert sol.ok
    assert sol.unscheduled                # something had to give
    assert verify(sc, sol) == []          # what it did place is legal


def test_optimise_mode_drops_from_the_contested_section_only():
    """It sheds work where the contention actually is.

    SEC-A can hold two of its three requests; SEC-B is uncontested.
    Dropping a SEC-B request would free no SEC-A capacity, so a correct
    solver never trades one for the other — even though the SEC-B work
    is lower priority. Priority only decides between requests that are
    genuinely competing.
    """
    sc = scenarios.overloaded()
    sol = solve(sc)

    assert len(sol.unscheduled) == 1
    dropped = sc.request(sol.unscheduled[0])
    assert dropped.section == "SEC-A"
    assert {b.request for b in sol.blocks} >= {"R04", "R05"}


def test_optimise_mode_schedules_the_most_valuable_set():
    """Two of SEC-A's three plus both of SEC-B's is the best possible."""
    sc = scenarios.overloaded()
    sol = solve(sc)
    best = 5 + 5 + 2 + 2
    assert sum(b.priority for b in sol.blocks) == best


# ══════════════════════════════════════════════════════════════════
#  Claim: it is fast enough to feel interactive
# ══════════════════════════════════════════════════════════════════
def test_solves_quickly_enough_for_a_live_slider():
    sc = scenarios.full_corridor()
    sol = solve(sc)
    assert sol.solve_time < 2.0, f"took {sol.solve_time:.2f}s"


# ══════════════════════════════════════════════════════════════════
def _main() -> int:
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {name}\n          {e}")
        except Exception as e:                      # noqa: BLE001
            failed += 1
            print(f"  ERROR {name}\n          {type(e).__name__}: {e}")
    print()
    print(f"  {len(tests) - failed} passed, {failed} failed, "
          f"{len(tests)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_main())

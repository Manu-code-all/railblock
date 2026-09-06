"""
Why is this block here?

A solver that only prints a schedule asks to be trusted. This module
reconstructs the reasoning for any single block from the finished plan:
which traffic-free windows could have held the work, what ruled each of
the others out, and what fixed the start time.

Every statement is checked against the plan rather than asserted — if a
window is called "occupied", the blocks occupying it are named.
"""
from __future__ import annotations

from dataclasses import dataclass

from .model import DAY, Scenario, Solution


def hhmm(m: int) -> str:
    return f"{(m % DAY) // 60:02d}:{m % 60:02d}"


def daytime(m: int) -> str:
    return f"day {m // DAY}, {hhmm(m)}"


@dataclass
class WindowVerdict:
    window: str
    day: int
    span: str
    ok: bool
    why: str


@dataclass
class Why:
    request: str
    scheduled: bool
    headline: str
    reasons: list[str]
    alternatives: list[WindowVerdict]


def _free_gaps(win, blocks, ignore: str) -> list[tuple[int, int]]:
    """Stretches of a window left free by the other blocks on that section."""
    busy = sorted(
        (b.start, b.end) for b in blocks
        if b.section == win.section and b.request != ignore
        and b.start < win.end and b.end > win.start)

    gaps, cursor = [], win.start
    for s, e in busy:
        if s > cursor:
            gaps.append((cursor, min(s, win.end)))
        cursor = max(cursor, e)
    if cursor < win.end:
        gaps.append((cursor, win.end))
    return [(a, b) for a, b in gaps if b > a]


def explain(scenario: Scenario, solution: Solution, rid: str) -> Why:
    r = scenario.request(rid)
    block = next((b for b in solution.blocks if b.request == rid), None)
    sec_name = scenario.section_name(r.section)
    deadline = (r.deadline_day + 1) * DAY

    on_section = [w for w in scenario.windows if w.section == r.section]
    on_section.sort(key=lambda w: w.start)

    alternatives: list[WindowVerdict] = []
    for w in on_section:
        span = f"{hhmm(w.start)}–{hhmm(w.end)}"
        if w.length < r.duration:
            alternatives.append(WindowVerdict(
                w.id, w.day, span, False,
                f"only {w.length} min long, the job needs {r.duration}"))
            continue
        if w.start >= deadline:
            alternatives.append(WindowVerdict(
                w.id, w.day, span, False,
                f"opens after the day-{r.deadline_day} deadline"))
            continue

        gaps = _free_gaps(w, solution.blocks, rid)
        room = max((b - a for a, b in gaps), default=0)
        if room < r.duration:
            others = sorted({
                b.request for b in solution.blocks
                if b.section == w.section and b.request != rid
                and b.start < w.end and b.end > w.start})
            alternatives.append(WindowVerdict(
                w.id, w.day, span, False,
                f"only {room} min free — held by {', '.join(others)}"
                if others else f"only {room} min free"))
            continue

        chosen = block is not None and block.window == w.id
        alternatives.append(WindowVerdict(
            w.id, w.day, span, True,
            "chosen" if chosen else "was also possible"))

    # ── Unscheduled ──────────────────────────────────────────────
    if block is None:
        viable = [a for a in alternatives if a.ok]
        reasons = []
        if not on_section:
            reasons.append(f"{sec_name} has no traffic-free windows at all.")
        elif not viable:
            short = sum(1 for a in alternatives if "only" in a.why
                        and "long" in a.why)
            late = sum(1 for a in alternatives if "deadline" in a.why)
            held = sum(1 for a in alternatives if "held by" in a.why)
            if short:
                reasons.append(
                    f"{short} window(s) on {sec_name} are shorter than the "
                    f"{r.duration} minutes this job needs.")
            if late:
                reasons.append(
                    f"{late} window(s) open only after its day-"
                    f"{r.deadline_day} deadline.")
            if held:
                reasons.append(
                    f"{held} window(s) are already held by other work.")
        else:
            reasons.append(
                "A window was available, so this was dropped by the "
                "objective: other requests carried more weight than its "
                f"priority {r.priority}.")
        return Why(rid, False,
                   f"{rid} could not be placed on {sec_name}.",
                   reasons, alternatives)

    # ── Scheduled ────────────────────────────────────────────────
    win = next(w for w in scenario.windows if w.id == block.window)
    reasons = [
        f"Placed in the {hhmm(win.start)}–{hhmm(win.end)} window on "
        f"{sec_name}, day {win.day}."
    ]

    if block.start == win.start:
        reasons.append("Starts the moment the section goes traffic-free.")
    else:
        before = [b for b in solution.blocks
                  if b.section == block.section and b.end <= block.start
                  and b.end > win.start]
        if before:
            prev = max(before, key=lambda b: b.end)
            reasons.append(
                f"Waits for {prev.request} ({prev.dept}) to clear the "
                f"section at {hhmm(prev.end)}.")
        else:
            reasons.append(
                f"Starts at {hhmm(block.start)}, "
                f"{block.start - win.start} min into the window.")

    slack = deadline - block.end
    if slack < DAY:
        reasons.append(
            f"Finishes {slack // 60}h {slack % 60}m before its day-"
            f"{r.deadline_day} deadline — little room to move.")
    else:
        reasons.append(
            f"Finishes {slack // DAY} day(s) before its day-"
            f"{r.deadline_day} deadline.")

    if win.disruption:
        reasons.append(
            f"This is a daytime window (disruption cost {win.disruption}); "
            f"the plan spent it to clear the work sooner.")
    else:
        reasons.append("A night window, so no train paths were given up.")

    others = sum(1 for a in alternatives if a.ok and a.window != win.id)
    if others:
        reasons.append(
            f"{others} other window(s) could also have held it — this one "
            f"scored best under the current priority setting.")
    else:
        reasons.append("No other window on this section could have held it.")

    return Why(rid, True,
               f"{rid} runs {daytime(block.start)}–{hhmm(block.end)} "
               f"on {sec_name}.",
               reasons, alternatives)


def as_text(why: Why) -> str:
    out = [why.headline, ""]
    out += [f"  - {r}" for r in why.reasons]
    if why.alternatives:
        out += ["", "  Windows considered on this section:"]
        for a in why.alternatives:
            mark = "OK " if a.ok else "no "
            out.append(f"    {mark} day {a.day} {a.span}  {a.why}")
    return "\n".join(out)

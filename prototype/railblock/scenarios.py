"""
Demo scenarios for RailBlock.

The problem statement lists its own inputs — sections, maintenance
demands, traffic-free windows, crews — so building them here is the
correct method, not a workaround for missing data. It also lets us
demo a small division and a large corridor side by side, which real
data from a single division could never do.

Times are minutes from 00:00 on Monday.
"""
from __future__ import annotations

from .model import DAY, Request, Scenario, Section, Window

ENGG, SNT, TRD = "ENGG", "S&T", "TRD"

DEPT_NAME = {
    ENGG: "Engineering (P.Way)",
    SNT:  "Signalling & Telecom",
    TRD:  "Traction (OHE)",
}


def _nightly(sections, days, start_h=1, end_h=5, disruption=0, tag="N"):
    """A traffic-free window every night on every section."""
    out = []
    for d in range(days):
        for s in sections:
            out.append(Window(
                id=f"{tag}{d}-{s.id}",
                section=s.id,
                start=d * DAY + start_h * 60,
                end=d * DAY + end_h * 60,
                disruption=disruption,
            ))
    return out


def _daytime(sections, days, start_h=13, end_h=16, disruption=5, tag="D"):
    """A shorter daytime window — available, but it costs train paths."""
    out = []
    for d in range(days):
        for s in sections:
            out.append(Window(
                id=f"{tag}{d}-{s.id}",
                section=s.id,
                start=d * DAY + start_h * 60,
                end=d * DAY + end_h * 60,
                disruption=disruption,
            ))
    return out


# ══════════════════════════════════════════════════════════════════
#  A — one division, everything fits
# ══════════════════════════════════════════════════════════════════
def small_division() -> Scenario:
    secs = [
        Section("SEC-A", "Phulera – Jaipur"),
        Section("SEC-B", "Jaipur – Dausa"),
        Section("SEC-C", "Dausa – Bandikui"),
    ]
    days = 5
    wins = _nightly(secs, days) + _daytime(secs, days)

    reqs = [
        Request("R01", ENGG, "SEC-A", "Rail grinding, km 12-18",       180, 4, 2),
        Request("R02", ENGG, "SEC-B", "Ballast cleaning, km 41-44",    210, 3, 4),
        Request("R03", ENGG, "SEC-C", "Track tamping, km 66-70",       150, 3, 4),
        Request("R04", SNT,  "SEC-A", "Point machine replacement",     120, 5, 1),
        Request("R05", SNT,  "SEC-B", "Axle counter recalibration",     90, 4, 3),
        Request("R06", SNT,  "SEC-C", "Signal cable renewal",          180, 2, 4),
        Request("R07", TRD,  "SEC-A", "OHE mast replacement",          210, 5, 2),
        Request("R08", TRD,  "SEC-B", "Contact wire tension check",    120, 3, 4),
    ]
    return Scenario(
        name="A — Jaipur division, 5-day plan",
        days=days, sections=secs, windows=wins, requests=reqs,
        crews={ENGG: 2, SNT: 1, TRD: 1},
    )


# ══════════════════════════════════════════════════════════════════
#  B — full corridor, proves it scales
# ══════════════════════════════════════════════════════════════════
def full_corridor() -> Scenario:
    secs = [
        Section("SEC-A", "Phulera – Jaipur"),
        Section("SEC-B", "Jaipur – Dausa"),
        Section("SEC-C", "Dausa – Bandikui"),
        Section("SEC-D", "Bandikui – Alwar"),
        Section("SEC-E", "Alwar – Rewari"),
        Section("SEC-F", "Rewari – Gurgaon"),
    ]
    days = 7
    wins = _nightly(secs, days) + _daytime(secs, days)

    work = [
        (ENGG, "Rail grinding",            180, 4), (ENGG, "Ballast cleaning",     210, 3),
        (ENGG, "Track tamping",            150, 3), (ENGG, "Weld renewal",         120, 5),
        (ENGG, "Culvert repair",           240, 2), (ENGG, "Level-crossing resurface", 180, 3),
        (SNT,  "Point machine replacement", 120, 5), (SNT, "Axle counter recalibration", 90, 4),
        (SNT,  "Signal cable renewal",     180, 2), (SNT, "Interlocking upgrade",  240, 5),
        (SNT,  "Track circuit tuning",      90, 3), (SNT, "Block instrument test", 120, 4),
        (TRD,  "OHE mast replacement",     210, 5), (TRD, "Contact wire tension",  120, 3),
        (TRD,  "Insulator cleaning",        90, 2), (TRD, "Feeder cable renewal",  240, 4),
        (TRD,  "Neutral section repair",   150, 4), (TRD, "Earthing audit",         90, 2),
    ]
    reqs = []
    for i, (dept, title, dur, pri) in enumerate(work):
        sec = secs[i % len(secs)]
        reqs.append(Request(
            id=f"R{i + 1:02d}", dept=dept, section=sec.id,
            title=f"{title}, {sec.name.split(' – ')[0]}",
            duration=dur, priority=pri,
            deadline_day=days - 1 if pri < 5 else 3,
        ))
    return Scenario(
        name="B — Jaipur–Gurgaon corridor, 7-day plan",
        days=days, sections=secs, windows=wins, requests=reqs,
        crews={ENGG: 2, SNT: 2, TRD: 2},
    )


# ══════════════════════════════════════════════════════════════════
#  C — deliberately impossible
# ══════════════════════════════════════════════════════════════════
def overloaded() -> Scenario:
    """Three departments, one section, one night — one too many jobs.

    SEC-A has a single 4-hour window on day 0 (240 min). R01, R02 and
    R03 each need 90 minutes of it. ANY TWO fit comfortably (180 of 240),
    but all three need 270 and cannot. That makes the clash genuinely
    three-way: no pair is the problem, so the solver has to identify the
    trio. R04 and R05 sit on SEC-B and must NOT appear in the answer.

    Run in STRICT mode: the solver does not say "infeasible", it names
    exactly which requests are fighting.
    """
    secs = [
        Section("SEC-A", "Phulera – Jaipur"),
        Section("SEC-B", "Jaipur – Dausa"),
    ]
    days = 1
    wins = _nightly(secs, days)          # night only: no daytime relief

    reqs = [
        # Any two of these fit (180 of 240). All three need 270 — they cannot.
        Request("R01", ENGG, "SEC-A", "Emergency weld renewal, km 14",    90, 5, 0),
        Request("R02", SNT,  "SEC-A", "Point machine failure, Phulera",   90, 5, 0),
        Request("R03", TRD,  "SEC-A", "OHE mast down, km 16",             90, 5, 0),
        # These are fine and must not appear in the conflict set.
        Request("R04", ENGG, "SEC-B", "Routine tamping, km 44",          120, 2, 0),
        Request("R05", SNT,  "SEC-B", "Track circuit tuning",             90, 2, 0),
    ]
    return Scenario(
        name="C — overloaded night, conflict demo",
        days=days, sections=secs, windows=wins, requests=reqs,
        crews={ENGG: 1, SNT: 1, TRD: 1},
    )


ALL = {
    "A": ("Small division (feasible)", small_division),
    "B": ("Full corridor (scales)",    full_corridor),
    "C": ("Overloaded (conflict)",     overloaded),
}


def load(key: str) -> Scenario:
    return ALL[key.upper()][1]()

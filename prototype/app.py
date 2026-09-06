"""
RailBlock — coordinated maintenance block planning.

    streamlit run app.py

Four roles share one screen. The three maintenance departments submit block
requests; the section controller plans the corridor and publishes the block
order. Everything is read from and written to the database, so work survives a
restart and every action lands in the activity log.

Roles here are *selected*, not authenticated — see docs/03-security-and-access.
"""
from __future__ import annotations

import csv
import io

import streamlit as st

from railblock import solve, store, verify
from railblock.chart import gantt
from railblock.explain import explain as explain_why
from railblock.model import DAY
from railblock.scenarios import DEPT_NAME

# ── Roles ─────────────────────────────────────────────────────────
CONTROLLER = "Section controller"
ROLES = {
    "Engineering (P.Way)": "ENGG",
    "Signalling & Telecom": "S&T",
    "Traction (OHE)": "TRD",
    CONTROLLER: None,
}
ACTOR = {"ENGG": "p.way", "S&T": "snt", "TRD": "ohe", None: "controller"}

STATUS_COLOUR = {"pending": "#6B7280", "planned": "#1E8449",
                 "deferred": "#CA8A04"}

st.set_page_config(page_title="RailBlock", page_icon="🚆", layout="wide")

st.markdown("""
<style>
  .block-container {padding-top: 2.2rem; max-width: 1500px;}
  div[data-testid="stMetricValue"] {font-size: 1.5rem;}
  .rb-title {font-size:1.95rem; font-weight:800; color:#1F3864;
             letter-spacing:-.5px; margin-bottom:.1rem;}
  .rb-sub   {color:#5A6B82; font-size:.95rem; margin-bottom:1.1rem;}
  .rb-good  {background:#E8F5EC; border-left:4px solid #1E8449;
             padding:.7rem .9rem; border-radius:6px; color:#14532d;}
  .rb-bad   {background:#FDEDEC; border-left:4px solid #C0392B;
             padding:.7rem .9rem; border-radius:6px; color:#7f1d1d;}
  .rb-pill  {display:inline-block; padding:1px 9px; border-radius:10px;
             font-size:.75rem; font-weight:700; color:white;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#  Helpers
# ══════════════════════════════════════════════════════════════════
def hhmm(m: int) -> str:
    return f"{(m % DAY) // 60:02d}:{m % 60:02d}"


def pill(status: str) -> str:
    c = STATUS_COLOUR.get(status, "#6B7280")
    return f'<span class="rb-pill" style="background:{c}">{status}</span>'


def horizon(sections, windows) -> int:
    """How many days the loaded corridor covers."""
    if not windows:
        return 7
    return max(w.day for w in windows) + 1


def signature() -> str:
    """Changes whenever the requests change, so cached solves expire."""
    rows = store.list_requests()
    return "|".join(f"{r['id']}{r['status']}{r['duration']}{r['priority']}"
                    f"{r['deadline_day']}{r['section']}" for r in rows)


@st.cache_resource(show_spinner=False)
def _warm_solver():
    """Pay CP-SAT's one-time start-up cost before any solve the user sees.

    Without this the first solve reports well over a second, almost all of
    it library warm-up, which badly misrepresents the speed of every solve
    after it.
    """
    from railblock.scenarios import small_division
    solve(small_division(), time_limit=5.0)
    return True


@st.cache_data(show_spinner=False)
def run_solver(sig: str, days: int, strict: bool, urgency: float):
    """Cached on the request signature, so the slider stays responsive."""
    sc = store.to_scenario(days=days)
    sol = solve(sc, strict=strict, urgency=urgency)
    return sc, sol, verify(sc, sol)


# ══════════════════════════════════════════════════════════════════
#  Sidebar
# ══════════════════════════════════════════════════════════════════
store.init_db()
_warm_solver()
sections = store.sections()
windows = store.windows()
DAYS = horizon(sections, windows)

with st.sidebar:
    st.markdown("### RailBlock")
    st.caption("Coordinated maintenance block planning")

    role_name = st.radio("Signed in as", list(ROLES), index=0)
    dept = ROLES[role_name]
    actor = ACTOR[dept]

    st.divider()
    if sections:
        st.caption(f"**Corridor** · {len(sections)} sections · "
                   f"{DAYS}-day horizon")
        pending = len(store.list_requests(status="pending"))
        st.caption(f"**Pending requests** · {pending}")
        pub = store.published_plan()
        st.caption(f"**Block order** · "
                   f"{'plan #' + str(pub['id']) if pub else 'none published'}")
    else:
        st.caption("No corridor loaded")


# ══════════════════════════════════════════════════════════════════
#  No corridor yet
# ══════════════════════════════════════════════════════════════════
if not sections:
    st.markdown('<div class="rb-title">RailBlock</div>', unsafe_allow_html=True)
    st.warning("No corridor is loaded, so there is nothing to plan yet.",
               icon="⚠️")
    st.markdown("Load one from the terminal:")
    st.code("python -m railblock.seed", language="bash")
    st.markdown("or import real data from CSV:")
    st.code("python -m railblock.load ../team/2-data/corridor-1",
            language="bash")
    st.stop()


# ══════════════════════════════════════════════════════════════════
#  DEPARTMENT VIEW
# ══════════════════════════════════════════════════════════════════
def department_view(dept: str, role_name: str) -> None:
    st.markdown(f'<div class="rb-title">{role_name}</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="rb-sub">Your block requests for this '
                'corridor.</div>', unsafe_allow_html=True)

    mine = store.list_requests(dept=dept)
    counts = {s: sum(1 for r in mine if r["status"] == s)
              for s in ("pending", "planned", "deferred")}

    a, b, c, d = st.columns(4)
    a.metric("Requests", len(mine))
    b.metric("Pending", counts["pending"])
    c.metric("Planned", counts["planned"])
    d.metric("Deferred", counts["deferred"])

    # ── Submit ───────────────────────────────────────────────
    with st.expander("Submit a block request", expanded=not mine):
        with st.form("submit", clear_on_submit=True):
            c1, c2 = st.columns([2, 1])
            title = c1.text_input(
                "Work", max_chars=80,
                placeholder="e.g. Rail grinding, km 12-18")
            section = c2.selectbox(
                "Section", [s.id for s in sections],
                format_func=lambda i: next(
                    s.name for s in sections if s.id == i))

            c3, c4, c5 = st.columns(3)
            duration = c3.number_input("Duration (minutes)", 15, 480, 120, 15)
            priority = c4.slider("Priority", 1, 5, 3,
                                 help="1 routine · 5 safety-critical")
            deadline = c5.number_input("Finish by day", 0, DAYS - 1,
                                       min(3, DAYS - 1))

            if st.form_submit_button("Submit request", type="primary"):
                if not title.strip():
                    st.error("Give the work a title.")
                else:
                    longest = max((w.length for w in windows
                                   if w.section == section), default=0)
                    rid = store.add_request(
                        dept=dept, section=section, title=title.strip(),
                        duration=int(duration), priority=int(priority),
                        deadline_day=int(deadline), submitted_by=actor)
                    if longest < duration:
                        st.warning(
                            f"Submitted as {rid}, but no window on this "
                            f"section is longer than {longest} minutes, so "
                            f"it cannot be placed as it stands.", icon="⚠️")
                    else:
                        st.success(f"Submitted as {rid}.")
                    st.rerun()

    # ── My requests ──────────────────────────────────────────
    st.markdown("#### My requests")
    if not mine:
        st.info("No requests yet. Submit one above.")
    else:
        for r in mine:
            c1, c2, c3, c4, c5 = st.columns([1, 4, 3.2, 1.5, 1.3])
            c1.markdown(f"**{r['id']}**")
            c2.markdown(r["title"])
            c3.caption(f"{next(s.name for s in sections if s.id == r['section'])}"
                       f" · {r['duration']} min · P{r['priority']}"
                       f" · by day {r['deadline_day']}")
            c4.markdown(pill(r["status"]), unsafe_allow_html=True)
            if r["status"] == "pending":
                if c5.button("Withdraw", key=f"w{r['id']}"):
                    store.delete_request(r["id"], actor)
                    st.rerun()

    # ── Published block order, filtered to this department ────
    pub = store.published_plan()
    if pub:
        blocks = [b for b in store.plan_blocks(pub["id"]) if b["dept"] == dept]
        st.markdown("#### Published block order")
        if not blocks:
            st.caption("The live block order contains no work for your "
                       "department.")
        else:
            st.dataframe(
                [{"Request": b["request_id"], "Day": b["start"] // DAY,
                  "Time": f"{hhmm(b['start'])}–{hhmm(b['end'])}",
                  "Section": next(s.name for s in sections
                                  if s.id == b["section"]),
                  "Work": b["title"]} for b in blocks],
                width="stretch", hide_index=True)


# ══════════════════════════════════════════════════════════════════
#  CONTROLLER VIEW
# ══════════════════════════════════════════════════════════════════
def controller_view() -> None:
    st.markdown('<div class="rb-title">Plan the corridor</div>',
                unsafe_allow_html=True)
    reqs = store.list_requests()
    active = [r for r in reqs if r["status"] != "deferred"]
    st.markdown(
        f'<div class="rb-sub">{len(sections)} sections · {len(active)} live '
        f'requests · {len(windows)} traffic-free windows · {DAYS}-day '
        f'horizon</div>', unsafe_allow_html=True)

    if not active:
        st.info("No requests to plan. Departments submit from their own view.")
        return

    c1, c2 = st.columns([3, 1])
    urgency = c1.slider(
        "Planning priority", 0.0, 1.0, 0.5, 0.05,
        help="Left: protect train service by using the least disruptive "
             "windows. Right: clear urgent work as early as possible.")
    strict = c2.toggle(
        "Every request is mandatory",
        help="On: demand that all of them fit, and if they cannot, identify "
             "exactly which requests are in conflict.")
    l, r = st.columns(2)
    l.caption("◀ protect service")
    r.caption("clear urgent ▶")

    try:
        with st.spinner("Solving…"):
            sc, sol, violations = run_solver(signature(), DAYS, strict, urgency)
    except Exception as e:                                  # noqa: BLE001
        st.error(f"The solver could not run: {e}")
        st.caption("Check that the corridor loaded correctly, then try again.")
        return

    # ── Infeasible ───────────────────────────────────────────
    if not sol.ok:
        from railblock.model import explain_conflict
        m1, m2, m3 = st.columns(3)
        m1.metric("Result", "No valid plan")
        m2.metric("Requests in conflict", len(sol.conflict))
        m3.metric("Proved in", f"{sol.solve_time * 1000:.0f} ms")
        st.markdown(
            '<div class="rb-bad"><b>These requests cannot coexist.</b><br>'
            + explain_conflict(sc, sol.conflict) + "</div>",
            unsafe_allow_html=True)
        st.caption("This set is irreducible — deferring any one of them "
                   "makes the rest solvable.")
        st.write("")
        for rid in sol.conflict:
            rq = sc.request(rid)
            a, b, c, d, e = st.columns([1, 4, 3, 2, 1.3])
            a.markdown(f"**{rid}**")
            b.markdown(rq.title)
            c.caption(f"{DEPT_NAME.get(rq.dept, rq.dept)} · "
                      f"{sc.section_name(rq.section)}")
            d.caption(f"{rq.duration} min · P{rq.priority}")
            if e.button("Defer", key=f"defer{rid}"):
                store.set_status([rid], "deferred", actor)
                st.success(f"{rid} deferred — re-solving.")
                st.rerun()
        return

    # ── A plan ───────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Result", "Proven optimal" if sol.proven_optimal else "Feasible")
    m2.metric("Blocks scheduled", f"{len(sol.blocks)} / {len(sc.requests)}")
    m3.metric("Solved in", f"{sol.solve_time * 1000:.0f} ms")
    m4.metric("Rule violations", len(violations))

    st.pyplot(gantt(sc, sol), width="stretch")

    if violations:
        st.markdown('<div class="rb-bad"><b>Verification failed</b><br>'
                    + "<br>".join(violations) + "</div>",
                    unsafe_allow_html=True)
    else:
        st.markdown(
            f'<div class="rb-good"><b>Independently verified.</b> All '
            f'{len(sol.blocks)} blocks re-checked against the rules from '
            f'scratch: no section double-booked, every block inside a '
            f'traffic-free window, no deadline missed, crew limits '
            f'respected.</div>', unsafe_allow_html=True)

    # ── Explanation panel ────────────────────────────────────
    with st.expander("Explain a block", expanded=False):
        options = [r.id for r in sc.requests]
        label = {r.id: f"{r.id} — {r.title} ({sc.section_name(r.section)})"
                 for r in sc.requests}
        pick = st.selectbox("Pick a request", options,
                            format_func=lambda i: label[i],
                            key="explain_pick")
        why = explain_why(sc, sol, pick)
        box = "rb-good" if why.scheduled else "rb-bad"
        st.markdown(f'<div class="{box}"><b>{why.headline}</b></div>',
                    unsafe_allow_html=True)
        st.write("")
        for reason in why.reasons:
            st.markdown(f"- {reason}")
        if why.alternatives:
            st.markdown("**Windows considered on this section**")
            st.dataframe(
                [{"Window": a.window, "Day": a.day, "Time": a.span,
                  "Verdict": "OK" if a.ok else "ruled out",
                  "Why": a.why} for a in why.alternatives],
                width="stretch", hide_index=True)

    st.write("")
    if st.button("Publish as the block order", type="primary"):
        pid = store.save_plan(sol, DAYS, urgency, strict, actor)
        store.publish_plan(pid, actor)
        st.success(f"Published as plan #{pid}. Departments can now see it.")
        st.rerun()

    if sol.unscheduled:
        with st.expander(f"Not scheduled ({len(sol.unscheduled)})"):
            st.caption("The solver kept the highest-value work and dropped "
                       "what could not fit. Switch on \"every request is "
                       "mandatory\" to see exactly why.")
            for rid in sol.unscheduled:
                rq = sc.request(rid)
                st.markdown(f"**{rid}** — {rq.title} · "
                            f"{sc.section_name(rq.section)} · "
                            f"{rq.duration} min · P{rq.priority}")


# ══════════════════════════════════════════════════════════════════
#  BLOCK ORDERS
# ══════════════════════════════════════════════════════════════════
def block_orders_view() -> None:
    st.markdown('<div class="rb-title">Block orders</div>',
                unsafe_allow_html=True)
    pub = store.published_plan()
    if not pub:
        st.info("No block order published yet.")
        return

    blocks = sorted(store.plan_blocks(pub["id"]),
                    key=lambda b: (b["start"], b["section"]))
    st.markdown(f'<div class="rb-sub">Plan #{pub["id"]} · published '
                f'{pub["created_at"]} · {len(blocks)} blocks</div>',
                unsafe_allow_html=True)

    rows = [{"Day": b["start"] // DAY,
            "Time": f"{hhmm(b['start'])}–{hhmm(b['end'])}",
            "Section": next(s.name for s in sections if s.id == b["section"]),
            "Department": DEPT_NAME.get(b["dept"], b["dept"]),
            "Work": b["title"], "Request": b["request_id"]} for b in blocks]
    st.dataframe(rows, width="stretch", hide_index=True)

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Day", "Time", "Section", "Department", "Work", "Request"])
    for r in rows:
        writer.writerow([r["Day"], r["Time"], r["Section"], r["Department"],
                         r["Work"], r["Request"]])
    st.download_button("Download as CSV", buf.getvalue(),
                       file_name=f"block_order_plan_{pub['id']}.csv",
                       mime="text/csv")


# ══════════════════════════════════════════════════════════════════
#  ACTIVITY LOG
# ══════════════════════════════════════════════════════════════════
def activity_log_view() -> None:
    st.markdown('<div class="rb-title">Activity log</div>',
                unsafe_allow_html=True)
    rows = store.activity(limit=200)
    if not rows:
        st.info("No activity yet.")
        return

    actors = sorted({r["actor"] for r in rows})
    pick = st.selectbox("Filter by actor", ["All"] + actors)
    if pick != "All":
        rows = [r for r in rows if r["actor"] == pick]

    st.dataframe(
        [{"When": r["at"], "Actor": r["actor"], "Action": r["action"],
          "Detail": r["detail"]} for r in rows],
        width="stretch", hide_index=True)


# ══════════════════════════════════════════════════════════════════
if dept is None:
    tab_plan, tab_orders, tab_log = st.tabs(
        ["Plan the corridor", "Block orders", "Activity log"])
    with tab_plan:
        controller_view()
    with tab_orders:
        block_orders_view()
    with tab_log:
        activity_log_view()
else:
    department_view(dept, role_name)

st.caption("Google OR-Tools CP-SAT · no model training, no historical data · "
           "the solver proves the plan is optimal rather than predicting it.")

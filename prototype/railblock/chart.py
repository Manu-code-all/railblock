"""Gantt rendering for a solved corridor plan (matplotlib, no UI deps)."""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from .model import Scenario, Solution
from .scenarios import DEPT_NAME

DEPT_COLOUR = {"ENGG": "#2E6DA4", "S&T": "#1E8449", "TRD": "#CA8A04"}
WINDOW_FILL = "#E8EDF3"
GRID = "#D6DCE5"


def gantt(scenario: Scenario, solution: Solution):
    """Draw the block plan: sections down the side, time across."""
    secs = scenario.sections
    fig, ax = plt.subplots(figsize=(15, 0.62 * len(secs) + 1.5))
    ypos = {s.id: i for i, s in enumerate(secs)}
    H = 0.56

    # Show only the days the plan actually touches (plus one), so bars stay
    # readable instead of shrinking into a week of blank chart.
    used = max((b.day for b in solution.blocks), default=0)
    shown = min(scenario.days, used + 1)

    # Traffic-free windows, so it is visibly obvious every block sits in one.
    for w in scenario.windows:
        if w.day >= shown:
            continue
        ax.broken_barh([(w.start / 60, w.length / 60)],
                       (ypos[w.section] - H / 2, H),
                       facecolors=WINDOW_FILL, edgecolors="none", zorder=1)

    for b in solution.blocks:
        x, wdt = b.start / 60, (b.end - b.start) / 60
        ax.broken_barh([(x, wdt)], (ypos[b.section] - H / 2, H),
                       facecolors=DEPT_COLOUR.get(b.dept, "#666666"),
                       edgecolors="white", linewidth=1.2, zorder=3)
        if wdt >= 1.4:
            ax.text(x + wdt / 2, ypos[b.section], b.request,
                    ha="center", va="center", color="white",
                    fontsize=8, fontweight="bold", zorder=4)

    for d in range(shown + 1):
        ax.axvline(d * 24, color=GRID, lw=1.1, zorder=2)

    step = 3 if shown <= 2 else 6
    ticks = range(0, shown * 24 + 1, step)
    ax.set_yticks(range(len(secs)))
    ax.set_yticklabels([s.name for s in secs], fontsize=9)
    ax.set_xlim(0, shown * 24)
    ax.set_xticks(list(ticks))
    ax.set_xticklabels(
        [f"{(h % 24):02d}:00" if h % 24 else f"Day {h // 24}" for h in ticks],
        fontsize=8)
    ax.set_ylim(len(secs) - 0.5, -0.5)
    ax.grid(axis="x", color=GRID, lw=0.5, alpha=0.5, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)

    ax.legend(
        handles=[mpatches.Patch(color=c, label=DEPT_NAME.get(d, d))
                 for d, c in DEPT_COLOUR.items()]
        + [mpatches.Patch(color=WINDOW_FILL, label="Traffic-free window")],
        loc="upper center", bbox_to_anchor=(0.5, 1.16), ncol=4,
        frameon=False, fontsize=9)
    fig.tight_layout()
    return fig

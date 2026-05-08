"""Plotting helpers — light evocation of the 3B1B aesthetic.

Not a faithful reproduction of Manim's style. A muted dark background, soft
grid, and a hand-picked qualitative palette so plots in Phases 1–4 feel
coherent across notebooks.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# Palette borrowed loosely from 3B1B's blue/yellow accents.
_PALETTE: tuple[str, ...] = (
    "#3B83BD",  # 3blue
    "#E6B800",  # warm yellow
    "#B5403A",  # muted red
    "#5C9E62",  # muted green
    "#9B6BB0",  # muted violet
)


def setup_3b1b_style() -> None:
    """Apply repo-wide matplotlib style. Idempotent."""
    plt.rcParams.update(
        {
            "figure.facecolor": "#1B1F2A",
            "axes.facecolor": "#1B1F2A",
            "axes.edgecolor": "#888888",
            "axes.labelcolor": "#DDDDDD",
            "xtick.color": "#BBBBBB",
            "ytick.color": "#BBBBBB",
            "text.color": "#DDDDDD",
            "grid.color": "#333333",
            "grid.linestyle": "--",
            "axes.grid": True,
            "axes.prop_cycle": plt.cycler(color=list(_PALETTE)),
            "font.size": 11,
            "axes.titlesize": 13,
        }
    )

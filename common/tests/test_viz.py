"""Tests for common.viz."""

import matplotlib

matplotlib.use("Agg")  # headless backend for CI-style runs

import matplotlib.pyplot as plt

from common import viz


def test_setup_3b1b_style_runs_without_error() -> None:
    viz.setup_3b1b_style()


def test_setup_3b1b_style_changes_rcparams() -> None:
    plt.rcdefaults()
    before = plt.rcParams["axes.facecolor"]
    viz.setup_3b1b_style()
    after = plt.rcParams["axes.facecolor"]
    assert before != after

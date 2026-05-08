"""Reproducibility helpers.

`seed_all(seed)` seeds every RNG that experiments in this repo touch. Today
that's Python's `random` and NumPy's global state. PyTorch is added here when
Phase 3 starts.
"""

from __future__ import annotations

import random

import numpy as np


def seed_all(seed: int) -> int:
    """Seed Python's random module and NumPy's global RNG.

    Returns the seed for chaining/logging.
    """
    random.seed(seed)
    np.random.seed(seed)
    return seed

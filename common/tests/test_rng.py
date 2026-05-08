"""Tests for common.rng."""

import random

import numpy as np

from common import rng


def test_seed_all_makes_python_random_deterministic() -> None:
    rng.seed_all(42)
    a = [random.random() for _ in range(5)]
    rng.seed_all(42)
    b = [random.random() for _ in range(5)]
    assert a == b


def test_seed_all_makes_numpy_deterministic() -> None:
    rng.seed_all(42)
    a = np.random.standard_normal(5)
    rng.seed_all(42)
    b = np.random.standard_normal(5)
    assert np.allclose(a, b)


def test_seed_all_returns_seed() -> None:
    assert rng.seed_all(123) == 123

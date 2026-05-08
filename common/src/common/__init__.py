"""Shared utilities used across all phase packages.

Exposes the four submodules (`rng`, `data`, `viz`, `logging`) via the package
namespace so callers can write `from common import rng`.
"""

from . import data, logging, rng, viz

__all__ = ["data", "logging", "rng", "viz"]

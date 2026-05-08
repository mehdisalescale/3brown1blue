"""Dataset cache helpers.

`cache_dir()` returns a writable, gitignored directory under the repo root
where datasets (MNIST, CIFAR, Tiny-Shakespeare, etc.) are downloaded once
and reused across projects.
"""

from __future__ import annotations

from pathlib import Path


def _repo_root() -> Path:
    """Walk up from this file to the workspace root (the dir containing pyproject.toml with [tool.uv.workspace])."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "pyproject.toml"
        if candidate.exists() and "[tool.uv.workspace]" in candidate.read_text():
            return parent
    raise RuntimeError("Could not locate workspace root from common.data")


def cache_dir() -> Path:
    """Return (and create if missing) the dataset cache directory at <repo>/data/cache."""
    path = _repo_root() / "data" / "cache"
    path.mkdir(parents=True, exist_ok=True)
    return path

# 3brown1blue Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the standalone `3brown1blue` git repository as a `uv` workspace with all six phase skeletons, a shared `common/` package, a `posts/` folder for learn-in-public writing, and a baseline tooling setup — ready for the user to begin Phase 1 Project 01 immediately after the plan completes.

**Architecture:** Standalone git repo at `/Users/bm/ML/3brown1blue/`, separate from the parent `/Users/bm/ML/` repo (own remote, own identity files). `uv` workspace with seven members: `common/` plus `phase-01-math/` through `phase-06-production/`. Each phase folder is identically shaped (`pyproject.toml`, `README.md`, `SOURCES.md`, `journal.md`, `src/phase_NN_<slug>/`, `projects/NN-<slug>/`). Phases 1–3 lean on Jupyter notebooks; phases 4–6 lean on `.py` modules + pytest. Phase 5–6 will use Ollama for local LLMs and chroma for vector storage — those deps are *declared in the phase pyproject* but not installed/exercised during bootstrap. Pre-commit hooks enforce ruff format + lint on commit. Posts live in `posts/` as plain markdown (SSG choice deferred).

**Tech Stack:** Python 3.13, `uv` (workspace), `ruff`, `mypy`, `pytest`, `pre-commit`, `direnv`, `git`, `gh`. `numpy`, `matplotlib`, `jupyter` enter at Phase 1. `torch` enters at Phase 3. `ollama` Python client + `chromadb` enter at Phase 5. `fastapi` + `uvicorn` enter at Phase 6. None of the heavy deps are installed in this bootstrap — they're declared in their phase's `pyproject.toml`, but `uv sync` won't pull phase deps unless the phase is selected.

**Scope of this plan:** *Bootstrap only.* Implementing curriculum content (the actual ~38 projects' code) is explicitly out of scope — that's the user's ongoing learning journey, not infrastructure. This plan ends when the user can `cd projects/01-vectors-and-linear-maps && jupyter notebook notes.ipynb` and start working.

---

## Pre-flight inputs (block on these before Task 1)

The agent MUST gather these from the user before any file is written. They cannot be defaulted automatically.

| Input | What's needed | Why |
|---|---|---|
| `<identity>` | Name of the `sid` identity that owns this repo (run `sid --list` and read the user's choice) | Written into `.sid-identity` and `.envrc`; binds git/SSH/gh/gcloud to the right account. Per global rules, missing this blocks any push/deploy. |
| `<gh-repo-name>` | Public GitHub repo slug (default: `3brown1blue`) | Used in `gh repo create`. The local directory name does not have to match the GitHub slug. |
| `<gh-org-or-user>` | GitHub owner (default: the user account associated with `<identity>`) | `gh` will infer from auth, but confirm before creation to avoid wrong-org pushes. |

**Surface these as a single question to the user before Task 1 begins.** Example phrasing: "Before I start scaffolding, I need three answers: (1) which `sid` identity owns this repo? (2) GitHub repo name — default `3brown1blue` or something else? (3) GitHub owner — default is the user tied to that identity, override if it should land in an org."

If the user is not available to answer, **stop**. Do not invent defaults for these; identity mismatches are the highest-cost failure mode on this machine.

---

## Decisions resolved for this plan

The spec's "Open decisions" section listed 10 items. This plan resolves them as follows. The agent does not need to re-ask the user about these — they are already decided.

| # | Decision | Resolution |
|---|---|---|
| 1 | Notebook tool | **Jupyter** (`jupyter` + `jupyterlab`). Marimo deferred — re-evaluate if/when a phase is reached where it would help. |
| 2 | Volume per phase | **6–7 projects per phase** as written in spec Section 4. No trimming. |
| 3 | Coverage gaps (interp / RLHF / multimodal / diffusion) | **Deferred.** Not added in bootstrap. Recorded in `ROADMAP.md` "Future considerations" section. |
| 4 | Stretch markers | `phase-04/projects/06-llm-c-walkthrough` and `phase-06/projects/06-deploy-real` path (b). Documented in each project's README. |
| 5 | Resources management | **Linked-only.** `Resources/` contains `README.md` listing how to acquire each resource. Heavy files gitignored via `Resources/**` + `!Resources/README.md` whitelist. |
| 6 | Default local model | **Deferred to Phase 5.** The phase 5 pyproject declares `ollama` Python client; the README directs the user to benchmark candidates on their hardware before pinning. |
| 7 | Blog SSG | **Deferred.** Posts ship as plain markdown in `posts/`. SSG choice happens before first publish, not before first post. |
| 8 | Blog hosting | **Deferred.** Same reason as #7. |
| 9 | Cross-posting policy | **Deferred.** No automation built. Per-post manual decision when posting. |
| 10 | GitHub repo name | **`<gh-repo-name>` from pre-flight inputs** (default: `3brown1blue`). |

---

## File map

Every file the bootstrap creates, by responsibility. Tasks below reference these paths exactly.

### Repo root

| Path | Purpose |
|---|---|
| `.gitignore` | Python / uv / Jupyter / macOS / direnv / heavy-asset ignores |
| `.python-version` | Pin Python 3.13 for `uv` to install |
| `.sid-identity` | Identity pin (single line: `<identity>`) |
| `.envrc` | direnv config: `use_identity <identity>` |
| `pyproject.toml` | uv workspace root + ruff / mypy / pytest config |
| `uv.lock` | Generated by `uv sync` — committed |
| `.pre-commit-config.yaml` | Ruff, ruff-format, trailing-whitespace, end-of-file-fixer hooks |
| `README.md` | Journey overview + how to navigate |
| `ROADMAP.md` | Flat checklist of all ~38 projects in canonical order |
| `playlist-map.md` | 3B1B chapter/video → phase mapping |
| `CHANGELOG.md` | Loose changelog (optional, kept minimal) |

### `common/` package

| Path | Purpose |
|---|---|
| `common/pyproject.toml` | Common-package deps (`numpy`, `matplotlib`) |
| `common/src/common/__init__.py` | Package marker; exports public surface |
| `common/src/common/rng.py` | `seed_all(seed)` — seeds Python, NumPy, (later) torch |
| `common/src/common/data.py` | `cache_dir()`, `download_to_cache(url, name)` — dataset cache helpers |
| `common/src/common/viz.py` | `setup_3b1b_style()` — matplotlib rc settings to evoke 3B1B aesthetic |
| `common/src/common/logging.py` | `get_logger(name)` — thin structured-logging wrapper |
| `common/tests/test_rng.py` | seed determinism test |
| `common/tests/test_data.py` | cache_dir() test |
| `common/tests/test_viz.py` | smoke test (no exception when applying style) |
| `common/tests/test_logging.py` | logger emits at expected level |
| `common/tests/__init__.py` | empty (pytest needs it) |

### Per-phase skeleton (×6, replace `NN` and `<slug>` per phase)

| Path | Purpose |
|---|---|
| `phase-NN-<slug>/pyproject.toml` | Phase-specific deps |
| `phase-NN-<slug>/README.md` | Phase mission + coverage checklist + project table |
| `phase-NN-<slug>/SOURCES.md` | Living anchor list (seed pool from spec Section 2) |
| `phase-NN-<slug>/journal.md` | Empty header — user appends as they go |
| `phase-NN-<slug>/src/phase_NN_<slug>/__init__.py` | Phase utilities package marker |
| `phase-NN-<slug>/projects/MM-<project-slug>/README.md` | Per-project 6-section template (one per project — 6 or 7 per phase) |
| `phase-NN-<slug>/projects/MM-<project-slug>/notes.ipynb` *(phases 1–3 only)* | Empty notebook stub |
| `phase-NN-<slug>/projects/MM-<project-slug>/<slug>.py` *(phases 4–6 only)* | Empty `.py` module stub |
| `phase-NN-<slug>/projects/MM-<project-slug>/test_<slug>.py` *(phases 4–6 only)* | Test stub with one xfail placeholder test |

### Posts + Resources

| Path | Purpose |
|---|---|
| `posts/README.md` | Index template + tag legend + "how to write a post" |
| `posts/.gitkeep` | Keeps directory in git |
| `Resources/README.md` | Lists acquisition pointers for heavy reading material |
| `Resources/.gitkeep` | Keeps directory in git |
| `scratch/.gitkeep` | Empty scratchpad (its contents are gitignored) |

### Spec / plan docs (already exist — not touched)

| Path | Purpose |
|---|---|
| `docs/superpowers/specs/2026-05-07-3brown1blue-repo-design.md` | Source-of-truth design spec |
| `docs/superpowers/plans/2026-05-07-3brown1blue-bootstrap.md` | This file |

---

## Templates referenced by multiple tasks

These are inlined here once. Tasks point to them and provide the per-instance substitutions. The agent should NOT reinterpret them — copy verbatim and substitute the `{{placeholder}}` tokens.

### Template P-README (per-project README)

````markdown
# {{phase_num}}.{{project_num}} — {{project_slug}}

{{one_line_what}}

## What

_(one sentence: what is being built)_

## Why

_(the concept(s) being internalized — why does this project exist?)_

## References

_(resources actually used while doing this project. Append as you go.)_

## Success criteria

_(explicit, checkable. Examples: "training converges in <N min on M-series Mac", "tests pass", "I can explain X to a rubber duck without notes".)_

## Run it

```bash
{{run_command_placeholder}}
```

## Notes

_(short, post-hoc. What surprised you, what tripped you up.)_

## Posts

_(blog posts that draw on this project — link them here as they're written.)_
````

### Template P-Phase-README (per-phase README)

````markdown
# Phase {{phase_num}} — {{phase_title}}

> *{{format_note}}*

## Mission

By the end of this phase, you can {{mission_clause}}.

## Coverage checklist

{{coverage_bullets}}

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
{{project_table_rows}}

## Pacing

Rough estimate, not a deadline: ~{{pacing_estimate}}. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list for this phase.
- `journal.md` — dated breadcrumbs of what clicked, what didn't.
- `../ROADMAP.md` — overall progression checklist.
````

### Template P-Phase-pyproject (per-phase `pyproject.toml`)

```toml
[project]
name = "phase-{{phase_num_padded}}-{{phase_slug}}"
version = "0.1.0"
description = "{{phase_description}}"
requires-python = ">=3.13"
dependencies = [
    "common",
{{phase_specific_deps}}
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.sources]
common = { workspace = true }

[tool.hatch.build.targets.wheel]
packages = ["src/phase_{{phase_num_padded_underscored}}_{{phase_slug_underscored}}"]
```

### Template P-Sources (per-phase `SOURCES.md` opening)

````markdown
# Sources — Phase {{phase_num}}: {{phase_title}}

> Living document. Append resources as they help. Don't list things you haven't used.

## Topic-coverage checklist

{{coverage_bullets}}

## Seed pool

_(starting points only — not prescriptions. Replace or augment as the journey goes.)_

{{seed_sources}}

## Resources I actually used

_(populated as you go. Group by topic. Cite specific videos, chapters, posts — not whole books.)_

### {{first_topic_placeholder}}

- _(empty — fill as you work)_
````

### Template P-Project-test-stub (per-project test for phases 4–6)

```python
"""Test stub for {{project_slug}} — replace xfail with real tests as you build."""

import pytest


@pytest.mark.xfail(reason="not yet implemented")
def test_{{project_slug_underscored}}_placeholder() -> None:
    raise NotImplementedError
```

### Template P-Project-py-stub (per-project module for phases 4–6)

```python
"""{{project_slug}} — {{one_line_what}}

References: see README.md for the running list.
"""
```

### Template P-Notebook-stub (per-project `notes.ipynb` for phases 1–3)

A minimal valid Jupyter notebook JSON with a single markdown cell:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# {{project_slug}}\n",
    "\n",
    "{{one_line_what}}\n",
    "\n",
    "Working notes. See `README.md` for the project frame."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.13.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

---

## Task 1: Initialize standalone git repo + identity files

**Files:**
- Create: `/Users/bm/ML/3brown1blue/.python-version`
- Create: `/Users/bm/ML/3brown1blue/.sid-identity`
- Create: `/Users/bm/ML/3brown1blue/.envrc`
- Create: `/Users/bm/ML/3brown1blue/.gitignore`

- [ ] **Step 1: Confirm working directory and that pre-flight inputs are gathered**

```bash
cd /Users/bm/ML/3brown1blue && pwd && ls -la
```
Expected: `pwd` reports `/Users/bm/ML/3brown1blue`. The only existing entry beyond `.` and `..` is `docs/`. The pre-flight inputs (`<identity>`, `<gh-repo-name>`, `<gh-org-or-user>`) are pinned. If not, stop.

- [ ] **Step 2: Initialize git on the `main` branch**

```bash
cd /Users/bm/ML/3brown1blue && git init -b main
```
Expected: `Initialized empty Git repository in /Users/bm/ML/3brown1blue/.git/` and the new repo's default branch is `main`.

- [ ] **Step 3: Write `.python-version`**

Write the file `/Users/bm/ML/3brown1blue/.python-version` with content (single line, no trailing whitespace beyond newline):

```
3.13
```

- [ ] **Step 4: Write `.sid-identity`**

Write the file `/Users/bm/ML/3brown1blue/.sid-identity` with content (substitute `<identity>`):

```
<identity>
```

- [ ] **Step 5: Write `.envrc`**

Write the file `/Users/bm/ML/3brown1blue/.envrc` with content (substitute `<identity>`):

```bash
use_identity <identity>
```

- [ ] **Step 6: Write `.gitignore`**

Write the file `/Users/bm/ML/3brown1blue/.gitignore` with content:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
env/
*.egg-info/
*.egg
.eggs/
dist/
build/

# Tooling caches
.mypy_cache/
.ruff_cache/
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/

# Editors / OS
.DS_Store
.idea/
.vscode/
*.swp
*~

# Direnv
.direnv/

# Project-local
scratch/**
!scratch/.gitkeep
.env
.env.local

# Heavy assets (linked-only policy)
Resources/**
!Resources/README.md
!Resources/.gitkeep

# Models / data caches
*.gguf
*.safetensors
*.bin
data/cache/
data/raw/
.ollama/
```

- [ ] **Step 7: Activate direnv**

```bash
cd /Users/bm/ML/3brown1blue && direnv allow .
```
Expected: a single line confirming the `.envrc` is allowed. The first prompt after this should show identity-related env vars set.

- [ ] **Step 8: Verify identity alignment**

```bash
cd /Users/bm/ML/3brown1blue && sid --check
```
Expected: no mismatches reported. If a mismatch is reported, stop and resolve before proceeding (per global identity rules — destructive shortcut to "fix" a mismatch can clobber the wrong account).

- [ ] **Step 9: Stage and commit**

```bash
cd /Users/bm/ML/3brown1blue && git add .python-version .sid-identity .envrc .gitignore && git commit -m "chore: initialize standalone repo with identity pin"
```
Expected: one commit on `main` containing exactly these four files.

---

## Task 2: Bootstrap uv workspace root

**Files:**
- Create: `/Users/bm/ML/3brown1blue/pyproject.toml`

- [ ] **Step 1: Write the workspace root `pyproject.toml`**

Write the file `/Users/bm/ML/3brown1blue/pyproject.toml` with content:

```toml
[project]
name = "threebrown-oneblue"
version = "0.0.1"
description = "A self-driven, learn-in-public path from math intuition to production AI engineering."
requires-python = ">=3.13"
dependencies = []

[tool.uv.workspace]
members = [
    "common",
    "phase-01-math",
    "phase-02-nn-from-scratch",
    "phase-03-deep-learning",
    "phase-04-transformers",
    "phase-05-llm-systems",
    "phase-06-production",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3",
    "pytest-cov>=5.0",
    "ruff>=0.7",
    "mypy>=1.13",
    "pre-commit>=4.0",
    "jupyter>=1.1",
    "jupyterlab>=4.3",
    "ipykernel>=6.29",
]

[tool.ruff]
line-length = 100
target-version = "py313"
extend-exclude = [
    "**/.ipynb_checkpoints",
    "scratch",
    "Resources",
]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "SIM", "RET", "PT"]
ignore = []

[tool.ruff.lint.per-file-ignores]
"**/test_*.py" = ["F401"]
"**/notebooks/**" = ["E402"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.13"
strict = false
ignore_missing_imports = true
exclude = [
    "scratch",
    "Resources",
    "\\.ipynb_checkpoints",
]

[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra --strict-markers --strict-config"
testpaths = [
    "common/tests",
    "phase-04-transformers/projects",
    "phase-04-transformers/tests",
    "phase-05-llm-systems/projects",
    "phase-05-llm-systems/tests",
    "phase-06-production/projects",
    "phase-06-production/tests",
]
python_files = ["test_*.py"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "gpu: requires a GPU/MPS-capable accelerator",
]
```

- [ ] **Step 2: Stage but DO NOT commit yet**

```bash
cd /Users/bm/ML/3brown1blue && git add pyproject.toml
```

(Commit happens after Task 3 — the workspace is broken until at least one member exists, so committing both together leaves `main` always green.)

---

## Task 3: Create the `common/` package shell

**Files:**
- Create: `/Users/bm/ML/3brown1blue/common/pyproject.toml`
- Create: `/Users/bm/ML/3brown1blue/common/src/common/__init__.py`
- Create: `/Users/bm/ML/3brown1blue/common/src/common/py.typed`
- Create: `/Users/bm/ML/3brown1blue/common/tests/__init__.py`

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p common/src/common common/tests
```

- [ ] **Step 2: Write `common/pyproject.toml`**

```toml
[project]
name = "common"
version = "0.1.0"
description = "Shared utilities used across phase packages: RNG, data caching, plotting, logging."
requires-python = ">=3.13"
dependencies = [
    "numpy>=2.1",
    "matplotlib>=3.9",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/common"]
```

- [ ] **Step 3: Write `common/src/common/__init__.py`**

```python
"""Shared utilities used across all phase packages.

Exposes the four submodules (`rng`, `data`, `viz`, `logging`) via the package
namespace so callers can write `from common import rng`.
"""

from common import data, logging, rng, viz

__all__ = ["data", "logging", "rng", "viz"]
```

- [ ] **Step 4: Write `common/src/common/py.typed`**

Empty file (PEP 561 marker that the package ships type information):

```
```

- [ ] **Step 5: Write `common/tests/__init__.py`**

Empty file:

```
```

- [ ] **Step 6: Verify directory structure**

```bash
cd /Users/bm/ML/3brown1blue && find common -type f | sort
```

Expected output (exactly):

```
common/pyproject.toml
common/src/common/__init__.py
common/src/common/py.typed
common/tests/__init__.py
```

- [ ] **Step 7: Stage**

```bash
cd /Users/bm/ML/3brown1blue && git add common/
```

- [ ] **Step 8: Run `uv sync` to verify the workspace is well-formed**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
```

Expected: a `.venv/` is created, `numpy` and `matplotlib` are installed, no errors. `uv.lock` appears in repo root.

- [ ] **Step 9: Stage `uv.lock` and commit the workspace + common shell**

```bash
cd /Users/bm/ML/3brown1blue && git add uv.lock && git commit -m "chore: bootstrap uv workspace + common package shell"
```

---

## Task 4: TDD `common.rng` module

**Files:**
- Create: `/Users/bm/ML/3brown1blue/common/tests/test_rng.py`
- Create: `/Users/bm/ML/3brown1blue/common/src/common/rng.py`

- [ ] **Step 1: Write the failing test**

Write `/Users/bm/ML/3brown1blue/common/tests/test_rng.py`:

```python
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
    a = np.random.default_rng().standard_normal(5)
    rng.seed_all(42)
    b = np.random.default_rng().standard_normal(5)
    assert np.allclose(a, b)


def test_seed_all_returns_seed() -> None:
    assert rng.seed_all(123) == 123
```

- [ ] **Step 2: Run the test and verify it fails**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_rng.py -v
```

Expected: tests fail because `common.rng` does not exist yet (or `seed_all` is undefined). The error mentions `ModuleNotFoundError: No module named 'common.rng'` or similar.

- [ ] **Step 3: Implement the minimum to pass**

Write `/Users/bm/ML/3brown1blue/common/src/common/rng.py`:

```python
"""Reproducibility helpers.

`seed_all(seed)` seeds every RNG that experiments in this repo touch. Today
that's Python's `random` and NumPy's global state plus a freshly-seeded
default generator. PyTorch is added here when Phase 3 starts.
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
    # Re-create the default generator so np.random.default_rng() is also seeded.
    np.random.default_rng(seed)
    return seed
```

Note on the second NumPy assertion: because `np.random.default_rng()` (no seed) returns a fresh generator each call, the test relies on `np.random.seed(seed)` having seeded the global state that `default_rng()` then samples from. Verify by running.

- [ ] **Step 4: Run tests and verify pass**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_rng.py -v
```

Expected: 3 passed.

If `test_seed_all_makes_numpy_deterministic` fails, replace its body with the more reliable form:

```python
def test_seed_all_makes_numpy_deterministic() -> None:
    rng.seed_all(42)
    a = np.random.standard_normal(5)
    rng.seed_all(42)
    b = np.random.standard_normal(5)
    assert np.allclose(a, b)
```

(Using `np.random.standard_normal` directly samples from the seeded global state.)

- [ ] **Step 5: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add common/src/common/rng.py common/tests/test_rng.py && git commit -m "feat(common): add seed_all reproducibility helper"
```

---

## Task 5: TDD `common.data` module

**Files:**
- Create: `/Users/bm/ML/3brown1blue/common/tests/test_data.py`
- Create: `/Users/bm/ML/3brown1blue/common/src/common/data.py`

- [ ] **Step 1: Write the failing test**

Write `/Users/bm/ML/3brown1blue/common/tests/test_data.py`:

```python
"""Tests for common.data."""

from pathlib import Path

from common import data


def test_cache_dir_returns_path() -> None:
    p = data.cache_dir()
    assert isinstance(p, Path)


def test_cache_dir_creates_directory() -> None:
    p = data.cache_dir()
    assert p.exists()
    assert p.is_dir()


def test_cache_dir_under_repo_root() -> None:
    p = data.cache_dir()
    # Must live under data/cache/ at repo root — gitignored.
    assert p.name == "cache"
    assert p.parent.name == "data"
```

- [ ] **Step 2: Run and verify fail**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_data.py -v
```

Expected: tests fail (`No module named 'common.data'`).

- [ ] **Step 3: Implement**

Write `/Users/bm/ML/3brown1blue/common/src/common/data.py`:

```python
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
```

- [ ] **Step 4: Run tests and verify pass**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_data.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Verify the cache directory got created and is gitignored**

```bash
cd /Users/bm/ML/3brown1blue && ls -la data/cache && git check-ignore data/cache/
```

Expected: directory exists; `git check-ignore` prints `data/cache/` (confirming it's ignored).

- [ ] **Step 6: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add common/src/common/data.py common/tests/test_data.py && git commit -m "feat(common): add cache_dir helper for dataset downloads"
```

---

## Task 6: TDD `common.viz` module

**Files:**
- Create: `/Users/bm/ML/3brown1blue/common/tests/test_viz.py`
- Create: `/Users/bm/ML/3brown1blue/common/src/common/viz.py`

- [ ] **Step 1: Write the failing test**

Write `/Users/bm/ML/3brown1blue/common/tests/test_viz.py`:

```python
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
    # We don't care which exact color — just that the style modifies the rc.
    assert before != after
```

- [ ] **Step 2: Run and verify fail**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_viz.py -v
```

Expected: tests fail (`No module named 'common.viz'`).

- [ ] **Step 3: Implement**

Write `/Users/bm/ML/3brown1blue/common/src/common/viz.py`:

```python
"""Plotting helpers — light evocation of the 3B1B aesthetic.

Not a faithful reproduction of Manim's style. A muted dark background, soft
grid, and a hand-picked qualitative palette so plots in Phases 1–4 feel
coherent across notebooks.
"""

from __future__ import annotations

import matplotlib.pyplot as plt

# Palette borrowed loosely from 3B1B's blue/yellow accents. Keep small.
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
```

- [ ] **Step 4: Run tests and verify pass**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_viz.py -v
```

Expected: 2 passed.

- [ ] **Step 5: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add common/src/common/viz.py common/tests/test_viz.py && git commit -m "feat(common): add setup_3b1b_style matplotlib helper"
```

---

## Task 7: TDD `common.logging` module

**Files:**
- Create: `/Users/bm/ML/3brown1blue/common/tests/test_logging.py`
- Create: `/Users/bm/ML/3brown1blue/common/src/common/logging.py`

- [ ] **Step 1: Write the failing test**

Write `/Users/bm/ML/3brown1blue/common/tests/test_logging.py`:

```python
"""Tests for common.logging."""

import logging as stdlib_logging

from common import logging as repo_logging


def test_get_logger_returns_logger_instance() -> None:
    log = repo_logging.get_logger("test")
    assert isinstance(log, stdlib_logging.Logger)


def test_get_logger_namespaces_under_3brown1blue() -> None:
    log = repo_logging.get_logger("phase01.foo")
    assert log.name == "3brown1blue.phase01.foo"


def test_get_logger_default_level_info() -> None:
    log = repo_logging.get_logger("level_check")
    assert log.getEffectiveLevel() == stdlib_logging.INFO
```

- [ ] **Step 2: Run and verify fail**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_logging.py -v
```

Expected: tests fail (module missing).

- [ ] **Step 3: Implement**

Write `/Users/bm/ML/3brown1blue/common/src/common/logging.py`:

```python
"""Logging helpers.

`get_logger(name)` returns a logger namespaced under `3brown1blue.*` so the
whole repo's logs can be filtered as one tree. Idempotent — repeated calls
return the same logger.

Configuration is intentionally minimal here. Phase 6 (`observability`)
replaces this with structured logging via `structlog` + OpenTelemetry; the
swap should be source-compatible.
"""

from __future__ import annotations

import logging
import sys

_ROOT_LOGGER_NAME = "3brown1blue"
_configured = False


def _configure_root_once() -> None:
    global _configured
    if _configured:
        return
    root = logging.getLogger(_ROOT_LOGGER_NAME)
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s — %(message)s")
    )
    root.addHandler(handler)
    root.propagate = False
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a logger named `3brown1blue.<name>`."""
    _configure_root_once()
    return logging.getLogger(f"{_ROOT_LOGGER_NAME}.{name}")
```

- [ ] **Step 4: Run tests and verify pass**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests/test_logging.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Run all common tests together**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest common/tests -v
```

Expected: all of `test_rng.py`, `test_data.py`, `test_viz.py`, `test_logging.py` pass — 11 tests total.

- [ ] **Step 6: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add common/src/common/logging.py common/tests/test_logging.py && git commit -m "feat(common): add get_logger namespaced under 3brown1blue"
```

---

## Task 8: Pre-commit hooks

**Files:**
- Create: `/Users/bm/ML/3brown1blue/.pre-commit-config.yaml`

- [ ] **Step 1: Write `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ["--maxkb=512"]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format
```

- [ ] **Step 2: Install the hook**

```bash
cd /Users/bm/ML/3brown1blue && uv run pre-commit install
```

Expected: `pre-commit installed at .git/hooks/pre-commit`.

- [ ] **Step 3: Run on the existing tree to verify**

```bash
cd /Users/bm/ML/3brown1blue && uv run pre-commit run --all-files
```

Expected: all hooks pass. If a hook auto-fixes something, run `git add -u && uv run pre-commit run --all-files` again until clean.

- [ ] **Step 4: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add .pre-commit-config.yaml && git commit -m "chore: add pre-commit hooks (ruff, basic file checks)"
```

---

## Task 9: Scaffold Phase 1 (math, notebooks-dominant)

**Files (8 files for the phase + 6 project subtrees):**
- Create: `phase-01-math/pyproject.toml`
- Create: `phase-01-math/README.md`
- Create: `phase-01-math/SOURCES.md`
- Create: `phase-01-math/journal.md`
- Create: `phase-01-math/src/phase_01_math/__init__.py`
- Create: `phase-01-math/projects/01-vectors-and-linear-maps/{README.md, notes.ipynb}`
- Create: `phase-01-math/projects/02-eigenstuff/{README.md, notes.ipynb}`
- Create: `phase-01-math/projects/03-pca-from-scratch/{README.md, notes.ipynb}`
- Create: `phase-01-math/projects/04-derivatives-and-chain-rule/{README.md, notes.ipynb}`
- Create: `phase-01-math/projects/05-gradient-descent-by-hand/{README.md, notes.ipynb}`
- Create: `phase-01-math/projects/06-probability-essentials/{README.md, notes.ipynb}`

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p \
  phase-01-math/src/phase_01_math \
  phase-01-math/projects/01-vectors-and-linear-maps \
  phase-01-math/projects/02-eigenstuff \
  phase-01-math/projects/03-pca-from-scratch \
  phase-01-math/projects/04-derivatives-and-chain-rule \
  phase-01-math/projects/05-gradient-descent-by-hand \
  phase-01-math/projects/06-probability-essentials \
  phase-01-math/notebooks \
  phase-01-math/tests
```

- [ ] **Step 2: Write `phase-01-math/pyproject.toml`**

Apply Template P-Phase-pyproject with:
- `phase_num_padded` = `01`
- `phase_slug` = `math`
- `phase_num_padded_underscored` = `01`
- `phase_slug_underscored` = `math`
- `phase_description` = `Math intuition: linear algebra, calculus, gradients, probability — the foundation for everything else.`
- `phase_specific_deps` = (these lines, with leading 4-space indent):

```
    "numpy>=2.1",
    "matplotlib>=3.9",
    "scipy>=1.14",
    "ipykernel>=6.29",
    "ipywidgets>=8.1",
```

Final file `/Users/bm/ML/3brown1blue/phase-01-math/pyproject.toml`:

```toml
[project]
name = "phase-01-math"
version = "0.1.0"
description = "Math intuition: linear algebra, calculus, gradients, probability — the foundation for everything else."
requires-python = ">=3.13"
dependencies = [
    "common",
    "numpy>=2.1",
    "matplotlib>=3.9",
    "scipy>=1.14",
    "ipykernel>=6.29",
    "ipywidgets>=8.1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.sources]
common = { workspace = true }

[tool.hatch.build.targets.wheel]
packages = ["src/phase_01_math"]
```

- [ ] **Step 3: Write `phase-01-math/src/phase_01_math/__init__.py`**

```python
"""Phase 1 — Math intuition. Shared utilities used across multiple projects in this phase."""
```

- [ ] **Step 4: Write `phase-01-math/README.md`**

Apply Template P-Phase-README:

```markdown
# Phase 01 — Math intuition

> *Notebooks dominant; primarily NumPy + matplotlib.*

## Mission

By the end of this phase, you can read a typical ML paper's math section without it feeling foreign — vectors and linear maps, eigen-stuff, gradients via the chain rule, and basic probability live in your head as pictures, not formulas.

## Coverage checklist

- [ ] Vectors, matrices, linear maps as geometric transformations
- [ ] Eigenvalues / eigenvectors and what they mean
- [ ] PCA from variance-maximization first principles
- [ ] Derivatives, partial derivatives, chain rule
- [ ] Gradients as direction-of-steepest-ascent; gradient descent
- [ ] Bayes rule, expectation, variance, CLT

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `vectors-and-linear-maps` | NumPy matrix ops + animated 2D/3D linear transformations (3B1B-style). | ☐ |
| 02 | `eigenstuff` | Power iteration, eigen decomposition by hand on small matrices, geometric intuition. | ☐ |
| 03 | `pca-from-scratch` | Derive PCA from variance maximization; run on Iris + MNIST; compare to sklearn. | ☐ |
| 04 | `derivatives-and-chain-rule` | Symbolic derivations + numerical finite-difference verification; gradient as direction of steepest ascent. | ☐ |
| 05 | `gradient-descent-by-hand` | GD on Rosenbrock + paraboloid; visualize paths; vanilla / momentum / lr sweeps. | ☐ |
| 06 | `probability-essentials` | Bayes (medical-test paradox, Monty Hall), expectation/variance derivations, CLT demo. | ☐ |

## Pacing

Rough estimate, not a deadline: ~6–10 weeks of evenings/weekends. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list for this phase.
- `journal.md` — dated breadcrumbs of what clicked, what didn't.
- `../ROADMAP.md` — overall progression checklist.
```

- [ ] **Step 5: Write `phase-01-math/SOURCES.md`**

```markdown
# Sources — Phase 01: Math intuition

> Living document. Append resources as they help. Don't list things you haven't used.

## Topic-coverage checklist

- [ ] Vectors, matrices, linear maps as geometric transformations
- [ ] Eigenvalues / eigenvectors and what they mean
- [ ] PCA from variance-maximization first principles
- [ ] Derivatives, partial derivatives, chain rule
- [ ] Gradients as direction-of-steepest-ascent; gradient descent
- [ ] Bayes rule, expectation, variance, CLT

## Seed pool

_(starting points only — not prescriptions. Replace or augment as the journey goes.)_

- 3Blue1Brown — *Essence of Linear Algebra* (full series).
- 3Blue1Brown — *Essence of Calculus* (full series).
- 3Blue1Brown — *Bayes theorem from the ground up*; *Binomial distributions*.
- Deisenroth, Faisal & Ong — *Mathematics for Machine Learning* (free at mml-book.com).
- Strang MIT 18.06 — selective lectures.

## Resources I actually used

_(populated as you go. Group by topic. Cite specific videos, chapters, posts — not whole books.)_

### Linear algebra

- _(empty — fill as you work)_

### Calculus

- _(empty — fill as you work)_

### Probability

- _(empty — fill as you work)_
```

- [ ] **Step 6: Write `phase-01-math/journal.md`**

```markdown
# Journal — Phase 01

Two-line dated entries. What clicked, what didn't. Not a blog.

---
```

- [ ] **Step 7: Write all six project READMEs**

For each project below, write `phase-01-math/projects/<NN>-<slug>/README.md` using Template P-README. Substitution table:

| NN | slug | one_line_what | run_command_placeholder |
|---|---|---|---|
| 01 | `vectors-and-linear-maps` | NumPy matrix ops + animated 2D/3D linear transformations (3B1B-style). | `uv run --package phase-01-math jupyter lab projects/01-vectors-and-linear-maps/notes.ipynb` |
| 02 | `eigenstuff` | Power iteration, eigen decomposition by hand on small matrices, geometric intuition. | `uv run --package phase-01-math jupyter lab projects/02-eigenstuff/notes.ipynb` |
| 03 | `pca-from-scratch` | Derive PCA from variance maximization; run on Iris + MNIST; compare to sklearn. | `uv run --package phase-01-math jupyter lab projects/03-pca-from-scratch/notes.ipynb` |
| 04 | `derivatives-and-chain-rule` | Symbolic derivations + numerical finite-difference verification; gradient as direction of steepest ascent. | `uv run --package phase-01-math jupyter lab projects/04-derivatives-and-chain-rule/notes.ipynb` |
| 05 | `gradient-descent-by-hand` | GD on Rosenbrock + paraboloid; visualize paths; vanilla / momentum / lr sweeps. | `uv run --package phase-01-math jupyter lab projects/05-gradient-descent-by-hand/notes.ipynb` |
| 06 | `probability-essentials` | Bayes (medical-test paradox, Monty Hall), expectation/variance derivations, CLT demo. | `uv run --package phase-01-math jupyter lab projects/06-probability-essentials/notes.ipynb` |

For each project, `phase_num` = `01` and `project_num` is the NN above.

Example expansion for the first project (`projects/01-vectors-and-linear-maps/README.md`):

````markdown
# 01.01 — vectors-and-linear-maps

NumPy matrix ops + animated 2D/3D linear transformations (3B1B-style).

## What

_(one sentence: what is being built)_

## Why

_(the concept(s) being internalized — why does this project exist?)_

## References

_(resources actually used while doing this project. Append as you go.)_

## Success criteria

_(explicit, checkable. Examples: "training converges in <N min on M-series Mac", "tests pass", "I can explain X to a rubber duck without notes".)_

## Run it

```bash
uv run --package phase-01-math jupyter lab projects/01-vectors-and-linear-maps/notes.ipynb
```

## Notes

_(short, post-hoc. What surprised you, what tripped you up.)_

## Posts

_(blog posts that draw on this project — link them here as they're written.)_
````

Repeat for the other five projects (02 through 06) with the substitutions from the table.

- [ ] **Step 8: Write all six project notebook stubs**

For each project, write `phase-01-math/projects/<NN>-<slug>/notes.ipynb` using Template P-Notebook-stub with `project_slug` and `one_line_what` from the same table.

Example for `projects/01-vectors-and-linear-maps/notes.ipynb`:

```json
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# vectors-and-linear-maps\n",
    "\n",
    "NumPy matrix ops + animated 2D/3D linear transformations (3B1B-style).\n",
    "\n",
    "Working notes. See `README.md` for the project frame."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.13.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
```

Repeat for the other five projects (02–06).

- [ ] **Step 9: Verify the phase tree**

```bash
cd /Users/bm/ML/3brown1blue && find phase-01-math -type f | sort
```

Expected (16 entries): the pyproject, README, SOURCES, journal, src `__init__.py`, and 12 files for the 6 projects (README + notes.ipynb each).

- [ ] **Step 10: `uv sync` to bring the new package into the workspace**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
```

Expected: phase-01-math is built and registered. No errors.

- [ ] **Step 11: Run pre-commit on the new files (auto-fix what's fixable)**

```bash
cd /Users/bm/ML/3brown1blue && git add phase-01-math/ uv.lock && uv run pre-commit run --files $(git diff --cached --name-only) || (git add -u && uv run pre-commit run --files $(git diff --cached --name-only))
```

Expected: hooks pass on the second invocation if the first auto-fixed anything.

- [ ] **Step 12: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git commit -m "feat(phase-01): scaffold math phase with 6 project skeletons"
```

---

## Task 10: Scaffold Phase 2 (NN from scratch, notebooks-dominant)

Same shape as Task 9. Substitutions follow.

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p \
  phase-02-nn-from-scratch/src/phase_02_nn_from_scratch \
  phase-02-nn-from-scratch/projects/01-perceptron \
  phase-02-nn-from-scratch/projects/02-mlp-numpy \
  phase-02-nn-from-scratch/projects/03-activations-and-losses \
  phase-02-nn-from-scratch/projects/04-micrograd \
  phase-02-nn-from-scratch/projects/05-mini-makemore \
  phase-02-nn-from-scratch/projects/06-optim-zoo \
  phase-02-nn-from-scratch/notebooks \
  phase-02-nn-from-scratch/tests
```

- [ ] **Step 2: Write `phase-02-nn-from-scratch/pyproject.toml`**

```toml
[project]
name = "phase-02-nn-from-scratch"
version = "0.1.0"
description = "Neural networks from scratch in NumPy: perceptron, MLP, autograd, optim zoo."
requires-python = ">=3.13"
dependencies = [
    "common",
    "numpy>=2.1",
    "matplotlib>=3.9",
    "ipykernel>=6.29",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.sources]
common = { workspace = true }

[tool.hatch.build.targets.wheel]
packages = ["src/phase_02_nn_from_scratch"]
```

- [ ] **Step 3: Write `phase-02-nn-from-scratch/src/phase_02_nn_from_scratch/__init__.py`**

```python
"""Phase 2 — Neural networks from scratch. Shared utilities used across multiple projects."""
```

- [ ] **Step 4: Write `phase-02-nn-from-scratch/README.md`**

```markdown
# Phase 02 — Neural networks from scratch

> *Notebooks dominant; NumPy only — no PyTorch yet.*

## Mission

By the end of this phase, you can implement a small MLP, train it via SGD, derive its backward pass on paper, and explain — without notes — why it works. You also have a working scalar autograd engine you wrote yourself.

## Coverage checklist

- [ ] Perceptron and the linear-separability frontier
- [ ] MLP forward + backward by hand (NumPy only)
- [ ] Activations and their derivatives; vanishing-gradient demo
- [ ] Common loss functions (CE, MSE) and their derivatives
- [ ] Scalar autograd engine (micrograd-style)
- [ ] Mini language model on names dataset
- [ ] Optimizer zoo: SGD, momentum, RMSprop, Adam by hand

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `perceptron` | Single neuron, manual weight updates, linearly separable data. | ☐ |
| 02 | `mlp-numpy` | Full MLP with manual forward+backward; train on MNIST; match a PyTorch baseline. | ☐ |
| 03 | `activations-and-losses` | ReLU/sigmoid/tanh/softmax + CE/MSE; derive derivatives; demo vanishing gradients. | ☐ |
| 04 | `micrograd` | Scalar autograd à la Karpathy; train a tiny net through your own engine. | ☐ |
| 05 | `mini-makemore` | Bigram → MLP language model on names dataset; train/val discipline. | ☐ |
| 06 | `optim-zoo` | Implement SGD/momentum/RMSprop/Adam by hand; compare on a fixed task. | ☐ |

## Pacing

Rough estimate, not a deadline: ~8–12 weeks. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list for this phase.
- `journal.md` — dated breadcrumbs of what clicked, what didn't.
- `../ROADMAP.md` — overall progression checklist.
```

- [ ] **Step 5: Write `phase-02-nn-from-scratch/SOURCES.md`**

```markdown
# Sources — Phase 02: Neural networks from scratch

> Living document. Append resources as they help. Don't list things you haven't used.

## Topic-coverage checklist

- [ ] Perceptron and the linear-separability frontier
- [ ] MLP forward + backward by hand (NumPy only)
- [ ] Activations and their derivatives; vanishing-gradient demo
- [ ] Common loss functions (CE, MSE) and their derivatives
- [ ] Scalar autograd engine (micrograd-style)
- [ ] Mini language model on names dataset
- [ ] Optimizer zoo: SGD, momentum, RMSprop, Adam by hand

## Seed pool

- 3Blue1Brown — *Neural Networks* series, Ch. 1–4 (including Ch. 4 backprop calculus).
- Karpathy — *Neural Networks: Zero to Hero* (`micrograd`, `makemore` parts 1–2).
- Michael Nielsen — *Neural Networks and Deep Learning* (free at neuralnetworksanddeeplearning.com).
- Chris Olah — *Calculus on Computational Graphs*.

## Resources I actually used

### Backpropagation

- _(empty)_

### Autograd / micrograd

- _(empty)_

### Optimizers

- _(empty)_
```

- [ ] **Step 6: Write `phase-02-nn-from-scratch/journal.md`**

```markdown
# Journal — Phase 02

Two-line dated entries. What clicked, what didn't.

---
```

- [ ] **Step 7: Write all six project READMEs and notebook stubs**

Per-project substitutions for Phase 2:

| NN | slug | one_line_what |
|---|---|---|
| 01 | `perceptron` | Single neuron, manual weight updates, linearly separable data. |
| 02 | `mlp-numpy` | Full MLP with manual forward+backward; train on MNIST; match a PyTorch baseline. |
| 03 | `activations-and-losses` | ReLU/sigmoid/tanh/softmax + CE/MSE; derive derivatives; demo vanishing gradients. |
| 04 | `micrograd` | Scalar autograd à la Karpathy; train a tiny net through your own engine. |
| 05 | `mini-makemore` | Bigram → MLP language model on names dataset; train/val discipline. |
| 06 | `optim-zoo` | Implement SGD/momentum/RMSprop/Adam by hand; compare on a fixed task. |

For each project, write `projects/<NN>-<slug>/README.md` using Template P-README with `phase_num`=`02`, `project_num`=`NN`, `project_slug`=`<slug>`, `one_line_what` per table, and `run_command_placeholder`=`uv run --package phase-02-nn-from-scratch jupyter lab projects/<NN>-<slug>/notes.ipynb`.

Then for each project write `projects/<NN>-<slug>/notes.ipynb` using Template P-Notebook-stub with the same `project_slug` and `one_line_what`.

Total: six README files + six notebook files = 12 files for this step. (Both templates are inlined verbatim in the "Templates referenced by multiple tasks" section near the top of this plan; copy-paste the template text and substitute the tokens.)

- [ ] **Step 8: `uv sync`, pre-commit, commit**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
cd /Users/bm/ML/3brown1blue && git add phase-02-nn-from-scratch/ uv.lock
cd /Users/bm/ML/3brown1blue && uv run pre-commit run --files $(git diff --cached --name-only) || (git add -u && uv run pre-commit run --files $(git diff --cached --name-only))
cd /Users/bm/ML/3brown1blue && git commit -m "feat(phase-02): scaffold nn-from-scratch phase with 6 project skeletons"
```

---

## Task 11: Scaffold Phase 3 (Deep learning, transitional)

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p \
  phase-03-deep-learning/src/phase_03_deep_learning \
  phase-03-deep-learning/projects/01-pytorch-fundamentals \
  phase-03-deep-learning/projects/02-mnist-cnn \
  phase-03-deep-learning/projects/03-cifar-resnet \
  phase-03-deep-learning/projects/04-debugging-training \
  phase-03-deep-learning/projects/05-lstm-text \
  phase-03-deep-learning/projects/06-data-pipeline \
  phase-03-deep-learning/notebooks \
  phase-03-deep-learning/tests
```

- [ ] **Step 2: Write `phase-03-deep-learning/pyproject.toml`**

```toml
[project]
name = "phase-03-deep-learning"
version = "0.1.0"
description = "Deep learning with PyTorch: CNNs, RNNs, training discipline, real data pipelines."
requires-python = ">=3.13"
dependencies = [
    "common",
    "numpy>=2.1",
    "matplotlib>=3.9",
    "torch>=2.5",
    "torchvision>=0.20",
    "datasets>=3.1",
    "ipykernel>=6.29",
    "tqdm>=4.66",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.sources]
common = { workspace = true }

[tool.hatch.build.targets.wheel]
packages = ["src/phase_03_deep_learning"]
```

- [ ] **Step 3: Write `phase-03-deep-learning/src/phase_03_deep_learning/__init__.py`**

```python
"""Phase 3 — Deep learning. Shared utilities used across multiple projects."""
```

- [ ] **Step 4: Write `phase-03-deep-learning/README.md`**

```markdown
# Phase 03 — Deep learning

> *Transitional: notebooks for exploration, modules for reusable code. PyTorch.*

## Mission

By the end of this phase, you can sit down at a fresh PyTorch project, write an idiomatic training loop, debug it when it goes sideways, and reason about why a chosen regularization or optimization technique helps.

## Coverage checklist

- [ ] PyTorch idioms: tensors, autograd, `nn.Module`, `DataLoader`
- [ ] Clean training loops with logging
- [ ] Regularization: dropout, weight decay, batchnorm
- [ ] CNNs: conv, pool, skip connections (ResNet)
- [ ] RNNs/LSTMs (briefly — to know they exist before transformers)
- [ ] Real data pipelines (multi-worker, proper splits, augmentation)
- [ ] Diagnosing training pathologies (vanishing grads, exploding loss, label leak, bad init)

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `pytorch-fundamentals` | Tensors, autograd, `nn.Module`, `DataLoader`. Reimplement Phase 2's MLP idiomatically. | ☐ |
| 02 | `mnist-cnn` | Small CNN on MNIST; conv/pool/dropout/batchnorm; clean training loop. | ☐ |
| 03 | `cifar-resnet` | ResNet-18 on CIFAR-10; skip connections, lr schedules, augmentation. | ☐ |
| 04 | `debugging-training` | Deliberately induce vanishing grads / exploding loss / label leak / bad init; diagnose. | ☐ |
| 05 | `lstm-text` | Small char-level LSTM; understand recurrence vs. MLP. | ☐ |
| 06 | `data-pipeline` | Real `Dataset` / `DataLoader` for a non-toy HF set; multi-worker, proper splits. | ☐ |

## Pacing

Rough estimate: ~10–14 weeks. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list.
- `journal.md` — dated breadcrumbs.
- `../ROADMAP.md` — overall progression.
```

- [ ] **Step 5: Write `phase-03-deep-learning/SOURCES.md`**

```markdown
# Sources — Phase 03: Deep learning

> Living document.

## Topic-coverage checklist

- [ ] PyTorch idioms (tensors, autograd, nn.Module, DataLoader)
- [ ] Clean training loops with logging
- [ ] Regularization: dropout, weight decay, batchnorm
- [ ] CNNs: conv, pool, skip connections (ResNet)
- [ ] RNNs/LSTMs (briefly)
- [ ] Real data pipelines
- [ ] Diagnosing training pathologies

## Seed pool

- fast.ai — *Practical Deep Learning for Coders* (free at course.fast.ai).
- Goodfellow, Bengio & Courville — *Deep Learning* (free, selective chapters).
- Sebastian Raschka — *Machine Learning with PyTorch and Scikit-Learn*.
- distill.pub — assorted diagrams (*Understanding LSTMs*, *Feature Visualization*).
- PyTorch official tutorials.
- *He et al.* — ResNet paper.
- *Ioffe & Szegedy* — BatchNorm paper.

## Resources I actually used

### PyTorch fundamentals

- _(empty)_

### CNNs

- _(empty)_

### Training pathologies

- _(empty)_
```

- [ ] **Step 6: Write `phase-03-deep-learning/journal.md`**

```markdown
# Journal — Phase 03

Two-line dated entries. What clicked, what didn't.

---
```

- [ ] **Step 7: Write all six project READMEs and notebook stubs**

Per-project substitutions:

| NN | slug | one_line_what |
|---|---|---|
| 01 | `pytorch-fundamentals` | Tensors, autograd, `nn.Module`, `DataLoader`. Reimplement Phase 2's MLP idiomatically. |
| 02 | `mnist-cnn` | Small CNN on MNIST; conv/pool/dropout/batchnorm; clean training loop. |
| 03 | `cifar-resnet` | ResNet-18 on CIFAR-10; skip connections, lr schedules, augmentation. |
| 04 | `debugging-training` | Deliberately induce vanishing grads / exploding loss / label leak / bad init; diagnose. |
| 05 | `lstm-text` | Small char-level LSTM; understand recurrence vs. MLP. |
| 06 | `data-pipeline` | Real `Dataset` / `DataLoader` for a non-toy HF set; multi-worker, proper splits. |

Apply Template P-README and Template P-Notebook-stub for each project, with `phase_num`=`03`, `project_num`=`NN`, `run_command_placeholder`=`uv run --package phase-03-deep-learning jupyter lab projects/<NN>-<slug>/notes.ipynb`.

- [ ] **Step 8: `uv sync` (note: this will pull torch — may take a few minutes)**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
```

Expected: PyTorch (CPU + MPS-capable build) and torchvision are downloaded. Disk usage for `.venv/` jumps significantly.

- [ ] **Step 9: pre-commit + commit**

```bash
cd /Users/bm/ML/3brown1blue && git add phase-03-deep-learning/ uv.lock
cd /Users/bm/ML/3brown1blue && uv run pre-commit run --files $(git diff --cached --name-only) || (git add -u && uv run pre-commit run --files $(git diff --cached --name-only))
cd /Users/bm/ML/3brown1blue && git commit -m "feat(phase-03): scaffold deep-learning phase with 6 project skeletons"
```

---

## Task 12: Scaffold Phase 4 (Transformers, modules-dominant)

This phase introduces the `.py` + `test_*.py` per-project pattern.

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p \
  phase-04-transformers/src/phase_04_transformers \
  phase-04-transformers/projects/01-tokenization \
  phase-04-transformers/projects/02-embeddings-and-positional \
  phase-04-transformers/projects/03-attention-from-scratch \
  phase-04-transformers/projects/04-nano-gpt \
  phase-04-transformers/projects/05-nano-gpt-extensions \
  phase-04-transformers/projects/06-llm-c-walkthrough \
  phase-04-transformers/notebooks \
  phase-04-transformers/tests
```

- [ ] **Step 2: Write `phase-04-transformers/pyproject.toml`**

```toml
[project]
name = "phase-04-transformers"
version = "0.1.0"
description = "Transformers from scratch: tokenization, attention, decoder-only LM, scaling."
requires-python = ">=3.13"
dependencies = [
    "common",
    "numpy>=2.1",
    "torch>=2.5",
    "tiktoken>=0.8",
    "tqdm>=4.66",
    "matplotlib>=3.9",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.sources]
common = { workspace = true }

[tool.hatch.build.targets.wheel]
packages = ["src/phase_04_transformers"]
```

- [ ] **Step 3: Write `phase-04-transformers/src/phase_04_transformers/__init__.py`**

```python
"""Phase 4 — Transformers. Shared utilities (tokenizer, training scaffolding) used across projects."""
```

- [ ] **Step 4: Write `phase-04-transformers/README.md`**

```markdown
# Phase 04 — Transformers

> *Modules dominant; tests required for every project except the stretch.*

## Mission

By the end of this phase, you have implemented a decoder-only transformer end-to-end (tokenizer → embeddings → multi-head attention → training loop → sampling), trained it on a real-but-tiny corpus, and can explain every part by reference to your own code.

## Coverage checklist

- [ ] Tokenization (BPE from scratch)
- [ ] Embeddings: token + positional (sinusoidal / learned / RoPE)
- [ ] Scaled dot-product attention; multi-head attention
- [ ] Full decoder-only transformer block
- [ ] Training a small GPT from scratch (Tiny Shakespeare scale)
- [ ] KV cache and inference-time scaling
- [ ] (Stretch) reading and porting `llm.c`

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `tokenization` | BPE from scratch; train on small corpus; compare to `tiktoken`. | ☐ |
| 02 | `embeddings-and-positional` | Token embeddings; sinusoidal vs. learned vs. RoPE. | ☐ |
| 03 | `attention-from-scratch` | Scaled dot-product → multi-head; tests against a reference. | ☐ |
| 04 | `nano-gpt` | Full decoder-only GPT; train on Tiny Shakespeare; sample. | ☐ |
| 05 | `nano-gpt-extensions` | KV cache for fast generation; sweep depth/width; observe scaling. | ☐ |
| 06 | `llm-c-walkthrough` *(stretch)* | Read llm.c; port the attention kernel back to Python with annotations. | ☐ |

## Pacing

Rough estimate: ~12–16 weeks (this is the most code-intensive phase). Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list.
- `journal.md` — dated breadcrumbs.
- `../ROADMAP.md` — overall progression.
```

- [ ] **Step 5: Write `phase-04-transformers/SOURCES.md`**

```markdown
# Sources — Phase 04: Transformers

> Living document.

## Topic-coverage checklist

- [ ] Tokenization (BPE from scratch)
- [ ] Embeddings: token + positional (sinusoidal / learned / RoPE)
- [ ] Scaled dot-product attention; multi-head attention
- [ ] Full decoder-only transformer block
- [ ] Training a small GPT from scratch
- [ ] KV cache and inference-time scaling
- [ ] (Stretch) reading and porting `llm.c`

## Seed pool

- 3Blue1Brown — transformers/LLM series (*But what is a GPT?*, *Attention in transformers, visually explained*, *How might LLMs store facts?*).
- Karpathy — *Let's build GPT: from scratch, in code, spelled out*.
- Karpathy — `nanoGPT` (github.com/karpathy/nanoGPT).
- Karpathy — `llm.c` (github.com/karpathy/llm.c).
- Jay Alammar — *The Illustrated Transformer* + *The Illustrated GPT-2*.
- Sebastian Raschka — *Build a Large Language Model (From Scratch)*.
- Vaswani et al. — *Attention Is All You Need*.
- Anthropic — *transformer-circuits.pub*.

## Resources I actually used

### Tokenization

- _(empty)_

### Attention

- _(empty)_

### Training a small LM

- _(empty)_
```

- [ ] **Step 6: Write `phase-04-transformers/journal.md`**

```markdown
# Journal — Phase 04

Two-line dated entries. What clicked, what didn't.

---
```

- [ ] **Step 7: Write all six project READMEs, .py stubs, and test stubs**

Per-project substitutions:

| NN | slug | slug_underscored | one_line_what | stretch? |
|---|---|---|---|---|
| 01 | `tokenization` | `tokenization` | BPE from scratch; train on small corpus; compare to `tiktoken`. | no |
| 02 | `embeddings-and-positional` | `embeddings_and_positional` | Token embeddings; sinusoidal vs. learned vs. RoPE. | no |
| 03 | `attention-from-scratch` | `attention_from_scratch` | Scaled dot-product → multi-head; tests against a reference. | no |
| 04 | `nano-gpt` | `nano_gpt` | Full decoder-only GPT; train on Tiny Shakespeare; sample. | no |
| 05 | `nano-gpt-extensions` | `nano_gpt_extensions` | KV cache for fast generation; sweep depth/width; observe scaling. | no |
| 06 | `llm-c-walkthrough` | `llm_c_walkthrough` | Read llm.c; port the attention kernel back to Python with annotations. | yes |

For each project:

a. Write `projects/<NN>-<slug>/README.md` using Template P-README with `phase_num`=`04`, `project_num`=`NN`, `project_slug`=`<slug>`, `one_line_what` per table, and `run_command_placeholder`=`uv run --package phase-04-transformers python -m pytest projects/<NN>-<slug>/test_<slug_underscored>.py -v` (or `uv run --package phase-04-transformers python projects/<NN>-<slug>/<slug_underscored>.py` for projects that have a runnable script). For project 06 (`llm-c-walkthrough`), append a `(stretch)` notice at the top of the README.

b. Write `projects/<NN>-<slug>/<slug_underscored>.py` using Template P-Project-py-stub with `project_slug`=`<slug>` and `one_line_what` per table.

c. Write `projects/<NN>-<slug>/test_<slug_underscored>.py` using Template P-Project-test-stub with `project_slug`=`<slug>` and `project_slug_underscored`=`<slug_underscored>`.

Example for project 03 (`attention-from-scratch`):

`projects/03-attention-from-scratch/attention_from_scratch.py`:

```python
"""attention-from-scratch — Scaled dot-product → multi-head; tests against a reference.

References: see README.md for the running list.
"""
```

`projects/03-attention-from-scratch/test_attention_from_scratch.py`:

```python
"""Test stub for attention-from-scratch — replace xfail with real tests as you build."""

import pytest


@pytest.mark.xfail(reason="not yet implemented")
def test_attention_from_scratch_placeholder() -> None:
    raise NotImplementedError
```

- [ ] **Step 8: `uv sync`, pre-commit, run all stub tests (xfails should report as expected failures), commit**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
cd /Users/bm/ML/3brown1blue && uv run pytest phase-04-transformers/projects -v
```

Expected: 6 xfails (one per project), 0 fails, 0 passes.

```bash
cd /Users/bm/ML/3brown1blue && git add phase-04-transformers/ uv.lock
cd /Users/bm/ML/3brown1blue && uv run pre-commit run --files $(git diff --cached --name-only) || (git add -u && uv run pre-commit run --files $(git diff --cached --name-only))
cd /Users/bm/ML/3brown1blue && git commit -m "feat(phase-04): scaffold transformers phase with 6 project skeletons"
```

---

## Task 13: Scaffold Phase 5 (LLM systems, modules-dominant, local LLMs)

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p \
  phase-05-llm-systems/src/phase_05_llm_systems \
  phase-05-llm-systems/projects/01-local-llm-basics \
  phase-05-llm-systems/projects/02-tool-use \
  phase-05-llm-systems/projects/03-rag-baseline \
  phase-05-llm-systems/projects/04-rag-improvements \
  phase-05-llm-systems/projects/05-agent-loop \
  phase-05-llm-systems/projects/06-evals \
  phase-05-llm-systems/projects/07-guardrails-and-resource-budget \
  phase-05-llm-systems/notebooks \
  phase-05-llm-systems/tests
```

- [ ] **Step 2: Write `phase-05-llm-systems/pyproject.toml`**

```toml
[project]
name = "phase-05-llm-systems"
version = "0.1.0"
description = "LLM systems with local models: prompting, tool use, RAG, agents, evals."
requires-python = ">=3.13"
dependencies = [
    "common",
    "ollama>=0.4",
    "chromadb>=0.5",
    "sentence-transformers>=3.3",
    "rank-bm25>=0.2",
    "pydantic>=2.10",
    "pydantic-settings>=2.7",
    "tqdm>=4.66",
    "tiktoken>=0.8",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.sources]
common = { workspace = true }

[tool.hatch.build.targets.wheel]
packages = ["src/phase_05_llm_systems"]
```

- [ ] **Step 3: Write `phase-05-llm-systems/src/phase_05_llm_systems/__init__.py`**

```python
"""Phase 5 — LLM systems. Shared utilities (Ollama client wrapper, embedding helpers) used across projects."""
```

- [ ] **Step 4: Write `phase-05-llm-systems/README.md`**

```markdown
# Phase 05 — LLM systems

> *Modules dominant. Local LLMs via Ollama.*

## Mission

By the end of this phase, you can compose a small but real LLM application: prompt a local model with structured outputs, give it tools, retrieve from a knowledge base, run it as an agent with a planning loop, and evaluate it with discipline.

## Coverage checklist

- [ ] Local LLM serving (Ollama) — pull a model, run inference, stream
- [ ] Prompting patterns and structured outputs (JSON mode)
- [ ] Tool use / function calling against a local model
- [ ] RAG baseline: chunking, embedding, retrieval, generation
- [ ] RAG improvements: hybrid search, reranking, query rewriting
- [ ] Agent loop: planning + tools + memory
- [ ] Evals: offline + LLM-as-judge
- [ ] Guardrails: prompt-injection, resource budgets, retries

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `local-llm-basics` | Ollama setup; pull a tool-capable model (Llama 3.x / Qwen 2.5); prompting; structured outputs (JSON mode); streaming; observe the KV cache from Phase 4 in production form. | ☐ |
| 02 | `tool-use` | Function calling against an Ollama-served model; dispatch loop; error handling; deliberate model selection for reliable tool support. | ☐ |
| 03 | `rag-baseline` | RAG over a small corpus (3B1B transcripts or your own `SOURCES.md` files). Local embeddings; local vector store (chroma). | ☐ |
| 04 | `rag-improvements` | Chunking, hybrid (BM25 + dense), reranking, query rewriting; measure delta. | ☐ |
| 05 | `agent-loop` | Single-agent: plan + tools + memory; pattern from Anthropic's *Building effective agents*; runs entirely against the local model. | ☐ |
| 06 | `evals` | Offline + LLM-as-judge eval harness; track regressions across versions. | ☐ |
| 07 | `guardrails-and-resource-budget` | Prompt-injection mitigations; resource budgeting (RAM, latency, tokens/s); structured retries; rate limiting per task. | ☐ |

## Required setup

Before starting Project 01, install Ollama from ollama.com and pull a tool-capable model. The phase README of Project 01 will help you benchmark candidates on your hardware before pinning a default.

## Pacing

Rough estimate: ~10–14 weeks. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list.
- `journal.md` — dated breadcrumbs.
- `../ROADMAP.md` — overall progression.
```

- [ ] **Step 5: Write `phase-05-llm-systems/SOURCES.md`**

```markdown
# Sources — Phase 05: LLM systems

> Living document.

## Topic-coverage checklist

- [ ] Local LLM serving (Ollama)
- [ ] Prompting patterns and structured outputs
- [ ] Tool use / function calling
- [ ] RAG baseline
- [ ] RAG improvements
- [ ] Agent loops
- [ ] Evals (offline + LLM-as-judge)
- [ ] Guardrails and resource budgets

## Seed pool

- Lilian Weng — lilianweng.github.io (*LLM Powered Autonomous Agents*, *Prompt Engineering*, *Adversarial Attacks on LLMs*).
- Eugene Yan — eugeneyan.com (*Patterns for Building LLM-based Systems & Products*, *Evals*, *LLM Patterns*).
- Anthropic — *Building effective agents* (anthropic.com/research/building-effective-agents).
- Hamel Husain — hamel.dev (*Your AI Product Needs Evals*, *Field Guide to Rapidly Improving AI Products*).
- Chip Huyen — *Building LLM applications for production* (huyenchip.com).
- Simon Willison — simonwillison.net (tool use & structured outputs).
- Ollama official documentation.
- `llama.cpp` and `vLLM` serving guides.
- Hugging Face open-weights model cards (Llama 3.x, Qwen 2.5, Mistral).
- *Lewis et al.* — RAG paper.

## Resources I actually used

### Local serving

- _(empty)_

### Prompting & structured outputs

- _(empty)_

### Agents

- _(empty)_

### Evals

- _(empty)_
```

- [ ] **Step 6: Write `phase-05-llm-systems/journal.md`**

```markdown
# Journal — Phase 05

Two-line dated entries. What clicked, what didn't.

---
```

- [ ] **Step 7: Write all seven project READMEs, .py stubs, and test stubs**

Per-project substitutions:

| NN | slug | slug_underscored | one_line_what |
|---|---|---|---|
| 01 | `local-llm-basics` | `local_llm_basics` | Ollama setup; pull a tool-capable model; prompting; JSON-mode outputs; streaming. |
| 02 | `tool-use` | `tool_use` | Function calling against an Ollama-served model; dispatch loop; error handling. |
| 03 | `rag-baseline` | `rag_baseline` | RAG over a small corpus with local embeddings + chroma. |
| 04 | `rag-improvements` | `rag_improvements` | Chunking, hybrid (BM25 + dense), reranking, query rewriting; measure delta. |
| 05 | `agent-loop` | `agent_loop` | Single-agent: plan + tools + memory; runs entirely against the local model. |
| 06 | `evals` | `evals` | Offline + LLM-as-judge eval harness; track regressions across versions. |
| 07 | `guardrails-and-resource-budget` | `guardrails_and_resource_budget` | Prompt-injection mitigations; resource budgeting; structured retries; rate limiting. |

For each project, write README + .py stub + test stub using the same approach as Task 12 Step 7. Run command in README is `uv run --package phase-05-llm-systems python -m pytest projects/<NN>-<slug>/test_<slug_underscored>.py -v`.

- [ ] **Step 8: `uv sync` (this pulls chromadb + sentence-transformers, sizable download), pre-commit, smoke test, commit**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
cd /Users/bm/ML/3brown1blue && uv run pytest phase-05-llm-systems/projects -v
```

Expected: 7 xfails.

```bash
cd /Users/bm/ML/3brown1blue && git add phase-05-llm-systems/ uv.lock
cd /Users/bm/ML/3brown1blue && uv run pre-commit run --files $(git diff --cached --name-only) || (git add -u && uv run pre-commit run --files $(git diff --cached --name-only))
cd /Users/bm/ML/3brown1blue && git commit -m "feat(phase-05): scaffold llm-systems phase with 7 project skeletons"
```

---

## Task 14: Scaffold Phase 6 (Production AI engineering)

- [ ] **Step 1: Create directory tree**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p \
  phase-06-production/src/phase_06_production \
  phase-06-production/projects/01-fastapi-serving \
  phase-06-production/projects/02-containerize \
  phase-06-production/projects/03-observability \
  phase-06-production/projects/04-caching-and-cost \
  phase-06-production/projects/05-ci-cd \
  phase-06-production/projects/06-deploy-real \
  phase-06-production/projects/07-mlops-basics \
  phase-06-production/notebooks \
  phase-06-production/tests
```

- [ ] **Step 2: Write `phase-06-production/pyproject.toml`**

```toml
[project]
name = "phase-06-production"
version = "0.1.0"
description = "Production AI engineering: serving, containers, observability, CI/CD, deployment."
requires-python = ">=3.13"
dependencies = [
    "common",
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "pydantic>=2.10",
    "pydantic-settings>=2.7",
    "httpx>=0.28",
    "structlog>=24.4",
    "opentelemetry-api>=1.28",
    "opentelemetry-sdk>=1.28",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv.sources]
common = { workspace = true }

[tool.hatch.build.targets.wheel]
packages = ["src/phase_06_production"]
```

- [ ] **Step 3: Write `phase-06-production/src/phase_06_production/__init__.py`**

```python
"""Phase 6 — Production AI engineering. Shared utilities (FastAPI app factory, observability setup) used across projects."""
```

- [ ] **Step 4: Write `phase-06-production/README.md`**

```markdown
# Phase 06 — Production AI engineering

> *Modules + infrastructure. Real serving, real deploys.*

## Mission

By the end of this phase, you have taken at least one Phase 4 or Phase 5 project from "runs on my laptop" to "runs in production with observability and CI/CD," and you understand each layer (FastAPI → container → host → CI/CD → observability) by having built it.

## Coverage checklist

- [ ] Packaging an inference workload behind FastAPI (streaming, schemas)
- [ ] Containerization with multi-stage Dockerfiles
- [ ] Structured logging + OpenTelemetry tracing + latency/cost metrics
- [ ] Caching: request/response + semantic cache for LLM calls
- [ ] CI/CD with GitHub Actions
- [ ] A real public deployment with observability hooked up
- [ ] Basic MLOps: model + prompt versioning, drift detection

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `fastapi-serving` | Wrap a Phase 4/5 model behind FastAPI; streaming endpoint; Pydantic schemas. | ☐ |
| 02 | `containerize` | Dockerfile (multi-stage, slim); local `compose` run. | ☐ |
| 03 | `observability` | Structured logs + OpenTelemetry tracing; latency + cost metrics; small dashboard. | ☐ |
| 04 | `caching-and-cost` | Request/response cache; semantic cache for LLM calls; cost dashboard. | ☐ |
| 05 | `ci-cd` | GitHub Actions: lint/test/typecheck on push; build container on tag; deploy on main. | ☐ |
| 06 | `deploy-real` | Deploy one project with public URL + observability. Default: FastAPI on Fly.io / Vercel. *Stretch:* full local-LLM stack on Modal / RunPod. | ☐ |
| 07 | `mlops-basics` | Model + prompt versioning (mlflow / DVC); basic drift detector. | ☐ |

## Pacing

Rough estimate: ~10–14 weeks. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list.
- `journal.md` — dated breadcrumbs.
- `../ROADMAP.md` — overall progression.
```

- [ ] **Step 5: Write `phase-06-production/SOURCES.md`**

```markdown
# Sources — Phase 06: Production AI engineering

> Living document.

## Topic-coverage checklist

- [ ] FastAPI / serving
- [ ] Containerization
- [ ] Observability (logs, tracing, metrics)
- [ ] Caching strategies
- [ ] CI/CD with GitHub Actions
- [ ] Deployment to a real platform
- [ ] MLOps basics (versioning, drift)

## Seed pool

- Full Stack Deep Learning — fullstackdeeplearning.com (2022 + 2023 cohort lectures).
- Chip Huyen — *Designing Machine Learning Systems* (book).
- Goku Mohandas — *Made With ML* (madewithml.com).
- Andriy Burkov — *Machine Learning Engineering* (book).
- *Sculley et al.* — *Hidden Technical Debt in ML Systems*.
- vLLM, Ray Serve, Triton, BentoML — official docs as tool references.
- MLOps community blog.

## Resources I actually used

### Serving

- _(empty)_

### Observability

- _(empty)_

### Deployment

- _(empty)_
```

- [ ] **Step 6: Write `phase-06-production/journal.md`**

```markdown
# Journal — Phase 06

Two-line dated entries. What clicked, what didn't.

---
```

- [ ] **Step 7: Write all seven project READMEs, .py stubs, and test stubs**

Per-project substitutions:

| NN | slug | slug_underscored | one_line_what | stretch? |
|---|---|---|---|---|
| 01 | `fastapi-serving` | `fastapi_serving` | Wrap a Phase 4/5 model behind FastAPI; streaming endpoint; Pydantic schemas. | no |
| 02 | `containerize` | `containerize` | Dockerfile (multi-stage, slim); local compose run. | no |
| 03 | `observability` | `observability` | Structured logs + OpenTelemetry tracing; latency + cost metrics; small dashboard. | no |
| 04 | `caching-and-cost` | `caching_and_cost` | Request/response cache; semantic cache for LLM calls; cost dashboard. | no |
| 05 | `ci-cd` | `ci_cd` | GitHub Actions: lint/test/typecheck on push; build container on tag; deploy on main. | no |
| 06 | `deploy-real` | `deploy_real` | Deploy with public URL + observability. Default: FastAPI on Fly.io / Vercel. Stretch path (b): full local-LLM stack on Modal / RunPod. | path-(b) is stretch |
| 07 | `mlops-basics` | `mlops_basics` | Model + prompt versioning (mlflow / DVC); basic drift detector. | no |

Apply Template P-README, Template P-Project-py-stub, Template P-Project-test-stub for each project. For project 06, note the stretch path in the README's "Notes" section.

- [ ] **Step 8: `uv sync`, pre-commit, smoke test, commit**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
cd /Users/bm/ML/3brown1blue && uv run pytest phase-06-production/projects -v
```

Expected: 7 xfails.

```bash
cd /Users/bm/ML/3brown1blue && git add phase-06-production/ uv.lock
cd /Users/bm/ML/3brown1blue && uv run pre-commit run --files $(git diff --cached --name-only) || (git add -u && uv run pre-commit run --files $(git diff --cached --name-only))
cd /Users/bm/ML/3brown1blue && git commit -m "feat(phase-06): scaffold production phase with 7 project skeletons"
```

---

## Task 15: Posts folder

**Files:**
- Create: `/Users/bm/ML/3brown1blue/posts/README.md`
- Create: `/Users/bm/ML/3brown1blue/posts/.gitkeep`

- [ ] **Step 1: Create directory and `.gitkeep`**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p posts && touch posts/.gitkeep
```

- [ ] **Step 2: Write `posts/README.md`**

````markdown
# Posts

Learn-in-public field notes from the 3brown1blue journey. Honest, dated, scoped to one specific moment of confusion or insight. Not tutorials.

## How to write a post

1. Create `YYYY-MM-DD-slug.md` with the front-matter below.
2. Loose three-act body:
   - **What I was trying to do** — one paragraph.
   - **What confused me / what I tried** — the story. This is the value; do not skip it.
   - **What I learned + what's next** — short.
3. Link the relevant repo project(s) in the front-matter `projects:` field. Then add a `Posts` section to those projects' READMEs linking back here.
4. Set `status: published` when ready. Markdown ships from this folder; static-site generator setup is deferred to whenever publishing volume warrants it.

## Front-matter template

```yaml
---
title: <one line>
date: YYYY-MM-DD
phase: 0  # 0 for meta posts, 1–6 otherwise
projects: [NN-slug]  # repo project(s) this post draws from; empty list ok
tags: [<topic-tag>, <tone-tag>]
status: draft  # or "published"
---
```

## Tag legend

Topic tags: `linalg`, `calculus`, `probability`, `nn-basics`, `pytorch`, `cnns`, `rnns`, `transformers`, `attention`, `tokenization`, `rag`, `agents`, `evals`, `serving`, `observability`, `deploy`, `mlops`.

Tone tags: `intuition` (something clicked), `confusion` (admitting a wrong turn), `synthesis` (drawing connections), `meta` (about the journey itself).

## Index

| Date | Title | Phase | Projects | Status |
|---|---|---|---|---|
| _(empty — write your first post)_ | | | | |
````

- [ ] **Step 3: Stage and commit**

```bash
cd /Users/bm/ML/3brown1blue && git add posts/ && git commit -m "feat(posts): add learn-in-public posts folder with index template"
```

---

## Task 16: Resources folder

**Files:**
- Create: `/Users/bm/ML/3brown1blue/Resources/README.md`
- Create: `/Users/bm/ML/3brown1blue/Resources/.gitkeep`

- [ ] **Step 1: Create directory and `.gitkeep`**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p Resources && touch Resources/.gitkeep
```

- [ ] **Step 2: Write `Resources/README.md`**

```markdown
# Resources

Heavy reference material — PDFs, slides, downloaded transcripts. Files in this directory are gitignored by default (`Resources/**` in `.gitignore`); only `README.md` and `.gitkeep` are tracked.

## Linked-only policy

Don't commit copyrighted PDFs. Instead, list each resource here with a note on where to acquire it. Drop the local copy in this folder (gitignored) for offline reading.

## How to add a resource

Append a row to the table below. Keep slugs stable so projects' `SOURCES.md` files can link consistently.

## Reading list

| Slug | Title | Author(s) | Where to acquire | Used by phase |
|---|---|---|---|---|
| `mml-book` | Mathematics for Machine Learning | Deisenroth, Faisal & Ong | Free PDF: mml-book.com | 1 |
| `nielsen-dl` | Neural Networks and Deep Learning | Michael Nielsen | Free online: neuralnetworksanddeeplearning.com | 2 |
| `goodfellow-dl` | Deep Learning | Goodfellow, Bengio & Courville | Free online: deeplearningbook.org | 3 |
| `raschka-pytorch` | Machine Learning with PyTorch and Scikit-Learn | Sebastian Raschka | Publisher / library | 3 |
| `raschka-llm` | Build a Large Language Model (From Scratch) | Sebastian Raschka | Publisher / library | 4 |
| `huyen-mlsys` | Designing Machine Learning Systems | Chip Huyen | Publisher / library | 6 |
| `burkov-mle` | Machine Learning Engineering | Andriy Burkov | Publisher / library | 6 |

_(Append rows as you acquire resources. The table is the canonical source for "what's in this folder.")_
```

- [ ] **Step 3: Stage and commit**

```bash
cd /Users/bm/ML/3brown1blue && git add Resources/ && git commit -m "feat(resources): add linked-only Resources/ folder with reading list template"
```

---

## Task 17: Scratch folder

**Files:**
- Create: `/Users/bm/ML/3brown1blue/scratch/.gitkeep`

- [ ] **Step 1: Create scratch directory and gitkeep**

```bash
cd /Users/bm/ML/3brown1blue && mkdir -p scratch && touch scratch/.gitkeep
```

- [ ] **Step 2: Force-add `.gitkeep` (its parent is gitignored except for .gitkeep)**

```bash
cd /Users/bm/ML/3brown1blue && git add -f scratch/.gitkeep
```

- [ ] **Step 3: Verify scratch contents are otherwise gitignored**

```bash
cd /Users/bm/ML/3brown1blue && touch scratch/test.txt && git status --porcelain | grep scratch/
```

Expected: only `scratch/.gitkeep` shows as added (or no lines if already added). `scratch/test.txt` does NOT appear in the output (it's ignored).

```bash
cd /Users/bm/ML/3brown1blue && rm scratch/test.txt
```

- [ ] **Step 4: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git commit -m "chore: add scratch/ playground (contents gitignored)"
```

---

## Task 18: Root README

**Files:**
- Create: `/Users/bm/ML/3brown1blue/README.md`

- [ ] **Step 1: Write `README.md`**

```markdown
# 3brown1blue

A self-driven, learn-in-public path from math intuition to production AI engineering.

Anchored in the 3Blue1Brown neural-network and math series wherever Grant covers the topic; everywhere else, the best canonical explainer wins.

## Why this exists

I wanted one disciplined repository to learn ML the slow, honest way — not by chasing tutorials, but by reimplementing each idea from first principles, in order, and writing about what was confusing while it was confusing. This is the result.

The repo is for me first. It's public second so others can follow the actual process, mistakes and all. It is *not* a polished teaching resource.

## Layout

```
3brown1blue/
├── common/                  # shared utilities (RNG, data cache, plotting, logging)
├── phase-01-math/           # linear algebra, calculus, probability
├── phase-02-nn-from-scratch/  # NumPy-only neural nets
├── phase-03-deep-learning/  # PyTorch, CNNs, training discipline
├── phase-04-transformers/   # tokenization → attention → nano-GPT
├── phase-05-llm-systems/    # local LLMs, RAG, agents, evals (Ollama)
├── phase-06-production/     # serving, observability, deployment
├── posts/                   # dated learn-in-public blog posts
├── Resources/               # heavy reading (linked-only; mostly gitignored)
├── docs/                    # design specs and implementation plans
├── ROADMAP.md               # flat checklist of every project, in canonical order
├── playlist-map.md          # 3B1B videos → phase mapping
└── pyproject.toml           # uv workspace root
```

Each `phase-NN-*/` folder has the same shape: `README.md`, `SOURCES.md`, `journal.md`, an importable `src/` package for shared phase utilities, and `projects/NN-<slug>/` directories for the actual work.

## Setup

Requires `uv` and `direnv`. On first clone:

```bash
direnv allow .
uv sync
```

Then drop into any phase:

```bash
uv run --package phase-01-math jupyter lab phase-01-math/projects/01-vectors-and-linear-maps/notes.ipynb
```

## How to navigate

- Reading the journey in order? Start with `ROADMAP.md` and follow phase by phase.
- Looking for the design? `docs/superpowers/specs/2026-05-07-3brown1blue-repo-design.md`.
- Looking for posts? `posts/README.md`.
- Looking for source pointers? Each phase's `SOURCES.md`.

## License

Code: MIT. Posts and prose: CC-BY-4.0. Each phase's `Resources/` references its own copyright holders — those are linked-only, never redistributed from this repo.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add README.md && uv run pre-commit run --files README.md || git add -u
cd /Users/bm/ML/3brown1blue && git commit -m "docs: add root README"
```

---

## Task 19: ROADMAP.md

**Files:**
- Create: `/Users/bm/ML/3brown1blue/ROADMAP.md`

- [ ] **Step 1: Write `ROADMAP.md`**

```markdown
# Roadmap

Flat checklist of every project across all six phases, in canonical order. The source of truth for "what's next." Tick boxes as you complete projects.

## Phase 01 — Math intuition

- [ ] 01.01 — `vectors-and-linear-maps`
- [ ] 01.02 — `eigenstuff`
- [ ] 01.03 — `pca-from-scratch`
- [ ] 01.04 — `derivatives-and-chain-rule`
- [ ] 01.05 — `gradient-descent-by-hand`
- [ ] 01.06 — `probability-essentials`

## Phase 02 — Neural networks from scratch

- [ ] 02.01 — `perceptron`
- [ ] 02.02 — `mlp-numpy`
- [ ] 02.03 — `activations-and-losses`
- [ ] 02.04 — `micrograd`
- [ ] 02.05 — `mini-makemore`
- [ ] 02.06 — `optim-zoo`

## Phase 03 — Deep learning

- [ ] 03.01 — `pytorch-fundamentals`
- [ ] 03.02 — `mnist-cnn`
- [ ] 03.03 — `cifar-resnet`
- [ ] 03.04 — `debugging-training`
- [ ] 03.05 — `lstm-text`
- [ ] 03.06 — `data-pipeline`

## Phase 04 — Transformers

- [ ] 04.01 — `tokenization`
- [ ] 04.02 — `embeddings-and-positional`
- [ ] 04.03 — `attention-from-scratch`
- [ ] 04.04 — `nano-gpt`
- [ ] 04.05 — `nano-gpt-extensions`
- [ ] 04.06 — `llm-c-walkthrough` *(stretch)*

## Phase 05 — LLM systems

- [ ] 05.01 — `local-llm-basics`
- [ ] 05.02 — `tool-use`
- [ ] 05.03 — `rag-baseline`
- [ ] 05.04 — `rag-improvements`
- [ ] 05.05 — `agent-loop`
- [ ] 05.06 — `evals`
- [ ] 05.07 — `guardrails-and-resource-budget`

## Phase 06 — Production AI engineering

- [ ] 06.01 — `fastapi-serving`
- [ ] 06.02 — `containerize`
- [ ] 06.03 — `observability`
- [ ] 06.04 — `caching-and-cost`
- [ ] 06.05 — `ci-cd`
- [ ] 06.06 — `deploy-real` *(stretch path (b): full local-LLM stack on Modal / RunPod)*
- [ ] 06.07 — `mlops-basics`

## Future considerations

These are recorded but not committed to. Add as projects to the appropriate phase only after deciding deliberately.

- Mechanistic interpretability mini-project (Phase 4 stretch).
- RLHF / DPO / fine-tuning workflow (Phase 5 candidate).
- Vision-language or multimodal (Phase 5 candidate).
- Diffusion models (Phase 3.5 or Phase 5 candidate).

## How to use this file

- Promote a `[ ]` to `[x]` when the project's success criteria (in its README) are met.
- If you trim or expand a phase, edit this file in the same commit so it stays the source of truth.
- This file is never auto-generated. Hand-curated.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add ROADMAP.md && uv run pre-commit run --files ROADMAP.md || git add -u
cd /Users/bm/ML/3brown1blue && git commit -m "docs: add ROADMAP.md as canonical project checklist"
```

---

## Task 20: playlist-map.md

**Files:**
- Create: `/Users/bm/ML/3brown1blue/playlist-map.md`

- [ ] **Step 1: Write `playlist-map.md`**

```markdown
# 3Blue1Brown playlist map

The 3B1B trunk videos, mapped to the phases / projects they anchor. Not a curriculum spine — a reading map. Phases 3, 5, and 6 have no 3B1B trunk and aren't listed here; see those phases' `SOURCES.md` for their canonical sources.

| 3B1B series / video | Phase | Anchored in | Watched? |
|---|---|---|---|
| Essence of Linear Algebra (full series, 15 vids) | 01 | `01-vectors-and-linear-maps`, `02-eigenstuff`, `03-pca-from-scratch` | ☐ |
| Essence of Calculus (full series, 12 vids) | 01 | `04-derivatives-and-chain-rule`, `05-gradient-descent-by-hand` | ☐ |
| Bayes theorem from the ground up | 01 | `06-probability-essentials` | ☐ |
| Binomial distributions | 01 | `06-probability-essentials` | ☐ |
| Neural Networks Ch. 1 — *But what is a neural network?* | 02 | `01-perceptron`, `02-mlp-numpy` | ☐ |
| Neural Networks Ch. 2 — *Gradient descent* | 02 | `02-mlp-numpy`, `03-activations-and-losses` | ☐ |
| Neural Networks Ch. 3 — *Backpropagation* | 02 | `02-mlp-numpy` | ☐ |
| Neural Networks Ch. 4 — *Backpropagation calculus* | 02 | `04-micrograd` | ☐ |
| But what is a GPT? | 04 | `04-nano-gpt` | ☐ |
| Attention in transformers, visually explained | 04 | `03-attention-from-scratch` | ☐ |
| How might LLMs store facts? | 04 | `04-nano-gpt`, `05-nano-gpt-extensions` | ☐ |

## Phases with no 3B1B trunk

Phases 03 (Deep learning), 05 (LLM systems), and 06 (Production AI) draw exclusively on canonical content from other authors. See `phase-NN-*/SOURCES.md` in each.
```

- [ ] **Step 2: Commit**

```bash
cd /Users/bm/ML/3brown1blue && git add playlist-map.md && uv run pre-commit run --files playlist-map.md || git add -u
cd /Users/bm/ML/3brown1blue && git commit -m "docs: add playlist-map mapping 3B1B videos to phases"
```

---

## Task 21: Workspace-wide smoke test

**Files:** none modified.

- [ ] **Step 1: Sync the entire workspace one more time**

```bash
cd /Users/bm/ML/3brown1blue && uv sync
```

Expected: clean exit, all 7 workspace members resolved, `.venv/` populated.

- [ ] **Step 2: Run the entire test suite**

```bash
cd /Users/bm/ML/3brown1blue && uv run pytest -v
```

Expected:
- `common/tests/`: 11 passes (3 from `test_rng`, 3 from `test_data`, 2 from `test_viz`, 3 from `test_logging`).
- `phase-04-transformers/projects/`: 6 xfails.
- `phase-05-llm-systems/projects/`: 7 xfails.
- `phase-06-production/projects/`: 7 xfails.
- Phases 01–03 contribute no tests (notebook-dominant).

Total: 11 passes, 20 xfails, 0 fails.

- [ ] **Step 3: Run pre-commit on the entire tree**

```bash
cd /Users/bm/ML/3brown1blue && uv run pre-commit run --all-files
```

Expected: all hooks pass without modifications.

- [ ] **Step 4: Verify ruff and mypy run clean**

```bash
cd /Users/bm/ML/3brown1blue && uv run ruff check . && uv run ruff format --check . && uv run mypy common/src
```

Expected: ruff reports no issues; ruff format reports `would not reformat` on every file; mypy reports `Success: no issues found`.

- [ ] **Step 5: Verify identity once more before pushing anywhere**

```bash
cd /Users/bm/ML/3brown1blue && sid --check
```

Expected: aligned. If not, stop and resolve.

- [ ] **Step 6: No commit needed (no file changes); proceed**

---

## Task 22: Push to GitHub

**Files:** none modified locally; this creates a remote.

- [ ] **Step 1: Confirm GitHub repo name and owner from pre-flight inputs**

The pre-flight inputs include `<gh-repo-name>` (default: `3brown1blue`) and `<gh-org-or-user>`. Confirm these are still correct before creating.

- [ ] **Step 2: Verify `gh` is using SSH protocol globally**

```bash
gh config get git_protocol
```

Expected: `ssh`. If anything else, stop — per global rules HTTPS is forbidden on this machine.

- [ ] **Step 3: Confirm `gh` is authenticated as the right user**

```bash
gh auth status
```

Expected: shows `<gh-org-or-user>` (or a user with admin in that org). If it shows the wrong account, the identity is misaligned — stop and resolve via `sid` before continuing.

- [ ] **Step 4: Create the GitHub repository (public, no README — local already has one)**

Substitute `<gh-org-or-user>` and `<gh-repo-name>`:

```bash
gh repo create <gh-org-or-user>/<gh-repo-name> --public --source=/Users/bm/ML/3brown1blue --remote=origin --description "A self-driven, learn-in-public path from math intuition to production AI engineering."
```

Expected: a new public repo at `https://github.com/<gh-org-or-user>/<gh-repo-name>`, and `origin` is set on the local repo to `git@github.com:<gh-org-or-user>/<gh-repo-name>.git`.

- [ ] **Step 5: Verify remote is SSH**

```bash
cd /Users/bm/ML/3brown1blue && git remote -v
```

Expected: both `fetch` and `push` URLs start with `git@github.com:`. If they start with `https://`, run `git remote set-url origin git@github.com:<gh-org-or-user>/<gh-repo-name>.git` and verify again.

- [ ] **Step 6: Push `main`**

```bash
cd /Users/bm/ML/3brown1blue && git push -u origin main
```

Expected: all commits land on origin/main; tracking branch set.

- [ ] **Step 7: Verify the repo is browsable**

```bash
gh repo view <gh-org-or-user>/<gh-repo-name> --web
```

Or just open the URL printed in Step 4 in a browser. Confirm: README renders, ROADMAP visible, all six phase folders present.

- [ ] **Step 8: Final task — print "next steps" for the user**

The bootstrap is complete. The user's natural next move is Phase 01 Project 01:

```bash
cd /Users/bm/ML/3brown1blue
uv run --package phase-01-math jupyter lab phase-01-math/projects/01-vectors-and-linear-maps/notes.ipynb
```

Suggest the user write the zeroth post (`posts/2026-05-07-why-3brown1blue.md`) before opening the notebook — committing publicly to the journey while the why is fresh is the cleanest start.

---

## Verification checklist (run after Task 22)

Quick sanity sweep so the user knows the bootstrap is honest:

- [ ] `git log --oneline | wc -l` reports ~22 commits (one per task).
- [ ] `git remote -v` shows SSH origin.
- [ ] `uv sync` is idempotent (re-running produces no changes).
- [ ] `uv run pytest` reports 11 passes + 20 xfails.
- [ ] `uv run pre-commit run --all-files` is clean.
- [ ] `gh repo view` opens the public GitHub repo.
- [ ] `find . -maxdepth 2 -name pyproject.toml | wc -l` = 8 (root + 7 members).
- [ ] All six `phase-NN-*/projects/` directories exist with the expected per-project subfolder count (6, 6, 6, 6, 7, 7).
- [ ] `posts/README.md`, `Resources/README.md`, `ROADMAP.md`, `playlist-map.md`, root `README.md` all rendered cleanly on GitHub.

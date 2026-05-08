# Development notes

How to work in this repo without tripping on the same things the bootstrap tripped on. Read this before your first commit. It's short.

## Quickstart for a fresh clone

```bash
git clone git@github.com:mehdisalescale/3brown1blue.git
cd 3brown1blue
direnv allow .
direnv exec . uv sync --all-packages
direnv exec . uv run pre-commit install
direnv exec . uv run pytest
```

Expected: 11 passes (`common/`) + 20 xfails (project stubs in phases 4–6) = a green workspace.

## Three operational rules (non-negotiable)

These were learned the hard way during bootstrap. The repo is built around them.

### 1. Always run git, gh, and uv commands via `direnv exec .`

The shell on this machine exports stale `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, and `GIT_COMMITTER_EMAIL` env vars from prior identity switches. Those env vars take precedence over local `git config`, so a plain `git commit` lands under the wrong author and silently corrupts history.

`direnv exec .` loads `.envrc`, which calls `use_identity mehdisalescale` and then explicitly re-exports the `GIT_*` vars to the right values. Inside that wrapper, every commit is correctly authored.

```bash
# right
direnv exec . git commit -m "..."
direnv exec . gh repo view
direnv exec . uv run pytest

# wrong — env vars from the parent shell pollute the call
git commit -m "..."
gh repo view
uv run pytest
```

After every commit, verify:

```bash
direnv exec . git log -1 --format="%an <%ae>"
# must print: mehdisalescale <mehdi@salescale.me>
```

If author is wrong, amend (safe on no-remote branches, or before push):

```bash
direnv exec . git commit --amend --reset-author --no-edit
```

### 2. Use `uv sync --all-packages`, not plain `uv sync`

`uv sync` from the workspace root only installs the *root* package's dependencies (which are empty). Workspace members (`common`, `phase-NN-*`) and *their* dependencies are skipped. The resulting `.venv` is missing `numpy`, `torch`, `chromadb`, etc., and tests fail to import.

`uv sync --all-packages` resolves and installs every workspace member. That's what you want every time.

```bash
# right
direnv exec . uv sync --all-packages

# wrong
uv sync
```

### 3. Inside a package's `__init__.py`, use relative imports

`common/src/common/__init__.py` re-exports the four submodules. The right way:

```python
from . import data, logging, rng, viz
```

Not:

```python
from common import data, logging, rng, viz   # circular self-reference
```

Same rule applies inside any `phase_NN_*/__init__.py` if/when those packages start re-exporting modules.

## How to add a new project

The repo is heavily templated — every project across all six phases has the same shape. To add one (e.g., a new project under Phase 4):

1. Append the row to `phase-04-transformers/README.md`'s project table.
2. Append the row to root `ROADMAP.md`.
3. `mkdir -p phase-04-transformers/projects/NN-<slug>`
4. Inside it, create:
   - `README.md` — copy the 6-section template from a sibling project, change the heading to `04.NN — <slug>` and the run command.
   - `<slug_underscored>.py` — module stub matching the docstring pattern in sibling projects.
   - `test_<slug_underscored>.py` — xfail stub matching the pattern in sibling projects.
5. (Phases 1–3 only:) replace the `.py` + test pair with a `notes.ipynb` stub.
6. `direnv exec . git add phase-04-transformers/projects/NN-<slug>/ phase-04-transformers/README.md ROADMAP.md`
7. `direnv exec . git commit -m "feat(phase-04): add project NN-<slug>"`

Pre-commit hooks will catch ruff E501 (line ≥100 chars) on the module docstring — wrap it across two lines if needed.

## How to write a post

1. Create `posts/YYYY-MM-DD-slug.md` with the front-matter block from `posts/README.md`.
2. Write the three-act body (what I was trying to do / what confused me / what I learned).
3. Update `posts/README.md`'s index table.
4. In any project README that the post draws from, append a link under the `## Posts` section.
5. Commit with `direnv exec . git commit -m "post: <slug>"`.

The post lives as plain markdown in this repo. Static-site publishing is deferred — when there are enough posts to warrant it, pick an SSG (Astro / Hugo / Quartz) and point it at this folder.

## How to ship a phase project

When a project's success criteria (in its README) are met:

1. Replace the xfail stub in `test_<slug>.py` with real tests; make them green.
2. Update the project README's `## What`, `## Why`, `## Success criteria`, and `## Notes` sections with the actual content.
3. Append used resources to the project's `## References` section AND to the phase's `SOURCES.md`.
4. Tick the box in `phase-NN-*/README.md`'s project table and in root `ROADMAP.md`.
5. Add a one-line dated entry to `phase-NN-*/journal.md`.
6. Commit. Push.
7. (Optional) Write a post if anything was worth admitting publicly.

## Pre-commit hooks

Installed by `pre-commit install` (per quickstart). They run on every commit:

- `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`, `check-merge-conflict`, `check-added-large-files` (max 512KB).
- `ruff --fix` (lint with auto-fix).
- `ruff-format` (formatter).

If a hook auto-fixes a file during a commit attempt, the commit is *blocked* (this is intentional — pre-commit wants you to review the fix). Re-stage with `direnv exec . git add -u` and re-commit. Repeat until clean.

To run hooks across the whole tree:

```bash
direnv exec . uv run pre-commit run --all-files
```

## Tests

```bash
direnv exec . uv run pytest                          # everything
direnv exec . uv run pytest common/tests             # common only
direnv exec . uv run pytest phase-04-transformers    # one phase
```

Phases 4–6 ship with `xfail` stubs (one per project). When a project is implemented, the xfail decorator goes away and the tests become real.

## Identity recap

This repo is pinned to identity `mehdisalescale` via `.sid-identity` and `.envrc`. The user's machine has 8 identities; `mehdisalescale` is the one tied to this repo and to the GitHub account `github.com/mehdisalescale` where this lives. **Don't switch global identity** to fix a per-repo issue — use `sid --repo <name>` for per-repo pins, never plain `sid <name>`.

## When something is wrong

- **Commit landed under wrong author** — `direnv exec . git commit --amend --reset-author --no-edit`. If already pushed, stop and ask.
- **Pre-commit hook failed** — read the failure. `ruff --fix` fixes most things; rest are usually wrapping a long line or escaping a yaml gotcha.
- **`uv sync` errors** — try `direnv exec . uv sync --all-packages --reinstall`. If that fails, the `uv.lock` may be out of date; delete it and re-sync.
- **Tests fail unexpectedly after a `uv sync`** — a dependency version moved. Pin the offending one in the relevant `pyproject.toml` and re-lock.
- **`direnv` says the `.envrc` is not allowed** — `direnv allow .`. Required after any `.envrc` change.

## Where things live

- Design spec: `docs/superpowers/specs/2026-05-07-3brown1blue-repo-design.md`
- Bootstrap implementation plan (with task-level detail): `docs/superpowers/plans/2026-05-07-3brown1blue-bootstrap.md`
- Per-phase mission, coverage, project list: `phase-NN-*/README.md`
- Per-phase living source list: `phase-NN-*/SOURCES.md`
- Per-phase dated breadcrumbs: `phase-NN-*/journal.md`
- Per-project frame: `phase-NN-*/projects/NN-<slug>/README.md`
- Public posts: `posts/`

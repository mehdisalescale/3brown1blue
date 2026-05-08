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
uv sync --all-packages
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

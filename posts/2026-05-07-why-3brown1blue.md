---
title: Reading 3Blue1Brown is not the same as doing it
date: 2026-05-07
phase: 0
projects: []
tags: [meta]
status: draft
---

## What I was trying to do

I've been watching 3Blue1Brown's neural network series on and off for years. Each time I finish a video I feel like I understand attention or backprop or eigenvectors a little better. Then a week later I can't reconstruct the argument from scratch, and a month later I'm not sure I ever could.

This is the gap. Watching is not learning. Implementing is.

So I'm starting a long, slow project to walk the full path from math intuition to production AI engineering — six phases, around thirty-eight projects, a multi-year arc — and reimplement every idea from first principles, in order, while writing about what was confusing *while* it was confusing. The repo is at [github.com/mehdisalescale/3brown1blue](https://github.com/mehdisalescale/3brown1blue).

## What confused me / what I tried

The first confusion was scoping. ML curricula sprawl. You can pick up any of: Karpathy, fast.ai, Goodfellow, Raschka, Lilian Weng, Eugene Yan, Anthropic's blog, Full Stack Deep Learning, or just the original papers. Pick wrong and you spend a year on something tangential. Pick rigid and you grind through material that doesn't click.

The frame I landed on: 3B1B is the trunk where Grant covers the topic — linear algebra, calculus, NN basics, attention. Everywhere else, the best canonical explainer of a specific idea wins. Each phase has a `SOURCES.md` that's a *living* document — what actually helped, not what was supposed to. Every project's README ends with a `## References` block that gets filled in as I go, not before.

The second confusion was about the public part. Most learning-in-public I've seen is performative: "I built X" posts that hide the confusion and skip to the win. That's the opposite of useful. The differentiator of this repo is that it admits the uncertainty. Posts here document the actual learning — including the wrong turns, the half-understood concepts, the moments I gave up and went back. Field notes, not tutorials.

The third confusion was structural. Personal-learning repos rot. Notebooks accumulate, names drift, future-me can't navigate. The fix: every phase has the same shape — `pyproject.toml`, `README.md`, `SOURCES.md`, `journal.md`, `projects/NN-<slug>/`. Learn the layout once, never re-orient. There's a flat `ROADMAP.md` at the root that's the single source of truth for what's next. The whole thing is a `uv` workspace so each phase can have its own dependencies (Phase 1 needs NumPy; Phase 5 needs Ollama and chroma) without one heavy environment for everything.

## What I learned + what's next

I haven't done any actual ML yet. The bootstrap took longer than I expected — figuring out what to build *before* building was the work. The repo as it stands is empty scaffolding: every project has a stub README and a placeholder test waiting for real code. The brainstorm spec and the 22-task implementation plan are committed in `docs/superpowers/`, partly so future-me can remember why each decision was made, partly because I think the meta is interesting.

The most useful thing I learned during the bootstrap had nothing to do with ML: my shell exports stale `GIT_AUTHOR_*` env vars from a prior identity switch, which silently corrupts commit authorship. The fix is wrapping every `git` call in `direnv exec .`. That kind of friction — boring, off-topic, but real — is exactly what the journal-and-posts model is for. Document it once, stop tripping on it.

Next: Phase 1, Project 01 — `vectors-and-linear-maps`. NumPy matrix ops, animated 2D/3D linear transformations. Feels like a warmup, but I'm betting that doing it (rather than rewatching the 3B1B videos) will reveal what I actually don't remember.

If you want to follow along: the repo is public, the roadmap is there, every project's README will fill in over time. No newsletter, no schedule. Just commits, and the occasional post when something clicks or breaks.

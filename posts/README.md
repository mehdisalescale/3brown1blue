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
| 2026-05-07 | [Reading 3Blue1Brown is not the same as doing it](2026-05-07-why-3brown1blue.md) | 0 | — | draft |

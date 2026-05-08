# 3brown1blue — repository design

- **Date:** 2026-05-07
- **Status:** Draft, revision 2 (awaiting second-pass user review)
- **Author:** brainstormed with Claude (Opus 4.7)
- **Scope:** Greenfield personal-learning monorepo at `/Users/bm/ML/3brown1blue/`

## Mission

A single, disciplined, sequentially-ordered hands-on repository covering the full path from mathematical intuition to production AI engineering, **built in public**. The 3Blue1Brown neural-network series is the spine where Grant covers the topic; every other phase pulls in whatever reliable, famous, intuitive resources best explain the idea at hand. The repo's primary purpose is the author's own internalization of the material; its secondary purpose is to share the journey honestly through dated blog posts so others can follow the actual learning process — confusion, wrong turns, and clicks included. It is *not* a polished teaching artifact, but it is organized seriously throughout so future-you (and anyone reading along) can revisit any phase without re-orienting.

## Captured decisions

| Decision | Choice | Source |
|---|---|---|
| Audience | Personal learning journey, disciplined sequential, all six phases covered | Q1 (D, refined) |
| Project layout | `uv` workspace; one package per phase + `common/` | Q3 (B) |
| Granularity | Project-based — each unit is a runnable thing | Q4a (iii) |
| Format | Notebooks dominant in Phases 1–3; modules + tests dominant in Phases 4–6 | Q4b (z) |
| Source anchor | 3B1B as trunk where it covers the topic; canonical co-anchors per phase; `SOURCES.md` is a *living* document, not a contract | Q5 (B, revised) |
| Repo strategy | Standalone git repository — own remote, own `.sid-identity`, own `.envrc` | Post-spec review |
| LLM provider | Local LLMs (Ollama default) for Phases 5–6; cloud providers added later only if specifically needed | Post-spec review |
| Public-ness | Learn-in-public — repo public from day one; dated blog posts in `posts/`; honest tone throughout | Post-spec review |

## Section 1 — Top-level layout

```
3brown1blue/
├── .envrc                  # direnv: use_identity <name> — own copy, repo is standalone
├── .sid-identity           # identity pin — own copy, repo is standalone
├── .python-version         # 3.13
├── pyproject.toml          # uv workspace root
├── uv.lock                 # one lockfile, whole workspace
├── README.md               # journey overview + how to navigate
├── ROADMAP.md              # ordered checklist of every project; tick as you go
├── playlist-map.md         # 3B1B chapter/video → phase/project table
├── docs/
│   └── superpowers/specs/  # design docs (this file lives here)
├── common/                 # shared workspace package: viz, data loaders, RNG, logging
│   ├── pyproject.toml
│   └── src/common/
├── phase-01-math/
├── phase-02-nn-from-scratch/
├── phase-03-deep-learning/
├── phase-04-transformers/
├── phase-05-llm-systems/
├── phase-06-production/
├── posts/                  # learn-in-public dated blog posts (Section 6)
├── Resources/              # PDFs, slides — heavy items gitignored, README lists them
└── scratch/                # gitignored playground for throwaway experiments
```

**Workspace mechanics.** Root `pyproject.toml` declares `[tool.uv.workspace] members = ["common", "phase-*"]`. Each member has its own `pyproject.toml` with phase-specific deps. One `uv sync` from root resolves the whole tree into a single `.venv`. Per-phase scoping with `uv run --package phase-04-transformers python ...`.

**`common/` purpose.** Three things repeat across phases and deserve one home: (a) seeded RNG helpers (reproducibility), (b) dataset download/cache helpers (MNIST/CIFAR/Tiny-Shakespeare/etc. fetched once), (c) a `viz/` module for the 3B1B-flavored plotting style used in Phases 1–4. `common/` is not a junk drawer — code used in only one place stays in that phase.

**`ROADMAP.md` is the source of truth for "what's next."** Disciplined sequential order requires a single durable pointer. It's a flat checklist of every project across all six phases, in canonical order. Phase READMEs link into it.

## Section 2 — Anchor strategy

**Principle.** Each phase aims for **complete topical coverage**, drawing on whatever well-known, intuitive resources fit. 3B1B is the trunk *only where Grant covers the topic* (linear algebra, calculus, NN basics, attention/transformers). Everywhere else, the best canonical explainer of that specific idea wins. Seed pools below are starting points, not prescriptions.

**How it lives in the repo:**

- Each `phase-NN-*/SOURCES.md` is a **living document**. It opens with a topic-coverage checklist and a running list of resources that helped, grouped by topic. Append as you go.
- Per-project `README.md` ends with a `## References` section listing whatever resources you actually used for that project.
- Root `playlist-map.md` tracks only the 3B1B trunk videos — a checklist of Grant's content you've watched and connected to projects.

### Coverage targets per phase

- **Phase 1 — Math:** vectors / matrices / linear maps, eigen-stuff, derivatives & chain rule, multivariate calculus, gradients, basic probability & expectations, Bayes.
- **Phase 2 — NN from scratch:** perceptron → MLP, forward / backward pass by hand, activations, loss functions, SGD, autograd.
- **Phase 3 — Deep learning:** PyTorch idioms, training loops, regularization (dropout / weight-decay / batchnorm), CNNs, RNNs/LSTMs (briefly), data pipelines, debugging training.
- **Phase 4 — Transformers:** tokenization, embeddings, attention (single → multi-head), positional encoding, transformer block, decoder-only LM, training from scratch, scaling intuitions.
- **Phase 5 — LLM systems:** prompting patterns, structured outputs, tool use, RAG (retrieval / chunking / reranking), agents (planning / memory / multi-step), evals (offline & LLM-as-judge), guardrails.
- **Phase 6 — Production AI:** packaging, FastAPI / serving, containerization, observability / tracing, cost control, caching, CI/CD, deployment to a real platform, basic MLOps (versioning, drift).

### Seed sources to reach for first

- **Math** → 3B1B *Essence of Linear Algebra* + *Essence of Calculus*; *Mathematics for Machine Learning* (Deisenroth, Faisal, Ong); Strang MIT 18.06 (selective).
- **NN from scratch** → 3B1B *Neural Networks* Ch. 1–4; Karpathy *Zero to Hero* (`micrograd`, `makemore` 1–2); Nielsen *Neural Networks and Deep Learning*.
- **Deep learning** → fast.ai *Practical Deep Learning for Coders*; Goodfellow / Bengio / Courville (selective); Raschka *ML with PyTorch and Scikit-Learn*; distill.pub diagrams.
- **Transformers** → 3B1B transformers / LLM series; Karpathy *Let's build GPT* + nanoGPT + llm.c; Jay Alammar *Illustrated Transformer / GPT-2*; Raschka *Build an LLM From Scratch*.
- **LLM systems** → Lilian Weng (lilianweng.github.io); Eugene Yan (eugeneyan.com); Anthropic *Building effective agents*; Hamel Husain (hamel.dev); Chip Huyen *Building LLM applications for production*; Simon Willison. **Local-LLM specific:** Ollama docs, `llama.cpp` and `vLLM` serving guides, Hugging Face open-weights model cards (Llama 3.x, Qwen 2.5, Mistral).
- **Production** → Full Stack Deep Learning; Chip Huyen *Designing ML Systems*; Goku Mohandas *Made With ML*; Andriy Burkov *Machine Learning Engineering*.

**Honesty rule.** The journey trumps the curriculum. If a random YouTube diagram unlocks a concept that a canonical anchor failed to convey, the diagram goes into `SOURCES.md` and gets cited in the project README. The repo records *what actually worked for you*.

## Section 3 — Canonical phase shape

Every `phase-NN-*/` folder has the same skeleton. Learn the layout once, never re-orient.

```
phase-NN-<slug>/
├── pyproject.toml           # phase-specific deps
├── README.md                # phase mission, coverage checklist, ordered project table
├── SOURCES.md               # living anchor list (per Section 2)
├── journal.md               # dated breadcrumbs: what clicked, what didn't
├── src/
│   └── phase_NN_<slug>/     # importable package — shared phase-level utilities only
│       └── __init__.py
├── projects/
│   ├── 01-<slug>/           # self-contained, runnable as scripts (not importable)
│   ├── 02-<slug>/
│   └── ...
├── notebooks/               # cross-project scratch (optional)
└── tests/                   # phase-level integration tests (optional)
```

**Conventions.**

- Hyphenated, numbered project folders: filesystem order *is* study order. Folders, not Python packages — run scripts directly.
- `src/phase_NN_<slug>/` holds *only* code reused across multiple projects in the phase (e.g., a tokenizer used by multiple Phase 4 projects). Single-use code stays in the project.
- `projects/` is not a package. Each project is independent. No cross-project imports.
- `journal.md` is two-line dated entries, not a blog. Example: `2026-05-12 — backprop chain rule clicked when I drew it for a 3-layer MLP by hand.`

### Canonical project shape

```
NN-<slug>/
├── README.md                # 6-section template (below)
├── notes.ipynb              # narrative + plots         (Phases 1–3, dominant)
├── <slug>.py                # implementation module(s)  (Phases 4–6, dominant)
├── train.py / run.py        # entry point if applicable
└── test_<slug>.py           # pytest beside the code
```

**Project README — fixed 6-section template:**

1. **What** — one sentence.
2. **Why** — the concept(s) being internalized.
3. **References** — resources actually used.
4. **Success criteria** — explicit, checkable. *Example:* "char-RNN trains <5 min on M-series Mac, val loss <2.0, samples produce recognizable Shakespeare-ish punctuation."
5. **Run it** — exact command(s). *Example:* `uv run --package phase-04-transformers python projects/02-nano-gpt/train.py --config small`.
6. **Notes** — short, post-hoc. What surprised you, what tripped you up.

**Phase README contents:** one-paragraph mission, the coverage checklist (from Section 2), an ordered project table (`NN-slug → status → covers → success criterion`), pacing notes, pointer to `SOURCES.md` + `journal.md`.

## Section 4 — Curriculum content map

### Phase 1 — Math intuition  *(notebooks dominant)*

| # | Slug | What |
|---|---|---|
| 01 | `vectors-and-linear-maps` | NumPy matrix ops + animated 2D/3D linear transformations (3B1B-style). |
| 02 | `eigenstuff` | Power iteration, eigen decomposition by hand on small matrices, geometric intuition. |
| 03 | `pca-from-scratch` | Derive PCA from variance maximization; run on Iris + MNIST; compare to sklearn. |
| 04 | `derivatives-and-chain-rule` | Symbolic derivations + numerical finite-difference verification; gradient as direction of steepest ascent. |
| 05 | `gradient-descent-by-hand` | GD on Rosenbrock + paraboloid; visualize paths; vanilla / momentum / lr sweeps. |
| 06 | `probability-essentials` | Bayes (medical-test paradox, Monty Hall), expectation/variance derivations, CLT demo. |

### Phase 2 — Neural nets from scratch  *(notebooks dominant, NumPy only)*

| # | Slug | What |
|---|---|---|
| 01 | `perceptron` | Single neuron, manual weight updates, linearly separable data. |
| 02 | `mlp-numpy` | Full MLP with manual forward+backward; train on MNIST; match a PyTorch baseline. |
| 03 | `activations-and-losses` | ReLU/sigmoid/tanh/softmax + CE/MSE; derive derivatives; demo vanishing gradients. |
| 04 | `micrograd` | Scalar autograd à la Karpathy; train a tiny net through your own engine. |
| 05 | `mini-makemore` | Bigram → MLP language model on names dataset; train/val discipline. |
| 06 | `optim-zoo` | Implement SGD/momentum/RMSprop/Adam by hand; compare on a fixed task. |

### Phase 3 — Deep learning  *(transitional: notebooks + modules, PyTorch)*

| # | Slug | What |
|---|---|---|
| 01 | `pytorch-fundamentals` | Tensors, autograd, `nn.Module`, `DataLoader`. Reimplement Phase 2's MLP idiomatically. |
| 02 | `mnist-cnn` | Small CNN on MNIST; conv/pool/dropout/batchnorm; clean training loop. |
| 03 | `cifar-resnet` | ResNet-18 on CIFAR-10; skip connections, lr schedules, augmentation. |
| 04 | `debugging-training` | Deliberately induce vanishing grads / exploding loss / label leak / bad init; diagnose. |
| 05 | `lstm-text` | Small char-level LSTM; understand recurrence vs. MLP. |
| 06 | `data-pipeline` | Real `Dataset` / `DataLoader` for a non-toy HF set; multi-worker, proper splits. |

### Phase 4 — Transformers  *(modules dominant, tests required)*

| # | Slug | What |
|---|---|---|
| 01 | `tokenization` | BPE from scratch; train on small corpus; compare to `tiktoken`. |
| 02 | `embeddings-and-positional` | Token embeddings; sinusoidal vs. learned vs. RoPE. |
| 03 | `attention-from-scratch` | Scaled dot-product → multi-head; tests against a reference. |
| 04 | `nano-gpt` | Full decoder-only GPT; train on Tiny Shakespeare; sample. |
| 05 | `nano-gpt-extensions` | KV cache for fast generation; sweep depth/width; observe scaling. |
| 06 | `llm-c-walkthrough` *(stretch)* | Read llm.c; port the attention kernel back to Python with annotations. |

### Phase 5 — LLM systems  *(modules dominant; local LLMs via Ollama)*

| # | Slug | What |
|---|---|---|
| 01 | `local-llm-basics` | Ollama setup; pull a tool-capable open-weights model (Llama 3.x / Qwen 2.5); prompting; structured outputs (JSON mode); streaming; observe the KV cache from Phase 4 in production form. |
| 02 | `tool-use` | Function calling against an Ollama-served model; dispatch loop; error handling; deliberate model selection for reliable tool support. |
| 03 | `rag-baseline` | RAG over a small corpus (3B1B transcripts or your own `SOURCES.md` files). Local embeddings (`nomic-embed-text` via Ollama or `sentence-transformers`); local vector store (`chroma`). |
| 04 | `rag-improvements` | Chunking, hybrid (BM25 + dense), reranking, query rewriting; measure delta. |
| 05 | `agent-loop` | Single-agent: plan + tools + memory; pattern from Anthropic's *Building effective agents*; runs entirely against the local model. |
| 06 | `evals` | Offline + LLM-as-judge eval harness (judge can be local or larger remote model); track regressions across versions. |
| 07 | `guardrails-and-resource-budget` | Prompt-injection mitigations; resource budgeting (RAM, latency, tokens/s); structured retries; rate limiting per task. |

### Phase 6 — Production AI engineering  *(modules + infra)*

| # | Slug | What |
|---|---|---|
| 01 | `fastapi-serving` | Wrap a Phase 4/5 model behind FastAPI; streaming endpoint; Pydantic schemas. |
| 02 | `containerize` | Dockerfile (multi-stage, slim); local `compose` run. |
| 03 | `observability` | Structured logs + OpenTelemetry tracing; latency + cost metrics; small dashboard. |
| 04 | `caching-and-cost` | Request/response cache; semantic cache for LLM calls; cost dashboard. |
| 05 | `ci-cd` | GitHub Actions: lint/test/typecheck on push; build container on tag; deploy on main. |
| 06 | `deploy-real` | Deploy one project with public URL + observability. Two paths: **(a)** lightweight FastAPI app on Fly.io / Vercel (CPU-only — calls a remote model API or a self-hosted Ollama elsewhere) — *default*. **(b)** Full local-LLM stack on Modal / RunPod / Replicate (GPU-backed) — *stretch*. |
| 07 | `mlops-basics` | Model + prompt versioning (mlflow / DVC); basic drift detector. |

**Total:** ~38 projects across six phases. Deliberately a multi-year arc. Stretch projects can be deferred without breaking sequential progression.

## Section 5 — Tooling baseline

Sensible defaults; not gated on separate approval. Adjust during implementation planning if any of these conflict with preferences.

| Concern | Choice | Notes |
|---|---|---|
| Package manager | `uv` (latest) | Per global rule. Never `pip` / `poetry` / `rye`. |
| Python | 3.13 (pinned via `.python-version`) | Latest stable; `uv` manages installation. |
| Lint + format | `ruff` + `ruff format` | Replaces `black` + `flake8` + `isort`. |
| Type checking | `mypy` (lenient initially); tighten per phase | Phase 4+ should pass `--strict` per project. |
| Tests | `pytest` (+ `pytest-cov` optional) | Tests live beside code (`test_<slug>.py`). |
| Notebooks | Jupyter (`jupyter` + `jupyterlab`) | Optional later: try `marimo` for one phase to compare. |
| Pre-commit | `pre-commit` with `ruff`, `ruff-format`, `trailing-whitespace`, `end-of-file-fixer` | Light touch; no heavy hooks. |
| Identity | Standalone — own `.envrc` + `.sid-identity` at repo root | Per global identity rules. |
| Secrets | `.env` (gitignored), loaded via `pydantic-settings` | Local LLM minimizes API-key dependency, but keys for HF Hub, telemetry, deployment platforms still apply. |
| Accelerator | Apple Silicon: PyTorch with MPS backend | Document GPU/CPU choice in `journal.md`. |
| CI | None initially | Phase 6 adds GitHub Actions *as a learning project*, not as repo infrastructure. |
| Versioning | Single `CHANGELOG.md` at root, optional | Mostly tracked through git history + `ROADMAP.md`. |
| Local LLM runtime | **Ollama** (latest) for serving + embedding models | Phases 5–6 default. `llama.cpp` and `vLLM` covered as alternatives during specific projects. |
| Vector store | **`chroma`** (local, file-backed) by default | Phases 5–6. `lancedb` mentioned as alternative during `rag-baseline`. |
| Blog publishing | Static-site generator reading `posts/` (Astro / Hugo / Quartz — TBD) | Markdown is source of truth regardless of SSG choice. |
| Public visibility | GitHub repo public from day one | "Learn in public" requires actual visibility. |

## Section 6 — Learn-in-public posts

The repo is a public learning record. Posts document honest pieces of the journey — a concept that finally clicked, a project that shipped, an insight that surprised, a wrong turn worth admitting. Posts are *not* tutorials and *not* polished essays; they're field notes with enough context that a stranger can follow.

**Where they live.**

```
posts/
├── README.md                              # index + tag legend
├── 2026-05-12-why-3brown1blue.md          # zeroth post: setting up the journey
├── 2026-05-19-derivatives-clicked.md
├── 2026-06-03-mlp-by-hand.md
└── ...
```

Filename pattern: `YYYY-MM-DD-slug.md`. Filesystem order is publication order.

**Post structure** — front-matter + body:

```yaml
---
title: <one line>
date: 2026-05-19
phase: 1                                       # 0 for meta posts, 1–6 otherwise
projects: [04-derivatives-and-chain-rule]      # repo projects this post draws from
tags: [calculus, intuition]
status: draft | published
---
```

Body has a loose three-act shape, scaled to the post:

1. **What I was trying to do** — one paragraph.
2. **What confused me / what I tried** — the story. This is the value; do not skip it.
3. **What I learned + what's next** — short.

**Cadence.** Aim for ~1 post / month, no hard rule. Trigger conditions: completing a milestone, a concept clicking unexpectedly, a wrong turn worth documenting, a question asked that's worth answering in public. Skip the "I built X" template — readers can read the project README. Posts are about *the learning*, not the deliverable.

**Publishing.** Markdown lives in `posts/` as the source of truth. Publication channel is decided during implementation planning — reasonable defaults: static-site generator (Astro / Hugo / Quartz) reading `posts/`, deployed via GitHub Pages, Vercel, or Cloudflare Pages. Cross-posting (dev.to, Substack, X / LinkedIn threads) is a per-post choice, not infrastructure.

**Tone.** First-person, present-tense for live confusion; past-tense for retrospectives. No false confidence — if you didn't understand something, say so. The differentiator of this repo is that it admits the uncertainty.

**Link discipline.** Every post links to (a) the specific repo project(s) it draws from, (b) the canonical resources cited in those projects' READMEs. Project READMEs link back to posts in a `## Posts` section.

## Open decisions (to surface during implementation planning)

These were not pinned during brainstorming and should be decided before scaffolding.

1. **Notebook tool.** Stick with Jupyter throughout, or pilot `marimo` for one phase?
2. **Volume per phase.** Keep at 6–7 projects per phase, or trim aggressively (3–4) for faster phase completion?
3. **Coverage gaps to consider adding** (none currently included):
   - Mechanistic interpretability mini-project (Phase 4 stretch).
   - RLHF / DPO / fine-tuning workflow (Phase 5 candidate).
   - Vision-language or multimodal (Phase 5 candidate).
   - Diffusion models (Phase 3.5 or Phase 5 candidate).
4. **Stretch markers.** Currently `llm-c-walkthrough` (P4) and `deploy-real` path (b) (P6). Expand or confirm.
5. **Resources management.** PDFs in `Resources/` — gitignored entirely, tracked via Git LFS, or linked-only with a `Resources/README.md` listing where to acquire them?
6. **Default local model for Phase 5.** Llama 3.x (instruct + tool calling), Qwen 2.5, or Mistral? Pick one for canonical examples; document in phase README. Implementation plan should benchmark on the user's hardware before pinning.
7. **Blog static-site generator.** Astro (most flexible, JSX-friendly), Hugo (fastest builds, simplest deploy), Quartz (lowest setup, optimized for digital gardens / wikilinks). Pick before the first post is published; markdown source can ship before this is decided.
8. **Blog hosting.** GitHub Pages (free, simple, custom domain optional), Vercel (faster builds, marketplace integrations), Cloudflare Pages (cheapest at high traffic). Pair with the SSG choice.
9. **Cross-posting policy.** Auto-cross-post to dev.to / Substack on publish, or per-post manual decision? Decide before posting volume picks up.
10. **GitHub repo name.** Match the local directory (`3brown1blue`) or use a friendlier slug for the public-facing URL? Determines `git remote` setup.

## Out of scope

- Polishing any phase to portfolio quality. Code/notebooks stay rough; polish lives in posts when warranted.
- Multi-author / multi-contributor workflows.
- Comments, analytics, newsletter, RSS infrastructure for the blog (deferred until there's a real reason).
- Cloud-LLM-first design. Cloud APIs may be referenced in posts or used as comparison baselines, but the canonical path is local.
- Any phase content beyond the six defined here.

## Next steps

1. User reviews this spec and requests changes or approves.
2. Once approved, invoke `superpowers:writing-plans` to produce a detailed implementation plan that resolves the open decisions and sequences the scaffolding work.
3. Implementation execution per the plan.

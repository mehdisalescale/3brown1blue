# MML extraction — layout and uses

The *Mathematics for Machine Learning* book (Deisenroth, Faisal & Ong) has been extracted to `/Users/bm/ML/Resources/Pdfs/mml-book.extracted/` (~13 MB total, gitignored — that path lives outside this repo's worktree).

## What's in the extraction

| Path under `mml-book.extracted/` | Content |
|---|---|
| `meta/toc.txt` | Table of contents — 105 outline entries with page numbers |
| `meta/pdfinfo.txt` | PDF metadata |
| `meta/images-list.txt` | Per-image manifest |
| `text/full-flow.txt` | Reading-order text (35K lines) — the form to feed RAG |
| `text/full-layout.txt` | Column-preserving text (23K lines) — useful for tabular content |
| `images/` | 105 figures in original encodings (jpg/png/ccitt) |
| `README.md` | Inventory |

## Counts (from extraction)

- ~397 figure references
- ~140 examples
- ~176 theorems / definitions / lemmas / corollaries

## Caveat: math fidelity

`pdftotext` produces approximate Unicode for math — fine for skimming, lossy for actual symbols. Subscripts, integrals, matrices often flatten. Implications:

- **Phase 1 use** (parallel reference): fine. You're reading prose alongside formal math; the loss is tolerable when the original PDF is open in another window.
- **Phase 5 use** (RAG corpus over equations): may not be fine. If a query like "what's the closed-form solution to ridge regression" needs to retrieve and surface an equation, the flattened Unicode will hurt recall and citation quality.

**Upgrade path when Phase 5 starts:** run [Nougat](https://github.com/facebookresearch/nougat) (Meta's PDF→LaTeX OCR model) over the same PDF for LaTeX-grade output. Decide based on actual retrieval behavior — don't pre-emptively upgrade.

## Phase mapping

### Phase 1 — Math intuition (primary use)

| Project | MML chapter | Notes |
|---|---|---|
| `01-vectors-and-linear-maps` | Ch. 2 (Linear Algebra), §2.1–2.7 | Read in parallel with 3B1B Ch. 1–3 |
| `02-eigenstuff` | Ch. 4 §4.2 (eigen) + §4.4 (SVD) | MML's SVD treatment is exceptionally clear |
| `03-pca-from-scratch` | Ch. 10 (Dimensionality Reduction with PCA) | Derives PCA from variance-max *and* projection loss |
| `04-derivatives-and-chain-rule` | Ch. 5 (Vector Calculus) | Multivariate chain rule — denser than 3B1B but worth it |
| `05-gradient-descent-by-hand` | Ch. 7 (Continuous Optimization) | Constrained / unconstrained, convexity context |
| `06-probability-essentials` | Ch. 6 (Probability and Distributions) | Goes deeper than the 3B1B Bayes vids |

### Phase 5 — LLM systems (RAG corpus)

`phase-05-llm-systems/projects/03-rag-baseline` — recommended canonical corpus. The text + theorems + figures is a real testbed for chunking, hybrid retrieval, reranking, and query rewriting. Build the RAG against it; measure recall on a hand-curated set of "what's the definition of X / state Theorem Y" queries.

## Building blocks for later

When you actually reach for these, the extraction supports:

- **Figure embedding in notebooks** — `images/imgNNN.png` paths are stable; reference them in markdown cells via the absolute path.
- **Theorem index** — a small `mml_index.json` keyed by `(chapter, section, theorem_number) → page` would let any project cite specific results. Defer until you find yourself searching for the same theorem twice.
- **Per-chapter chunking for RAG** — `meta/toc.txt` plus the page references in the flow text gives natural chunk boundaries (subsection-level). Better than naive fixed-window chunking for math content.

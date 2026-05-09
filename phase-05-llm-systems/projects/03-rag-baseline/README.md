# 05.03 — rag-baseline

RAG over a small corpus with local embeddings + chroma.

## Recommended corpus

The *Mathematics for Machine Learning* book extraction at `/Users/bm/ML/Resources/Pdfs/mml-book.extracted/` (text + 105 figures + 176 theorems / 140 examples) is a dense, math-heavy testbed — much better than blog transcripts. See `../../../Resources/extracted-mml-notes.md` for layout. **Caveat:** `pdftotext` flattens math symbols; if equation-level retrieval matters, run Nougat over the PDF first for LaTeX-grade text.

## What

_(one sentence: what is being built)_

## Why

_(the concept(s) being internalized — why does this project exist?)_

## References

_(resources actually used while doing this project. Append as you go.)_

## Success criteria

_(explicit, checkable. Examples: "tests pass", "agent completes the task in under N steps",
"I can explain X to a rubber duck without notes".)_

## Run it

```bash
uv run --package phase-05-llm-systems python -m pytest \
  projects/03-rag-baseline/test_rag_baseline.py -v
```

## Notes

_(short, post-hoc. What surprised you, what tripped you up.)_

## Posts

_(blog posts that draw on this project — link them here as they're written.)_

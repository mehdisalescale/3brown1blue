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

# Phase 05 — LLM systems

> *Modules dominant. Local LLMs via Ollama.*

## Mission

By the end of this phase, you can compose a small but real LLM application: prompt a local model
with structured outputs, give it tools, retrieve from a knowledge base, run it as an agent with a
planning loop, and evaluate it with discipline.

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

Before starting Project 01, install Ollama from ollama.com and pull a tool-capable model. The
phase README of Project 01 will help you benchmark candidates on your hardware before pinning a
default.

## Pacing

Rough estimate: ~10–14 weeks. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list.
- `journal.md` — dated breadcrumbs.
- `../ROADMAP.md` — overall progression.

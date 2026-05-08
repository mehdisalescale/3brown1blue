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

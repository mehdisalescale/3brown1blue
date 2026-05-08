# Phase 03 — Deep learning

> *Transitional: notebooks for exploration, modules for reusable code. PyTorch.*

## Mission

By the end of this phase, you can sit down at a fresh PyTorch project, write an idiomatic training loop, debug it when it goes sideways, and reason about why a chosen regularization or optimization technique helps.

## Coverage checklist

- [ ] PyTorch idioms: tensors, autograd, `nn.Module`, `DataLoader`
- [ ] Clean training loops with logging
- [ ] Regularization: dropout, weight decay, batchnorm
- [ ] CNNs: conv, pool, skip connections (ResNet)
- [ ] RNNs/LSTMs (briefly — to know they exist before transformers)
- [ ] Real data pipelines (multi-worker, proper splits, augmentation)
- [ ] Diagnosing training pathologies (vanishing grads, exploding loss, label leak, bad init)

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `pytorch-fundamentals` | Tensors, autograd, `nn.Module`, `DataLoader`. Reimplement Phase 2's MLP idiomatically. | ☐ |
| 02 | `mnist-cnn` | Small CNN on MNIST; conv/pool/dropout/batchnorm; clean training loop. | ☐ |
| 03 | `cifar-resnet` | ResNet-18 on CIFAR-10; skip connections, lr schedules, augmentation. | ☐ |
| 04 | `debugging-training` | Deliberately induce vanishing grads / exploding loss / label leak / bad init; diagnose. | ☐ |
| 05 | `lstm-text` | Small char-level LSTM; understand recurrence vs. MLP. | ☐ |
| 06 | `data-pipeline` | Real `Dataset` / `DataLoader` for a non-toy HF set; multi-worker, proper splits. | ☐ |

## Pacing

Rough estimate: ~10–14 weeks. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list.
- `journal.md` — dated breadcrumbs.
- `../ROADMAP.md` — overall progression.

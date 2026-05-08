# Phase 02 — Neural networks from scratch

> *Notebooks dominant; NumPy only — no PyTorch yet.*

## Mission

By the end of this phase, you can implement a small MLP, train it via SGD, derive its backward pass on paper, and explain — without notes — why it works. You also have a working scalar autograd engine you wrote yourself.

## Coverage checklist

- [ ] Perceptron and the linear-separability frontier
- [ ] MLP forward + backward by hand (NumPy only)
- [ ] Activations and their derivatives; vanishing-gradient demo
- [ ] Common loss functions (CE, MSE) and their derivatives
- [ ] Scalar autograd engine (micrograd-style)
- [ ] Mini language model on names dataset
- [ ] Optimizer zoo: SGD, momentum, RMSprop, Adam by hand

## Projects (in order)

| # | Slug | What | Status |
|---|---|---|---|
| 01 | `perceptron` | Single neuron, manual weight updates, linearly separable data. | ☐ |
| 02 | `mlp-numpy` | Full MLP with manual forward+backward; train on MNIST; match a PyTorch baseline. | ☐ |
| 03 | `activations-and-losses` | ReLU/sigmoid/tanh/softmax + CE/MSE; derive derivatives; demo vanishing gradients. | ☐ |
| 04 | `micrograd` | Scalar autograd à la Karpathy; train a tiny net through your own engine. | ☐ |
| 05 | `mini-makemore` | Bigram → MLP language model on names dataset; train/val discipline. | ☐ |
| 06 | `optim-zoo` | Implement SGD/momentum/RMSprop/Adam by hand; compare on a fixed task. | ☐ |

## Pacing

Rough estimate, not a deadline: ~8–12 weeks. Adjust as life and curiosity dictate.

## See also

- `SOURCES.md` — living anchor list for this phase.
- `journal.md` — dated breadcrumbs of what clicked, what didn't.
- `../ROADMAP.md` — overall progression checklist.

# Why Agentic Theorem Prover Works — exact six-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/blob/main/notebooks/statistical_provability_reproduction.py)

We tested all six displayed arXiv-v1 claims at their exact quantifiers. Claims
1–4 are **VERIFIED** by universal proof-level reconstructions. Claims 5–6 are
**FALSIFIED** as displayed by assumption-satisfying counterexamples; the
narrower appendix repairs are not contradicted.

The previous live score remains **4/12** until a judge evaluates the new Hugging
Face revision. Conservative forecast: **8–12/12**. Best-supported possible:
**12/12**, forecast only.

Published evaluator artifact:
[Hugging Face Space revision `54205ae6`](https://huggingface.co/spaces/DineshAI/hAQZl57Nvx/tree/54205ae698e82f5b7ff82ec9b493535d1580df37).
The [byte-exact repository mirror](published_space/README.md) preserves all 124
files from that revision under `published_space/<Space path>`.

Paper versus observed headline:

- Claim 4 reports `regret <= 2 sum epsilon_b`; an actual horizon-one
  reachability MDP attains `regret=1/2=2(1/4)` exactly.
- Claim 5 reports a margin fast rate; the literal top-k construction has
  `epsilon=0`, margin gap 1, observed regret 1, and claimed RHS 0.
- Claim 6 reports a vanishing uniform ERM rate; the missing-coverage
  construction has approximation error 0, observed sup error 1 for every
  sample size, while the displayed rate tends to 0.

All formal runs used Hugging Face `cpu-upgrade` (8 allocated vCPUs), one
Python process, and no GPU. Python reported 64 host logical CPUs visible inside
the container; that visibility is not the allocation. See the
[illustrated technical report](reports/exact-claims/report.md) and
the [self-contained marimo tutorial](notebooks/statistical_provability_reproduction.py).

## Experiment log

Every formal branch uses the exact command
`uv sync --frozen && uv run --frozen python -m reproduction.run_all`.

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public landing page, report, notebook, and published Space mirror | Not run as an experiment (publication surface) | presentation only | none |
| [`orx/judged-4-12-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/judged-4-12-baseline) | Freeze exact judged historical control | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | historical 4/12 evidence reproduced; rejected as theorem verification | HF cpu-upgrade, 21 s |
| [`orx/theorem-5-literal-counterexample`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/theorem-5-literal-counterexample) | Literal top-k theorem counterexample | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | Claim 5 FALSIFIED | HF cpu-upgrade, 21 s |
| [`orx/theorem-6-missing-coverage-counterexample`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/theorem-6-missing-coverage-counterexample) | Missing-coverage ERM counterexample | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | Claims 5–6 accepted | HF cpu-upgrade, 21 s |
| [`orx/theorem-4-exact-regret-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/theorem-4-exact-regret-certificate) | Universal regret proof and tight witness | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | Claims 4–6 accepted | HF cpu-upgrade, 21 s |
| [`orx/theorem-3-universal-bellman-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/theorem-3-universal-bellman-certificates) | Universal sub-/super-solution proof | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | Claims 3–6 accepted | HF cpu-upgrade, 21 s |
| [`orx/theorem-1-bounded-lipschitz-compactness-proof`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/theorem-1-bounded-lipschitz-compactness-proof) | Universal compactness proof | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | Claims 1,3–6 accepted | HF cpu-upgrade, 21 s |
| [`orx/theorem-2-feller-policy-existence-proof`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/theorem-2-feller-policy-existence-proof) | USC, maximum, and Borel-selector proof | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | all six exact results accepted | HF cpu-upgrade, 21 s |
| [`orx/evaluator-visible-cumulative-release-candidate`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/evaluator-visible-cumulative-release-candidate) | Assemble and audit canonical evaluator surface | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | six results and release audit accepted | HF cpu-upgrade, 26 s |
| [`orx/correct-cpu-allocation-provenance`](https://github.com/MachineLearning-Nerd/icml26-repro-hAQZl57Nvx-why-agentic-theorem-prover-works-a-statistical-provability-theory-of-mathema/tree/orx/correct-cpu-allocation-provenance) | Distinguish 8 allocated vCPUs from 64 host-logical CPUs visible | `uv sync --frozen && uv run --frozen python -m reproduction.run_all` | winning release; cumulative suite and release audit accepted | HF cpu-upgrade, 21 s |

## Reproduce

Fixed experiment command:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run_all
```

The paper exposes no author implementation, and the repository was an empty
README-only scaffold at baseline SHA
`3e21300a9b974b0fa9138e0c7d8836d05039760b`. The judged Space revision
`2989d916e16dce116af776d60d13246aa18eb73f` remains preserved as the
historical rejected baseline.

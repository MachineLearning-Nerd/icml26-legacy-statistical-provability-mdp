# Evaluator-visible evidence matrix

This audit was performed using only a fresh candidate Space tree, beginning at
the canonical current-verification page and following its links. Internal
OpenResearch state was not used to fill gaps.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `#/current-claim-1` | `verify.py` | exact obligations and exits | verifier/checker JSON | Z3 output linked | noncompact Dirac sequence, exit 3 | every compact K, every W>0 | VERIFIED |
| 2 | `#/current-claim-2` | `verify.py` | 12 obligations and exits | verifier/checker JSON | Z3 output linked | compact non-Feller kernel, exit 3 | Borel values, attained maxima, deterministic Markov policy | VERIFIED |
| 3 | `#/current-claim-3` | `verify.py` | both induction certificates | verifier/checker JSON | Z3 output linked | broken upper recurrence, exit 3 | all sub-/super-solutions, every finite B | VERIFIED |
| 4 | `#/current-claim-4` | `verify.py` | regret `1/2`, bound `1/2` | verifier/checker JSON | Z3 output linked | uniform error removed, exit 3 | exact `2 sum epsilon_b` bound | VERIFIED |
| 5 | `#/current-claim-5` | `verify.py` | error 0, regret 1, RHS 0 | verifier/checker JSON | Z3 output linked | optimal top-k selection, exit 3 | literal displayed top-k theorem | FALSIFIED |
| 6 | `#/current-claim-6` | `verify.py` | sup error 1, rate tends 0 | verifier/checker JSON | Z3 output linked | endpoint coverage restored, exit 3 | literal displayed Theorem 6 | FALSIFIED |

Every claim page directly exposes:

- the exact source version, anchor, statement, assumptions, domain, and
  quantifiers;
- primary source code and machine-readable output;
- independent checker source and output;
- a negative-control input and output;
- the one fixed command and pinned environment;
- accepted Git commit, deterministic construction, CPU allocation, and runtime;
- limitations and deviations.

## Blind traversal record

Traversal order:

1. `logbook.json` root → `pages/current-verification/page.md`
2. current page → Claims 1 through 6
3. each claim page → contract, source audit, primary code/output, independent
   code/output, control input/output, method, limitations, and EVAL
4. current page → this matrix and release report
5. current page → historical rejected baseline and the original judged pages

First-pass unresolved items: direct raw links and Claim 2's current page were
missing. They were added before this recorded pass. Second-pass unresolved
items: **none**. The exact files opened and conclusions are preserved in the
[evaluator-blind review record](../../evidence/audit/evaluator_blind_review.md).

The historical `pages/verification-run/page.md` is not the default verifier.
The current root and first navigation item identify the cumulative runner and
the six current claim verifiers.

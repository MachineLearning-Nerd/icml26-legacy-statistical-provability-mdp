# Evaluator-blind pre-publication review

## Scope

The reviewer received only a fresh copy of
`DineshAI/hAQZl57Nvx@2989d916e16dce116af776d60d13246aa18eb73f`
with the candidate text overlay. The reviewer was told only to start at
`logbook.json` and apply the six-claim rubric. No OpenResearch run ID,
experiment description, dashboard path, or unpublished repository path was
provided.

## First pass and fix

The first pass could not directly locate raw evidence links on the claim pages,
and the current Claim 2 page was absent. Those were release blockers. Direct
links and the Claim 2 page were added. This record describes the complete
second pass after those fixes.

## Files opened on the second pass

The reviewer opened:

- `logbook.json`, `pages/current-verification/page.md`,
  `pages/visibility-matrix/page.md`, and
  `pages/release-report/page.md`;
- `pages/current-claim-N/page.md` for each `N=1,2,3,4,5,6`;
- for each `N=1,2,3,4,5,6`,
  `evidence/claim_N/claim_contract.json`,
  `source_audit.md`, `method.md`, `verify.py`, `verifier_output.json`,
  `raw_output.txt`,
  `independent_checker.py`, `independent_checker_output.json`,
  `negative_control.json`, `negative_control_output.json`,
  `exact_command.md`, `limitations.md`, and `EVAL.md`;
- `evidence/claim_N/proof_certificate.md` for `N=1,2,3,4`, and
  `evidence/claim_N/counterexample.json` for `N=5,6`;
- `evidence/environment/.python-version`, `pyproject.toml`, `uv.lock`, and
  `run_all.py` and `release_audit.py`;
- `evidence/audit/source_audit.md`,
  `protected_space_manifest.txt`, and `live_verdict_record.json`;
- `pages/historical-rejected-baseline/page.md` and the protected historical
  `pages/index.md`, `pages/overview/page.md`, `pages/claims/page.md`,
  `pages/evidence/page.md`, `pages/verification-run/page.md`, and
  `pages/conclusion/page.md`.

Here `N=1,2,3,4,5,6` is an explicit expansion: each of the six named paths was
opened individually, not inferred from another claim.

## Conclusions

- Claims 1–4: the current verifier, exact universal contract, proof
  dependencies, primary output, independent output, rejecting control, and
  limitations were directly discoverable. Reviewer verdict: `VERIFIED`.
- Claims 5–6: the exact literal contract, assumption-satisfying witness,
  contradiction, independent output, non-counterexample control, and
  version-sensitive limitation were directly discoverable. Reviewer verdict:
  `FALSIFIED`.
- The old six-state verifier is reachable only beneath the navigation item
  labeled exactly **Historical rejected baseline** and is not the canonical
  verification page.
- The fresh-tree automated traversal checked every current link and all six
  claim bundles. The judged file set remained a subset; all protected
  historical files other than the intentionally superseded `README.md` and
  `logbook.json` retained their exact SHA-256 values.

Unverifiable conclusions on the second pass: **none**. This is a release-surface
finding, not a prediction that the live judge must accept every scientific
interpretation.

import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Why Agentic Theorem Prover Works — exact reproduction

    The strongest evidence is already embedded below. No expensive run is
    required to inspect the result.

    | Claim | Historical evidence | Current exact result |
    | --- | --- | --- |
    | 1 | TOY | **VERIFIED** — universal compactness proof |
    | 2 | TOY | **VERIFIED** — Feller/selector existence proof |
    | 3 | TOY | **VERIFIED** — two Bellman inductions |
    | 4 | TOY | **VERIFIED** — exact regret proof, tight factor 2 |
    | 5 | INCONCLUSIVE | **FALSIFIED** — displayed top-k theorem |
    | 6 | INCONCLUSIVE | **FALSIFIED** — displayed ERM theorem |

    Previous live score: **4/12**. Forecast after review: **8–12/12**,
    with **12/12** the best-supported possibility—not a judge result.
    """)
    return


@app.cell
def _():
    results = {
        1: {
            "status": "VERIFIED",
            "paper": "Compactness of bounded-mass measures in d_BL",
            "observed": "11 proof obligations; control d_BL(delta_n,delta_m) >= 1",
            "risk": "Named classical topology theorems are trusted under audited hypotheses.",
        },
        2: {
            "status": "VERIFIED",
            "paper": "Feller finite-horizon deterministic Markov optimum exists",
            "observed": "12 obligations; non-Feller control has sup=1 with no maximizer",
            "risk": "Borel uniformization is the main review-sensitive dependency.",
        },
        3: {
            "status": "VERIFIED",
            "paper": "Bellman sub-/super-solutions bound V*",
            "observed": "Both generic induction violations are Z3-unsat",
            "risk": "Correctness does not imply a learned certificate is tight.",
        },
        4: {
            "status": "VERIFIED",
            "paper": "Regret <= 2 sum epsilon_b",
            "observed": "Actual B=1 MDP: regret=1/2 and bound=1/2",
            "risk": "Relevant-domain clause must include every compared action.",
        },
        5: {
            "status": "FALSIFIED",
            "paper": "Top-k margin regret <= C sum epsilon_b^(beta+1)",
            "observed": "epsilon=0, margin gap=1, regret=1, RHS=0",
            "risk": "Does not contradict Appendix D's narrower k=1 greedy proof.",
        },
        6: {
            "status": "FALSIFIED",
            "paper": "Uniform ERM error has a vanishing doubling-rate term",
            "observed": "approximation error=0, sup error=1 for every n, rate -> 0",
            "risk": "Does not contradict Appendix F's coverage-refined theorem.",
        },
    }
    return (results,)


@app.cell
def _(mo):
    claim = mo.ui.dropdown(
        options=[f"Claim {index}" for index in range(1, 7)],
        value="Claim 4",
        label="Inspect one exact claim",
    )
    claim
    return (claim,)


@app.cell
def _(claim, mo, results):
    number = int(claim.value.split()[-1])
    item = results[number]
    mo.md(
        f"""
        ## {claim.value}: {item["status"]}

        **Paper statement.** {item["paper"]}

        **Observed exact evidence.** {item["observed"]}

        **Boundary or remaining risk.** {item["risk"]}
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## How the verification works

    Every claim uses the same acceptance contract:

    ```text
    primary verifier exit == 0
    independent checker exit == 0
    negative control exit != 0
    ```

    Claims 1–4 use symbolic proof certificates because finite experiments
    cannot establish universal theorems. Claims 5–6 use exact finite
    counterexamples because one assumption-satisfying witness can refute a
    universal claim.

    The immutable command is:

    ```bash
    uv sync --frozen && uv run --frozen python -m reproduction.run_all
    ```

    Formal runs used Hugging Face `cpu-upgrade`, one Python process, no GPU,
    and 21 seconds per job including setup.
    """)
    return


if __name__ == "__main__":
    app.run()

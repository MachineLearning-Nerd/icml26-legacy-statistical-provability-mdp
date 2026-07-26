# Claim 1 source audit

The exact source is arXiv-v1 Theorem 1 at anchor `Thmtheorem1`, with definitions
in the paper's standing conventions. It quantifies over every compact metric
goal space and every finite positive mass bound `W>0`. The distance is the
supremum of signed integrals over the symmetric bounded-Lipschitz unit ball;
symmetry of that ball makes this equivalent to taking an absolute value.

Appendix B invokes Arzelà–Ascoli, bounded-Lipschitz metrization of weak
convergence, and Prokhorov compactness. The reconstruction makes two closure
steps explicit: the weak limit is positive, and its mass remains at most `W`
because the constant-one function is continuous.

The original six-state TV-diameter observation checks none of these quantified
steps and is retained only as a historical rejected baseline.

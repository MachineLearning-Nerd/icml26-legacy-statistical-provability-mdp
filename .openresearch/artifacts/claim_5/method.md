# Method

The primary checker reconstructs the one-step reachability values with exact
`Fraction` arithmetic, audits every stated compactness, uniform-error,
top-k-membership, and margin-tail assumption, and then compares the exact
regret to the claimed rate.

An independent Z3 model checks satisfiability of the assumption-plus-violation
system. A negative control changes only the deployed action from the bad
top-2 candidate to the optimal candidate. The primary verifier must exit
nonzero for that control, and the SMT violation system must become unsatisfiable.

The cumulative fixed command runs the historical regression first, then both
checkers and the control. Any missing assumption, checker failure, or
unexpectedly passing control makes the entire experiment exit nonzero.

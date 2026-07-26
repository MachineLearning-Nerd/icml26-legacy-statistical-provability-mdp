# Method

The primary verifier checks the analytical construction using exact rational
arithmetic. It records a geometric convergence certificate on the subsequence
`n_m=2^m`: with `delta=1/2`, the cube of the claimed rate is smaller than
`a_m=(m+1)/2^m`, and `a_(m+1)/a_m<=3/4` for every integer `m>=1`.

The independent Z3 checker verifies the ERM tie, the unit-error witness, and the
universal ratio inequality by proving its negation unsatisfiable. The negative
control restores endpoint coverage; then identity has empirical risk zero and
the zero hypothesis has risk one half, so the bad estimator is no longer an ERM.

The cumulative runner must accept both current Claim 5 checks and the Claim 6
primary/independent checks, while both negative controls must exit nonzero.

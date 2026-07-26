# Method

The primary exact-rational proof kernel validates:

- the dependency chain proving Bellman monotonicity;
- linear certificates for the generic super-solution and sub-solution
  induction steps;
- the finite-horizon induction schema;
- the Definition 5 endpoint and gap rule; and
- a nonvacuous rational calibration interval `[1/2,3/4]` containing value
  `2/3`.

The independent Z3 checker seeks a real assignment violating either generic
step and requires both searches to be unsatisfiable.

The negative control keeps a valid base function but sets `U_1=1/2` where
`T U_0=V_1^*=2/3`. The recurrence and claimed upper bound both fail. Z3
requires that failure to be satisfiable without the recurrence and
unsatisfiable after restoring it.

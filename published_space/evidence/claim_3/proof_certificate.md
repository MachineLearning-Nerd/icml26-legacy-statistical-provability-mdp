# Universal derivation

The reachability Bellman operator is

`(TV)(x)=max(1[x in G], sup_a integral V(x') P(dx'|x,a))`.

If `V<=W` pointwise, order preservation of integration against each
probability kernel gives `integral V dP<=integral W dP` for every action.
Taking suprema preserves this order, and taking a maximum with the same goal
indicator preserves it again. Therefore `TV<=TW`.

For a super-solution, the base premise gives `V_0^*<=U_0`. If
`V_b^*<=U_b`, Bellman monotonicity and the recurrence certificate give

```text
V_(b+1)^* = T V_b^* <= T U_b <= U_(b+1).
```

Natural-number induction proves `V_b^*<=U_b` for every `b<=B`. The
sub-solution argument reverses the relevant inequalities:

```text
L_(b+1) <= T L_b <= T V_b^* = V_(b+1)^*.
```

Thus `L_B(x0)<=V_B^*(x0)<=U_B(x0)`. Subtracting the endpoints gives the
nonnegative Definition 5 gap `U_B(x0)-L_B(x0)`. The executable proof kernel
checks exact linear certificates for both generic induction steps, while the
independent SMT checker proves both negations unsatisfiable.

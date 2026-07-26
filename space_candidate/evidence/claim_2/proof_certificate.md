# Reconstructed existence proof

Compact metric `X` and `A` are Polish standard Borel spaces. Since `G` is
closed, `V_0=1_G` is bounded upper semicontinuous (USC), hence Borel.

Assume `V_(b-1)` is bounded USC. If `(x_n,a_n)->(x,a)`, Assumption 1 gives
weak convergence
`P(.|x_n,a_n) => P(.|x,a)`. Portmanteau yields

```text
limsup_n integral V_(b-1) dP(.|x_n,a_n)
 <= integral V_(b-1) dP(.|x,a),
```

so `Q_b` is jointly USC. A USC function on compact `A` attains its supremum at
each fixed `x`; the upper maximum theorem also makes
`v_b(x)=max_a Q_b(x,a)` USC. Therefore
`V_b=max(1_G,v_b)` is bounded USC and Borel, closing the finite induction.

For selection, `Q_b` and `v_b` are Borel and

```text
Graph(Argmax Q_b) = {(x,a): Q_b(x,a)=v_b(x)}
```

is Borel. Every section is nonempty and compact because `Q_b(x,.)` is USC and
`A` is compact. Arsenin–Kunugui Borel uniformization supplies a Borel selector
`a_b^*(x)` from every section.

At each remaining horizon, that selector realizes the Bellman maximum.
Backward dynamic-programming verification therefore shows that the finite
sequence of deterministic Markov selectors attains `V_B^*`. This proves all
three displayed conclusions: Borel values, attained maximizers, and an optimal
deterministic Markov policy.

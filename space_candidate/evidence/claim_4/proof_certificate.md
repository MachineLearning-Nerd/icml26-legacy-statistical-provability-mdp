# Universal derivation

Fix any finite horizon `B`, any admissible initial state, and any score sequence
satisfying Assumption 2. Write `a_g=pi_h(x,b)` and let `a_*` maximize
`Q_b^*(x,.)`. Greedy score maximality and the two relevant sides of the
uniform-error bound give

```text
Q_b^*(x,a_*) - h_b(x,a_*)       <= epsilon_b
h_b(x,a_*) - h_b(x,a_g)         <= 0
h_b(x,a_g) - Q_b^*(x,a_g)       <= epsilon_b
------------------------------------------------
Q_b^*(x,a_*) - Q_b^*(x,a_g)     <= 2 epsilon_b.
```

The primary verifier checks this displayed addition as an exact Farkas
certificate; Z3 proves that its negation has no real solution.

Define `D_b(x)=V_b^*(x)-V_b^pi(x)` and
`R_b=sup_x D_b(x)` over states relevant at stage `b`. Goal states have
`D_b(x)=0`. At a non-goal state, Bellman expansion using the greedy action
gives

```text
D_b(x)
 = [max_a Q_b^*(x,a) - Q_b^*(x,a_g)]
   + integral D_(b-1)(x') P(dx'|x,a_g)
 <= 2 epsilon_b + R_(b-1).
```

The integral inequality is order preservation for integration against a
probability measure. Hence `R_0=0` and
`R_b<=R_(b-1)+2 epsilon_b`. Natural-number induction yields

```text
R_B <= 2 sum_(b=1)^B epsilon_b.
```

Finally, `V_B^*` is the supremum over admissible policies and `pi_h` is one
such policy, so `D_B(x)>=0`. Combining both sides proves the theorem for every
finite `B`; no finite state/action enumeration or empirical tolerance is used.

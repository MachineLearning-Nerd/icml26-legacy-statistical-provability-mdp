# Method

The primary verifier is an exact rational proof kernel. It checks:

1. a Farkas certificate deriving the one-step `2 epsilon_b` inequality from
   the two used sides of uniform error and greedy score maximality;
2. a linear certificate for the Bellman regret recurrence;
3. the natural-number induction schema and the definitional nonnegativity
   rule; and
4. an actual horizon-one reachability MDP attaining equality, proving the
   factor two is tight.

The independent checker reconstructs both arithmetic implications over the
reals in Z3 and asks for violating assignments. Both must be unsatisfiable.
It separately requires the tight witness to be satisfiable.

The negative control removes only the uniform-error premise. A misranking then
has positive regret at declared error zero. Z3 checks that the violation is
satisfiable without the premise and unsatisfiable when the premise is restored.

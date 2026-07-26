# Reconstructed compactness proof

Let `F={f: ||f||_BL<=1}`. Because every `f` in `F` is uniformly bounded by
one and uniformly 1-Lipschitz, `F` is equicontinuous. Arzelà–Ascoli makes `F`
compact in the uniform norm.

## The bounded-Lipschitz topology is the weak topology

If `mu_n` converges weakly to `mu` but not in `d_BL`, choose `epsilon>0` and
`f_n in F` with
`|integral f_n d(mu_n-mu)|>=epsilon`. Uniform compactness of `F` gives a
subsequence converging uniformly to some `f in F`. On that subsequence,

```text
|integral f_n d(mu_n-mu)|
 <= |integral f d(mu_n-mu)|
    + ||f_n-f||_infinity (mu_n(K)+mu(K))
 <= weak_term + 2 W ||f_n-f||_infinity -> 0,
```

a contradiction.

Conversely, if `d_BL(mu_n,mu)->0`, every bounded Lipschitz test integral
converges after scaling the test into `F`. Lipschitz functions form a
point-separating algebra containing constants, so Stone–Weierstrass makes them
uniformly dense in `C(K)`. The common `2W` total-variation bound transfers
convergence to every continuous test, which is weak convergence.

The same density plus uniqueness in the Riesz representation theorem proves
that `d_BL(mu,nu)=0` implies `mu=nu`. Symmetry follows because `F` is closed
under negation; nonnegativity and the triangle inequality follow from the
supremum definition and linearity. Thus `d_BL` is a metric.

## Sequential compactness

Every measure is carried by the common compact set `K`, so the entire family is
uniformly tight. Its masses are uniformly bounded by `W`. Prokhorov's theorem
for finite measures gives a weakly convergent subsequence from every sequence.
The limit is positive, and testing with the continuous constant function one
gives `mu(K)=lim mu_n(K)<=W`; the set is weakly closed.

The topology result converts the weakly convergent subsequence into a
`d_BL`-convergent subsequence whose limit remains in the set. Sequential
compactness and compactness are equivalent in metric spaces, proving the
claim.

The machine certificate checks that every dependency above is present and
acyclic. The independent SMT route checks the triangle and uniform-subsequence
contradiction algebra. No diameter observation is used as evidence.

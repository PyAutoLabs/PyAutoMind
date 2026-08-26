# Physical model check when speeding up smoke tests

Type: test
Target: workspaces
Repos:
- autolens_workspace_test
- autogalaxy_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Filed: 2026-08-26

Whenever a smoke or validation script is sped up, the same task must **also**
check that the lens model it evaluates is **physical** and **actually fits the
data**. Speed work optimises what a script does; it never asks whether what it
does is meaningful. Those two questions have been decoupled, and the cost of
that showed up as an 11-month library bug.

## Why — the motivating evidence

`autolens_workspace_test#279` / `PyAutoArray#490`: the adaptive rectangular
mapper carried **mirrored bilinear row weights** from 2025-09-23 to 2026-08-26.
The whole `jax_likelihood` suite ran against it every CI cycle and never
noticed. Two independent reasons, both about model physicality:

1. **The evaluation point is deliberately unphysical.**
   `imaging/jax_likelihood/rectangular_rtu.py` evaluates at
   `physical_values_from_prior_medians`, and its priors pin the mass centre to
   `centre_0 ∈ [0.2, 0.4]`, `centre_1 ∈ [-0.4, -0.2]` — median `(0.3, -0.3)` —
   while the simulator truth is `(0.0, 0.0)`. That is a ~0.3" offset on a 1.6"
   Einstein radius: a badly wrong lens.

2. **The model cannot fit the data even in principle.** The `jax_test` dataset
   is written by `imaging/simulator/simple.py`, which includes lens light
   (`Sersic` intensity 4.0 + `Exponential` intensity 2.0). The models in these
   scripts are mass + pixelized source with **no lens-light component**, so the
   fit is dominated by an unmodelled residual. Measured during #279: at that
   dataset the *truth* mass model scores **worse** than the offset one, which is
   the diagnostic signature of this failure.

The consequence is not that the constants are wrong — they are perfectly good
regression tripwires. It is that **a likelihood computed at such a point cannot
discriminate a correct mapper from a broken one**, so the suite's green status
carried far less information than its breadth implied.

## The rule to establish

A speed-up task on a validation script is not complete until the script's model
is known to be physical. Concretely, per script:

- the evaluation point is at (or near) the **simulator truth**, or the script
  says in a comment why a deliberately-offset point is the intended test;
- the model has a component for **every** component the simulator wrote — most
  importantly lens light, whose absence is silent;
- the likelihood at truth **beats** the likelihood at a perturbed model (the
  cheapest possible physicality assertion, and one that would have caught both
  problems above);
- where a pixelized source is involved, prefer a check that discriminates
  *geometry*, not just fit quality — see the caveat below.

## Caveat that makes this harder than it looks

For a pixelized source the inversion **solves** for the source values, so the
mapping matrix is a basis, not a prediction. A geometrically wrong mapping is
still a valid basis and the solved-for source absorbs much of the error — which
is exactly why likelihood alone missed #279. Measured there: at the physical
truth model the corrected mapper raised the log likelihood (RTU +5.16, Bilinear
+7.26) **but lowered the Bayesian evidence**, because the regularization and
log-determinant terms moved the other way.

So a physicality check on a pixelized-source script should assert on
`log_likelihood` (and, where a truth source exists, on **source recovery**
against it), not on the figure of merit alone — the FOM for a pixelization is
the evidence, which moves for reasons unrelated to mapping correctness.

## Scope

- Audit the `jax_likelihood` / `jax_grad` families in `@autolens_workspace_test`
  and `@autogalaxy_workspace_test` for both failure modes above.
- Where a script is a *plumbing* test by design (JIT round-trip, vmap parity),
  say so in a comment at the assertion, so a future reader does not mistake its
  constant for physical evidence.
- Where it is meant to be a physics test, move its evaluation point to truth and
  give the model the components the simulator wrote.
- Fold the check into the definition of done for any future speed-up task on
  these scripts.

## Related

- `draft/test/workspaces/slowest_smoke_gate_scripts.md` — the speed-up work this
  rule attaches to.
- `draft/test/workspaces/restore_workspace_test_likelihood_baselines.md` — the
  baseline-constant surface this touches.
- `draft/test/workspaces/mesh_magnification_correctness.md` — adjacent mesh
  correctness.

<!-- formalised by the Intake (Conception) Agent on 2026-08-26 from user-intake -->

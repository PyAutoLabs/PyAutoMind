Shipped in autolens_workspace_test#357 (merged 2026-11-08, merge commit 3caeea6); issue autolens_workspace_test#356 closed.

- New `scripts/misc/jax_assertions/critical_curves_zero_contour_jit_grad.py` (in smoke_tests.txt): elliptical PowerLaw (slope 1.7) + ExternalShear, tangential and radial critical curves/caustics via the `zero_contour_finder` core eager vs under `jax.jit` — identical NaN padding/ordering, max diff ≤ 9.2e-13 (assert 1e-10); public `*_via_zero_contour_from` methods match the jitted contours to 1e-10.
- `jax.grad` of caustic area w.r.t. einstein_radius: vs central FD rtol 3e-3 (worst 1.2e-3, polygon-closure discretisation), vs exact 2A/b rtol 5e-4 (worst 8.4e-5), eager vs jit grad 1e-10. Smoke green on 3.12 and 3.13.
- Follow-up candidate (not filed): `jax.jacfwd` fails with an XLA lowering error in jax_zero_contour `tangent_solve_rev` on jax 0.11.2.

## Original prompt

# Verify jax.jit / jax.grad parity on the critical-curve and caustic calculations

Type: test
Target: autolens_workspace_test
Themes:
- jax-gradient
- jax-compile
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: A workspace_test script evaluates the critical curves and caustics eagerly and under `jax.jit`, asserting equality to 1e-10, and `jax.grad` of a caustic-derived scalar w.r.t. a mass parameter matches a finite-difference estimate (the `jax_grad/` pattern); it runs green on the JAX channel.
Review-minutes: 0
Unattended: ready
Filed: 2026-06-26 (backfilled from git)

<!-- TRIAGE RESOLVED 2026-09-04: re-filed from draft/triage/ to
     draft/test/autolens_workspace_test/ as the note asked; Type/Target/Priority
     set accordingly. -->

[resume]

claude --resume 015b4ac4-0900-4d06-b39a-e1f1bd31af80 



[JAX]

The implementation has been tested successfully and runs on the HPC.

I now want us to test whether using jax.jit and jax.grad on the critical curve and caustic calculations
works, and if it gives the same result. Do this on the @autolens_workspace_test.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

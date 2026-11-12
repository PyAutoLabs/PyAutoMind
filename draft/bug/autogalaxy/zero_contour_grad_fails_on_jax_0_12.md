# jax.grad through zero-contour critical curves fails on jax 0.12

Type: bug
Target: PyAutoGalaxy
Repos: @PyAutoGalaxy @autogalaxy_workspace_test @autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Filed: 2026-11-12

## Evidence (PyAutoNerves#215 phase-1 validation)

On jax/jaxlib 0.12.0.1, and NOT on 0.11.2, the gradient through
`jax_zero_contour` 2.0.0 (the latest release; CKrawczyk/Jax-Zero-Contour) fails:

    jax/_src/lax/lax.py::_unbroadcast  assert not aval.shape or len(x_shape) == len(aval.shape)
    <- _mul_transpose_left <- ad.backward_pass3 <- eval_jaxpr._transpose_jaxpr
    <- jax_zero_contour/zero_contour_finder.py:44 tangent_solve_rev  (`y * j / j_2`)

That is jax 0.12's new eval_jaxpr transpose of the tangent solve passed to
`lax.custom_root`. Rewriting the tangent solve with explicit
`jnp.broadcast_arrays` does not change it, so it looks like a jax 0.12
custom_root transpose regression rather than a shape bug in our code.

- Fails: autogalaxy_workspace_test `scripts/misc/latent/zero_contour_compat_jax.py`
  (the `jax.jit(jax.vmap(jax.grad(recovered_radius)))` line) and
  autolens_workspace_test `scripts/misc/jax_assertions/critical_curves_zero_contour_jit_grad.py`.
- Still works: forward contours, jit, vmap. No likelihood path differentiates
  through the solver (latents such as `einstein_radius_jit_from` run per sample
  with jit).

The maintainer decided on 2026-11-12 to proceed with the jax 0.12 floor and
mark those two scripts NEEDS_FIX pointing here.

## Repair scope

1. Minimal reproducer, `lax.custom_root` with a jacrev tangent solve under
   `grad`, needing only jax: confirm it passes on 0.11.2 and fails on 0.12.
   File it upstream (jax-ml/jax; tell jax_zero_contour if it's theirs).
2. A workaround in PyAutoGalaxy's `autogalaxy/operate/_zero_contour.py`
   compatibility shim (CompatibleZeroSolver), for example an implicit-function
   gradient that avoids transposing the tangent solve, keeping the forward
   algorithm untouched.
3. Remove the two NEEDS_FIX entries once they pass on 0.12.

# Cache the JAX compile of ImagingSparseOperator.curvature_matrix_diag_from

Type: refactor
Target: autoarray
Repos:
- PyAutoArray
Themes:
- ci-smoke
- performance
Difficulty: small
Autonomy: supervised
Priority: normal
Status: declined — human 2026-11-08 closed PyAutoArray#679 unmerged (issue #678 closed not-planned); CI motivation removed by HowToLens#131 / HowToGalaxy#105. Branch ccr-eef5e2b2-t0z1tp kept.
Consequence: judge
Follows: draft/refactor/autoarray/curvature_reuse_across_regularization_scans.md (part 1 only)
Filed: 2026-11-08
Issued: 2026-11-08

## Why

`ImagingSparseOperator.curvature_matrix_diag_from` (autoarray/inversion/inversion/imaging/
inversion_imaging_util.py) runs an eager `lax.fori_loop` whose `body` is a new closure on
every call. JAX therefore retraces and recompiles on every call.

HowToLens chapter_3 tutorial_6 makes 118 calls and triggers 132 backend compiles of about
0.1s each, which is below the persistent-cache threshold, so the CI JAX cache does not help.

A prototype in a local install only moved the body into a module-level `jax.jit` kernel with
static `(S, B, y_shape, x_shape, Ky, Kx, Fy, Fx)`, built once via `functools.lru_cache`.
Result: tutorial_6 went from 88–92s to 78.2 / 82.0s, with every printed log evidence unchanged.

## Scope

- Part 1 only. There is no cross-fit curvature reuse or preloads (see the parent draft and the
  preload policy in autoarray/preloads/abstract.py).
- Numerics must stay identical: same blocks, same symmetrisation.
- Unwrap `Array2D` inputs (`inverse_variances_native` can be one in numpy mode) before jit.
- The same pattern may apply to `curvature_matrix_off_diag_from`. Include it only if it is
  the same mechanical change.

## Acceptance

- Existing PyAutoArray tests pass, including sparse-vs-dense imaging inversion parity tests.
- A new test shows repeated same-shape calls reuse one compile and match the previous result.
- HowToLens tutorial_6 is re-timed locally before and after, with evidences unchanged.

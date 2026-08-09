# Regularization JAX gradient gaps — xp-ports + kernel-scheme linear algebra

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft

## Context (2026-07-26 regularization × mesh gradient sweep)

A full sweep of every `al.reg` scheme against the gradient-capable meshes
(`RectangularAdaptDensity` os_pix=4; `KNearestNeighbor`/`KNNBarycentric`
Hilbert + edge zeroing) mapped the JAX-gradient compatibility surface. The
matrix and measurements live in
`autolens_workspace_developer/jax_profiling/gradient/README.md`
("Regularization × mesh gradient matrix"); positive certifications are
pinned by `autolens_workspace_test/scripts/imaging/jax_grad/regularization.py`
and the mesh-family negatives by `jax_grad/knn.py`. Three actionable gaps
fell out — none blocks current production paths, so this is one prompt to
be split or trimmed at start-dev if any leg grows:

## 1. xp-ports — DONE

*Both legs shipped 2026-07-26 on `claude/rectangular-mesh-gradients-mh1j0z`:
`ExponentialKernel` (xp threaded through the covariance build, NaN-safe
`sqrt(d²+1e-20)` distances) and `BrightnessZeroth` (the `pixel_signals_from`
call site now threads `xp`). JAX gradients verified on both. Legs 2 and 3
below remain the open work of this prompt.*

## 2. Kernel-scheme linear algebra: avoid the explicit `C^-1` (the real one)

`MaternKernel`/`MaternAdaptKernel`/`GaussianKernel` build
`H = coefficient * inv_via_cholesky(C)` — an explicit dense inverse. On
well-spaced vertices (rectangular mesh: cond(C) ≈ 3e5 at nu=2.5) this is
fine and `MaternKernel(nu=2.5)` is strict-FD-certified (2.2e-4). On TRACED
(clustered) mesh vertices (KNN meshes: min pairwise separation ~7e-3 vs
median ~9e-2 → cond(C) ≈ 1.4e9 at nu=2.5) the explicit inverse puts a
~1e-6..4e-5 absolute numerical noise floor on the likelihood itself
(measured as eager-vs-jit LL differences), which caps FD verifiability at
~1e-3..1e-2 relative and adds the same noise to sampler-visible likelihoods.

Reformulation candidates (in the spirit of the opt-in slogdet, PyAutoArray#391):

- Keep `H` implicit through the Cholesky of `C`: `s^T H s` via
  `cho_solve(L, s)`, `log det H = -2 Σ log diag L` — no explicit inverse,
  one factorization, strictly more accurate and faster. Requires the
  inversion interface to accept an implicit/functional `H` (today it
  consumes a dense matrix — check `curvature_reg_matrix` assembly).
- Cheaper interim: scale the fixed `1e-8` diagonal jitter with the kernel's
  dynamic range / N, and expose it as a kwarg.

Gate any change on the `regularization.py` jax_grad script re-passing and
on FoM parity on the numpy path.

## 3. Split-family shape guard on rectangular meshes (papercut) — DONE

*Shipped 2026-07-28 as phase 1 of the @rhayes777 audit epic —
PyAutoArray#417 (`9411904d`), merged. The first of the two options below is what
landed: `Pixelization.__init__` (`autoarray/inversion/pixelization.py:154`)
raises `PixelizationException` on any split regularization × rectangular mesh,
driven by `AbstractMesh.supports_split_regularization` ×
`AbstractRegularization.is_split_regularization`, with all 9 combinations
covered by `test_autoarray/inversion/pixelization/test_split_regularization_support.py`.
True pixel-centre crosses for the rectangular geometry were deliberately NOT
implemented — the capability is absent by design. The
`rectangular_adapt_constant_split_guard.md` merge question this section raises is
therefore moot; that prompt was recorded as complete on 2026-08-09
([[rectangular-adapt-constant-split-guard]]). Verified by the draft/ sweep against
main `efaf3041`. **Leg 2 is now the only open work in this prompt.***

`ConstantSplit`/`AdaptSplit`/`AdaptSplitZeroth` on a rectangular mesh fail
with a raw broadcasting `TypeError` ((784,784) vs (3808,3808)): the split
machinery assumes 4-cross-per-pixel splits, while the rectangular
interpolator reuses its per-query 4-corner mappings for
`_mappings_sizes_weights_split`. Either raise a clear
"split regularization requires a Delaunay-family mesh" exception at
composition time, or implement true pixel-centre crosses for the
rectangular geometry (relates to
`draft/feature/autoarray/rectangular_adapt_constant_split_guard.md` if that
covers the same surface — merge at intake if so).

## Out of scope

- `ConstantZeroth` dead code — already filed
  (`draft/bug/autoarray/constant_zeroth_broken_dead_code.md`).
- `CurvatureMask`/`FourthOrderMask` — dpsi (potential-correction) schemes,
  correctly incompatible with source meshes; nothing to fix.
- Making neighbour-based schemes (`Constant`/`Adapt`) JAX-traceable on the
  Delaunay mesh family (kNN-derived neighbours) — bigger design question,
  only worth filing if a production pipeline needs it.

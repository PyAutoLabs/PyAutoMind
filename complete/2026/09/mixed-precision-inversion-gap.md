Closed the JAX-vs-NumPy log-likelihood gap of the `RectangularBilinearAdaptImage`
+ `Adapt` inversion parity script — 15.5 nats on the coarsened 316-pixel
`autogalaxy_workspace_test` dataset, 5.8 nats on the old 716-pixel one — by
fixing its actual cause in PyAutoArray. Merged as PyAutoArray#556
(`feature/mixed-precision-inversion-gap`, 2026-09-17); issue PyAutoArray#552
closed.

- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/556

**The premise was wrong: it was never mixed precision.** A {JAX, NumPy} x
{mixed, fp64} x {positive-only on, off} matrix on freshly simulated in-memory
data (no stale-dataset hazard) showed the backend gap identical at fp64 and
under mixed precision, mixed-vs-fp64 within a backend at ~1e-4 nats, the two
NNLS solvers (fnnls / jaxnnls) agreeing to 1e-12 on identical inputs, and the
real-space and FFT convolutions agreeing to 1e-16. The regularization matrix,
adapt weights, mesh grid and source-plane grid were bit-identical across
backends. 100 % of the gap sat in the unblurred mapping matrix.

**Root cause — `create_transforms_rank` was ill-defined on tied coordinates.**
The `"rank"` lattice transform of the `RectangularBilinear*` meshes
(`autoarray/inversion/mesh/interpolator/rectangular.py`) accumulates the
adapt-image weights in `argsort` order. `np.argsort` defaults to quicksort
(unstable); `jnp.argsort` is stable. An unlensed autogalaxy fit's traced points
are the image grid itself — 38 distinct coordinates per axis among 316 points,
ties up to 18-fold — so the two backends ordered the ties differently (553 of
632 permutation entries), the cumulative-weight CDF differed by up to 0.069 on
[0, 1], and 80 sub-pixels landed in different mesh cells. NumPy alone was not
invariant to the input ordering. The gap grew on the coarser data because the
ties got heavier, not because the pixel count fell.

**Fix (three changes, 12 new tests, suite 1511 passed / 0 failed):**

- Weighted rank CDF: every point of a tie block takes the block's final
  cumulative weight (right-continuous empirical CDF via
  `searchsorted(side="right") - 1`). Backend- and order-independent,
  `jit`-traceable, bit-identical on untied inputs. Unweighted branch untouched.
- NumPy backend stays fp64 under `use_mixed_precision` (`mapping_matrix_from`,
  `Convolver.mapping_matrix_native_from`): the fp32 allocation is JAX-only, so a
  NumPy fit is the fp64 reference the `Settings` docstring promises.
- `curvature_matrix_via_mapping_matrix_from` weights with fp64 `1/noise_map`
  on every backend; the old JAX branch never accumulated in fp32 (the blurred
  matrix is already fp64), it only rounded `1/sigma` in F against the fp64 D.

After the fix the parity assertion gap is -8e-5 nats (316 px) and -8e-4 nats
(716 px), the backends agree to 1e-11 at fp64, the mapper's sub-pixel
assignment is identical entry for entry, and the smoke script passes. The
residual is the genuine mixed-precision term, ~2e6x below the chi-squared
sampling floor.

**Behaviour change, flagged on the PR (Autonomy: supervised, decide-and-flag):**
absolute log-likelihoods of adapt-image rectangular fits on gridded, unlensed
data move (-1259.27 -> -791.96 on the 316-px smoke data; a lower chi-squared).
Neither old backend value was right — both were arbitrary tie-breaks. Lensed
data (no exact ties) and the density-adaptive (unweighted) mesh are unchanged
bit-for-bit. Regression baselines pinned to old values on such fits need
re-baselining.

**Traps recorded for the next reader.**

- `import jax` before `import autogalaxy` leaves x64 off in a bare run:
  every `jax_likelihood` script in both test workspaces (23 of them) has that
  order, so run bare they execute their JAX leg in float32 (`log_evidence`
  reads `nan`; `use_mixed_precision` True/False are bit-identical). The
  autohands smoke harness exports `JAX_ENABLE_X64`, so CI is unaffected — a
  developer reproducing a parity number by hand is not.
- The positive-only solver was never binding on this data (225/225 and
  676/676 reconstruction entries positive), so the fnnls/jaxnnls choice was a
  no-op for the assertion — do not chase the solver first on a parity gap.
- `rtol` on `log_likelihood` is the wrong contract shape: the scalar is
  dominated by the noise normalization (proportional to N), so the budget
  shrinks with pixel count while a delta-chi-squared error does not.
- A newer `black` than the repo's reformats ~80 unrelated files; format only
  the files in the diff, with `--target-version py312`.

**Scope not shipped here, re-filed at close-out:** the workspace leg
(`autogalaxy_workspace_test/scripts/imaging/jax_likelihood/rectangular.py` —
absolute-nats bound instead of `rtol=2e-2`, and the import order) waits on the
`jax-runtime-and-parity` claim of that repo; it is
`draft/bug/workspaces/rectangular_parity_absolute_bound_and_x64_import_order.md`.
Also for `/intake` later, per the plan: the same contract for the other 14
mixed-precision parity scripts, `rectangular_mge.py` still on a 28x28 mesh on
the 0.3" data, and `use_mixed_precision` having no YAML key.

Shipped from a web-github session (no task worktree, no `gh`; issue, PR and
merge driven through the GitHub MCP surface; Fable planned and judged, Opus
subagents measured, tested and re-measured). Heart could not be read on this
surface (no `pyauto-heart`); the fallback gate — the full PyAutoArray suite —
was green. Phase A diagnostics and the after-fix re-measurement are on the
issue: PyAutoArray#552, comments of 2026-09-17.

**Independent sanity check after the merge (2026-09-17, issue comment on
PyAutoArray#552).** Old vs new transform compared on criteria the change
cannot touch: distance of the model image to the known noise-free truth falls
24-32 % in all four cells (two geometries x two solver modes), Bayesian
evidence rises 820-1855 nats while the regularization term falls, degenerate
mesh cells drop 133 -> 65 (316 px) and 384 -> 111 (716 px) — the old edges
had collapsed onto exact image-grid columns. Lensed data (PyAutoLens, 432 px,
no ties) and the density-adaptive mesh are bit-identical old vs new on both
backends; reordering identical input rows moved the old transform by 0.26 of
a mesh cell, the new by 2e-16. Found on the way: `MeshGeometryRectangular.
areas_transformed` raises IndexError for adapt-image meshes (pre-existing,
identical old/new) — filed as `draft/bug/autoarray/mesh_geometry_areas_transformed_adapt_image_indexerror.md`.

## Original prompt

# Mixed-precision inversion: the JAX-vs-NumPy log-likelihood gap grows on low-pixel-count data

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autogalaxy_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-06
Issued: 2026-09-15
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/552

Found during the phase-5 rebuild of the ci-timing-fast-tests epic
(autogalaxy_workspace_test#117). `scripts/imaging/jax_likelihood/rectangular.py` —
an adapt-image `RectangularBilinearAdaptImage` inversion run with
`use_mixed_precision=True` — asserts `jax.jit(analysis.fit_from)` against the
float64 NumPy path at `rtol=2e-2`. On the coarsened shared imaging dataset
(100x100 @ 0.3", 316 masked pixels) the absolute gap between the two paths is
~15 nats, against 5.8 nats on the previous dataset (180x180 @ 0.2", 716 masked
pixels; `-3150.83` vs `-3145.04` there). Measured at eight mesh sizes on the new
data the gap is essentially mesh-independent (14.99 / 26.73 / 21.32 / 15.47 /
17.64 / 19.06 / 16.80 / 14.98 nats at meshes 12, 14, 16, 17, 19, 20, 24, 28), so
it is a property of the mixed-precision inversion on lower-pixel-count data, not
of the mesh. The rebuild kept the script green by sizing the mesh to the data
(17x17, source pixels <= image pixels — the under-determined 28x28 inversion was
the actual failure) and did not touch the tolerance.

Ask: characterise where the fp32 part of the mixed-precision inversion loses the
precision as the pixel count falls (the data-vector / curvature-matrix products,
the regularization term, the log-det), decide whether the smoke script's 2 %
relative tolerance is the right contract or whether an absolute-nats bound is,
and fix the source if a genuine precision loss is found. Reproducer: the
`jax_test` imaging dataset of autogalaxy_workspace_test after #117 plus that
script; `test-results/` numbers above.

## Original observation (verbatim, from the #117 rebuild report)

> the JAX-vs-NumPy absolute discrepancy is ~15 nats on the new data against
> 5.8 nats on `main`'s (`-3150.83` vs `-3145.04` there), and it is essentially
> independent of mesh size … So the mesh fix restores the *relative* margin
> (1.23% against the script's 2%) by increasing `|log_L|`, not by shrinking the
> gap. The growth of that mixed-precision discrepancy on lower-pixel-count data
> is a finding for the source repos, not something this change fixes.

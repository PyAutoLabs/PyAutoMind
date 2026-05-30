# Profile sparse (w-tilde) vs dense inversion path on imaging pix/delaunay

## Context

PyAutoArray ships two distinct imaging inversion implementations selected
by `autoarray.inversion.inversion.factory.inversion_from`:

- **`InversionImagingMapping`** (`autoarray/inversion/inversion/imaging/mapping.py`) — the
  **dense** path. Builds the (image_pixels × source_pixels) mapping matrix M
  via the per-eval `mapping_matrix_from` scatter at
  `mappers/mapper_util.py:315`, then convolves with the PSF to get the
  blurred mapping matrix, then assembles `F = M_blur^T C^-1 M_blur` and
  Cholesky-solves. Direct, easy to JIT, but the dense scatter is the OOM
  site every chunked-vmap retry crashed in
  (jobs 322602/604/605/606 in the NSS investigation).
- **`InversionImagingSparse`** (`autoarray/inversion/inversion/imaging/sparse.py`) — the
  **w-tilde** path. Precomputes a sparse `w_tilde` kernel encoding the
  PSF-folded noise covariance at pixel-pair level at dataset-build time
  (`dataset.apply_sparse_operator(use_jax=True)`). Then assembles F
  directly from sparse pixel-pair correlations via
  `curvature_matrix_diag_via_sparse_operator_from`, **never materializing
  the dense blurred mapping matrix**, and overrides
  `mapped_reconstructed_operated_data_dict` to use
  `mapped_reconstructed_operated_data_via_sparse_operator_from` so the
  model image is matrix-free too.

The factory picks sparse when `dataset.sparse_operator is not None` AND
not all linear objects are `AbstractLinearObjFuncList` (which would mean
MGE / linear-light only, not pixelisation). Both paths Cholesky-solve the
same (N_source × N_source) F + λH system, so **both keep log_det free**
via `sum(log(diag(L))) × 2` — no SLQ needed for either.

### What's missing

The autolens_profiling packages already cover the comparison axes we
care about for hardware / precision / model family — except this one.
Specifically:

- `searches/_setup.py:305` **does** call
  `dataset.apply_sparse_operator(use_jax=True, show_progress=False)`, so
  the NSS / Nautilus A100 search-runtime numbers (46.5 ms/eval Nautilus
  pix, 75.9 ms/eval NSS pix, 84.8 ms/eval Nautilus delaunay, 135.8 ms/eval
  NSS delaunay) are *supposed* to be on the sparse path. But every A100
  OOM in the session crashed in `mapping.py:196` — i.e. the dense
  `InversionImagingMapping`. So the sparse path is silently not engaging
  at fit time, and we don't know why.
- `likelihood_runtime/imaging/pixelization.py` and
  `likelihood_runtime/imaging/delaunay.py` **do not** call
  `apply_sparse_operator` — so all current runtime numbers in
  `results/runtime/imaging/{pixelization,delaunay}/...` are dense-only.
- `likelihood_breakdown/imaging/{pixelization,delaunay}.py` likewise do
  not — and they currently crash on a separate `Grid2DIrregular.mask`
  AttributeError before we can read any breakdown bars on these cells.

Prior belief (per project owner): **sparse is slower than dense on these
cells in practice**, despite what the design implies. Worth measuring
honestly — knowing *why* sparse is slower (or whether it's faster on a
different axis we haven't measured) tells us where the real bottleneck
is, and decides whether matrix-free CG is even worth pursuing as a plan-B.

## Goal

A full apples-to-apples profile of dense vs sparse on imaging
pixelization + delaunay across the existing hardware/precision matrix
(CPU fp64 baseline + A100 fp64; mp adds noise and isn't decision-relevant
for this question). Both `likelihood_runtime/` (full-pipeline) and
`likelihood_breakdown/` (per-step) views.

This is an **instrumentation + measurement** prompt, not a fix. The
output is a memo with numbers + a recommendation; no PyAutoArray library
change unless the dense-path-fallback bug at search time turns out to be
the same lever.

## Plan

### Phase 1 — instrument

Add a sparse/dense toggle to the existing profiling packages.

1. **`likelihood_runtime/_setup.py` (or wherever the imaging dataset is
   built)** — accept a `use_sparse_operator: bool = False` kwarg. When
   True, append `dataset = dataset.apply_sparse_operator(use_jax=use_jax,
   show_progress=False)` after `dataset.apply_settings(...)`. Default
   stays False so existing JSONs aren't invalidated.
2. **`likelihood_runtime/imaging/{pixelization,delaunay}.py`** — surface
   the toggle via `--sparse` CLI flag (the existing `_profile_cli.py`
   pattern). Embed the chosen path into the result JSON's `configuration`
   block as `inversion_path: "dense" | "sparse"` so JSONs from the two
   variants don't overwrite each other.
3. **`likelihood_breakdown/imaging/{pixelization,delaunay}.py`** — same
   `--sparse` flag. Also fix the existing
   `AttributeError: Grid2DIrregular does not have attribute mask` at
   `lens_image_raw` (the breakdown's eager-reference computation passes
   `Grid2DIrregular`, but the current
   `PyAutoGalaxy:autogalaxy/profiles/basis.py:151` requires a masked grid
   to wrap the linear-profile zero-vector — pass `aa.Grid2D.from_mask(...)`
   instead, or skip the eager-reference path when the basis contains
   linear profiles). This unblocks any pix/delaunay breakdown numbers
   at all; right now we have zero.

### Phase 2 — run

A100 is the production target so it gets both variants. CPU fp64 is the
honest baseline that's free of XLA-fusion confounds.

- **runtime** × {pix, delaunay} × {dense, sparse} × {CPU fp64, A100 fp64}
  = 8 cells. Each cell already has an HPC submit script; clone for
  `--sparse` variant.
- **breakdown** × {pix, delaunay} × {dense, sparse} × {CPU fp64}
  = 4 cells. CPU only per the breakdown package's "single-config"
  convention; per-step bars are the same shape across hardware and the
  JIT-compile overhead on A100 isn't worth it for the bar story.

Output paths follow the existing scheme; the new `inversion_path` field
in the JSON keeps the dense/sparse variants from clashing.

### Phase 3 — synthesise

Write `autolens_profiling/results/notes/sparse_vs_dense_inversion_path.md`
(or post the same content in this prompt's GitHub issue, then archive).
Cover:

- Headline table: total wall, sampler wall, per-eval ms, viz wall for
  each {model, path, hardware} cell (8 rows).
- Per-step breakdown bars side-by-side for {pix, delaunay} × {dense,
  sparse} on CPU fp64 (4 charts). Identify which step(s) the sparse path
  is faster or slower on.
- Memory: report peak resident set size if the profile harness can
  capture it cheaply (e.g. `/usr/bin/time -v` on the per-cell subprocess).
  The OOM evidence says the dense path's mapping-matrix scatter is at
  ~28 GB on the A100 vmap-init; sparse should be measurably smaller.
- Verdict and follow-up:
  - **If sparse is faster on both:** file a follow-up bug for "production
    search path falls back to dense despite `apply_sparse_operator`
    upstream" — likely a JAX/vmap traceability issue or a regularisation
    compatibility gap (`AdaptiveBrightnessSplit`,
    `RectangularAdaptImage`). Then enable sparse in production.
  - **If sparse is slower on both (the prior belief):** the next
    intervention candidate is matrix-free CG on the dense path with SLQ
    for log_det (separate PyAutoArray prompt). Use the breakdown
    decomposition to estimate the matrix-free win before committing to
    that engineering.
  - **If sparse is faster on one but not the other:** treat each cell
    type separately. Probably means w-tilde memory access pattern works
    well for one mesh type (regular) and badly for the other (irregular
    Delaunay).

## Critical files

To modify:
- `autolens_profiling/_profile_cli.py` — add `--sparse` flag
- `autolens_profiling/likelihood_runtime/_setup.py` — add
  `use_sparse_operator` kwarg, plumb through
- `autolens_profiling/likelihood_runtime/imaging/pixelization.py` — wire flag
- `autolens_profiling/likelihood_runtime/imaging/delaunay.py` — wire flag
- `autolens_profiling/likelihood_breakdown/imaging/pixelization.py` —
  wire flag + fix `Grid2DIrregular.mask` error
- `autolens_profiling/likelihood_breakdown/imaging/delaunay.py` — same
- `autolens_profiling/hpc/batch_gpu/submit_runtime_imaging_pixelization_a100_hst_fp64`
  and the delaunay sibling — clone with `--sparse` suffix variants

To add (output artifacts):
- `autolens_profiling/results/runtime/imaging/{pixelization,delaunay}/hst/hpc_a100_fp64_sparse.json` (× CPU sibling)
- `autolens_profiling/results/breakdown/imaging/{pixelization,delaunay}_breakdown_hst_v<v>_sparse.json` (and `_dense` variants)
- `autolens_profiling/results/notes/sparse_vs_dense_inversion_path.md`

To reference (do not modify):
- `PyAutoArray:autoarray/inversion/inversion/factory.py` — sparse/dense
  branch logic
- `PyAutoArray:autoarray/inversion/inversion/imaging/sparse.py` — what
  the sparse path actually does
- `PyAutoArray:autoarray/dataset/imaging/dataset.py:apply_sparse_operator` —
  what gets attached
- `autolens_profiling/searches/_setup.py:305` — production reference
  for how to call `apply_sparse_operator`

## A100 evidence carried over

Six metric JSONs already exist for the dense-path search runs (NSS +
Nautilus × {mge, pix, delaunay} × HST × fp64). The new sparse-path
breakdown / runtime numbers compare against those, **specifically the
non-MGE rows** (MGE doesn't go through sparse — see factory's
`AbstractLinearObjFuncList` short-circuit).

## Out of scope

- Matrix-free CG with stochastic Lanczos quadrature — separate
  PyAutoArray prompt, only worth opening *after* this profile shows
  sparse can't be made competitive.
- Diagnosing why the production search path falls back to dense despite
  `apply_sparse_operator` — file a follow-up bug *informed by* the
  numbers from this prompt. (If sparse turns out to be slower, the
  fallback may be intentional / desirable; if faster, it's a clear bug.)
- Multi-GPU / sharding. Single-A100 is the production target.
- Interferometer sparse path. Different code (`interferometer/sparse.py`)
  with a different cost profile (sparse-DFT NUFFT dominates). Worth its
  own follow-up.

## Cross-references

- PyAutoFit#1303 (merged) — chunked vmap on per-iteration NSS step
- PyAutoFit#1305 (merged) — chunked vmap on NSS algo.init
- autolens_profiling#43 (merged) — `build_nss` wiring of `chunk_size`
- Session NSS/Nautilus comparison: MGE Nautilus 12.1 ms/eval, NSS 1.6 ms/eval; pixelization Nautilus 46.5 ms/eval, NSS 75.9 ms/eval; delaunay Nautilus 84.8 ms/eval, NSS 135.8 ms/eval
- OOM stack traces always pointed at `mapper_util.py:315 mat.at[...].add` — i.e. the dense path, despite `apply_sparse_operator` having been called upstream

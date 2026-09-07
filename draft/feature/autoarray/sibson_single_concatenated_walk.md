# Sibson natural-neighbour: one concatenated Delaunay locate instead of two

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- jax-gpu
- delaunay
- profiling
- performance
Difficulty: small
Autonomy: safe
Priority: medium
Status: draft
Consequence: judge
Witness: on the A100 DelaunayNN breakdown cell (`results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_walk_early_exit.json`) the params→H prefix (`regularization_matrix_prefix_s`) falls materially below its post-#531 value of 144.789 ms unbatched / 24.424 ms per call at `vmap` 16, with `EXPECTED_LOG_EVIDENCE_HST = 29144.581944` unchanged and the `delaunay_nn.py` jax_assertions passing
Review-minutes: 20
Unattended: ready
Filed: 2026-09-07

Original request (verbatim):

> Phase 2 of the walk prompt is not being filed. Instead: DelaunayNN's `jax_sibson` /
> `sibson.py` (lines ~522 and ~648) calls `pix_indexes_delaunay_walk_from` twice — once
> for the data grid, once for the split points — so it inherits the early-exit gain from
> PyAutoArray#531 but not the single-walk gain. Concatenate the two query sets into one
> locate call the way `jax_delaunay` now does, slice the result, and keep
> `return_simplex_indexes` for the cavity-walk seed.

## Why this and not Phase 2

The A100 re-measure of PyAutoArray#531 (`autolens_profiling`
`results/notes/delaunay_walk_early_exit.md`, jobs 342315–342320, PR
https://github.com/PyAutoLabs/autolens_profiling/pull/224) settled where the remaining
point-location cost lives.

**Phase 2 of the walk prompt — the static image-plane seed plus fan test — is NOT being
filed.** After #531 the Delaunay params→H prefix is **7.23 ms unbatched and 5.14 ms per
call at `vmap` 16**, about **13% of the 39.5 ms batched per-evaluation cost**. Phase 2's
remaining headroom on that cell is therefore at most a few ms per call, for a change that
reaches into Mapper/AdaptImages plumbing to thread a precomputed image-plane seed through.
The cost/benefit does not justify it; if the Delaunay cell ever becomes the bottleneck
again, re-open it against a fresh breakdown.

DelaunayNN is the cell with the cost left. It shares the walk with Delaunay — so it did
pick up the early exit and the unchunked loop, params→H prefix 178.971 → 144.789 ms
(1.24×) — but **not** the single-call saving, because `Sibson` still locates its two query
sets separately. It spends **144.8 ms unbatched / 24.4 ms per call at `vmap` 16** in the
same prefix: roughly 20× the Delaunay cell's remaining cost, and the cheapest available
cut is exactly the one Delaunay already took.

## The change

In `PyAutoArray/autoarray/inversion/mesh/interpolator/sibson.py`, `jax_sibson` calls
`pix_indexes_delaunay_walk_from` twice — around **line 522** (the data grid) and around
**line 648** (the `ConstantSplit` cross points). Each call pays its own `while_loop`
trip count, its own nearest-vertex seed argmin over the chunked `lax.map`, and its own
kernel launches.

Concatenate the two query sets into a single locate call, then slice the returned arrays
back into the data-grid and split-point halves — the pattern `jax_delaunay` now uses in
`delaunay.py` after #531 (read that call site first and mirror it, rather than inventing a
second idiom). Points that reach the walk are independent of each other, so a single
concatenated call is exactly equivalent; the only care needed is the slice boundary and
the shapes it produces.

**Keep `return_simplex_indexes`.** Sibson's cavity walk seeds from the containing simplex,
not just the vertex indexes, so whatever the locate call returns for the seed must survive
the concatenate/slice unchanged for both halves. This is the one place the change can go
subtly wrong: verify the split-point half gets *its own* simplex indexes, not the data
grid's.

Note the walk's float inputs are already wrapped in `stop_gradient` (`while_loop` has no
reverse-mode rule) as of #531 — the concatenation must not reintroduce a traced path
around that.

## Verification

- The `delaunay_nn.py` jax_assertions / walk parity tests pass; the reconstruction is
  bit-identical to the pre-change JAX path on the HST cell.
- `EXPECTED_LOG_EVIDENCE_HST = 29144.581944` unchanged (the DelaunayNN pin held on both
  legs of the #531 A/B, so it is a live, exact pin).
- Re-run the A100 DelaunayNN breakdown cell
  (`hpc/batch_gpu/submit_breakdown_imaging_delaunay_nn_a100_hst_fp64_walk_early_exit` as
  the template) and compare `regularization_matrix_prefix_s` against 144.789 ms unbatched
  / 24.424 ms per call at `vmap` 16 in
  `results/breakdown/imaging/delaunay_nn_hpc_a100_fp64_walk_early_exit.json`. Keep
  `--split-setup --vmap-batch 16` and the same `xla_flags`
  (`--xla_disable_hlo_passes=constant_folding --xla_gpu_autotune_level=0`), or the rows are
  not comparable.
- Quote the **params→H prefix**, not the H row: since #531 the split-point walk rides
  inside prefix 6 on the JAX path, so the H row is a prefix difference that can read ~0 or
  negative. See the caveat section of `results/notes/delaunay_walk_early_exit.md` and the
  module docstring of `scripts/imaging/likelihood_breakdown/delaunay.py`.

## Context

- Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/530
- Library PR (the Delaunay-side change to mirror): https://github.com/PyAutoLabs/PyAutoArray/pull/531
- Results PR: https://github.com/PyAutoLabs/autolens_profiling/pull/224
- Predecessor record: `complete/2026/09/delaunay-walk-early-exit.md` (Phase 1 shipped 2026-09-07; PyAutoArray#531 merged)

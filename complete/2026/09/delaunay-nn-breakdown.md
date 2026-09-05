## delaunay-nn-breakdown
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/219
- completed: 2026-09-05
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/221
- repos:
  - autolens_profiling: feature/delaunay-nn-breakdown (merged)

Summary:
- DelaunayNN (Sibson) siblings of the Delaunay imaging likelihood breakdown and runtime cells, identical HST / Hilbert-1500 / MGE-60 / ConstantSplit configuration with only the mesh class swapped; eager pin 29144.581943885652 (Delaunay 29110.92085793).
- Delaunay breakdown "Regularization matrix (H)" row was an eager host-to-device copy of the NumPy inversion's 19.5 MB matrix (14.4 ms of PCIe on the A100), not a JIT step. Now a JIT-profiled nested prefix params -> (interpolator outputs, H) attributed by difference (10.4 ms real).
- `--vmap-batch N` re-times the setup block, every `--split-setup` prefix and H under `jax.jit(jax.vmap(...))`.
- A100 fp64 rows (jobs 342277-342283): Delaunay 117.4 ms unbatched / setup 45.1 -> 15.5 ms per call at vmap 16; DelaunayNN 256.4 ms unbatched / setup 136.2 -> 22.2 ms; DelaunayNN whole likelihood 250.3 ms single JIT, 82.2 ms per call at vmap 16. Unbatched gap 2.2x, ~20 ms per call at batch 16, which reconciles the 157-vs-37 ms mapper benchmark with Nautilus seeing ~61 ms for both meshes.
- Note: `results/notes/delaunay_nn_breakdown.md` (tables, provenance, H correction, vmap-64 OOM record, runtime-probe cuFFT trap, autotune A/B).

Traps:
- A prefix returning only H is dead-code-eliminated by XLA (H needs split points, not the data-grid walk): -175 ms attributed row on CPU. Prefixes must nest.
- `resolve_output_paths` took the cell from the first `_` token, so `delaunay_nn_*` resolved to cell `delaunay` and clobbered the Delaunay A100 JSON; fixed with an explicit `cell=` kwarg.
- The vmap probe's batch-1 extrapolation recommends 64 replicas for the DelaunayNN runtime cell, which passes the memory budget but fails cuFFT batched-plan creation; the submit skips the probe and the VMAP_BATCH table (16) applies. Dense-path vmap 64 OOMs at a 46.9 GiB allocation.
- **PyAutoNerves `--xla_gpu_autotune_level=0` default (e8d5842, 2026-07-17) makes the fp64 curvature GEMM 5.2x slower on the A100** (25.6 -> 4.9 ms with autotune 4; total 117 -> 101 ms; runtime vmap/16 82 -> 63 ms; compile +1.4 to +9 s). Every A100 row since mid-July carries it. Filed: `draft/bug/autonerves/xla_gpu_autotune_level_0_default_slows_fp64_gemm.md`.
- euclid-ral-gpu-1 MIG fault is gone (all four GPUs Disabled, JAX cuda init OK per GPU, 2026-09-05); the four task submits drop the exclusion and ran on both nodes. Fleet-wide retirement: `draft/maintenance/autolens_profiling/retire_gpu1_mig_exclusion.md`.
- RAL `/home` quota: JAX persistent compile cache under `~/.cache/pyauto_jax/` hit ENOSPC (warnings only).

Follow-ups filed:
- `draft/feature/autoarray/delaunay_walk_early_exit_unchunked.md` (point-location walk: early exit, unchunked, static image-plane seed).
- `draft/bug/autonerves/xla_gpu_autotune_level_0_default_slows_fp64_gemm.md`.
- `draft/maintenance/autolens_profiling/retire_gpu1_mig_exclusion.md`.
- Not filed: an A100 Delaunay runtime row (only local CPU rows exist) as the companion to the DelaunayNN runtime cell.

## Original prompt

# DelaunayNN likelihood breakdown on the A100, like-for-like with `delaunay.py`, plus the H-row artifact fix

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- jax-gpu
- delaunay
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: results/breakdown/imaging/delaunay_nn_hpc_a100_fp64.json and a refreshed delaunay_hpc_a100_fp64.json exist with a real in-JIT H row, a four-way setup split, and per-step vmap-batch timings; results/notes/delaunay_nn_breakdown.md tabulates the two side by side
Review-minutes: 15
Unattended: ready
Filed: 2026-09-05
Issued: 2026-09-05

The Delaunay imaging likelihood breakdown (`scripts/imaging/likelihood_breakdown/delaunay.py`)
has no DelaunayNN (Sibson natural-neighbour) sibling. The only DelaunayNN timings are the
mapper-only geometry benchmark (`results/delaunay_nn/`, 157 ms cap-32 vs 37 ms Delaunay on the
A100, unbatched, query chunk 256) and whole-likelihood Nautilus per-eval numbers (61 ms for
both meshes under vmap), which cannot be reconciled without a per-step breakdown that runs
both unbatched and under a vmap batch. The Delaunay breakdown also reports its
"Regularization matrix (H)" row as an eager `jnp.array(numpy_matrix)` host-to-device copy
(delaunay.py:838-842), not a JIT step, so the 14.4 ms A100 figure is a PCIe artifact.

Original request (verbatim):

> yes do all that now, a like with like comparison with delaunay.py is good, and rerun
> delaunay.py if you need to (E.g. to fix artifacts) you should have RAL + A100s

Where "all that" is the preceding proposal: add a `delaunay_nn.py` breakdown sibling with the
existing split-setup prefix decomposition carried over and the mesh class swapped, and run it
under both the unbatched single-JIT path and a vmap batch so the chunk-loop amortization is
visible rather than inferred.

Deliverables:
1. `delaunay.py` breakdown: replace the eager H row with a JIT-profiled prefix (params -> H)
   attributed by difference against the interpolator prefix; add `--vmap-batch N` that
   re-times the combined setup block and every `--split-setup` prefix under
   `jax.jit(jax.vmap(...))` and reports per-call amortized ms.
2. New `scripts/imaging/likelihood_breakdown/delaunay_nn.py`: identical configuration
   (HST, 1500-vertex Hilbert, MGE-60 lens, ConstantSplit, border relocator) with
   `al.mesh.DelaunayNN(pixels=1500, areas_factor=0.5, zeroed_pixels=0)` and its interpolator,
   its own pinned eager log-evidence, same JSON/PNG contract.
3. New `scripts/imaging/likelihood_runtime/delaunay_nn.py` mirroring the Delaunay runtime
   cell (single JIT, vmap probe, vmap batch) so the whole-likelihood numbers are also
   like-for-like.
4. A100 submits under `hpc/batch_gpu/` for the three runs; results JSON/PNG committed;
   `results/notes/delaunay_nn_breakdown.md` with the side-by-side table and the corrected
   H attribution; README dashboard regenerated if it lists breakdown rows.

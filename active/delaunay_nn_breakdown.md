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

# Point-source image-plane chi-squared on the A100: likelihood breakdown, bottleneck map, speed-up levers

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- point-source
- profiling
- jax-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 30
Unattended: ready
Filed: 2026-09-17

# Point-source image-plane chi-squared on the A100: likelihood breakdown, bottleneck map, speed-up levers

User request (verbatim, 2026-09-17): "In autolens_profiling, we have done lots of work
speeding up imaging and interferometer on CCD. Now, I want us to speed up the point_source
image plane chi-squared, with this issue focusing on JAX GPU Speed up, mostly using the A100s
on RAL to perform the profiling. Follow the same strurture as imaging and interferomerter,
produce the likelihood breakdown (which likely will ned to be made for the steps of the point
solver? I'm not sure if we ever made one) and focus on bottlenecks and so on."

Survey (2026-09-17):

- `point_source/` has a `likelihood_runtime/` tier (image_plane, image_plane_solved,
  source_plane, source_plane_solved) but **no `likelihood_breakdown/` tier** and **no A100
  row** — the only numbers are local CPU (image_plane_solved: 39 ms/JIT call, 28 ms under
  vmap, v2026.7.23.1). `cluster/likelihood_breakdown/image_plane.py` is the closest
  precedent but times `solver.solve` as one block; nobody has ever opened the solver loop.
- The JAX solve is `AbstractSolver.steps()`: `n_steps = ceil(log2(scale/precision))` (=8 for
  the 0.2"/0.001" cell) unrolled iterations of ray-trace → `containing_indices` (padded to
  `MAX_CONTAINING_SIZE=15`) → `for_indexes` → `neighborhood()`^degree → `up_sample()`, each
  of the last three calling `remove_duplicates` = `jnp.sort` + `jnp.unique(size=…)`, then
  `_filter_low_magnification`, then the all-pairs permutation log-sum-exp chi-squared,
  wrapped in the padded `custom_jvp` solve (`implicit_diff.py`).
- Hypotheses to test on the A100: (a) the call is launch-latency / host-sync bound (tens of
  tiny sort/unique/gather kernels per step, ~8 steps) rather than FLOP bound, so vmap over
  likelihood evaluations is the first-order lever; (b) sort-based `unique` dominates device
  time; (c) 8× unrolled steps inflate compile time; (d) the implicit-diff gradient leg
  (vmap'd Jacobian) is a separate cost centre for gradient searches.

Deliverable: a `point_source/likelihood_breakdown/image_plane.py` cell that opens the solver
loop (per-step rows + chi-squared row, prefix-walk by successive differences per the imaging
harness), A100 fp64 + mp rows and a local-CPU row in `results/breakdown/point_source/`, a
fused-program device-timeline trace leg (fixed_light_trace.py precedent) attributing GPU
kernels to library source lines, vmap-batch scaling on the A100, a compile-time row, a
gradient leg, README dashboard regen, and a `results/notes/point_source_gpu_breakdown_2026_09.md`
verdict ranking the levers with measured evidence. Library levers (PyAutoArray triangles /
PyAutoLens solver) are filed from the verdict as follow-up prompts, library-first.

Related: `draft/research/autolens_profiling/point_solver_profiling_cells.md` (cluster arc
phase 2 — more point-source cells, not a GPU campaign; do not merge scopes).

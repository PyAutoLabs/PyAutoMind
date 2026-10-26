# Profile rectangular imaging at 28² (the production preset) so inference rows link like-for-like

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Epic: likelihood-lifecycle
Status: formalised
Consequence: judge
Witness: every rectangular imaging setup that has an inference wall-time record (hst; numba_cpu_sparse, jax_cpu_sparse, jax_cpu_dense, jax_gpu_sparse, jax_gpu_dense on their host classes; default + light_fixed variants where inference ran) has a current 28x28 runtime row on pin 2026.10.25.1, and the autolens_inference exporter's size_match is true for those rows
Filed: 2026-10-26

## Request
HUMAN 2026-10-26, choosing "Profile 28² too": the SLaM inference runs use the rectangular production preset 28x28
(784 px, `mesh_shape`) while the profiling standard size is 35x35 (1225 px, human size rule 2026-10-23), so the
inference table's "Profiling runtime" link compares different likelihood sizes (autolens_inference#47:
size_match false on every rectangular match). Add 28² rectangular runtime rows (a size variant beside the
standard, not replacing it — the 35² standard stays the coverage cell) for the setups/instruments that have
inference records, measured on RAL at pin 2026.10.25.1 (private checkout /mnt/ral/jnightin/profiling/PyAuto_2026.10.25.1),
and make the exporter prefer the exact-size current record (#47 already tie-breaks on size_match).
Delaunay needs nothing: runs use 1250 = profiling standard.

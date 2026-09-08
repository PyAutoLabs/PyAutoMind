# Rerun the hpc_a100_fp64 Delaunay/DelaunayNN breakdown + runtime rows under the fixed XLA default

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax-gpu
- performance
- hpc
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: a fresh-cache A100 Delaunay breakdown JSON with "Curvature matrix (F)" under 6 ms and `--xla_gpu_enable_triton_gemm=false` in `device.xla_flags`, plus regenerated dashboard rows for the four cells dated after the Nerves merge
Review-minutes: 10
Unattended: ready
Parent: complete/2026/09/xla-triton-gemm-off.md
Filed: 2026-09-08

Depends on: PyAutoNerves PR #162 (https://github.com/PyAutoLabs/PyAutoNerves/pull/162)
merged and synced to the RAL install via `HPCPullPyAuto`; autolens_profiling PR #230
merged.

Every `hpc_a100_fp64` dashboard row recorded between 2026-07-17 (PyAutoNerves e8d5842
shipped `--xla_gpu_autotune_level=0`) and 2026-09-08 was measured on an un-autotuned
Triton fp64 GEMM unless the node's per-fusion autotune cache happened to be seeded by a
level-4 run (see `results/notes/xla_autotune_triton_gemm.md`, job 342333: Curvature
matrix F 25.5 ms vs 4.8 ms). PyAutoNerves#161 fixes the default by adding
`--xla_gpu_enable_triton_gemm=false`.

After that lands on RAL, rerun with the library defaults and a FRESH
`JAX_COMPILATION_CACHE_DIR` (pass it via `sbatch
--export=ALL,JAX_COMPILATION_CACHE_DIR=<empty dir>` from `hpc/batch_gpu`; the wrapper
respects a preset):

- `submit_breakdown_imaging_delaunay_a100_hst_fp64` (with `--split-setup --vmap-batch 16`)
- the DelaunayNN breakdown sibling
- the `likelihood_runtime/imaging/delaunay` and `delaunay_nn` cells

so the dashboard does not straddle the flag change.

The first breakdown run doubles as the witness for #161: "Curvature matrix (F)" under
6 ms, `curvature_matrix_jit_compile` under 0.2 s, and `device.xla_flags` containing
`--xla_gpu_enable_triton_gemm=false`.

Witness already run and PASSED on 2026-09-08 (RAL job 342339, euclid-ral-gpu-2,
PyAutoNerves 0e7163b, autolens_profiling c7c07ae, fresh cache
`scratch_xla_autotune/cache_witness_20260908_1509`): Curvature matrix (F) 4.764 ms,
`curvature_matrix_jit_compile` 0.0566 s, `device.xla_flags` carries
`--xla_gpu_enable_triton_gemm=false`, 0 per-fusion autotune entries. That run's JSON is
the witness-quality `hpc_a100_fp64` Delaunay breakdown row; it lives in the RAL worktree
`/mnt/ral/jnightin/autolens_profiling_wt/xla-triton-gemm-witness`
(results/breakdown/imaging/delaunay_hpc_a100_fp64.json) and has not been committed.
Remaining scope: pull that row in, rerun the DelaunayNN breakdown and the two runtime
cells on a fresh cache, regenerate the dashboard, and update
`results/notes/delaunay_nn_breakdown.md`.

Reference rows: the `_autotune4` rows from PR #221 and the post-09-05 gpu-2 rows. Update
`results/notes/delaunay_nn_breakdown.md` and the dashboard; do not touch the `_autotune4`
rows.

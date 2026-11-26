# Place or retire the autolens_inference runs left behind by the mirrored-layout move

Type: maintenance
Target: autolens_inference
Repos:
- autolens_inference
Difficulty: easy
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Filed: 2026-11-26

## Finding

The canonical `autolens_inference` checkout held untracked results under the pre-2026-10-21 layout (`results/searches/`, `results/slam/`, `results/archive/`). The mirrored scripts/results move (a34e31f, `git mv`) never picked them up. A Heart health session pushed them as autolens_inference#77, then removed them again from that PR because `test_results_mirror_scripts` rejects those folders. #77 now ships only the simulator summaries.

Of the 88 removed files, 53 are byte-identical to files already tracked (new layout or `archive/2026/10/...`) and need no action. Two groups are still unplaced:

1. **12 search experiments**: `results/searches/experiments/cs1017_hpc_a100_jax_gpu_dense_fp64_slam_base{,_light_fixed}_{emcee,nautilus}_s{0,1,2}_a2.json`. Nothing named `cs1017` exists on main.
2. **23 SLaM stage files that differ from the tracked copies**: `results/slam/imaging/hst/{slam_delaunay,slam_delaunay_light_fixed}/hpc_{a100_jax_gpu_dense,a100_jax_gpu_sparse,ral_numba_cpu_sparse}_fp64/stages_seed{0,1}.{json,png}`, plus `slam_base{,_light_fixed}/hpc_a100_jax_cpu_sparse_fp64/stages_seed0.*`. Tracked files with the same names sit under `archive/2026/09/2026-09-24_pre_likelihood_speedup/`, so these may be later reruns or superseded runs.

## Where the files are

- Git: autolens_inference branch `results/commit-uncommitted-2026-11`, commit `9c97b2f` (the removal is `3ebb315`). Use `git show 9c97b2f:<path>`.
- Tarball: `C:\Users\Jammy\Workspace\Science\scratch\heart_canonical_dirty_2026-11-26\autolens_inference_results_PR77.tgz`.

## Task

For each group, decide whether it is a current result, a superseded run or noise:
- Current results go into the mirrored layout, in the folder whose `scripts/` variant produced them, so `test_results_mirror_scripts` passes. Then run `build_readme.py` and `export_inference_summary.py` and commit their output.
- Superseded runs go into a dated `archive/` entry.
- Noise is dropped, with a line in the Cortex ledger if it was ever cited.

This needs a science judgement on which runs are authoritative, so do not move files automatically.

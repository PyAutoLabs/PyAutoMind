## a100-pixelized-baseline
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/241
- completed: 2026-09-10
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/242 (merge c8b6058)
- pending-release: none — workspace-category task, no library PR, so the `active.md` row carried no uncleared `pending-release:` line.
- summary: |
    The final fp64 A100 baseline of the pixelized imaging likelihood, taken after PyAutoNerves#162
    (`--xla_gpu_enable_triton_gemm=false`) and PyAutoArray #531/#533/#537, as the reference set the
    matrix-free CG + SLQ work will be judged against. Four commits on `feature/a100-pixelized-baseline`:
    2689329 (12 fresh-cache A100 submits + launcher on the worktree-safe template), 59c0f84
    (w-tilde-native sparse breakdown, rectangular `--split-setup`/`--vmap-batch` parity, compile and
    cache provenance in every JSON), 58aa7a1 (the 12-leg results), be94ccc (the note, the superseded
    recommendation #4, the `delaunay_nn_breakdown.md` pointer, regenerated READMEs). All 12 legs
    (jobs 342617-342628) ran on `euclid-ral-gpu-2` inside one 17-minute window, fp64, fresh per-job
    `JAX_COMPILATION_CACHE_DIR` with `AUTOTUNE_ENTRIES count=0` at exit, every pin PASSED.
- witness: |
    The prompt's Witness clause named {rectangular bilinear, Delaunay} x {dense, sparse} x
    {runtime, breakdown}; the task delivered that grid **plus DelaunayNN**, 12 legs rather than 8.
    Clause by clause:
    - *one results note carrying fresh-cache same-node A100 fp64 rows dated after PyAutoNerves#162
      with `--xla_gpu_enable_triton_gemm=false` in `device.xla_flags`* — MET.
      `results/notes/a100_pixelized_baseline_2026_09.md`; all 12 jobs on one node
      (euclid-ral-gpu-2), each with `cache_fresh: true`, `autotune_cache_entries_at_start: 0`, and
      the Triton-off flag in `device.xla_flags`.
    - *"Curvature matrix (F)" under 6 ms on every dense row* — MET: 4.826 / 4.824 / 4.830 ms on
      rectangular / Delaunay / DelaunayNN.
    - *the sparse breakdown rows built from the w-tilde operator (no mapping matrix step)* — MET:
      `likelihood_breakdown/{pixelization,delaunay,delaunay_nn}.py` now time the w-tilde preload and
      mapper under `--sparse`, with F from the sparse operator and D from the w-tilde data term;
      sparse F/D checked against `fit.inversion` to 1e-8 on all three meshes (jobs 342626-342628).
    - *per-call-at-vmap-16 numbers for both meshes* — MET, for all three: dense/sparse ms per call
      rectangular 32.1/36.7, Delaunay 42.5/48.0, DelaunayNN 46.4/49.3.
    - *the dashboard regenerated* — MET: `build_readme.py` regenerated `README.md` and
      `scripts/misc/likelihood_breakdown/README.md` in be94ccc.
    - *`sparse_vs_dense_inversion_path.md` status and recommendation #4 updated* — MET: status line
      refreshed and recommendation #4 marked superseded, pointing at the new note.
- findings: |
    - **Dense F holds at ~4.83 ms on every mesh**, confirming the PyAutoNerves#162 cuBLASLt lowering
      carries to the pixelized cells, not just the Delaunay witness that motivated it.
    - **The w-tilde F is 17.9-20.4 ms**, replacing the dense blurred-mapping-matrix + F chain
      (9.3-13.2 ms). Sparse therefore costs **+6-14 % per call at vmap 16** while using ~7x less
      device memory, with ~12x cheaper batched inversion setup on the rectangular cell (0.75 ms vs
      9.11 ms per call). Sparse remains the memory lever, never the speed lever.
    - **The solve is the target, not the matrix.** Regularized reconstruction (NNLS + Cholesky) is
      ~37 ms — **61-71 % of the per-call cost on every row**, and identical dense vs sparse. A
      matrix-free formulation that only replaces F is attacking the wrong 10 ms.
    - DelaunayNN's `sparse_nnz` is 491,552 against 46-61k for the other two meshes.
    - This is the **fiducial tier** (1500 Delaunay vertices / 1521 rectangular pixels), not the #235
      production preset; decision 3 there stays open and the two must not be mixed.
- follow-ups: |
    Not filed as prompts here — a later `/intake` owns them:
    1. No cell emits the Cholesky log-det terms, which an SLQ-vs-exact comparison needs.
    2. The rectangular **runtime** cell still pins pre-#235 `28622.397322591198` while measuring
       `28621.128714…` (passes at 4.4e-5) — re-measure the pin. Bookkeeping, not a gate failure.
    3. Split the ~37 ms reconstruction row into NNLS iterations vs Cholesky before sizing
       matrix-free CG.
    4. File the matrix-free CG + SLQ PyAutoArray prompt itself, against this note.
- trap: |
    The RAL bridge is pull-only: commit inside the RAL worktree, fetch it over ssh from the laptop,
    push from local. There is no push path from RAL to origin.
- heart: |
    Shipped under an acknowledged YELLOW (2026-09-10, in-session): "workspace validation not passing
    (5 failed, 2 timeout, cloud#34099198772 …)" plus three "profiling drift: runtime/imaging/…" rows.
    All organism-scope; none touched by this branch. Not frozen at merge.

## Original prompt

# Final A100 fp64 baseline of the pixelized imaging likelihood (rectangular bilinear + Delaunay, dense + sparse) under the fixed XLA default

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- jax-gpu
- performance
- hpc
- pixelization
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: one results note carrying, for {rectangular bilinear, Delaunay} x {dense, sparse} x {runtime, breakdown}, fresh-cache same-node A100 fp64 rows dated after PyAutoNerves#162 with `--xla_gpu_enable_triton_gemm=false` in `device.xla_flags`, "Curvature matrix (F)" under 6 ms on every dense row, the sparse breakdown rows built from the w-tilde operator (no mapping matrix step), and per-call-at-vmap-16 numbers for both meshes; the dashboard regenerated; `sparse_vs_dense_inversion_path.md` status and recommendation #4 updated
Review-minutes: 20
Unattended: ready
Supersedes: draft/research/autolens_profiling/rerun_a100_fp64_delaunay_rows_fixed_xla_default.md
Parent: complete/2026/09/xla-triton-gemm-off.md
Filed: 2026-09-10
Issued: 2026-09-10
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/241

## Original request (verbatim)

> We recently sped up the curvature matrix by changing a JAX environemtn variable. I think we
> will need to do this matrix free task, in fact I am sure we will, but first can we do a final
> A100 profilng of the likelihood function for the bilinear rectangular mesh and the delaunay
> mesh, with this enviroment variable issue now fixed (And other speed ups to delaunay recently
> implemented). Do this on the sparse path too, and do this in autolens_profiling. We are
> basically getting the exact numbers we need to then compare against the matrix free approach.

## Context

- The "environment variable" is PyAutoNerves#162 (merged 2026-09-08, on RAL at 0e7163b):
  `jax_wrapper` now appends `--xla_gpu_enable_triton_gemm=false` to the level-0 default, so
  the fp64 curvature GEMM reaches cuBLASLt (4.8 ms) instead of an un-tuned Triton fusion
  (25.5 ms). See `results/notes/xla_autotune_triton_gemm.md`.
- Recent Delaunay speed-ups, all merged to PyAutoArray main and present on RAL (35aa681f):
  walk early exit #531, Sibson launch latency #533, ConstantSplit assembly compaction #537;
  profiling-side AdaptSplit(0.1, 10, 0.1) re-basing autolens_profiling#232.
- The matrix-free line (CG solve + stochastic Lanczos quadrature for the two log-det terms) was
  deferred on 2026-06-07 in `results/notes/sparse_vs_dense_inversion_path.md` recommendation
  #4 because sparse won on memory with exact Cholesky log-det. This baseline is the reference
  set that a matrix-free prototype will be judged against, so it must be same-node,
  fresh-cache, and honest about which steps each path actually performs.

## What is stale or missing today (survey 2026-09-10)

1. Every rectangular (`pixelization`) A100 row — breakdown fp64/mp, dense and sparse — is from
   2026-07-11 at PyAutoLens 2026.7.6.649 with no Triton flag, pre bilinear/RTU mesh split,
   pre lp [4,2,2], pre re-pin. There is no committed rectangular A100 runtime JSON at all; only
   June SLURM stdout in `results/runtime/imaging/a100_logs/`.
2. `delaunay_hpc_a100_fp64_sparse.json` is 2026-07-11, ConstantSplit, no Triton flag. No
   sparse runtime JSON exists for any cell. No DelaunayNN sparse row or submit exists.
3. The `_sparse` breakdown rows are dense per-step tables with a sparse dataset attached:
   `likelihood_breakdown/{pixelization,delaunay,delaunay_nn}.py` hard-code
   `curvature_matrix_via_mapping_matrix_from` and a dense mapping-matrix setup regardless of
   `--sparse` (dense vs sparse rows agree to <1 % step-for-step). For a matrix-free comparison
   the sparse breakdown must time the w-tilde path: no mapping matrix, F and D from the sparse
   operator.
4. `likelihood_breakdown/pixelization.py` has no `--split-setup` / `--vmap-batch`, so the
   rectangular baseline has no "Mapping matrix" row and no per-call-at-vmap-16 number to set
   beside the Delaunay rows.
5. Compile time (`full_pipeline_compile`, `<step>_jit_compile`) exists only in gitignored SLURM
   stdout; no submit sets `JAX_COMPILATION_CACHE_DIR`, so a seeded node silently inherits the
   cuBLAS choice (the F value is the only tell).
6. The pixelization and every `_sparse` submit are the old template: hard-coded
   `AP_ROOT=/mnt/ral/jnightin/autolens_profiling`, `--exclude=euclid-ral-gpu-1`, buffered
   python, no revision echo. PR autolens_profiling#222 (merged 2026-09-10, d3933536) rewrote these same
   files to drop the gpu-1 exclusion and the `_gpu_preflight.sh` backstop, so a branch from
   current `main` already has them clean.

## Scope

Grid: {rectangular bilinear 39x39, Delaunay Hilbert-1500 AdaptSplit, DelaunayNN} x {dense,
sparse} x {likelihood_runtime, likelihood_breakdown} on `hpc_a100_fp64`, HST fiducial preset
(15361 masked pixels, MGE-60 lens light, lp [4,2,2], pixelization over-sampling 1) — 12 legs,
one node, fresh compilation cache per leg (decided 2026-09-10: DelaunayNN in, w-tilde-native
breakdown in; autolens_profiling#222 merged 2026-09-10, so branch from current `main`).

This is the **fiducial-tier** baseline (1500/1521 source pixels), not the production
Euclid/subhalo preset (profiling #235 decision 3 remains open); label it as such so the
matrix-free comparison is like-for-like with every existing A100 pin.

## Deliverables

1. Sparse-native breakdown path in the three breakdown cells: under `--sparse`, the setup
   block times the w-tilde preload and mapper (no blurred mapping matrix), step 10 times F via
   the sparse operator (`curvature_matrix_via_w_tilde…` / the `InversionImagingSparse`
   route), D via the w-tilde data term, then H, F+λH, Cholesky/NNLS reconstruction, model
   image (matrix-free), chi-squared, both log-det terms. The dense path is untouched. Pins
   must match the dense pins (log_L bit-identical to 12 sig figs per the June sweep).
2. `--split-setup` and `--vmap-batch` on `likelihood_breakdown/pixelization.py`, mirroring
   `delaunay.py`.
3. Compile time (`full_pipeline_compile`, per-step `_jit_compile`), `xla_flags`, the
   `JAX_COMPILATION_CACHE_DIR` used and whether it was fresh, written into every JSON.
4. Submits regenerated on the worktree-safe template (derived `AP_ROOT`, `python3 -u`,
   revision echo, no gpu-1 exclude), each exporting a fresh per-job
   `JAX_COMPILATION_CACHE_DIR`; new `submit_{breakdown,runtime}_imaging_delaunay_nn_a100_hst_fp64_sparse`.
   Branch from current `main` (#222 merged 2026-09-10).
5. One same-node A100 window running all legs (breakdown with `--split-setup --vmap-batch 16`,
   runtime plain so the vmap phase is measured — `--vmap-probe` exits before it); results
   JSONs committed from the RAL worktree.
6. New note `results/notes/a100_pixelized_baseline_2026_09.md`: the per-step tables for all
   rows, unbatched and per-call at vmap 16, with the two columns a matrix-free prototype must
   beat called out explicitly (dense: mapping matrix + F + Cholesky/NNLS reconstruction;
   sparse: w-tilde F + reconstruction) and the exact log-det values each row reports.
   Update `sparse_vs_dense_inversion_path.md` (status line, A100 table, recommendation #4 →
   "superseded, see baseline note") and `delaunay_nn_breakdown.md`; regenerate the dashboard
   (`build_readme.py`); fold in the witness row from the RAL worktree
   `autolens_profiling_wt/xla-triton-gemm-witness` if it still differs from the canonical row.

## Out of scope

- The matrix-free implementation itself (separate PyAutoArray prompt, to be filed against
  this baseline).
- Closing #235 decision 3 (GPU production-representative preset).
- Rewiring `aggregate.py` so A100 runtime rows appear in the README headline runtime table
  (file as a follow-up if it is more than a few lines).
- Mixed-precision rows.

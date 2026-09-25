# Interferometer likelihood campaign 2/3: Delaunay-1500 and rectangular mesh breakdown on JAX A100 (sparse operator), optimisation task list

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- interferometer
- pixelization
- likelihood-profiling
- jax-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Witness: `results/breakdown/interferometer/delaunay_hpc_a100_fp64.json` steps sum to within 10 % of the full-JIT runtime cell at alma, and step names are the sparse-path steps (no `transformed_mapping_matrix` row in the sparse arm).
Review-minutes: 8
Unattended: ready
Lane: local-dev
Epic: interferometer-likelihood-campaign
Filed: 2026-09-25

Mirror of the imaging A100 pixelized baseline (#241 / PR #242: Delaunay 67.5 ms,
rectangular 60 ms) for the interferometer sparse-operator (W~) likelihood on the RAL A100.
No JAX-GPU interferometer breakdown has ever been committed; the two
`submit_breakdown_interferometer_delaunay_a100_alma_high_{fp64,mp}` SLURM scripts have no
output, and the only A100 interferometer rows are v2026.5.14.2 Hilbert-1000 runtime
numbers in `autolens_workspace_developer/jax_profiling/results/jit/interferometer/`.

## Step 0 — make the JAX breakdown time the path the library runs

Supersedes `draft/bug/autolens_profiling/interferometer_delaunay_breakdown_oom_sma.md`
(fold it in, retire the draft on filing).

- `scripts/interferometer/likelihood_breakdown/delaunay.py` calls
  `apply_sparse_operator` (:216-221) but then times **dense-path** steps: the transformed
  mapping matrix (:522-536) and F from the real/imag transformed matrices (:632-700).
  Rewrite steps 8-10 to time `InversionInterferometerSparse`'s actual per-evaluation
  work: sparse triplets, `D = L^T d~`, blocked-rfft2 `curvature_matrix_diag_from`
  (`inversion_interferometer_util.py:1099-1253`, `batch_size` default 128), regularisation,
  PDIP / certified solve, log-dets, `fast_chi_squared`. Keep one dense-path arm
  (`InversionInterferometerMapping`) for the comparison rows.
- The script is OOM-killed on sma at 14.6 GB RSS during PART B (`jit_profile` keeps
  compiled artefacts alive; free between sections, `jax.clear_caches()`), and needs
  `--skip-part-b`. Acceptance: completes on sma under ~4 GB.
- Add `scripts/interferometer/likelihood_breakdown/pixelization.py` (rectangular, JAX);
  only numba variants exist today.

## Setups (align to the imaging campaign for comparability)

- Delaunay: Hilbert 1500, `AdaptSplit(inner=0.1, outer=10, signal_scale=0.1)` as
  imaging since #232 (the interferometer cells still use `ConstantSplit(1.0)`); record
  the ConstantSplit row once as the bridge to the v2026.5 numbers.
- Rectangular: 39x39 = 1521 pixels via `rect_mesh_classes`, `al.reg.Constant(1.0)`
  (interferometer cells use 32x32 = 1024 today).
- Mass fixed at truth, no lens light (interferometer datasets carry none; state it).
- Instruments: sma, alma, alma_high, jvla; `TransformerNUFFT` with the preset chunk size;
  sparse operator built with `method="nufft"` (7.3 s at alma).
- fp64 everywhere, mp arm on the A100 (May: mp only helped at jvla).
- Use `--source-pixels` for an N sweep (1000/1500/2500/4000) as in the imaging
  fixed-light campaign, so the affordable-N verdict has an interferometer counterpart.

## Then: optimisation task list

Note `results/notes/interferometer_mesh_a100_breakdown_2026_09.md`, ranked levers with
step, bound and predicted gain; file each worthwhile one as its own prompt. Evaluate:

1. `curvature_matrix_diag_from` block size and the `lax.fori_loop` over S/B blocks on
   the GPU (M = 4*y*x of the mask extent, so the FFT cost is N_vis-independent; the
   question is whether the A100 is FFT-bound, scatter-bound or launch-bound).
2. Solver share: imaging found NNLS 60-85 % of the call and the certified active-set
   solve halved the A100 time (#259). Measure PDIP vs certified on the interferometer
   F (denser than the imaging F?) at N = 1500 and 4000.
3. Off-diagonal / func-list blocks are mirrored and assembled in `sparse.py:267-400`;
   check for redundant transposes or double FFTs.
4. `preloads.curvature_matrix` is honoured by the sparse path but not the dense one;
   whether a fixed-mass datacube-style preload applies.
5. Mixed precision: `use_mixed_precision` is not honoured by the transformers or the
   FFT apply; whether an fp32 rfft2 arm holds the 0.5-nat log-evidence bar.

## Done when

- Committed `results/breakdown/interferometer/{delaunay,pixelization}_hpc_a100_fp64[_mp].json`
  at sma/alma/alma_high/jvla with non-null `steps`, plus the local-CPU JAX
  `delaunay_breakdown_sma` JSON+PNG the OOM draft asked for; README dashboards
  regenerated, lint green.
- The `submit_breakdown_interferometer_*` SLURM scripts cover both meshes and all
  instruments.
- The note ranks the levers and gives the per-instrument A100 baseline table
  (the interferometer analogue of #241's 67.5 / 60 ms).
- Its N-sweep rows are the GPU half of the epic's decision matrix (task 3/3 owns the
  matrix itself).

Consequence: glance
Witness: `results/breakdown/interferometer/delaunay_hpc_a100_fp64.json` steps sum to within 10 % of the full-JIT runtime cell at alma, and step names are the sparse-path steps (no `transformed_mapping_matrix` row in the sparse arm).
Review-minutes: 8

<!-- formalised by the Intake (Conception) Agent on 2026-09-25 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/ab334050-3e04-48cf-8914-a1e38ba0a9e5/scratchpad/prompts/interferometer_mesh_breakdown_jax_a100.md -->

- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/575 (closed completed 2026-09-26)
- completed: 2026-09-26
- library-pr: PyAutoArray https://github.com/PyAutoLabs/PyAutoArray/pull/576 (head `b5ef2e89`, merged 2026-09-26T15:33:44Z)
- library-pr: PyAutoGalaxy https://github.com/PyAutoLabs/PyAutoGalaxy/pull/629 (head `36d1b436`, merged 2026-09-26T15:33:48Z)
- library-pr: PyAutoLens https://github.com/PyAutoLabs/PyAutoLens/pull/750 (head `ac333b17`, merged 2026-09-26T15:33:51Z)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/313 (head `fbfb2210`, merged 2026-09-26T15:33:55Z)
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/576
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/629
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/750
- pending-release: autolens_profiling@https://github.com/PyAutoLabs/autolens_profiling/pull/313
- merge-order: library-first — PyAutoArray#576 → PyAutoGalaxy#629 → PyAutoLens#750 → autolens_profiling#313, all by the human's /prm on 2026-09-26.
- heart-red-override: "2026-09-26 live user chose 'Override, open PRs' for this task (commit/push/pending-release PR only; merge via /prm on green checks; no release). RED reasons: release validation FAILED (stage integrate); workspace validation not passing (4 failed, cloud#35579888156); manifest drift hub organism blurb 7; manifest drift organism-map blocks 1. Gates passed: unit 1706/1240/757+1xf, smoke 24/24."
- heart-at-workspace-ship: "2026-09-26 YELLOW (manifest drift hub blurb 7; organism-map blocks 1); human authorized shipping the workspace PR"

- summary: MGE-only interferometer inversions now take the W~ sparse operator when `apply_sparse_operator()` is applied (the factory guard is removed). The sparse data vector takes `DatasetInterface.sparse_dirty_image`; galaxy and lens fits with ordinary light profiles pass d~ − W~ i_p. This fixed a silent bug: the unsubtracted dirty image gave a 23% wrong D at sma (logL −26.77 vs −24.34 dense). `profile_visibilities` skips the zero-image NUFFT when no ordinary light is present. Incidental: `TransformerDFT.image_from` now honours `xp`.
- results: A100 full library pipeline alma 2.69 ms, jvla 16.7 ms, where the dense library path OOMs (chunked dense 940 ms / 24.2 s). CPU alma 34.7 ms vs 13.1 s dense. |ΔlogL| = 0.0 wherever dense runs; MGE + lens Sersic matches exactly.
- gotcha: the root `activate.sh` was rewritten mid-task by another session; worked around with a private env file.
- gotcha: the adjoint-NUFFT dirty-image route was ~4 s at alma; replaced by W~·i_p at 2 ms.
- gotcha: a stale `autolens_workspace_test` `dataset/interferometer/simple` faked a smoke failure.
- limit: CPU alma_high ran out of memory in the `apply_sparse_operator` build (10.8 GB).
- limit: jvla vmap64 still OOMs (41 GiB; likely the W~ curvature FFT — inferred, not measured).
- note: a Heart freeze delayed the merge.
- follow-ups (still-open epic drafts): `interferometer_chunked_transform_mapping_matrix`, `interferometer_transform_mapping_matrix_real_scatter`, `ral_venv_dependency_floor_drift`. The docs draft `workspace_interferometer_mge_sparse_operator_memory_docs` was retired at close-out (its premise is falsified by this merge; record `complete/2026/09/workspace-interferometer-mge-sparse-operator-memory-docs.md`); the chunked-transform draft's wording was updated to say lever 1 shipped.
- ral-leftovers (not touched at close-out): `/mnt/ral/jnightin/PyAuto_branch/interferometer-mge-w-tilde-route/`; `/mnt/ral/jnightin/autolens_profiling_wt/interferometer-mge-w-tilde-route` (+ the `feature/interferometer-mge-w-tilde-route` branch in the RAL autolens_profiling checkout).
- worktree: `~/Code/PyAutoLabs-wt/interferometer-mge-w-tilde-route` removed at close-out.

## Original prompt

# Interferometer likelihood campaign: route MGE-only interferometer fits through the W~ sparse operator

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_profiling
Themes:
- interferometer
- mge
- sparse-operator
- jax-gpu
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Consequence: glance
Witness: with `apply_sparse_operator()` applied, an MGE-only `FitInterferometer` on the alma dataset takes the func-list W~ path (inversion class is the sparse/W~ interferometer inversion, not `InversionInterferometerMapping`), its `log_likelihood` matches the dense path within 1e-6 nats, and `jax.jit(FitInterferometer)` no longer OOMs the A100 at alma/alma_high/jvla.
Review-minutes: 10
Epic: interferometer-likelihood-campaign
Issued: 2026-09-26

Source: `autolens_profiling/results/notes/interferometer_mge_breakdown_2026_09.md`, lever 1
(autolens_profiling#308).

## Why

`autoarray/inversion/inversion/factory.py:202-208` sets `use_sparse_operator = False` when
every linear object is an `AbstractLinearObjFuncList`, so an MGE-only interferometer fit
always pays the O(N_vis * n) dense NUFFT path even after `apply_sparse_operator()`. The
func-list W~ blocks already exist and are used by mixed mapper + MGE inversions
(`inversion_interferometer_util.py:1466` `operated_matrix_slim_from`, `:1628`
`curvature_matrix_func_list_from`).

Measured on the #308 breakdown cell's measurement-only W~ arm (fp64, nufftax 0.6.1):
dense chain from the mapping matrix vs W~ chain — A100 sma 855 ms -> 2.40 ms, alma 937 ms
-> 1.90 ms, alma_high 3.81 s -> 3.35 ms, jvla 23.62 s -> 13.53 ms; CPU alma 36.58 s ->
28.6 ms. F~ vs dense F agrees to <= 1.6e-11 rel; figure of merit to <= 7.1e-7 nats. The
library path cannot run above sma on the A100 at all (65.9 GB alma one-shot transform).

## What

- Let the factory keep the sparse operator on for func-list-only interferometer inversions
  when `dataset.sparse_operator` is set (imaging keeps today's behaviour unless measured).
- Data vector from the cached dirty image; the `fast_chi_squared` identity with per-dataset
  constants, so no transformed mapping matrix is formed.
- Check the mapped visibilities / residual map path (plots, `FitInterferometer` attributes
  that need `transformed_mapping_matrix`) stays correct — likely a lazy dense fallback.
- Re-run `scripts/interferometer/likelihood_breakdown/mge.py` (library path) CPU + A100 and
  update the VRAM table rows `("interferometer", "mge", alma+)` in
  `scripts/misc/vram/config.py`.

## Watch

- The one-off operator build (1.1-8.2 s A100, 18.5 s CPU alma) must be done once per
  dataset, not per likelihood.
- After this lands PDIP becomes the largest W~ step on the A100 (1.46 of 2.32 ms at alma).

<!-- filed from autolens_profiling#308 phase C (PR #312), 2026-09-26 -->

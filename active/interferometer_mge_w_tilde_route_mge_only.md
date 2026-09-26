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

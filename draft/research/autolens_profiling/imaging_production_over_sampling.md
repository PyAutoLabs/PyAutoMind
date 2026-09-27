# Profile imaging pixelizations at production over-sampling

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: an A100 row in `results/runtime/imaging/delaunay/` records `over_sample_size_pixelization_rule` = {source_snr_cut 3.0, sub_size_above 4, sub_size_below 2} on Euclid data (today every A100 row records None)
Review-minutes: 3
Unattended: ready

## Why

A Euclid session compared a 1.5 s cold likelihood evaluation from a real Euclid
fit against the autolens_profiling imaging headlines and found them not
comparable. On checking (2026-09-27):

- The JAX Delaunay runtime cell hard-codes `over_sample_size_pixelization=1`
  (`scripts/imaging/likelihood_runtime/delaunay.py:244`). The headline A100 row
  (`results/runtime/imaging/delaunay/delaunay_hpc_a100_fp64.json`, 65 ms per
  eval, AdaptSplit) records no pixelization over-sampling rule, uses HST data
  (0.05", 15 361 masked pixels) and the `[4, 2, 2]` light-profile bins.
- Euclid production (`EUCLID_VIS_PIX` in `_production_config.py`, vis_pix stage,
  job 342301) uses pixelization sub-size 4 above source S/N 3 and 2 below, with
  `[4, 4, 2]` light-profile bins. The HST subhalo preset (`hst_source_pix_2`)
  uses the same 4/2 pixelization rule.
- The fixed-lens-light numba result (932 → 459 ms, HST Delaunay N1500, job
  343311, `results/notes/fixed_lens_light_numba_2026_09.md`) was measured with
  the older cell settings (60×1 MGE, no pixelization over-sampling rule
  recorded). No fixed-light row exists at production settings.
- The only production-preset numba row
  (`results/runtime/imaging/delaunay_numba/delaunay_numba_likelihood_summary_hst_v2026.8.17.1.json`,
  linear 30×2 MGE, 4/2 over-sampling) reads 1.46 s cold / 1.97 s warm, and its
  witness against production job 342311 (0.52–0.81 s) is **FAIL**: about 2×
  slower than production for an unexplained reason.

The AdaptSplit vs ConstantSplit difference on the A100 is about 5 ms (65 vs 60
ms) and is not the gap.

## What

1. Make the JAX imaging pixelization cells (runtime + breakdown, Delaunay
   family, and rectangular where relevant) accept the production presets
   (`--instrument euclid|hst`) so pixelization over-sampling follows the 4/2
   S/N rule instead of a flat 1. Keep the legacy flat-1 setting selectable so
   the historic rows can still be reproduced.
2. Re-measure the A100 JAX headline at production over-sampling, on HST and on
   **Euclid data with the `EUCLID_VIS_PIX` preset**, so the headline matches
   what Euclid production runs.
3. Add a fixed-lens-light numba sparse row at production settings (HST, and
   Euclid if cheap), next to the linear-light production row, so both answers
   to "how long does HST take, light linear vs fixed?" are production-matched.
4. Investigate the `delaunay_numba` HST production-preset witness FAIL (cold
   1.46 s vs job 342311's 0.52–0.81 s): is it the cell, the host, or the
   reference?
5. Update `results/README.md` and the campaign status note so headline
   numbers state their over-sampling, preset and dataset, and older flat-1
   rows are labelled as such.

## Out of scope

Library changes to the over-sampling code itself; the fitting library's
summary-time evaluation timing (a separate question about the 1.5 s figure
being one cold call in the main process).

<!-- formalised by the Intake (Conception) Agent on 2026-09-27 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/44f36318-0f57-4a47-b6a1-c66501ff840f/scratchpad/profiling_production_over_sampling.md -->

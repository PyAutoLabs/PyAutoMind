# Streaming phase 3: visualizer on array-free datasets (natural-weighted dirty panels, uv panels skipped)

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
Themes:
- interferometer
- sparse-operator
- memory
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-09-30
Epic: streaming-visibilities
Phase: 3
Difficulty: medium
Consequence: glance
Witness: `visualize_before_fit` and `visualize` (ag + al interferometer visualizers) on an array-free fit write every png/fits without raising — uv/visibility panels skipped, dirty image / dirty beam / dirty model / dirty residual present from the terms and labelled "(natural weighting)" — while in-memory output is byte-unchanged; `inversion_plots._recon_array` no longer performs a forward transform to type-check.
Review-minutes: 6
Unattended: ready
Parent: draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md

Source: https://github.com/orgs/PyAutoLabs/discussions/13 phase 2, sliced 2026-09-30 (decision (c)). After this phase ships, post the promised follow-up on the discussion (see epics.md notes).

## What
1. `autoarray/dataset/plot/interferometer_plots.py`: guard uv/visibility/S-N panels on array presence (precedent: `fits_interferometer`
   `noise_map is not None` guards); dirty image / beam from `dirty_image_natural` / `dirty_beam` when arrays are absent.
2. `fit/plot/fit_interferometer_plots.py` (+ ag/al mirrors): dirty model = W~·image via `operated_matrix_slim_from`; dirty residual =
   d~ − W~·(M s + i_p); skip normalized-residual / chi-squared dirty panels and the uv subplots when arrays are absent.
3. `inversion/plot/inversion_plots.py` `_recon_array`: replace the forward-transform type probe.
4. ag/al visualizers: no crash paths; tests mirror `test_plotter_interferometer.py` with an array-free fixture.

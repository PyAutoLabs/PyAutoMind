## streaming-p3-visualizer
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/596
- completed: 2026-09-30
- epic: streaming-visibilities (phase 3 of 5)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/597
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/640
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/761
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/597
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/640
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/761

### What shipped
- **PyAutoArray#597** (merge c1d85810) — `aa.fit.fit_interferometer.dirty_model_image_natural_from(dataset, image)` (W̃·m/Σw, no transformer); array-free branches in `subplot_interferometer_dataset` / `subplot_interferometer_dirty_images` (1×2 natural dirty image / beam, same filenames), `fits_interferometer` (guards `data`, natural extensions), `subplot_fit_interferometer` / `subplot_fit_interferometer_dirty_images` (`model_image=None`); `inversion_plots._recon_array` reads `mapped_reconstructed_data_dict` for array-free interferometer inversions and both handlers catch `InversionException` (a live escape bug). `test_autoarray` 1898.
- **PyAutoGalaxy#640** (merge 6d522ce4) — `FitInterferometer.model_image_natural` (`profile_image + inversion.mapped_reconstructed_data`), `dirty_model_image_natural`, `dirty_residual_map_natural`; natural 1×3 in `subplot_fit`, `subplot_fit_dirty_images`, `subplot_fit_real_space`; `fits_dirty_images` writes `DIRTY_IMAGE_NATURAL` / `DIRTY_BEAM` / `DIRTY_MODEL_IMAGE_NATURAL` / `DIRTY_RESIDUAL_MAP_NATURAL`; visualizer `logger(...)` TypeError → `logger.warning`. `test_autogalaxy` 1293.
- **PyAutoLens#761** (merge a2fbe881) — same properties; array-free `subplot_fit` 2×3, `subplot_fit_dirty_images`, `subplot_fit_interferometer_combined`, `subplot_fit_real_space`, `subplot_tracer_from_fit`; positions image from `dirty_image_natural`; both visualizers' `logger(...)` fixed (imaging too, same defect); stale `dirty_images.fits` test assertion fixed and the dead tracked file removed. `test_autolens` 776 + 1 xfailed.
- In-memory output byte-unchanged (tested by value against `fit.dirty_*`). Witness: `visualize_before_fit` + `visualize` on a 1e5-visibility streamed dataset write the same 7 (ag) / 10 (al) files as in memory; W̃ path vs transformer path rel 3.4e-14 / 3.9e-14.

### Review and override
- Codex gpt-6-astra review: 1 finding — `model_image_natural` via `galaxy_image_dict` lost the ordinary light of a galaxy that also has a linear component (reproduced, rel error 1.0 / 1.14); fixed as `profile_image + mapped_reconstructed_data` with mixed-galaxy tests against an independent reference from `fit.model_data` (rel ≤ 2e-14), red-checked. Records on all three PRs.
- Third human-authorized Heart RED development override of the day (`release validation FAILED (stage integrate)` + other-session PyAutoLens checkout drift); recorded on the issue, PR bodies, `active.md`, `autonomy_log.md`. Merged Array → Galaxy → Lens on a separate human `/prm` with all legs green.

### Go/no-go evidence (why the epic continued)
- Benchmark on the epic ledger: in-memory `apply_sparse_operator` OOMs at 1e6 visibilities on a 16 GB laptop (3 kB/vis NUFFT temporaries); streaming 1.5–1.8 GB flat to 5e7 at ~11 s per 1e6 vis with chunk 65536 (5× faster than chunk 4096); 2e8 ≈ 37 min. Campaign prompt `draft/research/autolens_profiling/interferometer_streaming_scaling.md` filed to version it.

### Deferred
- Public switch to skip `visualize_before_fit` only (filed separately, PyAutoFit); non-linear light profiles on array-free datasets → phase 4; cubes / phase centre → phase 5; accumulator per-chunk JAX recompile → the profiling campaign.

### Notes
- A concurrent Codex session's Mind commit (89d44c97) deleted this task's `active.md` block; restored from 88f102d4 at ship.
- The promised follow-up on Discussion #13 is due now that fits, save/reload and visualization work end to end.

## Original prompt

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

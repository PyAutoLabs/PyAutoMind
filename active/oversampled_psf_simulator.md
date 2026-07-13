# Oversampled PSF support in SimulatorImaging + workspace simulator example

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoArray
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Follow-up to the oversampled PSF convolution series (design PyAutoArray#353;
phases 2a/2b/2c merged, phase 3 PRs PyAutoArray#358 + autolens_workspace_test#149).
Chosen as option (a) at the phase-3 sign-off (autolens_workspace#232,
2026-07-08): simulation with an oversampled PSF is not yet library-supported,
and the user-facing workspace simulator example should land together with that
support rather than via manual data assembly.

## Background

`SimulatorImaging.via_galaxies_from`
(`@PyAutoGalaxy/autogalaxy/imaging/simulator.py:22-77`) generates the
padded image via `galaxies.padded_image_2d_from(grid, psf_shape_2d=...)` —
evaluated **binned at image resolution** — and hands it to `via_image_from`
(the PyAutoArray simulator base), which convolves the padded native image
with the PSF kernel directly. The approved design (§5) deliberately kept
`padded_image_2d_from` at image resolution, so a `convolve_over_sample_size>1`
Convolver cannot be used to simulate: the kernel is at the fine pixel scale
while the padded image is at image resolution.

## Scope

1. **Fine-resolution simulation path.** When
   `psf.convolve_over_sample_size > 1`:
   - evaluate the padded image on the padded grid's over-sampled coordinates
     (the `Grid2DIrregular(grid.over_sampled)` pass-through pattern used
     throughout the series — no signature threading);
   - convolve at the fine resolution and bin to image resolution (reuse the
     Convolver machinery / an upscaled padded frame — mirror phase 2a's
     fine-state approach rather than writing new convolution code);
   - `psf_shape_2d` bookkeeping uses `psf.kernel_shape_image_resolution`
     (the image-resolution footprint), including `trimmed_after_convolution_from`.
   - Survey where the PyAutoArray simulator base (`via_image_from`) applies
     the kernel and whether the fine path is cleaner there or in
     `via_galaxies_from`; keep `s=1` byte-identical either way.
2. **Noise/exposure semantics unchanged** — oversampling affects only the
   noiseless model image; Poisson noise, background sky and exposure time
   apply at image resolution exactly as today.
3. **Workspace example**: extend
   `@autolens_workspace/scripts/imaging/simulator.py` (per the original
   phase-3 prompt) showing how to simulate with an oversampled PSF —
   supplying the fine-resolution kernel, choosing `convolve_over_sample_size`,
   and the uniform-over-sampling requirement. Brief prose; the guide-level
   treatment belongs to the docs phase (`oversampling_phase_4_docs.md`).
4. **Tests**: unit test that an s=2 simulation equals the brute-force
   fine-raster construction (ground-truth machinery); s=1 regression parity;
   round-trip test — simulate at s=2, fit at s=2 with `FitImaging`,
   chi_squared ~ noise expectation (extends
   `autolens_workspace_test/scripts/imaging/convolution_over_sampled.py`).

## Sequencing

After PyAutoArray#358 and autolens_workspace_test#149 merge. The
autolens_workspace claim from task `psf-oversample-workspace` is released
(no changes shipped there); this task claims it for the example.

Parent series: `issued/oversampling.md` → phase 3 (#232).
Related: `feature/autoarray/oversampling_refactor_followup.md` (run the
refactor only after this lands, so the simulator path is inside the guarded
test surface), `oversampling_phase_4_docs.md`.

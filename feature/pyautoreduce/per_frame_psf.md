# Per-frame native-pixel PSFs for the frame-products mode

Type: feature
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

The v1 frame-products mode (PyAutoReduce #16 / PR #18) ships per-exposure
data/noise/CR-DQ/WCS products but no PSF — the roadmap's open item. Without a
per-frame native-pixel PSF the frames are not fully modelable in PyAutoLens.

Deliver, per (exposure, chip) under frames/<root>_chipN/: a `psf.fits` in
NATIVE pixels (undrizzled, geometrically distorted frame space), plus manifest
provenance (method, source stars / model, normalisation).

Design questions to settle at start_dev (roadmap lists both routes):

- **ePSF route**: reuse psf/epsf machinery on the individual frame — star list
  found on the mosaic, positions projected into each frame via the
  full-distortion WCS (the footprint/`target_pixel` pattern), fit on native
  pixels. Cheap, self-consistent, noisier per frame (fewer counts/stars).
- **TinyTim / model-PSF route**: synthetic native-pixel PSF at the target's
  chip position + epoch focus. External dependency; well-tested for ACS.
- Likely v1: ePSF with the mosaic star list, TinyTim as the fallback/upgrade
  (mirror the mosaic's tiered PSF design); record tier in the manifest.
- Spatial variation: single PSF at the target position per chip is v1 scope
  (the cutout is small); note the variation caveat in the manifest.

Sequencing (user, 2026-07-10): AFTER the registration-shifts task
(research/pyautoreduce/frame_registration_shifts.md) — "Then do the PSF work".

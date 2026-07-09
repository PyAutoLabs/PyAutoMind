# JWST individual-frame output feasibility + literature scan (per-exposure modeling)

Type: research
Target: pyautoreduce
Repos:
- PyAutoReduce
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Split out of `feature/pyautoreduce/individual_frame_output_mode.md` at start_dev
on 2026-07-09 (the HST `_flc`/`_flt` half proceeded as a dev task; this is the
research half the Brain Feature Agent flagged as needing scoping before code).

Investigate whether the equivalent per-frame image output is possible and
meaningful for JWST data — the HST feature packages calibrated pre-drizzle
exposures (`_flc`/`_flt`); it is less clear what the right analogue is for the
JWST pipeline (stage-2 `_cal` products before `calwebb_image3` resample, ramp
handling, 1/f noise, distortion model differences).

Include a literature scan of galaxy-formation papers that do detailed analysis,
plus AGN and weak-lensing work, to assess whether people actually model
individual JWST frames or whether the standard mosaic is sufficient in practice.

Anchors from the HST work: the shipped mode is a packaging-only stage over
`ctx.exposures` (see PyAutoReduce `docs/design/roadmap.md` §"Per-exposure frame
products" and the design section added by the HST feature); per-frame cosmic-ray
handling there uses deepCR (Zhang & Bloom 2020; Chen et al. 2024 WFC3/UVIS
label-free retrain) with Cosmic-CoNN (Xu et al. 2023) the generalist
alternative — assess their applicability (or calwebb ramp-fitting jump
detection sufficiency) for JWST frames as part of the scan.

Deliverable: a design note in PyAutoReduce `docs/design/jwst.md` (or a new
section/doc) with a go/no-go recommendation and, if go, the adapter/pipeline
deltas needed to relax the HST-only guard on `frame_products`.

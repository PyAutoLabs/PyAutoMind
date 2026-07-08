# Oversampled PSF convolution — phase 1: design note + numerical ground truth

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Phase 1 of 4 of `feature/autoarray/oversampling.md` (split by the Feature Agent
on 2026-07-08 — the parent scored too-large). This phase produces the design
and the numerical reference result; **no source-code edits to the libraries**.

## Background (from the parent prompt)

A point spread function blurs images via 2D convolution, implemented in
`@PyAutoArray/autoarray/operators/convolver.py`. The source code currently
requires PSF blurring to occur at the same resolution (pixel scale) as the
image. For modeling, convolution can instead be performed at a higher
resolution: evaluate the image on an oversampled grid, blur with an
oversampled PSF, then downsample (bin) to the observed image resolution.
Oversampling machinery lives in `@PyAutoArray/autoarray/operators/over_sampling`.

Adaptive (per-pixel) over-sample sizes make 2D PSF convolution ill-defined —
this design assumes **uniform (non-adaptive) over sampling only**.

## Deliverables

1. **Design note** (posted to the phase GitHub issue, and saved alongside this
   prompt as `oversampling_design.md`) covering:
   - How `Convolver` gains a `convolve_over_sample_size` integer: the mapping
     between the oversampled evaluation grid, the oversampled PSF kernel, and
     the binning-down step to image resolution (e.g. size 2 = PSF at 2× the
     image resolution).
   - How `Imaging` (`@PyAutoArray/autoarray/dataset/imaging/dataset.py`) gains
     `convolve_over_sample_size_lp` and `convolve_over_sample_size_pixelization`
     attributes for the light-profile and pixelization operations respectively,
     alongside the existing `over_sample_size_lp` / `over_sample_size_pixelization`.
   - How PSF convolution enters the inversion path: read
     `@PyAutoArray/autoarray/inversion/inversion/imaging` and its parents.
     The working hypothesis is that oversampled convolution can be wired into
     `mapping.py`; `sparse.py` is explicitly deferred to future work — confirm
     or correct this and record why.
   - How model-image blurring in `@PyAutoGalaxy/autogalaxy/operate/image.py`
     consumes the new Convolver behaviour (survey only — implementation is
     phase 2).
   - How the code should behave when adaptive over sampling is requested
     together with oversampled convolution (expect: raise loudly, no silent
     fallback).
2. **Numerical ground truth**: a standalone brute-force reference computation
   (script or notebook-style scratch, checked in with this phase) using a
   simple analytic oversampled PSF, producing the number(s) the phase-2 unit
   tests and phase-3 workspace test will assert against.

## Acceptance

- Design note answers every point above with file/line grounding.
- Ground-truth script runs and its result is recorded in the design note.
- No edits to PyAutoArray/PyAutoGalaxy source.

Parent: `feature/autoarray/oversampling.md`. Next: `oversampling_phase_2_core_api.md`.

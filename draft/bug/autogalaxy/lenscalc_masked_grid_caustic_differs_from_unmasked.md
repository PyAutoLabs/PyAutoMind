# LensCalc tangential caustic on a masked grid differs ~27 % in ellipticity from every unmasked grid

Type: bug
Target: autogalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- caustics
- lens-calc
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: draft
Filed: 2026-09-17

## Original request (verbatim)

> (found while building the Witt–Wynne catalogue producer, euclid_strong_lens_modeling_pipeline#84)
> `LensCalc`'s `evaluation_grid` decorator rebuilds from `aa.Zoom2D(mask=grid.mask)`, and the
> masked DR1 grid gives caustic semi-axes ~27 % off the converged answer (`Tile102005065`:
> e=0.1267 masked vs e=0.1009 from 67×67@0.1", 100×100@0.1", 200×200@0.05", 300×300@0.02" and
> 400×400@0.01" — all unmasked grids agree to 1e-3). `b` and PA are unaffected (<0.15°).
> A masked grid silently yields a different caustic from every unmasked one.

## Context

- Witness: the euclid pipeline's `initial_lens_model/vis_pix` max-likelihood tracer for
  `Tile102005065RA0135279431487DECNEG0701599765928` (science clone
  `/mnt/c/Users/Jammy/Science/euclid_dr1_prelim/output/dr1_prelim_grade_ab`), `dataset.grid`
  (circular mask, radius 3.5") vs `al.Grid2D.uniform(shape_native=dataset.data.shape_native,
  pixel_scales=dataset.pixel_scales)`; compare `tangential_caustic_list_from` semi-axes.
- The pipeline producer (`catalogue/scripts/witt_wynne.py`) works around it by projecting on the
  unmasked uniform grid; the workaround and the numbers are documented in
  `euclid_strong_lens_modeling_pipeline/docs/witt_wynne.md`.
- Suspects: the Zoom2D extent/resolution chosen from a masked grid, or the critical-curve
  contour being clipped by the mask boundary before mapping to the source plane.

## Deliverables

1. Reproduce on a simulated SIE with a circular mask; bisect Zoom2D extent vs contour clipping.
2. Fix or document: either the caustic on a masked grid converges to the unmasked one, or
   `LensCalc` raises/warns when the critical curve is not enclosed by the mask.
3. Unit test pinning masked vs unmasked caustic semi-axes to 1e-3.

# Oversampled PSF convolution — phase 2c: PyAutoGalaxy consumer switch

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft

Phase 2c of the oversampled-PSF feature. **Blocked at creation** (2026-07-08)
by the `kaplinghat-sidm-cored-nfw` worktree claim on PyAutoGalaxy — start
after that task ships and after phase 2a is merged. Implements design note §5
(`feature/autoarray/oversampling_design.md`, approved on
PyAutoLabs/PyAutoArray#353) verbatim.

## Scope (design note §5)

1. `autogalaxy/operate/image.py::_blurred_image_2d_from` /
   `blurred_image_2d_from`: when `psf.convolve_over_sample_size > 1`,
   evaluate image and blurring image with `binned=False` (the 2a decorator
   kwarg) and pass the sub-gridded arrays to the Convolver.
2. The list/dict variants (`blurred_image_2d_list_from`,
   `galaxy_blurred_image_2d_dict_from`) route through the same switch.
3. `padded_image_2d_from` / `unmasked_blurred_image_2d_from` stay at image
   resolution — documented limitation (revisit in the docs phase).

## Tests (numpy-only)

- s=1: strict parity with existing blurred-image outputs.
- s=2: blurred image through `operate/image.py` matches the same computation
  done directly through the 2a Convolver API.
- Full PyAutoGalaxy pytest suite passes (plus PyAutoArray downstream check).

Parent: `oversampling_phase_2_core_api.md` (split record).
Previous: `oversampling_phase_2b_inversion_wiring.md`.
Next: `oversampling_phase_3_workspace_examples.md` (existing).

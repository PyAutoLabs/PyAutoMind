# SLaM / advanced-pipeline inversion+adapt-image cascade

Type: bug
Target: autolens
Repos:
- autolens_workspace
- HowToLens
- PyAutoLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Parked cluster of advanced-pipeline SLaM fit failures (2026-07-20 sweep), reproduced and scoped on
clean main 2026-07-21. The multi-wavelength `SersicCore alpha=0` failure proved **unrelated** and was
split out to `bug/autogalaxy/sersic_core_alpha_zero_division.md`. This task covers the SLaM
inversion / adapt-image cascade only.

## Reproduction (clean main, PYAUTO_TEST_MODE=2 PYAUTO_SMALL_DATASETS=1)

Two distinct signatures within the pixelized-SLaM cluster:

1. **double-Einstein-ring (imaging + group)** — `AttributeError: 'NoneType' object has no attribute
   'array'` at `PyAutoArray/.../inversion/mappers/abstract.py:476` (`self.adapt_data.array`), inside
   `pixel_signals_from` → adaptive-regularization weights. Occurs in phase `source_pix[1]_source_1`
   (imaging `slam.py:367`, group `slam.py:476`). **Same root cause in both scripts.**

2. **imaging/features/pixelization/slam** — `TypeError: add got incompatible shapes for broadcasting:
   (786, 786), (210, 210)` at `PyAutoArray/.../inversion/inversion/abstract.py:366`
   (`curvature_matrix + regularization_matrix`). A curvature/regularization **size mismatch** — needs
   phase-1 diagnosis to decide real-pipeline-bug vs synthetic-samples/test-mode artifact.

## Root cause (double-ring, confirmed real — not a test-mode artifact)

The SLaM setup uses `regularization_init = al.reg.Adapt` (adaptive regularization → needs a per-galaxy
adapt image). `source_pix_1_source_1` pixelizes `source_1`, but its stitched `galaxy_name_image_dict`
carries only `lens` + `source_0`. `source_0` obtained its adapt image from an earlier light-profile
phase; `source_1` was only ever a bare redshift galaxy, so **no adapt image can exist for it yet** →
`AdaptImages` yields no entry for source_1 → the source_1 mapper's `adapt_data` is `None` → crash.

## Chosen fix direction (phase 2)

**Seed `source_1` an adapt image** for its first pixelized fit — supply source_1 an adapt image derived
from the current tracer's lensed source-plane model image before the fit, so adaptive regularization
has data to weight on. (Alternative considered and rejected at scoping: bootstrap with `Constant`
regularization for source_1's first pix fit then switch to `Adapt`.)

## Phasing

- **Phase 1 — diagnose:** confirm double-ring root cause end-to-end; diagnose the pixelization/slam
  (786 vs 210) mismatch — is it the same adapt/synthetic-samples gap, a real mesh-size mismatch, or a
  test-mode-only artifact? Determine whether any fix is library (PyAutoArray/PyAutoGalaxy) or
  workspace-only. Reconcile the HowToLens target: the parent note's HowToLens paths
  (`imaging/features/pixelization/slam`) do not exist — HowToLens uses a `chapter_N_*` layout; find the
  real pixelization tutorial equivalents.
- **Phase 2 — fix double-ring:** seed source_1 adapt image; re-run both double-ring scripts green in
  test mode.
- **Phase 3 — fix pixelization/slam** per phase-1 verdict; update HowToLens equivalent.

Affected (remove NEEDS_FIX once green):
- autolens_workspace: `imaging/features/advanced/double_einstein_ring/slam`,
  `group/features/advanced/double_einstein_ring/slam`, `imaging/features/pixelization/slam`
- HowToLens: pixelization tutorial equivalent (verify real path in phase 1)

Split out (separate prompt): `multi/features/wavelength_dependence/modeling` → SersicCore alpha=0.

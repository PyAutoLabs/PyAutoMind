# Area magnification sub-pixel area follows the generated sub-pixels (arc 6a follow-up)

- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/687

Issue PyAutoGalaxy#686 → PR PyAutoGalaxy#687 merged 2026-10-30. Found by arc phase 6b smoke: `LensCalc`
`source_plane_area_from` assumed `sub_size**2` sub-pixels per pixel, but `Grid2D.from_mask` caps over-sampling to 2
under `PYAUTO_SMALL_DATASETS=1`, so A_src came out (2/sub_size)^2 too small; `area_magnification_from` unaffected.
Sub-pixel area now = pixel area × unmasked pixels / generated sub-pixels. Regression test sets the env var (fails
without the fix: 0.588 vs 2.352). PyAutoGalaxy 1467 passed; CI docs + 3.12/3.13/nojax green.

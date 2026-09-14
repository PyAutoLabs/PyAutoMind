# imaging/modeling smoke break: JSON guard fronts a visualizer-only FITS read

Type: bug
Target: autogalaxy_workspace
Repos:
- autogalaxy_workspace
Themes:
- workspace-smoke
- test-mode
Difficulty: easy
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Witness: `scripts/imaging/modeling.py` and its notebook pass the smoke profile (PYAUTO_TEST_MODE=2, PYAUTO_SKIP_VISUALIZATION=1) with the galaxies.json block executing and the FITS block skipped; autogalaxy_workspace Smoke Tests green on main
Review-minutes: 5
Filed: 2026-09-14

User request (verbatim, 2026-09-14):

"""
can you fix the PyAutoHeart being red
"""
(follow-up "continue"; plan approved 2026-09-14 23:50.)

## Context

autogalaxy_workspace Smoke Tests run 34904232479 (2026-09-14 22:27Z, push c70aed9) fails
`notebooks/imaging/modeling.ipynb` on both 3.12 and 3.13 legs (the regen-from-source retry fails identically):

    FileNotFoundError: .../output/test_mode/imaging/features/simple/start_here/<hash>/image/galaxy_images.fits

Cause: PyAutoFit #1626 (461ac836c, merged 20:25Z, between the passing 09:26Z run and this one) makes the
test-mode bypass call `analysis.save_results`, so `files/galaxies.json` now exists under smoke. The block at
`scripts/imaging/modeling.py:513-518` guards on that JSON but reads `image/galaxy_images.fits` inside the same
guard; the FITS is written only by the visualizer (PyAutoGalaxy imaging/model/plotter.py:86-87), which
PYAUTO_SKIP_VISUALIZATION=1 disables. Before #1626 the whole block was skipped, hiding the folded guard.
Sibling scripts already use two separate `exists()` guards (autolens_workspace scripts/imaging/modeling.py:656-661,
multi_galaxy/modeling.py:803-808; autogalaxy_workspace scripts/guides/results/start_here.py:242-244). A sweep of
every workspace and HowTo repo for `json").exists()` blocks containing `from_fits` found only this script.

## Fix

Split the guard: keep `galaxies = from_json(...)` under the galaxies.json check and move the
`ag.Array2D.from_fits(... "image" / "galaxy_images.fits" ...)` read (and anything that uses `galaxy_images`)
under its own `(result_path / "image" / "galaxy_images.fits").exists()` guard, mirroring the autolens sibling.
Regenerate the notebook per the workspace convention.

Split the folded guard in `autogalaxy_workspace/scripts/imaging/modeling.py`'s "Loading From
Output Folder" block: `files/galaxies.json` keeps the `from_json` load, and the
`image/galaxy_images.fits` read now sits behind its own
`if (result_path / "image" / "galaxy_images.fits").exists():` guard — mirroring
`autolens_workspace/scripts/imaging/modeling.py:656-661`. `notebooks/imaging/modeling.ipynb`
was regenerated from the script.

The break was exposed, not caused, by PyAutoFit #1626 (`test-mode-bypass-save-results`, merged
2026-09-14): the test-mode bypass now calls `analysis.save_results`, so `files/galaxies.json`
exists under the smoke profile for the first time and the folded block finally ran — then
`FileNotFoundError`d on the FITS, which only the visualizer writes and
`PYAUTO_SKIP_VISUALIZATION=1` disables. A sweep of every workspace and HowTo repo for
`json").exists()` blocks containing `from_fits` found no sibling to fix. Workspace-only; no
upstream library PR.

## Validation

Control on the unfixed `main` checkout reproduced the CI `FileNotFoundError` on both legs
(script FAIL 16.0s; notebook FAIL 12.6s plus an identical regen-from-source retry FAIL 16.3s).
Witness on the branch passes both (script PASS 14.7s; notebook PASS 10.9s), with
`files/galaxies.json` present and `image/` absent — the JSON block runs and the FITS block
skips, not a vacuous double-skip. Canonical PyAutoFit was at `f243e11` (past #1626), so the
control exercised the new bypass behaviour.

## Shipped

- autogalaxy_workspace PR #243 — merged 2026-09-15 as `16d98e0d80f5f14f0db633e17679e656d4ea0e5c`
  (https://github.com/PyAutoLabs/autogalaxy_workspace/pull/243)
- Issue #242 closed as completed.
- CI at merge: all 7 checks green on head `b4da2d69` — Navigator Check (paths+banner lint,
  catalogue staleness, unbatched multi-start search), Script Size Guard, Smoke Tests
  (changes, 3.12, 3.13).

Clears the Heart RED reason `autogalaxy_workspace: Smoke Tests failure on main`.

## Follow-up

`imaging/modeling.py` is still commented out of `autogalaxy_workspace` `smoke_tests.txt` —
unchanged by this PR.

## Original prompt

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
Status: active
Consequence: judge
Witness: `scripts/imaging/modeling.py` and its notebook pass the smoke profile (PYAUTO_TEST_MODE=2, PYAUTO_SKIP_VISUALIZATION=1) with the galaxies.json block executing and the FITS block skipped; autogalaxy_workspace Smoke Tests green on main
Review-minutes: 5
Filed: 2026-09-14
Issued: 2026-09-14

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

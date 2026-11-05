## cti-fits-fit-output-dir
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/119
- completed: 2026-11-05
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/120
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/41

Merged 2026-11-05 by glance-tier auto-merge (plan approved by the human): PyAutoCTI#120 (1cd2f0d0), then autocti_workspace#41. Issue #119 closed. cti-upkeep phase 3.

Both autocti FITS writers (`dataset_1d/plot/fit_plots.py`, `charge_injection/plot/fit_ci_plots.py`) now `mkdir(parents=True, exist_ok=True)` before writing `fit.fits`. Under `PYAUTO_FAST_PLOTS=1`, `subplot_save` returns before creating the plotter subfolder, so every visualized fit used to crash with FileNotFoundError. The autocti_workspace release profile is back to `PYAUTO_FAST_PLOTS: "1"`.

Evidence:
- 2 new tests, both failing on main (control).
- `test_autocti` 277 passed (serial).
- Witness PASS: 3/3 release smoke scripts with FAST_PLOTS=1 (about 10s / 9s / 26s, down from 46s / 34s / 98s).
- Independent review (separate-model subagent): CLEAN. The only two `writeto` calls outside instruments/ are both covered.
- CI green on both PRs.

PyAutoCTI#120 carries the GitHub `pending-release` label.

## Original prompt

# autocti: fits_fit writes fit.fits into a directory nothing creates when PYAUTO_FAST_PLOTS=1

Type: bug
Target: autocti
Repos:
- autocti
- autocti_workspace
Themes:
- cti
- visualization
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: with `PYAUTO_TEST_MODE=1 PYAUTO_SKIP_VISUALIZATION=0 PYAUTO_FAST_PLOTS=1`, `scripts/dataset_1d/modeling/start_here.py` and `scripts/imaging_ci/modeling/start_here.py` in autocti_workspace run to completion and write `image/fit_dataset/fit.fits`; autocti_workspace `config/build/profile_release.yaml` flips back to `PYAUTO_FAST_PLOTS: "1"`.
Review-minutes: 3
Unattended: ready
Epic: cti-upkeep
Phase: 3
Issued: 2026-11-05

## What happens

Found 2026-11-05 while adding autocti_workspace `config/build/profile_release.yaml`
for the release train (PyAutoHands#332). All 3 `smoke_tests.txt` scripts fail
under the release profile with FAST_PLOTS on:

```
FileNotFoundError: .../output/test_mode/dataset_1d/simple/species[x2]/<hash>/analyses/analysis_0/image/fit_dataset/fit.fits
  autocti/dataset_1d/model/plotter.py:202  fit_plots.fits_fit(fit=fit, output_path=output_path)
  autocti/dataset_1d/plot/fit_plots.py:216 hdu_list.writeto(Path(output_path) / "fit.fits", ...)
```

`output_path` is the `image_path / "fit_dataset"` subfolder. It only gets created as a
side effect of `autoarray.plot.utils.subplot_save` saving a figure. With
`PYAUTO_FAST_PLOTS=1` that function returns before it creates the directory, so the
FITS write fails. PyAutoGalaxy avoids this because its base plotter `image_path`
calls `os.makedirs`, and its fits writers target that path directly.

## Fix

Create the directory before the write in both FITS writers:
`autocti/dataset_1d/plot/fit_plots.py::fits_fit` and
`autocti/charge_injection/plot/fit_ci_plots.py::fits_fit` (or make the CTI plotters'
subfolder paths `mkdir(parents=True, exist_ok=True)`). Add a unit test that calls
`fits_fit` with a non-existent output directory. Then set the release profile's
FAST_PLOTS back to "1" (the temporary workaround comment points here).

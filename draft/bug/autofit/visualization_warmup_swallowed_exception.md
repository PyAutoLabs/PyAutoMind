# Visualization warm-up swallowed for ellipse and point-source analyses

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoGalaxy
- autogalaxy_workspace_test
- PyAutoLens
- autolens_workspace_test
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: running the ellipse and point_source modeling_visualization_jit.py scripts from a cleared output/ under profile_release logs 'Visualization warm-up complete.' and never 'Visualization warm-up failed'
Review-minutes: 3
Unattended: needs-slicing

# Visualization warm-up swallowed for ellipse and point-source analyses

Type: bug
Target: autofit
Difficulty: large
Priority: medium
Witness: running the ellipse and point_source modeling_visualization_jit.py scripts from a cleared output/ under profile_release logs 'Visualization warm-up complete.' and never 'Visualization warm-up failed'

Owner @PyAutoFit; @PyAutoGalaxy (AnalysisEllipse) and @PyAutoLens (AnalysisPoint) analyses involved.

Observed 2026-09-15 while re-running the four `modeling_visualization_jit.py` test-workspace scripts under `profile_release` on current `main` (PyAutoFit `27d41e7c8`, PyAutoGalaxy `840ffde0`, PyAutoLens `ccf9295f3`): `autogalaxy_workspace_test/scripts/ellipse/visualization/modeling_visualization_jit.py` and `autolens_workspace_test/scripts/point_source/visualization/modeling_visualization_jit.py` both log

    Visualization warm-up failed (non-fatal); first quick update may be slow.

while the imaging and interferometer siblings warm up fine.

Source: `PyAutoFit/autofit/non_linear/fitness.py:314-335`, `_warmup_visualization()`, which calls `self.model.instance_from_prior_medians()`, then `self.analysis.fit_for_visualization(instance)` and `fit.model_data` inside a bare `except Exception:` that logs the one-line warning with no exception text, so the cause is invisible.

Consequence: for `AnalysisEllipse` and `AnalysisPoint` the JAX pre-compile is silently skipped and every first quick update recompiles (point_source: 7.4 s first quick update vs 2.8 s for later ones; weakest JIT-cache ratio of the four scripts at 7.9x vs 18-54x). The scripts still pass, so there is no CI signal.

## Required work

1. Reproduce with the two scripts (cleared `output/`, `profile_release.yaml`, env resolved by the release-profile env resolver at workspace CWD).
2. Surface the swallowed exception — log with `exc_info` at minimum; decide whether a warm-up failure should raise under `PYAUTO_TEST_MODE` / in tests rather than warn.
3. Fix the underlying cause for the ellipse and point-source analyses so warm-up completes.
4. Add focused tests that `_warmup_visualization` succeeds for imaging, interferometer, ellipse and point analyses.

## Related observation (not the main defect)

Same runs, point_source, twice: `PyAutoGalaxy/autogalaxy/operate/lens_calc.py:565` `UserWarning: LensCalc Hessian: 1 of 625 points did not converge after 20 halvings (largest relative error estimate 2.58e+00); values kept` — a 2.58 relative error kept silently.

## Origin

Incidental finding of `complete/2026/09/jit-visualization-outputs.md` (autolens_workspace_test#318, closed 2026-09-17); not that task's scope.

<!-- formalised by the Intake (Conception) Agent on 2026-09-15 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b3c838a6-7f5b-48c8-964d-ea2e0cd93818/scratchpad/intake-warmup.txt -->

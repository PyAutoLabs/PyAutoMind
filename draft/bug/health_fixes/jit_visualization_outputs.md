# Fix JIT quick-update visualization output regressions

Type: bug
Target: health_fixes
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

## Context

Four test-workspace scripts expect real release-profile searches to invoke the JIT-cached
quick-update visualization path and produce fit images. CI reported missing files. Local
`main` still fails the ellipse, interferometer, and point-source cases, while imaging
passes.

Owners: @PyAutoFit, @PyAutoGalaxy, @PyAutoLens, @autogalaxy_workspace_test, and
@autolens_workspace_test.

## Scripts

- `autogalaxy_workspace_test/scripts/ellipse/modeling_visualization_jit.py`
- `autogalaxy_workspace_test/scripts/imaging/modeling_visualization_jit.py`
- `autogalaxy_workspace_test/scripts/interferometer/modeling_visualization_jit.py`
- `autolens_workspace_test/scripts/point_source/modeling_visualization_jit.py`

## Required work

1. Reproduce from clean output directories with JAX enabled and real release-profile
   searches.
2. Trace search update cadence, visualization dispatch, cached fit creation, output-path
   routing, and exception handling for all four dataset types.
3. Fix the shared library path where possible; do not add sleeps, weaken assertions, or
   fabricate image files in scripts.
4. Add focused tests proving quick updates invoke visualization and write the expected
   artifact for ellipse, imaging, interferometer, and point-source analyses.
5. Run owning-library tests and all four scripts under the release profile.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

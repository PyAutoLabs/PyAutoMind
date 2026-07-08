# Fix release result/sample parameter-path regressions

## Context

PyAutoHeart release validation run `28784914443` exposed a family of workspace
failures. Against current `main`, nine scripts converge on
`PyAutoFit/autofit/non_linear/samples/sample.py::parameter_lists_for_paths`
raising `KeyError` for model paths that no longer match stored sample kwargs.

Primary repository: @PyAutoFit. Downstream verification repositories:
@autogalaxy_workspace and @autolens_workspace.

## Scripts

- `autogalaxy_workspace/scripts/imaging/features/pixelization/galaxy_reconstruction.py`
- `autogalaxy_workspace/scripts/imaging/features/shapelets/modeling.py`
- `autogalaxy_workspace/scripts/multi/features/imaging_and_interferometer/modeling.py`
- `autolens_workspace/scripts/group/features/advanced/mass_stellar_dark/chaining.py`
- `autolens_workspace/scripts/guides/modeling/advanced/hierarchical.py`
- `autolens_workspace/scripts/imaging/features/advanced/shapelets/modeling.py`
- `autolens_workspace/scripts/interferometer/features/subhalo/detect/start_here.py`
- `autolens_workspace/scripts/interferometer/features/extra_galaxies/slam.py`
- `autolens_workspace/scripts/multi/features/imaging_and_interferometer/modeling.py`

## Required work

1. Reproduce from clean task worktrees with the release profile and current library
   sources; distinguish stale cached output from newly written samples.
2. Trace model path construction, stored kwargs, path aliases, and collection/list
   indices through `Samples`, `Sample`, and result loading.
3. Fix the owning PyAutoFit contract if valid current-model paths cannot resolve.
   Do not weaken workspace scripts or silently ignore missing parameters.
4. Add focused PyAutoFit regression tests covering single, multi-analysis, chained,
   list-profile, and multi-dataset paths represented above.
5. Run PyAutoFit pytest, then rerun all nine scripts under their release profiles.

Preserve tutorial prose and make workspace edits only where a script genuinely uses a
retired API rather than exposing a library defect.

# Fix release aggregator and generated-output contracts

## Context

Seven release failures involve results that are absent, shorter than examples assume,
or written to a different location. Several pass in a stateful local checkout, so the
first task is a clean, directory-ordered reproduction. Primary owners are @PyAutoFit,
@autogalaxy_workspace, @autolens_workspace, and @autolens_workspace_test.

## Scripts

- `autogalaxy_workspace/scripts/guides/results/start_here.py`
- `autogalaxy_workspace/scripts/guides/results/aggregator/samples_via_aggregator.py`
- `autolens_workspace/scripts/guides/results/start_here.py`
- `autolens_workspace/scripts/guides/results/aggregator/galaxies_fits.py`
- `autolens_workspace/scripts/guides/results/aggregator/samples_via_aggregator.py`
- `autolens_workspace/scripts/guides/results/workflow/csv_make.py`
- `autolens_workspace_test/scripts/imaging/convolution.py`

## Required work

1. Run each parent directory in CI order from a clean output tree under the release
   profile, then rerun each script independently to document prerequisites.
2. Determine whether failures are library output/aggregator regressions, invalid script
   assumptions about sample counts, or missing directory creation for generated files.
3. Fix PyAutoFit when valid completed searches are not discoverable. Otherwise update
   scripts minimally while preserving their teaching narrative.
4. Ensure scripts create their own output directories and do not depend on unrelated
   earlier legs or developer-local artifacts.
5. Add the narrowest appropriate tests and rerun all seven release-profile scripts.

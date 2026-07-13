## autolens-results-aggregator-valid-dataset
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/220
- completed: 2026-06-09
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/221 (merged 256ce20)
- repos: autolens_workspace
- notes: Fixed the results aggregator release failures by making `_quick_fit.py` reuse `output/results_folder` only when it contains at least one `image/dataset.fits`, regenerating stale/incompatible helper output otherwise. Updated the aggregator scripts to use the same valid-dataset guard and to pass the test-mode-aware `results_path` to `Aggregator.from_directory`. Verified the two reported scripts directly, the full `autolens scripts/guides/results/aggregator` PyAutoBuild directory run, and PR CI on Python 3.12/3.13 before merge.

## Original prompt

# Fix autolens results aggregator dataset reload

Original user request:

> continue

Release report context:

The PyAutoBuild release run reports two failures in `autolens_workspace`:

- `scripts/guides/results/aggregator/data_fitting.py`
- `scripts/guides/results/aggregator/models.py`

Both fail when `al.agg.ImagingAgg(...).dataset_gen_from()` attempts to reconstruct an imaging dataset:

```text
TypeError: 'NoneType' object is not subscriptable
  PyAutoGalaxy/autogalaxy/aggregator/agg_util.py:101
  header = aa.Header(header_sci_obj=fit.value(name=name)[0].header)
```

Reproduction on current `autolens_workspace/main` using the PyAutoBuild environment confirms that the aggregator finds fits under `output/results_folder`, but `agg.values("dataset.mask")` returns `[None, None]` for stale or incompatible results. The output tree can contain a completed fit without `image/dataset.fits`, while the aggregator tutorials require that FITS artifact.

Fix the workspace results aggregator flow so the affected scripts only scrape reusable helper results that contain `image/dataset.fits`, while preserving the normal tutorial behavior and PyAutoBuild test-mode path handling.

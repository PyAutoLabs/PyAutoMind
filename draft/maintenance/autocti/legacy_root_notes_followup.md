# Review unresolved CTI questions from retired root notes

Type: maintenance
Target: autocti
Consequence: judge
Status: draft

@PyAutoCTI @autocti_workspace

## Original request

> ok yeah sort those fils I agree these all look old and efunt

## Context

On 2026-11-10 the human approved cleanup of obsolete top-level material during
the README review. The nine files in the table below were removed locally, without commits
or pushes. Their exact contents remain in tracked history at the listed SHAs.
The old notes are historical questions, not evidence of present defects or an
instruction to implement every item.

## Existing work to consult first

- `draft/maintenance/autocti/cti_upkeep_epic.md` and its companion report:
  broader workspace, visualization and arcticpy upkeep.
- `draft/docs/autocti/installation_docs_arcticpy_recipe.md`: installation guidance.
- `draft/bug/autocti_workspace/database_scripts_stale_sqlite_under_test_mode.md`:
  database and temporal rerun failures.
- Existing `scripts/dataset_1d/advanced/temporal/` examples already address part
  of the time-evolution topic. Assess current coverage before creating work.

## Questions preserved for triage

- Does ImagingCI still need explicit pre-CTI data in cases where it can be estimated?
- Do temporal calibration examples demonstrate interpolation for science-image
  correction and compare independent fits, shared release timescales and
  parameterized evolution? Is a graphical-model comparison still wanted?
- Are calibration provenance / data-product interfaces and any Euclid XML
  integration still required? Historical collaborator names do not establish
  current requirements.
- Is flat-field calibration still desired?
- Are realistic cosmic-ray examples and tests adequate, including nonuniform
  charge injection and trails?
- Are plotting needs covered: rectangular extraction aspect, FPR labels,
  region selection, noise maps, chi-squared and useful zoom ranges?
- Do results, database, data-preparation and chaining examples need further
  teaching review beyond the existing upkeep tasks?

No additional science or API changes are authorized by this cleanup record.

## Cleanup evidence and recovery

- `libraries.txt`: old development bookmarks, including Python 2 documentation.
- `profiling`: orphaned code fragment, not a standalone profiling program.
- `to_do_list` / `notes`: historical development notes; questions retained above.
- `build_requirements.txt`: its sole `getdist==1.4` dependency is already declared
  in PyAutoFit's `pyproject.toml`; no consumer found in the source/CI or Hands searches.
- Four saved March plotting patches: superseded by the present function-based
  plotting implementation; not part of the current packaging or build flow.

| Repository | Removed path | Pre-delete commit |
|---|---|---|
| lens/PyAutoLens | `libraries.txt` | `5bb8d2ec51682c0a56bd29d81175b0f22a242c09` |
| cti/PyAutoCTI | `profiling` | `08040ff5f6e450f2c15644f324e7df7afe03b54d` |
| cti/PyAutoCTI | `to_do_list` | `08040ff5f6e450f2c15644f324e7df7afe03b54d` |
| cti/autocti_workspace | `notes` | `a4c11219cda9bd347326e0dddd844371bfe76da5` |
| fit/PyAutoFit | `build_requirements.txt` | `bdb7af0e9c339ad07850679fd6ac168aacc7d18c` |
| lens/PyAutoLens | `patches/autoarray/0001-PR-A1-Add-autoarray-plot-plots-direct-matplotlib-mod.patch` | `5bb8d2ec51682c0a56bd29d81175b0f22a242c09` |
| lens/PyAutoLens | `patches/autoarray/0002-PR-A2-A3-Switch-all-autoarray-plotters-to-use-direct.patch` | `5bb8d2ec51682c0a56bd29d81175b0f22a242c09` |
| lens/PyAutoLens | `patches/autoarray/0003-PR-A3-replace-mat_plot_2d.plot_array-in-FitImagingPl.patch` | `5bb8d2ec51682c0a56bd29d81175b0f22a242c09` |
| lens/PyAutoLens | `patches/autogalaxy/0001-PR-G1-G2-replace-mat_plot_2d.plot_array-with-_plot_a.patch` | `5bb8d2ec51682c0a56bd29d81175b0f22a242c09` |

Recover an individual file with `git restore --source=<commit> -- <path>` from
its repository. No history or recovery refs were deleted.

## Eden configs removed with explicit approval

The human subsequently instructed: "remove th eden things and continue".
Both configs were removed locally on 2026-11-10; external consumers were not
verified. Recovery remains available from tracked history:

- `fit/PyAutoFit/eden.yaml`: recover from `bdb7af0e9c339ad07850679fd6ac168aacc7d18c`.
- `cti/PyAutoCTI/eden.ini`: recover from `08040ff5f6e450f2c15644f324e7df7afe03b54d`.

Working build scripts, the Reduce size snapshot and CTI's bulk simulator script
remain in place.

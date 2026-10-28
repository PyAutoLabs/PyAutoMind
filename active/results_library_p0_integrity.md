# Results library phase 0: artefact integrity and honest reads in PyAutoFit (shared with hpc-campaign) — one issue, PR 0a then PR 0b

Type: feature
Target: autofit
Repos:
- PyAutoFit
Themes:
- results
- aggregator
- hpc
Difficulty: large
Autonomy: human-required
Priority: high
Status: formalised
Consequence: judge
Witness: PR 0a — a killed-mid-zip fixture resumes cleanly; two processes restore one zip concurrently and both read it; truncated-HDF5 and poisoned-checkpoint fixtures start fresh with the old state moved aside (`search_internal.failed_<utc>/`); `.png/.fits/.hdf5` members are ZIP_STORED; PR 0b — a fixture tree with one corrupt zip aggregates with `len(agg.errors) == 1`; an unknown AggregateCSV column raises; the header is the union of rows; a killed-mid-save leaves the previous CSV intact; `row.py` sigma-1/sigma-3/max_lh tests pass on an asymmetric latent fixture; `autolens_workspace_test` smoke green for both PRs
Review-minutes: 45
Unattended: never
Epic: results-library
Phase: 0
Shared-with: hpc-campaign
Parent: draft/feature/autofit/results_library_epic.md
Filed: 2026-10-28
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1734

Phase 0 of the `results-library` epic (ledger `draft/feature/autofit/results_library_epic.md`, §Phase 0;
report `results_library_epic_report.md` P1, P2, P11, P12, P13). Shared with `hpc-campaign`: its ledger
records this issue as its phase 0 #A and does not re-issue it (ruling F1, 2026-10-28). The `fit()` failure
record is **not** here; it is hpc-campaign phase 1. Scoping review:
`/mnt/c/Users/Jammy/Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/REVIEW.md` §D.1.

One PyAutoFit issue, two PRs in order. Ground against PyAutoFit `main` at or after `8740092dc`
(2026.10.26.1); the plan quotes the current lines (the ledger's `710f4b343` references are stale). Build on
`open_atomic` (`tools/util.py`), the Checkpointer/`internal_state.py` split (#1680) and the
"finalise archive then `.completed`" order (#1683).

## PR 0a — artefact integrity

- `zip_directory`: write `<path>.zip.tmp`, then `os.replace`; `ZIP_STORED` for `.png/.fits/.hdf5`, text
  DEFLATED. A zip is complete or absent, never truncated.
- `restore()`: extract to a temp dir and swap; never delete the zip unless the caller owns the result
  (`remove_files` **and** this search's identifier); `BadZipFile` → rename `<hash>.zip.corrupt_<utc>`, log,
  continue as "not complete". Read-only `open_result()` for downstream stages.
- `is_complete` for a zipped result: `.completed` member + `zipfile.testzip()`, cached per path; `fit()`
  consults it before `restore()`.
- Checkpoint validity probe in `Checkpointer.load` for Nautilus (h5py open; catch `OSError`, `ValueError`,
  `RuntimeError`, `KeyError`) and dynesty; on failure or a sampler `LinAlgError`, move `search_internal/` to
  `search_internal.failed_<utc>/`, start fresh, log once.
- Timer files → `<output_path>/files/` behind the `has_timer` capability; atomic write.

## PR 0b — honest reads

- `Aggregator.from_directory(..., on_error="skip"|"raise")`, `agg.errors` (path, exception); an empty
  aggregator logs a loud warning naming path and filters; `print` → `logging` across the aggregator.
- AggregateCSV: `strict=True` default; union header; atomic save; labels joined by key; `save()` reports
  blank columns.
- `row.py` regression tests (sigma-1, sigma-3, max_lh) on an asymmetric latent PDF fixture; fix the
  inverted `post_fit_output` docstring.

## Worktree file ownership (review §D.4, ruling F11)

This lane: `autofit/tools/util.py`, `non_linear/paths/`, `non_linear/checkpoint.py`, `aggregator/`,
`non_linear/timer.py`. Shared touchpoint `non_linear/search/abstract_search.py` (`fit()` consults
`is_complete` before `restore()`) lands in PR 0a; hpc-campaign phase 1 (`non_linear/status/`) merges after
PR 0a. Ships `pending-release`. Ledger entry in both epic ledgers on ship.

## test-mode-output-path
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1291
- completed: 2026-05-22
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1292
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/119
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/61
- notes: Shipped PYAUTO_TEST_MODE output-path namespacing. Library change adds `_test_mode_segment()` helper in `autofit/non_linear/paths/abstract.py` and threads it through three composition sites (`AbstractPaths.output_path`, `DirectoryPaths._make_path`, `open_database` when filename is relative); `SubDirectoryPaths` inherits via parent. Cross-workspace smoke sweep was the validation cost: 63 pass / 7 fail / 2 skip across 6 workspaces + ic50 native-habitat check. All 7 failures were aggregator integration scripts in autolens_workspace_test and autogalaxy_workspace_test that hardcoded `PYAUTO_TEST_MODE=1` inline and reconstructed `result_path` by joining `conf.instance.output_path` with the database name — migrated to include `"test_mode"` as a segment (20 sites total). SQLite database files stay at the bare output_path root because `Aggregator.from_database(filename=...)` is called with an absolute path, bypassing the library's relative-filename injection in `open_database`. Memory `feedback_autofit_cache_resume_pyauto_test_mode` rewritten — the historical `rm -rf` workaround is obsolete. Worth a future cleanup pass on `z_projects/ic50_workspace/scripts/profile_ep_sim.py` which still does `rm -rf output/ep_sim/` defensively; harmless now (deletes an empty bare path) but no longer load-bearing.

## Original prompt

# PYAUTO_TEST_MODE should mutate the AutoFit output path

When a script is smoke-tested under `PYAUTO_TEST_MODE` and then later run
for real, AutoFit silently returns the cached test-mode result ("Fit
Already Completed: skipping non-linear search") because the output path
is identical between the two runs. The proper run never happens —
symptom is every recovered σ on the supposedly-real run being exactly 0.

This was hit on the IC50 EP / graphical scripts and the current
workaround is "rm -rf `output/<path-prefix>/` before the first proper
run", which is runtime discipline that contributors will forget.

## What I want

Make `PYAUTO_TEST_MODE` mutate the output path so smoke and prod
outputs are physically co-resident and can't collide. The `rm -rf`
workaround becomes unnecessary.

## Where

Inject a `test_mode/` segment at the root of the output tree when
`os.environ.get("PYAUTO_TEST_MODE")` is set and truthy:

- prod: `output/<prefix>/<name>/<identifier>/`
- test: `output/test_mode/<prefix>/<name>/<identifier>/`

I prefer collecting all test-mode outputs under one tree (easy to
gitignore or wipe wholesale) rather than splitting at the identifier
level.

There are **three** places that compose paths from
`conf.instance.output_path` — they all need the same treatment, so
factor a shared helper rather than patching each site:

1. `PyAutoFit/autofit/non_linear/paths/abstract.py:239` — `output_path`
   property on `AbstractPaths`.
2. `PyAutoFit/autofit/non_linear/paths/directory.py:533` — `_make_path()`
   on `DirectoryPaths`, which reconstructs the path manually instead
   of using the property. (Aside: it omits `unique_tag` while the
   property includes it — pre-existing inconsistency, don't fix here.)
3. `PyAutoFit/autofit/database/__init__.py:60` — read the surrounding
   context before patching; may or may not need the segment depending
   on whether it represents a search-output dir.

`SubDirectoryPaths` overrides `output_path` in
`sub_directory_paths.py:74,123` but its `_output_path` delegates to
`self.parent.output_path`, so it inherits the fix for free via the
parent.

Suggested helper signature:

```python
def _test_mode_segment() -> Optional[str]:
    return "test_mode" if os.environ.get("PYAUTO_TEST_MODE") else None
```

Then filter it into the path components at each of the three sites,
right after `conf.instance.output_path`.

## Validation

The code change is small; the cost is validation across every
workspace, since the risk is a script that secretly relies on smoke
and prod sharing the output path.

- PyAutoFit unit suite green.
- Add a regression test: run a search under `PYAUTO_TEST_MODE=2`, then
  again with `PYAUTO_TEST_MODE` unset, and assert the second run
  re-fits (does not hit the `is_complete` short-circuit).
- `/health_check` followed by `/smoke_test` on every workspace:
  `autofit_workspace`, `autogalaxy_workspace`, `autolens_workspace`,
  `autolens_workspace_test`, `autogalaxy_workspace_test`,
  `euclid_strong_lens_modeling_pipeline`, `ic50_workspace`. ic50 is
  where the bug was first hit so it must be in the sweep.
- Pick one or two scripts that already have output in `output/`, run
  them with and without `PYAUTO_TEST_MODE`, and confirm the two land
  in distinct directories.

## Out of scope

- Renaming smoke runs script-by-script (the whole point is the
  per-script rename is unnecessary).
- Touching the `is_complete` short-circuit — once paths differ, the
  existing logic is correct.

## Once shipped

Update the `feedback_autofit_cache_resume_pyauto_test_mode` memory:
the `rm -rf` workaround is obsolete.

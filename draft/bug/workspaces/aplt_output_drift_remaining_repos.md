# `aplt.Output` stale-API drift in the remaining workspace repos

Type: bug
Target: workspaces
Repos:
- autocti_workspace_test
- euclid_strong_lens_modeling_pipeline
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-08-04 (backfilled from git)

Split out of `plot-array-stale-kwargs` (HowToGalaxy#56, 2026-08-04), which
repaired this same drift in `autolens_workspace_developer` but deliberately
stopped at that repo's boundary.

## The drift

`aplt.Output` no longer exists on the **autolens / autogalaxy** plot namespace —
verified: `hasattr(autolens.plot, "Output") == False`. It survives only as
`autoarray.plot.Output`. The removal was deliberate and is already documented in
`autolens_assistant/AGENTS.md:218` ("the `aplt.MatPlot2D` / `aplt.Output` objects
have been removed — do not use them").

Callers must move to the flat convention. Note the accepted kwargs differ per
callee — check each signature rather than blanket-renaming:

```python
# plot_array takes all three
aplt.plot_array(array=..., output_path=P, output_filename=F, output_format="png")
# subplot_* take only path + format (no output_filename)
aplt.subplot_tracer(tracer=..., grid=..., output_path=P, output_format="png")
```

## Sites

| Repo | Files | Status |
|------|-------|--------|
| `autocti_workspace_test` | 27 | **UNVERIFIED — check first** |
| `euclid_strong_lens_modeling_pipeline/tools/` | 2 (`psf_size.py`, `extra_galaxies_centres_gui.py`) | confirmed broken |

**Do not assume the autocti files are broken.** Those import
`import autocti.plot as aplt` — a *different* library's plot namespace.
`autocti` was not installed in the 2026-08-04 session so it could not be
checked. PyAutoCTI may still export `Output`, in which case those 27 files are
correct as written and must be left alone. Verify with
`hasattr(autocti.plot, "Output")` before touching anything.

Confirmed **not** bugs, do not "fix" them:
- `PyAutoArray/test_autoarray/plot/test_output.py` — there `aplt` *is*
  `autoarray.plot`, which does export `Output`.
- `autolens_assistant` markdown — documents the removal.

## Verification

Re-run an alias-aware AST scan after the fix (the 2026-08-04 session's first
sweep hardcoded the alias `aplt` and **missed** a call site written as `aaplt`;
resolve aliases from each file's own imports). Then bind each changed call's
kwargs against the real callee signature via `inspect.signature`, since these
repos have little or no CI to catch a wrong kwarg name.

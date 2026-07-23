# no_run.yaml (and sibling build configs) are 41% dead entries from copy-paste

Type: maintenance
Target: HowToLens
Repos:
- HowToLens
- HowToGalaxy
- autolens_workspace
- HowToFit
- autogalaxy_workspace_test
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> clean up no_run.yaml fiels in HowTo and other repos, which clearly are not in
> sync with their actual contents and have a lot of stuff from legacy old code
> etc. do a full census of all configs of this nature.

## Census (complete, 2026-07-23)

Evaluated every entry in every `config/build/` path-pattern config across all 10
build targets in `PyAutoHands/autobuild/config/workspaces.yaml`, using the real
matcher (`PyAutoHands/autobuild/build_util.py:143` `should_skip`): an entry
containing `/` is a substring match against the full path including extension;
an entry without `/` matches the file stem exactly. `run_all` walks only
`scripts/` (`run_all.py:78`).

### no_run.yaml — 122 entries, 50 zero-match (41%)

| Repo | Entries | Zero-match |
|---|---|---|
| autolens_workspace | 27 | 7 |
| HowToLens | 30 | 28 |
| HowToGalaxy | 16 | 15 |
| autolens_workspace_test | 23 | 0 |
| autogalaxy_workspace | 10 | 0 |
| autogalaxy_workspace_test | 9 | 0 |
| autofit_workspace | 5 | 0 |
| autofit_workspace_test | 2 | 0 |
| HowToFit | 0 | 0 |
| euclid_strong_lens_modeling_pipeline | 0 | 0 |

### Root cause: bidirectional copy-paste, not gradual drift

Each dead entry was attributed to the repo where its file actually lives:

- **HowToLens' list is a copy of autolens_workspace's.** 18 of its 28 dead
  entries (`gui/mask`, `cluster/modeling`, `mass_stellar_dark/slam`,
  `time_delays`, `hpc/example_cpu`,
  `imaging/features/advanced/subhalo/sensitivity/`, …) name real files that
  exist only in autolens_workspace. HowToLens contains nothing but
  `chapter_*/tutorial_*.py`, so none of those paths can ever exist there.
- **HowToGalaxy ← autogalaxy_workspace**, same mechanism, 11 of 15.
- **The copy went back the other way too:** autolens_workspace carries
  `tutorial_searches`, `tutorial_5_borders` and `tutorial_6_model_fit` —
  HowTo tutorial stems that cannot exist in a workspace.
- Only **3 of the 46 HowTo entries are live**: `tutorial_searches` (both) and
  `tutorial_5_borders` (HowToLens).

### One entry is an active silent failure, not cruft

`plot/visuals` (autolens_workspace + HowToLens), commented *"Bugged, but visuals
being refactored soon."* The file moved `scripts/plot/visuals.py` →
`scripts/guides/plot/examples/visuals.py` in commit `9e1a50dc4` (2025-07-18).
The pattern was never updated, so the skip stopped applying a year ago and the
script has been running in the build ever since. Deleting the entry is the wrong
fix — the pattern must be retested, then corrected or dropped on evidence.

`dataset/imaging/slacs1430+4105` is inert for a different reason: it points
outside `scripts/`, so the walker never sees it. Its own comment admits this.

### Siblings are contaminated the same way — 11 more dead entries

Same copy-paste mechanism, in `env_vars.yaml` / `env_vars_release.yaml`:

- **HowToLens**: `imaging/start_here`, `interferometer/start_here`,
  `group/start_here`, `multi/start_here`, `guides/results/` — autolens_workspace
  paths.
- **HowToGalaxy**: `guides/results/`.
- **HowToFit**: `plot/emcee_plotter`, `plot/zeus_plotter` — legacy, those
  scripts are gone.
- **autogalaxy_workspace_test**: `quantity/visualization.py` and
  `quantity/visualization_jax` (the latter in both env_vars files).

`markdown_examples.yaml` and `visualise_notebooks.yaml` are clean in every repo.

## Scope decisions already taken by the human

1. **Purge every zero-match entry**, including bare-stem prospective guards
   (`fits_make`, `png_make`, `data_fitting`, `deflections`, `examples/searches`).
   A guard for a script that does not exist is unverifiable and is exactly what
   produced this mess; if such a script is ever added the build fails loudly and
   the entry can be re-added with a real reason.
2. **`plot/visuals` gets tested, not guessed.** Run
   `scripts/guides/plot/examples/visuals.py` under the build env profile; if it
   passes, drop the entry as stale, if it still fails, re-add a correctly-spelled
   path entry with a fresh reason.

## Notes

- This closes the "~44 zero-match entries remain, needs a deliberate call before
  purging" item left open by the 2026-07-22 ell_comps/HowTo no_run sweep
  (autogalaxy_workspace#143, HowToGalaxy#34/#35, HowToLens#44).
- `tutorial_6_model_fit` (HowToLens + autolens_workspace) matches no file in any
  repo's history; it is deleted as part of the purge rather than repaired,
  since the intended target is unrecoverable.
- Config-only change. No script, notebook or library edits expected, beyond
  whatever the `plot/visuals` test verdict implies.

<!-- census performed in-session on 2026-07-23 before prompt creation -->

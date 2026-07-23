Purged every zero-match entry from the `config/build/` path-pattern configs across the
workspace and tutorial repos, after a full census of all 10 build targets. **50 of 122
`no_run.yaml` entries (41%) matched zero files**, plus 11 dead `env_vars.yaml` override
patterns. 5 PRs, all merged; 65/65 smoke scripts passed.

## PRs

| Repo | PR | Change | Smoke |
|---|---|---|---|
| HowToLens | #47 | `no_run` 30→2, `env_vars` 5→`[]` | 6/6 |
| HowToGalaxy | #37 | `no_run` 16→1, `env_vars` 1→`[]` | 4/4 |
| autolens_workspace | #319 | `no_run` 27→20 | 11/11 |
| HowToFit | #26 | `env_vars` 2→`[]` | 10/10 |
| autogalaxy_workspace_test | #82 | `env_vars` 2 + `env_vars_release` 1 | 34/34 |

Config-only: 8 files, zero script/notebook/library edits. Issue HowToLens#46.

## The finding: bidirectional copy-paste, not drift

The diagnostic that cracked it was **cross-repo attribution** — for each dead entry, find
the repo where its file actually lives. 18 of HowToLens' 28 dead entries name files existing
only in autolens_workspace; HowToGalaxy ← autogalaxy_workspace, 11 of 15; HowToFit's 2 dead
`env_vars` patterns came from autofit_workspace's `env_vars.yaml` lines 26/28, where the
identical patterns still live and still match. **And the copy went back** — autolens_workspace
carried three HowTo tutorial stems (`tutorial_searches`, `tutorial_5_borders`,
`tutorial_6_model_fit`). The HowTo repos contain only `chapter_*/tutorial_*.py`, so a
workspace path can never match there. Run cross-repo attribution before purging: it turns
"these are stale" into "these were copied", which is a different (and fixable) defect.

Not every dead entry shared that cause: autogalaxy_workspace_test's 3 came from commit
`49e53de` (2026-05-22), which deleted `scripts/quantity/` but missed its own config entries —
an incomplete removal.

Each cleaned file gained a header recording the matcher rule and that the list is repo-local
and must not be copied between repos. Without that, a purge just resets the clock.

## A zero-match entry is not always cruft

`plot/visuals` was an **active silent failure**. The file moved
`scripts/plot/visuals.py` → `scripts/guides/plot/examples/visuals.py` in `9e1a50dc4`
(2025-07-18) and the pattern was never updated, so a script commented *"Bugged, but visuals
being refactored soon"* had been **running in the build for a year**, not skipped. Tested it
under the real profile via `autobuild repro_command` rather than guessing — passes clean,
exit 0 — so the entry was dropped as stale rather than re-spelled to the moved path.
**A moved file turns a skip into a silent no-op; test before deleting OR re-spelling.**

## The verification that beat running the pipeline

Instead of `run_all` (~1h, and it only samples runtime), diff the **resolved state**: for all
532 scripts across the 5 repos, compute the `should_skip` set and the fully-resolved
`build_env_for_script` dict under the old config and the new. Byte-identical everywhere ⇒
provably behaviour-neutral, because every removed entry matched zero files. Strictly stronger
evidence than a test run, and minutes to compute. Reusable for any config purge.

## Traps

- **`overrides:` emptying to null.** `env_config.py:73` does `.get("overrides", [])`, which
  returns `None` — not `[]` — when the key exists but is empty; iteration then raises. Three
  repos lost all their overrides, so each got an explicit `overrides: []`. Same family as
  "comment-only YAML loads as None NOT `{}`".
- **Matcher semantics** (`PyAutoHands/autobuild/build_util.py:143` `should_skip`): entry with
  `/` = substring match against the full path *including extension*; entry without `/` =
  exact stem. `run_all` walks only `scripts/` (`run_all.py:78`).
- **The Heart RED gate was overridden by the human, not satisfied.** `ship_workspace` step 3
  said stop (score 0, 6 reasons; the task repaired none of them, so the corrective-PR
  exception did not apply). The concurrent rename session independently established that the
  RED was **largely stale evidence** — `release validation FAILED (stage integrate)` traced
  to run 29912642195, whose failures were fixed by autolens_workspace `f582fb7f5` merged 9h
  *after that run started*, and the "13 failed" reason was dated 2026-07-21, also pre-fix.
  Only manifest drift was live. **Before parking on RED, check whether the RED reasons predate
  the fixes that address them** — a stale verdict blocks real work.
- Ran concurrently with the parked `rename-autobuild-to-autohands` task, which claimed all 5
  repos. Approved after verifying the file sets were disjoint by grep. Separate branch and
  worktree; no collision.
- Brain Feature Agent scored this `too-large (19)` / split-into-phases. Overridden — the
  score is repo-count-driven and this was 8 YAML files with no code, API or docs surface.

## Scope decisions

Bare-stem prospective guards (`fits_make`, `png_make`, `data_fitting`, `deflections`,
`examples/searches`) were purged too: an unverifiable guard for a script that does not exist
is what produced the mess, and if such a script is ever added the build fails loudly and the
entry can be re-added with a real reason.

`tutorial_6_model_fit` was **deleted rather than repaired** — it matches no file in any repo's
history. `tutorial_8_model_fit.py` exists in HowToLens chapter_4 but the intended target was
unrecoverable.

## Left open

The clean repos are worth understanding: autolens_workspace_test has 23 entries and zero
dead, as do autogalaxy_workspace, autofit_workspace, the other two `_test` workspaces and the
euclid pipeline. Whatever discipline keeps them honest is what the HowTo repos lacked. Scope
was deliberately not widened to investigate.

Closes the "~44 zero-match entries remain, needs a deliberate call before purging" item left
open by the 2026-07-22 ell_comps/HowTo no_run sweep (autogalaxy_workspace#143,
HowToGalaxy#34/#35, HowToLens#44).

## Original prompt

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

Removed all three per-project config fallbacks from `PyAutoHands/autobuild/config/`,
making each workspace's `config/build/` the single source of truth. Started as a
one-file question about `copy_files.yaml`; the user asked mid-run to extend the
sweep to the HowTo\* and `_test` workspaces, which turned up two siblings — one of
them a live crash.

**9 PRs, all merged:** PyAutoHands#176 (the change), PyAutoBrain#149 (doc line),
PyAutoMind#94 (`spawn.py` seeds `no_run.yaml` instead), and 6 workspace deletions
(autofit_workspace#108, autogalaxy_workspace#145, autolens_workspace#316,
autofit_workspace_test#65, autogalaxy_workspace_test#80,
autolens_workspace_test#199).

## What was removed, and why each was dead

- **`copy_files.yaml`** — the copy-as-is mechanism, removed entirely. Every entry
  was stale or empty, so `is_copy_file()` was unconditionally `False`. The
  decisive proof was **zero `.py` files in any `notebooks/` tree** across all
  build targets: `generate.py` rmtree's `notebooks/` and rebuilds it, and
  copy-as-is was the only path that writes a `.py` there — so the feature had
  produced no output in any build.
- **`visualise_notebooks.yaml`** — a **comment-only husk**, so `yaml.safe_load`
  returned `None` and `run.py` called `None.get(project)` →
  `AttributeError`. This **crashed `autobuild run <target> --visualise`** for the
  four targets lacking their own file (HowToFit, HowToGalaxy, HowToLens, euclid).
  Reproduced on `main`, then fixed. `copy_files` used `.get(...) or []` and
  survived; this call site omitted the `or []` *after* the `.get`.
- **`no_run.yaml`** — unreachable (all 10 targets already owned one) but holding
  ~50 lines of stale duplicated skip rules that silently no-op'd when edited.

`workspaces.yaml` was kept: it is build *policy* (the run matrix), not config.

## Traps recorded

- **A comment-only YAML loads as `None`, not `{}`.** That is what made the
  visualise fallback a crash rather than a no-op.
- **There are TEN build targets, not 9** — `workspaces.yaml` also lists `euclid`
  → `euclid_strong_lens_modeling_pipeline`. Enumerate from `workspaces.yaml`,
  never from a directory listing. I initially missed it.
- **`run.py` now REQUIRES `config/build/no_run.yaml`** (raises
  `FileNotFoundError`). That is why `spawn.py` had to *swap* its emission to
  `no_run.yaml` rather than just drop `copy_files.yaml` — otherwise every newly
  spawned workspace would fail its first build.
- The two deleted precedence tests **never imported `generate.py`** — they
  re-implemented its if/else inline and asserted on their own fixture, testing a
  *copy* of the logic. No real coverage was lost.

## Verification

132/132 PyAutoHands tests pass on merged `main`. Behaviour-preservation was
proved empirically rather than assumed: regenerating `autofit_workspace` **and**
`HowToLens` (a target that genuinely used the deleted fallback) produced
byte-identical `notebooks/` trees versus `main`.

## Process note

The Brain Feature Agent scored this `too-large (25)` and proposed a 4-phase split
with a design phase. Overridden — the score tracked the 9-repo count, not
complexity (~13 lines of code removed), and the flagged "public-API ripple" risk
did not apply since `is_copy_file` was module-local and its branch provably never
taken. The standard 2-wave library-first split was the right shape.

## Original prompt

# Remove the dead copy_files.yaml build-config mechanism

Type: refactor
Target: PyAutoHands
Repos:
- PyAutoHands
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- autofit_workspace_test
- autogalaxy_workspace_test
- autolens_workspace_test
- PyAutoBrain
Difficulty: easy
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> Check if the copy_files.yaml config/build file is actually used anywhere (it
> may be in autofit_workspace, but this may also be legacy) and if not remove it
> or consider if we can remove it somewhere.
>
> Do B, but do one file deep dive to make sure its used nowhere

("B" = full removal of the feature, as opposed to "A" = purging only the stale
entries while keeping the mechanism.)

## Why

`copy_files.yaml` lists script paths that the notebook build copies verbatim
into `notebooks/` instead of converting to `.ipynb`. The mechanism is wired into
`PyAutoHands/autobuild/generate.py`, but it is **dead organism-wide**.

Deep-dive evidence (2026-07-23):

- **Every config entry is stale or empty.** `autofit_workspace` lists 3 paths
  (`howtofit/chapter_1_introduction/gaussian.py`, `profiles.py` ×2) that exist
  in no repo — the howtofit content moved to `HowToFit/`, and they are not there
  either. `autolens_workspace` lists
  `imaging/advanced/chaining/hyper_mode/extensions.py`; no `hyper_mode` directory
  exists at all. The other four workspace files are `[]`. The PyAutoHands
  fallback keyed dict has 4 keys (`howtogalaxy`, `howtolens`, `howtofit`,
  `BSc_Galaxies_Project`), **all null** — and `BSc_Galaxies_Project` is not even
  in the workspace.
- **`is_copy_file()` is therefore unconditionally `False`.**
- **Zero output artifacts.** No `.py` file exists in any `notebooks/` tree
  across all 9 build targets (the 6 workspaces + HowToFit/HowToGalaxy/HowToLens).
  Since `generate.py` `rmtree`s `notebooks/` and rebuilds it, and copy-as-is is
  the only path that writes a `.py` there, this proves the feature has produced
  nothing in any current build.
- **No consumer outside `generate.py`.** An exhaustive grep across all repos and
  file types (incl. `.yml`/`.sh`/`.toml`) found no CI workflow, release
  pipeline, packaging manifest, or second copy of `generate.py`. Every remaining
  hit is a comment, a test, a doc, or a historical PyAutoMind record.
- The HowTo\* repos have `config/build/` but no `copy_files.yaml`, so they take
  the fallback branch — which yields `[]`. The fallback branch, its precedence
  test, and the "not yet migrated" note in `bin/autobuild` all guard an empty
  dict.

This mirrors the already-completed removals of `notebooks_remove.yaml` and the
autobuild-level `env_vars.yaml`, which `test_dead_autobuild_files_removed`
guards.

## Scope

**PyAutoHands** (primary)

- `autobuild/generate.py` — remove the `copy_files.yaml` loader (the
  workspace/fallback precedence block) and `is_copy_file()`; collapse the
  `if is_copy_file(...)` branch so every script takes the convert path.
- Delete `autobuild/config/copy_files.yaml`.
- `bin/autobuild` — drop the `copy_files.yaml` rationale from `help_generate`.
- `docs/internals.md` — drop the `copy_files.yaml` bullet and its mention in the
  fallback paragraph.
- `tests/test_workspace_config_precedence.py` — delete
  `test_copy_files_workspace_wins` and
  `test_copy_files_falls_back_to_autobuild_keyed`; drop `copy_files.yaml` from
  the tuple in `test_actual_workspace_files_exist`; add it to
  `test_dead_autobuild_files_removed`.

**The 6 workspaces** — delete `config/build/copy_files.yaml`.

**PyAutoBrain** — `agents/conductors/build/BUILD_CAPABILITIES.md`: drop
`copy_files` from the per-workspace config list.

**PyAutoMind — DEFERRED to a follow-up task.** `scripts/spawn.py:523` emits
`autoproject_workspace/config/build/copy_files.yaml` into every spawned
workspace, and `docs/pyautobrain/spawn_spec.md:76` specifies it. Both must go,
but PyAutoMind is currently **claimed** by task
`arxiv-digest-strong-lensing-term` (branch
`feature/arxiv-digest-strong-lensing-term`, PR #93 open). File this as a small
follow-up once #93 merges. Until then spawn keeps seeding a config nothing
reads — harmless, since the reader is gone after this task.

## Phasing (decided 2026-07-23, overriding the Brain agent)

The Feature Agent scored this `too-large (25)` and proposed a 4-phase split
(design / core-api / workspace / docs). **Rejected by the user and by
inspection**: the score is driven by the 9-repo count, not by complexity — the
change is ~13 lines removed from one file plus 7 deletions and 4 doc/test edits,
and the "public-API ripple" risk does not apply (`is_copy_file` is module-local
to `generate.py` and its branch is provably never taken). Structure instead as
the standard library-first split:

- **PR 1** — PyAutoHands (+ the one PyAutoBrain doc line).
- **PR 2** — the 6 workspace `copy_files.yaml` deletions, merged after PR 1.

## Guardrails

- **Keep the `<project>` argument** to `autobuild generate`. Its help text
  justifies it via `copy_files.yaml`, but `project` is genuinely still used for
  `build_util.inject_colab_setup`. Only the help text changes.
- **`copy_to_notebooks()` stays** — it is not part of the dead surface. The
  normal conversion path and the `.rst`/`.md` sweeps both call it.
- **Leave `PyAutoMind/complete/**` records untouched.** They are a historical
  ledger; several record the original seeding of these configs.
- Behaviour-preserving by construction: the removed branch was never taken.
  Verify by running `autobuild generate` for one workspace before and after and
  diffing the produced `notebooks/` tree.
- Ship PyAutoHands first, then the workspace deletions, per the library-first
  merge gate.

<!-- filed by hand from a CLI deep dive on 2026-07-23; evidence recorded above -->

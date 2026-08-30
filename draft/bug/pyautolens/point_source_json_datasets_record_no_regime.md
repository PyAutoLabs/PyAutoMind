# Point-source JSON datasets record no resolution regime

Type: bug
Target: pyautolens
Repos:
- @PyAutoLens
- @PyAutoArray
- @PyAutoNerves
Themes:
- point-source
- ci-smoke
Difficulty: medium
Autonomy: supervised
Priority: low
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-08-22 (backfilled from git)

Split out of PyAutoNerves#153 on 2026-08-22, which stamped the small-datasets
regime into every FITS the stack writes and deliberately left the JSON side
alone. This is that leftover, scoped down to what the evidence actually
supports.

## What is exposed

Exactly **one** dataset directory: `dataset/point_source/multiple_sources`. It
is regime-dependent and writes no FITS — only `point_dataset_*.json` plus a
`point_datasets.csv` (`autonerves/csvable.py:21 output_to_csv`, written at
`multiple_sources/simulator.py:257`). A capped run and a full run therefore
leave indistinguishable files, and `should_simulate` degenerates to
existence-only there.

That is 5 of 268 `should_simulate` call sites, and `point_datasets.csv` is a
third on-disk dataset representation that neither the FITS stamp nor any JSON
stamp currently reaches.

## Why it was deferred rather than fixed

Two facts made it cost-free to defer. **Both expire** — do not re-derive them,
re-check them:

1. `dataset/point_source/multiple_sources` is excluded from harness execution by
   `config/build/no_run.yaml:41-42`, blocked on **PyAutoLens#480**. When #480
   lands the script runs again and the exposure goes live. *This is the trigger
   for doing this work.*
2. `dataset/weak/simple` — the other FITS-less directory, and the one the
   original issue named — is regime-**invariant**. Its script uses
   `via_tracer_from`, not `via_tracer_random_positions_from`
   (`autolens/weak/simulator.py:118` vs `:140-142`), and nothing in that path
   reads `PYAUTO_SMALL_DATASETS`. There is no bug to fix. Anyone switching that
   script to the random-positions helper reintroduces regime dependence with
   nothing to catch it.

Note the issue text this came from claimed point-source datasets are "JSON with
no FITS". That is wrong: ordinary point-source datasets write a top-level
`data.fits` and are already covered. Only `multiple_sources` is not.

## Constraints on any fix (verified, do not rediscover)

- **In-payload stamping is survivable, but only at the top level.** An unknown
  key alongside `type`/`class_path`/`arguments` is silently ignored by both
  `autonerves.dictable.from_dict` and autofit's `ModelObject.from_dict`
  (`assertions` is the existing precedent). A key *inside* `arguments` reaches
  `cls(**arguments)` and raises `TypeError`, breaking every existing on-disk
  JSON dataset's load path.
- **A generic stamp in `output_to_json` is the wrong shape.** Of 146 non-test
  call sites only 18 serialise a dataset; ~88% are tracers, galaxies and
  position lists with no resolution regime to record. Stamping the funnel would
  attach a meaningless marker to thousands of model files per run in autofit
  search-output directories.
- **A sidecar must not use a `.json`, `.pickle`, `.csv` or `.fits` suffix.**
  `autofit/aggregator/search_output.py:88-97` rglobs search-output directories
  admitting exactly those four, so a `*.json` sidecar becomes a spurious
  aggregator entry in every result loaded from a search that wrote any JSON.
- **`to_dict` can return a bare scalar**, so any in-payload stamp needs an
  `isinstance(payload, dict)` guard or it silently no-ops.
- **The read side has no file to key on.** `multiple_sources` offers only
  `point_dataset_*.json` (a glob) or `tracer.json` (not unique to the family).
  A glob in a predicate ending in `shutil.rmtree` is explicitly forbidden by the
  `autolens_workspace_test#260` traps. This needs a naming-convention decision
  first, and that decision is the real work here.

## Re-check log

**2026-08-23 — both facts re-verified, STILL BLOCKED. Do not build.**
Checked at the top of a `/start_dev` run; the gate in step 1 below said re-park,
so nothing was built, no issue was opened and no branch was cut.

1. **PyAutoLens#480 is still open.** Created 2026-04-28, `updated_at` identical
   to `created_at`, no assignees, `closed_by_pull_requests: 0`. Untouched in
   ~4 months.
2. **`weak/simple` is still regime-invariant.** Its simulator calls
   `simulator.via_tracer_from(tracer=tracer, grid=positions, name=dataset_name)`
   over an explicit 1500-galaxy annulus with `np.random.default_rng(1)`. It does
   not call `via_tracer_random_positions_from`, and the file contains no
   `os.environ` read at all, so nothing reads `PYAUTO_SMALL_DATASETS`.

Two path corrections found while re-checking — the originals below cost a search,
so they are fixed here rather than left to bite again:

- The `no_run.yaml` exclusion is in **@autolens_workspace**, not
  autolens_workspace_test (whose `config/build/no_run.yaml` has no
  `multiple_sources` entry at all). Line numbers omitted deliberately: the
  original `:41-42` had already drifted. Match on the entries themselves —

  ```
  - point_source/features/multiple_sources/simulator # Blocked by PyAutoLens #480: solver finds 0 positions for intermediate-plane source
  - point_source/features/multiple_sources/modeling # Blocked by PyAutoLens #480: same root cause as simulator above
  ```

  Note this is **two** skipped scripts, simulator *and* modeling, not one.
- The script path is `scripts/point_source/features/multiple_sources/`, not
  `dataset/point_source/multiple_sources` (that is the *output* directory).
  Likewise the weak simulator is `scripts/weak/simulator.py` in
  @autolens_workspace.

**2026-08-27 — both facts re-verified, STILL BLOCKED. Do not build.**
Second gate check in four days, same verdict: no issue was opened, no branch was
cut, no worktree claimed.

1. **PyAutoLens#480 is still open.** `updated_at` is still byte-identical to
   `created_at` (2026-04-28T21:01:57Z) — not one edit, comment, label or
   assignment since it was filed; still no assignees, still
   `closed_by_pull_requests: 0`. Four months untouched.
2. **`weak/simple` is still regime-invariant.** `scripts/weak/simulator.py:122`
   still calls `simulator.via_tracer_from(tracer=tracer, grid=positions,
   name=dataset_name)`, and the file still contains no `os.environ` read of any
   kind. Its last commit is 2026-07-27, i.e. it has not moved since the previous
   re-check either.

The `no_run.yaml` entries happen to sit at `config/build/no_run.yaml:41-42` in
@autolens_workspace again, matching the original citation the 2026-08-23 note
found drifted. That is coincidence, not a reason to trust line numbers — keep
matching on the entry text.

One standing risk the previous note did not record (it predates that note; the
file has not changed since 2026-07-27, so this is an omission, not a change):
`weak/simulator.py` *advertises* the helper that would break fact 2. Its prose
blocks at `:94-95` and `:116-117` name
`via_tracer_random_positions_from(tracer=..., n_galaxies=..., grid_extent=...)`
as the "quick uniform-square catalogue" alternative to the explicit annulus this
script passes. So the invariant is one plausible simplification away from being
reversed, with nothing in the suite to catch it. Not a reason to build now — but
if fact 2 ever expires, that is the likely route.

**2026-08-27 (later the same day) — THE TRIGGER HAS FIRED. #480 is fixed and closed.**

PyAutoLens#480 was fixed in PyAutoLabs/PyAutoLens#712 (merged `c1bba66`) and closed,
hours after the re-check above recorded it as still open. The record is
`complete/2026/08/point-solver-magnification-plane-redshift.md`.

**This does not make the task actionable yet, and the distinction matters.** The gate
named in "Why it was deferred" is not #480 itself — it is the `no_run.yaml` exclusion,
which #480 was only the *reason* for. That exclusion is in @autolens_workspace and is
untouched: both `point_source/features/multiple_sources/{simulator,modeling}` are still
skipped, so the script still does not run and the exposure is still not live. What
changed is that the blocker behind the exclusion is gone, so removing it is now
possible where before it would have failed.

The remaining chain, in order:

1. @autolens_workspace: revert the multi-source example to a richer multi-plane
   configuration (#480's own text asks for this — the example was simplified to work
   around the bug) and remove the two `multiple_sources` entries from
   `config/build/no_run.yaml`. **That work is already filed**, as
   `draft/feature/workspaces/restore_multiple_sources_lensing_of_lens.md` (unblocked
   2026-08-27); its step 7 is the `no_run.yaml` removal this prompt waits on. Do not
   file a duplicate.
2. Then the script runs, `dataset/point_source/multiple_sources` is written for real,
   and this prompt's exposure goes live — at which point steps 2-4 of "Suggested scope"
   below are the actual work.

So the next re-check trigger is no longer #480. **It is the `no_run.yaml` entries
disappearing from @autolens_workspace.** Re-check by grepping that file for
`multiple_sources`; if the entries are gone, build.

Fact 2 is unchanged and remains a standing invariant: `weak/simple` still uses
`via_tracer_from`, and only breaks if someone switches `weak/simulator.py` to the
random-positions helper.

## Suggested scope

1. Re-check both expiring facts above. If #480 is still open and `weak/simple`
   still uses `via_tracer_from`, this task is still not worth doing — say so and
   re-park it rather than building.
2. Decide the read-side naming convention. Without it there is nothing to build.
3. Then choose in-payload top-level key vs non-colliding sidecar, honouring the
   constraints above.
4. Cover `point_datasets.csv` in whatever is chosen, or state why not.

<!-- Sizing: medium. The code is small; the naming-convention decision is the task. -->

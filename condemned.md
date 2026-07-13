# Condemned material

The catalog of **condemned self-material** — stale branches, `git stash`
entries, dead code and retired tests that a hygiene / `repo_cleanup` sweep is
95%-but-not-100% sure is trash. Symmetric to `parked.md`: `parked.md` holds work
that is *paused and will resume*; this file holds material that is *spent and
awaiting elimination*, recoverable right up until it is voided.

This is the **index**; the payload is durable **git refs**, not markdown. Fragile
forms (local unmerged branches, stashes) are first materialised as real commits
and pushed under the archive namespace `refs/heads/archive/condemned/<name>`
(a branch prefix — GitHub only accepts pushes to `refs/heads/*` and
`refs/tags/*`, so a custom `refs/archive/*` namespace is unpushable; filter with
`git branch --list 'archive/condemned/*'`) into **PyAutoGut** as the attic remote
— *before* the local copy is deleted. Recovery is a checkout. The organ (PyAutoGut) holds
and voids; the Brain hygiene conductor drives (decides what to condemn, triggers
a sweep), mirroring the Heart ↔ vitals template. See the decision:
`research/pyautobrain/pyautogut_organ_decision.md`.

## Lifecycle

1. **Condemn** — the hygiene `tidy` pass files an entry here (async, no
   synchronous per-item gate). Fragile forms are archived to a durable ref
   first; merged branches and committed deletions need only a SHA recorded.
2. **Transit** — the entry sits with a `sweep-after` date. Until then it is
   recoverable (reabsorption): restore the branch/stash from its archive ref.
3. **Void** — a batch `sweep` runs the existing `repo_cleanup` safety gates
   against entries past `sweep-after` and eliminates them; the entry moves out
   of this file (to a voided log or is deleted).

## Entry schema

One `##` block per item. Fields:

- `type` — `branch` | `stash` | `file` | `test`
- `locator` — the local name/path (e.g. `feature/old-thing`,
  `stash@{2}`, `src/legacy/foo.py`)
- `confidence` — how sure it is trash (e.g. `0.95`)
- `reason` — why it is condemned
- `merged` — `yes` | `no` (a merged branch is reachable from `main` forever →
  skips the pen; near-zero risk)
- `condemned` — date filed (YYYY-MM-DD)
- `sweep-after` — earliest date it may be voided (the transit clock)
- `breaks-if-wrong` — what is lost if this was a false positive (informs the
  gate)
- `archive-ref` — the durable ref + SHA to recover from
  (`refs/heads/archive/condemned/<name>` @ `<sha>`), or `n/a` for a merged branch /
  committed deletion whose bytes live in remote history (record the pre-delete
  SHA instead)

### Recoverability is not uniform

- **Merged branches** — reachable from `main` forever; `archive-ref: n/a`, a note
  is enough. The conductor recommends these straight to deletion without staging.
- **Committed code / test deletions** — the old bytes live in remote history;
  record only the pre-delete SHA.
- **Local-only unmerged branches / stashes** — exist in one machine's reflog and
  are gc-pruned. These **must** be materialised as an archive ref before deletion;
  a manifest that merely *points* at a stash is worthless the moment it is dropped.

<!-- Example entry (schema illustration only — not a live condemnation):

## feature/abandoned-spike
- type: branch
- locator: feature/abandoned-spike
- confidence: 0.95
- reason: superseded by feature/real-approach; no unique commits worth keeping
- merged: no
- condemned: 2026-07-12
- sweep-after: 2026-08-12
- breaks-if-wrong: loses ~3 exploratory commits (delaunay prototype)
- archive-ref: refs/heads/archive/condemned/abandoned-spike @ 0de4514
-->

## release-datasets/autolens-regenerable
- type: file
- locator: autolens_workspace dataset/ (19 non-allowlisted simulated dirs — category A + multi): group/{dark_matter_subhalo,operated,simple,simple__no_lens_light,sky_background}, imaging/{dark_matter_subhalo,extra_galaxies,lens_light_asymmetric,light_operated,simple,simple__no_lens_light,sky_background}, interferometer/{extra_galaxies,simple}, point_source/{deblending,simple}, weak/simple, multi/{imaging,interferometer}
- confidence: 0.98
- reason: force-committed by pre_build's old `git add -f` (fixed PyAutoBuild#150); each is regenerated on demand by a guarded example script (`should_simulate()`/`not dataset_path.exists()` → simulator subprocess). Removing from tracking so the tree matches `.gitignore`. #126 leg 3.
- merged: no
- condemned: 2026-07-13
- sweep-after: 2026-08-13
- breaks-if-wrong: a consumer that does not self-provision would hit missing data at runtime; smoke (9/9) confirms the example entries regenerate post-purge
- archive-ref: n/a — committed deletion; bytes recoverable from remote history at pre-purge SHA `8625a1de` (autolens_workspace) via `git checkout 8625a1de -- dataset/<dir>`

## release-datasets/autogalaxy-regenerable
- type: file
- locator: autogalaxy_workspace dataset/ (13 non-allowlisted simulated dirs — category A + multi): imaging/{asymmetric,clumpy,extra_galaxies,operated,sersic_x2,simple,simple__sersic,sky_background}, interferometer/{clumpy,extra_galaxies,simple}, multi/{imaging,interferometer}
- confidence: 0.98
- reason: as above (#126 leg 3); regenerated on demand by guarded example scripts.
- merged: no
- condemned: 2026-07-13
- sweep-after: 2026-08-13
- breaks-if-wrong: as above; smoke (8/8) confirms regeneration post-purge
- archive-ref: n/a — committed deletion; bytes recoverable from remote history at pre-purge SHA `e940f8cd` (autogalaxy_workspace)

<!-- Remaining non-allowlisted dirs (deferred, see PyAutoBuild#126): regenerable-but-not-smoke-covered (imaging/simulated_lens, interferometer/simulated_lens, point_source/simulated_lens, imaging/simulated_galaxy, interferometer/simulated_galaxy, imaging/dark_matter_subhalo_no_lens_light, point_source/start_here_example, imaging/ellipse); genuinely-dead → archive-ref then purge (cluster/csv_api_example, imaging/misc, imaging/samples, point_source/samples, interferometer/many_visibilities, interferometer/simpleold); needs-human (interferometer/datacube nested-real; database/simple__{0,1,2} → Group B committed-by-design). -->

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
`complete/2026/07/pyautogut-organ-decision.md`.

<!-- toc:start -->

**Contents**

- [Lifecycle](#lifecycle)
- [Entry schema](#entry-schema)
- [feature/abandoned-spike](#featureabandoned-spike)
- [release-datasets/autolens-regenerable](#release-datasetsautolens-regenerable)
- [release-datasets/autogalaxy-regenerable](#release-datasetsautogalaxy-regenerable)
- [release-datasets-group-b/all-four](#release-datasets-group-ball-four)
- [pj011646-wfc3-parity/superseded-branch](#pj011646-wfc3-paritysuperseded-branch)
- [release-datasets/autolens-regenerable-leg2](#release-datasetsautolens-regenerable-leg2)
- [release-datasets/autogalaxy-database-orphans](#release-datasetsautogalaxy-database-orphans)
- [release-datasets/autolens-many-visibilities](#release-datasetsautolens-many-visibilities)
- [history-rewrite-2026-07-27-addendum](#history-rewrite-2026-07-27-addendum)
- [release-datasets/autocti-imaging-ci](#release-datasetsautocti-imaging-ci)
- [release-datasets/autocti-dataset-1d-overview](#release-datasetsautocti-dataset-1d-overview)
- [pyautogalaxy/docs-cite-prodigy](#pyautogalaxydocs-cite-prodigy)
- [pyautolens/docs-cite-prodigy](#pyautolensdocs-cite-prodigy)
- [pyautobrain/release-accept-red-override](#pyautobrainrelease-accept-red-override)
- [pyautobrain/stash-remove-pulse-compat](#pyautobrainstash-remove-pulse-compat)
- [pyautoheart/autonerves-verify-install](#pyautoheartautonerves-verify-install)
- [pyautomind/lifecycle-record-auto-index](#pyautomindlifecycle-record-auto-index)
- [pyautomind/morning-status-workflow](#pyautomindmorning-status-workflow)
- [potential-correction-validation-artifacts](#potential-correction-validation-artifacts)
- [pyautomind/stash-pre-sync-2026-07-06](#pyautomindstash-pre-sync-2026-07-06)
- [pyautohands/pre-2023-history](#pyautohandspre-2023-history)
- [pyautomind/claude-session-branches-2026-08-26-batch](#pyautomindclaude-session-branches-2026-08-26-batch)
- [pyautohands/2022-era-feature-branches](#pyautohands2022-era-feature-branches)
- [autolens_profiling/jax-optimizer-tuning](#autolens_profilingjax-optimizer-tuning)
- [autolens_profiling/multiband-compile-ab](#autolens_profilingmultiband-compile-ab)
- [autolens_profiling/stash-strip-non-jit-noise](#autolens_profilingstash-strip-non-jit-noise)
- [autolens_workspace_developer/rectangular-spline-rotated-experiments](#autolens_workspace_developerrectangular-spline-rotated-experiments)
- [autolens_profiling/inference-programme-ledger](#autolens_profilinginference-programme-ledger)

<!-- toc:end -->

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
- locator: autolens_workspace dataset/ (28 non-allowlisted simulated dirs, PR#272) — cat A+multi: group/{dark_matter_subhalo,operated,simple,simple__no_lens_light,sky_background}, imaging/{dark_matter_subhalo,extra_galaxies,lens_light_asymmetric,light_operated,simple,simple__no_lens_light,sky_background}, interferometer/{extra_galaxies,simple}, point_source/{deblending,simple}, weak/simple, multi/{imaging,interferometer}; + producer-output/guarded: cluster/csv_api_example, imaging/{dark_matter_subhalo_no_lens_light,misc,simulated_lens}, interferometer/{datacube,simulated_lens}, point_source/{simulated_lens,start_here_example}; + simpleold (dead, user-confirmed kill)
- confidence: 0.98 (0.90 for interferometer/simpleold — dead)
- reason: force-committed by pre_build's old `git add -f` (fixed PyAutoBuild#150); each is regenerated on demand by a guarded example script (`should_simulate()`/`not dataset_path.exists()` → simulator subprocess) or is scratch script-output with no consumer. simpleold is a stale old dataset with zero references. Removing from tracking so the tree matches `.gitignore`. #126 leg 3.
- merged: no
- condemned: 2026-07-13
- sweep-after: 2026-08-13
- breaks-if-wrong: a consumer that does not self-provision would hit missing data at runtime; smoke (9/9) confirms the example entries regenerate post-purge; datacube/ellipse have guarded consumers; producer-output dirs have no consumer
- archive-ref: n/a — committed deletion; bytes recoverable from remote history at pre-purge SHA `8625a1de` (autolens_workspace) via `git checkout 8625a1de -- dataset/<dir>`

## release-datasets/autogalaxy-regenerable
- type: file
- locator: autogalaxy_workspace dataset/ (17 non-allowlisted simulated dirs, PR#129) — cat A+multi: imaging/{asymmetric,clumpy,extra_galaxies,operated,sersic_x2,simple,simple__sersic,sky_background}, interferometer/{clumpy,extra_galaxies,simple}, multi/{imaging,interferometer}; + producer-output/guarded: imaging/{ellipse,misc,simulated_galaxy}, interferometer/simulated_galaxy
- confidence: 0.98
- reason: as above (#126 leg 3); regenerated on demand by guarded example scripts or scratch script-output.
- merged: no
- condemned: 2026-07-13
- sweep-after: 2026-08-13
- breaks-if-wrong: as above; smoke (8/8) confirms regeneration post-purge
- archive-ref: n/a — committed deletion; bytes recoverable from remote history at pre-purge SHA `e940f8cd` (autogalaxy_workspace)

<!-- Group A (#126) COMPLETE + MERGED 2026-07-13. KEPT (allowlisted, not condemned):
     interferometer/many_visibilities (autolens, active); database/simple__{0,1,2} (autogalaxy,
     committed-by-design aggregator). los_halos .npy+.fits were simulator-output → purged. -->

## release-datasets-group-b/all-four
- type: file
- locator: bare-`dataset/` Group B repos (PyAutoBuild#151) — autofit_workspace (408 files, dataset/example_1d/**), HowToFit (408, example_1d/**), HowToGalaxy (21, imaging/**), HowToLens (27, imaging/**). Full `dataset/` purge — nothing real was committed.
- confidence: 0.98
- reason: force-committed by pre_build's old `git add -f` (fixed PyAutoBuild#150). All four repos self-provision every dataset via `if not dataset_path.exists(): subprocess.run([sys.executable, ".../simulator(s).py"])` (autofit/HowToFit `path.exists()`+`from_json`; HowToGalaxy/HowToLens `dataset_path.exists()`+`from_fits`). Bare `dataset/` intent = nothing committed. #151.
- merged: no
- condemned: 2026-07-13
- sweep-after: 2026-08-13
- breaks-if-wrong: a non-self-provisioning script would hit missing data; smoke confirms regeneration (autofit 10/10, HowToFit 10/10, HowToGalaxy 4/4, HowToLens 6/6)
- archive-ref: n/a — committed deletion; bytes recoverable from remote history at pre-purge SHAs autofit_workspace `1254a2fe`, HowToFit `ccc19584`, HowToGalaxy `caf1657c`, HowToLens `554be8b4`

## pj011646-wfc3-parity/superseded-branch
- type: branch
- locator: feature/pj011646-wfc3-parity (PyAutoReduce, tip bd9806b) — scripts/reduce_pj011646.py (wfc3_ir production reduction) + prototypes/pj011646_parity_fit.py (model-parity fit); PyAutoReduce#25.
- confidence: 0.9
- reason: superseded — the human is redoing the PJ011646 WFC3-IR reduction fresh via a new autolens-assistant approach (not the PyAutoReduce prototype path). Branch never pushed / no PR; pixel-parity verdict already captured on #25 (closed superseded). Kept recoverable in case the fresh redo wants the reduction/fit scripts as reference.
- merged: no
- condemned: 2026-07-13
- sweep-after: 2026-10-11
- breaks-if-wrong: loses the working wfc3_ir reduction script (program 14653, F160W, final_bits=512 workaround) + the model-parity fit harness; recoverable via `pyauto-gut recover pj011646-wfc3-parity` until voided.
- archive-ref: refs/heads/archive/condemned/pj011646-wfc3-parity on PyAutoReduce origin (bd9806b)

## release-datasets/autolens-regenerable-leg2
- type: file
- locator: autolens_workspace dataset/ (7 committed simulated dirs, PR#353) — cluster/simple, imaging/{mass_stellar_dark,double_einstein_ring,extra_and_scaling_galaxies}, group/{mass_stellar_dark,double_einstein_ring,scaling_relation}
- confidence: 0.98
- reason: committed simulated data (~17 MB) each regenerated on demand by a guarded consumer running its paired simulator; regeneration proven from a clean tree for all 7 before purge (issue #352). .gitignore allowlist re-includes dropped in the same commit; interferometer/uv_wavelengths deliberately kept (real SMA input, no writer). #126 purge series leg (prior: PR#272).
- merged: no
- condemned: 2026-07-27
- sweep-after: 2026-08-27
- breaks-if-wrong: loses the exact historical noise realizations of the 7 datasets (regenerated copies use fresh noise); recoverable from remote history via the pre-purge SHA
- archive-ref: n/a — committed deletion; pre-purge SHA 0bb170c57 VOIDED by the 2026-07-27 leg-7 history rewrite — bytes recoverable ONLY from the local mirror backup ~/Code/PyAutoLabs-backups/autolens_workspace-pre-rewrite-2026-07-27.git

## release-datasets/autogalaxy-database-orphans
- type: file
- locator: autogalaxy_workspace dataset/database/simple__{0,1,2} + scripts/guides/results/database/simulators/light_sersic_exp__{0,1,2}.py (PR#170)
- confidence: 0.98
- reason: orphaned committed simulated data (512 KB) — no commit in repo history ever contained a reader of dataset/database/ (the database guide reads dataset/imaging/*; "database" is its output namespace, matching the autolens sibling guide). The 2026-07-13 allowlist call (#126 Group B "committed-by-design aggregator data") rested on a stale prose line fixed in the same PR. Simulators deleted with their output: unconsumed, and their absence from no_run.yaml made every build re-run them (dataset byte-churn commits 34ddb66d/10a1ee64/e942d360). Dataset-bulk series leg 2 (issue #169).
- merged: no
- condemned: 2026-07-27
- sweep-after: 2026-08-27
- breaks-if-wrong: loses the exact historical noise realizations + the 3 simulator scripts; both recoverable from remote history at the recover point
- archive-ref: n/a — committed deletion; SHAs e942d360/5632f6d0 VOIDED by the 2026-07-27 leg-7 history rewrite — bytes (incl. the 3 deleted light_sersic_exp simulators, the one non-regenerable item) recoverable ONLY from ~/Code/PyAutoLabs-backups/autogalaxy_workspace-pre-rewrite-2026-07-27.git

## release-datasets/autolens-many-visibilities
- type: file
- locator: autolens_workspace dataset/interferometer/many_visibilities (PR#356)
- confidence: 0.98
- reason: force-committed in a single 2026-05-14 "pre build" add and never referenced — no script writes or loads it (all 9 name mentions are prose pointing at the many_visibilities_preparation example, which reads interferometer/simple); FITS files are 8,640-byte test-resolution stubs, 1.6 of 1.64 MB is render PNGs. Dataset-bulk series follow-on, user-confirmed kill.
- merged: no
- condemned: 2026-07-27
- sweep-after: 2026-08-27
- breaks-if-wrong: loses nothing unique — stubs + renders, recoverable from remote history
- archive-ref: n/a — committed deletion; pre-purge SHA 7f6ba9954 VOIDED by the 2026-07-27 leg-7 history rewrite — bytes recoverable ONLY from ~/Code/PyAutoLabs-backups/autolens_workspace-pre-rewrite-2026-07-27.git

## history-rewrite-2026-07-27-addendum
- type: file
- locator: autolens_workspace + autogalaxy_workspace + autofit_workspace — ALL pre-rewrite remote history
- confidence: 1.0 (human-authorized leg-7 rewrite, dataset-bulk series)
- reason: git filter-repo removed dead-at-HEAD blobs (purged datasets, historical output/, old howtolens/ tree, etc.); clones now 32/6/98 MiB (were 107/27/310). Every condemned entry pointing at "remote history" SHAs of these three repos (incl. release-datasets/autolens-regenerable @8625a1de, release-datasets/autogalaxy-regenerable @e940f8cd, and the autofit_workspace SHA 1254a2fe of release-datasets-group-b/all-four — the three HowTo SHAs of that entry survive, HowTo repos were NOT rewritten) is void on the remote.
- merged: n/a
- condemned: 2026-07-27
- sweep-after: never — the backups below are the permanent recover path
- breaks-if-wrong: nothing further; the rewrite already happened (HEAD trees verified byte-identical, tags preserved by name)
- archive-ref: permanent local mirror backups ~/Code/PyAutoLabs-backups/{autolens,autogalaxy,autofit}_workspace-pre-rewrite-2026-07-27.git (fsck-verified; old main SHAs 6be18d0cf / f0efa50a9 / 277164bc5)

## release-datasets/autocti-imaging-ci
- type: file
- locator: autocti_workspace dataset/imaging_ci/{simple,bias_uncorrected,cosmic_rays,non_uniform,parallel_x2__serial_x2,serial_cti} (200 files, 120.2 MB, PR#12)
- confidence: 0.98
- reason: committed simulated CTI calibration data, each regenerated in ~10 s by its sole write-site simulator under scripts/imaging_ci/simulators/**; clean-tree regeneration proven per dataset pre-purge and end-to-end post-merge (92 MB rebuilt from empty with a clean git status). Dataset-bulk series leg 6 (issue #11).
- merged: no
- condemned: 2026-07-27
- sweep-after: 2026-08-27
- breaks-if-wrong: loses the exact historical noise realizations only; regenerated copies are equivalent by construction
- archive-ref: n/a — committed deletion; pre-purge SHA 272bae3 VOIDED by the 2026-07-27 leg-7 autocti rewrite — bytes recoverable ONLY from the local mirror backup ~/Code/PyAutoLabs-backups/autocti_workspace-pre-rewrite-2026-07-27.git

## release-datasets/autocti-dataset-1d-overview
- type: file
- locator: autocti_workspace dataset/dataset_1d/{simple,species_x1_continuum_0,species_x3,temporal} + dataset/overview/{dataset_1d,imaging_ci}/ (282 files, 5.35 MB, PR#18)
- confidence: 0.98
- reason: committed simulated 1D CTI calibration + overview datasets, each regenerated in seconds by its sole write-site simulator (scripts/dataset_1d/simulators/** and scripts/imaging_ci/simulators/overview/calibrate.py); clean-tree regeneration proven per dataset pre-purge and re-witnessed post-purge with clean git status; 21 auto-simulate guards added to 18 consumers. The dataset-bulk leftover recorded in complete/2026/08/autocti-util-dataset-export.md. The 5 non-simulated overview media files (ccd.gif, ccd_schematic.png, cti.gif, cti_time_evolution.png, what_is_cti.png) stay committed — no write site.
- merged: no
- condemned: 2026-08-07
- sweep-after: 2026-09-07
- breaks-if-wrong: loses the exact historical noise realizations only; regenerated copies are equivalent by construction
- archive-ref: n/a — committed deletion; pre-purge SHA 50b701d on autocti_workspace main (post-rewrite history — reachable on the remote)

## pyautogalaxy/docs-cite-prodigy
- type: branch
- locator: docs/cite-prodigy (PyAutoGalaxy, tip e06a527)
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged as a stale local unmerged branch (not the default branch, no unique work in flight) in the PyAutoGalaxy checkout. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses whatever cite-prodigy docs drafting the branch held; recoverable via `pyauto-gut recover pyautogalaxy-docs-cite-prodigy` until voided.
- archive-ref: refs/heads/archive/condemned/pyautogalaxy-docs-cite-prodigy on PyAutoGalaxy origin (e06a527)

## pyautolens/docs-cite-prodigy
- type: branch
- locator: docs/cite-prodigy (PyAutoLens, tip 03ad3f8)
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged as a stale local unmerged branch (not the default branch, no unique work in flight) in the PyAutoLens checkout. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses whatever cite-prodigy docs drafting the branch held; recoverable via `pyauto-gut recover pyautolens-docs-cite-prodigy` until voided.
- archive-ref: refs/heads/archive/condemned/pyautolens-docs-cite-prodigy on PyAutoLens origin (03ad3f8)

## pyautobrain/release-accept-red-override
- type: branch
- locator: feature/release-accept-red-override (PyAutoBrain, tip 29105d9)
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged as a stale local unmerged branch in the PyAutoBrain checkout. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses the release-accept-red-override prototype work; recoverable via `pyauto-gut recover pyautobrain-feature-release-accept-red-override` until voided.
- archive-ref: refs/heads/archive/condemned/pyautobrain-feature-release-accept-red-override on PyAutoBrain origin (29105d9)

## pyautobrain/stash-remove-pulse-compat
- type: stash
- locator: stash@{0} (PyAutoBrain) — "On remove-pulse-compat: preserve feature/remove-pulse-compat before PyAutoHeart issue 27"
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged a stale local stash in the PyAutoBrain checkout. Materialised to a branch (`git branch <tmp> stash@{0}`, non-destructive — no apply/pop) before archiving, then dropped. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses the preserved remove-pulse-compat WIP; recoverable via `pyauto-gut recover pyautobrain-stash--0-` until voided.
- archive-ref: refs/heads/archive/condemned/pyautobrain-stash--0- on PyAutoBrain origin (ff1af88)

## pyautoheart/autonerves-verify-install
- type: branch
- locator: feature/autonerves-verify-install (PyAutoHeart, tip 2a1f276)
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged as a stale local unmerged branch in the PyAutoHeart checkout. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses the autonerves-verify-install prototype work; recoverable via `pyauto-gut recover pyautoheart-feature-autonerves-verify-install` until voided.
- archive-ref: refs/heads/archive/condemned/pyautoheart-feature-autonerves-verify-install on PyAutoHeart origin (2a1f276)

## pyautomind/lifecycle-record-auto-index
- type: branch
- locator: feature/lifecycle-record-auto-index (PyAutoMind, tip 4b06f15)
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged as a stale local unmerged branch in the PyAutoMind checkout. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses the lifecycle-record-auto-index prototype work; recoverable via `pyauto-gut recover pyautomind-feature-lifecycle-record-auto-index` until voided.
- archive-ref: refs/heads/archive/condemned/pyautomind-feature-lifecycle-record-auto-index on PyAutoMind origin (4b06f15)

## pyautomind/morning-status-workflow
- type: branch
- locator: feature/morning-status-workflow (PyAutoMind, tip 13ecca7)
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged as a stale local unmerged branch in the PyAutoMind checkout. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses the morning-status-workflow prototype work; recoverable via `pyauto-gut recover pyautomind-feature-morning-status-workflow` until voided.
- archive-ref: refs/heads/archive/condemned/pyautomind-feature-morning-status-workflow on PyAutoMind origin (13ecca7)

## potential-correction-validation-artifacts
- type: file
- locator: ~/Code/PyAutoLabs/potential_correction_validation_artifacts/ (19 files, 688K — loose workspace-root dir, was in no git repo)
- confidence: n/a — not condemned; archived as a durable BACKUP on explicit human request 2026-08-19
- reason: artifacts of the closed potential-correction-validation campaign (PyAutoLens#672, closed 2026-08-01): phase 2 JAX-vs-Python parity results (phase2_results/*.npz), phase 3 evidence-grid results (subhalo_recovery_evidence_*.npz, iter_point_*.npz), diagnostic/run scripts, chain logs, and the phase 4 algorithm_review_report.md. Moved off the workspace root into the Gut attic; local copy deleted after ls-remote verification.
- merged: n/a
- condemned: 2026-08-19
- sweep-after: never — backup, void only on explicit human request
- breaks-if-wrong: loses the campaign's raw numerical evidence and the algorithm review report; recoverable via `pyauto-gut recover potential-correction-validation-artifacts` (run from the PyAutoGut checkout), then check out the branch to reabsorb.
- archive-ref: refs/heads/archive/condemned/potential-correction-validation-artifacts on PyAutoGut origin (716826e, orphan commit, 19 files)

## pyautomind/stash-pre-sync-2026-07-06
- type: stash
- locator: stash@{0} (PyAutoMind) — "pre-sync local PyAutoMind edits 2026-07-06 (restored after accidental drop)"
- confidence: 0.95
- reason: hygiene `tidy` pre-scan flagged a stale local stash in the PyAutoMind checkout. Materialised to a branch (`git branch <tmp> stash@{0}`, non-destructive — no apply/pop) before archiving, then dropped. Human-authorized batch condemnation 2026-07-30.
- merged: no
- condemned: 2026-07-30
- sweep-after: 2026-08-29
- breaks-if-wrong: loses the pre-sync 2026-07-06 WIP; recoverable via `pyauto-gut recover pyautomind-stash--0-` until voided.
- archive-ref: refs/heads/archive/condemned/pyautomind-stash--0- on PyAutoMind origin (9dc61c5)

## pyautohands/pre-2023-history
- type: branch
- locator: master (PyAutoLabs/PyAutoHands, tip 55da101c — 442 commits, 2021-02-12 → 2022-11-27)
- confidence: n/a — not condemned as trash; archived as durable ORIGINAL PROJECT HISTORY on explicit human request 2026-08-26, then removed from PyAutoHands.
- reason: the pre-2023 history of PyAutoHands, orphaned by a later history reset. Shares **no common ancestor** with `origin/main` (`git merge-base` exits 1) and is pinned by **no tag**, so `main` contains none of its 442 commits and nothing else anywhere reaches them. Authors: Richard 261, Jonathan Frawley 91, James Nightingale 90. The 2026-08-25 org-wide audit flagged it and deliberately left it in place; removed here only once the archive was independently verified.
- merged: no
- condemned: 2026-08-26
- sweep-after: never — original project history, void only on explicit human request
- breaks-if-wrong: loses the entire 2021-2022 development history of PyAutoHands, including 261 commits authored by Richard Hayes and 91 by Jonathan Frawley. Recoverable via `pyauto-gut recover pyautohands-pre-2023-history` (run from the PyAutoGut checkout), then check out the branch to reabsorb.
- archive-ref: refs/heads/archive/condemned/pyautohands-pre-2023-history on PyAutoGut origin (55da101c, 442 commits) — verified by independent clone-back: fetched tip matches, `rev-list --count` = 442, oldest 7d8743a (2021-02-12), newest 55da101 (2022-11-27). Note: PyAutoBrain `branch_archive.yml` could NOT do this — `PAT_PYAUTOLABS` lacks the `workflow` scope and GitHub rejects any PAT push that introduces `.github/workflows/release.yml`; archived from a local checkout with a `workflow`-scoped token instead.

## pyautomind/claude-session-branches-2026-08-26-batch
- type: branch
- locator: 37 `claude/*` session branches on PyAutoLabs/PyAutoMind (2026-06-20 → 2026-08-25)
- confidence: 0.95
- reason: abandoned Claude Code session branches, each carrying one or a few prompt-filing commits that never landed. Verified NOT silently merged: none had a PR, and for every branch whose touched paths exist on `main` today, **zero files were byte-identical** — a later session filed a different prompt at the same path, so the path collides but the content does not. Human-authorized batch condemnation 2026-08-26 ("remove nearly all PyAutoMind ones"). The 3 `archive/condemned/*` Gut-transit refs and today's live `claude/gradient-eager-jit-divergence-py313-5dylgx` were excluded.
- merged: no
- condemned: 2026-08-26
- sweep-after: 2026-11-24
- breaks-if-wrong: loses the unlanded prompt drafts and mind-state edits on those 37 branches. Each is recoverable via `pyauto-gut recover <name>` until voided; names are `pyautomind-<branch-suffix>`.
- archive-ref: 37 refs under `refs/heads/archive/condemned/pyautomind-*` on PyAutoGut origin — all 37 verified by fresh `ls-remote` SHA match against the pre-delete tips before any deletion. Full branch→SHA map:
    - `claude/pyautoprompt-docs-review-2af7eg` @ `c7d623618` → `archive/condemned/pyautomind-pyautoprompt-docs-review-2af7eg` (2026-06-20)
    - `claude/health-agent-implementation-x3z8w6` @ `23165376f` → `archive/condemned/pyautomind-health-agent-implementation-x3z8w6` (2026-06-29)
    - `claude/weak-package-review-016kv1` @ `75e918799` → `archive/condemned/pyautomind-weak-package-review-016kv1` (2026-07-15)
    - `claude/rename-pyautobuild-pyautohands-xqn0p4` @ `f80063350` → `archive/condemned/pyautomind-rename-pyautobuild-pyautohands-xqn0p4` (2026-07-18)
    - `claude/rename-pyautoconf-pyautomerves-i7w9f7` @ `be4ca3f53` → `archive/condemned/pyautomind-rename-pyautoconf-pyautomerves-i7w9f7` (2026-07-18)
    - `claude/autolens-free-ai-setup-jwpyjy` @ `ae4822372` → `archive/condemned/pyautomind-autolens-free-ai-setup-jwpyjy` (2026-08-01)
    - `claude/autolens-guard-small-datasets-jaqyxv` @ `d4e4e0dad` → `archive/condemned/pyautomind-autolens-guard-small-datasets-jaqyxv` (2026-08-03)
    - `claude/health-agent-full-run-myysos` @ `2ebc0f3ae` → `archive/condemned/pyautomind-health-agent-full-run-myysos` (2026-08-05)
    - `claude/hygiene-agent-run-n9qtd5` @ `89f540454` → `archive/condemned/pyautomind-hygiene-agent-run-n9qtd5` (2026-08-05)
    - `claude/interferometer-oom-nufft-yyz98z` @ `3e87583b3` → `archive/condemned/pyautomind-interferometer-oom-nufft-yyz98z` (2026-08-05)
    - `claude/markdown-sigma-min-debt-82rpcb` @ `64a61f697` → `archive/condemned/pyautomind-markdown-sigma-min-debt-82rpcb` (2026-08-07)
    - `claude/pyautomind-simple-issue-rvfp2b` @ `f6cf6419c` → `archive/condemned/pyautomind-pyautomind-simple-issue-rvfp2b` (2026-08-07)
    - `claude/wake-up-7c3ua4` @ `2f91a2221` → `archive/condemned/pyautomind-wake-up-7c3ua4` (2026-08-11)
    - `claude/wake-up-z3y6zi` @ `2d47239ea` → `archive/condemned/pyautomind-wake-up-z3y6zi` (2026-08-15)
    - `claude/clipper-search-identifier-4cowi2` @ `332890828` → `archive/condemned/pyautomind-clipper-search-identifier-4cowi2` (2026-08-18)
    - `claude/constantzeroth-regularization-cleanup-k1vd0j` @ `04731a656` → `archive/condemned/pyautomind-constantzeroth-regularization-cleanup-k1vd0j` (2026-08-18)
    - `claude/multi-galaxy-autolens-package-g1abb3` @ `9a00355c7` → `archive/condemned/pyautomind-multi-galaxy-autolens-package-g1abb3` (2026-08-18)
    - `claude/wake-up-x5emxb` @ `ca56cd9af` → `archive/condemned/pyautomind-wake-up-x5emxb` (2026-08-19)
    - `claude/autolens-numba-profiling-32su4s` @ `9795eddb1` → `archive/condemned/pyautomind-autolens-numba-profiling-32su4s` (2026-08-21)
    - `claude/bilinear-rtu-mesh-docs-pbhsxg` @ `e70134dfa` → `archive/condemned/pyautomind-bilinear-rtu-mesh-docs-pbhsxg` (2026-08-21)
    - `claude/pyautoarray-community-triage-mh7gnp` @ `14ce1f82b` → `archive/condemned/pyautomind-pyautoarray-community-triage-mh7gnp` (2026-08-21)
    - `claude/autoarray-pixel-scales-int-tuple-wfxlnj` @ `e69e01a4c` → `archive/condemned/pyautomind-autoarray-pixel-scales-int-tuple-wfxlnj` (2026-08-22)
    - `claude/community-release-notification-q4ls6e` @ `7f3e6225d` → `archive/condemned/pyautomind-community-release-notification-q4ls6e` (2026-08-22)
    - `claude/message-log-partition-tuple-shape-p7uylt` @ `466416546` → `archive/condemned/pyautomind-message-log-partition-tuple-shape-p7uylt` (2026-08-22)
    - `claude/autolens-point-jax-vmap-parity-htyfi1` @ `a2b051444` → `archive/condemned/pyautomind-autolens-point-jax-vmap-parity-htyfi1` (2026-08-23)
    - `claude/backport-per-script-timeout-r3w1sv` @ `785698b4c` → `archive/condemned/pyautomind-backport-per-script-timeout-r3w1sv` (2026-08-23)
    - `claude/slowest-smoke-gate-perf-ovsuay` @ `ce2217c56` → `archive/condemned/pyautomind-slowest-smoke-gate-perf-ovsuay` (2026-08-23)
    - `claude/stale-jax-pin-smoke-g805rn` @ `309d27f1c` → `archive/condemned/pyautomind-stale-jax-pin-smoke-g805rn` (2026-08-23)
    - `claude/api-drift-ellipse-grid-lines-8sfjjk` @ `dba72e390` → `archive/condemned/pyautomind-api-drift-ellipse-grid-lines-8sfjjk` (2026-08-24)
    - `claude/cti-ci-standardisation-phase-6-8uqpfd` @ `8abb854dd` → `archive/condemned/pyautomind-cti-ci-standardisation-phase-6-8uqpfd` (2026-08-24)
    - `claude/pyauto-cti-ci-phase-5-n4idom` @ `332c4513d` → `archive/condemned/pyautomind-pyauto-cti-ci-phase-5-n4idom` (2026-08-24)
    - `claude/pyautohands-rejects-autocti-bug-vu5ulq` @ `5c0ae8bea` → `archive/condemned/pyautomind-pyautohands-rejects-autocti-bug-vu5ulq` (2026-08-24)
    - `claude/pynufft-removal-phase-3-ird7b8` @ `15abb314f` → `archive/condemned/pyautomind-pynufft-removal-phase-3-ird7b8` (2026-08-24)
    - `claude/strong-lensing-papers-2026-6cpv0a` @ `f4865cebc` → `archive/condemned/pyautomind-strong-lensing-papers-2026-6cpv0a` (2026-08-24)
    - `claude/test-mode-bypass-assertion-ties-jqi2f1` @ `96143497a` → `archive/condemned/pyautomind-test-mode-bypass-assertion-ties-jqi2f1` (2026-08-24)
    - `claude/loggaussian-prior-support-buv5xe` @ `5dfffb4c3` → `archive/condemned/pyautomind-loggaussian-prior-support-buv5xe` (2026-08-25)
    - `claude/pyautohands-rejects-autocti-bug-mk1yi9` @ `85f6df2af` → `archive/condemned/pyautomind-pyautohands-rejects-autocti-bug-mk1yi9` (2026-08-25)

## pyautohands/2022-era-feature-branches
- type: branch
- locator: `feature/dynamic_scripts` (tip 3f5eaf0, 313 commits) and `feature/build_tests` (tip 0c1ad5d, 312 commits) on PyAutoLabs/PyAutoHands
- confidence: n/a — not condemned as trash; removed alongside [[pyautohands/pre-2023-history]] on explicit human request 2026-08-26.
- reason: siblings of the archived pre-2023 `master` — both share its ancestry and are likewise disjoint from today's `main`. `feature/build_tests` carried **0** commits not already reachable from the `master` archive, so it needed no archive of its own. `feature/dynamic_scripts` carried **9** unique commits (all Richard, 2022-10-10, CI iteration: "install and use jq", "checkout", "cd", "remove commented step") that the `master` archive did NOT cover, so it was archived separately before deletion.
- merged: no
- condemned: 2026-08-26
- sweep-after: never — 2022-era project history, void only on explicit human request
- breaks-if-wrong: `build_tests` loses nothing (fully contained in the `master` archive). `dynamic_scripts` would lose its 9 unique CI commits; recoverable via `pyauto-gut recover pyautohands-feature-dynamic-scripts`.
- archive-ref: `refs/heads/archive/condemned/pyautohands-feature-dynamic-scripts` on PyAutoGut origin (3f5eaf0, 313 commits) — verified by independent clone-back before the source branches were deleted. `feature/build_tests`: `n/a`, its content is reachable from `archive/condemned/pyautohands-pre-2023-history` (verified `git rev-list --count 55da101c..build_tests` = 0); pre-delete SHA `0c1ad5d`.

## autolens_profiling/jax-optimizer-tuning
- type: branch
- locator: `feature/jax-optimizer-tuning` (tip fc270a2, 2 commits ahead, last touched 2026-07-15) on PyAutoLabs/autolens_profiling
- confidence: 0.95
- reason: the harness work behind issue #69 ("tune the JAX multi-start optimizers into a standard option"), which was **CLOSED as superseded** on 2026-08-18 (human-confirmed) by the 2026-08-17 inference programme (#134, `results/notes/inference/PROGRAMME.md`, merged via #136/#137). The `learning_rate` axis dissolved into the lr-free MultiStartProdigy; the Sersic lens + Sersic source case was *deliberately dropped* by human decision. Never opened a PR, and the `searches/` tree it edits no longer exists on `main` at all. Mind record: `complete/archive/shelved/jax_optimizer_settings_tuning.md`.
- merged: no
- condemned: 2026-08-26
- sweep-after: 2026-11-26
- breaks-if-wrong: loses 181 lines of settings-grid/truth-scoring harness across `searches/_samplers.py`, `searches/_setup.py`, `searches/sweep.py` and two `imaging/sersic.py` cells. Recoverable via `pyauto-gut recover autolens-profiling-jax-optimizer-tuning`. Note the layout mismatch: `searches/` is gone from `main`, so a reabsorb is a port, not a merge.
- archive-ref: `refs/heads/archive/condemned/autolens-profiling-jax-optimizer-tuning` @ `fc270a2ffbf73393f6c1d85b2cb90d7a0e551bc6` on PyAutoGut — verified by independent clone-back (102 commits) before the source branch was deleted.

## autolens_profiling/multiband-compile-ab
- type: branch
- locator: `archive/condemned/multiband-compile-ab` (tip 7735151, 3 commits ahead, last touched 2026-07-21) on PyAutoLabs/autolens_profiling
- confidence: 0.9
- reason: a jax_compile multi-band A/B experiment (FactorGraphModel vag compile; the finding that `lax.map` scan is the compile killer and pyloop fixes it) that someone had already named into the archive namespace **in the wrong repo** — the archive lives on PyAutoGut, not on the source repo — and never filed a `condemned.md` entry, so nothing pinned it. This entry is that missing record; the payload has been re-homed to the Gut where the namespace actually means something.
- merged: no
- condemned: 2026-08-26
- sweep-after: never — its README carries the lax.map/pyloop compile finding, which is a result rather than spent scaffolding; void only on explicit human request
- breaks-if-wrong: loses 319 lines — `jax_compile/README.md` (113 lines of experiment write-up), `jax_compile/results/local_cpu/mge.json` measurements, and `instruments/imaging.py` / `searches/_setup.py` harness. Recoverable via `pyauto-gut recover autolens-profiling-multiband-compile-ab`.
- archive-ref: `refs/heads/archive/condemned/autolens-profiling-multiband-compile-ab` @ `7735151b89147c09d29ec98480fb03fb2bb3d21b` on PyAutoGut — verified by independent clone-back (130 commits) before the source branch was deleted.

## autolens_profiling/stash-strip-non-jit-noise
- type: stash
- locator: `stash@{0}` in the autolens_profiling canonical checkout — "On strip-non-jit-noise-add-alma-high-res: strip-noise wip", dated 2026-06-07
- confidence: 0.95
- reason: 11 weeks untouched; its base branch `strip-non-jit-noise-add-alma-high-res` no longer exists on origin, and the `likelihood/` scripts it edits are not on `main`'s current tree. The diff is a strip/simplify pass (325 insertions, 778 deletions across 9 likelihood scripts — removing per-channel eager numpy baselines in favour of the JIT loop), not unlanded new work.
- merged: no
- condemned: 2026-08-26
- sweep-after: 2026-11-26
- breaks-if-wrong: loses the noise-stripping edits to `likelihood/{datacube,imaging,interferometer,point_source}/*.py`. Materialised as a real commit before the drop, per the schema's rule that a manifest merely *pointing* at a stash is worthless once it is dropped. Recoverable via `pyauto-gut recover autolens-profiling-stash-strip-non-jit-noise`.
- archive-ref: `refs/heads/archive/condemned/autolens-profiling-stash-strip-non-jit-noise` @ `e6e72cc2dfd67a7ae5cb2fff3b0fb0ae3dc56e56` on PyAutoGut — verified by independent clone-back (9 files, 325/778 diff intact) before `git stash drop`.

## autolens_workspace_developer/rectangular-spline-rotated-experiments
- type: file
- locator: `rect_adapt_duo/` (7 files, incl. bundled `dataset/*.fits`), `searches_minimal/probe_grad_pix_adapt_image.py`, `jax_profiling/misc/pixelization_spline_vs_linear.py`, `jax_profiling/misc/pixelization_spline_fit_comparison.py`, `jax_profiling/results/jit/imaging/spline_vs_linear_fit/` (2 PNGs), `jax_profiling/results/jit/imaging/spline_vs_linear_hst_v2026.4.13.6.json`, `..._sweep.png` — 14 files, 1775 lines plus binaries, in PyAutoLabs/autolens_workspace_developer
- confidence: 0.97
- reason: every one of these exercises a mesh class that no longer exists in PyAutoArray. The 2026-07-23 rectangular-mesh consolidation (PyAutoArray#402/#403) deleted `RectangularSplineAdapt{Density,Image}` and `RectangularRotatedAdaptImage`; these scripts import them at module scope and cannot run at all against any `main` since. They are spent comparison experiments — the spline and rotated transforms lost to the consolidation, which chose the kernel-CDF transform instead. Not wrong code, just code whose subject the library removed. Task: autolens_workspace_developer#131, prompt `active/rectangular_experiments_gut_stash.md`.
- merged: no
- condemned: 2026-08-27
- sweep-after: n/a — nothing to void. These are committed deletions on a pushed repo, so the bytes stay reachable in remote history permanently; per the entry schema's "Committed code / test deletions" rule this record exists only to pin the pre-delete SHA. There is no ref to expire and no `pyauto-gut void` step.
- breaks-if-wrong: loses the rotated-vs-spline mesh demo (`rect_adapt_duo/compare_meshes.py` + its self-contained simulated dataset), the spline adapt-image FD gradient probe, and the spline-vs-linear pixelization profiling comparison with its measured HST results (JSON + sweep plot). The *findings* those runs produced survive in `jax_profiling/gradient/README.md` and the PyAutoArray#402 completion record; what is lost is the ability to re-run them, which already requires resurrecting three deleted library classes.
- archive-ref: `n/a` — committed deletion; pre-delete SHA `9ae0502` on PyAutoLabs/autolens_workspace_developer `main` (the base of `feature/rectangular-experiments-gut-stash`). Recover with `git checkout 9ae0502 -- <path>`.

## autolens_profiling/inference-programme-ledger
- type: branch
- locator: `feature/inference-programme-ledger` in autolens_profiling (laptop worktree `~/Code/PyAutoLabs-wt/inference-programme-ledger`, PR #135 closed unmerged)
- confidence: 0.99
- reason: the task was started twice; the mobile session's #136 and the reconciling #137 (merged `5ce0243`) folded this branch's richer CP-1 evidence, literature set and follow-ups into `results/notes/inference/` on `main`. The completion record `complete/2026/08/inference-programme-ledger.md` already marks the worktree and branch as stale leftovers for the next cleanup pass. 1 commit ahead of `main`, 203 behind; the programme it documents was retired 2026-09-04 (autolens_profiling#217).
- merged: no
- condemned: 2026-09-04
- sweep-after: 2026-12-04
- breaks-if-wrong: loses the laptop session's original 558-line PROGRAMME.md draft as a standalone commit; its content survives on `main` via #137. Recoverable via `pyauto-gut recover autolens-profiling-inference-programme-ledger`.
- archive-ref: `refs/heads/archive/condemned/autolens-profiling-inference-programme-ledger` @ `3e634abaf1f3ad8f6f25a3b77e6732768b421343` on PyAutoGut — verified by `git ls-remote` against the Gut before the source branch was deleted.

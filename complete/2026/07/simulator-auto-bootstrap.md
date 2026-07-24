## Outcome — SHIPPED + MERGED 2026-07-24 (PR #214)

Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/213
(closed). Consumers auto-bootstrap datasets via should_simulate + subprocess
(the autolens_workspace idiom); 11 seed-verified regenerable dataset dirs left
the repo tip (~2.6MB, 49 files, 32 FITS), gitignored; 11 simulators demoted to
BOOTSTRAP-TARGET no_run entries. History untouched (tip-removal only).

## The catches that mattered

- **point_source/simple is NON-reproducible**: regeneration yields LL -1e99 vs
  the hardcoded -83.38049778 (point.py:244, image_plane.py:143). Kept
  committed + a PROTECTIVE no_run entry on its simulator so a standalone
  mega-run can never overwrite the reference bytes. Lesson: seed-in-code is
  not proof of reproducibility — verify by regenerating against the literals.
- cluster/test is a two-stage csv_api → simulator chain over hand-authored
  CSVs — not bootstrappable; kept. sma.fits is a simulator INPUT (external SMA
  template); kept.
- The pattern was HALF-ADOPTED already — most consumers carried bootstraps;
  the real work was the removal safety + two missing bootstraps
  (multi/visualization_*) that would have broken after git rm.
- Declaration audit: exactly ONE full_datasets removal (imaging/model_fit,
  verified at 15x15); convolution.py's rationale was WRONG (real need = mesh
  geometry, not committed data) — corrected in its __Env__ prose.
- model_fit's TEST_MODE=2 corner-on-None crash: pre-existing, proven identical
  on HEAD (stale-fake shape [[feedback_stale_test_mode_output_fakes_nonetype]]).

## Blind-spot confirmed → follow-up filed

autolens_workspace release profile exempts interferometer
features/potential_correction from SMALL_DATASETS (:56-57) but NOT the imaging
sibling → runs mesh-starved (July #315 shape). Filed:
draft/bug/autolens_workspace/potential_correction_small_datasets_asymmetry.md.

## Follow-ups
5 cull low-confidence flags on #211 (human); profiling/ move (blackjax claim);
eyes_gallery_repoint; test_results_relayout (Phase 3, drafted); optional
later: explicit history purge of removed FITS (separate human decision).

## Original prompt

# autolens_workspace_test: adopt auto-simulation, uncommit regenerable datasets (Phase 2b)

Type: refactor
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Blocked-by: the #211 mirror-restructure PR (paths change under this task's feet — land that first)

Human decision on issue autolens_workspace_test#211 (2026-07-24), superseding
the cull list's 17 simulator demotes: mirror autolens_workspace's
auto-simulation pattern — NEVER commit simulator-regenerable data.

**The pattern (already live in autolens_workspace, e.g. imaging/modeling.py:96):**
```python
if al.util.dataset.should_simulate(str(dataset_path)):
    subprocess.run([sys.executable, "scripts/<dir>/simulator.py"], check=True)
```
`should_simulate` (PyAutoArray util/dataset_util.py) is SMALL_DATASETS-aware:
under the cap it deletes existing data so the simulator recreates it at
reduced resolution — this structurally removes the "committed full-res FITS
vs capped mask" shape-mismatch failure class (July's #297/#315 shape).

**The tasks (all paths POST-restructure — re-key from the merged #211 PR):**
1. Inventory `dataset/`: classify every committed dataset as
   simulator-regenerable (a scripts/ simulator produces it) vs real/external
   (RXJ1131, cluster observational data, pre-committed reference FITS with
   hand-calibrated assertions). ONLY the former is touched.
2. Convert every consuming script to the should_simulate bootstrap (subprocess
   to the sibling simulator, exactly the user-workspace idiom). Simulator
   scripts stay on disk as the bootstrap targets; remove them from the
   standalone run surface (no_run entry or equivalent) since consumers now
   invoke them.
3. `git rm` the regenerable datasets from the tip + `.gitignore` their paths.
   HISTORY PURGE IS OUT OF SCOPE — never-rewrite rule; tip-removal only.
4. Declaration cleanup: `full_datasets` declarations that existed ONLY because
   a script loaded committed full-res FITS become deletable (should_simulate
   regenerates at capped resolution under smoke). Audit each affected script's
   `__Env__` section: keep the declaration only where assertions genuinely
   need full resolution (prior counts, calibrated thresholds); delete
   otherwise, with the resolved-env diff documenting each intentional change.
5. `weak/` already follows this pattern (uncommitted, runtime producer) — use
   it as the reference; confirm it needs no changes.
6. Verify: full smoke gate green; a clean-clone dry run of 2-3 converted
   scripts (delete their dataset dirs, run, confirm bootstrap + pass);
   validator all-strict 0 errors; repo-size delta reported in the PR.

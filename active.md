# Active Tasks

## remove-inline-standalones
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/160
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/remove-inline-standalones
- autonomy: safe
- prompt: active/matplotlib_inline_standalones.md
- note: User-approved first task in the ordered matplotlib-inline cleanup; remove five standalone comments in AutoGalaxy/AutoLens before starting the dependent AutoCTI bootstrap sweep. The overlapping Colab-bootstrap PRs merged and released both claims before setup. AutoLens main-checkout formatting changes remain isolated and untouched.
- repos:

## clean-packaging-debris
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/159
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/clean-packaging-debris
- autonomy: supervised
- prompt: active/clean_generated_packaging_debris.md
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/160
- note: PR open at ccb7b88 with pending-release label. Validation: 19 targeted + 157 remaining Brain tests pass; the sizing-wrapper failure is pre-existing on main. Brain-only operational CLI change, so workspace smoke is n/a. Heart YELLOW (workspace failures, stale parked scripts, manifest drift, stale rehearsal) explicitly acknowledged by the user. Concurrent profiling-mirror-taxonomy changed only agents/conductors/profiling/_profiling.py at ship time; no overlap.
- repos:
  - PyAutoBrain: feature/clean-packaging-debris

## profiling-mirror-taxonomy
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/84
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/profiling-mirror-taxonomy
- autonomy: supervised
- prompt: active/mirror_scripts_taxonomy.md
- note: UNBLOCKED (group4 merged PR#83, claim released). Dataset-first inversion: scripts/<dataset>/<task>/, cluster/ first-class (group4 cells -> scripts/cluster/, human decision), datacube under interferometer, agnostic -> scripts/misc/<task>/. LOCKED: results/config/dataset stay at root, results section names stable; fix parents[1] import model FIRST; 28 sbatch rewrites; Brain profiling conductor lockstep (companion PR); RAL re-sync = post-merge step. Gates on issue #84. Fresh YELLOW ack at ship.
- repos:
  - autolens_profiling: feature/profiling-mirror-taxonomy
  - PyAutoBrain: feature/profiling-mirror-taxonomy

## testmode-env-drift
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/95
- status: PRs OPEN awaiting merge — PyAutoCTI#96 (delete dead fixture) + PyAutoFit#1417 (docstring). KEY FINDING: the obvious fix (rename PYAUTOFIT_TEST_MODE -> PYAUTO_TEST_MODE) is WRONG. Nothing reads PYAUTOFIT_TEST_MODE so the aggregator autouse fixture was always a no-op; making the var LIVE actually enables test mode, which bypasses sampling so the aggregator has no samples -> 6/13 tests FAIL. Measured 3 ways: baseline(dead var)=13 passed; renamed=6 failed/7 passed; fixture DELETED=13 passed. Shipped the deletion (behaviour-preserving, deletes the trap). Two gitignored .claude/settings.local.json allowlists deliberately LEFT ALONE — rewriting them would change what those commands do; they are stale permission strings, not a defect.
- worktree: ~/Code/PyAutoLabs-wt/testmode-env-drift
- autonomy: safe
- prompt: active/pyautofit_test_mode_env_var_drift.md
- note: canonical knob is PYAUTO_TEST_MODE (autonerves/test_mode.py:14) + PYAUTO_TEST_MODE_SAMPLES. autocti_workspace_test/AGENTS.md:42 and autocti_assistant/skills/ac_fit_cti_model.md:126 already DOCUMENTED that PYAUTOFIT_TEST_MODE does not exist — trap documented instead of deleted; this task deletes it. NEXT: merge both PRs, then close #95.
- repos:
  - PyAutoCTI: feature/testmode-env-drift
  - PyAutoFit: feature/testmode-env-drift

## jax-joss-benchmarks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/281
- status: PARKED-ON-JOB — #282 MERGED+cleaned; 8/8 runnable A100 rows committed (autolens_jax_joss@64204f6). SDP.81 prep = detached RAL job 330608 (330605 diagnosed: empty extracted/ leftover skipped untar via test-d guard; casatools import needs ~/.casa/data — both fixed; 42GB tarball CACHED, no re-download) (45GB ALMA Band6 download -> casatools venv -> 3-level export -> installs dataset/interferometer/{sdp81,sdp81_mid,sdp81_full} in /mnt/ral/jnightin/autolens_jax_joss). RESUME (short session): (1) check log /mnt/ral/jnightin/sdp81_prep_330608.log — expect 'SDP81 PREP ALL DONE' + per-level visibility counts; failure modes: casatools pip wheel on py3.12 (fallback = monolithic CASA tarball), datacolumn, MS_LIST empty (check find patterns); (2) sbatch interferometry benchmarks on A100: benchmarks/interferometer.py at --nvis default/mid/full + benchmarks/imaging_and_interferometer.py (pattern: /mnt/ral/jnightin/autolens_jax_joss/run_rest.sbatch); (3) scp results/*.json back, regen RESULTS.md, commit (guard: explicit file paths); (4) copy small sdp81/ product locally, rewrite scripts/interferometer/start_here.py on NEW branch (start_workspace; #282 merged) using it — decide hosting (commit few-MB FITS to workspace w/ .gitignore allowlist + git add -f, or Zenodo+SDP81_URL); (5) final issue #281 update. Also pending: cluster-tuning prompt draft/feature/autolens_workspace/joss_cluster_benchmark_tuning.md; weak JAX-viz PyAutoLens#614
- worktree: ~/Code/PyAutoLabs-wt/jax-joss-benchmarks
- autonomy: supervised
- prompt: active/autolens_jax_joss_benchmark_repo.md
- note: 5-phase epic (one-shot attempt per user); new repo autolens_jax_joss (PyAutoLabs, public) born alongside; datasets SDP.81 / RXJ1131 / A2744 user-approved
- repos:
  - autolens_jax_joss: main (born this task)

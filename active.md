# Active Tasks

## start-here-jax-simplify
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/336
- status: awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/start-here-jax-simplify
- autonomy: supervised
- prompt: active/start_here_jax_section_simplify.md
- workspace-pr: autolens_workspace#338 + autogalaxy_workspace#162
- heart-ack: user acknowledged YELLOW at ship (workspace validation 13f stale census 2026-07-21; 33 stale parked scripts; tenant-firewall manifest drift x3; release validation stale) — none touch this docs-only change
- note: Shipped with targeted smoke PASS (root start_here.py + guide in both repos). Both PRs also true-up a stale .script_sizes.json snapshot (drift inherited from earlier merged sweeps; new using_jax.py entry included). ag guide fixes stale api/data_structures.py cross-ref. NEXT: merge both PRs (standalone, no library gate), then lifecycle record + close #336.
- repos:
  - autolens_workspace: feature/start-here-jax-simplify
  - autogalaxy_workspace: feature/start-here-jax-simplify

## notebook-adjacent-docstrings
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/196
- session: codex
- status: library-shipped, smoke-passed
- worktree: ~/Code/PyAutoLabs-wt/notebook-adjacent-docstrings
- autonomy: supervised
- prompt: active/back_to_back_docstrings_notebook.md
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/197
- note: Commit 6916814; 218 PyAutoHands tests pass. User acknowledged Heart YELLOW (workspace validation not passing; 33 stale parked scripts). The initial parallel/manual smoke harness reported 8 failures, but triage showed two harness defects: regenerated notebooks ran from /tmp instead of the workspace root, and scripts sharing auto-simulated datasets ran concurrently. The canonical per-workspace runners pass all affected suites (AutoFit 10/10, AutoGalaxy 8/8, AutoLens 11/11); combined downstream result is 58 passed, 0 failed, 2 configured skips. Phase 2 may proceed; do not merge PR #197 without human approval.
- repos:
  - PyAutoHands: feature/notebook-adjacent-docstrings

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

# Active Tasks

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

## hygiene-adjacent-docstrings
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/162
- session: codex
- status: library-shipped, workspace-pending
- worktree: ~/Code/PyAutoLabs-wt/hygiene-adjacent-docstrings
- autonomy: supervised
- prompt: active/adjacent_docstring_hygiene.md
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/163
- note: Phase 2 of PyAutoHands#196. The read-only AST-backed Hygiene mode is shipped to an open pending-release PR. It reports root entry scripts plus scripts/**/*.py, exact human/JSON findings, default ranking, and /refactor delegation. Final live inventory before cleanup: 81 boundaries in 58 files across 6/7 repos with zero parse errors. Phase 3 is draft/maintenance/workspaces/merge_adjacent_docstrings.md.
- repos:
  - PyAutoBrain: feature/hygiene-adjacent-docstrings

## profiling-dataset-auto-simulate
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/88
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/profiling-dataset-auto-simulate
- autonomy: supervised
- heart-ack: 2026-07-24 human ack covers this ship (extended three-reason ack recorded on the completed dpie-simulator-port task; STOP if the reason set grows beyond those three or any gate fails)
- prompt: active/dataset_auto_simulate.md
- note: #213 recipe for autolens_profiling; BYTE-identity required (baselines calibrated against committed bytes); dPIE fix merged (#87) so cluster family verifiable. Non-reproducible => committed + protective note.
- repos:
  - autolens_profiling: feature/profiling-dataset-auto-simulate

## merge-adjacent-docstrings
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/341
- session: codex
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/merge-adjacent-docstrings
- autonomy: supervised
- prompt: active/merge_adjacent_docstrings.md
- note: Merge 81 scanner-confirmed adjacent documentation boundaries with exact ordered-text witnesses. Start with the six unclaimed repos; autolens_workspace is deferred until simulator-jax-sections-code-cells releases its active worktree claim. Branch approved as feature/merge-adjacent-docstrings. HowToFit is a verified zero-finding target.
- blocked-repo: autolens_workspace — simulator-jax-sections-code-cells
- repos:

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

## simulator-jax-sections-code-cells
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/339
- session: claude --resume 5028c921-5f5d-4142-8c9b-a86da5c3641e
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/simulator-jax-sections-code-cells
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/340
- heart-ack: 2026-07-24 human ack for this ship covers exactly: workspace validation not passing (13 failed, 2026-07-21T19-05-22Z); 33 stale parked script(s); manifest drift: tenant firewall (3 mismatches vs repos.yaml). STOP if the reason set grows.
- prompt: active/simulator_jax_sections_real_code_cells.md
- note: Convert fenced ```python blocks inside the __JAX Variant__ / __Oversampled PSF__ docstring sections of imaging/interferometer/point_source simulator.py into real code cells; comment out only the executing line (run-time / dataset-overwrite note); retitle with (Advanced) and add to __Contents__; update 5 cross-refs.
- repos:
  - autolens_workspace: feature/simulator-jax-sections-code-cells

# Active Tasks

## validation-searches-env-optax
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/77
- session: claude
- status: library-shipped, awaiting-merge
- library-pr: autofit_workspace_test#78, PyAutoGalaxy#530, PyAutoHeart#111 (all pending-release)
- heart-ack: ["workspace validation not passing (13 failed, 2026-07-21T19-05-22Z)", "33 stale parked script(s)", "manifest drift: tenant firewall (organ code) — 5 mismatch(es) vs PyAutoMind/repos.yaml"]
- worktree: ~/Code/PyAutoLabs-wt/validation-searches-env-optax
- autonomy: supervised
- prompt: active/validation_searches_env_and_optax_chain.md
- note: first of the three red overnight jobs from the 2026-07-27 /wake_up digest. Two independent causes — missing __Env__ declarations (autofit_workspace_test) + optax/blackjax never reaching the validation env (PyAutoGalaxy jax extra, PyAutoHeart smoke install). Brain phase-split (score 20, 4 phases) overridden: repo-count proxy, actual diff is 2 docstring sections + 2 one-liners.
- repos:
  - autofit_workspace_test: feature/validation-searches-env-optax
  - PyAutoGalaxy: feature/validation-searches-env-optax
  - PyAutoHeart: feature/validation-searches-env-optax

## jax-joss-benchmarks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/281
- status: PARKED-ON-JOB — #282 MERGED+cleaned; 8/8 runnable A100 rows committed (autolens_jax_joss@64204f6). SDP.81 prep = detached RAL job 330608 (330605 diagnosed: empty extracted/ leftover skipped untar via test-d guard; casatools import needs ~/.casa/data — both fixed; 42GB tarball CACHED, no re-download) (45GB ALMA Band6 download -> casatools venv -> 3-level export -> installs dataset/interferometer/{sdp81,sdp81_mid,sdp81_full} in /mnt/ral/jnightin/autolens_jax_joss). RESUME (short session): (1) check log /mnt/ral/jnightin/sdp81_prep_330608.log — expect 'SDP81 PREP ALL DONE' + per-level visibility counts; failure modes: casatools pip wheel on py3.12 (fallback = monolithic CASA tarball), datacolumn, MS_LIST empty (check find patterns); (2) sbatch interferometry benchmarks on A100: benchmarks/interferometer.py at --nvis default/mid/full + benchmarks/imaging_and_interferometer.py (pattern: /mnt/ral/jnightin/autolens_jax_joss/run_rest.sbatch); (3) scp results/*.json back, regen RESULTS.md, commit (guard: explicit file paths); (4) copy small sdp81/ product locally, rewrite scripts/interferometer/start_here.py on NEW branch (start_workspace; #282 merged) using it — decide hosting (commit few-MB FITS to workspace w/ .gitignore allowlist + git add -f, or Zenodo+SDP81_URL); (5) final issue #281 update. Also pending: cluster-tuning prompt draft/feature/autolens_workspace/joss_cluster_benchmark_tuning.md; weak JAX-viz PyAutoLens#614
- worktree: ~/Code/PyAutoLabs-wt/jax-joss-benchmarks
- autonomy: supervised
- prompt: active/autolens_jax_joss_benchmark_repo.md
- note: 5-phase epic (one-shot attempt per user); new repo autolens_jax_joss (PyAutoLabs, public) born alongside; datasets SDP.81 / RXJ1131 / A2744 user-approved
- repos:
  - autolens_jax_joss: main (born this task)

## pix-prodigy-cpu
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/117
- session: claude
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/pix-prodigy-cpu
- autonomy: supervised
- prompt: active/pixelized_multistart_prodigy_cpu.md
- repos:
  - autolens_workspace_developer: feature/pix-prodigy-cpu

## point-source-chi-squared-variants
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/657
- session: claude --resume daaa46f9-aac5-48e2-9146-1202a92d879e
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/point-source-chi-squared-variants
- repos:

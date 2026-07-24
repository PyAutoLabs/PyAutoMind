# Active Tasks

## hide-autonerves-colab-autogalaxy
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/158
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/hide-autonerves-colab-autogalaxy
- autonomy: human-required
- prompt: active/hide_autonerves_colab_autogalaxy_rollout.md
- note: AutoGalaxy product-family rollout after merged PyAutoHands#195/PyAutoHeart#107; update 4 handwritten setup scripts and regenerate autogalaxy_workspace + HowToGalaxy.
- repos:

## hide-autonerves-colab-bootstrap
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/194
- status: library-shipped, workspace-pending
- worktree: ~/Code/PyAutoLabs-wt/hide-autonerves-colab-bootstrap
- autonomy: human-required
- prompt: active/hide_autonerves_colab_bootstrap_api.md
- library-pr: PyAutoHands#195 + PyAutoHeart#107
- note: Phase 1 merged (216p Hands, 289p Heart, verify_install F PASS). Workspace impact is 527 files (12 source + 515 generated notebooks); phase 2 is split into AutoGalaxy, AutoFit, and AutoLens product-family prompts.
- repos:
  - PyAutoHands: feature/hide-autonerves-colab-bootstrap
  - PyAutoHeart: feature/hide-autonerves-colab-bootstrap

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

## group4-mge-search-benchmark
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/82
- status: workspace-dev — CODE COMPLETE (phases 1-3), BENCHMARK RUNS PENDING. Branch feature/group4-mge-search-benchmark pushed (bddedc5, no PR). DONE+VERIFIED: simulators/group4_mge.py (4 deflectors+4 sources, GROUP4_TRUTH single-source-of-truth, writes truth.json; preview shows 4 cores+arcs); searches/_setup.py dataset_class='group' _group_mge_model=54 free params (centres SEEDED near truth to break 4x4 permutation symmetry, geometry priors broad; AnalysisImaging; likelihood evals on numpy+JAX); searches/_recovery.py scores max_lh vs truth (theta_E+centre+shear, overall_pass); _runner recovery block; _samplers.py generic build_multi_start for adam/prodigy/lion/adabelief + multi_start_prodigy_autoconv (af.MultiStartGradientConvergence); 6 leaf scripts; sweep.py 6 group cells; README. ruff+smoke green. BLOCKER: multi_start_adam local CPU run sat 20min+ in JAX compile/pre-fit w/ ZERO steps — 54-param 8-galaxy vmap value_and_grad graph too heavy for CPU XLA. RESUME: (1) check if detached CPU run PID 25434 produced output/ or results JSON else kill; (2) RE-RUN ON LAPTOP GPU (~/venv/PyAutoGPU, JAX_PLATFORM_NAME=cuda JAX_PLATFORMS=cuda,cpu XLA_PYTHON_CLIENT_MEM_FRACTION=0.5, --config-name local_gpu_fp64) starting multi_start_adam then family then nautilus anchor; (3) if still too heavy dial _GROUP4_MGE_TOTAL_GAUSSIANS 10->6 and/or _MULTI_START_N_STARTS 64->32; (4) record recovery+walltime vs Nautilus, aggregate.py; (5) phase4 contingency = narrow-prior/warm-start init only if cold-start fails recovery. Env note: do NOT source worktree activate.sh locally (it repoints PYTHONPATH at /mnt/ral HPC); local libs resolve directly. Run w/ NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1.
- worktree: ~/Code/PyAutoLabs-wt/group4-mge-search-benchmark
- autonomy: safe
- prompt: active/research_profiling_experiment_in_the_autolens_pr.md
- note: single repo autolens_profiling (workspace/research, no library edits). Phased: (1) simulator+truth, (2) model cell+recovery+Nautilus anchor, (3) gradient family sweep, (4) contingency = careful init (narrow-prior/warm-start) if cold-start fails recovery.
- repos:
  - autolens_profiling: feature/group4-mge-search-benchmark

## jax-joss-benchmarks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/281
- status: PARKED-ON-JOB — #282 MERGED+cleaned; 8/8 runnable A100 rows committed (autolens_jax_joss@64204f6). SDP.81 prep = detached RAL job 330608 (330605 diagnosed: empty extracted/ leftover skipped untar via test-d guard; casatools import needs ~/.casa/data — both fixed; 42GB tarball CACHED, no re-download) (45GB ALMA Band6 download -> casatools venv -> 3-level export -> installs dataset/interferometer/{sdp81,sdp81_mid,sdp81_full} in /mnt/ral/jnightin/autolens_jax_joss). RESUME (short session): (1) check log /mnt/ral/jnightin/sdp81_prep_330608.log — expect 'SDP81 PREP ALL DONE' + per-level visibility counts; failure modes: casatools pip wheel on py3.12 (fallback = monolithic CASA tarball), datacolumn, MS_LIST empty (check find patterns); (2) sbatch interferometry benchmarks on A100: benchmarks/interferometer.py at --nvis default/mid/full + benchmarks/imaging_and_interferometer.py (pattern: /mnt/ral/jnightin/autolens_jax_joss/run_rest.sbatch); (3) scp results/*.json back, regen RESULTS.md, commit (guard: explicit file paths); (4) copy small sdp81/ product locally, rewrite scripts/interferometer/start_here.py on NEW branch (start_workspace; #282 merged) using it — decide hosting (commit few-MB FITS to workspace w/ .gitignore allowlist + git add -f, or Zenodo+SDP81_URL); (5) final issue #281 update. Also pending: cluster-tuning prompt draft/feature/autolens_workspace/joss_cluster_benchmark_tuning.md; weak JAX-viz PyAutoLens#614
- worktree: ~/Code/PyAutoLabs-wt/jax-joss-benchmarks
- autonomy: supervised
- prompt: active/autolens_jax_joss_benchmark_repo.md
- note: 5-phase epic (one-shot attempt per user); new repo autolens_jax_joss (PyAutoLabs, public) born alongside; datasets SDP.81 / RXJ1131 / A2744 user-approved
- repos:
  - autolens_jax_joss: main (born this task)

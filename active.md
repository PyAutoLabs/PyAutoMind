# Active Tasks

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

## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: coordinating — Phases 0,1,2,5 + Ph3 steps1-3 + Ph4 task1 DONE (~40 PRs); REMAINING queued as 5 draft prompts indexed in active/build_chain_umbrella.md (pick via /feature): version_skew rework NEXT, then version-consumers, HowTo sim, env-profile steps4-8, guard v1.3
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:

## pix-gradient-slogdet-revalidation
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/112
- status: workspace-dev — A100 JOB QUEUED-BUT-GPU-STARVED (330921, submitted 2026-07-20, still PENDING(Priority) after 2h+). BLOCKER: gpu partition has 2 A100 nodes but ONE is down* ("Not responding", indefinite) and the live node's 4 A100s are all held by user c4072114's multi-day jobs (2-3d TIME_LEFT, end 2026-07-23/24). SLURM est. my START ~2026-07-23 19:53 (~3 days). Not mine, cannot cancel; short-walltime backfill won't help (no gap frees for days). Job will run whenever a GPU frees — no action needed to keep it queued. RESUME (poll): Toggle committed (a5b53a6) + A/B sbatch (6461935) on feature/pix-gradient-slogdet-revalidation (local-only, NOT pushed). RAL PyAutoArray synced to PR#392 (had to repair a corrupt origin/main ref: rm .git locks + git update-ref -d refs/remotes/origin/main + fetch --prune; PR392=7 now). Harness scp'd to /mnt/ral/jnightin/autolens_workspace_developer/searches_minimal/. RESUME: (1) `ssh -o IdentitiesOnly=yes euclid_jump "sacct -j 330921 --format=JobID,State,Elapsed -X; tail -80 /mnt/ral/jnightin/pixgrad_logs/pix_slogdet_ab-330921.out"`; (2) A/B verdict = compare the two arms' "Collected X/N starts (from T draws)" (step-0 acceptance) + per-start "died after step N" reports — cholesky baseline died ~25-50, slogdet should survive to step 299; (3) verdict into searches_minimal/pix_nonfinite_findings.md → ship_workspace. Launch env: activate.sh BASE=/mnt/ral/jnightin/PyAuto, al.Settings=aa.Settings so PyAutoArray sync alone suffices.
- worktree: ~/Code/PyAutoLabs-wt/pix-gradient-slogdet-revalidation
- autonomy: supervised
- prompt: active/pix_gradient_landscape_revalidation.md
- note: verification tail of the pix-NaN lineage — localisation (#104/PR#105) + fix (PyAutoArray#392) + fitness-guard contract (PyAutoFit#1391) all shipped 2026-07-17. Toggle is env var PIX_LOGDET=slogdet threaded via al.Settings into build_analysis (one edit covers both pix_multi_start + pix_lr_free). Repro is A100-only (10.9 GiB/point OOMs laptop).
- repos:
  - autolens_workspace_developer: feature/pix-gradient-slogdet-revalidation (worktree live; commit a5b53a6 local-only)

## blackjax-smc-gradient-kernel
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/113
- status: workspace-dev — REFRAMED to the REPRESENTATIVE regime (user): these samplers are meant to be WARM-STARTED from a JAX optimizer MLE, so cold prior-start benchmarking was unrepresentative. RAL CPU job 331035 RUNNING (Prodigy warm start -> 2 warm SMC arms). Committed LOCAL 2b455e4 (+cfcf893) on feature/blackjax-smc-gradient-kernel; NOT pushed. NEW: _warm_start.py = SHARED harness for whole wave (multi-start Prodigy over _grad_setup MGE objective, per-start vmapped opt state, finite-grad start filter) -> ONE cached output/warm_start.json (mle + reference std + log_l) so ALL samplers stages (a)-(e) start from the IDENTICAL point; ref scale via Laplace inv-Hessian diag, fallback multistart-spread, fallback prior-fraction. blackjax_smc_grad.py --warm-start: does NOT just drop particles at MLE (that DESTROYS SMC logZ, valid only tempering from a NORMALISED dist); instead geometric bridge from normalised Gaussian ref g at the MLE: log target_l = log g + l*(log prior + log L - log g) => logprior_fn:=log g, loglikelihood_fn:=log prior+log L-log g; integral g=1 so logZ stays TRUE evidence, comparable to Nautilus. Needed LOG_PRIOR_NORM (prior normalisation incl truncated-Gaussian mass — cancels in MH, NOT in evidence). Init particles drawn FROM g (required for logZ validity); step auto-scales to ref width = the real fix for cold acceptance collapse. --ref-inflate 2.0 keeps g broader than posterior. EARLIER COLD FINDING (still valid, in smc_gradient_findings.md): all 3 cold step regimes collapse acceptance; 'Converged: yes' only means lambda hit 1.0 and can be a FALSE positive (force-jump when acc~0). 5 cold bugs fixed (median-not-mean warmup; centre 1/r singularity->custom_jvp mask; MALA scalar step->whitening; tune callback 3-arg; FLOAT32 [[reference_ral_sbatch_jax_x64_not_inherited]]). RESUME: (1) check 331035 log /mnt/ral/jnightin/smc_grad_logs/smc_warm_cpu-331035.out; SANITY = printed mle einstein_radius (idx 8) must be near truth 1.6 else Prodigy didn't converge and warm arms are meaningless; also watch whether Laplace holds or falls back (fell back locally at a non-optimum); (2) pull output/warm_start.json + blackjax_smc_grad_mala{,_tuned}_warm_summary.txt; compare logZ vs Nautilus -169k and max logL vs nss_grad -31; (3) then HMC arm + A100 rep-timing (GPUs full); (4) update findings + comparison row. Env: blackjax 1.5 isolated at /mnt/ral/jnightin/scratch/smc_grad_pylibs; use <=64p/3step (XLA-LLVM compile-mem); laptop caps ~4p. MGE ONLY; pix deferred.
- worktree: ~/Code/PyAutoLabs-wt/blackjax-smc-gradient-kernel
- autonomy: supervised
- prompt: active/jax_native_posterior_sampler_wave.md
- note: WAVE TRACKER — stages (b) ChEES-HMC, (c) MCLMC+harmonic, (d) flowMC, (e) jaxns remain. Do NOT move prompt to complete/ on stage-(a) ship; issue next stage only as this one nears shipping (no bulk-issue). Concurrent worktree alongside parked pix-gradient-slogdet-revalidation claim (different files). Gradient path certified OK_HMC_VIABLE (probe_grad.py); baseline nss_grad row = logZ -31.47.
- repos:
  - autolens_workspace_developer

## unblock-release-validation
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/314
- status: workspace-dev — DIAGNOSIS COMPLETE, all 5 shard failures reproduced locally 2026-07-22; NONE is a library regression, no source edits needed. Blocking nightly-release at Stage 3 (integrate); Heart RED score 40. Fixes: (1) autolens_workspace_test no_run.yaml permanent entry for gallery/gallery_build (CI runs the build tool without gallery_run.sh first -> scan_images() empty -> documented sys.exit(1) at :159-163); (2) autofit_workspace_test MultiStartResurrect.py:112 np.allclose rtol 1e-5 -> 1e-3 (one resurrection FIRES, n_resurrections 0 vs 1, consuming RNG draws -> arms diverge at 5th sig fig, max rel delta 3.2e-5; docstring invariant is SAME BASIN not bitwise, and truth asserts at :104-106 allow +/-2.0/3.0/2.0 — NOT masking a regression); (3) autolens_workspace env_vars_release.yaml overrides: unset PYAUTO_SMALL_DATASETS for interferometer/features/potential_correction/ (blanket defaults: cap grids to 15x15 -> dpsi mesh too sparse for dpsi_factor=2, mesh.py:132 correctly refuses; VERIFIED fails with cap / passes without, start_here 58s vs 1800s cap, logZ -6.0333e+03, 6.2 sigma); (4+5) autolens_workspace no_run.yaml two "# SLOW 2026-07-22" entries for cluster/start_here.py + weak/features/strong_lensing/a2744.py (both at full 1800s cap; next-slowest siblings 137.8s and 23.6s, so script-specific not shard-wide) — user-approved SLOW-skip-now, profile-later.
- worktree: ~/Code/PyAutoLabs-wt/unblock-release-validation
- autonomy: safe
- prompt: active/unblock_release_validation_2026_07_22.md
- note: Feature Agent MISCLASSIFIED this as too-large/research-first (score 11) — a length+keyword heuristic misfiring on an evidence-heavy prompt; it also resolved "(none)" repos because target is health_fixes and repos appear in a table not as @RepoName. Work is 1-3 lines in each of 4 files, fully diagnosed, zero open questions. Follow-ups filed in issue: profile the 2 SLOW scripts; clean_slate.sh deletes the TRACKED autolens_workspace_test/output/.gitignore.
- repos:
  - autolens_workspace: feature/unblock-release-validation
  - autolens_workspace_test: feature/unblock-release-validation
  - autofit_workspace_test: feature/unblock-release-validation

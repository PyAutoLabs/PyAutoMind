# Active Tasks

## env-declaration-docstring-form
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/189
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/env-declaration-docstring-form
- autonomy: supervised
- heart-ack: 2026-07-23 human acknowledged YELLOW for ship (merge order given): ["workspace validation not passing (13 failed, 2026-07-21T19-05-22Z)", "33 stale parked script(s)"]
- prompt: active/env_declaration_docstring_form.md
- note: Phase 1b follow-up from user feedback — __Env__ docstring form is THE one API everywhere (user decision 2026-07-23): user workspaces = BOTTOM placement + developer-only note + stripped from generated notebooks/markdown; _test repos = NEAR TOP after module docstring (shorter template). Comment form stays parser-valid until all migrations merge, then flipped to validator error in a final change (avoids broken-CI window). MUST land before next pre_build. Gate: resolved-env diff IDENTICAL (pure syntax move). REFINEMENT 2 (user): __Env__ = last SECTION INSIDE the adjacent docstring (user: final docstring; _test: module docstring), standalone only as no-adjacent-docstring fallback — parser/strip generalized on feature/env-comment-form-removal (extends the comment-form-removal flip); 231-script re-migration to merged form = separate pass after that lands; standalone stays parseable so main is valid throughout. Phase 2 (mirror restructure) stays UN-ISSUED until this ships.
- repos:
  - PyAutoHands: feature/env-declaration-docstring-form
  - autolens_workspace: feature/env-declaration-docstring-form
  - autogalaxy_workspace: feature/env-declaration-docstring-form
  - autofit_workspace_test: feature/env-declaration-docstring-form
  - autogalaxy_workspace_test: feature/env-declaration-docstring-form
  - autolens_workspace_test: feature/env-declaration-docstring-form

## rectangular-mesh-consolidation
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/402
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/403
- status: library-MERGED 2026-07-23 (human "merge all") — PyAutoArray#403 + citations PyAutoLens#644 + PyAutoGalaxy#520 all MERGED (403 needed a main-merge: version 2026.7.23.1 + LF restore, main's bump commit had CRLF'd autoarray/__init__.py). HowTo PRs HowToLens#53 + HowToGalaxy#43 MERGED on green CI. REMAINING: (1) autolens_workspace_test jax_grad migration (2 files: imaging_pixelization.py E/F/G → plain names, interferometer.py variant D) + strict-FD re-certification — NOW URGENT: merged main deleted the kernel names these scripts import, BLOCKED on env-declaration-docstring-form claim (re-claimed after env-inline-declarations closed); (2) user-workspace pixelization example citation paragraphs — blocked same claim holder (autolens_workspace/autogalaxy_workspace); (3) developer-repo cleanup + Gut stash — blocked on blackjax-smc-gradient-kernel. On resume: Opus-delegated ship, regen notebooks+navigator for any HowTo/workspace edits.
- worktree: ~/Code/PyAutoLabs-wt/rectangular-mesh-consolidation
- autonomy: supervised
- prompt: active/rectangular_mesh_consolidation.md
- note: Kernel-CDF meshes take over the plain names RectangularAdaptDensity/AdaptImage; linear/spline/rotated + density_components deleted from source (Gut refs). Brain scored too-large/4-phase off repo count — OVERRIDE recorded: standard library→workspace two-leg (workspace leg collapses to test/dev cleanup since user workspaces keep the plain names, zero code edits). Library leg: PyAutoArray primary; PyAutoGalaxy/PyAutoLens expected zero-diff (verify by test suite). Workspace leg AFTER library merge: autolens_workspace_test jax_grad variant consolidation (FD certification = gate); autolens_workspace_developer stash→PyAutoGut BLOCKED on blackjax-smc-gradient-kernel claim — do last/coordinate. Autodiff evidence + full file-level plan on the issue.
- repos:
  - PyAutoArray: feature/rectangular-mesh-consolidation
  - PyAutoLens: feature/rectangular-mesh-consolidation
  - PyAutoGalaxy: feature/rectangular-mesh-consolidation
- citation-leg: Enzi2026 (arXiv:2606.30620, RTU grids) added 2026-07-23 — PyAutoLens+PyAutoGalaxy docs/general/citations.md "Rectangular Mesh" section + files/citations.bib entry (adaptive rect meshes MUST cite; RectangularUniform exempt; note reg differs from paper's GP prior). WORKSPACE PART (blocked with the workspace legs, Opus-delegated): add a short paper-link paragraph to autolens_workspace/autogalaxy_workspace pixelization examples + HowToLens/HowToGalaxy ch4 rectangular tutorials — link arXiv:2606.30620, cite-when-used, one line that the paper pairs RTU with a GP prior whereas these examples use reg.Constant/reg.Adapt. Scripts only; notebooks regen at release.

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

## blackjax-smc-gradient-kernel
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/113
- status: workspace-dev — **IT SAMPLES**. Warm-started gradient SMC WORKING: acc 0.80->0.17 across tempering (was 0.000), particles move, max logL climbs to ~31781 vs Prodigy MLE 31787.93, einstein_radius 1.5998 vs TRUTH 1.6. RAL job 331058 RUNNING (3 arms @128p: MALA auto-step, MALA+tune, HMC; warm start --refresh'd for full covariance). Committed LOCAL a467fad+6867762 (+2b455e4, cfcf893) on feature/blackjax-smc-gradient-kernel; NOT pushed. THREE COMPOUNDING CAUSES, each MEASURED not guessed: (1) prior-whitening does NOT whiten the POSTERIOR — 269x anisotropy in prior-whitened coords (einstein_radius prior scale 8.0 vs posterior std 2e-4 => sigma_z 5.3e-5 vs 1.4e-2 loosest); scalar step tuned to mean is 88x too big for tightest => whiten by warm-start posterior scale; (2) DIAGONAL whitening insufficient — posterior CORRELATED (Laplace cov condition number 568, |r|=0.95 between 2 params) leaves a TILTED ridge => whiten by CHOLESKY of FULL covariance, add log|det L| to evidence; (3) step targeted REFERENCE width (sigma=1) but reference is INFLATED so posterior sigma~1/inflate => overshoot by inflate^2; MEASURED eps=1.148->acc 0.00, eps=0.1->acc 0.94 => auto step now targets posterior width (eps=0.287 @ inflate=2). ALSO FIXED an experiment-confounding bug: --step-size had a NUMERIC default so passing that same value explicitly was indistinguishable from not passing it -> silently auto-scaled -> a step bracket returned BYTE-IDENTICAL arms. Now default=None. Earlier fixed: MALA eps is a SQUARED length (proposal len=sqrt(2*eps)); tune callback 3-arg (rng_key,state,info); centre 1/r singularity custom_jvp mask; FLOAT32 sbatch [[reference_ral_sbatch_jax_x64_not_inherited]]. INFRA: _warm_start.py SHARED across stages (a)-(e) — multi-start Prodigy -> cached output/warm_start.json (mle + std + FULL cov + logL). EVIDENCE PRESERVED via geometric bridge from normalised Gaussian ref g: logprior_fn:=log g, loglikelihood_fn:=log prior+log L-log g (integral g=1 => true logZ), + LOG_PRIOR_NORM + log|det L| Jacobian. RESUME: (1) check 331058 /mnt/ral/jnightin/smc_grad_logs/smc_warm_ok-331058.out — KEY Q: does --tune HOLD acceptance near ~0.57 as lambda->1 (fixed step decays 0.80->0.17)? does HMC beat MALA? (2) compare logZ (~31690-31798) vs Nautilus + write comparison.txt row; (3) A100 rep-timing (GPUs were full); (4) stage (b) ChEES-HMC reusing _warm_start. NOTE RAL cached warm_start.json MUST be --refresh'd if it predates the cov field else silent diagonal fallback. MGE ONLY; pix deferred.
- worktree: ~/Code/PyAutoLabs-wt/blackjax-smc-gradient-kernel
- autonomy: supervised
- prompt: active/jax_native_posterior_sampler_wave.md
- note: WAVE TRACKER — stages (b) ChEES-HMC, (c) MCLMC+harmonic, (d) flowMC, (e) jaxns remain. Do NOT move prompt to complete/ on stage-(a) ship; issue next stage only as this one nears shipping (no bulk-issue). Concurrent worktree alongside parked pix-gradient-slogdet-revalidation claim (different files). Gradient path certified OK_HMC_VIABLE (probe_grad.py); baseline nss_grad row = logZ -31.47.
- repos:
  - autolens_workspace_developer

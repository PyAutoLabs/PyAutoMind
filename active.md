# Active Tasks


## no-run-config-purge
- issue: https://github.com/PyAutoLabs/HowToLens/issues/46
- status: workspace-dev — census COMPLETE, implementation not yet started. 50/122 no_run.yaml entries are zero-match (HowToLens 28/30, HowToGalaxy 15/16, autolens_workspace 7/27) plus 11 dead env_vars.yaml override patterns. Root cause is BIDIRECTIONAL COPY-PASTE between the HowTo* repos and their parent workspaces, not gradual drift — 18 of HowToLens' 28 dead entries name files that exist only in autolens_workspace, and autolens_workspace carries three HowTo tutorial stems in return. `plot/visuals` RESOLVED BY TEST: file moved scripts/plot/visuals.py -> scripts/guides/plot/examples/visuals.py in 9e1a50dc4 (2025-07-18) so the skip has not applied for a year; ran it under the real build env profile (autobuild repro_command) and it PASSES clean, exit 0 no output — entry dropped as stale, NOT re-spelled. Human approved purging ALL zero-match entries incl. bare-stem prospective guards.
- worktree: ~/Code/PyAutoLabs-wt/no-run-config-purge
- autonomy: supervised
- prompt: active/no_run_config_dead_entry_purge.md
- note: CONCURRENT CLAIM, HUMAN-APPROVED. All 5 repos are also claimed by `rename-autobuild-to-autohands` (parked, blocked on Heart RED, nothing committed). File sets verified DISJOINT: grep for autobuild|PyAutoHands|PyAutoBuild across every file this task edits returns nothing; the only build config naming PyAutoHands is markdown_examples.yaml, already renamed on main and NOT edited here. Separate branch + worktree. Brain Feature Agent said too-large(19)/split-into-phases; OVERRIDDEN with human approval — the score is repo-count-driven and the change is ~61 lines of YAML across 8 files with no code, API or docs surface. Config-only; no script, notebook or library edits expected. Clean repos are autolens_workspace_test (23 entries, 0 dead), autogalaxy_workspace, autofit_workspace, both other _test workspaces, HowToFit and the euclid pipeline — do NOT touch their no_run.yaml. markdown_examples.yaml and visualise_notebooks.yaml are clean everywhere. HowToFit is in scope ONLY for 2 dead env_vars patterns (it has no no_run entries) and was 1 commit behind origin/main at survey — pull before branching. Closes the "~44 zero-match entries remain, needs a deliberate call" item left open by the 2026-07-22 ell_comps/HowTo sweep.
- repos:
  - HowToLens: feature/no-run-config-purge
  - HowToGalaxy: feature/no-run-config-purge
  - autolens_workspace: feature/no-run-config-purge
  - HowToFit: feature/no-run-config-purge
  - autogalaxy_workspace_test: feature/no-run-config-purge

## rename-autobuild-to-autohands
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/177
- session: claude --resume 9f2ec381-2106-4eeb-bb89-d0a2e4aaf550
- status: blocked — PARKED AT THE SHIP GATE on Heart RED. Rename is COMPLETE and VERIFIED in the worktree but NOTHING is committed (AUTONOMY.md: RED forbids commit/push/PR-open at every autonomy level; the corrective-PR exception never fires under --auto and would not apply anyway, since this rename repairs no RED reason). Ship-time RED reasons: release validation FAILED (stage integrate); workspace validation 13 failed; 33 stale parked scripts; PyAutoFit/PyAutoGalaxy/PyAutoLens each 1 commit behind origin. Evidence: PyAutoHands 132 passed; PyAutoBrain 152 passed / 1 failed (test_skill_install missing `sizing` wrapper — PRE-EXISTING on main); repos_sync.py --check identical to main; autohands help renders; every PyAutoHands/autohands/<module> reference resolves. RESUME: wait for Heart to clear RED, then /ship_library merging Hands -> Heart -> Brain -> workspaces in ONE pass while CI is quiet.
- worktree: ~/Code/PyAutoLabs-wt/rename-autobuild-to-autohands
- autonomy: supervised (min of `supervised` header and the `safe` refactor cap)
- prompt: active/rename_autobuild_to_autohands.md
- note: EXPECT TO PARK AT THE SHIP GATE. Heart was RED (score 0) at launch — 13 test failures, 33 stale parked scripts, release validation integrate:fail. None caused by this task and the corrective-PR exception does not apply, so per AUTONOMY.md RED forbids commit/push/PR-open at every autonomy level. Landing is ATOMIC, no shim: merge order Hands -> Heart -> Brain -> workspaces, in one pass while CI is quiet, because the directory move breaks PyAutoHeart/workspace-validation.yml and every workspace run_smoke.py on merge. Brain Feature Agent said too-large(37)/split-into-phases; overridden with human approval (score is repo-count-driven and phases would violate atomic landing). PRESERVE: PyAutoBuild#NNN citations, rhayes777/PyAutoBuild url_fixups patterns, the pyautobuild->pyautohands policy alias, ~150 Mind historical records, planned.md:121 + dashboard.md:92 prompt-path pointers, and the two gitignored settings.local.json allowlists. Deep sweep caught PyAutoMind/scripts/repos_sync.py:558-570 (hard-coded autobuild dict keys, breaks silently) and ROUTING.md:38 as the only LIVE Mind files.
- caution: MAIN MOVED UNDER THIS WORKTREE 2026-07-23 (clone-skill-prefix-corruption, PyAutoBrain#150 — user-approved overlap). Expect a merge when you resume: (1) `PyAutoHands/autobuild/clone_seed.py` — main edited `substitute()` (+`import re`, docstring); this worktree has it as a pure `R autobuild/clone_seed.py -> autohands/clone_seed.py`, so git rename-detection should auto-resolve, but CHECK the merged file still has the `rule[2] == "word"` branch. (2) `PyAutoBrain/agents/conductors/clone/_clone.py` — main added a third element `"word"` to the skill-prefix rule at ~line 419; this worktree edits a different region (the clone_seed path string), so it should auto-merge. (3) `PyAutoHands/tests/test_clone_seed_substitute.py` is NEW on main and imports `from autobuild.clone_seed import substitute` — the rename must update that import too, or the new 16 tests break. Also unrelated: autocti_assistant/config/grids.yaml was deleted on main (#317), so it no longer exists to rename.
- caution: PyAutoMind is BOTH a worktree repo here (for repos_sync.py + ROUTING.md) and the task-state repo. Do every active.md / prompt_sync operation in the CANONICAL checkout (~/Code/PyAutoLabs/PyAutoMind, on main); only touch repos_sync.py + ROUTING.md inside the worktree. Different files, so they do not collide.
- repos:
  - PyAutoHands: feature/rename-autobuild-to-autohands
  - PyAutoBrain: feature/rename-autobuild-to-autohands
  - PyAutoHeart: feature/rename-autobuild-to-autohands
  - autolens_workspace: feature/rename-autobuild-to-autohands
  - autogalaxy_workspace: feature/rename-autobuild-to-autohands
  - autofit_workspace: feature/rename-autobuild-to-autohands
  - autolens_workspace_test: feature/rename-autobuild-to-autohands
  - autogalaxy_workspace_test: feature/rename-autobuild-to-autohands
  - autofit_workspace_test: feature/rename-autobuild-to-autohands
  - autocti_workspace_test: feature/rename-autobuild-to-autohands
  - HowToLens: feature/rename-autobuild-to-autohands
  - HowToGalaxy: feature/rename-autobuild-to-autohands
  - HowToFit: feature/rename-autobuild-to-autohands
  - autolens_assistant: feature/rename-autobuild-to-autohands
  - autofit_assistant: feature/rename-autobuild-to-autohands
  - autocti_assistant: feature/rename-autobuild-to-autohands
  - PyAutoMind: feature/rename-autobuild-to-autohands
  - admin_jammy: feature/rename-autobuild-to-autohands

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

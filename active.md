# Active Tasks

## interpolator-stale-needs-fix
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1411
- status: awaiting-merge — BOTH MARKERS STALE, 2 PRs open. Library bug was already fixed by PyAutoFit c8511b553 (2026-04-12), TWO DAYS AFTER the 2026-04-10 park; it added the `if not self.instances: raise IndexError` guard in autofit/interpolator/abstract.py:98 but shipped NO test. Reproduced on clean main with output/ moved aside: autofit_workspace features/interpolate exits 0 both real and under PYAUTO_TEST_MODE=1 (aggregator IS test-mode aware — finds outputs under output/test_mode/); HowToFit tutorial_5 exits 0. PRs: PyAutoFit#1412 (adds test_no_instances, 36 passed) + HowToFit#24 (removes marker). SCOPE CORRECTION: autofit_workspace needed NO change — its marker was already removed upstream by autofit_workspace PR#103 (7154e8a); my first grep hit a stale local main. Branch dropped there.
- worktree: none (in-place branches; 1 test + 1 yaml line)
- autonomy: supervised
- prompt: active/instance_interpolator_getitem_indexerror.md
- note: prompt's premise was WRONG twice — not a bracketing/off-by-one bug (t==1.5 always worked; test_interpolator.py covers it in 4 places), and HowToFit tutorial_5 contains ZERO interpolator code so the "likely related" attribution was never true. Real cause was an empty instances list reaching self.instances[0]. HowToFit no_run.yaml now has zero entries — safe, both PyAutoHands loaders do `no_run_data or []`.
- repos:
  - PyAutoFit: feature/interpolator-stale-needs-fix
  - HowToFit: feature/interpolator-stale-needs-fix


## group4-mge-search-benchmark
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/82
- status: workspace-dev — CODE COMPLETE (phases 1-3), BENCHMARK RUNS PENDING. Branch feature/group4-mge-search-benchmark pushed (bddedc5, no PR). DONE+VERIFIED: simulators/group4_mge.py (4 deflectors+4 sources, GROUP4_TRUTH single-source-of-truth, writes truth.json; preview shows 4 cores+arcs); searches/_setup.py dataset_class='group' _group_mge_model=54 free params (centres SEEDED near truth to break 4x4 permutation symmetry, geometry priors broad; AnalysisImaging; likelihood evals on numpy+JAX); searches/_recovery.py scores max_lh vs truth (theta_E+centre+shear, overall_pass); _runner recovery block; _samplers.py generic build_multi_start for adam/prodigy/lion/adabelief + multi_start_prodigy_autoconv (af.MultiStartGradientConvergence); 6 leaf scripts; sweep.py 6 group cells; README. ruff+smoke green. BLOCKER: multi_start_adam local CPU run sat 20min+ in JAX compile/pre-fit w/ ZERO steps — 54-param 8-galaxy vmap value_and_grad graph too heavy for CPU XLA. RESUME: (1) check if detached CPU run PID 25434 produced output/ or results JSON else kill; (2) RE-RUN ON LAPTOP GPU (~/venv/PyAutoGPU, JAX_PLATFORM_NAME=cuda JAX_PLATFORMS=cuda,cpu XLA_PYTHON_CLIENT_MEM_FRACTION=0.5, --config-name local_gpu_fp64) starting multi_start_adam then family then nautilus anchor; (3) if still too heavy dial _GROUP4_MGE_TOTAL_GAUSSIANS 10->6 and/or _MULTI_START_N_STARTS 64->32; (4) record recovery+walltime vs Nautilus, aggregate.py; (5) phase4 contingency = narrow-prior/warm-start init only if cold-start fails recovery. Env note: do NOT source worktree activate.sh locally (it repoints PYTHONPATH at /mnt/ral HPC); local libs resolve directly. Run w/ NUMBA_CACHE_DIR=/tmp/numba_cache MPLCONFIGDIR=/tmp/matplotlib PYAUTO_SKIP_WORKSPACE_VERSION_CHECK=1.
- worktree: ~/Code/PyAutoLabs-wt/group4-mge-search-benchmark
- autonomy: safe
- prompt: active/research_profiling_experiment_in_the_autolens_pr.md
- note: single repo autolens_profiling (workspace/research, no library edits). Phased: (1) simulator+truth, (2) model cell+recovery+Nautilus anchor, (3) gradient family sweep, (4) contingency = careful init (narrow-prior/warm-start) if cold-start fails recovery.
- repos:
  - autolens_profiling: feature/group4-mge-search-benchmark

## ep-hierarchical-scale-collapse
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1405
- status: reported — PyAutoFit exercised-not-edited (no worktree claimed). Cheap CPU toy diagnostic DONE; findings + minimal repro filed. Two defects reported: (1) hierarchical-EP parent scale hyperparameter COLLAPSE to ~0 with over-confident ~0 error (F10 guard misses it), (2) InitializerException hard-crash mid-EP. Awaiting fix-owner triage. slope_hierarchy#1 goal-2 write-up UNBLOCKED (comment posted).
- worktree: none (report-only; repro + findings in active/ep_scale_collapse_assets/)
- autonomy: supervised
- prompt: active/ep_hierarchical_scale_collapse.md
- note: spun out of slope_hierarchy#1 goal 2 to decide problem-specific vs framework. Verdict = framework stochastic instability (30 identical-problem runs: 21 RECOVER / 2 COLLAPSE / 7 CRASH), reproduces off-boundary (toy parent σ truth=10). Delta-method-boundary REFUTED; mechanism = over-shrinkage feedback basin. Ours is a stickier near-boundary variant.
- repos:

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


## slope-hierarchy
- issue: https://github.com/Jammy2211/slope_hierarchy/issues/1
- status: workspace-dev — ALL 4 GOALS ANSWERED. G1 NUTS ✓ (mean 2.028/sigma 0.143). G3 RAL pipeline ✓. G4 diagnostics ✓✓ (caught+fixed real projection bug, PR PyAutoFit#1383 MERGED). G2 = characterised partial parity: EP recovers parent MEAN (2.051, agrees NUTS) but converged SCATTER ~4× low (0.026 vs truth 0.1/NUTS 0.143), errors ~1000× too tight — documented EP scale-hyperparameter shrinkage (max_steps=5 snapshot 0.004 was under-converged; job 330639 max_steps=12 converged to 0.026, plateaued). NEXT (optional): N=25-50 scale-up (NUTS headline, EP cautionary) OR write-up. Not blocked.
- worktree: /mnt/c/Users/Jammy/Science/slope_hierarchy (external science project on its own main — no PyAutoLabs worktree; ic50_workspace-style non-standard)
- autonomy: supervised
- prompt: active/ep_hierarchical_power_law_slopes.md
- next: goal-2 fully answered; remaining is scale-up (N=25-50: edit simulator N + submit_* --array, rm output/<sample>/* before refits, force-sync truth files, verify RAL PyAutoFit mirror commit) or a methods write-up. NOTE repo now on autonerves (autoconf renamed, PRs #2/#3 landed 2026-07-18).
- note: hierarchical power-law slope recovery from N simulated imaging lenses — BlackJAX-NUTS joint fit vs EP parity (values AND errors), RAL scale-up, and end-to-end exercise of the 2026-07 EP diagnostics (PyAutoFit#1330 wave). PyAutoFit is exercised NOT edited: EP defects file as new bug prompts via intake. No PyAutoLabs repo claimed.
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
- status: workspace-dev — PARKED for resume. WIRING PROVEN (float64, end-to-end); NAIVE GRADIENT SMC DOES NOT CONVERGE (the stage-(a) finding). Committed LOCAL cfcf893 on feature/blackjax-smc-gradient-kernel (blackjax_smc_grad.py + smc_grad_cpu.sbatch + smc_gradient_findings.md); NOT pushed/shipped (no converging config yet). FINDING: MGE likelihood ~1000x sharper than prior → tempering needs step to shrink ~1000x; ALL 3 step regimes collapse acceptance (RAL job 330962/330959, float64, 64p): fixed 0.02 acc0.44→0; fixed-tiny 0.001 acc~0.8 + maxL IMPROVES -165k→-121k then collapses+crash; spread-adaptive --tune step too BIG(~0.6) acc frozen 0 → FALSE λ→1 jump (garbage logZ). Tiny-step improvement = gradient IS useful; blocker = step scheduling only. WARNING: 'Converged: yes' = merely λ reached 1.0, NOT real (force-jumps λ when acc~0). 5 BUGS FIXED: warmup cube-0.5-median (not prior-.mean); profile-CENTRE 1/r singularity→custom_jvp masks nonfinite grad→0; MALA SCALAR step→WHITEN z=params/prior_scale; tune callback (rng_key,state,info) 3-arg+step-from-state.particles; FLOAT32 trap [[reference_ral_sbatch_jax_x64_not_inherited]] export JAX_ENABLE_X64=True. NEXT LEVERS (resume, MOST PROMISING FIRST): (1) WARM-START particles from multi-start Adam basin (shorten tempering path, avoid step-scale gap — prompt's stage-c idea); (2) acceptance-feedback dual-averaging step control (needs outer loop/pretuning — standard inner_kernel_tuning callback doesnt expose prev step); (3) HMC --kernel hmc + posterior mass matrix; (4) A100 rep-timing (GPUs QUEUED FULL). ENV: isolated blackjax 1.5 at /mnt/ral/jnightin/scratch/smc_grad_pylibs (RAL venv had ancient 0.1.0b1); XLA-LLVM compile-mem crashes @128p/8step (use ≤64p/3step); laptop caps ~4p (16 OOMs @15GB) → RAL only. MGE ONLY; pix deferred.
- worktree: ~/Code/PyAutoLabs-wt/blackjax-smc-gradient-kernel
- autonomy: supervised
- prompt: active/jax_native_posterior_sampler_wave.md
- note: WAVE TRACKER — stages (b) ChEES-HMC, (c) MCLMC+harmonic, (d) flowMC, (e) jaxns remain. Do NOT move prompt to complete/ on stage-(a) ship; issue next stage only as this one nears shipping (no bulk-issue). Concurrent worktree alongside parked pix-gradient-slogdet-revalidation claim (different files). Gradient path certified OK_HMC_VIABLE (probe_grad.py); baseline nss_grad row = logZ -31.47.
- repos:
  - autolens_workspace_developer


## ell-comps-kwargs-keyerror
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/143
- status: AWAITING-MERGE (PR PyAutoLabs/HowToGalaxy#32 open, pending-release, MERGEABLE; commit a2dd056). SCOPE HALVED MID-TASK: autogalaxy_workspace half was ALREADY SHIPPED in PR #142 (merged 2026-07-21T21:06Z) — my local main was stale at 3c0c7e42 so I saw a marker that was already gone upstream; ALWAYS `git fetch` the target repo before trusting a marker, not just PyAutoMind. Remaining+shipped work = HowToGalaxy one-line deletion only. DIAGNOSIS SETTLED, both NEEDS_FIX markers are STALE. Root cause was library-side model-composition/kwargs drift, already fixed upstream between 2026-04 and 2026-07; NOT a stale call-site (model block byte-identical to marker commit 48dad395). DECISIVE TEST: the unmodified April-10 script run against today's installed library exits 0 with zero KeyError. HowToGalaxy's marker was NEVER valid — its entry is the literal path `autogalaxy_workspace/scripts/imaging/modeling`, copy-pasted from the workspace list; HowToGalaxy holds only chapter_*/ + simulators/, so the substring pattern matches ZERO files. Work = delete one line from each repo's config/build/no_run.yaml. No script changes → NO notebook regeneration. Smoke run timed 27.4s (<60s CI timeout), safe to un-park. PyAutoGalaxy dropped from scope.
- worktree: ~/Code/PyAutoLabs-wt/ell-comps-kwargs-keyerror
- autonomy: supervised
- heart-ack: YELLOW score 52 acknowledged 2026-07-22 — workspace validation not passing (10 failed, 2026-07-20T15-09-29Z); 58 stale parked script(s); 10 slow script(s); PyAutoCTI: open PR 1390d old. red_reasons empty. Ack does NOT extend to new reasons.
- prompt: active/ell_comps_kwargs_keyerror_imaging_modeling.md
- note: TRAP — running scripts/imaging/modeling.py regenerates dataset/database/simple__*/ FITS+JSON; restore with `git checkout -- dataset/` before committing (ship_workspace binary-leak). FOLLOW-UP (out of scope, same 2026-04-10 parking commit, likely stale for the same reason): `ellipse/modeling` KeyError on 'ellipses.0.centre_0', and `guides/advanced/over_sampling` plot_grid_lines kwarg.
- repos:
  - autogalaxy_workspace
  - HowToGalaxy

## convolver-gaussian-small-datasets-cap
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/397
- status: library-dev — plan approved, root cause CONFIRMED + fix empirically verified in scratch. Convolver.from_gaussian builds its kernel on Grid2D.uniform, which the PYAUTO_SMALL_DATASETS cap silently shrinks to 16x16, then wraps those 256 values in an Array2D at the caller's uncapped shape_native (31,31=961) -> ArrayException. Fix = pass respect_small_datasets=False at convolver.py:721 + numpy-only regression test in test_autoarray/operators/test_convolver.py.
- worktree: ~/Code/PyAutoLabs-wt/convolver-gaussian-small-datasets-cap
- autonomy: supervised
- prompt: active/mask_irregular_small_datasets_cap.md
- note: the prompt's own diagnosis (env-config gap, needs `unset: [PYAUTO_SMALL_DATASETS]` or mask capping) is WRONG — the traceback never reaches the mask code. Real library bug. NO workspace edits needed: autolens_workspace + autogalaxy_workspace scripts/imaging/data_preparation/manual/mask_irregular.py both go green off the library fix alone; HowToGalaxy/HowToLens do not carry the script. Latent same-bug sites at (21,21) are in non-executed fenced prose, and guides/ already unsets the flag.
- repos:
  - PyAutoArray: feature/convolver-gaussian-small-datasets-cap

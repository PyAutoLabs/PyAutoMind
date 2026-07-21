# Active Tasks


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
- status: workspace-dev — SCRIPT+WIRING DONE; CONVERGENCE IN PROGRESS on RAL CPU (job 330962 running). searches_minimal/blackjax_smc_grad.py = physical/WHITENED-space adaptive_tempered_smc, MALA/HMC(--kernel), JAX-native log_prior over 15 params, --tune=inner_kernel_tuning (spread-adaptive step). 4 BUGS FIXED: (1) warmup at cube-0.5 median not prior-.mean; (2) profile-CENTRE 1/r singularity at (0,0) → custom_jvp masks non-finite grad→0 (probe_grad GPU-only, symmetric median sits ON it); (3) MALA wants SCALAR step → WHITEN z=params/prior_scale (HMC=identity mass); (4) tune callback sig (rng_key,state,info) 3-arg + step from state.particles spread not prev-override. JOB HISTORY: 330955 script-mode-import→-m; 330958 FLOAT32→[[reference_ral_sbatch_jax_x64_not_inherited]] export JAX_ENABLE_X64=True; 330959 float64 CONFIRMED but FIXED-STEP MALA does NOT converge (acc 0.44→0 by step15, λ stuck 0.001 — likelihood ~1000x sharper than prior, prior-whitening under-conditions) +XLA-LLVM compile-mem crash @128p/8step. 330962 = spread-adaptive TUNE + smaller graph 64p/3step. RESUME: (1) ssh euclid_jump check 330962; log /mnt/ral/jnightin/smc_grad_logs/smc_grad_cpu-330962.out — KEY Q: does tune arm keep acc up + advance λ→1 (fixed arm2 tiny-step=0.001 control)? (2) pull output/blackjax_smc_grad_mala_tuned_summary.txt; max logL vs Nautilus -169k/nss_grad -31; (3) if tune converges → A100 rep-timing (GPUs full) + findings + comparison row; else reconsider (warm-start from multistart-Adam basin / Fisher precond). MGE ONLY; pix deferred. Isolated blackjax 1.5 at /mnt/ral/jnightin/scratch/smc_grad_pylibs (venv had ancient 0.1.0b1).
- worktree: ~/Code/PyAutoLabs-wt/blackjax-smc-gradient-kernel
- autonomy: supervised
- prompt: active/jax_native_posterior_sampler_wave.md
- note: WAVE TRACKER — stages (b) ChEES-HMC, (c) MCLMC+harmonic, (d) flowMC, (e) jaxns remain. Do NOT move prompt to complete/ on stage-(a) ship; issue next stage only as this one nears shipping (no bulk-issue). Concurrent worktree alongside parked pix-gradient-slogdet-revalidation claim (different files). Gradient path certified OK_HMC_VIABLE (probe_grad.py); baseline nss_grad row = logZ -31.47.
- repos:
  - autolens_workspace_developer

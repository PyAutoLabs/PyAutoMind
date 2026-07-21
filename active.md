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
- status: workspace-dev — SCRIPT DONE + WIRING PROVEN locally; RAL CPU convergence job 330958 QUEUED (330955 failed: script-mode import, fixed via python -m) (GPUs full). searches_minimal/blackjax_smc_grad.py = physical/WHITENED-space adaptive_tempered_smc, MALA(default)/HMC(--kernel hmc), JAX-native log_prior over 15 params, --tune=inner_kernel_tuning. 3 BUGS FIXED: (1) warmup at cube-0.5 median not prior-.mean (degenerate MGE point); (2) profile-CENTRE singularity 1/r at (0,0) → custom_jvp masks non-finite grad→0 (probe_grad only ran GPU, symmetric median sits ON the singularity); (3) MALA wants SCALAR step → WHITEN space z=params/prior_scale (HMC=identity mass). Laptop caps ~4 particles (16 OOMs @15GB), so quality meaningless locally → RAL. RESUME: (1) ssh euclid_jump 'squeue -u jnightin' check 330958; log /mnt/ral/jnightin/smc_grad_logs/smc_grad_cpu-330958.out; (2) pull searches_minimal/output/blackjax_smc_grad_{mala,mala_tuned}_summary.txt; assess max logL vs Nautilus -169k / nss_grad -31, logZ sanity, acc rate; (3) if converges → A100 job for representative timing (nextwave_a100.sbatch pattern; GPUs queued) + write smc_gradient_findings.md + comparison.txt row; (4) then HMC arm. Deliverable = blackjax_smc_grad.py + smc_gradient_findings.md + comparison row. MGE parametric ONLY; pixelized deferred.
- worktree: ~/Code/PyAutoLabs-wt/blackjax-smc-gradient-kernel
- autonomy: supervised
- prompt: active/jax_native_posterior_sampler_wave.md
- note: WAVE TRACKER — stages (b) ChEES-HMC, (c) MCLMC+harmonic, (d) flowMC, (e) jaxns remain. Do NOT move prompt to complete/ on stage-(a) ship; issue next stage only as this one nears shipping (no bulk-issue). Concurrent worktree alongside parked pix-gradient-slogdet-revalidation claim (different files). Gradient path certified OK_HMC_VIABLE (probe_grad.py); baseline nss_grad row = logZ -31.47.
- repos:
  - autolens_workspace_developer


## drop-interferometer-delaunay-marker
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/308
- session: claude --resume 37395538-a051-4b8d-8eeb-aa3f8df67454
- status: workspace-dev — MARKER-ONLY. interferometer/features/pixelization/delaunay now green on main (verified 3x, fresh data, smoke env); NEEDS_FIX stale. Fixed by recent concurrent work (prime suspect PyAutoArray#396 SMALL_DATASETS 15→16 even-cap; NOT the GaussianKernel PD-guard f1817af0 — this script uses ConstantSplit/AdaptSplit). Just drop the no_run.yaml entry. Latent (out of scope): analysis.py:175-182 numpy path wraps ANY error as FitException.
- worktree: ~/Code/PyAutoLabs-wt/drop-interferometer-delaunay-marker
- autonomy: supervised
- prompt: active/interferometer_delaunay_nonpd_fitexception.md
- repos:
  - autolens_workspace: feature/drop-interferometer-delaunay-marker

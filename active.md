# Active Tasks



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
- status: workspace-dev — goals 1/3/4 DONE; PR PyAutoFit#1383 (projection fix) MERGED. Goal 2 = PARTIAL PARITY: EP recovers parent MEAN (2.053, agrees NUTS 2.028/truth 2.0) but underestimates SCATTER (0.004 vs NUTS 0.143/truth 0.1); damping δ=0.5 makes it WORSE (full collapse, logZ→5e7). CONVERGENCE TEST overnight: RAL job 330639 (undamped, max_steps 5→12, ~3-4h)
- worktree: /mnt/c/Users/Jammy/Science/slope_hierarchy (external science project on its own main — no PyAutoLabs worktree; ic50_workspace-style non-standard)
- autonomy: supervised
- prompt: active/ep_hierarchical_power_law_slopes.md
- resume (2026-07-18 AM): (1) read job 330639: `ssh euclid_jump "grep -A3 'Parent recovery' /mnt/ral/jnightin/slope_hierarchy/hpc/batch_gpu/output/output.330639.out"` + collapse-count in ep_diagnostics.results; (2) PULL its ep_history.csv into repo results/ and inspect the parent-sigma trace over the 12 steps (did scatter grow toward 0.1 or stay ~0.004?); (3) if stayed crushed → goal-2 conclusion is 'EP gets mean, fundamentally misses scatter' (finalize parity table on issue #1, journal it) → then N=25-50 scale-up (simulate + submit chain; TRAPS: rm output/<sample>/ep before refits, force-sync truth files, verify RAL PyAutoFit mirror commit+content grep after any pull); if scatter grew → re-quote at converged max_steps. Also feed back to EP diagnostics: its 'try damping' hint is WRONG for this problem.
- note: hierarchical power-law slope recovery from N simulated imaging lenses — BlackJAX-NUTS joint fit vs EP parity (values AND errors), RAL scale-up, and end-to-end exercise of the 2026-07 EP diagnostics (PyAutoFit#1330 wave). PyAutoFit is exercised NOT edited: EP defects file as new bug prompts via intake. No PyAutoLabs repo claimed.
- repos:


## pix-gradient-slogdet-revalidation
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/112
- status: workspace-dev — BLOCKED-ON-RAL-CONNECTIVITY. Worktree created + harness toggle committed (a5b53a6 on feature/pix-gradient-slogdet-revalidation, NOT pushed). Next = launch the A100 A/B on RAL, but SSH euclid_jump is failing this session (too-many-auth-failures, then banner-exchange timeout through jump_finan). RESUME: (1) get SSH up (`! ssh -o IdentitiesOnly=yes euclid_jump hostname`; may need interactive key/2FA); (2) verify RAL PyAutoArray carries PR#392 `grep -rl log_det_method /mnt/ral/jnightin/PyAuto/PyAutoArray/autoarray/` (HPCPullPyAuto if stale); (3) sync worktree scripts to RAL; (4) run BOTH arms same seeds: baseline `PIX_LOGDET` unset (reproduce 330592 cholesky deaths) then `PIX_LOGDET=slogdet` (probe_nonfinite.sbatch, --partition=gpu --mem=64gb, ~5min ea); replay seed-0 rejected draws 12,35 — NOT last-finite recorded points; (5) measure survival%/min-death-step/step-0 NaN-grad count; (6) verdict into searches_minimal/pix_nonfinite_findings.md → ship_workspace.
- worktree: ~/Code/PyAutoLabs-wt/pix-gradient-slogdet-revalidation
- autonomy: supervised
- prompt: active/pix_gradient_landscape_revalidation.md
- note: verification tail of the pix-NaN lineage — localisation (#104/PR#105) + fix (PyAutoArray#392) + fitness-guard contract (PyAutoFit#1391) all shipped 2026-07-17. Toggle is env var PIX_LOGDET=slogdet threaded via al.Settings into build_analysis (one edit covers both pix_multi_start + pix_lr_free). Repro is A100-only (10.9 GiB/point OOMs laptop).
- repos:
  - autolens_workspace_developer: feature/pix-gradient-slogdet-revalidation (worktree live; commit a5b53a6 local-only)





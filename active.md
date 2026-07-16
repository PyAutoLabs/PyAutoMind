# Active Tasks


## survey-cutouts
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/50
- session: claude (CLI, 2026-07-16)
- status: library-shipped, awaiting-merge — PR PyAutoReduce#51 (pending-release); shipped through unrelated Heart RED on contemporaneous user ack 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/51
- heart-ack: PyAutoLens uncommitted source; workspace validation 3-failed (2026-07-09); 58 stale parked scripts; manifest drift tenant-firewall ×6; install verification not run; release validation stale (5 libs)
- worktree: ~/Code/PyAutoLabs-wt/survey-cutouts
- autonomy: safe (--auto; feature≤medium cap)
- prompt: active/ground_based_instruments_optional_noise_psf.md
- note: third adapter domain "cutout" — fetch+package pre-reduced survey coadds for color context (legacy_surveys/DES griz + invvar noise, sdss via astroquery, panstarrs fitscut); noise/PSF explicitly optional; HSC auth-gated deferred; unWISE/GALEX assessment in docs/design/surveys.md.
- repos:
  - PyAutoReduce: feature/survey-cutouts

## test-mode-representative-samples-phase-1-design
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1378
- session: claude --resume fceb9fd4-59ed-4cb4-acc0-bd4c04c23839
- status: library-dev (design-only phase — no source edits, no worktree; claims NO repos)
- worktree: none (phase 2 creates ~/Code/PyAutoLabs-wt/test-mode-representative-samples)
- autonomy: supervised
- prompt: active/test_mode_representative_outputs_size_realistic_phase_1_design.md
- note: phase 1/4 of the test-mode size-realistic-samples umbrella (draft/feature/autofit/test_mode_representative_outputs_size_realistic.md). DESIGN COMPLETE 2026-07-16 — D1-D4 posted (#1378 comment): knob PYAUTO_TEST_MODE_SAMPLES default 4 / accessor in autoconf via existing autofit shim / N==4 literal branch untouched / N>4 vectorized numpy -> production Sample.from_lists path / weights exp(-i/(N/10)) w_min>=4.5e-10 at N<=1e5 (threshold 1e-10; bypass write path never prunes — updater.py only). Production parity target measured: 10,187 rows x 21 cols = 9.07 MB (hst_fast source_lp[1]). Awaiting human validation of D1-D4, then close #1378 + issue phase 2 once aggregator-sqlite's PyAutoFit claim frees (#1376 awaiting merge).
- repos:

## aggregator-sqlite
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1377
- session: claude --resume aa483bab-3f5b-4ffe-b121-c968ff80ffae
- status: library-dev (bug — assessment-first; source fixes checkpointed after the failure survey)
- worktree: ~/Code/PyAutoLabs-wt/aggregator-sqlite
- autonomy: supervised
- prompt: active/exercise_fix_and_assess_the_sqlite_results.md
- note: aggregator Phase D (goal 3 of #1375): exercise sqlite scrape/build with the merged mock harness, cheap fixes only, written assessment of the direct-write (session) path; add database build/query stages to the profiling grid. "If its hard to fix dont bother."
- repos:
  - PyAutoFit: feature/aggregator-sqlite
  - autofit_workspace_test: feature/aggregator-sqlite


## jax-compile-time-research
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/71
- session: claude (CLI bg job b44b0e0f, 2026-07-16)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/jax-compile-time-research
- autonomy: supervised (--auto; research cap)
- prompt: active/jax_compile_time_is_prohibitive_for_complex.md
- note: parallel-claim override (user-approved 2026-07-16): slam-resume-profiling (#70) also claims autolens_profiling — different subtrees (it owns slam/resume paths; this task adds NEW jax_compile/ dir only, touches nothing existing). Research deliverable = compile-time probe + research note answering "jit boundaries in source vs settings/small changes". autolens_workspace_developer is READ-ONLY evidence (claimed by pixelized-gradient-experiment). Companion (separate task): draft/feature/autolens_profiling/jax_compile_time_profiling.md industrializes the probe. Established: autotune ruled out; lax.map scan-of-vmap >> plain value_and_grad (7m36s vs >30min same fusion); persistent cache warming in play on RAL job 330513.
- repos:
  - autolens_profiling: feature/jax-compile-time-research

## cti-resurrection-phase0
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/82
- session: claude (CLI, 2026-07-16)
- status: library-shipped, awaiting-merge — PR PyAutoCTI#83 (pending-release); tests 236p/5s
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/83
- heart-ack: 2026-07-16 human ack of RED for PR-open (6 pre-existing CTI-unrelated reasons: PyAutoLens uncommitted source; workspace validation 3-failed 2026-07-09; 58 stale parked scripts; manifest drift tenant-firewall ×6; install verification not run; release validation stale 5 libs); merge stays human
- worktree: ~/Code/PyAutoLabs-wt/cti-resurrection-phase0
- autonomy: supervised
- prompt: active/cti_resurrection_phase0_resurrect_and_register.md
- note: Phase 0 of the CTI resurrection epic (6 phases; later phases get own prompts). Org transfer Jammy2211→PyAutoLabs DONE. arcticpy 2.6 WORKS on py3.12/numpy2.2 (needs libgsl-dev headers; naive pip install DOWNGRADES numpy — use --no-build-isolation --no-deps; recipe in PyAutoCTI/AGENTS.md). Viz layer quarantined for Phase 1 (Plotter→matplotlib). 5 aggregator tests skipped for Phase 2 (analysis summing → AnalysisFactor/FactorGraphModel). Next after merge: Phase 1 viz-migration prompt. Follow-ups: worktree.sh doesn't know CTI repos (Phase 3); ag ellipse_multipole.yaml still has stale gaussian_limits (latent bug, file separately).
- repos:
  - PyAutoCTI: feature/cti-resurrection-phase0


## jax-joss-benchmarks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/281
- status: workspace-dev — repo born+pushed (10 benchmarks), workspace branch pushed (3 start_here real-data rewrites + 2 new joint scripts + rxj1131/a2744 datasets); smokes running locally; A100 job 330501 queued on RAL; SDP.81 leg blocked on CASA export (data_prep shipped)
- worktree: ~/Code/PyAutoLabs-wt/jax-joss-benchmarks
- autonomy: supervised
- prompt: active/autolens_jax_joss_benchmark_repo.md
- note: 5-phase epic (one-shot attempt per user); new repo autolens_jax_joss (PyAutoLabs, public) born alongside; datasets SDP.81 / RXJ1131 / A2744 user-approved
- repos:
  - autolens_workspace: feature/jax-joss-benchmarks
  - autolens_jax_joss: main (born this task)


## coolest-standard-support
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/612
- session: claude --resume 5c96151b-044f-49e4-aa35-e01ceb863124
- status: library-shipped, workspace-pending
- worktree: ~/Code/PyAutoLabs-wt/coolest-standard-support
- autonomy: supervised
- prompt: active/coolest_standard_support.md
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/501 (merge first), https://github.com/PyAutoLabs/PyAutoLens/pull/613
- note: shipped through Heart RED (6 pre-existing unrelated reasons) on user ack 2026-07-16. Phase C after merge: minimal autolens_workspace COOLEST guide + workspace_test round-trip script. Follow-up prompt draft/feature/autolens/coolest_powerlaw_herculens_parity.md stays in draft until this merges
- repos:
  - PyAutoGalaxy: feature/coolest-standard-support
  - PyAutoLens: feature/coolest-standard-support




## env-profile-validator
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/161 (migration step 1; epic #155)
- status: library-dev → shipping
- worktree: ~/Code/PyAutoLabs-wt/env-profile-validator
- autonomy: supervised
- repos:
  - PyAutoBuild: feature/env-profile-validator

## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: coordinating — Phases 0-2 shipped/awaiting-merge: 0a+#157/#158/#159/#160+audit#84 MERGED; 0b Brain#128 PR-open; fix-1 Heart#85 PR-open. Next: Phase 3 (env-profile brief), Phase 4 (version fork + version_skew rework + README pins + installable-floors invariant), Phase 5 (agent failure modes). Satellites: howto simulator stage; verify_install exercise run pairs with next rehearsal
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:


## slope-hierarchy
- issue: https://github.com/Jammy2211/slope_hierarchy/issues/1
- status: workspace-dev — GOAL 1 ACHIEVED: warm-started NUTS parent mean 2.028 [2.000,2.063] / sigma 0.143 [0.117,0.185] vs truth 2.0/0.1 (job 330508, 1h42m A100; cold start FREEZES — warm start from one_by_one medians mandatory). Per-lens recovery clean after over-sampling fix ([8,4,2]). Undamped EP sigma-COLLAPSED and the #1335 F10 diagnostics CAUGHT it (goal 4 validated); damped EP delta=0.5 = RAL job 330532 IN FLIGHT (goal-2 parity next). Upstream prompts filed: feature/autofit/ep_optimise_expose_updater_delta.md, bug/autolens_assistant/hpc_sync_first_push_race.md. Traps: see wiki/project/2026-07-16-first-science-results.md
- worktree: /mnt/c/Users/Jammy/Science/slope_hierarchy (external science project on its own main — no PyAutoLabs worktree; ic50_workspace-style non-standard)
- autonomy: supervised
- prompt: active/ep_hierarchical_power_law_slopes.md
- note: hierarchical power-law slope recovery from N simulated imaging lenses — BlackJAX-NUTS joint fit vs EP parity (values AND errors), RAL scale-up, and end-to-end exercise of the 2026-07 EP diagnostics (PyAutoFit#1330 wave). PyAutoFit is exercised NOT edited: EP defects file as new bug prompts via intake. No PyAutoLabs repo claimed.
- repos:

## pixelized-gradient-experiment
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/100
- status: in-progress — A100 pipeline WORKING. Gradient question SETTLED (yes). Search question OPEN. Nautilus baseline 330513 COMPLETE 2026-07-16 (1h32: 1h10 compile + 22m sampling): CONVERGED 27840 calls, N_eff 1233, logZ +17345.4, max logL +17418.9 at r_E=1.3102 — inside slack 0.3 tol by 0.01 only; 8k nats BELOW the FD probe's +25537 truth point (which IS in-model) → reads as pixelized source-degeneracy dominant mode. Optimizer bar = +17419 (adam's -39888 is 57k nats under it). RAL compile cache now WARM; pixgrad_pyautofit worktree safe to delete.
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (autolens_workspace_developer on feature/pixelized-gradient-experiment, pushed, NOT PR'd)
- autonomy: supervised (research)
- SETTLED: pix likelihoods ARE gradient-differentiable. A100 FD probe (kernel-CDF RectangularKernelAdaptDensity(bandwidth=0.1), os_pix=1, x64): every mass/shear param FD-matched ~1e-6 (einstein_radius rel=8.8e-7), logL +25537 at a truth-centred point. My earlier "no" was a methodology error (human caught it). NEVER use adaptive meshes at os_pix=1 (certified staircase = dead mass gradient); kernel-CDF is live at os_pix=1, adaptive needs os_pix=4.
- SHIPPED: PyAutoFit#1374 batch_size (merged 7262f832) — unbatched pix multi-start OOMs 80GB A100 (58.13 GiB jvp fusion); batch_size=4 completed a full f64 fit. Do NOT use fp32 (science compromise) or apply_sparse_operator (human: separate question, may slow the likelihood).
- OPEN (the real question): adam ran ONCE — wall 2090s, max logL -39888, einstein_radius 1.4169 (truth 1.6), per-start basin 0/16. "IN TRUTH BASIN: True" is an ARTIFACT of a slack 0.3 tol — do not trust it. logL -39888 vs the probe's +25537 at truth = the optimizer did NOT find the basin. Suspects: n_steps=300 too few from broad starts; lr=1e-2 mis-scaled; my per-start diagnostic indexing may be wrong.
- resume: (1) read Nautilus 330379 result (/mnt/ral/jnightin/pixgrad_logs/samp_pixgrad_nautilus_330379.log) — if Nautilus ALSO misses the basin, the model/priors are at fault, not the gradient optimizer; (2) then debug adam (steps/lr/diagnostics); (3) then adabelief + lion. Only adam has run — no ADABelief/Lion/Nautilus results yet.
- RAL: shared /mnt/ral/jnightin/PyAuto/PyAutoFit left CLEAN on main (human's release version-bumps in README/docs/paper preserved). My isolated PyAutoFit worktree /mnt/ral/jnightin/pixgrad_pyautofit (batch_size branch, now merged to main) is PYTHONPATH-prepended by the sbatch and still used by job 330379 — safe to delete once it finishes, then the shared mirror on main suffices.
- TRAPS: foreground `timeout ssh` does NOT kill the remote side (it severed a git op, leaving a stale index.lock + half-applied checkout in the SHARED mirror) — use nohup+setsid+sentinel. Nautilus on a JAX row MUST set force_x1_cpu=True + use_jax_vmap=True (else fork corrupts JAX state) and n_batch<=16 without the sparse operator (default 100 needs ~100GB).
- intakes filed: draft/feature/autolens_profiling/jax_compile_time_profiling.md (Fable, tomorrow — compile is ~all the wall time; autotune RULED OUT: 2100s vs 2090s identical), draft/refactor/autofit/split_fitness_batch_size_lh_vs_latent.md
- repos:
  - autolens_workspace_developer: feature/pixelized-gradient-experiment

## slam-resume-profiling
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/70
- session: claude --resume ce78c7e9-3f34-4983-bb53-8840527c1fb6
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/slam-resume-profiling
- prompt: active/slam_resume_overhead_profile_inter_stage_costs.md
- repos:
  - autolens_profiling: feature/slam-resume-profiling

## lr-free-multi-start-optimizers
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/101
- status: workspace-dev — GATE ANSWERED (see #100 entry: Nautilus +17419 @ r_E 1.31 = optimizer bar). Phase 1 MGE (laptop GPU 12x300): prodigy (lr-free) RECOVERS TRUTH +31787.9 r_E 1.600; ademamix +31786; adopt+adam in-basin; remaining 6 rules re-running detached (first run killed by session teardown — summaries for dog/mechanic/momo/schedule_free/dowg/dadapt in output/ are STALE SMOKE artifacts until rerun lands). Phase 2a SUBMITTED: adam lr sweep RAL jobs 330529/330530/330531 (PIX_LR=1e-3/3e-3/3e-2, 16 starts, batch 4, warm cache). Phase 2b (lr-free rules on pix) needs a standalone pix_lr_free.py — af.AbstractMultiStartGradient inits optimizer state on the STACKED params, which couples the lr-free rules' global scalar estimates across starts (library promotion must vmap init/update)
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (STACKED branch feature/lr-free-multi-start-optimizers on feature/pixelized-gradient-experiment; repo claim shared with #100 by design, user-approved, precedent #97-on-#96)
- autonomy: supervised (experiment)
- prompt: active/lr_free_multi_start_optimizers.md
- sibling drafts: draft/research/autolens_workspace_developer/jax_native_posterior_sampler_wave.md (issue when this ships — do not bulk-issue)
- repos:
  - autolens_workspace_developer: feature/lr-free-multi-start-optimizers

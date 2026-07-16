# Active Tasks


## eyes-paper-critique
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/117
- session: claude --resume 4a4bf99d-519c-4acc-9ac7-036e2850c56f
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/eyes-paper-critique
- autonomy: supervised
- prompt: active/eyes_paper_informed_critique.md
- parent: eyes-agent epic (#117, Phase 3 of 3 — FINAL; Phases 1+2 MERGED). Epic closes when this ships
- note: small core addition (eyes review --against <reference-dir> + optional `reference` note-schema field) + skill-prose Phase-3 step; first real paper run deferred to the /eyes maiden voyage
- repos:
  - PyAutoBrain: feature/eyes-paper-critique

## test-mode-representative-samples-phase-1-design
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1378
- session: claude --resume fceb9fd4-59ed-4cb4-acc0-bd4c04c23839
- status: library-dev (design-only phase — no source edits, no worktree; claims NO repos)
- worktree: none (phase 2 creates ~/Code/PyAutoLabs-wt/test-mode-representative-samples)
- autonomy: supervised
- prompt: active/test_mode_representative_outputs_size_realistic_phase_1_design.md
- note: phase 1/4 of the test-mode size-realistic-samples umbrella (draft/feature/autofit/test_mode_representative_outputs_size_realistic.md). Deliverable = D1-D4 locked design decisions posted on #1378. Phase 2 (core API) blocked-by aggregator-sqlite's PyAutoFit claim (#1376 awaiting merge); issue phase 2 only as this nears shipping.
- repos:

## consolidation-sweep
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/48
- session: claude (CLI, 2026-07-16)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/consolidation-sweep
- autonomy: safe (--auto; refactor cap)
- prompt: active/consolidation_sweep.md
- note: behaviour-preserving consolidation: adapter-owned max_single_exposure_seconds (pipeline._psf branches), shared psf/moments.moment_fwhm, jwst_rms fold into rms, cache_inject gitignore rider. Witness: test_autoreduce (229/3skip baseline).
- repos:
  - PyAutoReduce: feature/consolidation-sweep

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
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cti-resurrection-phase0
- autonomy: supervised
- prompt: active/cti_resurrection_phase0_resurrect_and_register.md
- note: Phase 0 of the CTI resurrection epic (6 phases; later phases get own prompts). Org transfer Jammy2211→PyAutoLabs DONE 2026-07-16 (user-approved). Scope: workspace clone + repos.yaml registration, arcticpy 2.6 spike (hard C++ dep, THE risk), setup.py→pyproject floors, non-viz import fixes, unit tests green with plot subpackage quarantined for Phase 1 (viz Plotter→matplotlib migration).
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


## pre-build-slim
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/156 (Phase 1 step 3; epic #155)
- status: library-shipped, awaiting-merge — PR PyAutoBuild#160 (sweep vestige deleted)
- library-pr: https://github.com/PyAutoLabs/PyAutoBuild/pull/160
- worktree: ~/Code/PyAutoLabs-wt/pre-build-slim
- autonomy: supervised
- repos:
  - PyAutoBuild: feature/pre-build-slim

## heart-testrun-wiring
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/83 (fix 1 of the audit; epic PyAutoBuild#155)
- status: library-shipped, awaiting-merge — PR PyAutoHeart#85
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/85
- worktree: ~/Code/PyAutoLabs-wt/heart-testrun-wiring
- autonomy: supervised
- repos:
  - PyAutoHeart: feature/heart-testrun-wiring

## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: coordinating — Phases 0-2 shipped/awaiting-merge: 0a+#157/#158/#159/#160+audit#84 MERGED; 0b Brain#128 PR-open; fix-1 Heart#85 PR-open. Next: Phase 3 (env-profile brief), Phase 4 (version fork + version_skew rework + README pins + installable-floors invariant), Phase 5 (agent failure modes). Satellites: howto simulator stage; verify_install exercise run pairs with next rehearsal
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:


## slope-hierarchy
- issue: https://github.com/Jammy2211/slope_hierarchy/issues/1
- status: workspace-dev — Phases 1-3 scripts SHIPPED + smoke-tested (sim verified exact truth-logL round-trip; NUTS jax.grad through full hierarchical graph CONFIRMED via 1-dataset probe, compile-dominated on CPU). Phase 4 IN FLIGHT: RAL job 330484 (one_by_one ×5, gpu) running under monitor; graphical+ep submit next. Traps fixed: lp_snr intensity not serialized; hpc/sync first-push race (bug prompt filed); PROJECT_PATH/PYAUTO_HPC_BASE not in sbatch env
- worktree: /mnt/c/Users/Jammy/Science/slope_hierarchy (external science project on its own main — no PyAutoLabs worktree; ic50_workspace-style non-standard)
- autonomy: supervised
- prompt: active/ep_hierarchical_power_law_slopes.md
- note: hierarchical power-law slope recovery from N simulated imaging lenses — BlackJAX-NUTS joint fit vs EP parity (values AND errors), RAL scale-up, and end-to-end exercise of the 2026-07 EP diagnostics (PyAutoFit#1330 wave). PyAutoFit is exercised NOT edited: EP defects file as new bug prompts via intake. No PyAutoLabs repo claimed.
- repos:

## pixelized-gradient-experiment
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/100
- status: in-progress — A100 pipeline WORKING. Gradient question SETTLED (yes). Search question OPEN. Nautilus baseline: 330379 CANCELLED at 1h07 mid input_reduce_fusion compile (never sampled); RE-SUBMITTED as job 330513 (2026-07-16, 12h limit, cache dir already set — compile must complete once to warm it). Log: pixgrad_logs/samp_pixgrad_nautilus_330513.log.
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
- status: workspace-dev — phase 1 (MGE local wiring) starting; pixelized phase GATED on #100's Nautilus arbiter (330379 cancelled mid-compile; re-submitted as 330513, 12h, 2026-07-16 — cache dir was already set, it needed wall time)
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (STACKED branch feature/lr-free-multi-start-optimizers on feature/pixelized-gradient-experiment; repo claim shared with #100 by design, user-approved, precedent #97-on-#96)
- autonomy: supervised (experiment)
- prompt: active/lr_free_multi_start_optimizers.md
- sibling drafts: draft/research/autolens_workspace_developer/jax_native_posterior_sampler_wave.md (issue when this ships — do not bulk-issue)
- repos:
  - autolens_workspace_developer: feature/lr-free-multi-start-optimizers

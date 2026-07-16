# Active Tasks


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


## community-ears-v2-prs
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/125
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/community-ears-v2-prs
- autonomy: human-required
- prompt: active/community_ears_v2_external_prs.md
- note: community conductor v2 — scan/triage hear external PRs + review requests. Parallel-PR override (user "go"): ic50-assistant-seed claims PyAutoBrain but is clone/-only (PR #120, zero overlap); retire-complete-ledger claim is STALE (Brain PR #123 merged, worktree deleted).
- repos:
  - PyAutoBrain: feature/community-ears-v2-prs


## simulate-injection-feasibility
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/44
- session: claude (CLI, 2026-07-16)
- status: library-shipped, awaiting-merge — PR PyAutoReduce#45 (pending-release); shipped through unrelated Heart RED on user ack 2026-07-16 ("go" at resume, recorded on #44)
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/45
- heart-ack: PyAutoLens uncommitted source; workspace validation 3-failed (2026-07-09); 58 stale parked scripts; manifest drift tenant-firewall ×2; install verification not run; release validation stale (5 libs)
- worktree: ~/Code/PyAutoLabs-wt/simulate-injection-feasibility
- autonomy: supervised (--auto; research cap)
- prompt: active/simulated_lens_through_reduction_pipeline.md
- note: research deliverable = docs/design/simulate.md feasibility verdict (frame-level injection + simobserve) + phased follow-up prompts; docs-only, no autoreduce/ source edits.
- repos:
  - PyAutoReduce: feature/simulate-injection-feasibility

## aggregator-profiling
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1375
- session: claude --resume aa483bab-3f5b-4ffe-b121-c968ff80ffae
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/aggregator-profiling
- autonomy: supervised
- prompt: active/aggregator_profiling_harness_and_result_loading.md
- note: Phase A harness (autofit_workspace_test scripts/profiling/aggregator/) then Phase B speedups (PyAutoFit aggregator). autolens_workspace_test leg deferred — repo claimed by viz-render-gallery. sqlite (goal 3) = separate follow-up prompt when A+B near ship.
- repos:
  - PyAutoFit: feature/aggregator-profiling
  - autofit_workspace_test: feature/aggregator-profiling


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

## ic50-assistant-seed
- issue: https://github.com/Jammy2211/ic50_assistant/issues/1
- status: awaiting-input — Phase 1 (seed) shipped; Phases 2-4 (domain adaptation) authored+pushed; Phase 5 demonstrations RUN (goals 1-3 ✅: ep_sim 33/33 within 3σ, EP scaling ~linear, real drug_1003/1073 fits; goal 4 partial — LS↔EP done, random_forest blocked → ic50_workspace#8). PARKED at ship sign-off (supervised --auto) — human opens/merges domain-adaptation PR
- question: https://github.com/Jammy2211/ic50_assistant/issues/1#issuecomment-4990016860
- worktree: ~/Code/PyAutoLabs-wt/ic50-assistant-seed
- autonomy: supervised
- prompt: active/build_ic50_assistant_from_autofit_assistant.md
- note: build ic50_assistant (PyAutoFit domain assistant, EP/graphical IC50) seeded from autofit_assistant. Phase 1 = Clone Agent reference-profiled (PyAutoBrain#120 + autofit_assistant#11, OPEN) + PRIVATE Jammy2211/ic50_assistant born (c3487afc1). Phases 2-4 = domain adaptation on ic50_assistant branch feature/ic50-domain-adaptation (b404fc2, pushed, NO PR yet — supervised parks at ship): AGENTS reframe, profile, literature wiki (5 real papers), 6 ic50_* skills, HPC skill; validated (citations/links/tests green). Phase 5 = execute the fits (some HPC-scale) — checkpoint compute first. Downstream: ic50_workspace → closed science repo. PyAutoBrain claim: clone/-only parallel PR, no overlap, user-approved.
- repos:
  - PyAutoBrain: feature/ic50-assistant-seed
  - autofit_assistant: feature/ic50-assistant-seed
  - ic50_assistant: feature/ic50-domain-adaptation (pushed; PR awaiting human sign-off)



## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: coordinating — 0a MERGED; 0b parser fix queued (Brain claims); Phase 1 DONE (#157/#158/#159 merged; step 3 parked on dataset/config-sweep decision); Phase 2 (heart-evidence-audit) in flight
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
- status: in-progress — A100 pipeline WORKING. Gradient question SETTLED (yes). Search question OPEN. Nautilus baseline job 330379 running on RAL (submitted 2026-07-15, 4h limit).
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

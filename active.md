# Active Tasks


## inject-jwst
- issue: https://github.com/PyAutoLabs/PyAutoReduce/issues/52
- session: claude (CLI, 2026-07-16)
- status: library-shipped, awaiting-merge — PR PyAutoReduce#53 (pending-release); shipped through unrelated Heart RED on contemporaneous user ack 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/53
- heart-ack: PyAutoLens uncommitted source; workspace validation 3-failed (2026-07-09); 58 stale parked scripts; manifest drift tenant-firewall ×6; release validation stale (5 libs) — note install-verification cleared vs earlier lists
- worktree: ~/Code/PyAutoLabs-wt/inject-jwst
- autonomy: supervised (--auto; Feature Agent sized large)
- prompt: active/inject_stage_jwst.md
- note: phase 2a of simulate.md — JWST _cal injection; input contract Jy/pixel (flux-exact via PIXAR_SR; nominal e_per_dn=2 shapes Poisson width only, disclosed); ERR variance added pre-image3; gate widens to jwst_image3. 2b (Keck registration design) stays in draft.
- repos:
  - PyAutoReduce: feature/inject-jwst

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
- session: claude (CLI, resumed 2026-07-16 evening; was bg job b44b0e0f)
- status: workspace-dev — MGE CPU matrix DONE (grad ≈ 13-15× jit compile; lax.map∘vag 47×); persistent cache CERTIFIED locally (warm 117s→2.3s, 51×; trace ~14s uncacheable); RAL 330513 confirmed 1h10m fusion DID serialize (1.7MB entry); A100 warm-repeat job 330534 pending (nautilus 0 16 — args MUST match or shapes miss cache); local pixelization jit+vag CPU probe running. Remaining: pix numbers, A100 warm verdict, piecewise-jit prototype (cold-compile half of core question)
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
- status: workspace-shipped, awaiting-merge — PR autolens_workspace#282 open (pending-release, notebooks regenerated); JOSS repo live with 10 benchmarks; 4 official A100 rows on RAL (point_source 5.95m / group 8.44m / imaging 10.0m / weak 0.75m). OVERNIGHT: RAL 330501 (cluster, 7h+ at bedtime) + 330527 (strong_and_weak -> imaging_and_point_source -> multi_band -> imaging --search nautilus). RESUME: (1) check both job logs + pull results/*.json from /mnt/ral/jnightin/autolens_jax_joss/results/ -> commit to JOSS repo + regen RESULTS.md; (2) resubmit clean viz-off re-timings of point_source/group/imaging (330501 rows carry viz overhead); (3) local saw_smoke2 (weak/features/strong_lensing/a2744.py TEST_MODE) died with session — optional, A100 strong_and_weak validates same composition; (4) final issue update + offer merge. FINDINGS: imaging cold-start Adam missed basin (logL -3e7, known open search question) -> nautilus row queued; cluster >>5min target, needs tuning (point-solver depth x 7 sources); weak JAX-viz crash = PyAutoLens#614
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





## agent-failure-modes
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/130
- status: library-shipped, awaiting-merge — doc PR PyAutoBrain#131
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/131
- worktree: none (manual worktree for the doc branch)
- autonomy: supervised
- prompt: active/agent_failure_modes_structural_mitigations.md
- parent: build-chain-umbrella (Phase 5, epic PyAutoBuild#155)
- repos:

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
- resume: (1) read damped-EP job 330532 (submitted 2026-07-16 ~18:00, delta=0.5, 12h limit): `ssh euclid_jump "grep -A3 'Parent recovery' /mnt/ral/jnightin/slope_hierarchy/hpc/batch_gpu/output/output.330532_0.out"` + its ep_diagnostics.results (did damping cure the F10 collapse?); (2) scp results/ep_sample_n5_seed42_delta0.5.json back; (3) build the goal-2 parity table EP-vs-NUTS (NUTS numbers in results/graphical_nuts_sample_n5_seed42.json) and post to issue #1; (4) if parity holds → scale-up sample (N=25-50, new simulate + resubmit chain; remember output-clear + truth-file force-sync traps); if collapse persists → try delta 0.2-0.3 or per-factor sampler optimisers per the F10 hint
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
- status: workspace-dev — harness pushed (9129d49+0af2d6e); --fast chain running detached overnight (setsid python, pid in scratchpad slam_fast.pid, log slam_fast_cold3.log; stage 2/5 sampling at bedtime)
- worktree: ~/Code/PyAutoLabs-wt/slam-resume-profiling
- prompt: active/slam_resume_overhead_profile_inter_stage_costs.md
- note: resume checklist = (1) check overnight run: output/pipeline_resume/hst_fast/ stage dirs + results/pipeline_resume/*_fast.json (record will be mode=partial — stages 2-5 sampled); (2) rerun `python3 pipeline_resume/slam_resume.py --fast` for the PURE resume record; (3) decomposition sanity → full-fidelity cold+resume (no --fast; n_batch 50/20 needs uncontended RAM, OOM'd twice at higher batch); (4) judgment on #70 — key pre-findings: adapt images already persisted per stage in files/ + agg_util.adapt_images_from loader exists (targeted load-not-recompute beats checkpoint system); resume also pays zip→unzip per stage; test-mode sibling PyAutoFit#1378 makes cold runs instant later. Parallel claim: jax-compile-time-research adds jax_compile/ only, no overlap.
- repos:
  - autolens_profiling: feature/slam-resume-profiling

## lr-free-multi-start-optimizers
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/101
- status: workspace-dev — phase 1 COMPLETE, phase 2a COMPLETE (negative), phase 2b OVERNIGHT job 330535
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (branch feature/lr-free-multi-start-optimizers @ 555eb4e, STACKED on #100's branch, pushed; RAL checkout synced to same commit)
- autonomy: supervised (experiment)
- prompt: active/lr_free_multi_start_optimizers.md
- PHASE 1 (MGE, 12x300, laptop GPU) COMPLETE: ALL 10 rules basin-hit; prodigy (lr-free) BIT-IDENTICAL to tuned adam optimum (+31787.84, r_E 1.5997). Findings: searches_minimal/lr_free_findings.md (committed). Wiring rules for any promotion: per-start vmapped optimizer state (lr-free global scalars couple under stacked params — af.AbstractMultiStartGradient can NOT carry them as-is) + optax.apply_if_finite (forwards momo value= kwarg on optax>=0.2.5).
- PHASE 2a (pix adam lr sweep 1e-3/3e-3/3e-2, jobs 330529-31) COMPLETE, NEGATIVE: best -28462 @ lr 3e-3 (vs 1e-2's -39888) — no lr within 46k nats of the Nautilus bar +17419. LR MIS-SCALING RULED OUT. Warm cache = 17-20min/job.
- RESUME (morning): (1) read /mnt/ral/jnightin/pixgrad_logs/samp_pixlr_free_330535.log (phase 2b: prodigy/dadapt/mechanic on pix via pix_lr_free.py, submitted 2026-07-16 ~22:20, 8h limit). If they also stall ~-28k → failure is landscape/step-budget: next levers = PIX_N_STEPS=3000 rerun (env exists in pix_lr_free.py) and/or warm starts near the Nautilus mode r_E 1.31. (2) Then findings doc phase-2 section + ship_workspace (PR against main; branch stacked on #100's — coordinate merge order with #100). (3) Ship gate: offer merge + issue close per feedback_prompt_merge_close.
- next after ship: issue draft/research/autolens_workspace_developer/jax_native_posterior_sampler_wave.md (do not bulk-issue)
- repos:
  - autolens_workspace_developer: feature/lr-free-multi-start-optimizers

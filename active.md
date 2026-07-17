# Active Tasks


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


## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: ALL PHASES COMPLETE 2026-07-16 (16+ merged PRs; 3 refusal mechanisms live incl. guard v1.1; epic #155 = remaining-queue tracker: Ph3 steps 2-8, Ph4 four tasks, Ph2 satellites, Ph5 items 3-6)
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
- repos:


## ep-projection-weights
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1382
- status: library-shipped, awaiting-merge — PR PyAutoFit#1383 (pending-release); tests 1494p/1s; shipped through Heart RED (same 6 pre-existing unrelated reasons) on explicit user PR-open instruction 2026-07-17
- worktree: ~/Code/PyAutoLabs-wt/ep-projection-weights (not yet created — /start_library on resume)
- autonomy: supervised
- prompt: active/ep_projection_linear_weights_as_log.md
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1383
- heart-ack: PyAutoLens uncommitted source; workspace validation 3-failed (2026-07-09); 58 stale parked scripts; manifest drift tenant-firewall ×6; release validation stale (5 libs)
- note: TWO stacked defects fixed (investigation upgraded during impl): PRIMARY = TransformedMessage.project never transformed samples to base space (equal-weight cluster at 2.05 projected to 2.97); secondary = linear weights fed to log-weight moment match. Regression test fails on either alone. slope-hierarchy goal 2 unblocks on merge (rerun submit_ep after clearing output/<sample>/ep on RAL).
- repos:

## slope-hierarchy
- issue: https://github.com/Jammy2211/slope_hierarchy/issues/1
- status: workspace-dev — goals 1/3/4 DELIVERED; goal 2 BLOCKED on upstream fix. EP collapse ROOT-CAUSED 2026-07-17: Result.projected_model feeds LINEAR samples.weight_list into AbstractMessage.project which requires LOG weights (exp(w-max) ≈ uniform ⇒ canonical-space boundary attractor ⇒ cavity poisoned ⇒ honest sigma-collapse; damping irrelevant — δ=0.5 job 330532 collapsed identically; probe 330591 proved fit RIGHT 2.0448 / projection WRONG 2.9875±0.011). Bug prompt: draft/bug/autofit/ep_projection_linear_weights_as_log.md (next action = /start_dev it). After the fix merges: clear output/<sample>/ep on RAL, rerun submit_ep, parity table, then N=25-50 scale-up
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
- status: workspace-shipped, awaiting-merge — PR autolens_profiling#75 (pending-release); shipped through Heart RED on human ack 2026-07-17 (5 pre-existing reasons, none from this branch)
- worktree: ~/Code/PyAutoLabs-wt/slam-resume-profiling
- prompt: active/slam_resume_overhead_profile_inter_stage_costs.md
- note: resume recipe (post-#1379): (1) PYAUTO_TEST_MODE=2 PYAUTO_TEST_MODE_SAMPLES=~10000 python3 pipeline_resume/slam_resume.py --reset → instant cold with production-size samples.csv (~10k rows/9MB parity target from #1378); (2) SAME env vars on the rerun for the pure resume record (output lives under output/test_mode/); (3) decomposition → judgment on #70 — pre-findings: adapt images already persisted per stage in files/ + agg_util.adapt_images_from loader exists (targeted load-not-recompute beats checkpoint system); resume also pays zip→unzip per stage; test-mode resume skips latents (small known delta). WSL rebooted overnight 2026-07-17 killing the --fast chain mid-stage-2 (stage-1 output + stage-2 checkpoint remain under output/pipeline_resume/hst_fast if a real-sampling record is ever wanted). Parallel claim: jax-compile-time-research adds jax_compile/ only, no overlap.
- repos:
  - autolens_profiling: feature/slam-resume-profiling

## lr-free-multi-start-optimizers
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/101
- status: workspace-dev — DIAGNOSIS COMPLETE + RESURRECTION BREAKTHROUGH; long-budget run 330598 (3000 steps) in flight
- worktree: ~/Code/PyAutoLabs-wt/pixelized-gradient-experiment (branch feature/lr-free-multi-start-optimizers @ 555eb4e, STACKED on #100's branch, pushed; RAL checkout synced to same commit)
- autonomy: supervised (experiment)
- prompt: active/lr_free_multi_start_optimizers.md
- PHASE 1 (MGE, 12x300, laptop GPU) COMPLETE: ALL 10 rules basin-hit; prodigy (lr-free) BIT-IDENTICAL to tuned adam optimum (+31787.84, r_E 1.5997). Findings: searches_minimal/lr_free_findings.md (committed). Wiring rules for any promotion: per-start vmapped optimizer state (lr-free global scalars couple under stacked params — af.AbstractMultiStartGradient can NOT carry them as-is) + optax.apply_if_finite (forwards momo value= kwarg on optax>=0.2.5).
- PHASE 2a (pix adam lr sweep 1e-3/3e-3/3e-2, jobs 330529-31) COMPLETE, NEGATIVE: best -28462 @ lr 3e-3 (vs 1e-2's -39888) — no lr within 46k nats of the Nautilus bar +17419. LR MIS-SCALING RULED OUT. Warm cache = 17-20min/job.
- DIAGNOSIS CHAIN COMPLETE (jobs 330588/89/92/93): NaN mortality 16/16→0/16 by step 50 in BOTH broad and FD-certified narrow bands; reg pinned at 1.0 does NOT help; deaths scattered (reg 1e-4..4e3, r_E 1.36..6.4) → pixelized likelihood has HARD NON-FINITE WALLS everywhere (invalid inversions); even step 0 has only 13-14/16 finite grads. #100 failure = objective property, not optimizer knob.
- RESURRECTION WORKS (330595, 600 steps): redraw dead starts + reinit vmapped opt state each step → population stays alive (14-16/16), adam@1e-2 climbs -51201→-21443 @ r_E 1.5690 (truth band) STILL IMPROVING at 575; prodigy -26946 @ r_E 1.258. Bar +17419 not yet reached. PROMOTION DESIGN IMPLICATION: af.MultiStart* needs restart-on-death, not just NaN-guards (apply_if_finite latches at the cliff).
- RESUME: (1) read job 330598 (pixresur3k: adam+prodigy, 3000 steps, ~2.5h loop) — does descent reach/approach +17419? (2) Final findings section in lr_free_findings.md (MGE prodigy==adam; pix mortality diagnosis; resurrection viability). (3) ship_workspace (branch STACKED on #100's — coordinate merge order). (4) Draft follow-up prompts: localise-the-NaN library bug (PyAutoArray/Lens) + PyAutoFit multi-start resurrection+contrib-rules promotion. (5) Ship gate: offer merge + issue close per feedback_prompt_merge_close.
- next after ship: issue draft/research/autolens_workspace_developer/jax_native_posterior_sampler_wave.md (do not bulk-issue)
- repos:
  - autolens_workspace_developer: feature/lr-free-multi-start-optimizers

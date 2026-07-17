# Active Tasks


## compile-census-final
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/77
- session: claude (CLI, 2026-07-17)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/compile-census-final
- autonomy: supervised (research cap)
- prompt: active/final_compile_time_census_and_remaining_speedup.md
- note: coda to #71/#74 — census of compile UX with cache #128 + autotune-off #132 defaults live (cold+warm, CPU+A100), plus remaining-lever analysis (jax.export vs tracing floor; compile-parallelism flags; warm floor). Writes only jax_compile/. Parallel claim precedent with #70 applies if it still holds autolens_profiling.
- repos:
  - autolens_profiling: feature/compile-census-final

## cti-resurrection-phase4
- issue: https://github.com/PyAutoLabs/autocti_workspace/issues/1
- session: claude (CLI, 2026-07-17)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/cti-resurrection-phase4
- autonomy: supervised
- prompt: active/cti_resurrection_phase4_workspace.md
- note: Phase 4 of the CTI resurrection epic (0-3 merged). 118 scripts / 79 notebooks onto current APIs: plot function API (70 scripts), simulator/fitsable/priors drift, config sync, TEST_MODE validation. Notebooks regenerate at release (Phase 5).
- repos:
  - autocti_workspace: feature/cti-resurrection-phase4
  - PyAutoCTI: feature/cti-resurrection-phase4

## jax-joss-benchmarks
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/281
- status: PARKED-ON-JOB — #282 MERGED+cleaned; 8/8 runnable A100 rows committed (autolens_jax_joss@64204f6). SDP.81 prep = detached RAL job 330605 (45GB ALMA Band6 download -> casatools venv -> 3-level export -> installs dataset/interferometer/{sdp81,sdp81_mid,sdp81_full} in /mnt/ral/jnightin/autolens_jax_joss). RESUME (short session): (1) check log /mnt/ral/jnightin/sdp81_prep_330605.log — expect 'SDP81 PREP ALL DONE' + per-level visibility counts; failure modes: casatools pip wheel on py3.12 (fallback = monolithic CASA tarball), datacolumn, MS_LIST empty (check find patterns); (2) sbatch interferometry benchmarks on A100: benchmarks/interferometer.py at --nvis default/mid/full + benchmarks/imaging_and_interferometer.py (pattern: /mnt/ral/jnightin/autolens_jax_joss/run_rest.sbatch); (3) scp results/*.json back, regen RESULTS.md, commit (guard: explicit file paths); (4) copy small sdp81/ product locally, rewrite scripts/interferometer/start_here.py on NEW branch (start_workspace; #282 merged) using it — decide hosting (commit few-MB FITS to workspace w/ .gitignore allowlist + git add -f, or Zenodo+SDP81_URL); (5) final issue #281 update. Also pending: cluster-tuning prompt draft/feature/autolens_workspace/joss_cluster_benchmark_tuning.md; weak JAX-viz PyAutoLens#614
- worktree: ~/Code/PyAutoLabs-wt/jax-joss-benchmarks
- autonomy: supervised
- prompt: active/autolens_jax_joss_benchmark_repo.md
- note: 5-phase epic (one-shot attempt per user); new repo autolens_jax_joss (PyAutoLabs, public) born alongside; datasets SDP.81 / RXJ1131 / A2744 user-approved
- repos:
  - autolens_jax_joss: main (born this task)



## build-chain-umbrella
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/155
- status: ALL PHASES COMPLETE 2026-07-16 (16+ merged PRs; 3 refusal mechanisms live incl. guard v1.1; epic #155 = remaining-queue tracker: Ph3 steps 2-8, Ph4 four tasks, Ph2 satellites, Ph5 items 3-6)
- prompt: active/build_chain_umbrella.md (full decomposition)
- autonomy: supervised
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

## slam-resume-fastpath
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/502
- session: claude --resume ce78c7e9-3f34-4983-bb53-8840527c1fb6
- status: library-shipped, awaiting smoke + merge — PRs PyAutoGalaxy#504 (merge first) + PyAutoLens#619 (both pending-release, suites 985p/387p); shipped through Heart RED on human ack 2026-07-17; six-workspace smoke in flight
- worktree: ~/Code/PyAutoLabs-wt/slam-resume-fastpath
- autonomy: supervised
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/504, https://github.com/PyAutoLabs/PyAutoLens/pull/619
- prompt: active/slam_resume_fast_path_load_persisted_adapt.md
- note: implements the #70 judgment (adapt disk-first in PyAutoGalaxy + positions persist/reload in PyAutoLens; PRs ag-first). Step 1 = A-vs-B hook decision (result-property lazy vs lazy maker), recorded on the issue. autolens_profiling used READ-ONLY for validation (claimed by jax-compile-time-research — no edits). PyAutoLens main has unrelated dirty paper_jax/paper.md (JOSS draft) — warning only, worktree cut from origin/main.
- repos:
  - PyAutoGalaxy: feature/slam-resume-fastpath
  - PyAutoLens: feature/slam-resume-fastpath

## potential-correction-port
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/618
- session: claude (CLI, 2026-07-17)
- status: phase-1-shipped (PyAutoArray PR open, awaiting merge); phases 2-3 queued
- worktree: ~/Code/PyAutoLabs-wt/potential-correction-port
- autonomy: supervised
- prompt: active/potential_correction_port.md
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/390 (pending-release; 923 tests passed; smoke 44/44 across 6 workspaces; Heart RED acked — 5 pre-existing unrelated reasons)
- note: port caoxiaoyue/lensing_potential_correction (gravitational imaging: joint source+dpsi evidence inversion) into the stack; cite caoxiaoyue/potential_correction_paper (Cao et al. 2025). Phase 1 = PyAutoArray (masked-grid diff operators, curvature/4th-order mask regs, coarse-mesh itp matrix — reuse existing kernel regs). Phases 2 (PyAutoGalaxy Input* mass profiles + GRF) and 3 (autolens/potential_correction subpackage) QUEUED behind slam-resume-fastpath's PyAutoGalaxy+PyAutoLens claims — claim those repos here only after it ships. NumPy/numba only; JAX port is a known follow-up. No GPy/multiprocess/powerbox/numba-scipy deps.
- repos:
  - PyAutoArray: feature/potential-correction-port

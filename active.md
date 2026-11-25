
## autonomous-orchestrators-p4c
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/574
- issued: 2026-11-04
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session
- status: human-ops (pilot run; no worktree — briefs land in PyAutoMind/batches/ by the human)
- prompt: active/autonomous_orchestrators_p4c_pilot_run.md
- epic: autonomous-orchestrators (phase 4c of 4a–4c)
- pre-check: open shadow tick on system python3.10, minimal env — 6 notify proposals, 0 spawns (2026-11-04)
- tier: judge — merge mode: human /prm

## pyautolens-ii-case-studies
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/147
- issued: 2026-11-12
- session: OpenAI Codex desktop
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pyautolens-ii-case-studies
- repos:
  - autolens_workspace_developer: feature/pyautolens-ii-case-studies
- prompt: active/pyautolens_ii_case_studies.md
- coordination: human approved PyAutoLens/paper_jax/paper.md-only edits alongside magnification-maps-wiring; no library code changes
- next: validate JWST PSF/noise and export calibrated ALMA visibilities, then joint gradient check and bounded pilots
- tier: judge — merge mode: human /prm

## numba-wtilde-validation-legs-stall
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/73
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (da579b3a-de74-4060-a9fc-d5b17ae8c5c4)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/autolens_inference/issues/73#issuecomment-7035552262
- verdict: https://github.com/PyAutoLabs/autolens_inference/issues/73#issuecomment-7035547161
- prompt: active/numba_wtilde_validation_legs_stall_nautilus.md
- note: research, no claim/worktree. Rectangular SMA: zero source after source_pix[1] makes mass_total[1] flat on BOTH routes (A100 + numba seed 0 "converged" rows invalid). Datacube: ~50% not-PD evaluations, in-run values don't reproduce serially (+106 nat outlier). Remedy pick parked
- tier: supervised — merge mode: human /prm

## sensitivity_slam_source_pixelized_mappervalued
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/685
- issued: 2026-11-23
- session: shift worker 2026-11-23-am3 (codex:b1a928033a0d472f97e99ca81604b708)
- status: awaiting-input
- next: choose Ludlow NFW or generalized NFW on issue 685 and resume local adec6521
- worktree: /home/jammy/Code/PyAutoLabs-wt/sensitivity-slam-source-pixelized
- repos:
  - autolens_workspace: feature/sensitivity-slam-source-pixelized
- prompt: active/sensitivity_slam_source_pixelized_mappervalued.md
- tier: glance

## sparse_terms_nufft_origin_and_mask_compatibility
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/707
- issued: 2026-11-23
- session: shift worker 2026-11-23-am3 (codex:1b72ba278ac443b1bf858031a61c1c9a)
- status: awaiting-input
- prompt: active/sparse_terms_nufft_origin_and_mask_compatibility.md
- question: https://github.com/PyAutoLabs/PyAutoArray/issues/707#issuecomment-7099834237
- next: Resolve PyAutoGalaxy FITS round-trip scope and coordinate the reader with the aggregator-reload task before claiming worktrees.
- tier: judge — supervised, human /prm

## smoke_cache_stats_warnings_nameerror
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/365
- session: shift worker 2026-11-24-am (codex:64472140ca8443f8a5e1ce9c73f90fc7)
- status: awaiting-input
- prompt: active/smoke_cache_stats_warnings_nameerror.md
- question: https://github.com/PyAutoLabs/PyAutoHeart/issues/365#issuecomment-7126294143
- next: #368 claim cleared 2026-11-24 (PyAutoHeart#369 merged; record complete/2026/11/heart-health-rerun-stale-push.md) — resumable.

## multi_dataset_jax_likelihood_delaunay_wrong_likelihood
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/371
- issued: 2026-11-24
- session: shift worker 2026-11-24-am (01a20c95-1f26-72d0-8529-1a903019348a)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/autolens_workspace_test/issues/371
- prompt: active/multi_dataset_jax_likelihood_delaunay_wrong_likelihood.md
- tier: judge — supervised, human /prm
- next: Retire the historical report or supply the September FITS files and exact stack/config. Both numerical assertions passed on workspace main 48f40953.

## digest-review-table
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/718
- issued: 2026-11-24
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5; Opus 5.5 worker at medium effort)
- status: library-shipped, awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/719
- mind-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/606
- worktree: /home/jammy/Code/PyAutoLabs-wt/digest-review-table
- repos:
  - PyAutoBrain: feature/digest-review-table
  - PyAutoMind: feature/digest-review-table
- prompt: active/digest_review_action_table.md
- coordination: human-approved 2026-11-24 ("Release after 15 min", "fix it first" before the gate shift) — PyAutoBrain shared with parked-hold-grace (PyAutoBrain#720; _orchestrator.py, AUTONOMY.md) while #719 (_digest.py) awaits /prm
- epic: autonomous-orchestrators (M3; before the M3 gate shift; folds M3.3 slice 2 item 1)
- tier: judge — merge mode: human /prm

## parked-hold-grace
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/720
- issued: 2026-11-24
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5; Opus 5.5 worker at medium effort)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/parked-hold-grace
- repos:
  - PyAutoBrain: feature/parked-hold-grace
  - PyAutoMind: feature/parked-hold-grace
- prompt: active/shift_closes_early_with_held_tasks_unstarted.md
- coordination: human-approved 2026-11-24 — PyAutoBrain shared with digest-review-table (PyAutoBrain#719, _digest.py); PyAutoMind shared too (batches/AGENTS.md, a different section from #606)
- epic: autonomous-orchestrators (M3; before the M3 gate shift; amends ruling (d))
- tier: judge — merge mode: human /prm

## cluster-family-fit-figures
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/883
- issued: 2026-11-24
- session: Codex desktop
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/884
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/890
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/891
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/884
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/890
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/891
- release-gate: PyAutoLens
- workspace-pr: https://github.com/PyAutoLabs/autolens_visualization/pull/20
- workspace-pr: https://github.com/PyAutoLabs/autolens_visualization/pull/22
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/38
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/687
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/family-plot-api
- repos:
  - PyAutoLens: feature/family-plot-api
  - autolens_workspace: feature/family-plot-api

## nautilus-bound-geometry
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/18
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/19
- prompt: active/nautilus_bound_geometry_attribution.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-bound-geometry
- retained-repos: autofit_profiling (feature/nautilus-bound-geometry); PR #19 remains in review. Coding claim transferred to nautilus-whole-fit-geometry.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-whole-fit-geometry
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/20
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/21
- prompt: active/nautilus_whole_fit_geometry.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-whole-fit-geometry
- retained-repos: autofit_profiling (feature/nautilus-whole-fit-geometry); PR #21 awaits human review. Coding claim transferred to nautilus-ellipsoid-weight-update.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-ellipsoid-weight-update
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/22
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/23
- prompt: active/nautilus_ellipsoid_weight_update.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-ellipsoid-weight-update
- retained-repos: autofit_profiling (feature/nautilus-ellipsoid-weight-update); PR #23 awaits human review. Coding claim transferred to nautilus-weight-whole-fit.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-weight-whole-fit
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/24
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/25
- prompt: active/nautilus_weight_whole_fit.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-weight-whole-fit
- retained-repos: autofit_profiling (feature/nautilus-weight-whole-fit); PR #25 awaits human review. Coding claim transferred to nautilus-bound-cadence.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-bound-cadence
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/26
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/27
- prompt: active/nautilus_bound_cadence.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-bound-cadence
- retained-repos: autofit_profiling (feature/nautilus-bound-cadence); PR #27 awaits human review. Coding claim transferred to nautilus-worker-headroom.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-worker-headroom
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/28
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/29
- prompt: active/nautilus_worker_headroom.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-worker-headroom
- retained-repos: autofit_profiling (feature/nautilus-worker-headroom); PR #29 awaits review. Coding claim transferred to nautilus-30d-evidence-check.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-30d-evidence-check
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/30
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/31
- prompt: active/nautilus_30d_evidence_check.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-30d-evidence-check
- retained-repos: autofit_profiling (feature/nautilus-30d-evidence-check); PR #31 awaits review. Coding claim transferred to nautilus-30d-independent.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-30d-independent
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/32
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/33
- prompt: active/nautilus_30d_independent.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-30d-independent
- retained-repos: autofit_profiling (feature/nautilus-30d-independent); PR #33 awaits review. Coding claim transferred to nautilus-30d-matched-ess.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-30d-matched-ess
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/34
- issued: 2026-11-24
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/35
- prompt: active/nautilus_30d_matched_ess.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-30d-matched-ess
- retained-repos: autofit_profiling (feature/nautilus-30d-matched-ess); PR #35 awaits review. Coding claim transferred to nautilus-shell-efficiency.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-shell-efficiency
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/36
- issued: 2026-11-25
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/37
- prompt: active/nautilus_shell_efficiency.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-shell-efficiency
- retained-repos: autofit_profiling (feature/nautilus-shell-efficiency); PR #37 awaits review. Coding claim transferred to nautilus-shell-geometry-signal.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-shell-geometry-signal
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/38
- issued: 2026-11-25
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/39
- prompt: active/nautilus_shell_geometry_signal.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-shell-geometry-signal
- retained-repos: autofit_profiling (feature/nautilus-shell-geometry-signal); PR #39 awaits review. Coding claim transferred to nautilus-bound-core-scaling.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-bound-core-scaling
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/40
- issued: 2026-11-25
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/41
- prompt: active/nautilus_bound_core_scaling.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-bound-core-scaling
- retained-repos: autofit_profiling (feature/nautilus-bound-core-scaling); PR #41 awaits review. Coding claim transferred to nautilus-gpu-feed.
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## likelihood-lifecycle-p5f
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/688
- issued: 2026-11-25
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5 orchestrator)
- status: workspace-shipped, awaiting-merge (all 3 PRs OPEN: PR1 autolens_workspace#689, PR2 autolens_workspace#690 (merge after #689), PR3 HowToLens#139; merge with/after the library release carrying 5A–5E + banner)
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/689
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/139
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/690
- worktree: /home/jammy/Code/PyAutoLabs-wt/likelihood-lifecycle-p5f
- repos:
  - autolens_workspace: feature/likelihood-lifecycle-p5f1-workspace
  - autolens_workspace: feature/likelihood-lifecycle-p5f2-slam
  - HowToLens: feature/likelihood-lifecycle-p5f3-howtolens
- prompt: active/likelihood_lifecycle_p5f_workspace_setup.md
- coordination: human-approved claim override 2026-11-25 for autolens_workspace (held by `cluster-family-fit-figures` PR #687: scripts/cluster/plot.py + generated indexes; and `sensitivity_slam_source_pixelized_mappervalued`: subhalo/sensitivity/slam_source_pixelized.py, which 5F leaves untouched). Whichever merges second regenerates llms-full.txt / workspace_index.json.
- epic: likelihood-lifecycle (phase 5F; three PRs; merge with/after the release carrying 5A–5E + banner)
- tier: judge — merge mode: human /prm

## adapt-mesh-weighting
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/714
- issued: 2026-11-25
- session: claude-code desktop (WSL), ~/Science session (Fable 5.2)
- status: research (phases 1-2 run in the science project Science/development/adapt_snr_cap; no claim/worktree until gate 2)
- prompt: active/make_the_source_adapt_image_hilbert_image.md
- note: research, no claim/worktree. Library phase (PyAutoArray, PyAutoGalaxy), workspace phase (autolens_workspace) and docs are filed as their own prompts after the human judges the fits; suggested branch feature/adapt-mesh-weighting. Human added 5 COWLS M25 lenses (F150W, F277W) on 2026-11-25.
- next: gate 1, the human picks 1-2 candidate weightings from Science/development/adapt_snr_cap/results/weighting/index.html
- tier: judge — merge mode: human /prm

## nautilus-gpu-feed
- issue: https://github.com/PyAutoLabs/autofit_profiling/issues/42
- issued: 2026-11-25
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autofit_profiling/pull/43
- prompt: active/nautilus_gpu_feed.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-gpu-feed
- repos:
  - autofit_profiling: feature/nautilus-gpu-feed
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## nautilus-ring-gpu-feed
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/74
- issued: 2026-11-25
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/75
- prompt: active/nautilus_ring_gpu_feed.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-ring-gpu-feed
- retained-repos: autolens_inference (feature/nautilus-ring-gpu-feed), awaiting review
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

## likelihood-lifecycle-p5g
- issue: https://github.com/PyAutoLabs/autolens_assistant/issues/191
- issued: 2026-11-25
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5 orchestrator)
- status: workspace-shipped, awaiting-merge (autolens_assistant#192 OPEN 24bcb36; merge with/after the library release — wiki-currency checks released autolens)
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/192
- worktree: /home/jammy/Code/PyAutoLabs-wt/likelihood-lifecycle-p5g
- repos:
  - autolens_assistant: feature/likelihood-lifecycle-p5g-assistant
- prompt: active/likelihood_lifecycle_p5g_assistant_setup.md
- epic: likelihood-lifecycle (phase 5G; merge with/after the library release)
- tier: judge — merge mode: human /prm

## likelihood-lifecycle-p5h
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/141
- issued: 2026-11-25
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5 orchestrator)
- status: workspace-shipped, awaiting-merge (euclid_strong_lens_modeling_pipeline#142 OPEN f80ccef; merge with/after the library release; HPCPullPyAuto before RAL use; at close-out, retire draft/feature/euclid/single_process_cpu_route_jax_vis_lp_numba_vis_pix.md as superseded)
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/142
- worktree: /home/jammy/Code/PyAutoLabs-wt/likelihood-lifecycle-p5h
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/likelihood-lifecycle-p5h-setup
- prompt: active/likelihood_lifecycle_p5h_euclid_pipeline_setup.md
- epic: likelihood-lifecycle (phase 5H; merge with/after the library release; HPCPullPyAuto before RAL use)
- tier: judge — merge mode: human /prm

## nautilus-ring-latent-placement
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/76
- issued: 2026-11-25
- status: workspace-dev
- prompt: active/nautilus_ring_latent_placement.md
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dev/nautilus-ring-latent-placement
- repos:
  - autolens_inference: feature/nautilus-ring-latent-placement
- epic: nautilus-fast-likelihoods
- tier: judge — merge mode: human /prm

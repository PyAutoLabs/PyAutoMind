
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
- coordination: human-approved 2026-11-24 — PyAutoBrain shared with digest-review-table (PyAutoBrain#719, _digest.py; merged 2026-11-25); PyAutoMind shared too (batches/AGENTS.md, a different section from #606)
- epic: autonomous-orchestrators (M3; before the M3 gate shift; amends ruling (d))
- tier: judge — merge mode: human /prm

## adapt-mesh-weighting
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/714
- issued: 2026-11-25
- session: claude-code desktop (WSL), ~/Science session (Fable 5.2)
- status: research (phases 1-2 run in the science project Science/development/adapt_snr_cap; no claim/worktree until gate 2)
- prompt: active/make_the_source_adapt_image_hilbert_image.md
- note: research, no claim/worktree. Library phase (PyAutoArray, PyAutoGalaxy), workspace phase (autolens_workspace) and docs are filed as their own prompts after the human judges the fits; suggested branch feature/adapt-mesh-weighting. Human added 5 COWLS M25 lenses (F150W, F277W) on 2026-11-25.
- next: phases 1-2 merged 2026-11-26 (records complete/2026/11/adapt-mesh-weighting-library.md, adapt-mesh-weighting-galaxy.md); phase 3 draft/feature/autolens_workspace/adapt_mesh_weighting_workspace_default.md
- tier: judge — merge mode: human /prm

## slam_source_parametric_model_has_no_centre
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/695
- issued: 2026-11-26
- session: claude-desktop 2026-11-26 (Opus 5.5), ~/Science session
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_workspace/pull/696
- next: human /prm on autolens_workspace#696; merge releases the autolens_workspace claim
- worktree: /home/jammy/Code/PyAutoLabs-wt/sensitivity-slam-source-parametric
- repos:
  - autolens_workspace: feature/sensitivity-slam-source-parametric
- prompt: active/slam_source_parametric_model_has_no_centre.md
- tier: judge — merge mode: human /prm
- heart-override: organism RED at start-dev door; human authorized development 2026-11-26 (recorded on issue 695)

## adapt-mesh-weighting-workspaces
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/693
- issued: 2026-11-26
- session: claude-code desktop (WSL), ~/Science session (Opus 5.5), session ID unavailable
- status: workspace-dev (3a PRs open, release-gated; 3b autolens_workspace pending its claim)
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/141
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/110
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/374
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/142
- prompt: active/adapt_mesh_weighting_workspace_default.md
- worktree: ~/Code/PyAutoLabs-wt/adapt-mesh-weighting-workspaces
- repos:
  - HowToLens: feature/adapt-mesh-weighting-workspaces
  - HowToGalaxy: feature/adapt-mesh-weighting-workspaces
  - autolens_workspace_test: feature/adapt-mesh-weighting-workspaces
  - autogalaxy_workspace_test: feature/adapt-mesh-weighting-workspaces
- release-gate: PyAutoArray
- release-gate: PyAutoGalaxy
- release-gate: PyAutoLens
- heart-red-override:
  - authorized: live human, 2026-11-26, this session — "Override for phase 3" (autolens_workspace#693)
  - not exercised for 3a: the scoped dev gate (HowToLens, HowToGalaxy, autolens_workspace_test, autogalaxy_workspace_test) was GREEN at PR-open
  - record: https://github.com/PyAutoLabs/autolens_workspace/issues/693
- note: phase 3a now (HowTo tutorials, _test pinned HilbertSNR scripts); 3b autolens_workspace after sensitivity_slam_source_pixelized_mappervalued (#685) releases its claim
- next: 3a PRs merge only after a release carries PyAutoArray#717/#718, PyAutoGalaxy#763, PyAutoLens#897 (human /prm); 3b (autolens_workspace ~37 scripts) once sensitivity_slam_source_pixelized_mappervalued releases autolens_workspace
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

## intake-memory-workspace-root
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/723
- issued: 2026-11-25
- status: issued
- prompt: active/intake_apply_crashes_on_memory_citations_when.md
- summary: |
    Filed 2026-11-25 from a Science session; the filing session skipped create_issue step 4, so this row was backfilled during the repo cleanup. Not started: no worktree or branch yet.

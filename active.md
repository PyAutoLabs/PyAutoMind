
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

## sed-waveband-search-cap
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (79ac305d-a450-40fe-b02b-8b0ccf4e159a)
- status: awaiting-merge
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1793
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/140
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1793
- resumed: 2026-11-22, Codex desktop, Q17 option 1
- worktree: /home/jammy/Code/PyAutoLabs-wt/sed-waveband-search-cap
- repos:
  - PyAutoFit: feature/sed-waveband-search-cap
  - euclid_strong_lens_modeling_pipeline: feature/sed-waveband-search-cap
- question: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136#issuecomment-7034635460
- prompt: active/sed_chain_waveband_fit_can_spin_forever.md
- validation: PyAutoFit 936b073d4 passed the timeout and conformance checks, including a real sampler and empty-posterior recovery. Euclid 89b7f7c passed 511 fast tests and all nine smoke scripts. Two sequential synthetic plateau fits hit a reduced call budget and wrote QA markers.
- next: Human review of PyAutoFit #1793 first, then Euclid #140. The maintainer will run the original tile on RAL after merge and report on Euclid #136.
- tier: judge — supervised, human review and /prm

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

## likelihood-lifecycle-p5b-array
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/708
- issued: 2026-11-23
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5 orchestrator)
- status: library-shipped, awaiting-merge (5B-1 MERGED 2026-11-24 PyAutoArray#709 e70af85d; 5B-2 PR PyAutoArray#710 OPEN 32888ab5, awaiting human /prm; issue #708 stays open until #710 merges)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/709
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/709
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/710
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/710
- worktree: /home/jammy/Code/PyAutoLabs-wt/likelihood-lifecycle-p5b-array
- repos:
  - PyAutoArray: feature/likelihood-lifecycle-p5b2-array
- prompt: active/likelihood_lifecycle_p5b_array_setup.md
- epic: likelihood-lifecycle (phase 5B of 5A–5H; two PRs: 5B-1 choose, 5B-2 apply)
- tier: judge — merge mode: human /prm

## multi_dataset_jax_likelihood_delaunay_wrong_likelihood
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/371
- issued: 2026-11-24
- session: shift worker 2026-11-24-am (01a20c95-1f26-72d0-8529-1a903019348a)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/autolens_workspace_test/issues/371
- prompt: active/multi_dataset_jax_likelihood_delaunay_wrong_likelihood.md
- tier: judge — supervised, human /prm
- next: Retire the historical report or supply the September FITS files and exact stack/config. Both numerical assertions passed on workspace main 48f40953.

## stale-auto-simulated-cluster-dataset
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/445
- issued: 2026-11-24
- session: shift worker 2026-11-24-am (codex:ed9c08135ae444d58e3a7109b7db7613)
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/532
- worktree: /home/jammy/Code/PyAutoLabs-wt/stale-auto-simulated-cluster-dataset
- repos:
  - autolens_profiling: feature/stale-auto-simulated-cluster-dataset
- prompt: active/stale_auto_simulated_cluster_dataset.md
- coordination: blocker xla-census-anchors-convolver merged 2026-11-24 (autolens_profiling#534, main lint fixed); #532 lint re-run requested

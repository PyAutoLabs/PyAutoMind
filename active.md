
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
- session: shift worker 2026-11-26-pm (claude:9e8338a5)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/smoke_cache_stats_warnings_nameerror
- repos:
  - PyAutoHeart: feature/smoke_cache_stats_warnings_nameerror
- prompt: active/smoke_cache_stats_warnings_nameerror.md
- previous-session: shift worker 2026-11-24-am (codex:64472140ca8443f8a5e1ce9c73f90fc7) — parked Q31, answered "resume after 369 merges"

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
- next: phases 1-3 shipped and released 2026-11-26 (records complete/2026/11/adapt-mesh-weighting-library.md, -galaxy.md, -workspaces.md; libraries 2026.11.26.1). Open follow-ups: draft/bug/autoarray/adaptive_mesh_degenerate_pixel_pair.md (re-scope), rectangular meshes (draft/research/autoarray/adaptive_rectangular_meshes_repeat_the_adapt_ima.md), interferometer (draft/research/autoarray/interferometer_adapt_image_get_the_imaging_mesh.md); human to judge whether this research task can close
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

## grid-search-cores-auto
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1805
- issued: 2026-11-26
- status: library-dev
- tier: supervised
- epic: likelihood-lifecycle
- prompt: active/grid_search_number_of_cores_auto_hangs.md
- worktree: ~/Code/PyAutoLabs-wt/grid-search-cores-auto
- repos:
  - PyAutoFit: feature/grid-search-cores-auto

## installation_docs_arcticpy_recipe
- issue: https://github.com/PyAutoLabs/PyAutoCTI/issues/133
- issued: 2026-11-26
- session: shift worker 2026-11-26-pm (d3322c16-c97e-4195-8166-6d268d4f1fe5)
- status: pr-open
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/134
- worktree: ~/Code/PyAutoLabs-wt/installation-docs-arcticpy-recipe
- prompt: active/installation_docs_arcticpy_recipe.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- repos:
  - PyAutoCTI: feature/installation-docs-arcticpy-recipe

## convolver_blurring_image_warning
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/719
- issued: 2026-11-26
- session: shift worker 2026-11-26-pm (13f69e98-e9f4-48ff-8459-52f29d0f9cd8)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/convolver-blurring-image-warning
- prompt: active/convolver_blurring_image_warning.md
- tier: supervised — auto-merge on green if the Witness passes after a merge slot (decision-taken → human /prm)
- repos:
  - PyAutoArray: feature/convolver-blurring-image-warning

## cosmos-web-ring-mask-dtype
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/700
- issued: 2026-11-26
- session: shift worker 2026-11-26-pm (710c1a77-37b6-43ed-84bc-85b4a82c3438)
- status: awaiting-merge
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/701
- worktree: ~/Code/PyAutoLabs-wt/cosmos-web-ring-mask-dtype
- repos:
  - autolens_workspace: feature/cosmos-web-ring-mask-dtype
- prompt: active/cosmos_web_ring_mask_dtype.md
- tier: glance — merge mode: auto-merge on green if the Witness passes after a merge slot

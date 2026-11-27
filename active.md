
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

## group-subhalo-sensitivity
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/702
- issued: 2026-11-26
- session: shift worker 2026-11-26-pm2 (0f971892-bf2d-4ebe-8fb3-1d104ea7a79c)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/autolens_workspace/issues/702#issuecomment-7203769475
- prompt: active/group_subhalo_sensitivity.md
- note: no repo claim, branch or worktree yet. #701 merged 2026-11-27, so autolens_workspace is free. Q40 answered: Witness = deterministic injected-signal S/N map with vs without companions. Imaging half already done; its no_run.yaml entry is stale (runs in 18s under smoke).
- next: next shift resumes — branch feature/group-subhalo-sensitivity from the plan in the issue body, with the S/N-map Witness
- tier: glance — merge mode: auto-merge on green if the Witness passes after a merge slot

## group-los-halos
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/703
- issued: 2026-11-26
- session: shift worker 2026-11-26-pm2 (1f616415-9676-4136-a025-6e1195558fab)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/autolens_workspace/issues/703#issuecomment-7203799575
- prompt: active/group_los_halos.md
- note: no repo claim, branch or worktree yet. #701 merged 2026-11-27, so autolens_workspace is free; Q39 answered: build the plan in the issue body. Imaging half already done (02f19489). LOS halo must sit in `galaxies` (analysis drops other collections).
- next: next shift resumes — branch feature/group-los-halos and build the plan in the issue body
- tier: glance — merge mode: auto-merge on green if the Witness passes after a merge slot

## vmap-jit-recompiles-per-nautilus-batch-length
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1811
- issued: 2026-11-26
- session: shift worker 2026-11-26-pm2 (04ca20f9-79a0-4372-9b9b-1a21cf73502d)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/PyAutoFit/issues/1811#issuecomment-7204076931
- prompt: active/vmap_jit_recompiles_per_nautilus_batch_length.md
- repos:
  - PyAutoFit: (no branch; parked before implementation — stated bug did not reproduce)

## heart-report-only-red-no-ack
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/727
- issued: 2026-11-27
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5; Opus 5.5 worker at medium effort)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/heart-report-only-red-no-ack
- repos:
  - PyAutoBrain: feature/heart-report-only-red-no-ack
- prompt: active/heart_report_only_red_needs_no_shift_ack.md
- coordination: human-approved 2026-11-27 — PyAutoBrain shared with cockpit-same-chat-late-window (#728); built back to back, disjoint files (this: AUTONOMY.md, _brief.py, watcher Heart read, batch skill Heart text).
- epic: autonomous-orchestrators (M3.6h)
- tier: judge — merge mode: human /prm

## cockpit-same-chat-late-window
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/728
- issued: 2026-11-27
- session: claude-code desktop (WSL), ~/Code/PyAutoLabs session (Opus 5.5; Opus 5.5 worker at medium effort)
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/cockpit-same-chat-late-window
- repos:
  - PyAutoBrain: feature/cockpit-same-chat-late-window
- prompt: active/shift_cockpit_same_chat_and_late_window.md
- coordination: human-approved 2026-11-27 — PyAutoBrain shared with heart-report-only-red-no-ack (#727); built back to back, disjoint files (this: batch.md step 5, cockpit.md, batch collect).
- epic: autonomous-orchestrators (M3.6g)
- tier: glance — merge mode: human /prm (built outside a shift)

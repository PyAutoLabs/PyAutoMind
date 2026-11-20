
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

## cortex-development-split
- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/95
- issued: 2026-11-19
- session: claude-code desktop (WSL), Opus 5.5, ~/Science session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/cortex-development-split
- repos:
  - PyAutoCortex: feature/cortex-development-split
  - PyAutoBrain: feature/cortex-development-split
- prompt: active/development_projects_split.md
- tier: supervised — merge mode: human /prm
- unblocked: 2026-11-20 — PyAutoBrain claims released (shift-smoke-targeted merged PyAutoBrain#685; queued-epics-drive-shifts released)

## slam-simultaneous-subhalo-grid-search
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/683
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (24ac8476-2f82-4029-b4e9-dfbd4eebbcbd)
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs-wt/slam-simultaneous-subhalo-grid-search
- repos:
  - autolens_workspace: feature/slam-simultaneous-subhalo-grid-search
- prompt: active/slam_simultaneous_subhalo_grid_search_fits_last.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- heart-ack:
  - Heart GREEN at the door (2026-11-20); brief heart-ack covers the RED local-checkout and manifest-drift reasons

## plot-grid-small-datasets-indexes
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/705
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (9c372a5f-e023-412c-b694-19a647a4490d)
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/plot-grid-small-datasets-indexes
- repos:
  - PyAutoArray: feature/plot-grid-small-datasets-indexes
- prompt: active/plot_grid_indexerror_under_small_datasets.md
- tier: supervised — merge mode: auto-merge on green if the Witness passes after a merge slot (shift worker ends at PR-open)

## sed-waveband-search-cap
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (79ac305d-a450-40fe-b02b-8b0ccf4e159a)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/136#issuecomment-7034635460
- prompt: active/sed_chain_waveband_fit_can_spin_forever.md
- note: parked before any claim or worktree; n_like_max=50000 cap already exists (calls, not wall time); wall-clock cap needs PyAutoFit `timeout`; repro + witness need a human-run RAL re-run
- tier: supervised — merge mode: auto-merge on green if the Witness passes after a merge slot

## latent-total-source-flux-jax-vs-numpy-regression
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/137
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (8333550b-b72f-47e9-a9c1-d7510145ae95)
- status: awaiting-input
- question: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/137#issuecomment-7034677032
- prompt: active/latent_total_source_flux_jax_vs_numpy_regression.md
- note: does not reproduce on main (passes locally on febc33f + library mains; passed on main CI 2026-11-16); no branch, worktree or code change
- tier: supervised — merge mode: none (parked before any PR)

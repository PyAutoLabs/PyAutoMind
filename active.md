
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

## slam-simultaneous-subhalo-grid-search
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/683
- issued: 2026-11-20
- session: shift worker 2026-11-20-am (24ac8476-2f82-4029-b4e9-dfbd4eebbcbd)
- status: awaiting-input (blocked on PyAutoFit: SearchGridSearch + FactorGraphModel make_result KeyError; question on issue #683)
- question: https://github.com/PyAutoLabs/autolens_workspace/issues/683#issuecomment-7035177232
- blocked-by: draft/bug/autofit/grid_search_factor_graph_make_result_keyerror.md
- next: once PyAutoFit is fixed, rerun scripts/multi_dataset/features/slam/simultaneous.py under PYAUTO_TEST_MODE=1 on branch 84b05719, regenerate the notebook, ship
- worktree: /home/jammy/Code/PyAutoLabs-wt/slam-simultaneous-subhalo-grid-search
- repos:
  - autolens_workspace: feature/slam-simultaneous-subhalo-grid-search
- prompt: active/slam_simultaneous_subhalo_grid_search_fits_last.md
- tier: glance — effective level: supervised; merge mode: auto-merge on green if the Witness passes after a merge slot
- heart-ack:
  - Heart GREEN at the door (2026-11-20); brief heart-ack covers the RED local-checkout and manifest-drift reasons

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

## agent-help-text-rot
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/702
- issued: 2026-11-22
- session: claude-code desktop (WSL), bounded Opus worker for ~/Code/PyAutoLabs session
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/agent-help-text-rot
- repos:
  - PyAutoBrain: feature/agent-help-text-rot
- prompt: active/agent_help_text_is_rotted_in_feature.md
- tier: supervised — merge mode: auto-merge on green (merge left to human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/703

## batch-collect-docs
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/596
- issued: 2026-11-22
- session: claude-code desktop (WSL) worker, ~/Code/PyAutoLabs session
- status: shipped (PRs open; merge is the human's)
- prs:
  - https://github.com/PyAutoLabs/PyAutoMind/pull/597
  - https://github.com/PyAutoLabs/PyAutoHeart/pull/362
- worktree: /home/jammy/Code/PyAutoLabs-wt/batch-collect-docs
- repos:
  - PyAutoMind: feature/batch-collect-docs
  - PyAutoHeart: feature/batch-collect-docs
- prompt: active/docs_in_pyautomind_and_pyautoheart_still_describ.md
- tier: notify — effective level: safe; merge mode: auto-merge on green (merge left to the human this session)
- heart-ack:
  - Heart YELLOW at the door (2026-11-22): euclid_assistant end-at-deliverable block drift, fixed by open PR Jammy2211/euclid_assistant#18; unrelated

## help-docstrings-history
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/704
- issued: 2026-11-22
- session: claude-code desktop (WSL), bounded Opus worker for ~/Code/PyAutoLabs session
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/help-docstrings-history
- repos:
  - PyAutoBrain: feature/help-docstrings-history
- prompt: active/docstrings_printed_as_help_still_carry_incident.md
- tier: safe — merge mode: auto-merge on green (merge left to human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/705

## grid-factor-results
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1789
- issued: 2026-11-22
- session: Codex desktop, approved six-bug review batch, distinct feature worktrees
- status: awaiting-merge (PRs open for human review)
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/grid-factor-results
- repos:
  - PyAutoFit: feature/grid-factor-results
- prompt: active/grid_search_factor_graph_make_result_keyerror.md
- tier: supervised — human review requested, leave PRs open
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1791
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1791

## mixed-galaxy-light
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/743
- issued: 2026-11-22
- session: Codex desktop, approved six-bug review batch, distinct feature worktrees
- status: awaiting-merge (PRs open for human review)
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/mixed-galaxy-light
- repos:
  - PyAutoGalaxy: feature/mixed-galaxy-light
  - PyAutoLens: feature/mixed-galaxy-light
- prompt: active/galaxy_image_dict_mixed_galaxy_overwrites_ordinary_light.md
- tier: supervised — human review requested, leave PRs open
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/746
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/746
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/877
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/877

## truncated-tail-evidence
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1790
- issued: 2026-11-22
- session: Codex desktop, approved six-bug review batch, distinct feature worktrees
- status: awaiting-merge (PRs open for human review)
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/truncated-tail-evidence
- repos:
  - PyAutoFit: feature/truncated-tail-evidence
  - autofit_workspace_test: feature/truncated-tail-evidence
- prompt: active/truncated_normal_log_partition_tail_underflow.md
- tier: supervised — human review requested, leave PRs open
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1792
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1792
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/120

## database-dataset-fits
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/744
- issued: 2026-11-22
- session: Codex desktop, approved six-bug review batch, distinct feature worktrees
- status: awaiting-merge (PRs open for human review)
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/database-dataset-fits
- repos:
  - PyAutoGalaxy: feature/database-dataset-fits
  - PyAutoLens: feature/database-dataset-fits
- prompt: active/database_paths_dataset_fits_not_registered.md
- tier: supervised — human review requested, leave PRs open
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/745
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/745
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/878
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/878

## euclid-nautilus-batch
- issue: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/issues/138
- issued: 2026-11-22
- session: Codex desktop, approved six-bug review batch, distinct feature worktrees
- status: awaiting-merge (PRs open for human review)
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/euclid-nautilus-batch
- repos:
  - euclid_strong_lens_modeling_pipeline: feature/euclid-nautilus-batch
- prompt: active/vis_lp_batch_size_kwarg_silently_ignored.md
- tier: supervised — human review requested, leave PRs open
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/139

## cti-database-reruns
- issue: https://github.com/PyAutoLabs/autocti_workspace/issues/49
- issued: 2026-11-22
- session: Codex desktop, approved six-bug review batch, distinct feature worktrees
- status: awaiting-merge (PRs open for human review)
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/cti-database-reruns
- repos:
  - autocti_workspace: feature/cti-database-reruns
- prompt: active/database_scripts_stale_sqlite_under_test_mode.md
- tier: supervised — human review requested, leave PRs open
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/50

## batch-collect-leftovers
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/706
- issued: 2026-11-22
- session: claude-code desktop (WSL), bounded Opus worker for ~/Code/PyAutoLabs session
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/batch-collect-leftovers
- repos:
  - PyAutoBrain: feature/batch-collect-leftovers
- prompt: active/remove_what_batch_collect_left_behind_in.md
- tier: supervised — merge mode: auto-merge on green (merge left to human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/707

## one-repos-yaml-reader
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/708
- issued: 2026-11-22
- session: claude-code desktop (WSL), bounded Opus worker for ~/Code/PyAutoLabs session
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/one-repos-yaml-reader
- repos:
  - PyAutoBrain: feature/one-repos-yaml-reader
- prompt: active/one_reader_for_repos_yaml_instead_of.md
- tier: supervised — merge mode: auto-merge on green (merge left to human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/709

## launcher-registry
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/710
- issued: 2026-11-22
- session: claude-code desktop (WSL), bounded Opus worker for ~/Code/PyAutoLabs session
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/launcher-registry
- repos:
  - PyAutoBrain: feature/launcher-registry
  - PyAutoMind: feature/launcher-registry
- prompt: active/replace_the_nine_pure_launcher_scripts_with.md
- tier: supervised — merge mode: auto-merge on green (merge left to human /prm)

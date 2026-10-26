
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## linear-operated-sersic-priors
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/666
- issued: 2026-10-26
- prompt: active/linear_operated_sersic_has_no_prior_yaml.md
- session: Codex; session ID unavailable
- status: library validated; downstream smoke running
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/linear-operated-sersic-priors
- approval: Five-task configuration scope approved in this session; merge remains human.
- repos:
  - PyAutoGalaxy: feature/linear-operated-sersic-priors
- validation: Full Galaxy suite: 1374 passed; documented MRO prior inheritance and added regression test. Evidence: .worktrees/linear-operated-sersic-priors/logs/galaxy-suite.log.

## config-leaf-comments
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1732
- issued: 2026-10-26
- prompt: active/config_yaml_keys_missing_their_one_line.md
- session: Codex; session ID unavailable
- status: library draft PR open; remaining library validation and workspace setup
- approval: Five-task configuration scope approved; same-session shared-repository edits are sequential; human merge only.
- affected-repos:
  - PyAutoFit
  - PyAutoArray
  - PyAutoGalaxy
  - PyAutoLens
  - autolens_workspace
  - autogalaxy_workspace
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/config-leaf-comments
- repos:
  - PyAutoFit: feature/config-leaf-comments
  - PyAutoArray: feature/config-leaf-comments
  - PyAutoGalaxy: feature/config-leaf-comments
  - PyAutoLens: feature/config-leaf-comments
  - autogalaxy_workspace: feature/config-leaf-comments
  - autolens_workspace: feature/config-leaf-comments
- validation: 277 comments added; 125 YAML values unchanged; checker reports zero missing comments; 4 focused tests pass. Full serial Fit suite passed 3932 tests; isolated Zeus failure is order-sensitive and reproduced on pristine main. Human approved draft PRs with the baseline behavior documented; merge blocked.

- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1733
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1733

## workspace-prior-copies
- issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/90
- issued: 2026-10-26
- prompt: active/sync_remaining_workspace_config_priors_copies.md
- session: Codex; session ID unavailable
- status: config validation passed; workspace smoke running
- approval: Five-task configuration scope approved; same-session shared-repository edits are sequential; human merge only.
- affected-repos:
  - HowToGalaxy
  - autogalaxy_workspace_test
  - autolens_assistant
  - autogalaxy_assistant
  - autocti_assistant
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/workspace-prior-copies
- repos:
  - HowToGalaxy: feature/workspace-prior-copies
  - autogalaxy_workspace_test: feature/workspace-prior-copies
  - autolens_assistant: feature/workspace-prior-copies
  - autogalaxy_assistant: feature/workspace-prior-copies
  - autocti_assistant: feature/workspace-prior-copies
- validation: 496 YAML files pass strict parsing; 54 changed mappings match intended corrections; 30 model checks pass. Independent evidence: .worktrees/workspace-prior-copies/logs/prior-validation.md.

## workspace-config-key-drift
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/263
- issued: 2026-10-26
- prompt: active/config_key_mirror_drift.md
- session: Codex; session ID unavailable
- status: verified already implemented, awaiting human close-out
- evidence: 14 notation values match; both test keys present; 3 config loads and label render passed. Existing commits autogalaxy_workspace 801a8ce and autofit_workspace 4778b42. No source edits.
- approval: Five-task configuration scope approved; same-session shared-repository edits are sequential; human merge only.
- affected-repos:
  - autofit_workspace
  - autogalaxy_workspace
  - autolens_workspace
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/workspace-config-key-drift
- repos:
  - autofit_workspace: feature/workspace-config-key-drift
  - autogalaxy_workspace: feature/workspace-config-key-drift
  - autolens_workspace: feature/workspace-config-key-drift

## corner-plot-workspace-config
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/177
- issued: 2026-10-26
- prompt: active/corner_plot_config_keys_pr1709_phase3.md
- session: Codex; session ID unavailable
- status: workspace validation running; latent examples gated on Galaxy #656
- approval: Five-task configuration scope approved; same-session shared-repository edits are sequential; human merge only.
- affected-repos:
  - autofit_workspace
  - autogalaxy_workspace
  - autolens_workspace
  - HowToGalaxy
  - HowToLens
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/corner-plot-workspace-config
- release-evidence: PyAutoFit 2026.10.23.1 published, non-yanked; contains #1709.
- repos:
  - autofit_workspace: feature/corner-plot-labels (samlange04 fork)
  - autogalaxy_workspace: feature/corner-plot-labels (samlange04 fork)
  - autolens_workspace: feature/corner-plot-labels (samlange04 fork)
  - HowToGalaxy: feature/corner-plot-labels (samlange04 fork)
  - HowToLens: feature/corner-plot-labels (samlange04 fork)
- validation: Existing contributor branches retained; 20 notebooks regenerated; all five config/superscript checks pass. PyAutoFit release gate cleared; executed latent-output Markdown remains pending PyAutoGalaxy#656.
- blocked-by: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/656

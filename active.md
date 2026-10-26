
## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## corner-plot-workspace-config
- issue: https://github.com/PyAutoLabs/autofit_workspace/issues/177
- issued: 2026-10-26
- prompt: active/corner_plot_config_keys_pr1709_phase3.md
- session: Codex; session ID unavailable
- status: five existing PRs updated; Galaxy #656 merged; awaiting Galaxy publication and executed latent-output Markdown validation
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
- validation: Existing contributor branches retained; 20 notebooks regenerated; all five config/superscript checks pass. PyAutoFit release gate cleared; Galaxy #656 merged; executed latent-output Markdown validation remains pending.
- blocked-by: Published PyAutoGalaxy release containing merged #656; executed latent-output Markdown validation still required.
- library-completion: complete/2026/10/latent-profile-declarations.md
- release-gate: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/656
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/174
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/259
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/595
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/87
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/100
- coordination: Galaxy/Lens contributor branches now include the comment-mirror branches with notation conflicts resolved; all pre-merge corner YAML values preserved. Prerequisites autogalaxy_workspace#264 and autolens_workspace#602 merged on 2026-10-26; completed comment task: complete/2026/10/config-leaf-comments.md.
- smoke: 152 checks passed across five contributor workspaces; evidence in .worktrees/corner-plot-workspace-config/logs/smoke-summary.json.
- ci: Fork workflow approvals issued for Fit/HowToGalaxy/HowToLens after verifying workflow files unchanged; inspect current CI at human merge time.

## likelihood-lifecycle-p2a-restamp-12core
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/466
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-restamp-12core
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-restamp-12core
- prompt: active/likelihood_lifecycle_p2a_pin_restamp_12core.md
- epic: likelihood-lifecycle
- compute-go: human 2026-10-26 ('go') for the 2-task ao A100 breakdown rerun after the memory fix
- progress: branch pushed 65b17065 (3 commits: carry-forward + 12-core, OOM fix, regen); RAL private autolens_profiling_p2a on the branch; ao rerun SUBMITTED 413033 (--array=2,16 of batch0 a100 script, pin 2026.10.23.1 then carried forward) → output/p2a_batch0


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
- status: workspace-dev; all 152 fresh smoke checks pass; four PRs updated; Lens executed pages and final artifact review in progress
- approval: Five-task configuration scope approved; same-session shared-repository edits are sequential; human merge only. Human approved finishing executed examples, Markdown and PR validation against merged Galaxy on 2026-10-26; no publication or workspace merge authorized.
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
- validation: Fresh isolated smoke: 146 scripts + 6 notebooks passed. Independent source/config and 20-notebook parity review CLEAN; Galaxy three-page artifact review CLEAN. Fit normal latent cookbook passed. Lens full renders still in progress.
- blocked-by: Published PyAutoGalaxy release containing #656 for shipping; Lens executed pages and artifact review still required before final PR update. Approved Galaxy checkpoint retry succeeded.
- library-completion: complete/2026/10/latent-profile-declarations.md
- release-gate: PyAutoGalaxy
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/174
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/259
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/595
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/87
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/100
- coordination: Galaxy/Lens contributor branches now include the comment-mirror branches with notation conflicts resolved; all pre-merge corner YAML values preserved. Prerequisites autogalaxy_workspace#264 and autolens_workspace#602 merged on 2026-10-26; completed comment task: complete/2026/10/config-leaf-comments.md.
- smoke: 152 fresh checks passed against continuation scripts/config; logs/continuation/smoke-validation-summary.json and smoke-validation-equivalence.json in the claimed worktree.
- ci: Fork workflow approvals issued for Fit/HowToGalaxy/HowToLens after verifying workflow files unchanged; inspect current CI at human merge time.

## likelihood-lifecycle-p2a-inference-timings
- issue: https://github.com/PyAutoLabs/autolens_inference/issues/47
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-inference-timings
- repos:
  - autolens_inference: feature/likelihood-lifecycle-p2a-inference-timings
- prompt: active/likelihood_lifecycle_p2a_inference_timings.md
- epic: likelihood-lifecycle
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/48
- heart-red-override:
  - authorized: live human 2026-10-26 "I authorize you to work and overrude heart red" (#466 + this task)
  - red: release validation FAILED (stage integrate); Release Integrate failure; Workspace Smoke failure; manifest_drift workspace checkouts red; autolens red; Workspace validation NOT ready 1429p/1f/125s @ cloud#40294511523; test_run red; NOT release_ready (2026-10-26T07:48:52Z); PyAutoBrain red; PyAutoLens red; autolens_profiling red; Worktree drift 1 orphan/3 dirty
  - gates: ruff, --checks, pytest 222 (Pulse validator test running), SLaM leaf smoke, independent review 2 rounds (CLEAN)
  - merge: needs fresh human /prm + green CI; no release

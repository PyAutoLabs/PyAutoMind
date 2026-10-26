
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
- status: release-blocker-repair; Fit #174 merged; four Galaxy-dependent PRs await publication; bounded smoke-profile prerequisite in progress
- approval: Original five-task scope and contributor history preserved; human merge only. On 2026-10-26 human accepted focused checks plus six representative rendered pages, explicitly stopping further full modeling; group Markdown regeneration is waived for this task. Latest request: "yes, finis the PRs and wrap up this epic task". No release or merge authorized.
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
- validation: 152 fresh smoke checks passed (146 scripts + 6 notebooks); 20 notebook parity checks and independent source/config review CLEAN; six rendered pages reviewed CLEAN (Galaxy imaging/interferometer/ellipse, Lens imaging/interferometer/point_source). Group source/notebook smoke-tested; group Markdown deliberately not regenerated under accepted scope.
- blocked-by: Publication of PyAutoGalaxy containing #656 before Galaxy-dependent workspace shipping; current-head CI gates for remaining PRs. Fit #174 merged 2026-10-26 under explicit human authorization. No further modeling required.
- library-completion: complete/2026/10/latent-profile-declarations.md
- release-gate: PyAutoGalaxy
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/174
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/259
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/595
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/87
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/100
- coordination: Five contributor branches updated by normal pushes, preserving history; comment prerequisites Galaxy #264/Lens #602 incorporated. No release, merge, issue close, claim removal or worktree cleanup. All render/smoke processes stopped; checkpoints retained.
- smoke: 152 fresh checks passed against continuation scripts/config; logs/continuation/smoke-validation-summary.json and smoke-validation-equivalence.json in the claimed worktree.
- ci: Current-head audit: Fit 7/7, Galaxy 8/8, HowToGalaxy 8/8, HowToLens 8/8 jobs passed; Lens new-head CI still running at wrap-up audit. Evidence logs/continuation/ci/.

- continuation-approval: 2026-10-26 human authorized all non-Pulse backlog resolution and Heart RED development override for release-blocker fixes; green in-turn merges only, no release through RED.
- smoke-prerequisite: Config-only fix/group-slam-smoke-real-sampling from main; same task coordinates this alongside contributor PR595 to avoid release-gate circularity.

- prerequisite-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/603
- prerequisite-worktree: /home/jammy/Code/PyAutoLabs/.worktrees/corner-plot-workspace-config/autolens_workspace-smoke-fix
- heart-red-override:
  - authorized: live human 2026-10-26 "Authorize development override" for release-blocker development; green in-turn merges already authorized, no release through RED
  - red: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; PyAutoHeart/workflows/Workspace Smoke: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); autolens: red; Workspace validation: NOT ready — 1429p / 1f / 125s @ cloud#40294511523; test_run: red; Release validation: NOT release_ready — v? profile=? (2026-10-26T07:48:52+00:00); validation_report/stages/integrate: fail; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - gates: group SLaM targeted Heart smoke64.7s; strict profile validation0 errors/warnings; CI prerequisite pending

## colab-gemini-instructions
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/324
- issued: 2026-10-26
- prompt: active/colab_custom_instructions_assistant_context.md
- session: Claude Code CLI; session ID unavailable
- status: library-dev
- worktree: ~/Code/PyAutoLabs-wt/colab-gemini-instructions
- repos:
  - PyAutoHands: feature/colab-gemini-instructions
  - autolens_assistant: feature/colab-gemini-instructions
- summary: |
    Phase 1 of 3 (Hands injector + CLI, release checkout, autolens_assistant colab/contexts.yaml + cosmos
    notebook). Human-approved 2026-10-26: 20k-char cap, human /prm (glance overridden), Heart RED
    dev-only override. Phase 2 galaxy + fit mappings, phase 3 CTI via CLI. Human gate before merge:
    open cosmos notebook via Colab GitHub URL on the PR branch.

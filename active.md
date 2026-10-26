
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
- status: awaiting-merge; implementation and accepted validation complete; five existing PRs updated; Galaxy-dependent shipping release-gated
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

## pulse-timings-redesign
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/78
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/pulse-timings-redesign
- repos:
  - PyAutoPulse: feature/pulse-timings-redesign
- prompt: active/pulse_timings_dashboard_redesign.md
- epic: likelihood-lifecycle
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/79
- heart-red-override:
  - authorized: live human 2026-10-26 "I authroize" (this task)
  - red: release validation FAILED (stage integrate); Release Integrate failure; Workspace Smoke failure; manifest_drift workspace checkouts red; autolens red; Workspace validation NOT ready 1429p/1f/125s @ cloud#40294511523; test_run red; NOT release_ready (2026-10-26T07:48:52Z); PyAutoBrain red; PyAutoLens red; autolens_profiling red; Worktree drift 1 orphan/3 dirty
  - gates: ruff, pytest 363, Playwright browser test, check --offline, independent review 3 rounds (fixed)
  - merge: needs fresh human /prm + green CI; no release

## pre-build-black-only-staged-dirs
- issue: https://github.com/PyAutoLabs/PyAutoHands/pull/315
- issued: 2026-10-26
- prompt: active/pre_build_blacks_unstaged_slam_pipeline.md
- session: Codex; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/pre-build-black-only-staged-dirs
- repos:
  - PyAutoHands: fix/pre-build-black-only-staged-dirs
- approval: Human approved backlog resolution and green in-turn merges, excluding Pulse #79.
- heart-red-override:
  - authorized: live human 2026-10-26 "Authorize development override" for both CI fixes and release-blocker development; no release through RED.
  - red: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; PyAutoHeart/workflows/Workspace Smoke: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); autolens: red; Workspace validation: NOT ready — 1429p / 1f / 125s @ cloud#40294511523; test_run: red; Release validation: NOT release_ready — v? profile=? (2026-10-26T07:48:52+00:00); validation_report/stages/integrate: fail; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - gates: local validation passed; exact-head CI checked before merge

## standalone-memory-template-ci
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/516
- issued: 2026-10-26
- prompt: active/standalone_memory_template_ci.md
- session: Codex; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/standalone-memory-template-ci
- repos:
  - PyAutoMind: feature/standalone-memory-template-ci
- approval: Human approved backlog resolution and green in-turn merges, excluding Pulse #79.
- heart-red-override:
  - authorized: live human 2026-10-26 "Authorize development override" for both CI fixes and release-blocker development; no release through RED.
  - red: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; PyAutoHeart/workflows/Workspace Smoke: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); autolens: red; Workspace validation: NOT ready — 1429p / 1f / 125s @ cloud#40294511523; test_run: red; Release validation: NOT release_ready — v? profile=? (2026-10-26T07:48:52+00:00); validation_report/stages/integrate: fail; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - gates: local validation passed; exact-head CI checked before merge

## isolate-validation-artifacts
- issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/319
- issued: 2026-10-26
- prompt: active/isolate_validation_artifacts.md
- session: Codex; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/isolate-validation-artifacts
- repos:
  - PyAutoHeart: feature/isolate-validation-artifacts
- approval: Explicit human approved addressing release blockers and green in-turn merges, excluding Pulse.
- heart-red-override:
  - authorized: live human "Authorize development override" for release-blocker development; no release through RED
  - red: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; PyAutoHeart/workflows/Workspace Smoke: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); autolens: red; Workspace validation: NOT ready — 1429p / 1f / 125s @ cloud#40294511523; test_run: red; Release validation: NOT release_ready — v? profile=? (2026-10-26T07:48:52+00:00); validation_report/stages/integrate: fail; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - gates: pending targeted tests, artifact replay and CI

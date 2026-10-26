
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
- status: awaiting-release; production and full recovery integration deferred by human until other AI tasks finish; four community PRs remain open
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
- prerequisite-result: PR603 merged f3c94aff4f0c5ed78e5c87ae6a8c4d5e849c653e; all8 CI jobs passed; clean prerequisite worktree removed; contributor PR595 includes merged main at365c8311be8e6fdefc47947ba903f0ef08bd228b.
- recovery-approval: Live human 2026-10-26 "Authorize recovery validation; continue through gated release" explicitly permits post-fix TestPyPI rehearsal and full integration while RED; production publication remains gated on the fresh verdict.
- recovery-run: https://github.com/PyAutoLabs/PyAutoHands/actions/runs/40363490490 (TestPyPI only); source pins .worktrees/pr-backlog-evidence/recovery/commit_shas.json include Galaxy656.
- recovery-freeze: Cleared at human release deferral; later source freshness must be rechecked.
- heart-red-override:
  - authorized: live human 2026-10-26 "Authorize development override" for release-blocker development; green in-turn merges already authorized, no release through RED
  - red: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; PyAutoHeart/workflows/Workspace Smoke: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); autolens: red; Workspace validation: NOT ready — 1429p / 1f / 125s @ cloud#40294511523; test_run: red; Release validation: NOT release_ready — v? profile=? (2026-10-26T07:48:52+00:00); validation_report/stages/integrate: fail; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - gates: group SLaM targeted Heart smoke64.7s; strict profile validation0 errors/warnings; prerequisite CI8/8 passed; broader community PR595 release-gated

- latest-direction: Human: "lets not do a gated production release, lets do that in a bit once I have other AI tasks finish". No production/full integration dispatched; TestPyPI-only run40363490490 remains in progress, no completed validation claim or waiter.
- continuation: Recheck all current source pins and PR CI after other tasks finish, complete recovery validation and gated production release, then merge four Galaxy-dependent PRs; preserve all data worktrees until then.

## colab-gemini-instructions
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/324
- issued: 2026-10-26
- prompt: active/colab_custom_instructions_assistant_context.md
- session: Claude Code CLI; session ID unavailable
- status: library-dev
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/541, https://github.com/PyAutoLabs/autolens_assistant/pull/165, https://github.com/PyAutoLabs/PyAutoHands/pull/325 (phase 1, ALL MERGED 2026-10-26 by human)
- library-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/59, https://github.com/PyAutoLabs/autogalaxy_assistant/pull/39, https://github.com/PyAutoLabs/PyAutoHands/pull/326 (phase 2, ALL MERGED 2026-10-26 by human)
- heart-red-override:
  authorization: live human 2026-10-26 "prm, I authorize shop on RED"
  reasons: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; PyAutoHeart/workflows/Workspace Smoke: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); autolens: red; Workspace validation: NOT ready — 1429p / 1f / 125s @ cloud#40294511523; test_run: red; Release validation: NOT release_ready — v? profile=? (2026-10-26T07:48:52+00:00); validation_report/stages/integrate: fail; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  gates: Hands 558 tests; assistant 14 colab tests + check; Brain 64 clone tests; independent review no blockers (4 fixed)
- heart-red-override:
  authorization: live human 2026-10-26 "yeah I approve go" (phase 2)
  reasons: release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; PyAutoHeart/workflows/Workspace Smoke: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); autolens: red; Workspace validation: NOT ready — 1429p / 1f / 125s @ cloud#40294511523; test_run: red; Release validation: NOT release_ready — v? profile=? (2026-10-26T07:48:52+00:00); validation_report/stages/integrate: fail; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  gates: Hands 567 tests + firewall; fit 12 + check; galaxy 12 + check; independent review CLEAN (3 minors fixed)
- worktree: ~/Code/PyAutoLabs-wt/colab-gemini-instructions (phase-1 branches merged; worktree_remove refuses while the task is active — recreate per phase, remove at completion)
- repos:
  - autocti_assistant: feature/colab-gemini-phase3
  - autocti_workspace: feature/colab-gemini-phase3
  - autolens_assistant: feature/colab-gemini-phase4
  - autofit_assistant: feature/colab-gemini-phase4
  - autogalaxy_assistant: feature/colab-gemini-phase4
- summary: |
    Phases 3+4 running together (human 10-26 "do both auto mode"; --auto parks on Heart RED, so run
    supervised under the task's dev override, single ship ask at the end).
    PHASE 2 MERGED 2026-10-26 (autofit_assistant#59, autogalaxy_assistant#39, Hands#326): fit 20k cap,
    galaxy cap 36000 (ag skills 21-32k; trim follow-up draft/refactor/autogalaxy_assistant/). NEXT phase 3:
    autocti_assistant colab/contexts.yaml + autocti_workspace notebooks via `autohands gemini_context apply`.
    PHASE 1 MERGED 2026-10-26 (Brain#541, autolens_assistant#165, Hands#325); human verified Colab
    upload, size (52k) and GitHub-badge routes. Workspace notebooks get instructions at next release.
    NEXT phase 2: autogalaxy_assistant + autofit_assistant colab/contexts.yaml, then set release.yml
    assistant: for galaxy/fit/HowToGalaxy/HowToFit. Then phase 3 CTI (Hands CLI), phase 4 upkeep skills.
    Phase 1 of 4 (+ Brain clone-boundary `colab/*` mixed — assistant PR declares Brain-ref) (Hands injector + CLI, release checkout, autolens_assistant colab/contexts.yaml + cosmos
    notebook). Human-approved 2026-10-26: 20k-char cap, human /prm (glance overridden), Heart RED
    dev-only override. Phase 2 galaxy + fit mappings, phase 3 CTI via CLI. Human gate before merge:
    open cosmos notebook via Colab GitHub URL on the PR branch.

## rectangular-28sq-profiling-rows
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/468
- issued: 2026-10-26
- session: Claude Code (Opus 5.5); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/rectangular-28sq-profiling-rows
- repos:
  - autolens_profiling: feature/rectangular-28sq-profiling-rows
  - autolens_inference: feature/rectangular-28sq-profiling-rows
  - PyAutoPulse: feature/rectangular-28sq-profiling-rows
- prompt: active/rectangular_28sq_profiling_rows.md
- epic: likelihood-lifecycle
- heart-red-override: authorized by live human 2026-10-26 "I approve of the override" (this task incl. RAL jobs); reasons + gates recorded at ship
- scope-add: HUMAN 2026-10-26 chose "Yes, small Pulse PR first" (option text: "Same RED override extended to it. Ships before the profiling rows.") — PyAutoPulse one-current-per-key adds regime
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/80 MERGED 2026-10-26 5474e3cb via human /prm (regime in @3 one-current key)

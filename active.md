# Active Tasks

## search-ext-b1-registration
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/492
- issued: 2026-10-07
- prompt: active/search_extensibility_b1_registration.md
- epic: search-extensibility (phase B1 registration)
- session: Claude CLI (Fable 5.1, /start_dev); https://claude.ai/code/session_01QJmrnXNQdq6HSruUt3MqVW
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/search-ext-b1-registration
- repos:
  - autofit_inference: feature/search-ext-b1-registration
  - autofit_profiling: feature/search-ext-b1-registration
  - PyAutoMind: feature/search-ext-b1-registration (coordination authorised by the human 2026-10-07 with mind-dashboard-simplify #491: repos.yaml, ROUTING.md, epics.md only)
  - PyAutoHeart: feature/search-ext-b1-registration
  - PyAutoCortex: feature/search-ext-b1-registration
  - PyAutoPulse: feature/search-ext-b1-registration
- tier: judge (human /prm)
- summary: minimal lint-green skeletons for both new fit repos; Mind repos.yaml rows + repos_sync --write; Heart excluded; Cortex planned row; Pulse task adoption (no registry rows at B1); org profile rows; RAL clones. Clears Heart manifest-drift YELLOW.

## search-conformance-metadata
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1666
- issued: 2026-10-07
- prompt: active/search_conformance_metadata_layer.md
- epic: search-extensibility (phase A0a(i))
- session: Claude CLI (Fable 5.1, /start_dev); https://claude.ai/code/session_01QJmrnXNQdq6HSruUt3MqVW
- status: library-shipped, awaiting-merge — PR #1667 open 2026-10-07 (judge tier: human /prm); worktree kept for /prm close-out
- worktree: ~/Code/PyAutoLabs-wt/search-conformance-metadata
- repos:
  - PyAutoFit: feature/search-conformance-metadata
- tier: judge (human /prm)
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1667
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1667
- heart-ack: manifest drift: workspace checkouts (manifest ↔ disk) — 2 mismatch(es) vs PyAutoMind/repos.yaml (autofit_inference, autofit_profiling: B1 registration pending); release validation incomplete: no rehearsal for current source — acknowledged by the human 2026-10-07 at ship
- summary: tests-only metadata/serialization conformance suite over the 15 public searches; frozen golden identifier table; collects on unittest-nojax. Human ruling: identifiers stay the same, any change flagged first.

## mind-dashboard-simplify
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/500
- issued: 2026-10-07
- session: Codex; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/mind-dashboard-simplify
- repos:
  - PyAutoBrain: feature/mind-dashboard-simplify
  - PyAutoMind: feature/mind-dashboard-simplify
- plan: approved; remove requested dashboard copy, move Epics below Start here and Pending release last; retain Update button; human /prm merge

- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/501
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/491
- heart-ack: user explicitly authorized shipping on 2026-10-07 with manifest drift: workspace checkouts (manifest ↔ disk) — 3 mismatch(es) vs PyAutoMind/repos.yaml; release validation incomplete: no rehearsal for current source
- validation: Brain 1271 passed; Mind 696 passed; generated dashboard current; copy payloads and requested layout verified
- next: human /prm; merge Brain #501 before Mind #491; no public API or scientific workspace impact

## linear-solver-p3a-a100-parity
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/393
- issued: 2026-10-07
- session: Claude Code CLI (Fable 5.1) https://claude.ai/code/session_013yiZUnJowr5bnXGpSV2YpC
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-p3a-a100-parity
- repos:
  - autolens_profiling: feature/linear-solver-p3a-a100-parity
- pulse-task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/mge_nnls_fix_pyautoarray_571_slam_60.md

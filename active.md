# Active Tasks

## linear-solver-p3b-gpu-timing
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/395
- issued: 2026-10-08
- session: Claude Code CLI (Fable 5.1), session 331e5f0e
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/linear-solver-p3b-gpu-timing
- repos:
  - autolens_profiling: feature/linear-solver-p3b-gpu-timing

## shapelets-smoke-slow-park
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/586
- prompt: active/shapelets_modeling_smoke_slow_park.md
- issued: 2026-10-08
- session: Claude CLI (Opus 5.5 worker, --auto); session ID unavailable
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/shapelets-smoke-slow-park
- repos:
  - autolens_workspace: feature/shapelets-smoke-slow-park
- tier: glance (auto-merge on green if Witness passes)
- plan: --auto launch by the human 2026-10-08 (review_release 2026.10.7.1 follow-up); plan on the issue

## inference-setup-contract
- issue: https://github.com/PyAutoLabs/PyAutoInsight/issues/13
- issued: 2026-10-08
- prompt: active/inference_setup_contract.md
- epic: inference-setup-redesign (phase 1)
- session: Codex GPT-6; session ID unavailable
- status: workspace-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/inference-setup-contract
- repos:
  - PyAutoInsight: feature/inference-setup-contract
- tier: judge (human /prm)
- plan: approved in conversation; "ok begin" after baseline and cold/warm/resume refinements. Reader first, v1 retained; no compute or merge authorized.
- remaining: human /prm for Insight#14; then phase 2 producer/catalogue/script migration. UI, wiki/assistant and literature candidate phases remain in the parent prompt.
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/14
- commit: 4f8eaec (feature/inference-setup-contract)
- validation: 157 tests passed; Ruff lint/format and offline contract/dashboard check passed; GitHub lint and refresh pending at handoff.
- heart: STALE (85), release validation incomplete: no rehearsal for current source; freeze clear; no yellow/red readiness reasons.
- handoff: v2 reader retains v1; explicit setup/prepared problem and baseline references, cold/warm/resume provenance, JIT/cache state, work units and clocks. Live registry remains v1; no compute or scientific acceptance performed.

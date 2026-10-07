# Active Tasks

## dashboard-checkin-prompts
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/484
- issued: 2026-10-07
- prompt: active/dashboard_checkin_prompts.md
- session: Codex local
- status: workspace-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dashboard-checkin-prompts
- repos:
  - PyAutoBrain: feature/dashboard-checkin-prompts
  - PyAutoEars: feature/dashboard-checkin-prompts
  - PyAutoHeart: feature/dashboard-checkin-prompts
  - PyAutoHands: feature/dashboard-checkin-prompts
  - PyAutoMemory: feature/dashboard-checkin-prompts
  - PyAutoPulse: feature/dashboard-checkin-prompts
  - PyAutoInsight: feature/dashboard-checkin-prompts
  - PyAutoNerves: feature/dashboard-checkin-prompts
  - PyAutoGut: feature/dashboard-checkin-prompts
  - PyAutoEyes: feature/dashboard-checkin-prompts
  - PyAutoScientist: feature/dashboard-checkin-prompts
- summary: Implement the thirteen individually approved check-in prompts; no dashboard restructuring, merge or publication.
- ears-follow-up: User approved board cleanup and coordination with PR #17 on 2026-10-07; shipped as Ears commit 1ed08da on the existing branch. 73 tests, Chromium copy/layout/expiry checks and state contract passed. PR #17 merged 2026-10-07 (d08c6c5); all three CI jobs passed. Ten sibling PRs remain open, so retain the shared issue and worktree.
- resume: All 13 prompts implemented and pushed as 11 pending-release PRs. 1268 applicable local tests pass, plus targeted metadata-portability reruns; all approved rendered wording verified. Tenant firewall, required lint/offline checks and Eyes live-link check pass. Next: human /prm when every required CI leg is green; then regenerate/publish Mind and Cortex boards from merged Brain. No merge or publication authorization.
- heart-ack: Human said "those are fixed, so continue". Fresh canonical Heart YELLOW at 2026-10-07T06:49:56.708128+00:00; no RED reasons. Remaining warning: manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml. Release validation remains stale because source moved since rehearsal. Development PRs only.
- workspace-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/485
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEars/pull/17
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/288
- workspace-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/304
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/119
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/20
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/9
- workspace-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/189
- workspace-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/25
- workspace-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/21
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/46
- validation: .worktrees/dashboard-checkin-prompts/scratch/review.md; scratch/shipped.json holds exact commit SHAs.

## profiling-dashboard-completion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/387
- issued: 2026-10-07
- prompt: active/profiling_dashboard_completion.md
- session: Codex local
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-dashboard-completion
- repos:
  - autolens_profiling: feature/profiling-dashboard-completion
- summary: Approved phase A: useful axis/run navigation, visible measurements, explicit hazard discovery; preserve scientific identity and historical evidence.
- resume: Plan approved. Issue registered; isolated worktree setup. Parent draft/feature/autolens_profiling/profiling_redesign_completion.md retains phases B/C; Pulse claimed by dashboard-checkin-prompts.

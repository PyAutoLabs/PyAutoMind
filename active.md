# Active Tasks

## nnls-memo-scattered-backoff
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/613
- issued: 2026-10-04
- prompt: active/nnls_memo_scattered_backoff.md
- session: claude (Opus 5.5 subagent, https://claude.ai/code/session_01S11WE9oj7Mvkfhc4EPBnyN)
- status: library-shipped, awaiting-merge
- worktree: ~/Code/PyAutoLabs-wt/nnls-memo-scattered-backoff
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/615
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/615
- repos:
  - PyAutoArray: feature/nnls-memo-scattered-backoff
- summary: Per-key exponential back-off for the fnnls warm-start memo after consecutive fallbacks, so scattered (iid) streams stop paying for a bad seed every other solve; local-walk behaviour unchanged. Pulse task organs/PyAutoPulse/tasks/interferometer_nnls_memo_scattered_stream_guard.md.
- resume: shipped 2026-10-07 as PyAutoArray#615 (rebased e54123b4, pending-release, Heart YELLOW acknowledged; 1975 passed, 4 xfailed). No workspace impact. Next: CI green then human /prm. Follow-ups on #613 (not merge gates): real Nautilus-replay witness; autolens_profiling harnesses should call nnls_memo.memo_clear().

## dashboard-checkin-prompts
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/484
- issued: 2026-10-07
- prompt: active/dashboard_checkin_prompts.md
- session: Codex local
- status: workspace-dev, awaiting-heart-override
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
- resume: All 13 prompts implemented; 1268 applicable tests pass. Required lint/offline checks and Eyes live 265-PNG check pass. Full evidence, diffs and PR drafts: .worktrees/dashboard-checkin-prompts/scratch/review.md. Source uncommitted pending explicit development-only Heart RED override for #484. No merge or publication authorization.
- heart-red-reasons: PyAutoFit: 5 commit(s) behind origin; PyAutoArray: 2 commit(s) behind origin; PyAutoLens: 2 commit(s) behind origin (canonical readiness 2026-10-07T06:43:42.803462+00:00).

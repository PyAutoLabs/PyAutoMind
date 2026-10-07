# Active Tasks

## scribbler-wave2-radial-panels-regrid
- discussion: https://github.com/orgs/PyAutoLabs/discussions/23
- user-facing: true
- author: @samlange04 (external)
- issued: 2026-10-07
- session: Claude CLI (Fable 5.1, /community); session ID unavailable
- status: library-shipped, awaiting-merge
- repos:
  - PyAutoGalaxy: samlange04:feature/scribbler-radial-panels-regrid (PR #641, maintainer fixups pushed c0a9a387, CI 4/4 green)
  - PyAutoLens: feature/scribbler-regrid-reexport (DRAFT PR #770, red until #641 merges — CI clones autogalaxy main)
  - autolens_workspace: samlange04:feature/scribbler-radial-panels-regrid (DRAFT PR #583, fixup f81a3577)
  - autogalaxy_workspace: samlange04:feature/scribbler-radial-panels-regrid (DRAFT PR #254, no changes needed)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/641
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/770
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/583
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/254
- summary: Wave 2 of the Scribbler proposal (radial-subtracted side-by-side panels, cross-grid mask regrid, white/black brushes, arcsinh default). Wave 1 (#635, docs #579/#251) is released in autogalaxy 2026.10.2.1.
- resume: Merge order is PyAutoGalaxy#641 → PyAutoLens#770 (mark ready, re-run CI) → release carrying both → approve fork CI on #583/#254, mark ready, merge. Workspace prose describes white/black brushes, so #583/#254 must not merge before the release. Human /prm for all merges.

## dashboard-freshness
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/486
- issued: 2026-10-07
- prompt: active/dashboard_freshness.md
- session: Codex local; session ID unavailable
- status: library-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/dashboard-freshness
- repos:
  - PyAutoBrain: feature/dashboard-freshness
  - PyAutoEars: feature/dashboard-freshness
  - PyAutoHeart: feature/dashboard-freshness
  - PyAutoHands: feature/dashboard-freshness
  - PyAutoMemory: feature/dashboard-freshness
  - PyAutoPulse: feature/dashboard-freshness
  - PyAutoInsight: feature/dashboard-freshness
  - PyAutoNerves: feature/dashboard-freshness
  - PyAutoGut: feature/dashboard-freshness
  - PyAutoEyes: feature/dashboard-freshness
  - PyAutoScientist: feature/dashboard-freshness
- summary: User approved shared freshness footer; <1h green, <24h yellow, otherwise red, unknown grey; exact timestamp and real owner Update link. Shared core then thirteen-board adoption. Merge human /prm.


- heart-ack: User invoked $prm in direct response to the disclosed Heart YELLOW warning on 2026-10-07; authorizes shipping and green-CI merge. Exact warning: manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml. Canonical readiness re-read unchanged, no RED reasons. Release evidence stale; no release authorized.
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/487
- library-pr: https://github.com/PyAutoLabs/PyAutoEars/pull/18
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/289
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/305
- library-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/120
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/22
- library-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/10
- library-pr: https://github.com/PyAutoLabs/PyAutoNerves/pull/190
- library-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/26
- library-pr: https://github.com/PyAutoLabs/PyAutoEyes/pull/22
- library-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/47
- resume: /prm stopped on Ears #18 browser CI: tests/board_browser.py:50 expects 2 orchestration links; new Update makes 3. Brain #487 merged green. Eight consumers green, Eyes #22 pending at audit; all ten consumers remain open. Fix missed Ears owner-browser assertion through dev flow, run exact browser check, ship fix, then /prm. Log: worktree tmp/ci-failure-PyAutoEars-112691117119.log; all PRs listed above. No watcher/auto-rerun/cleanup.

## profiling-browser-completion
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/21
- issued: 2026-10-07
- prompt: active/profiling_browser_completion.md
- session: Codex local
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-browser-completion
- repos:
  - PyAutoPulse: feature/profiling-browser-completion
- summary: Approved Phase C setup-browser parity, preserving captured provenance and scientific qualifications.
- coordination: Human explicitly said "Coordinate in parallel" with dashboard-freshness (#486). This branch owns setup_browser.* and browser tests; freshness owns board/ingest/workflows. Re-render generated dashboard from merged sources when reconciling.
- resume: Port measurement navigation and qualified hazards, test real data and multi-instance routes, then ship.

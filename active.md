# Active Tasks

## profiling-dashboard-completion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/387
- issued: 2026-10-07
- prompt: active/profiling_dashboard_completion.md
- session: Codex local
- status: workspace-shipped, awaiting-merge
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-dashboard-completion
- repos:
  - autolens_profiling: feature/profiling-dashboard-completion
- summary: Approved phase A: useful axis/run navigation, visible measurements, explicit hazard discovery; preserve scientific identity and historical evidence.
- resume: Phase A shipped as autolens_profiling#388 at 4c0961c; independent Sol CLEAN. 1136 Python tests pass across full run/checksum rerun, 6 skipped; expanded Chromium, seven import smokes and tooling checks pass. Human acknowledged current Heart YELLOW. Next human /prm when CI green, then approved Phase B. Parent retains B/C; Pulse still claimed.
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/388
- heart-yellow-reasons: manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml
- heart-stale-reasons: release validation stale: source moved since rehearsal (PyAutoNerves, PyAutoFit, PyAutoArray, PyAutoGalaxy, PyAutoLens)

- heart-ack: Human said "I acknowledge, go" on 2026-10-07 for manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml. Fresh readiness query has same warning and no RED reasons. Development PR only; no merge/release authorization.

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

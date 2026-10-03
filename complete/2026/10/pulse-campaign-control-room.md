# Pulse campaign control room and profiling task migration

- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/6
- completed: 2026-10-03
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/7 (merged 2cf456a4e58c997a9c91df7ee93e492083b4fae8)
- workspace-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/470 (merged 05dc32121b4ef1636da4cf8919ded1655463aa12)
- authorization: Human /prm, 2026-10-03; Pulse merged before Mind.
- summary: One editable/copyable check-in prompt, 11 campaign rows, 25 open tasks, then detailed measurement evidence. 26 original task records migrated with pinned source URLs and SHA256 hashes; one superseded task retained in history. CHECKIN.md supports one ongoing chat and optional campaign direction before or after the prompt. Mind retains bounded development PR claims and historical completions.
- validation: 86 Pulse tests and 619 Mind tests pass; Ruff/format, offline summary/feed checks, 26 pinned source hashes and clipboard normal/fallback/denied paths pass. Exact-head CI green for both PRs. Spawn Drift publication job intentionally skipped on pull_request; its 619-test privacy leg passed.
- heart: At ship, published 2026-10-03T10:12:06Z scoped GREEN for Pulse/Mind, organism-wide RED; no release authorized or performed.
- corrections: Removed extra blank lines in planned.md and epics.md to satisfy registry round-trip invariant; regenerated planned contents.
- cleanup: Repository claims released. Standalone local clones retained (not registered task worktrees); no scientific data or remote branches deleted.
- limitations: No new benchmark or HPC job run. Browser screenshot unavailable (Chromium absent); HTML generation and clipboard handlers tested. A check-in is not stamped by dashboard refresh.

## Original prompt

# Pulse campaign control room and task migration

Type: feature
Target: PyAutoPulse
Repos:
- PyAutoPulse
- PyAutoMind
Status: awaiting-merge
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/6
Issued: 2026-10-03
Filed: 2026-10-03

## Original request

I have not looked at the PyAutoPulse dashboard yet but basically I want it to mirror PyAutoCortex was a table of active campaigns (profilijg specifci) a single copyable prompt at the top to get all updates which will mean all profiling work is managed in a single chat from now on. I also want all profiling tasks in PyAutoMind to move to PyAutoPulse as active tasks listed under the table. Then all the profiling info itself further down. For that initial prompt, it should be I can add to it if I want to direct a specific campaign suggest a specific idea albeit like Cortex I could just tell a prompt at the start.

## Plan

- Add a single editable check-in prompt above a campaign table.
- Give Pulse a validated campaign/task ledger and migrate profiling prompts with provenance.
- Preserve existing task gates and retain the detailed measurement dashboard below.
- Document one-chat check-ins, task updates and bounded development handoffs.
- Validate renderer, task links, migration coverage and repository checks.

Tier: undeclared — merge mode: human /prm.

Implementation: `PyAutoPulse/pulse/campaigns.py`, `campaigns.yaml`, `tasks/`,
`CHECKIN.md`, board/CLI integration and regression tests. Mind's migration record
and routing link replace duplicate queued work; historical completion records remain.
Project measurement producers and scientific acceptance criteria stay authoritative.

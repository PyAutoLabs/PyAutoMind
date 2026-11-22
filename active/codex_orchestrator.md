# Codex execution backend for the shift orchestrator

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: human-required
Consequence: judge
Priority: high
Status: active
Issued: 2026-11-22
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/712
Filed: 2026-11-22
Lane: local-dev
Unattended: never
Witness: Existing orchestrator tests pass; Codex fake-CLI integration exercises launch, restart-safe liveness, usage, failure and stop; an explicit local smoke test precedes live shifts.

## Original request

ok in claude we have developed an orchestrator in PyAutoBrain which autonomously does lots of tasks. I have not yet run this in codex and it prob doesnt support it. Can you review the orchestrator (noting that I have done a lot ofpolish to make it work in an ideal way for this project) and then try get codex suppot in ready to then do some orchestrator runs

## Approved plan (2026-11-22)

The human approved the reviewed plan with “Yeah i approve”. Add a backend seam for worker launch, liveness, stop, auth and accounting, retaining Claude defaults. Codex uses its authenticated CLI, never an API fallback. Briefs and leases record the backend and explicit Codex configuration. Preserve the scheduler, single Mind writer, questions inbox, recovery, merge order, expiry and Opus independent-review default. Test both backends and prepare a bounded laptop smoke test. No real shift launched by this implementation task.

Tier: judge; effective level: human-required; merge mode: human /prm.

## Implementation checkpoint (2026-11-22)

- Brain draft PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/713 (60e6365bb7c75a96ac3fc7b03e56b86c2c335064).
- Mind schema draft PR: https://github.com/PyAutoLabs/PyAutoMind/pull/599 (62dbec2193907b80c610b38d2ad071ae68ed7365).
- Both use feature/codex-orchestrator. Published Git trees exactly match the tested working files.
- Codex execution selected explicitly per brief; Claude defaults and Opus pre-ship review/close-out preserved. Independent Opus helper usage is included in worker accounting.
- Durable prelaunch identities and recovery of reservation/session/retry counts prevent duplicate starts after watcher failure. Unknown state holds; cancellation cleans child groups.
- Brain full suite: 2426 passed, 78 skipped. Mind full suite: 1056 passed. 27 new backend tests.
- Logs in this execution environment: /tmp/codex-brain-final.log, /tmp/codex-mind-final.log.
- Independent Codex implementation review CLEAN after crash-window, descendant, accounting and fast-exit fixes. Not a live Opus shift-adversary claim.
- Scoped published vitals GREEN, generated 2026-11-22T18:27:36Z. Local fresh-checkout snapshot is STALE; published evidence used explicitly.
- Default prerequisite check passes Codex checks but lacks Claude login in this cloud environment. Real laptop hook trust, authentication and smoke remain unverified.
- Next: review/merge both draft PRs; on laptop run bin/codex_orchestrator_check.py, then explicit --smoke --model MODEL; first approved shift has one named task, backlog none, one worker, merge-cap 0, finite budget and review-at.
- No model smoke, real shift, timer, merge or release was started by this task. Human /prm remains the merge mode.

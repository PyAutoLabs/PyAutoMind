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

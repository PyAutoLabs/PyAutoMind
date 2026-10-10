# Reconcile the current generated-guidance manifest drift

Type: bug
Target: health_fixes
Autonomy: supervised
Consequence: judge
Priority: high
Status: awaiting-merge
Issued: 2026-10-10
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/497

Primary repository: @PyAutoMind.

## Incident evidence (2026-10-10)

Health workflow then bug health completed. Supported vitals tick ingested release-integrate
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/38038078541 .
Heart at 2026-10-10T16:21:14.391928+00:00: RED, score 60; exact release RED:
`release validation FAILED (stage integrate)`.
Version 2026.10.10.1.dev81101: 726 passed, 2 failed, 85 skipped, zero timeouts;
installation A–F passed. Same two failures recur from run 37907620652.
Local evidence: workspace-root `tmp/heart-red-investigation/` (artifacts, logs,
status-refreshed.json, health-refreshed.json, door.json).

## Workflow boundary

Historical entry gate: start-dev step 0a initially stopped at Heart RED.
Resolved by live scoped user authorization on 2026-10-10; implemented through
start-dev worktrees and ship workflow. No merge or release
is authorized. Preserve Scientist adoption and Broca expansion plans. Recheck claims
and remote refs before starting. Do not modify other sessions' worktrees.

## Bounded defect and owner

Independent of the PyAutoFit search refactor. Fresh Heart tick still reports eight
yellow reason categories / 18 concrete mismatches:
- PyAutoBroca: missing end-at-deliverable and where-to-file blocks.
- PyAutoDNA: three missing Claude hook/settings files and missing AGENTS guidance.
- Hub index: Broca and DNA absent from organism blurb.
- Stale organism maps: Cortex, Eyes, Ears, Pulse, Insight, Nerves, Gut.
- Stale public tables: org .github/profile/README.md and Scientist README.md.
- Root AGENTS routing table stale.

Before any repair, fetch each owning repository, read its guidance, compare remote
main and local dirty/claimed files, and identify existing registration work. Fresh
local drift is proven; whether each mismatch needs a PR versus safe checkout
synchronization remains unverified. Do not bulk-write across canonical checkouts:
Cortex/Eyes/Gut already have local modifications. No edits to Scientist adoption or
Broca expansion plans. Split owner-specific changes as needed; use canonical
repos_sync generation and its checks, not hand-written generated content.
Acceptance: current remote source and local checkout state explained, generated
checks pass without suppression, supported Heart tick removes these warnings.
Requires development-only RED authorization for this non-RED corrective scope.

## Original user request (verbatim)

Investigate and resolve the current PyAutoHeart RED before we resume the PyAutoScientist adoption pilot. Use the health workflow first, then the bug/start-dev workflow for any fixes.

Fetch the relevant repositories, read their AGENTS.md instructions, and inspect Heart’s latest authoritative verdict and underlying evidence. Distinguish current failures from stale evidence, expected in-progress work, and unrelated problems.

Specifically check whether the failures are caused by, or already being addressed by, the ongoing PyAutoFit refactor. Find its Mind task records, issues, branches, worktrees, PRs and CI results. Trace each relevant Heart failure to concrete evidence; do not assume the refactor explains everything. Avoid duplicating work, modifying its claimed worktrees, or interfering with another session.

Briefly report each RED reason, its likely cause, related existing work, and the next action. If the refactor already covers a failure, record that dependency and identify what completion or validation will clear it. For independent failures, create bounded tasks and implement the necessary fixes through the existing workflow. Make routine decisions autonomously; ask only for genuine blockers or required Heart RED authorization, quoting the exact reasons and requested scope.

Refresh Heart through its supported procedures after fixes or completed upstream work. Do not suppress failures, weaken checks, or mark unresolved evidence green. Finish with the authoritative verdict, validation evidence, remaining blockers, and whether the Scientist dashboard phase can start.

Leave the Scientist adoption and Broca expansion plans unchanged during this work. Their implementation resumes after Heart is sorted

## Current deliverable (2026-10-10)

https://github.com/PyAutoLabs/PyAutoMind/issues/497

12 linked PRs; full canonical generator check PASS; 946 tests PASS; independent CLEAN; remaining CI runs pending, no observed failed test checks.
Heart refresh remains RED 60, exact release blocker `release validation FAILED (stage integrate)`. All source corrections are committed/pushed; no merge or release performed. Full local logs/reviews in workspace-root `tmp/heart-red-investigation/`. Human merge and fresh supported integration evidence remain required.

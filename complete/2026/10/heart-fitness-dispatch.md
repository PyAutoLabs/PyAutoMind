## heart-fitness-dispatch
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/109
- completed: 2026-10-10
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/110
- release-gate: PyAutoFit

Shipped: PR #110 merged after human `/prm`; every head-SHA Actions run and job passed, including smoke Python 3.12 and 3.13. Git ancestry confirms zero unmerged commits.

Replaced obsolete private Fitness dispatch assumptions with explicit JAX analysis and behavioral scalar/batch accuracy, compile reuse, objective cache and pickle reconstruction checks. Existing array/visualization coverage retained. Adopts already merged PyAutoFit A1/A2; no library changes or other-session worktrees modified.

Validation: baseline failure reproduced using release profile; repaired script PASS (6.4s), full local smoke 15 PASS; independent CLEAN review and seven mutation faults detected.

Heart remains RED: `release validation FAILED (stage integrate)` from run 38038078541. Fresh supported wheel integration and evidence ingestion are still required; this merge neither authorizes release/rehearsal nor clears the refactor epic's review 05/06 release blockers. Scientist adoption and Broca expansion plans unchanged. Epic handoff updated to prevent duplicate repair work.

## Original prompt

# Adopt the objective-factory contract in fitness dispatch integration assertions

Type: bug
Target: health_fixes
Autonomy: supervised
Consequence: judge
Priority: high
Status: awaiting-merge
Issued: 2026-10-10
Issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/109

Primary repository: @autofit_workspace_test.

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

`scripts/jax_assertions/fitness_dispatch.py:43` fails `fitness.use_jax_jit is True`.
The fixture builds `af.ex.Analysis` without `use_jax=True`; A2's factory selects
backend from the analysis and no longer treats the deprecated flag as a backend
selector. Subsequent `_call is _jit` / `_vmap` identity assertions also describe
retired internals. Preserve behavioral coverage of scalar JIT, batches, pickle
restoration and visualization; do not delete assertions or disable JAX.
Fix locus candidate: integration-script adoption, after checking the library contract.
Acceptance: focused script passes under release env and meaningful objective/roundtrip
assertions hold; workspace smoke passes; fresh wheel integration clears this row.

## Existing-work dependency and non-duplication

A2 PyAutoFit issue #1676 / PR #1679 merged 2026-10-08. A3 #1677/#1680 and A3b
#1678/#1681 also merged. Main 7d056728c is exactly the rehearsed SHA. CI run
37836895635 passes Python 3.12, 3.13 and no-JAX. No active Mind PyAutoFit claim,
no open PR here; only unrelated PyAutoFit PR #1665 is open (green).
Completion records: `complete/2026/10/search-ext-a{2-objective-bridge,3-samples-checkpointer,3b-nss-preflight}.md`.
Existing epic `draft/research/autofit/search_extensibility_epic.md` Resume lists
unimplemented legacy-pickle/preflight/checkpoint findings; those are separate from
this fixture failure. If investigation needs library changes, reuse/slice the
existing follow-up rather than duplicating it. A4 completion alone is not evidence.
Retained remote feature/search-ext-* refs are merged history, not active PRs.
Canonical git worktree lists show no active refactor feature checkout; B3 pilot
output worktree is explicitly retained in the epic and must remain untouched.

## Original user request (verbatim)

Investigate and resolve the current PyAutoHeart RED before we resume the PyAutoScientist adoption pilot. Use the health workflow first, then the bug/start-dev workflow for any fixes.

Fetch the relevant repositories, read their AGENTS.md instructions, and inspect Heart’s latest authoritative verdict and underlying evidence. Distinguish current failures from stale evidence, expected in-progress work, and unrelated problems.

Specifically check whether the failures are caused by, or already being addressed by, the ongoing PyAutoFit refactor. Find its Mind task records, issues, branches, worktrees, PRs and CI results. Trace each relevant Heart failure to concrete evidence; do not assume the refactor explains everything. Avoid duplicating work, modifying its claimed worktrees, or interfering with another session.

Briefly report each RED reason, its likely cause, related existing work, and the next action. If the refactor already covers a failure, record that dependency and identify what completion or validation will clear it. For independent failures, create bounded tasks and implement the necessary fixes through the existing workflow. Make routine decisions autonomously; ask only for genuine blockers or required Heart RED authorization, quoting the exact reasons and requested scope.

Refresh Heart through its supported procedures after fixes or completed upstream work. Do not suppress failures, weaken checks, or mark unresolved evidence green. Finish with the authoritative verdict, validation evidence, remaining blockers, and whether the Scientist dashboard phase can start.

Leave the Scientist adoption and Broca expansion plans unchanged during this work. Their implementation resumes after Heart is sorted

## Authorization / active handoff

2026-10-10 live user authorized the named repair scopes under `release validation FAILED (stage integrate)`: “yeah I authorize, fix the bugs and ensure when we continue work on the epic it knows this owkr happened but just get the fixes sorted for now”. Prior entry-gate stop resolved for development only. Issue holds implementation plan; no merge/release/rehearsal authority.

## Current deliverable (2026-10-10)

https://github.com/PyAutoLabs/autofit_workspace_test/pull/110

release-profile PASS; 15 smoke scripts PASS; independent CLEAN with seven mutation faults detected; PR CI all three checks successful.
Heart refresh remains RED 60, exact release blocker `release validation FAILED (stage integrate)`. All source corrections are committed/pushed; no merge or release performed. Full local logs/reviews in workspace-root `tmp/heart-red-investigation/`. Human merge and fresh supported integration evidence remain required.

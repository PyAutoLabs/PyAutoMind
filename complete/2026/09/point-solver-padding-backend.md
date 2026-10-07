# PointSolver effective-backend padding — phase 1b

- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/759
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/760
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/330

## Shipped

Both PRs merged on 2026-09-30, library first: PyAutoLens merge
`73dc5d27512c79effc835909618398d64cdddb9a`; workspace merge
`7f75f6c22900f2cbfd4d5edc3ee98d155624a119`. Both task heads are ancestors
of origin/main (zero unmerged commits per repo).

Omitted PointSolver.solve remove_infinities follows the effective call-time xp.
NumPy strips padding; JAX retains static padding, including constructor backend
overrides. Explicit True/False remains authoritative. Added six NumPy cases and
an opt-in 12-case workspace matrix for ordinary and registered tracers, eager/JIT.

## Validation and authorization

Full library rerun: 776 passed, 1 xfailed, 34 warnings. Initial run terminated;
no result inferred from it. Focused matrix 12/12 and full smoke 32/32 passed.
New NumPy and JAX regressions failed before the fix. In-session diff review,
Black and diff checks passed. No independent review claimed.

Every exact-head GitHub run and job passed: library Tests run 36760677556
(Python 3.12, 3.13, no-JAX), Docs 36760677644; workspace Smoke Tests
36760733834 (changes, Python 3.12 and 3.13). All three runs were pull_request;
no additional push runs existed for either head. Both PRs CLEAN/MERGEABLE.
Heart freeze expired, read clear. Live user $prm authorized this merge and
close-out separately from the development-only RED override. Heart's recorded
RED remains “release validation FAILED (stage integrate)”; no release authorized.

## Remaining epic scope

Phase 1b is complete; parent phase 1 is not. Duplicate-image handling and
containment-overflow policy remain in the parent bug prompt. No next-phase issue
queued. Cortex phase 11 remains dropped under R-20260907-05.
Library merge is not publication; pending-release obligation retained above.

## Neighbourhood reconciliation

No sibling prompt retired. Folder-scoped reconciliation flagged four bug and
eight feature prompts through references/overlap; this merge proves only the
bounded padding fix, not those broader scopes. Parent solver hardening was
updated and retained. Re-run `/intake reconcile draft/bug/autolens` or
`/intake reconcile draft/feature/autolens` to inspect the standing candidates.

## Original prompt

# PointSolver padding defaults follow the effective backend — arc phase 1b

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace_test
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/759
Consequence: judge
Epic: cluster-strong-lensing
Phase: 1
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-09-30

## Original request (verbatim)

go

Context: user approved continuing the padding-default fix after phase 1a shipped
in autolens_workspace_test#329 (record complete/2026/09/point-solver-error-audit.md).

## Scope and high-level plan

1. Make PointSolver's omitted remove_infinities depend on the effective backend
   selected for this call, including explicit xp overrides.
2. Preserve explicit True/False choices and implicit constructor-default calls.
3. Prove the old failure, run the library suite and downstream JAX regression,
   then ship library first and its workspace regression through the normal gates.

## Detailed plan / issue body

Primary: PyAutoLens. Classification: both (library fix, workspace regression).
Suggested branch: feature/point-solver-padding-backend.

- autolens/point/solver/point_solver.py, PointSolver.solve: after resolving xp=None
  to self._xp, set an omitted remove_infinities to `xp is np`; document that
  explicitly passed values take precedence. Existing numerical solve is untouched.
- test_autolens/point/triangles/test_solver_edge_cases.py: NumPy-only regression
  for a use_jax=True solver overridden with xp=np, plus explicit padding choices.
  Exercise rejected candidates so padding/stripping is observable.
- autolens_workspace_test/scripts/point_source/solver/padding_backend.py: test
  both constructor backends with default/call-time backend choices, eager and
  jit JAX, registered and unregistered tracers, and explicit padding overrides.
  Compare finite positions with the same explicit-padding reference. Do not
  rewrite phase-1a JSON evidence, which is historical.
- Record red-before/green-after for the JAX reproduction and NumPy regression;
  full PyAutoLens suite and relevant point-source downstream smoke required.
- Workspace regression is opt-in (like the adjacent audit); follow library-first
  shipping/merge and record any release gate. No defaults besides omitted
  padding selection change. Duplicate-image and overflow work remain in the
  parent phase-1 bug prompt; no new issues for them in this session.

## Survey / authorization

User's "go" approves the bounded next padding-default fix named in the prior
turn. Main checkouts: both main and clean; workspace behind origin/main (use
fresh worktree base). Conflict helper finds no active claim on either repo.
PyAutoLens has a recent streaming-p3-visualizer branch; survey its file scope
before worktree setup. Use an isolated task worktree inside this workspace.
Heart entry feed: STALE (no report.json); planning allowed. The RED override
for completed #328 was task-specific and is not authority to ship this task.

## Readiness refresh — 2026-09-30T18:22:29Z

The full Vitals refresh superseded the stale entry feed: RED
“release validation FAILED (stage integrate)”. The completed #328 override is
task-specific. Await a live development-only override for
`point-solver-padding-backend` before issuing/starting this task. No issue,
worktree, or source edit yet. The user approved the bounded fix with “go”;
no second plan approval is needed.

Live user override: “I authorize”, in direct response to the phase-1b development-only RED override request. Exact RED: “release validation FAILED (stage integrate)”. Development shipping only; merge remains separate.

## Current state — PRs open 2026-09-30

Prior blocked notes above are historical. Issue PyAutoLens#759, library PR #760
(commit 9c747c069), workspace PR autolens_workspace_test#330 (9cbcc37).
776 library tests passed, 1 xfailed; focused matrix 12/12; full smoke 32/32.
Development-only override exercised; no merge or release authorized.
Library-first merge and PyAutoLens release gate apply.

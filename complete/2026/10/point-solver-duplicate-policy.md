# PointSolver duplicate-image policy — cluster arc phase 1c

Completed: 2026-10-01
Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/331 (closed)
PR: https://github.com/PyAutoLabs/autolens_workspace_test/pull/332 (merged)
Merge: 13c9d1ff58b56716f63766e6409a9ee8e870f95f
Reviewed head: 2941721607d4075571c30e365a989bc033251c93
Epic: cluster-strong-lensing

## Shipped scope and result

Workspace-only numerical research: duplicate_policy.py, raw evidence JSON and
DUPLICATE_POLICY.md under scripts/point_source/solver/. NO-GO for promoting the
three tested grouping heuristics. All 36 analytic quad rows pass, but four
resolved untruncated NumPy controls fail each rule. 18 near-cusp rows exceed
JAX capacity 20; only 12 JAX rows truncate (uncapped maximum 87). NumPy already
has image-position errors despite small source residuals; root polishing can
accept inaccurate positions. Direct distance grouping merges four true roots
into two. Vmap agreement does not prove physical completeness. No cap-size A/B
was run, so overflow is not established as the sole cause.

Phase 1c complete; parent phase 1 remains incomplete. Separate image-plane
accuracy/identity and observable overflow contracts are next. Phase 2 remains
gated; no later issue queued. Cortex phase 11 stays dropped under R-20260907-05.
The existing PyAutoLens release obligation remains in
complete/2026/09/point-solver-padding-backend.md; this research adds none.

## Validation, review and authorization

Final exact-script run: 54 scalar cases + 6 vmap controls, pinned script SHA
and before/after provenance PASS; summarize verified read-only. Padding 12/12,
image-plane/JIT regression, full smoke 32/32, Black/compile/JSON/diff passed.
An earlier rerun failed environment provenance after another task overwrote the
shared activation symlink; discarded and successfully rerun with a task-owned
activation file.

Independent claude-fable-5-1 review: six findings fixed, re-review CLEAN
(session 2eb5a6d4-323e-4a3f-bd9b-6506a6de2b0f). GitHub run 36839380744 on exact
head 2941721 completed successfully: changes, smoke Python 3.12, smoke Python
3.13. All claimed commits are ancestors of origin/main; no unmerged commits.

Shipping used the recorded live development-only Heart RED override:
"release validation FAILED (stage integrate)" at 2026-10-01T08:46:35.028848+00:00.
Human /prm separately authorized this merge and close-out. No release authorized.

## Close-out

Issue closed; active claim released and epic/parent references reconciled.
Dashboard regenerated with this completion. Task worktree cleanup is subject
to the ignored-data confirmation; retain it unless deletion is authorized.
Review and validation logs remain in the task bundle scratch/ until archived.

Folder-scoped reconciliation: draft/research/workspaces is clean.
draft/bug/autolens reports four suspects: point_image_pair_all_forward_grad_nan,
point_solver_error_bisect_health, jit_cache_not_hit_modeling_visualization and
positions_threshold_fixture_off_axis. None is covered by this research-only
merge; retain all four. Follow-up door: `/intake reconcile draft/bug/autolens`.

## Original prompt

# PointSolver duplicate-image policy — cluster arc phase 1c

Type: research
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Epic: cluster-strong-lensing
Phase: 1
Parent: draft/bug/autolens/point_solver_error_bisect_health.md
Filed: 2026-10-01
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/331

## Original user request (verbatim)

Continue the 'Cluster strong lensing — Source & Cluster arc' epic. Its canonical state lives in draft/feature/autolens/source_cluster_arc.md — read that ledger (and any DECISIONS/RESULTS files beside it) first. Cross-check this epic's entry in PyAutoMind/epics.md, any related rows in PyAutoMind/active.md, and the referenced repos' open issues and PRs, to work out the last completed phase and what is currently in flight. Then pick the next logical step and continue it through the normal workflow (/start_dev — filing the phase's prompt first if none exists), updating the ledger as the work advances. Note: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: the PyAutoCortex project ledger of the science project it births (arc phase 11).

## Why this bounded step

Phase 1a shipped in autolens_workspace_test#329; phase 1b shipped in
PyAutoLens#760 and autolens_workspace_test#330. The remaining duplicate witness
is six NumPy/eager-JAX rows for four analytic images at initial scale 0.05,
versus four under JIT. The audit's grouping within twice the requested
precision is diagnostic only: it is not safe evidence for merging real close
image pairs. Establish the production policy before a library repair.

Only @autolens_workspace_test is a write target. Library source is read-only.
Keep containment-overflow hardening in the parent phase; do not issue it now.

## High-level plan

1. Reproduce the shipped duplicate witness on pinned current library commits.
2. Distinguish duplicate triangle representatives from physically distinct
   close images using lens-equation roots, parity, and triangle geometry.
3. Compare candidate policies on boundary-aligned and near-caustic controls
   across NumPy, eager JAX, JIT and a small vmap batch.
4. Publish raw evidence and one recommended rule, or an explicit no-go with
   the unresolved condition; hand off the bounded library repair separately.

## Detailed plan / proposed issue body

- Branch: `feature/point-solver-duplicate-policy`; workspace-only research.
  After approval, use start_workspace and the standard isolated task worktree.
- Reuse `scripts/point_source/solver/error_audit.py` fixture definitions,
  analytic references, residual checks and provenance. Add
  `scripts/point_source/solver/duplicate_policy.py` as an independently runnable
  full-data CPU diagnostic. Do not change the historical audit witnesses.
- Measure the analytic quad at scales 0.2 and 0.05 and precisions 1e-3 and
  1e-4. Include zero and small source offsets to distinguish exact boundary
  alignment from generic behavior. Record raw positions, finite counts,
  per-step candidate counts, final triangle vertices, lens-equation residuals
  and image parity. Label any capacity-hit row inconclusive for deduplication.
- Add a bounded near-caustic source-offset sequence with successively closer
  genuine image pairs. Establish independent numerical roots with residual
  and refinement-convergence checks; do not use the candidate grouping rule
  as its own oracle. Mark unresolved pairs explicitly instead of claiming
  completeness from a grouped count.
- Compare the audit distance-only grouping as a negative/control candidate
  against geometry/root-informed candidate rules in the diagnostic script.
  Require four distinct analytic images with error consistent with requested
  precision, preservation of resolved close pairs, deterministic representative
  selection, and matching physical membership across backends. Explain behavior
  for unresolved pairs and the static padded JAX output/implicit-gradient seam.
  A rule that works only for the symmetric quad is a no-go.
- Save `scripts/point_source/solver/duplicate_policy_evidence.json` with pins,
  settings, raw and interpreted results. Save
  `scripts/point_source/solver/DUPLICATE_POLICY.md` with the recommendation,
  counterexamples, limitations and exact follow-up library targets (starting
  from PointSolver._solve_array and the containing-triangle path).
- Validation: full-data CPU matrix, one small vmap batch including the boundary
  case and close-pair controls; rerun existing `padding_backend.py` and
  `scripts/point_source/jax_likelihood/image_plane.py`; full workspace smoke;
  Black/diff checks and JSON parsing. Avoid adding the full research sweep to
  default CI; only add a cheap deterministic witness if justified by timing.
- Update the epic ledger as evidence arrives. Ship one workspace PR through
  ship_workspace; do not assert that phase 1 is complete. No production
  deduplication, cap/default changes, later phase issue, HPC job or Cortex birth
  belongs to this task.

## Start-dev reconciliation / approval state

2026-10-01: no matching active.md claim or open phase issue/PR across the eight
referenced repositories. Related workspace_test#106 covers cluster likelihood
scripts, not this solver diagnostic. Workspace checkout main is clean, six
commits behind origin/main at survey time; start_workspace must use fresh main.
Conflict guard passes for autolens_workspace_test. Heart entry feed is STALE:
"test run status unknown (no report.json)"; planning is permitted. Plan pending
explicit human approval; no issue, implementation worktree or source/test edit.

Approved 2026-10-01: user "I approve". Issued as #331; workspace development started.

## Validated local deliverable — 2026-10-01

Implemented `scripts/point_source/solver/duplicate_policy.py`, raw JSON and
`DUPLICATE_POLICY.md`. 54 scalar rows + 6 vmap controls. All 36 quad rows meet
the four-image positional criterion under all three policies; all 18 new
near-cusp rows exceed JAX capacity 20 (uncapped maximum 87). Independent roots
show a four-NumPy/three-JAX fine-precision witness; no cap-size A/B, so no
sole-cause attribution. Distance grouping of the true roots can reduce four
to two. NO-GO for promoting these heuristics; overflow observability is next.

Validation: padding 12/12, existing image-plane/JIT regression, full smoke
32/32, evidence/JSON totals, Black/compile/diff checks and in-session review
all pass. No independent-review claim. Worktree branch remains local and
uncommitted on base `7f75f6c2`; three new scripts/evidence/report files only.
Logs: task bundle `scratch/{duplicate-policy,padding,image-plane,smoke}.log`.
PR body: separate Mind planning checkout `tmp/duplicate-pr.md`.

Ship gate: fresh authoritative Heart RED, "release validation FAILED (stage
integrate)" (snapshot 2026-10-01T08:11:41.393196+00:00, re-read at handoff).
Yellow reasons also recorded in task scratch `readiness-final.json`:
"workspace validation not passing (0 failed, 1 timeout, cloud#36404726969:
autolens_test scripts/multi_dataset/rectangular.py)" and "manifest drift:
public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml".
Await live task-specific development-only override for #331, then ship_workspace.
The plan approval is not a RED override. No source commit/push/PR, merge or
release authorized. Do not repeat successful tests absent source changes or
new concerns. No later phase issued; parent phase 1 remains incomplete.

## Phase 1c Fable review and PR open — 2026-10-01

Independent `claude-fable-5-1` review initially returned FINDINGS; all six
resolved, then re-review CLEAN (session
`2eb5a6d4-323e-4a3f-bd9b-6506a6de2b0f`). This supersedes the earlier inference
that close-pair work should simply wait for capacity-clean evidence: NumPy
is uncapped and already exhibits substantial image-position errors near the
cusp. Small residuals also let root polishing accept inaccurate positions.
The report now separates these accuracy/identity problems from JAX truncation,
adds per-root coverage and polishing errors, and makes summarize read-only.

Final exact-script rerun: 54 scalar + 6 vmap; script SHA pinned, explicit
before/after library/environment/script provenance PASS. 18 rows exceed JAX
capacity 20, but only 12 JAX rows truncate; four resolved untruncated NumPy
controls fail each rule. All 36 quad rows meet the grouping criterion. Existing
padding 12/12, image-plane/JIT, smoke 32/32, Black/compile/JSON/diff pass.
One rerun failed provenance because the shared activation symlink was clobbered
by another task and its bundle removed; discarded, then rerun successfully
with a task-owned activation file. Final log: task scratch/duplicate-policy-final-stable.log.

User "ok review with fable" granted the requested development-only override
for #331 with review first. Heart RED remained exactly "release validation
FAILED (stage integrate)" at 2026-10-01T08:46:35.028848+00:00. Recorded on issue,
PR, active.md and autonomy_log.md. PR
https://github.com/PyAutoLabs/autolens_workspace_test/pull/332 is open at
`2941721`, labelled pending-release. No merge/release authorized. Last shipped
subphase remains 1b; 1c is PR-open, parent phase 1 incomplete, phase 2 gated.
Do not repeat successful validation without changed inputs or a new concern.

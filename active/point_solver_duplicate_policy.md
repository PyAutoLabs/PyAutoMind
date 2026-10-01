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

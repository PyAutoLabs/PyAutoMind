# PointSolver image-position accuracy — phase 1d shipped

- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/333 (closed)
- PR: https://github.com/PyAutoLabs/autolens_workspace_test/pull/334 (MERGED)
- merged: 2026-10-01T10:31:07Z, commit 26da5b1458490fbf0f01d4c5d4a7e7c99eee3fc4
- head: 4bec6a72a20659dca5bd08c8348142ab2c64d5c4; ancestor of origin/main
- epic: cluster-strong-lensing, phase 1d

Added the bounded CPU fp64 research cell, pinned 32-row evidence and
IMAGE_ACCURACY.md under scripts/point_source/solver/. NO-GO for production
promotion: 10/32 raw rows miss per-root coverage; the conditioning screen
falsely accepts three non-converged candidates. Requiring convergence rejects
those but covers only 1–2 of four true images in every closest-cusp row.
No production solver, defaults, capacity or API changed.

Final matrix/provenance and geometry 32/32, evidence/read-only/corruption/empty
controls, padding 12/12, image-plane/JIT and full smoke 32/32 PASS. Black,
compile/JSON/diff and in-session review pass. Every job in GitHub run
36847665642 succeeded at the exact head: changes, smoke Python 3.12 and 3.13.

Live user approved the plan and development-only Heart RED override with
“I approve”; RED remained “release validation FAILED (stage integrate)” with
workspace timeout and manifest drift additional reasons. Human `$prm` then
separately authorized green-CI merge and close-out. No release authorized.
This workspace research task adds no library pending-release obligation;
phase 1b's existing PyAutoLens obligation remains in its own completion record.

Parent phase 1 remains incomplete; phase 2 stays gated. Next bounded production
scope is observable containment overflow, plus separate accuracy/identity work.
The prior PyAutoArray streaming #600 claim is now closed; recheck claims at
next start_dev. No subsequent issue is queued. Cortex phase 11 remains dropped
under R-20260907-05. Generated worktree artifacts are awaiting the cleanup choice;
the committed evidence and report are durable in the merged repository.

## Original prompt

# PointSolver uncapped image-position accuracy — cluster arc phase 1d

Type: research
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Themes:
- point-source
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Epic: cluster-strong-lensing
Phase: 1d
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-10-01
Issued: 2026-10-01

## Purpose and evidence

Phase 1c shipped in autolens_workspace_test#332 (13c9d1f); #331 is closed.
Its `scripts/point_source/solver/DUPLICATE_POLICY.md` rejects distance,
shared-edge and fixed-residual polishing rules. Uncapped NumPy already returns
inaccurate positions near a cusp; JAX truncation is a separate defect.
Investigate the former before choosing a production identity/accuracy policy.
This is a bounded @autolens_workspace_test research cell, not a solver repair.
PyAutoLens and PyAutoArray are read-only inputs. PyAutoArray is currently
claimed by streaming-p5-cubes-phase-centre (#600); no overlapping edits.

## High-level plan

1. Reuse the shipped quad and SIE cusp fixtures and independent root reference.
2. Trace uncapped NumPy refinement and measure image-plane error, root coverage,
   triangle geometry and local conditioning independently of source residual.
3. Test a bounded refinement/polishing diagnostic against true-root errors,
   keeping close roots separate and reporting unresolved cases explicitly.
4. Save reproducible evidence and a go/no-go recommendation for one subsequent
   production task; keep containment overflow and the phase-2 gate open.

## Detailed implementation and acceptance plan

- Add `scripts/point_source/solver/image_accuracy.py`,
  `image_accuracy_evidence.json` and `IMAGE_ACCURACY.md`.
- Reuse `duplicate_policy.py` helpers `reference`, `cases_for`, `solver_for`
  and the existing provenance conventions without rewriting its shipped JSON.
  Verify imported-helper hashes as well as the new script hash.
- Restrict the experiment to the existing quad control and three cusp offsets
  (fractions 1e-3, 1e-5, 1e-7); requested precisions 1e-3 and 1e-4. Use uncapped
  NumPy as the causal experiment. Read the existing JAX evidence as context;
  do not conflate capacity-exceeding NumPy counts with actual truncation.
- Compare raw production solve positions with separately instrumented
  `AbstractSolver.steps`; only interpret triangle ancestry/coverage where
  the terminal centroids correspond to the production output. Locate the
  first loss of reference coverage or persistent false candidate where possible.
- For each candidate record nearest-reference error and per-root coverage,
  source residual, singular values of the lens-equation Jacobian, triangle
  size and parity. Test the linearized correction as a diagnostic against
  measured image-plane error; do not call it a rigorous bound near singularity.
- Bound extra refinement to three additional triangle levels per base row.
  Record step counts/runtime and explicit resource-limited outcomes; do not
  silently shrink the matrix if a case becomes expensive. Compare a bounded
  polishing diagnostic with both actual positional error and conditioning;
  unresolved/singular cases stay explicit. Do not merge roots by distance.
- Retain the independent angular-reference convergence and analytic quad
  cross-check; require coverage of each reference root rather than image count
  alone. A failed candidate policy is a valid research result, never a passing
  production correctness claim. Scope is these fixtures, CPU fp64, forward
  solutions; no general-lens completeness or gradient guarantee.
- Validate saved matrix completeness, finite/explicitly-invalid diagnostics,
  provenance and read-only summarize behavior. Execute the new bounded cell,
  existing padding/backend and image-plane/JIT checks, full workspace smoke,
  formatting/compile/JSON/diff checks. Keep full logs in task scratch.
- Deliver an evidence-based next repair proposal or explicit no-go. Do not
  modify library defaults, capacity, APIs, production deduplication or gradients.
  Library repair and observable overflow each require their own approved scope.

## Workflow state

Proposed branch: `feature/point-solver-image-accuracy`.
Implementation worktree: `.worktrees/point-solver-image-accuracy` under PyAutoLabs.
Heart entry: STALE, "test run status unknown (no report.json)"; planning allowed.
Workspace main clean, eight commits behind origin/main at survey; setup from
fresh origin/main. Conflict guard passes. Recent branches: main,
feature/point-solver-duplicate-policy (merged), chore/session-start-hook-regen.
Await explicit plan approval, then issue only this task via create_issue and
route start_workspace → ship_workspace. No issue or implementation edits yet.
Parent phase 1 remains incomplete. Cortex phase 11 remains dropped under
R-20260907-05; this task does not birth or revive a science project.

## Original request (verbatim)

Continue the 'Cluster strong lensing — Source & Cluster arc' epic. Its canonical state lives in draft/feature/autolens/source_cluster_arc.md — read that ledger (and any DECISIONS/RESULTS files beside it) first. Cross-check this epic's entry in PyAutoMind/epics.md, any related rows in PyAutoMind/active.md, and the referenced repos' open issues and PRs, to work out the last completed phase and what is currently in flight. Then pick the next logical step and continue it through the normal workflow (/start_dev — filing the phase's prompt first if none exists), updating the ledger as the work advances. Note: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: the PyAutoCortex project ledger of the science project it births (arc phase 11).

## Full Vitals gate

Refresh 2026-10-01T09:18:46.359669+00:00: RED,
"release validation FAILED (stage integrate)". Additional readiness reasons:
"workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)";
"manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml".
Await plan approval and live task-specific development-only override before
issue creation or implementation. Brain direct research; declared medium versus
heuristic too-large (11): bounded existing-fixture diagnostic scope justifies
medium; no production API/gradient/general-lens work included.

## Approved and issued
User “I approve” approved the plan and task-specific development-only Heart RED override. Issue autolens_workspace_test#333; branch feature/point-solver-image-accuracy, base 13c9d1f. Proceed through PR creation, no merge/release. Prior awaiting-approval statements are historical.


## Phase 1d PR open — 2026-10-01

Implemented and validated autolens_workspace_test#333; PR
https://github.com/PyAutoLabs/autolens_workspace_test/pull/334 open at
`4bec6a72a20659dca5bd08c8348142ab2c64d5c4`, labelled pending-release.
Files: scripts/point_source/solver/{image_accuracy.py,
image_accuracy_evidence.json,IMAGE_ACCURACY.md}. No production changes.

Final exact-script matrix: 32/32 CPU fp64 rows, zero resource limits,
geometry correspondence 32/32, before/after script/helper/library/environment
provenance PASS. 10/32 raw rows miss per-root coverage; three non-converged
polished candidates falsely pass the conditioning screen, one in a resolved
reference-pair row. Requiring convergence removes all three false accepts but
covers only one or two of four images in every closest-cusp row. NO-GO for
production promotion; neither extra refinement nor this local correction
screen establishes safe image identity. See report for the exact counterexample.

Validation: saved-matrix/read-only summary, coordinate-metric recomputation,
four corrupt-evidence controls and empty-candidate controls PASS; existing
padding 12/12, image-plane/JIT PASS; full workspace smoke 32/32; Black,
compile/JSON/diff checks and in-session review PASS (not independent review).
Logs: .worktrees/point-solver-image-accuracy/scratch/{image-accuracy-final.log,
evidence-validation.log,summary.log,padding.log,image-plane.log,smoke.log,
review.md,vitals.log,readiness.json}. Task-owned activation avoids shared-link
clobbering. Earlier development passes are not the shipped evidence.

Live user “I approve” authorized the plan and task-specific development-only
Heart RED override through PR creation. Ship-time readiness re-read at
2026-10-01T10:10:03.098482+00:00 retains “release validation FAILED (stage integrate)”.
Additional reasons unchanged: “workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)”;
“manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml”.
Recorded on issue, PR, active.md and autonomy_log.md. No merge/release authorized.
GitHub changes gate passed; Python 3.12/3.13 smoke queued at handoff.
Last completed subphase remains 1c; 1d awaits review/merge. Phase 1 remains
incomplete; phase 2 gated; no later issue queued. Next production scope is an
observable containment-overflow contract once Array's claim clears, with
separate accuracy/identity work still required. Cortex phase 11 stays dropped.

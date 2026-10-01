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
Status: draft
Epic: cluster-strong-lensing
Phase: 1d
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-10-01

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

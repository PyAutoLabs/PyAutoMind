# PointSolver error audit — Source & Cluster arc phase 1a

Type: research
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Epic: cluster-strong-lensing
Phase: 1
Parent: draft/feature/autolens/source_cluster_arc.md
Filed: 2026-09-30

Bounded audit slice of `draft/bug/autolens/point_solver_error_bisect_health.md`.
The parent bug prompt retains the library hardening scope. Issue this slice only;
do not issue phase 2 or a hardening follow-up until this evidence is reviewed.

## Original request (verbatim)

Continue the 'Cluster strong lensing — Source & Cluster arc' epic. Its canonical state lives in draft/feature/autolens/source_cluster_arc.md — read that ledger (and any DECISIONS/RESULTS files beside it) first. Cross-check this epic's entry in PyAutoMind/epics.md, any related rows in PyAutoMind/active.md, and the referenced repos' open issues and PRs, to work out the last completed phase and what is currently in flight. Then pick the next logical step and continue it through the normal workflow (/start_dev — filing the phase's prompt first if none exists), updating the ledger as the work advances. Note: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: the PyAutoCortex project ledger of the science project it births (arc phase 11).

## Proposed issue

Title: research: audit PointSolver error boundaries (cluster arc 1a)
Primary repo: PyAutoLabs/autolens_workspace_test
Classification: Workspace; libraries and profiling are read-only evidence inputs.
Branch: feature/point-solver-error-audit
Worktree: create through start_workspace after approval, inside the permitted workspace.

## High-level plan

1. Freeze an analytic isothermal quad and the profiling near-caustic preset with
   explicit parameters, grid extent, precision, magnification threshold and dtype.
2. Measure historical before/after boundaries and current NumPy/JAX results,
   distinguishing raw position error from magnification-filter membership changes.
3. Record a reproducible verdict and the smallest remaining hardening scope.

## Detailed plan / proposed issue body

- Add `scripts/point_source/solver/error_audit.py` and a focused fixture/helper
  only if needed, following `scripts/AGENTS.md`. Mirror existing point_source
  integration-script conventions. Keep the near-caustic preset a read-only input
  with provenance from autolens_profiling's simulator; freeze its resolved source
  coordinates so each boundary sees the same physical problem.
- Audit `PointSolver.solve`, `_solve_array`, `_filter_low_magnification` and
  `AbstractSolver` refinement against the four boundaries in the parent prompt:
  November 2025 dynamic/padded split; March 2026 Hessian-buffer change plus
  April Richardson/exact-JAX change; fca58c468 cap removal; d24339c37 output defaults.
  Use isolated historical checkouts/environments inside the workspace. Record
  exact library/dependency SHAs; never switch shared main checkouts or install
  old dependencies over the shared environment. If an old stack cannot run,
  label mechanism-replay evidence separately from an actual boundary execution.
- Emit matched image counts/positions, source-plane residuals, maximum position
  errors, signed and absolute magnifications, filter survival, output shape,
  dtype/x64 mode, cap and solver settings. Match unordered images before comparing;
  distinguish padding from missing images. Use an analytic quad reference and
  a convergence-tested reference for near-caustic positions, stating tolerances.
- On the current stack compare NumPy, eager JAX and jitted JAX using actual solves
  (disable SMALL_DATASETS/test shortcuts); include a precision/threshold sweep.
  Keep JAX validation in this workspace, not NumPy-only library unit tests.
- Reconcile already-shipped PyAutoLens#480/#710, PyAutoGalaxy#591 and
  PyAutoArray#584/PyAutoLens#753. The current cap is 20, not 15. Investigate the
  float32 placeholders in PyAutoArray as evidence; change no library defaults in
  this slice. Read related autolens_workspace_test#106 for the precision-floor
  finding without absorbing its cluster-script scope.
- Add `scripts/point_source/solver/RESULTS.md` with commands, version pins,
  compact tables and a supported verdict. Store bulky raw logs in ignored scratch;
  retain the compact evidence needed to reproduce the conclusions. Explain
  whether exact local magnification or a finite-area quantity is appropriate
  for point-image filtering; flag unresolved scientific decisions explicitly.
- Run the new audit with full data and existing relevant point-source parity
  scripts, then the repository-required smoke gate before shipping. Historical
  experiments stay opt-in; do not add a long bisect sweep to routine CI.
- Update the epic ledger with evidence links and remaining acceptance criteria.
  Ship via start_workspace / ship_workspace. This slice alone does not declare
  the PointSolver trusted or unlock phase 2 if required hardening remains.

## Survey and gate evidence — 2026-09-30

autolens_workspace_test: main, clean, locally behind origin/main by two commits
at survey; refresh the approved task base before worktree creation. Recent local
branches: main, chore/session-start-hook-regen. No active Mind claim; conflict
guard returned clear. Open #106 is related but targets cluster likelihood scripts.

The full parent scope conflicts with raw-pdip-forward-polish (PyAutoArray and
autolens_profiling) and interferometer-decision-matrix (autolens_profiling).
Those claims remain intact. Profiling main also has untracked dataset/abell_1201/.

Heart: STALE — test run status unknown (no report.json); install verification not
run; no release validation for current source. Refresh at shipping.

Awaiting human plan and issue-body approval under start_dev; no issue or worktree
has been created. After approval create only this issue through create_issue,
register the claim, and continue implementation.

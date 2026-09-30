# PointSolver error audit — cluster arc phase 1a

- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/328
- pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/329
- epic: cluster-strong-lensing
- scope: Audit-only phase 1a; parent phase 1 still requires hardening. No library edits or subsequent phase issues.

## Delivered

Three opt-in audit scripts, RESULTS.md, and three version-pinned JSON evidence files under `scripts/point_source/solver/`. Measured an analytic isothermal-plus-shear quad and a frozen near-caustic fixture across 24 NumPy/eager-JAX/JIT cases; checked 16 historical-Hessian method replays and capacity/dtype witnesses.

Findings: explicit call-time xp=jnp inherits the NumPy constructor's padding default and fails under JIT; symmetric quad can return six centroids for four distinct image groups; synthetic capacity overflow silently truncates. Float32 NaN placeholders preserve float64 vertices in the tested paths. Neither physical fixture exceeds the old cap (maximum 13). Local point magnification is the appropriate filter; historical step changes affect threshold survival but do not demonstrate the original position-error regression at threshold 0.1.

Historical corrections: cap parameter removed by 5c42d8133 in December 2024, not April 2026; JAX jacfwd arrived in March 2026 (ee92bebe). The old-stack import lacked autoconf; the report explicitly distinguishes a historical-method replay on current deflections from a full historical-stack bisect.

## Validation and authorization

Local 24-case audit, 16 replay comparisons, capacity/dtype witnesses, image-plane parity, Black and diff checks passed. Workspace smoke 32/32 passed. GitHub Actions run 36756347920 succeeded at c54fcf8792719d9c0fa5ef19711db3def12c6fcd: changes job and both Python 3.12/3.13 smoke legs green. PR #329 merged 2026-09-30T18:14:51Z as bf3f7532ac780b682e64207c1a94394bbe5a1819; branch ancestry verified against origin/main.

Live human authorization: “Override Heart RED for #328; ship the PR, then merge when CI is green”. Exact RED reason: “release validation FAILED (stage integrate)”. Development shipping and green-CI merge only; no release. Human also authorized removal of the task worktree and generated artifacts after merging.

## Next

Parent `draft/bug/autolens/point_solver_error_bisect_health.md` retains hardening: padding backend selection, duplicate-image policy/regressions, loud containment-overflow signal and deliberate cluster capacity policy. Do not unlock phase 2 merely because the audit shipped. Cortex phase 11 remains dropped under R-20260907-05; any successor needs a fresh science-project birth.

## Neighbourhood reconciliation

No sibling prompt retired: the parent `point_solver_error_bisect_health.md` still needs hardening. `point_image_pair_all_forward_grad_nan.md`, `jit_cache_not_hit_modeling_visualization.md`, and `positions_threshold_fixture_off_axis.md` had overlap/stale-status signals, not proof that this audit completed them. Recheck through `/intake reconcile draft/bug/autolens`. The research/workspaces scope returned no suspects.

## Original prompt

# PointSolver error audit — Source & Cluster arc phase 1a

Type: research
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-09-30
Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/328
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

Plan and branch approved by user (“go”) 2026-09-30. Issued as #328; implementation
and local validation complete. See active.md and the parent epic ledger for
results and the Heart RED ship block. No feature commit/push/PR yet.

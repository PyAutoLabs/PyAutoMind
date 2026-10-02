# Critical-curve dispatch: current cluster evidence and contract

Type: research
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft
Epic: cluster-strong-lensing
Phase: 3a
Parent: draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md
Filed: 2026-10-02

## Original request

Continue the 'Cluster strong lensing — Source & Cluster arc' epic. Its canonical state lives in draft/feature/autolens/source_cluster_arc.md — read that ledger (and any DECISIONS/RESULTS files beside it) first. Cross-check this epic's entry in PyAutoMind/epics.md, any related rows in PyAutoMind/active.md, and the referenced repos' open issues and PRs, to work out the last completed phase and what is currently in flight. Then pick the next logical step and continue it through the normal workflow (/start_dev — filing the phase's prompt first if none exists), updating the ledger as the work advances. Note: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: the PyAutoCortex project ledger of the science project it births (arc phase 11).

## Purpose and boundary

Re-audit the historical phase-3 assumptions before selecting a production
engine-dispatch contract. Only @autolens_workspace_test changes. PyAutoGalaxy,
PyAutoLens and PyAutoArray are read-only inputs. No solver, dependency,
production API, config-default, or grid-cap change. No HPC or real-data fitting.
Medium scope: two synthetic fixtures, CPU fp64, bounded evidence and one report.

## High-level plan

1. Map current dispatch and JIT boundaries; mark historical findings resolved or live.
2. Compare both engines on a simple lens control and a small multi-plane cluster.
3. Measure cold/warm costs and a time-limited disabled-JIT control.
4. Publish a supported dispatch contract and exact next implementation scope.

## Detailed implementation plan

- Read scripts/AGENTS.md; reuse conventions and geometric comparisons from
  scripts/misc/critical_curves_zero_contour.py and the synthetic cluster setup
  in scripts/cluster/visualization.py. Read current source at pinned commits:
  Galaxy autogalaxy/util/plot_utils.py (_critical_curves_method,
  _critical_curves_from, _caustics_from), operate/lens_calc.py (from_tracer,
  _critical_curve_list_via_zero_contour), and Lens cluster/plot/cluster_plots.py.
- Add scripts/cluster/critical_curves_dispatch_audit.py, a bounded evidence
  driver: simple analytic control plus cluster with two source redshifts;
  LensCalc.from_tracer(use_multi_plane=True, plane_j=j) for each source plane.
  Test tangential/radial curves and caustics, reporting empty/missing components
  explicitly. Separate automatic-seed behavior from explicit-seed controls.
- Compare component coverage, centroids, enclosed areas and distance to a
  refined marching-squares reference. Record effective grid extent/resolution;
  use two resolutions to expose convergence and the existing evaluation cap.
  Define tolerances against the analytic control and reference convergence,
  not by relaxing them to make engine disagreement pass.
- Record CPU fp64 cold first call and repeated warmed calls with synchronization;
  time-limit each zero-contour worker to 120 seconds, including a single
  JAX_DISABLE_JIT=1 control. Record timeout/error honestly, never as a numerical
  pass. Distinguish internally compiled contour tracing from outer-jit support
  of Python/list/NumPy return wrappers. Do not assume backend=xp implies tracing.
- Save scripts/cluster/critical_curves_dispatch_evidence.json with code/dependency
  versions, fixture/engine/settings, geometry metrics, timing and status.
  scripts/cluster/CRITICAL_CURVES_DISPATCH.md records current vs historical
  findings, supported/default/explicit-engine behavior, missing-dependency and
  disabled-JIT policy, plane selection and proposed follow-up files/tests.
  Recommend rather than implement any new auto-dispatch API.
- Summarization is read-only. Validate evidence schema/provenance, analytic control,
  geometry recomputation, existing zero-contour regression, full workspace smoke,
  formatting and diff checks. Keep the slow audit outside PR smoke; identify the
  bounded regressions that the eventual implementation must wire into CI.

## Acceptance and handoff

One workspace evidence PR with reproducible commands and a concrete dispatch
contract, including failures and unsupported combinations. Phase 3 stays open;
only after reviewing this evidence, issue the next bounded production task.
No later arc issues. Phase 11 remains dropped.

## Preflight

Heart feed GREEN on 2026-10-02. No active repo claim; workspace main clean.
Branch: feature/critical-curves-dispatch-audit.
Planned bundle: .worktrees/critical-curves-dispatch-audit inside PyAutoLabs.
Plan awaiting explicit approval; no issue or implementation worktree created.

Brain classified this as direct research. Its size heuristic initially scored
too-large (20) with read-only library references. After restricting routing to
the sole workspace target it still scores 13 / too-large; retain declared medium
because this is two CPU fixtures and an evidence report, with no production
API change. Re-slice if the bounded matrix exposes broader required work.

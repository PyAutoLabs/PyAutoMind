# Critical-curve dispatch: current cluster evidence and contract

Type: research
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/337
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

Plan approved by human “go” on 2026-10-02; issued as #337.

## Human scope update — 2026-10-02

User: "This also feels like work which, once were done, belongs in autolens_profiling (in its lens or misc folder) as a task which we build up a wiki which adds more information and research for us to draw on as we run more expwriment. We do of course still need autolens_workspace_test examples for CI."

This supersedes the original workspace-only artifact placement. The experiment
moves to autolens_profiling scripts/lens/critical_curves/dispatch.py, versioned
JSON/PNG under results/lens/critical_curves/, a results/notes ledger and an indexed
wiki/campaigns/critical_curves.md page. Workspace_test retains only the small
scripts/cluster/critical_curves.py numerical regression, wired into smoke_tests.txt.
One task / existing issue #337, one PR per affected repository, no new phase issue.

Repo claim conflict: point-source-search-nautilus-leaf claims autolens_profiling
for PR #361. User explicitly answered "Allow concurrent, separate scope".
That PR touches point-source campaign ledgers and a fixed-light test; this task
is restricted to critical-curves files plus lens/wiki navigation links.
Profiling branch feature/critical-curves-dispatch-audit, base 4d6523f. Its canonical
checkout has unrelated untracked dataset/abell_1201/; it is untouched.

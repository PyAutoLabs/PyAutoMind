## evaluation-grid-cap-field
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/645
- completed: 2026-10-04
- epic: cluster-strong-lensing (phase 3b)
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/646
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/343
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/365
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/646
- PyAutoGalaxy#646 merged 2026-10-02 (2e36de4e). `LensCalc.evaluation_grid` keeps the effective zoom's physical field and centre under the grid cap. The real-decorator witness now gives 1000x1000 at 0.06 arcsec, where it used to give 1000x1000 at 8.333 arcsec. The fix is included in release 2026.10.4.1. The pending-release key above is carried verbatim because /prm never clears it; /review_release clears it.
- autolens_profiling#365 merged 2026-10-02 (9d0b1317). Adds before/after evidence to the critical_curves campaign ledger and wiki.
- autolens_workspace_test#343 merged 2026-10-04T19:07Z (head fcd6bd5, merge ebb9c866). Adds the cap invariant to the required `scripts/cluster/critical_curves.py` example. It stayed DRAFT until the Galaxy release, then went through /prm.
- Validation: 1315 full and 49 focused Galaxy tests pass, and the companion smoke passes 33/33 (501.91s).
- Notes: `Zoom2D.region` square-padding policy and origin convention were deliberately left unchanged.

## Original prompt

# Preserve the LensCalc evaluation field when the grid cap activates

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- autolens_workspace_test
- autolens_profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-10-02
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/645
Epic: cluster-strong-lensing
Phase: 3b
Parent: draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md
Filed: 2026-10-02

## Original request (verbatim)

Continue the 'Cluster strong lensing — Source & Cluster arc' epic. Its canonical state lives in draft/feature/autolens/source_cluster_arc.md — read that ledger (and any DECISIONS/RESULTS files beside it) first. Cross-check this epic's entry in PyAutoMind/epics.md, any related rows in PyAutoMind/active.md, and the referenced repos' open issues and PRs, to work out the last completed phase and what is currently in flight. Then pick the next logical step and continue it through the normal workflow (/start_dev — filing the phase's prompt first if none exists), updating the ledger as the work advances. Note: 12 phased prompts under draft/; issue phases ONE at a time as predecessors near shipping — no bulk issue queues. Science half: the PyAutoCortex project ledger of the science project it births (arc phase 11).

Continuation instruction: "prm and continue"

## Evidence and dependency

Phase 3a: autolens_workspace_test#337; research PR autolens_profiling#364,
CI PR autolens_workspace_test#341. Do not queue later phases. Audit artifacts:
results/notes/critical_curves_dispatch.md and wiki/campaigns/critical_curves.md
in autolens_profiling. Its real-decorator witness transforms a 60-arcsec field
(120×120 at 0.5 arcsec, requested 0.05) into 1000×1000 at 8.333333 arcsec.
Expected capped sampling is 1000×1000 at 0.06 arcsec. Dimensional error is in
PyAutoGalaxy/autogalaxy/operate/lens_calc.py:evaluation_grid.

## High-level plan

1. Fix capped sampling to retain the effective zoom field and centre, bounding both axes.
2. Specify rounding for non-square effective zoom shapes and keep below-cap behaviour stable.
3. Add independent geometry unit tests plus the small exact witness to required workspace CI.
4. Record before/after evidence and the fix in the profiling campaign.

## Detailed plan for approval

- Change only `evaluation_grid` in @PyAutoGalaxy. Derive capped scalar pixel scale
  from the effective zoom's physical extent and cap, rather than a dimensionless
  ratio. Check the longer axis; compute the shorter shape with conservative
  rounding so the field is not cropped. Bound both dimensions and document any
  subpixel padding. Preserve the current effective zoom centre.
- `Zoom2D.region` deliberately pads toward a square; do not redefine its mask
  support policy, introduce anisotropic pixels, or silently fix its origin
  convention in this patch. Non-square effective shapes (including odd-size
  differences) must retain their footprint within the stated rounding bound.
- Add NumPy tests in `test_autogalaxy/operate/test_evaluation_grid.py`, using a
  decorated grid recorder: exact 120×120 witness, both axis orientations,
  odd rectangular dimensions, shifted/masked effective zooms, below-cap and
  already-evaluation-grid paths. Avoid million-point Hessian evaluation.
- Add the fixed cap invariant to the existing small required
  @autolens_workspace_test `scripts/cluster/critical_curves.py` example. Keep
  its analytic per-plane curve and caustic checks.
- Append @autolens_profiling's ledger/wiki with before/after captured-grid
  evidence. Preserve the phase-3a JSON and measured source unchanged.
- Run focused and full Galaxy tests, the changed workspace example and required
  smoke through Heart; ship library first with linked workspace/research PRs.
- Related draft `lenscalc_masked_grid_caustic_differs_from_unmasked.md` remains
  independent: no claim that this cap fix resolves its ellipticity discrepancy.

## Exclusions

No engine/default changes, seed coverage or tracing-budget policy, outer-JIT
API, general masked-caustic fix, magnification map, or Cortex revival.

Proposed branch: feature/evaluation-grid-cap-field. Plan/branch approval and
fresh repo-claim survey are required before issue/worktree/source changes.

## Approval — 2026-10-02

Human answered "Approve plan and separate scope". Both phase-3a PRs are now
merged. Approval covers the stated effective-Zoom2D footprint/rounding contract
and concurrency alongside Galaxy docs, workspace numerical-audit and point-solver
ledger tasks, with their files untouched. No further phases are authorized for
bulk issue creation.

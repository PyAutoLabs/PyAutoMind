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

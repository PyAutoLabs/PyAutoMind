# JIT cache not hit in modeling_visualization delaunay/rectangular scripts

Type: bug
Target: autolens
Repos:
- PyAutoLens
- autolens_workspace_test
Themes:
- jax-compile
- visualization
- pixelization
Difficulty: medium
Autonomy: safe
Priority: normal
Status: draft
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-07-30 (backfilled from git)

## Symptom

Found by the 2026-07-30 parked-script sweep (autolens_workspace_test#234): both
`imaging/visualization/modeling_visualization_delaunay_jit.py` (52s) and
`modeling_visualization_rectangular_jit.py` (36s) now FAIL their own JIT-cache
regression assertion:

    AssertionError: Cached call (2.451s) not faster than compile (2.722s) —
    JIT cache is not being hit.

The scripts run fast enough now (previously parked >300s), but the second call
recompiles instead of reusing the cache — the known closure cache-busting
failure mode (memory: JAX closure cache-busts — cache (closure, solver) on the
instance). The plain `modeling_visualization_jit.py` variant still exceeds the
300s cap, so only the mesh variants expose the assertion today.

## Scope

Reproduce the cache miss (both scripts, entries re-tagged NEEDS_FIX 2026-07-30
in autolens_workspace_test config/build/no_run.yaml), identify what re-traces
between calls on the delaunay/rectangular visualization path (closure identity,
non-weakref'd solver, or per-call object construction), fix the producer, and
un-park the two scripts.

Merged autolens_workspace_test#376 (human /prm, 2026-11-27), from shift 2026-11-26-pm2.

The JIT cache was always hit. The probe timed an already-warm call, so the draft's hypothesis was refuted. The probe now times a cold analysis: rectangular 11.73s→0.64s (18.2x) and delaunay 21.20s→0.91s (23.3x). Both scripts exit 0 end to end, and the 2 no_run scripts are un-parked.

Decision taken (accepted at /prm): a workspace-only fix, and the zero_contour perf guard is now a cold/warm ratio, not a fixed 100 ms (the #148 pattern). Two independent Opus reviews were CLEAN. Heart GREEN. The PyAutoArray eager recompiles are filed as a draft.

## Original prompt

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
Consequence: glance
Witness: `modeling_visualization_delaunay_jit.py` and `modeling_visualization_rectangular_jit.py` pass their own JIT-cache assertion (cached call faster than compile), the PR names what re-traced between calls (closure identity, un-weakref'd solver or per-call construction) and the producer that fixed it, and both entries lose their NEEDS_FIX tag in `autolens_workspace_test/config/build/no_run.yaml`.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-26 bae1101a (PyAutoLens), be51efb0 (autolens_workspace_test)
Lane: any
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

# Delaunay-family JAX modules never hit the persistent compilation cache

Type: research
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoNerves
Themes:
- jax-compile
- pixelization
Difficulty: medium
Autonomy: safe
Priority: medium
Status: formalised
Consequence: judge
Review-minutes: 20
Unattended: ready
Filed: 2026-07-28 (backfilled from git)

Found during the MultiStartProdigy compile census (autolens_profiling#93):
every `delaunay_matern` transform recompiles at cold cost in **every process**
(warm compile ≈ cold, 26–28 s, n=8 process pairs), while `knn`,
`pixelization` (rect kernel-CDF) and `mge` warm to 0.2–4 s from the persistent
cache. Same probe, same cache mechanics — the miss is model-specific.

Prime suspect: the qhull `pure_callback` in the Delaunay tables path
(PyAutoArray). Callback custom_calls embed a process-specific descriptor in
the serialized HLO, so the persistent-cache key never matches across
processes. knn (pure-JAX, no host callback) caching perfectly is the control.

## Scope

1. Confirm the mechanism (e.g. dump HLO from two processes and diff the
   custom_call attributes; or probe a minimal `pure_callback` toy).
2. Investigate fixes, cheapest first:
   - jax config knobs that strip volatile pointers from cache keys (the
     `jax_remove_custom_partitioning_ptr_from_cache_key` family — check what
     jax 0.10.x offers for callback descriptors); would land as an
     autonerves `jax_wrapper` default like #128/#132.
   - stable callback registration in autoarray (if jax keys on the callable
     identity, a module-level function vs closure may already fix it).
   - upstream jax issue if neither works.
3. Cost if unfixed: ~40–65 s trace+compile per process forever on the
   delaunay family (the census table in
   `autolens_profiling/scripts/misc/jax_compile/README.md`).

<!-- filed 2026-07-28 from the multistart-prodigy-compile census (autolens_profiling#93) -->

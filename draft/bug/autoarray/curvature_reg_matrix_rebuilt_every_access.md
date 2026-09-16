# `curvature_reg_matrix` rebuilds `F + H` on every access — and the docstring's reason not to cache it is stale

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
Themes:
- inversion
- performance
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Witness: An instrumented likelihood call reports `n_calls >= 3` on
`AbstractInversion.curvature_reg_matrix`; after the fix `n_calls` is 1 per evaluation on the
numpy/numba path, every log-evidence is unchanged to 1e-12 relative, and peak memory does not
rise by more than one (n,n) array.
Review-minutes: 20
Filed: 2026-09-14
Folded-into: autolens_profiling#267

`AbstractInversion.curvature_reg_matrix`
(`autoarray/inversion/inversion/abstract.py:358-370`) is a plain `@property`. Its body is

```python
return self._xp.add(self.curvature_matrix, self.regularization_matrix)
```

— an **out-of-place** add that allocates a fresh (n,n) array on **every access**. It is
reached at least three times per likelihood evaluation:

| Site | Path |
|---|---|
| `abstract.py:613` | inside `reconstruction`, under edge zeroing — and then subset `[ids_to_keep][:, ids_to_keep]`, i.e. **two further full fancy-index copies** |
| `abstract.py:647` / `:655` | inside `reconstruction`, the non-edge-zeroed branches |
| `abstract.py:894` -> `:388` / `:397` | the `log_det_curvature_reg_matrix_term` path, via `curvature_reg_matrix_reduced` (itself also a plain `@property`), with another `[ids_to_keep][:, ids_to_keep]` pair at `:397` |
| `abstract.py:1026` | the defensive `np.asarray(self.curvature_reg_matrix)` diagnostic path |

At the HST fiducial (n = 1500, fp64) one such array is ~18 MB; at n = 4000 it is ~128 MB.

## The part that makes this a bug and not just a missed optimisation

The docstring on that property explains why it is *not* cached:

> "For a single mapper, this function overwrites the cached `curvature_matrix`, because for
> large matrices this avoids overheads in memory allocation. The `curvature_matrix` is removed
> as a cached property as a result, to ensure if we access it after computing the
> `curvature_reg_matrix` it is correctly recalculated in a new array of memory."

**The code no longer does that.** There is no in-place overwrite and no cache invalidation —
the body is a plain out-of-place `_xp.add`. The docstring describes an earlier implementation
that wrote into `curvature_matrix`'s buffer, and the hazard it warns about (a stale
`curvature_matrix` cache) is the reason the property is not cached. That reason appears to have
evaporated when the implementation changed, and the docstring kept it alive.

So the first deliverable is not a fix, it is a determination: **does the stated hazard still
exist?** Read the history of that property, confirm the in-place form is gone, and confirm
nothing else depends on `curvature_reg_matrix` returning a freshly-allocated array each time.
If the hazard is real and merely mis-described, say so and fix the docstring instead — that is
a perfectly good outcome for this prompt and it stops the next person re-deriving the same
question.

## Scope the fix by backend before making one

Do not assume the cost is universal. Under `jax.jit` XLA's common-subexpression elimination
plausibly collapses the duplicate adds already, in which case this is a **numpy / numba-only**
cost and the fix should be scoped accordingly. Measure both backends before changing anything:
an `n_calls` count is not a cost until it survives the compiler.

The counterweight to caching is memory, not correctness: a `cached_property` holds an (n,n)
fp64 array alive for the life of the inversion, which is ~128 MB at n = 4000. Weigh that
against the allocations saved, and against the fact that GPU work is now pushing toward larger
N.

## Why it is worth doing

Two costs, and the second is worse than the first.

1. **The direct cost** — redundant (n,n) allocations and adds in the hot path of every
   pixelized likelihood evaluation, on every backend where the compiler does not remove them.
2. **The reporting cost.** Every sequential-touch profiling decomposition in `autolens_profiling`
   (`scripts/imaging/likelihood_breakdown/delaunay_numba.py:596-672` and its siblings) measures
   **one** of these builds in its "F + H" row and silently loads the other two into its
   "reconstruction solve" and "log det" rows. Those rows are published in
   `results/notes/` and get quoted. Anyone reading them today is over-attributing cost to the
   solver — which is exactly the error the GPU fixed-lens-light epic spent six phases working
   around, and which the numba campaign's phase 1 (autolens_profiling#263) had to build an
   access-counting harness to avoid.

Phase 1 pins the observation from the profiling side: its test asserts `n_calls >= 2` on this
property, so if this prompt lands a cache, that test fails loudly and the decomposition is
updated deliberately rather than shifting underneath a published number. **Coordinate with
autolens_profiling#263 when this ships** — the failing assertion is the intended handshake, not
a regression.

## Fold-in scope (2026-09-16 — lever 3 of autolens_profiling#267)

Folded into #267 lever 3 (one shared Cholesky of `F + lambda*H`) on the human's ask; not issued
separately. Scope as set there:

1. **Determine** whether the docstring hazard on `AbstractInversion.curvature_reg_matrix`
   (`abstract.py:358-371`) still exists. `git` shows the in-place `curvature_matrix +=` form was
   removed around `0766edd4` (2025-06-26); the body is now a plain out-of-place `_xp.add`.
2. **Fix or cache on the numpy/numba path only**, measured with the phase-1 `call_accounting`
   harness, and update the `n_calls >= 2` handshake test
   (`autolens_profiling/scripts/misc/test/test_fixed_light_numba.py:546`) deliberately.
3. **Fix the stale docstring regardless** of which option lands.

**Do not touch the JAX branch.** The GPU session (epic `hst-gpu-non-solver-residue`, phase 1) is
producing an optimized-HLO census that answers whether XLA already collapses the duplicate adds
under the production jit, and will post that verdict on #267.

Correction to the count above: this draft counted 3+ reaches per evaluation; on the default
(edge-zeroed) path it is **2** — `:613` inside `reconstruction` and `:894 -> :388 / :397` via
`curvature_reg_matrix_reduced`. `:647` / `:655` are the non-edge-zeroed branches and `:1026` is a
diagnostic path.

## Out of scope

The two `[ids_to_keep][:, ids_to_keep]` fancy-index copy pairs at `:397` and `:613-615` are a
separate, larger question (a masked or view-based subset), and the edge-zeroing design they
belong to is settled. Note the cost; do not redesign it here.

# Fix release JAX runtime compatibility and likelihood parity

Type: bug
Target: health_fixes
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: formalised

## 2026-08-09 — EVERY SCRIPT PATH BELOW IS STALE (they moved, they were not deleted)

Checked by the draft/ sweep. All 6 scripts named in § Scripts return **404** at the
paths written below, and **all 6 still exist** under a renamed layout. Do not read the
404s as "the scripts were deleted" or "this was fixed by removal".

Two systematic renames landed in both test workspaces since this prompt was filed:

```
scripts/jax_likelihood_functions/<dataset>/X.py  ->  scripts/<dataset>/jax_likelihood/X.py
scripts/<dataset>/modeling_visualization_jit.py  ->  scripts/<dataset>/visualization/modeling_visualization_jit.py
scripts/multi/...                                ->  scripts/multi_dataset/...
```

Verified in `autolens_workspace_test` (`4cea3f8c`, cloned) and
`autogalaxy_workspace_test` (raw, every path resolves 200). This is the **same rename
family** that cost a previous session time on
`draft/bug/autolens/jax_point_source_point_smoke_sentinel.md` — treat a 404 in this
cluster as path drift until proven otherwise.

Corrected paths:

| named in § Scripts | actual path on main | repo |
|---|---|---|
| `…/jax_likelihood_functions/imaging/delaunay_mge.py` | `scripts/imaging/jax_likelihood/delaunay_mge.py` | autogalaxy_workspace_test |
| `…/jax_likelihood_functions/interferometer/delaunay_mge.py` | `scripts/interferometer/jax_likelihood/delaunay_mge.py` | autogalaxy_workspace_test |
| `…/jax_likelihood_functions/multi/delaunay_mge.py` | `scripts/multi_dataset/jax_likelihood/delaunay_mge.py` | autogalaxy_workspace_test |
| `…/jax_likelihood_functions/interferometer/delaunay_mge.py` | `scripts/interferometer/jax_likelihood/delaunay_mge.py` | autolens_workspace_test |
| `…/jax_likelihood_functions/multi/rectangular.py` | `scripts/multi_dataset/jax_likelihood/rectangular.py` | autolens_workspace_test |
| `…/jax_likelihood_functions/multi/rectangular_mge.py` | `scripts/multi_dataset/jax_likelihood/rectangular_mge.py` | autolens_workspace_test |

### Parking state — read before assuming CI still exercises these

**4 of the 6 are parked SLOW**, all dated 2026-07-14 and all citing PyAutoHeart#74
(flaking at the 1800s `mode=release` cap):

- `autogalaxy_workspace_test` `no_run.yaml`: `imaging/jax_likelihood/delaunay_mge.py`,
  `interferometer/jax_likelihood/delaunay_mge.py`, `multi_dataset/jax_likelihood/delaunay_mge`
- `autolens_workspace_test` `no_run.yaml`: `interferometer/jax_likelihood/delaunay_mge.py`

The two `multi_dataset/jax_likelihood/rectangular*.py` scripts are **not** parked.

Also note `autolens_workspace_test` parks `multi_dataset/jax_likelihood/delaunay.py`
as `NEEDS_FIX 2026-08-01 - hangs to the 1800s release cap in 3 of 5 release-integrate
runs` — a sibling in the same family, filed after this prompt, suggesting the JAX
likelihood timeout story has moved on independently of this prompt.

**This changes what the prompt's premise means.** A parked script cannot fail in
release validation, so the 2026-08-07 release drive's Stage 3 result (51/51 jobs green,
`657p/0f/101s/0t` — note the **101 skips**) is *not* evidence these were fixed. Nothing
here is graded shipped; the failures are simply no longer being provoked. Note too that
the parkings are for **timeouts**, a different failure from the defect this prompt
describes — so unparking is a precondition for reproducing it at all.

Not re-graded here: whether the underlying defect still reproduces. That needs real
runs, which a cloud session cannot do.

---
## Context

Six JAX likelihood scripts failed with the rehearsed release stack. CI included
TensorFlow Probability using removed JAX internals and NumPy/JAX likelihood mismatches.
All six passed locally with current `main` and JAX 0.9.2, so verify whether upstream
library changes already fixed them or whether environment/order sensitivity remains.

Owners: @PyAutoArray, @PyAutoFit, @PyAutoGalaxy, @PyAutoLens,
@autogalaxy_workspace_test, and @autolens_workspace_test.

## Scripts

- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/imaging/delaunay_mge.py`
- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/interferometer/delaunay_mge.py`
- `autogalaxy_workspace_test/scripts/jax_likelihood_functions/multi/delaunay_mge.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/interferometer/delaunay_mge.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/multi/rectangular.py`
- `autolens_workspace_test/scripts/jax_likelihood_functions/multi/rectangular_mge.py`

## Required work

1. Reproduce in a clean source environment using the release dependency constraints and
   record exact JAX, jaxlib, TFP, NumPy, nufftax, and pynufft versions.
2. Confirm whether current `main` fixes every CI traceback without cached compiled state.
3. If TFP remains incompatible, fix or replace the owning library path rather than
   disabling JAX in JAX-specific scripts.
4. Investigate parity differences from data/model construction through inversion and
   regularization; do not merely loosen tolerances without a numerical error budget.
5. Add library regression tests and rerun all six scripts in both fresh processes and
   their normal directory sequence.

<!-- formalised retroactively by the Intake (Conception) Agent on 2026-07-08 -->

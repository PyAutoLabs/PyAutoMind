# `@PyAutoArray` rectangular mesh mapper: mirrored row weights + round-off-dependent cell assignment

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
- @autolens_workspace_test
- @autogalaxy_workspace_test
Difficulty: medium
Autonomy: human-required
Priority: high
Status: draft
Filed: 2026-08-26
Source: autolens_workspace_test#279 — found while diagnosing the eager/jit
divergence in `scripts/interferometer/jax_grad/gradient.py`; that symptom is a
consequence of this bug, not a separate issue.

## Summary

`adaptive_rectangular_mappings_weights_via_interpolation_from`
(`autoarray/inversion/mesh/interpolator/rectangular.py:452`) — the bilinear
mapper shared by **every** rectangular mesh — has two coupled defects:

1. **Mirrored row weights.** `t_row` is the fractional distance measured *from*
   `ix_down`, so `ix_up` must carry `t_row` and `ix_down` must carry
   `1 - t_row`. Lines 572-579 have them swapped. The column weights are
   correctly paired; only the rows are mirrored.
2. **Round-off-dependent cell assignment.** `ix_up = ceil(g)` collapses onto
   `ix_down` wherever `g` is exactly integral. `transform()` ends in
   `xp.clip(F_q, 0.0, 1.0)` (line 342), so saturated points land on exactly
   integer `g` *systematically*, not by chance. There the cell degenerates and
   `t_row` is forced to 0 by the `+ 1e-12` guard; a 1-ULP change in the traced
   grid moves the point off the plateau and jumps its weight a whole mesh row.

(2) is what makes the eager and jitted likelihoods disagree — the two
compilations differ by ~1e-16 in the traced grid, which is enough to flip the
assignment. (1) is why (2) cannot be fixed without a behaviour change.

## Evidence for (1) — mathematically decisive, no astronomy involved

A correct bilinear scheme must satisfy partition of unity **and** reproduce the
query position: `sum_i w_i * node_i == g`. Over 2000 random interior points plus
the exactly-integer cases, with `flatten(ix, iy) = (n - ix) * n + iy`:

```
CURRENT:  max|sum(w) - 1|        = 2.220e-16   (partition of unity OK)
          reproduces col coord   = 0.000000    (columns correct)
          reproduces row coord   = 0.999759    <-- nearly a full mesh cell
FIXED:    max|sum(w) - 1|        = 1.110e-16
          reproduces col coord   = 0.000000
          reproduces row coord   = 0.000000
```

The row interpolation is mirrored. Because the mirroring is *consistent*, the
surface stays smooth, which is why every FD/AD gradient check in the workspaces
passes — the mesh is effectively reflected in the row direction, not noisy.

## Evidence for (2)

Capturing arrays via `jax.debug.callback` inside the function, for Variant B of
`autolens_workspace_test/scripts/interferometer/jax_grad/gradient.py`:

| array | eager vs jit |
|---|---|
| `data_grid_over_sampled` | max abs diff 8.88e-16 (1 ULP) |
| `mappings` | 2 of 11312 entries differ, row 0: `[18 19 18 19]` → `[18 19 26 27]` |
| `weights` | max abs diff 0.512 |

Eager's `18 == 18` is `floor == ceil` — an exactly integer index, from
`(8-3) * 1.0 + 1 = 6.0` where the CDF clipped to exactly 1.0. The capture
confirms the plateau: exactly 2 entries at `0.0` and 2 at `1.0`.

## Fix (validated locally, needs review + a downstream sweep)

```python
# Step 4
ix_down = xp.clip(xp.floor(grid_over_index[:, 0]), 0, source_grid_size - 2)
iy_down = xp.clip(xp.floor(grid_over_index[:, 1]), 0, source_grid_size - 2)
ix_up = ix_down + 1
iy_up = iy_down + 1

# Step 7 — each corner gets its own weight; no 1e-12 guard needed
t_row = grid_over_index[:, 0] - ix_down
t_col = grid_over_index[:, 1] - iy_down
w_tl = t_row * (1 - t_col)          # tl = (ix_up,   iy_down)
w_tr = t_row * t_col                # tr = (ix_up,   iy_up)
w_bl = (1 - t_row) * (1 - t_col)    # bl = (ix_down, iy_down)
w_br = (1 - t_row) * t_col          # br = (ix_down, iy_up)
```

Steps 5 and 6 are unchanged; the pairing above matches their existing
`[tl, tr, bl, br]` ordering.

Measured with the full source-installed stack (jax/jaxlib 0.11.1, numpy 2.5.2,
scipy 1.17.1 — matching retime run 32741386752), on both Python 3.12 and 3.13:

- `pytest test_autoarray/` — **1220 passed**
- `autolens_workspace_test/scripts/interferometer/jax_grad/gradient.py` — green
  on **both** legs, all four variants, all three `assert_eager_jit_consistent`
  guards passing at the untouched `rtol=1e-10`, eager/jit gap exactly `0.0`.
  3.13: 83s, 3.12: 86s (300s cap).

## Downstream impact — the reason this is `human-required`

The fix changes reconstructions wherever a rectangular mesh is used. Measured on
`autolens_workspace_test/scripts/imaging/jax_likelihood/rectangular.py`: log
likelihood moves `-651692.997799` → `-650470.379097`, a shift of **+1222.6** —
a *better* fit, the direction expected if the interpolation had been mirrored.

**16 scripts** in `autolens_workspace_test` carry hardcoded `EXPECTED_LOG_*`
constants on adaptive rectangular meshes and will need regenerating:
`interferometer/{datacube/rectangular, jax_likelihood/{rectangular,
rectangular_dspl, rectangular_mge, rectangular_sparse}}`,
`imaging/jax_likelihood/{rectangular, rectangular_rtu, rectangular_dspl,
rectangular_dspl_rtu, rectangular_mge, rectangular_mge_rtu}`,
`multi_dataset/jax_likelihood/{rectangular, rectangular_rtu, rectangular_mge,
rectangular_mge_rtu}`, `misc/jax_assertions/sparse_operators`.
`autogalaxy_workspace_test` exercises the same `xp` path and needs the same
sweep.

Note `PyAutoArray/AGENTS.md`: unit tests are NumPy-only, so `test_autoarray/`
passing is necessary but not sufficient — the workspace parity scripts are the
real gate.

## Task

1. Decide whether the corrected pairing is the intended geometry. The mirroring
   is consistent, so an argument that the current behaviour is deliberate would
   have to explain the linear-reproduction failure above; absent that, treat it
   as a bug.
2. Land the fix in PyAutoArray with a regression test asserting linear
   reproduction (`sum_i w_i * node_i == g`) and continuity across an exactly
   integer `grid_over_index` — both of which the current code fails.
3. Sweep the affected workspace scripts and regenerate their constants,
   library-first.
4. Only then remove the `interferometer/jax_grad/gradient.py` `NEEDS_FIX` entry
   from `autolens_workspace_test/config/build/no_run.yaml` (issue #279).

## Do not

- Widen `assert_eager_jit_consistent`. At `rtol=1e-10` it caught a real library
  bug; that is exactly its job.
- Regenerate the `EXPECTED_LOG_*` constants before deciding item 1 — that would
  bake the mirrored geometry in as the reference.

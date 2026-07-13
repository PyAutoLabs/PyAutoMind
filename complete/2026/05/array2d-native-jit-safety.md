## array2d-native-jit-safety
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/338
- completed: 2026-05-25
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/339
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/123, https://github.com/PyAutoLabs/autolens_workspace/pull/208, https://github.com/PyAutoLabs/autogalaxy_workspace/pull/104

## Original prompt

# Refactor `Array2D.native` / `array_2d_via_indexes_from` for JAX-jit safety

`SimulatorImaging.use_jax=True` and `SimulatorInterferometer.use_jax=True`
work end-to-end on **JAX-eager** today (shipped in Phase 2 of
`z_features/jax_user_intro.md` — PRs PyAutoArray#335, #336 +
PyAutoLens#539, #540 + PyAutoGalaxy#442, #443) but **cannot currently
be wrapped in `@jax.jit`**. This task unblocks that.

## The blocker

When the user wraps a simulator in their own `@jax.jit`:

```python
simulator = al.SimulatorImaging(..., use_jax=True)

@jax.jit
def simulate(tracer):
    return simulator.via_tracer_from(tracer=tracer, grid=grid)
```

The call fails with `TracerArrayConversionError: __array__() was called
on traced array`. The traceback (full chain captured during Phase 2 PR 2
implementation):

```
File ".../autolens/imaging/simulator.py", line 70, in via_tracer_from
File ".../autoarray/dataset/imaging/simulator.py", line 229, in via_image_from
File ".../autoarray/structures/arrays/uniform_2d.py", line 295, in native
File ".../autoarray/structures/arrays/uniform_2d.py", line 243, in __init__
File ".../autoarray/structures/arrays/array_2d_util.py", line 147, in convert_array_2d
File ".../autoarray/structures/arrays/array_2d_util.py", line 516, in array_2d_native_from
File ".../autoarray/structures/arrays/array_2d_util.py", line 562, in array_2d_via_indexes_from
```

The two failing sites are:

1. **`array_2d_via_indexes_from`** (`array_2d_util.py:535-562`) — for the
   JAX path it does `array.at[tuple(native_index_for_slim_index_2d.T)].set(array_2d_slim)`.
   The `tuple(jax_array.T)` call iterates the outermost axis of the JAX
   array, which forces `__array__()` and breaks the trace.

2. **`Array2D.native`** (`uniform_2d.py:295`) — accessed by the simulator
   to re-wrap the image against the all-false output mask
   (`Array2D(values=image.native, mask=mask)`). Routes through (1).

3. **`Imaging.trimmed_after_convolution_from`** — same `.native` access on
   the post-convolution dataset.

## Why the simulator workaround in PR 2 doesn't fully solve it

Phase 2 PR 2 (`PyAutoArray#335`) added a partial workaround at the
simulator's image re-wrap:

```python
# autoarray/dataset/imaging/simulator.py
if xp is np:
    image = Array2D(values=image.native, mask=mask)
else:
    image = Array2D(values=image.array, mask=mask)
```

That guard skips `.native` for the image re-wrap *inside the simulator*.
But the `.native` access still fires later inside
`Imaging.trimmed_after_convolution_from` (PyAutoLens simulator override
line 70) — and any other consumer of `.native` outside the simulator
also breaks under JIT.

The full fix is in `array_2d_via_indexes_from` itself.

## Scope

**In scope:**
- Refactor `array_2d_via_indexes_from` to use JAX-traceable operations
  on the JAX path. The numpy path can stay as indexed assignment; the
  JAX path needs an equivalent that doesn't iterate a tuple of native
  indices in Python.
- Likely fix: replace
  `array.at[tuple(native_index_for_slim_index_2d.T)].set(array_2d_slim)`
  with `jnp.zeros(shape).at[native_index_for_slim_index_2d[:, 0], native_index_for_slim_index_2d[:, 1]].set(array_2d_slim)`
  — uses 2D advanced indexing rather than tuple-unpacked rows, no Python
  iteration of a traced array.
- Verify the change end-to-end: a `SimulatorImaging(use_jax=True)`
  call wrapped in `@jax.jit` should now succeed and return an `Imaging`
  with `jax.Array` data.
- Remove the temporary `if xp is np: ... else: ...` guard in
  `autoarray/dataset/imaging/simulator.py:229` once the underlying
  `.native` issue is fixed (it's now redundant).
- Update the `SimulatorImaging.use_jax=True` and `SimulatorInterferometer.use_jax=True`
  docstrings to drop the "@jax.jit currently blocked by Array2D.native"
  caveat.

**Out of scope:**
- Other autoarray jit-incompatibilities not in this `array_2d_via_indexes_from`
  / `.native` path. If new ones surface during validation, file as
  separate prompts.
- Workspace doc updates beyond the simulator docstring caveat removal.
  The workspace `__JAX Variant__` blocks already show the user-facing
  `@jax.jit` pattern; they'll just start working at runtime once this
  ships, no doc changes needed.

## Implementation steps

1. **Identify all `.native` use sites that fire under JIT.** Grep
   PyAutoArray for `array_2d_via_indexes_from`, `array_2d_native_from`,
   `.native`. Map which fire during a typical
   `SimulatorImaging.via_tracer_from(use_jax=True)` call.

2. **Refactor `array_2d_via_indexes_from`** in
   `PyAutoArray/autoarray/structures/arrays/array_2d_util.py`:

   ```python
   def array_2d_via_indexes_from(array_2d_slim, shape, native_index_for_slim_index_2d, xp=np):
       array = xp.zeros(shape, dtype=array_2d_slim.dtype)
       if xp.__name__.startswith("jax"):
           # 2D advanced indexing — no Python iteration of the index tuple.
           return array.at[native_index_for_slim_index_2d[:, 0],
                           native_index_for_slim_index_2d[:, 1]].set(array_2d_slim)
       array[tuple(native_index_for_slim_index_2d.T)] = array_2d_slim
       return array
   ```

3. **Audit other slim/native helpers** for the same pattern
   (`native_index_for_slim_index_2d_from`, `array_2d_slim_from`,
   `array_2d_via_mask_from`, etc.). Fix any that use Python iteration
   of traced arrays.

4. **Remove the simulator temporary guard** in
   `autoarray/dataset/imaging/simulator.py:229`:
   ```python
   # Before (Phase 2 PR 2 workaround):
   if xp is np:
       image = Array2D(values=image.native, mask=mask)
   else:
       image = Array2D(values=image.array, mask=mask)

   # After (now redundant):
   image = Array2D(values=image.native, mask=mask)
   ```

5. **Update docstrings** on `SimulatorImaging.__init__` and
   `SimulatorInterferometer.__init__` to drop the
   "Note: @jax.jit wrapping is currently blocked by Array2D.native ..."
   caveat.

6. **Tests:**
   - Library unit tests stay NumPy-only per [[feedback_no_jax_in_unit_tests]].
   - Add a workspace_test parity script that wraps `SimulatorImaging(use_jax=True).via_tracer_from`
     in `@jax.jit` and asserts the JIT'd dataset matches the eager-JAX
     dataset to atol=1e-8 (extend the existing
     `autolens_workspace_test/scripts/imaging/simulator_use_jax_parity.py`
     — its disabled `@jax.jit` test block is currently a `print` saying
     "currently blocked"; restore the active test).
   - Same for interferometer: extend `autolens_workspace_test/scripts/interferometer/simulator_use_jax_parity.py`.

7. **Workspace doc cleanup:** the `__JAX Variant__` blocks in
   `autolens_workspace/scripts/{imaging,interferometer,group}/simulator.py`
   and the `autogalaxy_workspace/scripts/{imaging,interferometer}/simulator.py`
   each carry a "@jax.jit wrap is currently blocked by Array2D.native"
   note. Sweep them and drop those notes.

## Validation

After all changes:

1. `SimulatorImaging(use_jax=True)` + `@jax.jit` works end-to-end on a
   typical lens (verified via the workspace_test parity script).
2. `SimulatorInterferometer(use_jax=True)` + `@jax.jit` works
   end-to-end (verified via the analogous parity script).
3. Full PyAutoArray + PyAutoLens + PyAutoGalaxy test suites pass.
4. The simulator `__JAX Variant__` blocks in autolens / autogalaxy
   workspace `simulator.py` scripts now run cleanly under `@jax.jit`.

## References

- Phase 2 PR 2 — `PyAutoArray#335` — added the temporary simulator guard
  this task removes.
- Phase 0 design doc — `admin_jammy/notes/jax_interface.md` — the
  end-state of `Simulator.use_jax=True` was originally meant to support
  `@jax.jit` from the start; this refactor delivers on that.
- Phase 3a / 3b / 4a / 4b workspace PRs (autolens#203, autogalaxy#101)
  flagged the `.native` limitation in each `__JAX Variant__` block.
  Those notes need cleanup as step 7.

## Out-of-band notes

- This is the **only** known remaining structural JAX-compatibility gap
  in the simulator path. PointSolver already works under `@jax.jit`
  (it doesn't go through `.native`). Once this ships, the entire
  "JIT-it-yourself" image-simulation story is functional, not
  aspirational.

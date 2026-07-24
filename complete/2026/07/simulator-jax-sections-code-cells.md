## simulator-jax-sections-code-cells
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/339
- completed: 2026-07-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/340 (MERGED)
- summary: Converted the fenced ```python blocks inside the __JAX Variant__ / __Oversampled PSF__ docstring sections of imaging/interferometer/point_source simulator.py into real code cells (setup live, executing line commented with run-time/overwrite note), retitled with (Advanced), added to __Contents__, updated 5 cross-refs. Content fixes surfaced by making code real: interferometer snippet referenced nonexistent real_space_grid and had stale "pynufft not JAX-traceable" claim (installed TransformerNUFFT is JAX-native nufftax; live code now uses it — DFT would be enormous on the 800x800/1M-vis setup at that point); adjacent docstrings in imaging merged (current generator renders the second as a literal ''' code cell until PyAutoHands#197 merges); point_source commented var named positions_jax to avoid shadowing the saved positions. Validated: py_compile x7, three simulators rc=0 under smoke profile (dataset/ untouched — SKIP_VISUALIZATION no-ops writers), check_sizes OK, notebooks + navigator catalogue regenerated, CI 4/4 green. Heart YELLOW human-acked (3 reasons, recorded in entry). Ops: Mind checkout was on a concurrent session's branch all session — every registry write went via detached temp worktrees to main.

## Original prompt

# Simulator JAX / Oversampled-PSF sections: fenced code blocks → real code cells

**Work type:** docs (workspace)
**Target repo:** autolens_workspace
**Filed:** 2026-07-24

## Original request (verbatim)

> I do not like how imaging/simulator.py, and presumably other exampels, have this
> kind of in line python commenting to document JAX and over sampling: [quotes the
> `__JAX Variant__` and `__Oversampled PSF__` trailing docstring sections of
> `scripts/imaging/simulator.py`, which embed ```python fenced code blocks inside
> the docstring]. Can you make it so they use the usual docstring format (so in
> python scripts code has lint and color as normal, and in notebooks they are
> markdown and cells). But just comment out the actual simulation line with a note
> to avoid excessive run time and data overrites. Put (Advanced) next to both and
> make sure they are in the contents.

## Scope (surveyed)

Sections embedding ```python fenced code inside docstrings for JAX / over-sampling:

- `scripts/imaging/simulator.py` — `__JAX Variant__` + `__Oversampled PSF__`
- `scripts/interferometer/simulator.py` — `__JAX Variant__`
- `scripts/point_source/simulator.py` — `__JAX Variant__`

For each: split into docstring prose + real top-level code (lint/color in scripts,
markdown + code cells in generated notebooks). Setup lines (imports, simulator /
solver construction, `@jax.jit` wrappers) stay live; the executing simulation /
solve line (and any lines depending on its result) is commented out with a note
that it is skipped to avoid excessive run time and overwriting the shipped
dataset. Retitle sections `__JAX Variant (Advanced)__` /
`__Oversampled PSF (Advanced)__` and add both to each script's `__Contents__`.

Cross-references to the old section titles to update:
`imaging/simulator.py:142`, `imaging/likelihood_function.py:79`,
`guides/data_structures.py:434`, `guides/tracer.py:576`,
`guides/advanced/over_sampling.py:528`.

Regenerate notebooks after; smoke-test the three edited simulator scripts.

# Simplify start_here.py JAX section; move technical detail to guides/using_jax.py

Difficulty: easy
Autonomy: supervised

## Original request (verbatim)

> The JAX sectin of the autolens_workspace/start_here.py section is way too
> detailed for a new user, can you make it much simpler just focusing on how it
> is auto enabled for modeling, and move all the trechnical stuff to a
> guide/using_jax.py.

## Scope

- @autolens_workspace root `start_here.py`, `__JAX__` section (lines ~218-301):
  reduce to a short new-user-facing section — JAX is auto-enabled for lens
  modeling when installed (`pip install autolens[jax]`), falls back to NumPy
  with a warning otherwise, and a pointer to the new guide for everything else.
- Create `scripts/guides/using_jax.py` holding the technical material moved
  out: the vmap/jit search internals, `use_jax=False` / `PYAUTO_DISABLE_JAX=1`
  opt-outs, the "when you write `@jax.jit` yourself" patterns (custom
  simulations, custom likelihood functions), the JIT-it-yourself pointer to
  `lens_calc.py`, and the return-type contract (`jax.Array` vs
  `numpy.ndarray`, `.array` property).
- Tutorial-prose repo: narrative stays in the judgment tier per
  `PyAutoBrain/skills/WORKFLOW.md`.
- Regenerate notebooks after script edits.

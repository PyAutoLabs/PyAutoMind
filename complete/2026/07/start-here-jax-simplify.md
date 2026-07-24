## start-here-jax-simplify
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/336
- completed: 2026-07-24
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/338 + https://github.com/PyAutoLabs/autogalaxy_workspace/pull/162
- summary: Trimmed the ~83-line __JAX__ section of the root start_here.py in autolens_workspace AND autogalaxy_workspace to a short new-user version (JAX auto-enabled for modeling with the [jax] extra, one-time compile log line, NumPy fallback) and moved the technical material to a new scripts/guides/using_jax.py in each (auto-enabled internals, disabling JAX via use_jax=False / PYAUTO_DISABLE_JAX=1, writing @jax.jit yourself, JIT-ing library methods, return-type contract). Guides registered in navigator catalogues; notebooks regenerated per-file (avoided full generate.py rebuild churn). Gotchas: ag's old section cited nonexistent scripts/guides/api/data_structures.py — fixed to the real path after verifying content; autolens.jax.register_tracer_classes verified in installed stack before reuse; Feature-Agent large/phased score overridden (repo-count proxy, cosmetic single change); both PRs trued-up a stale .script_sizes.json snapshot inherited from earlier merged sweeps; task started while a stale active.md claim (remove-inline-standalones) was still registered — its PRs had already merged, so branches cut clean from post-merge main.

## Original prompt

# Simplify start_here.py JAX section; move technical detail to guides/using_jax.py

Difficulty: easy
Autonomy: supervised

## Original request (verbatim)

> The JAX sectin of the autolens_workspace/start_here.py section is way too
> detailed for a new user, can you make it much simpler just focusing on how it
> is auto enabled for modeling, and move all the trechnical stuff to a
> guide/using_jax.py.

Follow-up: "yes and make sure autogalaxy_workpace has all this too." —
@autogalaxy_workspace gets the same treatment (its root `start_here.py`
`__JAX__` section, lines ~176-247, mirrors the AutoLens one with the `ag.`
API; it also has no `using_jax.py` guide).

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
- @autogalaxy_workspace: same split — trim its root `start_here.py` `__JAX__`
  section the same way and create its `scripts/guides/using_jax.py` mirror
  (`ag.` API, no `lens_calc.py` pointer; keep the two guides structurally
  parallel).
- Tutorial-prose repo: narrative stays in the judgment tier per
  `PyAutoBrain/skills/WORKFLOW.md`.
- Register both new guides in the navigator catalogues; regenerate notebooks
  after script edits.
- Blocked at registration: autolens_workspace claimed by
  hide-autonerves-colab-autolens (workspace-dev), autogalaxy_workspace by
  hide-autonerves-colab-autogalaxy (awaiting-merge). Start after those ship.

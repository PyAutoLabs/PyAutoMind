# JAX pytree _partition crashes on instances without __dict__ (vars() TypeError) during vmap/jit

Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

JAX-fitting a shapelet model crashes when autofit flattens the model instance into a
pytree. Surfaced by the 2026-07-13 release-validation Stage-3 run (PyAutoHeart
workspace-validation `run_id=29266305445`, TestPyPI `2026.7.13.1.dev65501`) — `autogalaxy`
imaging `scripts/imaging/features/shapelets/modeling.py` FAIL under the release env profile
(JAX enabled).

Traceback:

```
scripts/imaging/features/shapelets/modeling.py:424   result = search.fit(model=model, analysis=analysis)
autofit/non_linear/search/nest/nautilus/search.py:189   fitness = Fitness(...)
autofit/non_linear/fitness.py:134   self._call = self._vmap
autofit/non_linear/fitness.py:486   func = jax.vmap(jax.jit(self.call))
autofit/jax/pytrees.py:168 (flatten) -> :152 (_partition)
    for name, value in vars(instance).items():
TypeError: vars() argument must have __dict__ attribute
```

Root cause — `autofit/jax/pytrees.py:152` (`_partition`) assumes every model instance /
component exposes `__dict__`; it calls `vars(instance)` unconditionally. A shapelet model
carries a component whose instance has no `__dict__` (e.g. `__slots__`-based or an
array-like leaf), so `vars()` raises. This blocks `jax.vmap(jax.jit(self.call))` in
`Fitness._vmap`, i.e. any JAX-accelerated fit whose model contains such a component.

Only exercised under the JAX/release profile (the curated smoke subset does not JAX-fit
shapelets), so the nightly release would not catch it — but it breaks JAX shapelet fitting
for users. Fix `_partition` to handle no-`__dict__` instances (fall back to
`__slots__` traversal / treat as an opaque leaf as appropriate) rather than assuming
`vars()`; add a JAX pytree-flatten unit test covering a slotted/array-like component.
Do NOT paper over it with a silent guard — see [[feedback_no_silent_guards]]. Cross-check
against the existing pytree PoC work ([[register_and_iterate]] history) for the intended
partition contract.

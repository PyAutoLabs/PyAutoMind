# Make `add_assertion` enforceable on the JAX likelihood path

Type: feature
Target: autofit
Repos:
- PyAutoFit
- autofit_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Issued: 2026-09-08
Consequence: review
Witness: an `autofit_workspace_test/scripts/jax_assertions/` script composes a model with an ordering assertion between compound priors (`(a0**2 + a1**2) > (b0**2 + b1**2)`), builds a JAX analysis and the `Fitness` Nautilus builds (`use_jax_vmap=True`) plus the non-vmapped one; for a violating vector both return the resample sentinel with no exception, for a satisfying vector both return the same log likelihood as the NumPy path to 1e-8, and `jax.jit` of the fitness compiles; numpy-only unit tests pin the new traced assertion evaluation and the unchanged NumPy resample path.
Review-minutes: 10
Unattended: ready


Make `model.add_assertion(...)` work when the analysis runs on JAX, so that a label-symmetry-breaking ordering (the Euclid two-basis MGE `|e_A|^2 > |e_B|^2`, euclid_strong_lens_modeling_pipeline#54, `docs/mge_label_degeneracy.md`) can be applied to a Nautilus search with `use_jax=True`.

Today (af 2026.8.17.1) assertions are enforced only by `check_assertions` raising `exc.FitException` inside `instance_for_arguments` (`autofit/mapper/prior_model/abstract.py:193-226, 1600-1628`), and `Fitness.call` (`autofit/non_linear/fitness.py:380-394`) catches that exception and returns `resample_figure_of_merit` only on the NumPy branch. Measured on 2026-09-08 with a real model:
- non-vmapped JAX `Fitness`: `FitException` propagates uncaught from `Fitness.call`, killing the run on the first violating sample;
- vmapped `Fitness`, which Nautilus builds by default (`use_jax_vmap=True`, `autofit/non_linear/search/nest/nautilus/search.py:116, 242-256`): `jax.errors.TracerBoolConversionError` at trace time for satisfying and violating vectors alike, because `check_assertions` does `not assertion.instance_for_arguments(...)` on a tracer. The model cannot compile at all.

Required behaviour: on the JAX branch of `Fitness.call`, build the instance with assertions ignored, evaluate every assertion as a traced boolean with the array module (`GreaterThanLessThanAssertion` / `GreaterThanLessThanEqualAssertion` / `CompoundAssertion` in `autofit/mapper/prior/arithmetic/assertion.py`; their `left_for_arguments` / `right_for_arguments` already evaluate compound priors arithmetically), combine them, and fold the result into the log likelihood with `xp.where(violated, resample_figure_of_merit, log_likelihood)`, the penalty-term shape `autofit/mapper/prior_model/constraint.py` anticipates. The NumPy branch keeps its exception-and-resample behaviour and its results byte-for-byte. `exception_override` and `ignore_assertions` semantics are unchanged. Gradient safety follows the existing contract in the `Fitness.call` docstring: the `where` is value-only, which is fine here because the likelihood is evaluated at a valid instance either way.

Constraints: no `import jax` in library unit tests (JAX path pinned by the workspace_test script); do not change `resample_figure_of_merit` defaults; do not touch `__model_constraint__` / ball constraints (separate mechanism); `take_attributes` / `assert_no_assertions` unchanged.

Out of scope (separate follow-ups already in ideas.md): the `mge_model_from` ordering option in PyAutoGalaxy and the Euclid pipeline edit + witness rerun.

<!-- filed 2026-09-08 by the mge-label-degeneracy research session (euclid pipeline#54) from the ideas.md bullet tagged "research mge-label-degeneracy · fitness.py:380"; that bullet is retired by this prompt -->

## traced-assertions-on-jax-path
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1581
- completed: 2026-09-08
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1583
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/100
- pending-release: PyAutoFit@https://github.com/PyAutoLabs/PyAutoFit/pull/1583
- heart-ack: 2026-09-08 in-session, same two organism-scope reasons as mge-label-degeneracy (autolens workspace validation failures; no release rehearsal)
- Summary: `model.add_assertion(...)` is now enforced on the JAX likelihood path. `AbstractPriorModel.gathered_assertions()` collects assertions across the model tree (including an assertion's own operand graph); `assertions_satisfied_for_arguments` / `assertions_satisfied_from_vector` evaluate them as a boolean array; `Fitness.call`'s JAX branch builds the instance with `ignore_assertions=True` and applies `xp.where(satisfied, figure_of_merit, resample_figure_of_merit)` to the FINAL figure of merit (after log-prior and chi-squared conversions, matching the NumPy early return). Gather and `exception_override` read happen once in `__init__` and are recomputed on unpickle. NumPy path unchanged, including the compound-assertion short-circuit (`xp is np`).
- Review: Codex CLI gpt-6-astra adversarial review; four defects (stale-pickle restore, sentinel before conversion, lost NumPy short-circuit, operand assertions dropped) each reproduced with a failing test then fixed (aefea1d54); witness script defect (jax imported before autofit → float32 → -1e99 sentinel overflowed to -inf in a plain shell) reproduced with `env -u JAX_ENABLE_X64` and fixed (0339180).
- Tests: `pytest test_autofit` 2533 passed, 2 skipped; new `test_fitness_assertions_jax.py` (importorskip) covers eager/jit/vmap, child-attached, conversions, boundaries, exception_override, legacy restore; witness `autofit_workspace_test/scripts/jax_assertions/assertions_traced.py` passes against the branch and fails against old main.
- Traps: `codex review` rejects `-m` and a prompt with `--base` (use `codex exec -s read-only`); autonerves enables x64 only if JAX_ENABLE_X64 is set before `import jax`, so the -1e99 sentinel overflows under float32 (pre-existing, filed in ideas.md).
- Next: Euclid pipeline ordering assertion + seed once released (ideas.md); `mge_model_from` ordering option.

## Original prompt

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

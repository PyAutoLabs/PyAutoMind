# Skip the likelihood for assertion-violating samples on the JAX path

Type: feature
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Witness: A model with an `add_assertion` between two priors, fitted with `af.Nautilus` on the JAX backend with a deliberately high violating fraction (an assertion satisfied by roughly half the prior volume, and a bound geometry prevented from learning it), performs measurably fewer `log_likelihood_function` evaluations than today - counted by an instrumented analysis that increments a counter per lane - while the returned figure of merit for every sample is bit-identical to the current implementation and to the numpy backend, and `test_fitness.py` still shows the two backends agreeing exactly on value.
Review-minutes: 25
Unattended: ready

# Skip the likelihood for assertion-violating samples on the JAX path

Type: feature
Difficulty: large
Autonomy: supervised
Priority: normal
Witness: A model with an `add_assertion` between two priors, fitted with `af.Nautilus` on the JAX backend with a deliberately high violating fraction (an assertion satisfied by roughly half the prior volume, and a bound geometry prevented from learning it), performs measurably fewer `log_likelihood_function` evaluations than today - counted by an instrumented analysis that increments a counter per lane - while the returned figure of merit for every sample is bit-identical to the current implementation and to the numpy backend, and `test_fitness.py` still shows the two backends agreeing exactly on value.

In PyAutoFit, a sample that violates an `add_assertion` costs a full likelihood evaluation on
the JAX backend and costs nothing on the numpy backend. The two backends agree on the *value*
they return, which is deliberate, but they differ by the entire cost of the analysis, which is
not. This prompt is about closing the cost gap without touching the value agreement.

## The asymmetry

`autofit/non_linear/fitness.py`, `Fitness.call`:

- numpy (`fitness.py:434-440`): `instance_from_vector` calls `check_assertions`
  (`autofit/mapper/prior_model/abstract.py:193-235`), which raises `exc.FitException`. The
  `except` returns `self.resample_figure_of_merit`. `analysis.log_likelihood_function` is
  **never reached** for a violating point.
- JAX (`fitness.py:416-432`): `instance_from_vector(..., ignore_assertions=True)` is followed
  by an unconditional `analysis.log_likelihood_function(instance)`. Only afterwards is the
  traced boolean from `assertions_satisfied_from_vector`
  (`abstract.py:300-351`) applied as `xp.where(assertions_satisfied, figure_of_merit,
  self.resample_figure_of_merit)` (`fitness.py:498-503`).

The docstring at `fitness.py:356-369` records that applying the assertion at the end is what
makes the two backends agree exactly on value. That reasoning is sound and should be preserved;
the cost consequence appears to be an accepted side effect rather than an intended one.

`_is_jax` (`fitness.py:341-349`) keys purely off `analysis._xp.__name__.startswith("jax")`, so
this branch runs whenever the analysis backend is JAX, including JAX pinned to the CPU backend.

## Why it cannot be dodged today

Nautilus is driven with `vectorized=fitness.use_jax_vmap` (default True) and `n_batch=100`
(`autofit/non_linear/search/nest/nautilus/search.py:329-354`), and the likelihood is
`jax.vmap(jax.jit(self.call))` (`fitness.py:838-857`). `vmap` compiles one program across all
lanes with no data-dependent branch, so a violating lane costs exactly the same FLOPs and wall
time as a satisfying one. `lax.cond` under `vmap` degrades to a select that evaluates both
branches, so it is not a fix either.

The sampler does not help: `nautilus/sampler.py` `evaluate_likelihood` increments `n_like` by
the full batch length unconditionally, and `add_bound`'s docstring states "The number of new
points added is always equal to the batch size". A violating point is stored with its penalty
figure of merit and simply fails to count toward the shell's quota. There is no
reject-and-redraw, and no short-circuit.

Note the penalty is not NaN and not `-inf`: Nautilus overrides `resample_figure_of_merit` to
`-1.0e99` (`search.py:216` and `:239`).

## Suggested approach

Evaluate the assertions on the raw parameter batch first - they are cheap prior-space
comparisons - then run the expensive likelihood only on the passing rows and scatter the
penalty back:

1. compute the boolean mask for the batch without building instances or touching the analysis;
2. gather the passing rows, padded to a static shape so `jit` still sees fixed shapes (pad to
   the batch size, or to a small set of bucket sizes to limit recompilation);
3. `vmap` the likelihood over the padded gather only;
4. scatter results back into the full-length output, writing `resample_figure_of_merit` into the
   violating positions.

The value contract must not move: every sample's returned figure of merit has to stay
bit-identical to today and to the numpy backend. Watch recompilation - a padding scheme with a
varying number of buckets can cost more in re-tracing than it saves, so the bucket count wants
measuring rather than assuming.

## How much is actually on the table

Measured on a real ten-lens run (`af.Nautilus`, `n_live=750`, JAX CPU, an assertion ordering two
MGE bases that admits half the prior volume): the constrained fit used 564,200 samples against
546,100 unconstrained, a ratio of 1.03x. So in that case the waste is only a few percent,
because Nautilus's bound geometry learns the half-space within the first few shells and stops
proposing violating points.

The case worth fixing is the one where the violating fraction does **not** decay - many
assertions, or a constraint whose geometry the bounds cannot learn. There the tax is unbounded
and invisible, because the numpy backend does the right thing and only JAX users pay it. This
prompt should be judged on that case, not on the 3% one, and the witness above is written
accordingly.

## Out of scope

Folding a joint constraint into the prior transform so the sampled volume shrinks by
construction - an order-statistics reparameterisation of two ordered priors. That is a larger
and separate piece of work: `autofit/mapper/prior/vectorized.py` `PriorVectorized` implements
only marginal per-dimension unit-cube transforms and has no concept of a joint constraint
between two priors. `autofit/non_linear/clipper.py`'s `ClipperPriorBoxJoint` is a real
pre-evaluation projection but is explicitly scoped to the gradient searches and is not wired to
any nested sampler.

<!-- formalised by the Intake (Conception) Agent on 2026-09-09 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/99cc7b63-471e-41d6-8867-5fced69005fd/scratchpad/intake_assert.md -->

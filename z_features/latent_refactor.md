# Latent variables — first-class library API across PyAutoLens + PyAutoGalaxy

This is the parent epic for promoting latent-variable handling from ad-hoc per-script subclasses (see `euclid_strong_lens_modeling_pipeline/util.py:306-332` and the workspace `scripts/guides/results/workflow/*_make.py` files) into a proper library API in PyAutoLens and PyAutoGalaxy.

## Original prompt

In euclid_lens_modeling_pipeline, but also autolens_workspace, we have started to build up quite a lot of calculations
in compute_latent_variables, and many now have different behaviour depending on if we are using JAX, numpy and
other variants.

Furthermore, these are hard coded into the code and users have to change python code, commenting stuff out, in order
to disable or enable certain latent variables. The interface in general is not very user-facing and its not
a clear and concise API for users to interface with the latent variable API.

First, the calculations should move to dedicated library modules. Per the user clarification: latent code lives
**with the model API stuff** — i.e. `autolens/analysis/latent.py` and `autolens/imaging/model/latent.py` (mirroring
where `Analysis` and `AnalysisImaging` live), not a top-level `autolens/latent.py`. This will also ensure
we have documentation on each variable and some much-needed unit tests can be added. We should avoid where possible
the actual calculations being done here — we don't want lensing primitives to be stuck in a latent variable module
(delegate to existing helpers like `LensCalc.einstein_radius_jit_from()` at
`PyAutoGalaxy/autogalaxy/operate/lens_calc.py:1520`).

These should all be paired with a config file, `config/latent.yaml`, which allows users to turn latents on and off
via bools so `compute_latent_variables` doesn't waste compute on disabled ones. Per exploration: PyAutoFit's
`LATENT_KEYS` mechanism is purely class-level (no autoconf integration — `autofit/non_linear/analysis/analysis.py:34`,
positional zip with vmap output at line 285). The config-driven on/off lives entirely in the
PyAutoGalaxy/PyAutoLens `Analysis` subclass, which reads the yaml and filters BOTH `LATENT_KEYS` and the
`compute_latent_variables` return dict. No PyAutoFit core changes needed.

This work should be done on PyAutoLens and PyAutoGalaxy so both have this first-class latent variable API.

Create autolens and autogalaxy workspace examples explaining what latent variables are (good descriptions already in
autofit_workspace — expand where context is missing), what their errors and whatnot correspond to, explain posterior
draws. Workspace examples, probably borrowing from results, show how to load and use latent variables — this can
be a section at the end of the above workspace example rather than its own tutorials. Make it clear that adding
latents to the modeling enables this loading and inspection thereafter.

Workspace example also includes a section showing users how to extend Analysis objects with their own latent
variables, by inheriting the Analysis and overwriting the LATENT_KEYS and `compute_latent_variables` method. Encourage
them to submit source-code extensions for all users.

Add a smoke test in autolens_workspace_test which runs often in claude (a high-class smoke test) that does a proper
run on all latent variables to ensure the functionality works — use just one draw, this may benefit from using
PYAUTO_TEST_MODE to do it in an efficient but representative way.

In autolens_profiling add a package `latent/` which does runtime profiling on the output of all the variables
and produces a README.md in the style of `autolens_profiling/likelihood_runtime/` (sweep.py + aggregate.py +
README.md).

Finally: is there some fancy or complicated math we should do when the priors or distributions of parameters to
latent variables get a bit complicated? e.g. mapping a uniform thing to a log10 thing?

## Sub-prompts (sequenced)

1. [autogalaxy/latent_module.md](../autogalaxy/latent_module.md) — library spine in PyAutoGalaxy. **Dependency root — start here.**
2. [autolens/latent_module.md](../autolens/latent_module.md) — library spine in PyAutoLens. Depends on #1.
3. [euclid_strong_lens_modeling_pipeline/latent_migration.md](../euclid_strong_lens_modeling_pipeline/latent_migration.md) — migrate the euclid pipeline to use library latents. Depends on #1, #2.
4. [autofit_workspace/latent_variables_tutorial_expand.md](../autofit_workspace/latent_variables_tutorial_expand.md) — expand autofit-level latent docs so workspace tutorials can link to them.
5. [autogalaxy_workspace/latent_variables_tutorial.md](../autogalaxy_workspace/latent_variables_tutorial.md) — workspace tutorial. Depends on #1, #4.
6. [autolens_workspace/latent_variables_tutorial.md](../autolens_workspace/latent_variables_tutorial.md) — workspace tutorial. Depends on #2, #4.
7. [autolens_workspace_test/latent_smoke_test.md](../autolens_workspace_test/latent_smoke_test.md) — smoke test covering all library latents. Depends on #2.
8. [autolens_profiling/latent_profiling.md](../autolens_profiling/latent_profiling.md) — runtime profiling package. Depends on #2.
9. [autolens/latent_prior_mapping_math.md](../autolens/latent_prior_mapping_math.md) — research stub: prior→latent transforms (uniform → log10, etc.).

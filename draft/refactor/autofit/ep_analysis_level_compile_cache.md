# EP: cache the compiled JAX likelihood on the Analysis across factor steps

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
Themes:
- graphical-ep
- jax
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: an EP run over N AnalysisFactors with a JAX likelihood logs "JAX jit compiling vectorized (vmap) likelihood function" N times in total across M factor steps (once per analysis), not N*M times; the per-factor compile is paid on step 1 only and the per-step wall-clock drops by the compile cost from step 2 on.
Review-minutes: 3
Unattended: ready
Filed: 2026-09-17

Follow-up split out of PyAutoFit#1631 (release each EP factor search's internals
so JAX executables are collectable). That fix bounds memory to one factor
search's executables; it does not stop the recompile.

Every EP factor step builds a fresh `Fitness` for the same `Analysis`
(`autofit/non_linear/search/nest/nautilus/search.py`, the `Fitness(...)` in
the `force_x1_cpu or analysis._use_jax` branch), and `Fitness._vmap` /
`_jit` / `_grad` are per-instance `cached_property` compile caches
(`autofit/non_linear/fitness.py`). So slope_hierarchy_scale job 342410 logged
76 compiles for 25 analyses over ~3 steps: one compile per factor search, each
about 2-3 s of an ~8 min search.

Proposal: cache the compiled callables on the `Analysis` (or a small
per-analysis registry the `Fitness` consults) keyed by the compile-affecting
statics: `use_jax_vmap`, `fom_is_log_likelihood`, `convert_to_chi_squared`,
`resample_figure_of_merit`, `log_likelihood_ceiling`, the traced assertions
and the ordered prior-id tuple of the model. Invalidate for analyses that read
the EP cavity (an `EPAnalysisFactor`-style analysis whose likelihood closes
over per-step state). Prove it with a test that counts compiles over two
`optimise` calls on one `AnalysisFactor` (mock the compile path, assert one
compile) and with the same 5-factor JAX witness script used on #1631.

Keep the #1631 release in place: the cache must hold the compiled callable,
never the `Fitness` or the sampler, or the retention chain returns.

# imaging/start_here: 26-minute XLA compile of the 48-start Prodigy multi-start on CPU

Type: bug
Target: autolens_workspace
Repos:
- autolens_workspace
- PyAutoFit
Themes:
- jax
- compile-time
- first-contact
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: draft
Consequence: judge
Witness: under the release profile (full FITS, fp64, JAX on) `scripts/imaging/start_here.py` compiles the multi-start objective in well under 5 min on the CI CPU runner across 5 consecutive release-integrate runs (max wall < 900 s), with the same max-log-likelihood model recovered; the script's "under ten minutes on a CPU" promise (line ~344) is true
Review-minutes: 20
Filed: 2026-09-14

User request (verbatim, 2026-09-14):

"""
can you fix the PyAutoHeart being red
"""
(filed by intake after the release-validation diagnosis; no development started.)

## Context

Release-integrate timing history for the script over 09-09..09-14: 1805/1147/735/586/1805/1695/749/1805 s
(3 kills at the 1800 s cap); siblings in the same leg stable within ±30%. Kill traceback (identical each time):

    slow_operation_alarm.cc: The operation took 26m27s  [Compiling module jit_call for CPU] Very slow compile?
    autofit/non_linear/search/mle/multi_start_gradient/search.py  _broad_starts -> _fit
    jax/_src/compiler.py backend_compile_and_load

Script: `af.MultiStartProdigy(n_starts=48, batch_size=None, n_steps=300, iterations_per_quick_update=50,
live_visual_update=True)` with `al.AnalysisImaging(use_jax=True)` and over-sampling `sub_size_list=[4,2,2]`,
`radial_list=[0.3,0.6]` (line ~177). `batch_size=None` vmaps all 48 starts into one XLA module; a non-uniform
over-sample map is known to multiply jit compile time (PyAutoLens #523 -> #534 memo). Compile time is bimodal
on the same code, so it also depends on runner/XLA state.

## Candidate levers (evaluate, pick one, measure)

1. Explicit `batch_size` (8 or 12) so XLA compiles a small module a few times instead of one 48-wide module.
2. Uniform over-sampling for the compile path, or a smaller `sub_size_list`, if the science figures survive.
3. In PyAutoFit: a default `batch_size` cap in `MultiStartProdigy` when the objective is a large vmapped graph,
   or a persistent JAX compilation cache in the release-integrate job.
Measure compile + total wall for each under the release profile locally and on CI; keep the tutorial prose
honest about runtime.

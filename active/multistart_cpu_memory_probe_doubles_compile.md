# MultiStartGradient's unbatched-memory guard pays two throwaway full-model XLA compiles on CPU

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: high
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1646
Status: formalised
Consequence: glance
Witness: a unit test in test_autofit/non_linear/search/mle/test_multi_start_gradient.py shows that on the CPU JAX backend `_warn_if_unbatched_exceeds_memory` never calls `analysis.batched_memory_bytes` (red on unfixed main), while with `jax.default_backend` monkeypatched to "gpu" the probe is still called.

## Request (verbatim)

Nightly release Stage 3 (PyAutoHeart release-integrate run 36226772178) TIMEOUT on autolens_workspace scripts/imaging/start_here.py at 3605s (prior nights 704-770s). Cause: `MultiStartGradient._warn_if_unbatched_exceeds_memory` (PyAutoFit `autofit/non_linear/search/mle/multi_start_gradient/search.py` ~line 815, called at ~1080 when batch_size is None) calls `analysis.batched_memory_bytes` (autofit/non_linear/analysis/analysis.py:338) at batch 1 and 2, each a full throwaway XLA compile of jit(vmap(value_and_grad(fitness.call))). Its docstring assumes memory_analysis returns 0 on CPU so it would bail; on jax 0.10.2 CPU it is non-zero, so both compiles run, then budget from psutil. One drew the slow bimodal compile (~54 min).

## Fix

Return early before any probe compile when `jax.default_backend() == "cpu"`; check `_memory_budget_bytes()` before the probes; rewrite the docstring's "Known limitation" paragraph citing run 36226772178. Keep the 3600 s BUILD_SCRIPT_TIMEOUT override in autolens_workspace for now.

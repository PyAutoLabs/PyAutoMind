## multistart-cpu-memory-probe
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1646 (closed, completed 2026-09-26)
- completed: 2026-09-26
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1647 (MERGED, head `3220566e`, merge `326f611b1b40afd89bb73956441faa7379328407`; CI green on all legs, no Heart freeze)
- heart-ack: "2026-09-26 human acked YELLOW: workspace validation 4 failed cluster/weak notebooks; manifest drift x3; release validation stale"
- Consequence: glance — no tier-`notify` shadow row
- summary:
  - `MultiStartGradient._warn_if_unbatched_exceeds_memory` now skips its batch-1/batch-2 memory probe (two throwaway full-model XLA compiles) on the CPU JAX backend, and checks the memory budget before probing.
  - The probe caused the 2026-09-26 release-integrate `imaging/start_here.py` 3605 s TIMEOUT (run 36226772178).
  - 3 new tests (red then green); 139 mle tests pass.
  - Follow-up to watch: the next nightly Stage 3 `start_here.py` should return near ~700 s; the 3600 s `BUILD_SCRIPT_TIMEOUT` override in `autolens_workspace/config/build/profile_release.yaml` can be retired once runs are consistently fast.

## Original prompt

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

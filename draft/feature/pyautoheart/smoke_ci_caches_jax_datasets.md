# CI caches in the reusable smoke workflow: JAX compile cache + dataset builds

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoNerves
Difficulty: large
Autonomy: safe
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: ci-timing-fast-tests
Phase: 7

CI caches in the reusable smoke workflow: persist the JAX compile cache and dataset builds across runs.

`autonerves/jax_wrapper.py:98-125` already auto-writes a persistent JAX compilation cache
to `~/.cache/pyauto_jax` (JAX_PERSISTENT_CACHE_MIN_COMPILE_TIME_SECS=1), and the closed
jax-compile-time arc certified the cache at both scales (51x local, 5.9x A100 end-to-end).
But `PyAutoHeart/.github/workflows/smoke-tests.yml` — the one reusable workflow every
workspace/_test/HowTo smoke gate calls — has NO actions/cache step: the cache helps within
one job (scripts are subprocesses) and is discarded between runs.

1) Add an `actions/cache` step for `~/.cache/pyauto_jax`, keyed on jaxlib version + python
matrix leg (+ a manual epoch salt for invalidation). Expected: removes the 12-18s+ compile
from every `ENV: jax` script on cache-hit runs — plausibly 30-50% off the jax_likelihood
wall total. Traced-code changes miss the cache naturally, which is correct. (Run
33078033016 already refuted any interaction between the cache and the Eigen-pool hang.)

2) Same mechanism for simulated dataset builds: `should_simulate` auto-simulation persists
datasets locally but CI runners start clean, so each job re-simulates each dataset family
(~10-20s incl. import per family). Cache the dataset build trees keyed on a hash of the
simulator scripts so any simulator edit invalidates.

3) Measure honestly: compare cache-hit vs cache-miss gate wall-clock on the phase-1/2
timing surface, and confirm cache restore/save overhead doesn't eat the win for the small
repos (autocti: 3 entries).

## blackjax-nuts-search
- issue: https://github.com/rhayes777/PyAutoFit/issues/1255
- completed: 2026-05-06
- library-pr: https://github.com/rhayes777/PyAutoFit/pull/1256
- workspace-prs:
  - https://github.com/PyAutoLabs/autofit_workspace/pull/52 (mcmc.py extended)
  - https://github.com/PyAutoLabs/autofit_workspace_test/pull/23 (BlackJAXNUTS.py integration test)
- repos: PyAutoFit, autofit_workspace, autofit_workspace_test
- notes: Added `af.BlackJAXNUTS` as a first-class non-linear search alongside Emcee/Zeus/Nautilus/etc. Lives under `autofit/non_linear/search/mcmc/blackjax/nuts/search.py` so the `blackjax/` namespace can hold future BlackJAX samplers (HMC, MALA). Inherits `AbstractMCMC`, runs `blackjax.window_adaptation` warmup followed by NUTS sampling in a JIT'd `jax.lax.scan`, chunked by `iterations_per_full_update` for periodic `perform_update` flushes. Strict requirement: `Analysis(use_jax=True)` — clear error otherwise. Sampling in physical parameter space; bounded priors contribute -inf outside support. Single-chain v1 (`num_chains>1` raises `NotImplementedError`); resume stubbed for later. AutoCorrelations populated from BlackJAX per-param ESS via τ_int = N / ESS (canonical identity). Persistence via pickle under `search_internal/`. Target log-density built from `Fitness.call` directly (pure-JAX path; `call_wrap`/`__call__` were intentionally bypassed because they convert to Python float and would break NUTS gradients). `blackjax>=1.2.0` added to `optional-dependencies.optional` (lazy import in `_fit`). 7 unit tests + integration test on the 1D Gaussian (recovers truth within 0.05σ, ESS ~50% of num_samples, 0 divergences).

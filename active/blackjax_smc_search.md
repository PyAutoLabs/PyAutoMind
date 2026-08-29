# af.SMC: blackjax adaptive tempered SMC search

Type: feature
Target: PyAutoFit
Autonomy: human-required
Issued: 2026-08-29

## Problem

The JAX-native posterior sampler wave validated a gradient SMC prototype on the
`autolens_workspace_developer` branch `feature/blackjax-smc-gradient-kernel`
(`searches_minimal/blackjax_smc_grad.py`, `_warm_start.py`,
`smc_gradient_findings.md`). Warm-started, it samples: acceptance 0.80 → 0.17
across the tempering path, `einstein_radius` 1.5998 against a truth of 1.6, and
all three warm arms' log Z bracket the Nautilus bar within ±0.8 nats — a
gradient sampler that *also* yields the evidence.

That prototype lives in a workspace script. It has to become a first-class
PyAutoFit search (`af.SMC`) before the profiling workspace can build an SMC cell
and put SMC runs on the A100.

## Scope

- `autofit/non_linear/search/mcmc/blackjax/smc/{__init__.py,search.py,samples.py}`
  — `class SMC(AbstractMCMC)` around `blackjax.adaptive_tempered_smc`, inner
  kernel `mala` (default) or `hmc`, templated on the sibling
  `blackjax/nuts/search.py` and reusing `blackjax/chains.py`.
- Whitening from a warm start: full-covariance Cholesky via
  `InverseMassMatrixSpec` + `chains.resolve_inverse_mass_matrix`; step scaled to
  the **posterior** width, MALA's squared-length units honoured. No kernel
  adaptation in this wave (`--tune` collapses acceptance, phase-0 finding).
- Warm start sets particle positions and the whitening, but tempering still
  starts at λ=0 — from a **normalised** Gaussian reference, bridged as
  `logprior_fn := log g`, `loglikelihood_fn := log prior + log L - log g`, so
  log Z stays the true evidence.
- Likelihood through `Fitness.call`. λ schedule, per-step acceptance and ESS
  recorded in `search_internal`; `log_evidence` from the tempering bridge.
- `af.SMC` exported lazily via `_LAZY_ATTRS`; `apply_test_mode`; docs
  autosummary entry; release-notes new-feature entry.
- Tests: `test_autofit/non_linear/search/mcmc/test_blackjax_smc.py` — Gaussian
  target log Z within 0.1 nat of analytic, warm and cold both run, test mode.

## Original request

> do the 5 things above listed and make sure we have some SMC runs going soon

(This is rung 2 of that five-rung wave: the `af.SMC` library half; the profiling
SMC cell and the A100 probe follow in Wave B.)

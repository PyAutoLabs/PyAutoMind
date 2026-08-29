## blackjax-smc-search
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1544
- completed: 2026-08-29
- library-pr: PyAutoFit#1546 (merged b70cf7fc3 -> main)
- what shipped: `af.SMC` (lazy `_LAZY_ATTRS`) — `blackjax.adaptive_tempered_smc`, inner kernel `mala` (default) or `hmc`, `num_particles=256`, `num_mcmc_steps=5`, `target_ess=0.5`, `step_size` scaled to posterior width, `whiten_inflate=2.0`, no step adaptation by default (phase-0: `--tune` collapses acceptance), full-covariance whitening from a warm-start `Result`/`Samples` via `inverse_mass_matrix` (the "diagonal"/"dense" strings are REJECTED — they name an adaptation SMC doesn't have), default initializer `InitializerPrior` (cold evidence needs prior-drawn particles; the AbstractMCMC ball default would void it); warm start = bridge + Jacobian, λ still starts at 0. `SamplesSMC(SamplesPDF)` with `log_evidence`, `lambda_list`, `acceptance_rate_list`, `ess_list`, `converged`. `__identifier_fields__` = num_particles, kernel, num_mcmc_steps, num_integration_steps, target_ess, inverse_mass_matrix. Ported from wsdev branch `feature/blackjax-smc-gradient-kernel`.
- validation: analytic isotropic Gaussian under Uniform(-5,5), logZ=−2.7673, 1000 particles: cold −0.082 / warm −0.020 / hmc +0.014 nat (HMC holds acceptance 0.96 where MALA decays 0.80→0.24); 31 new tests; full suite 2336 passed / 3 skipped; sphinx 31 warnings = baseline (fixed an `|r|` RST substitution error); CI 4/4.
- notes: no YAML config — PyAutoFit#1202 removed that layout; defaults are explicit Python args. Release notes = PR "API Changes" section.
- heart-ack: shipped + merged under human-authorised YELLOW ("merge", 2026-08-29) — same two reasons as fitness-log-likelihood-ceiling, unrelated.
- follow-up: autolens_profiling Wave B — `build_smc` + `searches/smc/mge.py` leaf + A100 warm probe (PROGRAMME Phase 7 / Gate D).

## Original prompt

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

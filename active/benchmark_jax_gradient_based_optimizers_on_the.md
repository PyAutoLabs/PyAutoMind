# Benchmark JAX gradient-based optimizers on the MGE lens likelihood

Type: experiment
Target: workspaces
Repos:
- autolens_workspace_developer
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> We have a dedicated agent for implementing non-linear searches in PyAutoBrain
> (the samplers / `sampler_pipeline`). Use it to fit some JAX gradient-based
> optimizations or maximum-likelihood estimators, using the autolens
> Multi-Gaussian Expansion (MGE) lens-light and source examples in the autolens
> developer workspace. Implement them via the searches **minimal API** (NOT in
> PyAutoFit source code). Try different ones and find if there's one that gives
> robust results whilst simultaneously running really fast; give statistics on
> the run times. Also read papers that use e.g. Herculens for good examples of
> JAX gradient-based optimization for strong lens modelling —
> paper: https://arxiv.org/abs/2606.30620 (Enzi et al. 2026) and references therein.

## Scope

Workspace-only prototyping in `autolens_workspace_developer/searches_minimal/`,
plugging JAX gradient-based optimizers directly into the existing MGE
`AnalysisImaging(use_jax=True)` likelihood via `jax.value_and_grad` — no
`NonLinearSearch` subclass, no PyAutoFit source changes. The MGE lens+source
problem already exists as the standard benchmark here (`_setup.py`: 20-Gaussian
MGE bulge + Isothermal + ExternalShear lens, 20-Gaussian MGE source, ~50 free
params, HST imaging). The `use_jax=True` likelihood is proven end-to-end
`jax.grad`-differentiable (`jax_profiling/gradient/imaging/mge.py`).

## Candidates (all cold-start: prior median / `init_to_median`)

| # | Candidate | Rationale | Kind |
|---|-----------|-----------|------|
| 1 | optax **Adam** | Herculens' actual optimizer / baseline | 1st-order MLE |
| 2 | optax **ADABelief** | Enzi et al. 2026's optimizer | 1st-order MLE |
| 3 | jaxopt **L-BFGS** | quasi-Newton, *true* `jax.grad` (vs existing scipy finite-diff `lbfgs_simple`) | quasi-Newton MLE |
| 4 | numpyro **SVI** | paper-faithful: ADABelief on mean-field Gaussian ELBO, `init_to_median`; yields a variational posterior | variational inference |
| 5 | jaxopt **Levenberg-Marquardt** ⭐ | wildcard — chi-squared is nonlinear least-squares; LM interpolates gradient-descent↔Gauss-Newton via the residual Jacobian; textbook robust-and-fast for this shape | Gauss-Newton |

Decisions taken with the user: **drop the warm-start / chaining axis** (test
robustness from a cold start only); **include SVI** as the paper's real method;
LM is the deep-research wildcard.

## Metrics / deliverable

Honour `_metrics.MLTracker` (evals-to-ML, time-to-ML). Per candidate record:
JIT/compile time, forward vs forward+grad ms/eval, iterations to plateau,
wall time, final max log L, and **robustness** = distance of the recovered
log L to the simulator-truth log L. Add rows to
`searches_minimal/output/comparison.txt` + per-script summaries, and a short
findings writeup (runtime-stats table). Record durable findings in
`PyAutoMemory/methods_wiki/concepts/sampler-benchmarks.md`.

## Budget / run location

Default: **laptop CPU, modest step budgets** — honest runtime characterization
(compile, ms/eval, time-to-converge) + extrapolation, 1–2 seeds cold-start;
not a converged multi-seed robustness proof. NOTE: the MGE grad-path JIT
compile is slow (~minutes; the full-SMC `nss_grad` took ~20 min) and each
fwd+grad eval ≈0.8 s on CPU (WSL2 GPU JAX unavailable). A converged multi-seed
robustness study is a follow-up for A100/HPC (`autolens_profiling`), aligning
with the faculty's real-likelihood promotion gate.

## Grounding

Enzi et al. 2026 (arXiv:2606.30620): source reconstruction in Herculens
(Galan+2022, JAX+NumPyro); inference via **Stochastic Variational Inference**
with the **ADABelief** optimizer, `init_to_median` + warm-start chaining;
they deliberately skip HMC. Herculens' primary optimizer is **Adam (optax)**.
jaxopt provides the LM/Gauss-Newton least-squares family.

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake -->

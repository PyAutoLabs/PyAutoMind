# Next-wave population gradient optimizers on the MGE lens likelihood

<!-- Scope: fast many-points OPTIMIZERS (MAP point estimates). Full Bayesian
     samplers (SMC/HMC/nested/flowMC/SVGD-as-VI) are a deferred later wave.
     Filename kept as ..._samplers_... (stable id); the work is optimizers. -->


Type: experiment
Target: workspaces
Repos:
- autolens_workspace_developer
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## The insight this builds on

Follow-up to `experiment/workspaces/benchmark_jax_gradient_based_optimizers_on_the.md`
(autolens_workspace_developer#95). That run established, on the HST MGE lens
likelihood, that **every single cold-start method fails the same way** —
optax Adam (r_E 4.89), ADABelief (5.01), jaxopt L-BFGS (4.42) and numpyro SVI
(3.54 ± 0.07, overconfident) all lock onto the WRONG basin (log L ≈ −158000),
while **12-start Adam (the GIGA-Lens recipe) recovers the truth** (r_E 1.600,
log L +31788; 2/12 starts hit the basin, ~17% each). The failure is *basin
selection*, not optimizer or speed — the JAX likelihood is ~170–230 ms/eval for
all of them.

The lesson: **the many-point / population principle is what buys robustness.**
It is precisely why gradient-free nested sampling (Nautilus/MultiNest) is the
workhorse for strong-lens modelling — its live-point population collectively
covers multiple basins (MultiNest even clusters them). Nested sampling pays for
that robustness in eval count (no gradients); GIGA-Lens gets the same robustness
with gradients (many starts) and so needs far fewer evals to the basin. The next
wave should **unify many-points robustness WITH gradient efficiency.**

## Selection constraints (from the user)

1. **Fast OPTIMIZERS, not full samplers — yet.** This wave stays in the
   point-estimate (MAP/MLE) regime that multi-start Adam won in. Methods that
   produce a *posterior* — tempered SMC, HMC/NUTS, nested sampling (jaxns,
   Nautilus), flowMC, and SVGD-run-as-variational-inference — are **DEFERRED to
   a later full-sampling wave**, once the robust *fast optimizer* is settled.
   (SMC/HMC are Bayesian samplers, not maximum-likelihood optimizers — they do
   not belong in this wave.)
2. **Open source, easy, JAX-native.** Favours reusing the existing multi-start
   harness (zero deps) and the installed JAX-native libs: `optax`, `jaxopt`,
   `evosax` (JAX-native evolutionary strategies), `blackjax`.

## Candidates (fast many-points OPTIMIZERS; searches_minimal, same MGE MAP objective + harness)

Theme: *smarter ways to spend many points to find the MAP fast and robustly* —
independent multi-start (done) → multi-start of better local rules → interacting
populations. Baseline to beat = **multi-start Adam** (r_E 1.600, 2/12 starts,
~1254 s end-to-end) on robustness (fraction of starts → truth) and wallclock.

| Candidate | Principle | Implementation (JAX-native, open source) |
|-----------|-----------|------------------------------------------|
| **Multi-start of other local optimizers** ★ | reuse the multi-start harness with L-BFGS, ADABelief, Lion, and **Levenberg-Marquardt / Gauss-Newton** — does the local rule matter within multi-start? multi-start LM = the high-value form of the deferred single-start wildcard | `optax` + `jaxopt` (installed), **zero new deps**; reuse `multi_start_adam.py` |
| **CMA-ES** ★ | *interacting* population optimizer — adapts a covariance from the population each generation; the classic robust global optimizer. Tests whether a smart ES matches multi-start gradient descent, and whether the gradient even helps vs. a good ES | `evosax` (JAX-native, **installed**); also PSO / Differential Evolution from evosax |
| **SVGD as a mode-finder** | many particles + gradient + kernel **repulsion**, take the **best particle** as the point estimate — "interacting multi-start" that uses gradients AND particle interaction | `blackjax.svgd` (**installed**). Borderline VI — used here purely as an optimizer, not for the posterior |

★ = start here (zero / installed deps, easiest).

**Deferred to the later full-sampling wave (do NOT build in this one):** tempered
SMC + HMC, flowMC, jaxns, SVGD-as-posterior, and a converged nested-sampling
posterior baseline. Those answer "what is the posterior?"; this wave answers
"what is the robust MAP, fastest?".

## Deliverable

End-to-end **wallclock** and **number of likelihood-evals** (overheads included
— JIT compile vs per-eval vs eval-count) for each optimizer, plus the
**robustness** metric that actually matters here: **fraction of starts/particles
that reach the true basin** (r_E ≈ 1.6) and time-to-first-basin-hit. All against
the **multi-start Adam** baseline. Report which reach the truth and at what cost;
extend `output/comparison.txt` + the findings writeup. Record durable findings in
`PyAutoMemory/methods_wiki/concepts/sampler-benchmarks.md`.

_(The converged nested-sampling / Nautilus wallclock-and-samples comparison
belongs to the later full-sampling wave — it is a posterior baseline, not a fast
optimizer.)_

## Grounding

GIGA-Lens (Gu/Huang et al. 2022; 2.0 = arXiv:2606.30633, up to 512 A100s),
Herculens / Enzi et al. 2026 (arXiv:2606.30620), flowMC (Gabrié et al. 2022),
pocoMC / Preconditioned Monte Carlo (Karamanis et al.), SVGD (Liu & Wang 2016),
Branching SVGD (arXiv:2506.13916), gradient-guided nested sampling
(arXiv:2312.03911). Scale note: population methods parallelise across particles,
so this is where GPU/multi-GPU (GIGA-Lens 2.0) pays off — plan the converged
runs for the A100/HPC path (`autolens_profiling`).

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake -->

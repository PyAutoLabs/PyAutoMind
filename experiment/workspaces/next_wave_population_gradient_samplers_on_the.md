# Next-wave population gradient samplers on the MGE lens likelihood

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

## Candidates (prototype in searches_minimal, same MGE likelihood + harness)

| Candidate | Principle | Notes |
|-----------|-----------|-------|
| **SVGD** (Stein Variational Gradient Descent) | N particles + gradient + kernel **repulsion** → deterministic particle VI, mode-covering | the direct "interacting multi-start"; Liu & Wang 2016. Add **Branching SVGD** (arXiv:2506.13916) for multimodality |
| **flowMC** (Gabrié et al.) | ensemble of gradient (MALA/HMC) local chains + a learned **normalizing-flow** global proposal | JAX-native; proven on gravitational waves (`jim`). Population + gradients + learned global structure |
| **gradient-guided nested sampling** | nested-sampling live-point population + **gradient-informed** proposals | arXiv:2312.03911 — the literal synthesis of the insight (nested sampling's robustness + gradients) |
| **SMC + HMC** | population of particles annealed with **gradient (HMC)** moves | extend the existing `blackjax_smc.py`; pocoMC (Karamanis) = SMC + normalizing-flow preconditioning (existing `pocomc_simple.py`) |

Reference/contrast: **multi-start Adam** (this run's winner) and a **converged
Nautilus** (see below).

## Deliverable

End-to-end **wallclock** and **number of samples/likelihood-evals** (overheads
included — JIT compile vs per-eval vs eval-count) for each candidate, versus
multi-start Adam and a **converged Nautilus** run (the existing Nautilus rows are
smoke configs, ~100 evals, non-converged — a real converged run, est. ~10–50k
evals / ~1 h on the JAX path, is needed for the apples-to-apples comparison the
insight demands). Report which reach the true basin and at what cost. Record
durable findings in `PyAutoMemory/methods_wiki/concepts/sampler-benchmarks.md`.

## Grounding

GIGA-Lens (Gu/Huang et al. 2022; 2.0 = arXiv:2606.30633, up to 512 A100s),
Herculens / Enzi et al. 2026 (arXiv:2606.30620), flowMC (Gabrié et al. 2022),
pocoMC / Preconditioned Monte Carlo (Karamanis et al.), SVGD (Liu & Wang 2016),
Branching SVGD (arXiv:2506.13916), gradient-guided nested sampling
(arXiv:2312.03911). Scale note: population methods parallelise across particles,
so this is where GPU/multi-GPU (GIGA-Lens 2.0) pays off — plan the converged
runs for the A100/HPC path (`autolens_profiling`).

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake -->

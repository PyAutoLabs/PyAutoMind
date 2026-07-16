# Learning-rate-free multi-start gradient optimizers on the pixelized likelihood

Type: experiment
Target: autolens_workspace_developer
Repos:
- autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Experiment: benchmark learning-rate-free multi-start gradient optimizers on the pixelized likelihood. Research question: do optax.contrib learning-rate-free optimizers (prodigy, dadapt_adamw, dog/dowg, mechanize, momo_adam, schedule_free_adamw; plus ADOPT/AdEMAMix as cheap extras) recover the mass basin on the pixelized-source likelihood where fixed-lr Adam went 0/16 (autolens_workspace_developer#100 — lr=1e-2 mis-scaling is a prime suspect; kernel-CDF mesh gradients certified FD ~1e-6, gradient correctness settled)? Benchmark inside the existing multi-start harness in @autolens_workspace_developer searches_minimal/ (_grad_setup.py; af.AbstractMultiStartGradient accepts any optax GradientTransformation, so each candidate is a one-line builder). Secondary: confirm on the MGE cell that the local update rule still barely matters within multi-start. Also adopt optax.apply_if_finite as the principled NaN-step guard (replaces argmin-over-finite bookkeeping for the ell_comps/shear singularity re-entry). Local CPU smoke first, then A100 on RAL (euclid_jump pipeline, batch_size lax.map tiling per Fit#1374). Deliverable: findings doc extending the phase-3 series.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from user-intake -->

# Learning-rate-free multi-start optimizers

- Issue: autolens_workspace_developer#101 (closed) · PR #103 (merged 2026-07-17, after #102)
- Branch: feature/lr-free-multi-start-optimizers (stacked on #100's)

MGE (12x300, 10 rules): every rule basin-hits; Prodigy (lr-free) bit-identical to hand-tuned
adam (+31787.84, r_E 1.5997) — the lr hyperparameter deletes at zero cost on parametric cells.
Pixelized: elimination chain (lr sweep, 10 rules, start bands incl. FD-certified narrow, fixed
reg) proved the #100 failure is trajectory NaN mortality — hard non-finite walls throughout
(even step 0: 2-3/16 NaN grads). Resurrection (redraw dead start + reinit per-start vmapped
optax state) converts the landscape to searchable: adam -51201 -> +1718 @ r_E 1.570 over 3000
steps, still improving — but converged Nautilus reaches +17419 in ~22 min warm, so the MGE
speed conclusion INVERTS on inversion-heavy cells. Promotion spec (drafted,
draft/feature/autofit/multistart_resurrection_and_contrib_rules.md): optax.contrib lookup +
per-start vmapped state (stacked state couples lr-free global scalars) + restart-on-death
(apply_if_finite latches at the cliff). Highest-leverage follow-up (drafted,
draft/bug/autoarray/pixelized_likelihood_nonfinite_regions.md): localise the NaN with the
preserved death-point coordinates. Deliverables: searches_minimal/{lr_free_multistart,
pix_lr_free}.py, lr_free_findings.md, lr_free_results/.

## Original prompt

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

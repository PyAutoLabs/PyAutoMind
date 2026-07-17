# Localise and fix the pixelized likelihood's non-finite regions

Type: bug
Target: autoarray
Repos:
- @PyAutoArray
- @PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft

The #101 lr-free experiment proved by elimination (autolens_workspace_developer
issues #100/#101, jobs 330529-330598) that the pixelized-source likelihood
(kernel-CDF mesh, NNLS positive-only solve, free Isothermal+shear mass) has
**hard non-finite walls throughout the broad parameter space**: every gradient
trajectory from broad starts hits a NaN loss/grad within ~25-50 steps,
regardless of learning rate (1e-3..3e-2), update rule (adam + 9 optax.contrib
rules), start band (broad AND the FD-certified narrow U(0.4,0.6)), or fixing
the regularization coefficient. Even at step 0, 2-3 of 16 broad starts have
finite loss but NaN gradient. Deaths scatter across reg 1e-4..4e3 and
r_E 1.36..6.4 — no single runaway parameter.

Task: instrument the likelihood (jax.debug / stagewise probes) at recorded
death points (per-start death report in
`autolens_workspace_developer/searches_minimal/pix_lr_free.py`, log
`samp_pixdeath_free_330592.log` on RAL) to localise WHICH intermediate goes
non-finite (mesh weight map? curvature-matrix Cholesky NaN-resample — the
PyAutoArray#607-adjacent path? NNLS? tracing?), then decide per site: fix
(finite-safe formulation), guard with a finite penalty that preserves a useful
gradient, or document as genuinely-invalid model space. This is the old
sweep_findings "localise the NaN" follow-up, now with concrete death-point
coordinates to replay.

Leverage: helps every gradient consumer (multi-start MAP, HMC/NUTS, MCLMC,
SVGD) — higher value than any optimizer work on this landscape.

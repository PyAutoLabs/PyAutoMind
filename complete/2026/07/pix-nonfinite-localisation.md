## pix-nonfinite-localisation (phase 1 — LOCALISED)
- issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/104
- completed: 2026-07-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/105 (MERGED 2026-07-17T12:16:25Z)
- verdict: LOCALISED — one site, one bug; the prime suspect was wrong
- summary: |
    Phase 1 of the pixelized-likelihood non-finite walls that #100/#101 proved
    existed BY ELIMINATION but could not attribute. Diagnosis only, no library
    edits (the Brain Bug Agent's investigate-first verdict).

    THE SITE: AbstractInversion.log_det_regularization_matrix_term
    (autoarray/inversion/inversion/abstract.py:734-764) — the
    log(diag(cholesky(H))) of the REDUCED regularization matrix. First
    non-finite stage in BOTH the forward and backward walks; culprit parameter
    = the regularization coefficient. Evidence: RAL A100 jobs 330609/330611.

    EXONERATES the three other suspects, including the PRIME one:
      - abstract.py:719 curvature-reg cholesky (PyAutoArray#607-adjacent):
        FINITE at 1.6913e+04. F + H is better conditioned than bare H — only
        the regularization-only log-det breaks.
      - inversion_util.py:333-335 NNLS Jacobi 1/sqrt(diag): d in
        [3.16e-2, 1.39e4], no zero diagonal — kills the "structurally unmapped
        mesh pixel" theory inherited from knn-barycentric.
      - rectangular_kernel.py:123 weight-map normalise: mapping_matrix finite.

    BOTH death classes die at the SAME site — in-basin (r_E 1.2824, beside the
    Nautilus mode 1.31) and out-of-basin (r_E 5.9252). So the in/out-of-basin
    triage that motivated #104 does NOT split the fix: one bug, and no
    "penalty for genuinely-invalid space" verdict was needed.

    MECHANISM (confirmed structurally): constant.py:43-58 builds
    H = lam^2*L + 1e-8*I with L a graph Laplacian (PSD, exact constant null
    mode). The 1e-8 lift is ABSOLUTE, not scaled to lam, so eig_min is pinned
    at 1e-8 while eig_max ~ lam^2*degree => cond(H) ~ lam^2*1e8. Verified
    against the real library function: eig_min == 1e-8 across four decades; at
    lam=1e5 it goes numerically negative (-9.9e-6) -> numpy RAISES where JAX
    returns NaN silently (abstract.py:762 already documents the asymmetry).

    TWO THREADS LEFT EXPLICITLY OPEN (not dropped):
      1. The synthetic clean grid only fails at lam >= 3e4, but the real fit
         died at lam ~ 6.9e3. A numpy-vs-JAX divergence is RULED OUT (tested —
         they agree exactly), so the real REDUCED matrix is worse-conditioned
         than a regular grid. Phase 2 must dump its spectrum before choosing a
         fix. Candidates: the 20 unregularized MGE amplitudes in the 920x920
         reduction; isolated/disconnected mesh pixels adding null modes;
         unique_indices=True in the scatter at constant.py:55-58.
      2. The #101 finite-loss/NaN-grad class is NOT reproduced — 90 seed-0
         draws gave only non-finite-loss rejects (draws 12 and 35).

    SECOND BUG FOUND (separate repo, arguably higher leverage):
    autofit/non_linear/fitness.py:239-240 guards with
    xp.where(xp.isnan(ll), resample, ll). It repairs the VALUE (rejects report
    loss=inf, not nan — the guard fires) but reverse-mode AD differentiates the
    masked branch: 0 * NaN = NaN. THE RESAMPLE GUARD DOES NOT PROTECT GRADIENT
    CONSUMERS AT ALL — every jax.grad consumer of every likelihood, not just
    pixelized. Retroactively explains #101's silent deaths and apply_if_finite
    latching at the cliff (#100's -39888).

    Shipped: searches_minimal/probe_nonfinite_pix.py (stagewise probe, forward
    AND backward walks) + searches_minimal/pix_nonfinite_findings.md.

    TRAPS (durable):
      - Will NOT run locally: one point's value_and_grad needs 10.90 GiB; a
        15GB/6GB-VRAM laptop OOMs on CPU (killed at 9.3GB RSS) AND GPU. A100:
        261-306 s (probe_nonfinite.sbatch, --partition=gpu --mem=64gb).
      - The recorded death points reproduce NOTHING: pix_lr_free.py:206-208
        stores LAST-FINITE params, which evaluate finite by construction. Use
        the seed-0 rejected draws that pix_lr_free.py:124-130 silently discards.
      - A forward-only probe is useless for the step-0 deaths (finite value,
        NaN gradient) — the backward walk is what localises them.
      - autoarray wrappers need .array before jnp.sum under a tracer, else
        TracerArrayConversionError.

    Follow-ups filed as DRAFTS (not issued — no bulk-issuing):
    draft/bug/autoarray/reg_matrix_logdet_nonfinite_fix.md (phase 2, opens with
    the spectrum dump; science-visible, needs evidence parity) and
    draft/bug/autofit/fitness_where_guard_nan_gradient.md.

## Original prompt

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

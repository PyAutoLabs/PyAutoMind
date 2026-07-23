# Kernel-CDF bandwidth defaults — config-dependent quality, investigate adaptivity

Type: research
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
- autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

## Context (2026-07-23, from the rectangular-mesh-consolidation reference re-derivation)

Post-consolidation (#402/#403), `RectangularAdaptImage`'s reconstruction quality
vs the old linear mesh is bandwidth- AND config-dependent, with opposite signs
across configs (log-likelihood, higher = better):

| config (autolens_workspace_test jax_likelihood_functions/imaging) | linear (old) | kernel bw=1.0 (default) | kernel bw=0.1 |
|---|---|---|---|
| rectangular.py (smoke config) | −651,693 | **−644,121** | −646,786 |
| rectangular_dspl.py (double power law) | −3,695.7 | −6,339.8 | **−3,823.9** |
| rectangular_mge.py | −82.9 | **−9.1** | not measured |

The 2026-07-10 certification sweep found the image-weighted parity floor at
bandwidth=0.1 (6.3e-4), and the dspl config now confirms the default (1.0) can
over-smooth the adapt-image weights badly on structured configs. Interim fix
(user-approved): dspl script pins `bandwidth=0.1` explicitly; other configs use
the default. All four interferometer configs pass at the default.

## Questions

1. Is there a principled default — e.g. bandwidth scaled by the adapt-image's
   effective structure scale, or per-axis adaptive bandwidth — that avoids
   per-config hand-tuning?
2. Should bandwidth be a free model parameter (prior config implications), a
   config-file knob, or stay a constructor kwarg?
3. Does the FD certification stay strict across the candidate default(s)
   (re-run jax_grad at any new default)?
4. Sweep bandwidth × config (the 3 imaging + 4 interferometer test configs +
   an HST-realistic developer config) to map the quality surface before
   deciding.

## Constraints

- Any default change is a behavior change for every workspace user — needs the
  same certification + reference-value discipline as #402.
- Library unit tests numpy-only; JAX validation via workspace_test jax_grad.

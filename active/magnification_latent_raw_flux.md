# Magnification latent from raw fluxes (no magzero), opt-in, documented only in results (arc phase 7a)

Type: feature
Target: autolens
Repos:
- PyAutoLens
- autolens_workspace
Epic: cluster-strong-lensing
Phase: 7a
Parent: draft/feature/autolens/magnification_errors_posterior_draws.md
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: judge
Filed: 2026-10-30
Issued: 2026-10-30
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/812
Witness: `magnification` latent = `total_lensed_source_flux / total_source_flux` (raw), finite with `magzero=None`, numerically equal to the old µJy ratio for positive fluxes; stays default `false`; `config/latent.yaml` and `guides/results/latent_variables.py` explain it; no source_science script mentions latents.

## Original request (human, 2026-10-30)

> do phase 7

Human ruling on the latent question: "I like the idea of us rewiring it in but latents are only explained in results
so dont do it in all workspaces [...] I dont want us to bring this concept in everywhere for a specific calculation
only certian users need" → rewire, keep opt-in (default false), document only in latent.yaml + the results guide.
Per-image point-magnification latents: not added (the number of images varies by dataset; documented).

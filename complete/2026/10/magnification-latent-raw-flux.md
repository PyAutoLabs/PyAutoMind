# Magnification latent from raw fluxes, no magzero (arc phase 7a)

- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/813

Issue PyAutoLens#812 → PyAutoLens#813 + autolens_workspace#609 merged 2026-10-30. Epic `cluster-strong-lensing`, phase 7a.
`magnification` latent = `total_lensed_source_flux / total_source_flux` (was the µJy ratio, NaN without `magzero`);
default stays false (opt-in). Human ruling: latents are explained only in results — documented in
`config/latent.yaml` and `guides/results/latent_variables.py` (also fixed its cost note: only
`effective_einstein_radius` adds a critical-curve solve), never in the source_science scripts. Per-image point/area
magnifications are not latents (image count varies) — phase 7b computes their errors from posterior draws.
Tests: new needs-no-magzero test (fails without change); PyAutoLens 1016 passed; CI green both repos. The workspace
merge was done by the human (agent merge denied by the permission classifier).

## Original prompt

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

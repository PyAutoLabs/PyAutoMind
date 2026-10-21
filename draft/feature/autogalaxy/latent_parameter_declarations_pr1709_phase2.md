# PyAutoGalaxy latent-parameter declarations (phase 2 of community PR PyAutoFit#1709)

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Blocked-by: release of PyAutoFit#1709 (pending-release)
Filed: 2026-10-21

Remainder of `complete/2026/10/finish-pr-1709-corner-plots.md`. PyAutoFit#1709 (merged 2026-10-21) added
`latent_parameters` class declarations, `af.Periodic`, path superscripts and the latent corner plot. The
contributor (@samlange04, proposal PyAutoLabs/.github#38) will open the PyAutoGalaxy PR declaring the
conversions after release. Their `feature/latent-parameters` branch was not public on 2026-10-21.

- Declare the conversions on PyAutoGalaxy components: external shear `(gamma_1, gamma_2)` → magnitude + angle;
  elliptical `ell_comps` → axis_ratio + angle (`Periodic` 180); multipoles → strength + phase (`Periodic` 360/m).
- Linked ellipticity (a power law's `ell_comps` shared into its multipoles) must keep the mass's latents. PyAutoFit
  now converts shared priors for every holder; add a PyAutoGalaxy test with real `PowerLaw` + multipole.
- Update the `notation.yaml` `superscript:` block comments. It now applies only to a bare unnamed `Model`.
- Review the contributor's PR rather than authoring it, unless they ask us to take it over.

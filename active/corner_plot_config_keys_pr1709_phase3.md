# Workspace config + docs for corner-plot labels and latent plots (phase 3 of PyAutoFit#1709)

Issued: 2026-10-26
Issue: https://github.com/PyAutoLabs/autofit_workspace/issues/177
Type: docs
Target: workspaces
Repos:
- autofit_workspace
- autogalaxy_workspace
- autolens_workspace
- HowToGalaxy
- HowToLens
Difficulty: small
Autonomy: supervised
Priority: medium
Status: issued
Consequence: glance
Blocked-by: PyAutoGalaxy#656 for profile latent-output examples and executed Markdown
Release-evidence: PyAutoFit 2026.10.23.1 is published/non-yanked and includes #1709 (verified 2026-10-26).
Filed: 2026-10-21

Remainder of `complete/2026/10/finish-pr-1709-corner-plots.md`. The library defaults cover the missing keys, so nothing breaks meanwhile.

- `config/visualize/plots_search.yaml` `nest:` add `corner_anesthetic_components`, `corner_anesthetic_latent` (false),
  `corner_anesthetic_latent_components`, with the library's comments.
- `config/output.yaml` add `latent_model_parameters: true`.
- `config/notation.yaml` `superscript:` comments: it now applies only to priors directly on an unnamed `Model`;
  named components are labelled by their path (`lens.bulge`, `source.pix.reg`).
- Contributor branches `feature/corner-plot-labels` on autofit/autogalaxy/autolens_workspace, HowToLens and HowToGalaxy may
  already carry these; land theirs if so.
- Release note: corner-plot labels change from class abbreviations to component paths (user-visible).

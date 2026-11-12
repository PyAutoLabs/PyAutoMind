# PyAutoLens II case studies

Issue: https://github.com/PyAutoLabs/autolens_workspace_developer/issues/147
Issued: 2026-11-12
Consequence: judge
Primary: @autolens_workspace_developer
Related: @PyAutoLens (paper_jax/paper.md only)

## Request (verbatim)

Looks good, go ahead with the plan. Update the paper around the three case studies and the Workspace and HowToLens section, then start setting up the JWST and ALMA fit.

## Approved scope

Three scientific case studies replace the standalone framework/benchmark sections:
SPT0418-47 joint JWST–ALMA with Nautilus and gradients, MACS J0416 source/image-plane
cluster fits, and a future autonomous 100-lens Euclid Q1 catalogue. Add Workspace and
HowToLens coverage; describe gradient teaching as planned until implemented.
Start implementation with the JWST–ALMA acquisition and bounded pilot setup.

Paper-only coordination with magnification-maps-wiring explicitly approved by user.
No library code changes, no merge authority. Full Euclid campaign remains gated.

## Implementation and validation

- Manuscript: approved case-study framing and figure placeholders.
- Developer scripts: scripts/paper_ii/jwst_alma/{acquire,model,fit,preview}.py,
  config.template.json and README.md. Data under ignored dataset/paper_ii/spt0418.
- Validate model sharing and separate source emission, input completeness gate,
  file syntax, downloaded FITS and checksums. Scientific fits require calibrated
  visibilities, PSF/noise/coordinate validation and a gradient check.
- Extend to staged SLaM after the parametric pilot is scientifically prepared.

Tier: judge — merge mode: human /prm

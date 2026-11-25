# Fiducial lens and pixelised-source set-up for each setting

Type: feature
Target: autolens_assistant
Repos:
- autolens_assistant
- autolens_workspace
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: For each setting, a committed script fits the fiducial lens (smooth, no perturbers, with noise) using the fiducial pixelised-source set-up, and the true power-law slope and Einstein radius lie inside the fit's 3 sigma posterior intervals; the assistant's pixelisation skill names the fiducial set-up as the default.
Review-minutes: 3
Unattended: needs-slicing
Lane: ral

Set up a fiducial lens for each setting, with a pixelised-source set-up that is known to give correct fits, so that a task which needs a pixelised-source fit knows to use it and does not end up with incorrect pixelisation fits.

## Why (human, 2026-11-25)

The dm_sightlines project (`Science/development/dm_sightlines`) ran "tier 3" refits on RAL: a `PowerLaw` + shear macro model with a pixelised source, fitted with Nautilus to noise-free simulated images. The human's ruling on the results:

> The pixelization fits are not reliable, because the source plane resolution for these lenses is much more coarse than the signal in the data. Even without sightlines or multipoles we would get incorrect fits (e.g. the offset power-law slopes). [...] To do pixelizations correct we'd need to use Delaunays with carefully set up source planes, or a Rectangular mesh which is set up with adaptive resolution more carefully.

What the fits used: a 50 x 50 `RectangularBilinearAdaptDensity` mesh, constant regularisation with a free coefficient, uniform priors centred on truth, no positions likelihood, 121 x 121 image at 0.05"/pixel, peak S/N about 50, 3" mask.

What went wrong, with no halos in the image at all:
- the smooth image's best-fit slope was 2.195 without multipoles and 2.321 with them, against a truth of 2.264;
- the fitted model's log evidence was 65 above that of the true macro model;
- the smooth-image chi-squared floor was 293 (regularisation coefficient 2.6).

The set-up was chosen by an agent with no fiducial to copy. Pixelised fits were then descoped from dm_sightlines; the pixelisation science is to be a separate science project.

Evidence: `Science/development/dm_sightlines/results/phase6_tier3/SUMMARY.md`, `wiki/project/2026-11-25-tier3-results.md` and `scripts/phase6_tier3_fit.py` in that project.

## Goal

For each setting, one fiducial simulated lens and one fiducial pixelised-source set-up that a task can pick up without designing its own:

- the mesh: a Delaunay with a carefully set-up source plane, or a Rectangular mesh whose adaptive resolution is set up carefully, with a source-plane resolution matched to the signal in the data;
- the regularisation, over-sampling, mask and any positions likelihood that go with it;
- a check that the set-up recovers the true macro model (slope, Einstein radius) on the fiducial lens, noise-free and with noise, with no perturbers in the image;
- a home where agents and tasks will find it and use it by default (the workspace, `Science/simulators/`, the assistant's skills, or a mix), and a statement of when a fit is outside what the fiducial covers.

## To settle at the start

- What "each setting" spans: my reading is each data regime a task is likely to simulate (for example HST-like, Euclid-like, higher resolution), but it could also mean each mesh type or each source type. Ask the human.
- Whether the fiducial lens is one of the existing standard simulated lenses in `Science/simulators/` or a new one.

## Not in scope

- The dm_sightlines simulator itself.
- The pixelisation science project that will use this.

<!-- formalised by the Intake (Conception) Agent on 2026-11-25 from file:/tmp/claude-1000/-home-jammy-Science/06d4049a-9b53-4c49-a937-6012f315232f/scratchpad/fiducial_pixelization_intake.md -->

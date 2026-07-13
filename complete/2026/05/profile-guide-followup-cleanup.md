## profile-guide-followup-cleanup
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/182
- completed: 2026-05-18
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/88, https://github.com/PyAutoLabs/autolens_workspace/pull/183
- repos: autogalaxy_workspace, autolens_workspace
- notes: Follow-up to PyAutoGalaxy #425 (profile-return-type-fixes). Removed two workspace-side workarounds in scripts/guides/profiles/ now that the library returns the correct wrapper types. (1) Basis demo in both light.py guides was using Galaxy.image_2d_from to dodge a Basis.image_2d_from quirk — switched to plain basis.image_2d_from. Also surfaced a pedagogical issue: the demo used al.lp_linear.Gaussian constituents which produced an all-zeros plot (intensities unset before inversion). Swapped to al.lp.Gaussian with explicit decreasing intensities (1.0 → 0.5 → 0.25 → 0.1 with sigmas 0.05 → 0.15 → 0.4 → 1.0) so the MGE shape is actually visible, with a follow-on note saying use lp_linear in real fits. (2) mass.py walkthrough swapped al.mp.dPIEPotentialSph for the elliptical al.mp.dPIEPotential now that its convergence_2d_from returns Array2D. Surveying for other Galaxy-wrap / *Sph fallbacks found none worth changing — Point Mass section still wraps in a Galaxy due to a separate unfixed library quirk (PointMass.convergence_2d_from returns raw ndarray); left alone.

## Original prompt

Workspace follow-up to PyAutoGalaxy #425
(`profile-return-type-fixes`): now that
`Basis.image_2d_from` and `dPIEPotential.convergence_2d_from` return
the correct wrapper types, the Galaxy-wrap and Sph-substitute
workarounds in the `scripts/guides/profiles/` guides can be removed.

While auditing the workaround removal, the Basis demo was also found
to plot an all-zeros map (an MGE of `ag.lp_linear.Gaussian` constituents
has no intensities yet — the inversion would solve those at fit time,
but in the standalone demo the image is just zeros). Switching the
demo to use standard `ag.lp.Gaussian` constituents with explicit
intensities produces a meaningful MGE plot, and a follow-on note
explains that you'd use `ag.lp_linear.Gaussian` in an actual fit.

Three small edits:

1. `autogalaxy_workspace/scripts/guides/profiles/light.py` — Basis
   section: swap `lp_linear.Gaussian` for `lp.Gaussian` with explicit
   intensities; drop the Galaxy wrap; plot `basis.image_2d_from(grid)`
   directly; update the prose to reflect the inversion-vs-explicit
   framing.
2. `autolens_workspace/scripts/guides/profiles/light.py` — same edit,
   `al.*` namespace.
3. `autolens_workspace/scripts/guides/profiles/mass.py` — Remaining
   Walkthrough: add or swap to `al.mp.dPIEPotential` (the elliptical
   variant) now that its `convergence_2d_from` returns `Array2D`.

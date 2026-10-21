# Interferometer primary beam: workspace example and docs

Type: docs
Target: autolens_workspace
Repos:
- autolens_workspace
- autogalaxy_workspace
Difficulty: small
Autonomy: safe
Priority: medium
Parent: active/interferometer_primary_beam.md
Status: formalised
Consequence: glance
Witness: the new interferometer advanced example script runs end to end under the workspace smoke harness and shows a simulated dataset with a Gaussian primary beam fitted with and without the beam
Review-minutes: 3
Unattended: ready
Filed: 2026-10-21
Blocked-by: PyAutoArray release containing https://github.com/PyAutoLabs/PyAutoArray/pull/644

## What

Library feature shipped in PyAutoArray#644 (hub #35, @HRSAstro). Add an `interferometer/advanced/primary_beam.py` example to autolens_workspace (mirror in autogalaxy_workspace): simulate ALMA-like visibilities with `aa.primary_beam_gaussian_from(mask, frequency_hz, dish_diameter_m)` passed to the simulator, fit with `Interferometer(primary_beam=...)` and without, show the reconstructed source flux difference, and document the dataset `primary_beam` / `from_fits(primary_beam_path=)` API in the interferometer docs page. Note the numba route is skipped when a non-trivial beam is set.

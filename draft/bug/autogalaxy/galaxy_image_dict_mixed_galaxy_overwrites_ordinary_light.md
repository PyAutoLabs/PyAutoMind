# Interferometer `galaxy_image_dict` drops a mixed galaxy's ordinary light (dict merge overwrites)

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- interferometer
- adapt-images
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-10-01
Difficulty: small
Consequence: judge
Witness: for one galaxy with `bulge=ag.lp.Sersic(intensity=0.1)` and `disk=ag.lp_linear.Gaussian(sigma=1.0)` fitted to `interferometer_7` (in-memory and array-free), `fit.galaxy_image_dict[galaxy]` equals the bulge image plus the linear reconstruction (rel 1e-8 to `fit.model_image_natural` for a single-galaxy fit), `fits_galaxy_images` writes that sum, and `ResultInterferometer.adapt_images_from()` receives it; the `FitImaging` mirror is checked and either confirmed correct or fixed the same way.
Review-minutes: 4
Unattended: ready
Source: Codex gpt-6-astra review of the streaming P4 branch (PyAutoLabs/PyAutoArray#598), 2026-10-01 — three independent runs, same finding; pre-existing on main, newly reachable for array-free ordinary-light fits.

## What

`ag.FitInterferometer.galaxy_image_dict` (autogalaxy/interferometer/fit_interferometer.py ~L537-540) and the
`al.FitInterferometer` mirror (autolens/interferometer/fit_interferometer.py ~L388) build the per-galaxy image dict
by unpacking the ordinary-light dict and the linear-object dict: `{**galaxy_image_dict, **galaxy_linear_dict}`
(or equivalent). A galaxy that appears in both — an ordinary profile plus a linear light profile, Basis/MGE or
pixelization — has its ordinary image **replaced** by the linear reconstruction instead of summed. For images
`p` (ordinary) and `s` (linear) the dict holds `s`, not `p + s`.

Consumers: `ResultInterferometer.adapt_images_from()` via `model_image_galaxy_dict` (adaptive meshes/regularisation
get incomplete morphology), `fits_galaxy_images` output. `model_image_natural` (P3) is unaffected because it sums
`profile_image + mapped_reconstructed_data` directly — the P3 Codex finding fixed only that path.

## Plan

1. Reproduce with the witness galaxy on main (in-memory): assert `galaxy_image_dict[g] == bulge image + linear image`
   fails; check `FitImaging.galaxy_model_image_dict` for the same merge.
2. Fix: sum per galaxy when a key is in both dicts (`dict` comprehension over the union of keys), both libraries.
3. Tests: mixed-galaxy `galaxy_image_dict` in ag and al interferometer fit tests (in-memory and array-free), plus
   an adapt-images test if cheap.

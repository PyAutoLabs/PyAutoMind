`SersicGradient` and `GaussianGradient` now share one mass-to-light gradient convention: a positive `mass_to_light_gradient` means M/L falls outward, M/L ∝ (R / R_pivot)^-gradient. The Sersic pivot sits exactly on the R_e ellipse for any q (it was R_e/q); the GaussianGradient exponent sign is flipped and it pivots at `mass_to_light_radius`; `cse_settings_from` is branch-free so a free gradient runs under `jax.jit`. Release notes: GaussianGradient with a non-zero gradient reverses its radial trend; SersicGradient with q < 1 and a non-zero gradient changes normalisation by q^gradient.

Decision taken, accepted as is by the human: the GaussianGradient 0.01 arcsec softening was dropped (M/L diverges as sigma -> 0 for a positive gradient).

Shipped in PyAutoGalaxy#726 then autolens_workspace_test#368 (the Keeton-integral reference script's pivot), both merged 2026-11-19 by human /prm after shift 2026-11-18-pm2. Follow-ups noted on the PR, not filed: `convergence_2d_from` not jittable for any Sersic profile; a likelihood step at gradient 0.5 (CSE settings switch); ~2–3% CSE error at gradient -0.6, n = 4.5; dead `SersicGradient.decompose_convergence_via_mge`.


## Original prompt

# Stellar M/L-gradient profiles: SersicGradient pivots at R_e/q, GaussianGradient has the opposite sign…

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: for axis ratio 0.6 the `SersicGradient` M/L equals `mass_to_light_ratio` on the ellipse of effective radius, `SersicGradient` and `GaussianGradient` with the same positive gradient both have M/L falling outward, and a jitted likelihood with a free gradient runs
Review-minutes: 3
Unattended: ready
Verified: 2026-11-18 055509e3 (PyAutoGalaxy)
Lane: any

Found 2026-11-16 in the science project stars_dm_slope by reading the code (written up in `/home/jammy/Science/Science/development/stars_dm_slope/wiki/project/2026-11-16-parameterisation-and-systematics.md`, section 3). Three related problems in the mass-to-light gradient profiles:
1. `SersicGradient` (`autogalaxy/profiles/mass/stellar/sersic_gradient.py`): kappa = mass_to_light_ratio x (q R_c / R_e)^(-mass_to_light_gradient) x I(R_c). The gradient's argument carries an extra axis-ratio factor that the light's argument does not, so the M/L equals `mass_to_light_ratio` at R_e/q rather than at R_e (only correct for q = 1). The docstring gives no sign convention.
2. `GaussianGradient` (`gaussian_gradient.py`): M/L_i = base x ((sigma_i + 0.01) / radius)^(+mass_to_light_gradient), the opposite sign of exponent to SersicGradient, with a hard-coded 0.01 arcsec softening; its docstring says a positive value gives "more mass per unit light within the reference radius", which contradicts the code.
3. `cse_settings_from` (`mass/stellar/sersic.py`) branches in Python on `mass_to_light_gradient > 0.5`, so a traced (free) gradient probably raises a tracer-boolean error under `jax.jit` (unverified: write the reproducer first).
Fix: decide one convention (positive gradient = M/L falls outward, pivot exactly at R_e for the Sersic and at an explicit reference radius for the Gaussian), correct docstrings and code to match, make the gradient path branch-free for JAX, and add tests of the pivot, the sign and jit with a free gradient. Changing the sign or pivot changes results for existing users: flag it in the release notes.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Science/4543c7f0-9e90-432b-a76f-76d0789fa7b1/scratchpad/intake/6_mass_to_light_gradient_conventions.md -->

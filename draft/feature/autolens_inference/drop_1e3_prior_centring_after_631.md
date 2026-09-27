# Drop the 1e-3 prior centring for shear / multipole / ell_comps in the benchmark

Type: feature
Target: @autolens_inference
Filed: 2026-09-27

The inference benchmark centres ExternalShear, multipole_comps and ell_comps priors on 1e-3 to avoid NaN
jax.grad at exactly 0. PyAutoGalaxy#631 (PR #634, companion PyAutoLens#754) makes those gradients finite and
correct at 0 (Isothermal included). Once #634 is released, restore the natural 0 prior medians and
confirm gradient searches start cleanly (no NaN on the first step). Blocked on the PyAutoGalaxy release.

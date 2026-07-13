## group-mass-stellar-dark
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/158
- completed: 2026-05-16
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/164
- notes: Two-stage task. Stage 1 padded out imaging features/advanced/mass_stellar_dark/ with new fit.py + likelihood_function.py + a Practical Use chaining callout on modeling.py + committed dataset (FITS + tracer.json). Stage 2 created scripts/group/features/advanced/mass_stellar_dark/ — 8 files (simulator, fit, likelihood_function, modeling, chaining, slam, README, __init__) using the group lens_dict API where each main lens galaxy carries its own lmp.Sersic + NFWSph decomposition with ExternalShear on lens_0 only. Source remains single-plane (z=1.0). Both stages' executable scripts validated end-to-end — decomposition assertions pass (sum_i(alpha_stellar_i + alpha_dark_i) + alpha_shear matches tracer total deflection). Pre-existing PyAutoGalaxy bug in print_vram_use / cse_settings_from blocks modeling.py / chaining.py / slam.py full Nautilus runs for lmp.Sersic lenses (reproduces on canonical main; both use_jax=True and use_jax=False paths affected) — filed as https://github.com/PyAutoLabs/PyAutoGalaxy/issues/417, NOT touched here per "never modify code to make tests pass". SLaM gotcha: al.util.chaining.mass_light_dark_from hardcodes a single "lens" key path on light_result.instance.galaxies, incompatible with lens_dict — group slam.py constructs MASS LIGHT DARK per-galaxy manually via take_attributes + UniformPrior(mass_to_light_ratio). dataset/.gitignore precedence gotcha re-confirmed: workspace-root allow-list (!dataset/<type>/<name>/**) is shadowed by in-tree dataset/.gitignore (*); new datasets need git add -f.

## Original prompt

The imaging `features/advanced/mass_stellar_dark` example needs improving and padding out before adapting to group.

Once the imaging version is more complete, adapt it to the group context in
`scripts/group/features/advanced/mass_stellar_dark/`.

For group lenses, decomposing total mass into stellar and dark components for each galaxy is valuable
for studying the mass-to-light ratio across the group environment. Each main lens and extra galaxy
would get separate stellar (tied to light via M/L) and dark (e.g. NFW) components.

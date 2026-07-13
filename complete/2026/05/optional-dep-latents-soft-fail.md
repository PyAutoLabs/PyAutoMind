## optional-dep-latents-soft-fail
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/464
- completed: 2026-05-28
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/465, https://github.com/PyAutoLabs/PyAutoLens/pull/558
- repos: PyAutoGalaxy, PyAutoLens
- notes: Soft-fail backstop in PyAutoGalaxy `lens_calc.py` for missing `jax_zero_contour` (returns NaN / [] with one warning per process per feature, mirrors `_maybe_magzero_warn`). Caller-side fallback in PyAutoLens `effective_einstein_radius` routes the JAX path to the existing NumPy `einstein_radius_from(grid)` branch when the dep is missing, so users keep a real value instead of NaN. Surfaced on autolens_profiling job 322552.

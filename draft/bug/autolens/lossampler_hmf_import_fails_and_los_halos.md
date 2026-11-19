# LOSSampler hmf import fails and los_halos falls back silently

Type: bug
Target: PyAutoLens
Repos:
- PyAutoLens
- autolens_workspace
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: glance
Witness: In an environment with the declared dependencies only, `LOSSampler(z_lens=0.5, z_source=1.0)` with no precomputed coefficients samples a population whose per-plane mass-function slope is within 0.02 of -1.906 and whose expected halo count for 1e7 to 1e10 solar masses in a 5 arcsecond cone is within 5% of 1282; and the workspace `los_halos` simulators either use those real coefficients or stop with a clear message, never a silent placeholder.
Review-minutes: 3
Unattended: ready
Verified: 2026-11-19 a79a6b22 (PyAutoLens), 4674ae89 (autolens_workspace)
Lane: any

## Finding

Three linked problems, measured on PyAutoLens `main` a79a6b22c, 2026-11-19.

1. `@PyAutoLens/autolens/lens/los.py` `mass_function_ab_from` does `import hmf.fitting_functions`.
   With hmf 3.7.2 this raises `ModuleNotFoundError`; the module now lives at
   `hmf.mass_function.fitting_functions`.
2. `hmf` is not a declared dependency of any library, and is not installed in the science
   environment. `LOSSampler` with no precomputed coefficients therefore raises.
3. `@autolens_workspace/scripts/imaging/features/advanced/los_halos/simulator.py` and
   `simulator_jax.py` wrap the coefficient calculation in `except ImportError` and fall back to
   `[-1.9, 8.0]` for the mass function and `[-3.0, 40.0]` for the concentration relation. Because
   problem 1 is an `ImportError`, this fallback runs even when hmf is installed.

The placeholders are not close. Real fitted coefficients run from A = -1.905, B = 8.053 at z = 0.1 to
A = -1.910, B = 8.171 at z = 0.9. The fallback ignores redshift evolution and under-counts halos by
up to 20 to 23% at z = 0.9. The concentration fallback is off by up to 17%, 32% and 56% at
z = 0.1, 0.5 and 0.9.

## Why it matters

Every run of the workspace line-of-sight examples in the current environment simulates a halo
population that is not the Sheth-Tormen plus Ludlow16 population the text describes, with no
message saying so.

## Ask

Preferred: drop hmf and compute the mass function from colossus
(`colossus.lss.mass_function.massFunction`, `model='sheth99'`), which the sampler already uses for
the concentration relation. Measured agreement of the existing power-law fit with colossus
`sheth99`: integrated number 0.98 to 1.00, integrated mass 0.992. Then declare colossus as an
optional dependency of PyAutoLens for the line-of-sight feature.

Minimal alternative: fix the import path and declare hmf as an optional dependency.

In both cases, change the workspace simulators so a missing dependency stops with a clear message
or prints a loud warning; do not keep a silent placeholder. Library fix first, workspace second.

## Provenance

[from: research dm-sightlines-cdm] Checks 3 and 4 of the verification run. Scripts and logs:
`Science/scratch/dm_sightlines_research_2026-11-19/evidence/verify/check3_massfunction.py`,
`check3_import.log`, `check4_concentration.py`.

<!-- formalised by the Intake (Conception) Agent on 2026-11-19 from file:/tmp/claude-1000/-home-jammy-Science/4c8e2ded-c0f1-44a2-878a-797321efeaa7/scratchpad/raw/b2.md -->

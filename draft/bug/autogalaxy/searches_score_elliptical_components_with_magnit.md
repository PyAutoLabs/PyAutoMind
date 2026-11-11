# Searches score elliptical components with magnitude >= 1, so results can't be…

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoFit
- PyAutoGalaxy
- HowToLens
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: glance
Witness: re-running HowToLens chapter 2 tutorial 3's "less thorough" search (n_live=50, seed=1) produces a samples.csv with zero rows where any elliptical component pair has magnitude >= 1, and loading the result prints no "cannot be reconstructed as a model instance" warning.
Review-minutes: 3
Unattended: ready
Lane: ral

Found 2026-11-10 on HowToLens#130 (stored results, PR HowToLens#134).

## Symptom
HowToLens `scripts/chapter_2_lens_modeling/tutorial_3_why_modeling_is_hard.py`, search `tutorial_3_less_thorough` (Nautilus, n_live=50, seed=1, JAX likelihood on CPU), run for real on RAL at release 2026.11.9.1:
- The search completes (log Z -59,734, a deliberately failed fit).
- 9,693 of its 10,305 samples (99 % of posterior weight) have `galaxies.source.bulge.ell_comps` with magnitude >= 1. The lens bulge and mass components are all valid.
- Its stored max-likelihood sample is one of these. Rebuilding it raises `autogalaxy.exc.ModelParameterException: ell_comps must satisfy ell_comps[0]**2 + ell_comps[1]**2 < 1; got (-0.7748, 0.9988), whose magnitude is 1.264...`.
- PyAutoFit then warns ("The maximum log likelihood sample stored in the samples summary cannot be reconstructed as a model instance, falling back to the highest likelihood sample the model still accepts"). With only invalid stored samples it raises `autofit.exc.SamplesException: None of the stored samples can be reconstructed`.

## Likely cause (to confirm)
The magnitude check fires when a model instance is built eagerly (NumPy, checks on), but the sampled likelihood path, JAX vmap/batched and possibly with checks skipped, evaluates and scores points outside the unit circle instead of rejecting them. Nautilus therefore explores and weights an unphysical region. Default priors are independent `UniformPrior(-1, 1)`-style per component, so the square's corners are reachable.

## Questions
1. Where should invalid ell_comps be rejected during sampling: as a resample/`-inf`/invalid value in the JAX likelihood, or via prior/parameterization (e.g. a magnitude/angle parameterization or a joint prior constraint)?
2. Is the same true for numpy/non-batched searches and for other searches (Emcee, Prodigy)?
3. Does any default-prior configuration make |ell_comps| >= 1 reachable for other profiles?

## Context
- HowToLens's `.github/scripts/stored_results.py` works around it by thinning only valid rows and always keeping the best valid one. That workaround can go once this is fixed, and the tutorial's warning disappears.
- Related family: gradient-sweep item "ell_comps=0 point" (re-filed to PyAutoGalaxy), a different edge of the same constraint.

<!-- formalised by the Intake (Conception) Agent on 2026-11-11 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/5ee98b5f-b187-4b0a-83a9-3ad898ce13b8/scratchpad/ell_bug.md -->

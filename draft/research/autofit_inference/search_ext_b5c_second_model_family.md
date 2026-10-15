# `@autofit_inference` B5c: a second model family for the search benchmark

Type: research
Target: autofit_inference
Repos:
- autofit_inference
- PyAutoInsight
- PyAutoCortex
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Filed: 2026-10-14
Consequence: judge
Epic: search-extensibility
Phase: B5c
Witness: a second toy-likelihood family is committed with its own pre-registered protocol (`<family>@1`), seeded datasets, references per backend with the §6 agreement test, and a wave-1 pilot manifest, before any of its rows exist; the catalogue groups it by task, separately from gaussian_x3, and ranks nothing across families.

## Why
gaussian_x3 tests label switching and a blend at 10 parameters, but its posterior is close to Gaussian and low-dimensional. A ranking from one family says nothing about the geometries where searches really differ. B5c adds one family that stresses a different axis.

## Candidates
1. **Multimodal (well-separated modes).** For example, an 8-D mixture with 4 to 8 isolated Gaussian modes of unequal weight, and an exact ln Z by construction. It tests mode discovery and weight recovery, where nested samplers should win and gradient chains should fail. It overlaps with gaussian_x3's label modes, so it is a weaker new axis.
2. **High-D correlated (ill-conditioned Gaussian or banana).** For example, a 50–100-D Gaussian with condition number 10^3–10^4, plus a Rosenbrock-banana variant, with an exact posterior and ln Z. It tests scaling with dimension and mass-matrix adaptation, where NUTS and MultiStart should shine and nested samplers' wall should blow up. It is the axis PyAutoLens high-D pixelised fits care about most.
3. **Funnel (Neal's funnel, 10–20-D).** It has an exact marginal on v, tests varying curvature, and breaks naive NUTS without reparameterisation. Diagnostics are well understood (divergences, R-hat).

## Recommendation
Candidate 2, high-D correlated. Run the Gaussian at D = 20, 50 and 100 with condition number 10^3, plus one banana at D = 20.
- It is the most informative new axis relative to gaussian_x3, which already covers multimodality.
- It is cheap: the likelihood is analytic, and the reference is exact, so no Nautilus reference runs are needed.
- It feeds the epic's gradient-search questions directly (A2 gradients, NUTS warm start).

Keep funnel as B5d if B5c shows NUTS divergences matter.

## Size
- **Pilot:** 10 seeds × 3 dimensions × the gaussian_x3 menu, about 600–800 runs. Nested samplers will dominate the wall at D = 100, so cap or defer them per dimension with reasons.
- **Scored wave:** 50 seeds × 3 realisations, about 6–8k runs.
- **Compute:** about 1–2k core-hours on `ral` at the RAL speeds measured in B5a.

## Shape
Mirror B2–B5a: protocol first, a generator for datasets and exact references, then the pilot manifest and pilot, then the freeze and the scored wave. Use one Insight task per wave and Cortex run lines with job ids. It runs `--partition=ral` only, on a private library pin.

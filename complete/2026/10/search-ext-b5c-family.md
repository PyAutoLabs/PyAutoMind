## search-ext-b5c-family
- issue: https://github.com/PyAutoLabs/autofit_inference/issues/14
- completed: 2026-10-16
- epic: search-extensibility
- workspace-pr: https://github.com/PyAutoLabs/autofit_inference/pull/16
- workspace-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/70
- workspace-pr: https://github.com/PyAutoLabs/PyAutoInsight/pull/33
- summary: B5c stage 1 of search-extensibility — a second toy-likelihood family, `correlated_nd` (correlated Gaussians at D = 20/50/100 with condition number 10^3 from a seeded Haar rotation, plus a D = 20 hybrid Rosenbrock banana), each with an exact posterior and exact ln Z so no reference search is run. Protocol `correlated_nd@1` (`wiki/project/protocol_correlated_nd.md`) was committed first at `9ec37795f404`, amendment A1 before any row; seeded generator, exact-model module and 8 references (4 datasets × numpy/JAX) pass the §6 agreement test; the catalogue groups the family by task apart from `gaussian_x3` and ranks nothing across families. The 930-run pilot (10 seeds × realisation 1 × 93 cells; Nautilus exempt from the live-point floor under A1; 110 runs deferred — Emcee/Zeus D≥50, DynestyStatic/NSS D=100) ran on RAL as 410866_[0-929]%100 `--partition=ral` from the PRIVATE copy `/mnt/ral/jnightin/inference/autofit_inference_b5c` at pin df6d218f1: 926 COMPLETED, 4 OUT_OF_MEMORY at 8 G, wall 4:16 (2026-10-15 23:50 → 10-16 04:06 UTC). Nothing is pulled or scored in this stage (autofit_inference#16, merge 40fd0babe). Cortex run line closed with `cortex done` and a dated Log entry (PyAutoCortex#70, e7c7d5948); Insight task row `correlated_nd_pilot`, campaign next lines and board (PyAutoInsight#33, 15ec6fd9a).
- pilot-oom: all four on `corr_gaussian_d50` data_seed 1 — task 263 nautilus n_live_100 numpy seed 3 (7.6 G, 2:42); 273 nautilus n_live_100 jax_cpu seed 3 (7.7 G, 2:42); 304 nautilus n_live_400 numpy seed 4 (3.1 G, 0:52); 383 blackjax_nuts_warm warmup_200_samples_500 jax_cpu seed 3 (8.4 G, 3:52). Human decision 2026-10-16: not rerun in stage 1; B5c-2 raises the memory request for d50/d100 nested and NUTS cells or excludes them with reasons.
- traps: the first resubmission 409957 failed at import because the shared RAL clone was switched to an old main and lost `cli/` + `config/` by another actor while the array started — always submit from a private pinned copy. CI `lint` failed twice on the byte-for-byte dataset regeneration test (last-bit QR/LAPACK differences, then eigenvector entries near zero under a per-element rtol): the test now keeps the byte check and falls back to structural JSON comparison with normwise `np.allclose(rtol=1e-12, atol=1e-12 × max|x|)` for float arrays; committed datasets unchanged.
- follow-up: B5c-2 (`draft/research/autofit_inference/search_ext_b5c2_freeze_and_scored_wave.md`) pulls `results/` of 410866 from the private copy, judges under `@1`, settles the OOM cells, freezes `correlated_nd@2` and submits the scored wave (50 seeds × 3 realisations, about 6–8k runs, `--partition=ral`, private pin). Remaining for the epic beyond B5c-2: release of the pending-release PyAutoFit chain (#1667–#1696) by human `/review_release` once Heart clears RED.

### Compute (for B5c-2)

- compute: RAL 410866_[0-929]%100 `--partition=ral` COMPLETED 2026-10-16 04:06 UTC (926 ok, 4 OOM: 263/273/304/383); `results/` unpulled in the PRIVATE copy `/mnt/ral/jnightin/inference/autofit_inference_b5c` (pin df6d218f1; pilot manifest `hpc/batch_cpu/correlated_nd/pilot.tsv`, task N = line N+2); nothing running for this epic phase

## Original prompt

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
Issued: 2026-10-15
Issue: https://github.com/PyAutoLabs/autofit_inference/issues/14
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

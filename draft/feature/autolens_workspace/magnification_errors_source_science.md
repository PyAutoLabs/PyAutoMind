# Magnification errors from posterior draws in every source_science.py (arc phase 7b)

Type: feature
Target: autolens_workspace
Repos:
- autolens_workspace
Epic: cluster-strong-lensing
Phase: 7b
Parent: draft/feature/autolens/magnification_errors_posterior_draws.md
Difficulty: large
Autonomy: supervised
Priority: normal
Consequence: glance
Filed: 2026-10-31
Witness: All 11 `source_science.py` scripts (imaging, interferometer, group, multi_galaxy × top-level / multi_gaussian_expansion / pixelization) have a `__Magnification Errors__` section that fits the dataset (Nautilus, `PositionsLH`, `use_jax=True`; the pixelization scripts reuse their existing fit), draws N samples from `result.samples`, and prints median + 16/84 percentile intervals for source μ, point μ at the multiple images and area μ per image, with N and measured runtime in the prose; the draw loop takes the source redshift and maps it to `plane_j`; every changed script runs clean locally in full mode (fit recovers the simulated truth) and under PYAUTO_SMALL_DATASETS.

## Original request (human)

2026-10-30: phase 7 → "add a quick fit to each" (9 of 11 scripts have no fit today).
2026-10-31: "override heart red, go ahead with 7b"; quick-fit cost (~21 min laptop CPU, n_live=100) confirmed:
"Quick fit in each (as chosen)".

## Context

Prototype `/mnt/c/Users/Jammy/Workspace/Science/scratch/arc_phase7b_prototype_2026-10-30/proto7b.py`, valid run
`run3/` (full 100×100 simulation): fit 1265 s, θE 1.601 vs 1.6; 2.85 s/draw; σ_μ/|μ| source 0.7%, point 1.5–1.8%,
area 0.7–4% — below the LEGGOS II 0.03–0.09 range (high-S/N simulated data, simple parametric model); explain in prose.
Traps: the canonical on-disk dataset may be the 16×16 smoke simulation — keep the `should_simulate` guard before load;
a raw 10%-of-peak arc mask fragments into many "images" at 0.1″ — reuse each script's existing image definition
and combine fragments. Prose rule: describe calculations as they stand. Latents stay out of source_science (7a ruling).

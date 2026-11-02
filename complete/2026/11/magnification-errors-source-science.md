Arc phase 7b: every `source_science.py` script (imaging, interferometer, multi_galaxy, group × top-level /
multi_gaussian_expansion / pixelization; 11 scripts) ends with a `__Magnification Errors__` section — a quick
Nautilus fit with `PositionsLH`, 100 draws from the posterior, median and 68% interval of the source, point and area
magnifications, as LEGGOS II report theirs.

Shipped:
- autolens_workspace#613 (`c0ea84c7`) — the 11 scripts, isothermal quick fits for the pixelization scripts,
  `interferometer/simulator.py` high-resolution section writes `simple_high_resolution` (it overwrote `simple`),
  regenerated navigator catalogue.
- PyAutoFit#1751 (`e9d3c6a2`) — `draw_randomly_via_pdf` normalises sample weights; released in 2026.11.1.1.

Results (full runs vs simulated truth):
- imaging: fit ~10 min, ~2 s/draw, errors 1–2%, truth within or just outside the intervals.
- imaging pixelization (isothermal): mesh μ 30.6 ± 1% vs truth 34.9 (the true model's mesh μ is 30.9, so the −12%
  offset is the mesh reconstruction); point μ ~13% low. PowerLaw quick fit: slope ~2.2, μ ~40% low.
- interferometer: fit ~9 min, 1.3 s/draw; area μ within 1% of truth; source μ 7.85 vs 7.26 (+8%, outside errors).
- Prose states the errors are statistical only (human ruling 2026-11-02).

Scope change (human, 2026-11-02): "end to end runs ... testing overkill" — the multi_galaxy, group and
interferometer pixelization full runs were stopped/not run (multi_galaxy still exploring after ~9 h). Those 7 scripts
describe how to read the errors without measured numbers; all 11 pass smoke locally and in CI.

Follow-ups filed (Mind 3a220445):
- draft/bug/autogalaxy/area_magnification_critical_curve_fragments.md
- draft/docs/autolens_workspace/source_science_multi_galaxy_group_quick_fits_slow.md

Full-run outputs and logs: Science/scratch/arc_phase7b_full_runs_2026-11-02/.

## Original prompt

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
Issued: 2026-10-31
Issue: https://github.com/PyAutoLabs/autolens_workspace/issues/610
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

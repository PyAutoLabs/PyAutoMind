Arc phase 8c: the magnification uncertainty map of LEGGOS II figure 4. `magnification_fractional_error_2d_from`
(half the 16-84 percentile range of |mu| over posterior draws / best-fit |mu|, per pixel) and
`plot_magnification_uncertainty_2d` (that map, colour range capped at the 95th percentile, best-fit constant-mu contours
and critical curves on top). Workspace: all 11 source_science.py scripts (human scope) store each draw's
magnification map in the 7b draw loop and plot the map in a new `__Magnification Uncertainty Map__` section.

Shipped (merged 2026-11-02, human /prm):
- PyAutoGalaxy#693 (`f397c6b2`) — test_autogalaxy 1475 passed
- PyAutoLens#817 (`03ab1f82`) — 1021 passed
- autolens_workspace#616 (`6720e3d1`) — all 11 scripts smoke clean; catalogue regenerated

Witness (full imaging/source_science.py run, 100 draws, 1.84 s/draw): median sigma/|mu| 0.23% (|mu| 1-3), 0.50%
(3-10), 2.0% (10-30), 8.8% (>30, on the critical curve); consistent with the run's scalar errors (0.9-1.9%). Figure +
log: Science/scratch/arc_phase8c_uncertainty_map_2026-11-02/.

- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/693
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/817

## Original prompt

# Magnification maps 8c: LEGGOS Fig-4 fractional magnification uncertainty map

Type: feature
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
- PyAutoLens
- autolens_workspace
Themes:
- visualization
- cluster
Epic: cluster-strong-lensing
Phase: 8c
Parent: draft/feature/autolens/magnification_maps_visualization.md
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: no
Filed: 2026-11-02
Issued: 2026-11-02
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/692

## Context

Slice of phase 8. Per image pixel sigma_mu/|mu_best| over the phase-7b posterior draws (each draw → 8a mu map), with
the best-fit constant-mu contours overlaid, as LEGGOS II Fig. 4. Library helper only if the draw loop proves reusable.
Workspace: source_science scripts (start with imaging). Witness: map renders from 100 draws on imaging simple.

## Original request (human, 2026-11-02)

> start 8c
> yes go ahead, all 11 scripts

## Approved plan (2026-11-02)

1. PyAutoGalaxy: `magnification_fractional_error_2d_from(magnification_list, magnification_best)` (half the 16-84
   percentile range of |mu| over the draws / |mu_best| per pixel) and `plot_magnification_uncertainty_2d(
   magnification_list, magnification_best, grid, mass_obj=None, ...)` — fractional-error map, colour range capped
   (diverges on the critical curves), best-fit constant-mu contours via the 8a helper, optional critical curves.
2. PyAutoLens: aplt export + test.
3. autolens_workspace: all 11 source_science.py scripts — the 7b draw loop also stores each draw's mu map (coarser
   grid), new `__Magnification Uncertainty Map__` section; catalogue regen; smoke all 11.
4. Witness: one full run of imaging/source_science.py (100 draws); report fractional errors away from the critical
   curves next to 7b's 1-2% scalar errors. No full runs of the other 10 (human 2026-11-02: end-to-end runs overkill).

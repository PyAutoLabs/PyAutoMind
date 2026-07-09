# Released workspace datasets are 15×15 smoke artifacts

Autonomy: supervised
Difficulty: medium
Found: 2026-07-09, by the first run of verify_install check F (Colab simulation) —
the simulated notebook cell loaded `dataset/imaging/simple/data.fits` from the
2026.7.6.649 tag and got shape (15, 15) instead of (100, 100).

## Evidence (autolens_workspace)

- **30 of 49 `data.fits` files at tag `2026.7.6.649` are ≤15×15** — the exact
  `PYAUTO_SMALL_DATASETS=1` footprint.
- **29 of those are 15×15 on committed `main` too**, last touched by "pre build"
  commits dated 2026-05-21 (e.g. `1b54dbb7` for `imaging/dark_matter_subhalo`).
- `imaging/simple` was restored to 100×100 on main by `6f4d0049` (2026-05-29,
  extra-galaxies ingrain), **but the tag still ships 15×15** with
  `git log 2026.7.6.649..origin/main -- <file>` EMPTY — i.e. the release lineage
  itself re-committed a smoke-regenerated dataset on top of main's fix.

## Suspected mechanism

The pre-build / release pipeline runs workspace simulator scripts under the
smoke env (`PYAUTO_TEST_MODE` / `PYAUTO_SMALL_DATASETS=1` — which mutates
`Grid2D.uniform` inside decorators) and then commits the regenerated
`dataset/` outputs alongside notebooks. Both legs need fixing:

1. **Stop the leak**: the pipeline must never commit `dataset/` regenerated
   under smoke env (exclude dataset/ from the release commit, or run
   simulators full-size, or don't run them at all at release).
2. **Repair the data**: regenerate all affected datasets full-size and commit
   to main (the local checkouts' dirty dataset churn seen today in
   HowToFit/HowToGalaxy/HowToLens may be exactly such regenerations —
   verify before reusing). Audit autogalaxy_workspace, autofit_workspace and
   the three HowTo repos for the same committed 15×15 class.
3. **Guard**: a Heart check (or pre-commit in the pipeline) asserting example
   `data.fits` shapes exceed the smoke footprint (e.g. min dimension > 20 px).

## Impact

Every pip/Colab/tagged-zip user since at least 2026-05-21 gets degenerate
15×15 example images for most datasets — fits "work" but are scientifically
meaningless and visually broken. The Colab flagship `start_here` notebooks
load these.

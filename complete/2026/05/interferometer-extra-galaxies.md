## interferometer-extra-galaxies
- issue: https://github.com/PyAutoLabs/autogalaxy_workspace/issues/81
- completed: 2026-05-17
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/82
- notes: Single-repo task (autogalaxy_workspace only). Built scripts/interferometer/features/extra_galaxies/ — modeling.py + simulator.py + README + __init__. Adapts autogalaxy imaging extra_galaxies pattern (multi-galaxy field fitting via light profiles) for interferometer data, with autolens interferometer/features/extra_galaxies/ as a read-only structural template (lens-mass aspects stripped). Main galaxy: linear Sersic bulge + linear Exponential disk. Each extra galaxy: linear SersicSph with fixed centre loaded from extra_galaxies_centres.json (Option A); MGE alternative commented inline (Option B). Real-space mask radius=6.0" to cover extras offset at (±3.5"). Uses TransformerNUFFT (nufftax) — multi-galaxy fits practical because every galaxy's light profile is NUFFT'd inside the JIT'd likelihood. Key teaching point: autogalaxy/autolens role split (autogalaxy fits LIGHT of extras for multi-galaxy fields; autolens fits MASS of extras for lensing perturbation). Noise-scaling approach from autogalaxy imaging not portable to interferometer (uv-plane data not directly tied to image-plane pixels) — modeling.py uses modeling-approach exclusively with rationale called out in "Approaches to Extra Galaxies" section. No imaging Phase 1 sweep (prompt was direct-port, not review pass). No slam.py (autogalaxy is non-lensing). Both smoke tests pass — simulator.py produced dataset/interferometer/extra_galaxies/{data,noise_map,uv_wavelengths}.fits + galaxies.json + extra_galaxies_centres.json; modeling.py composed N=15 free-param model and called likelihood once under PYAUTO_TEST_MODE=2. Tracker now 5 shipped / 3 outstanding (double_einstein_ring, mass_stellar_dark, scaling_relation remain).

## Original prompt

The autogalaxy imaging `features/extra_galaxies` example needs adapting to interferometer.

Adapt it to the interferometer context in
`autogalaxy_workspace/scripts/interferometer/features/extra_galaxies/`. The `autolens_workspace`
already has an interferometer port at `scripts/interferometer/features/extra_galaxies/` — use it as
a structural template for `modeling.py` and `simulator.py`, stripped of the lens-mass aspects since
autogalaxy is for non-lensing morphology fits.

Modeling extra (perturber / line-of-sight companion) galaxies in the field works identically for
imaging and visibility data once light profile transforms are fast — which they now are thanks to
nufftax. The script should explain the autogalaxy use case (multiple galaxies in a field of view,
not lensing) and how the visibility-domain fit proceeds.

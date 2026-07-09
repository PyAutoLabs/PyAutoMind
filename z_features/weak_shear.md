Weak gravitational lensing series — multi-step epic adding `WeakDataset`, simulator, plotter, fit, modeling and likelihood-function tutorial across PyAutoLens + autolens_workspace, culminating in a real-data cluster analysis and a combined strong+weak example (the "home-straight push", scoped 2026-07-09).

Science scope: cluster/group-scale weak shear as the large-radius complement to strong lensing — Niemiec et al. 2020 hybrid-Lenstool (arXiv:2002.04635, joint SL+WL cluster reconstruction) and Oguri et al. 2012 Sloan Giant Arcs Survey (arXiv:1109.2594, stacked SL+WL of 28 group/cluster lenses). NOT cosmic shear or galaxy-galaxy lensing.

shipped: weak_0_docs (`weak-lensing-shear-docs`, PyAutoGalaxy #366, 2026-04-25)
shipped: [weak_1_simulator.md](../issued/weak_1_simulator.md) (`weak-shear-simulator`, PyAutoLens #473 + autolens_workspace #84, 2026-05-04)
shipped: [weak_2_visualization.md](../issued/weak_2_visualization.md) (`weak-visualization`, PyAutoLens #496 — 5 quiver plotters in `autolens/weak/plot/`)
shipped: [3_fit.md](../issued/3_fit.md) (`weak-fit` — `al.FitWeak` + 4 fit plotters + workspace `scripts/weak/fit.py`)
shipped: `weak-dataset-from-json` follow-up (`al.from_json(WeakDataset)` round-trip fix)

queued (dependency order — 4 is the keystone, 6 is independent):
- [feature/weak/4_modeling.md](../feature/weak/4_modeling.md) — `AnalysisWeak` mirroring the imaging model API + workspace `modeling.py`. Blocks 5, 7, 8.
- [feature/weak/5_likelihood_function.md](../feature/weak/5_likelihood_function.md) — `scripts/weak/likelihood_function.py` in the standard workspace style.
- [feature/weak/6_visualization_profiles.md](../feature/weak/6_visualization_profiles.md) — tangential/cross shear radial profile plotter (γ_t/γ_x binned, cross-shear B-mode null test) + Kaiser-Squires convergence map. Independent of 4.
- [feature/weak/7_real_data.md](../feature/weak/7_real_data.md) — real-data example on Abell 2744 public shear catalog; needs catalog loader + reduced-shear (g = γ/(1−κ)) + Σ_crit scaling. Depends on 4; profits from 6.
- [feature/weak/8_strong_lensing.md](../feature/weak/8_strong_lensing.md) — `scripts/weak/features/strong_lensing/{simulator,fit,modeling}.py` combined SL+WL via summed `AnalysisImaging + AnalysisWeak`. Depends on 4.

Issue steps one at a time as each predecessor nears shipping (no bulk-issuing).

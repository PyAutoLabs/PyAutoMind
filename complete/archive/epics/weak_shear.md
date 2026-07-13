Weak gravitational lensing series — COMPLETE (2026-07-09). Multi-step epic that added `WeakDataset`, simulator, plotters, fit, modeling, likelihood-function tutorial, combined strong+weak analysis, smoke support and a real-data example across PyAutoLens + autolens_workspace. All steps shipped; this tracker is ready to archive.

Science scope: cluster/group-scale weak shear as the large-radius complement to strong lensing — Niemiec et al. 2020 hybrid-Lenstool (arXiv:2002.04635) and Oguri et al. 2012 SGAS (arXiv:1109.2594). Not cosmic shear / galaxy-galaxy lensing.

shipped: weak_0_docs (PyAutoGalaxy #366, 2026-04-25)
shipped: weak_1_simulator (PyAutoLens #473 + workspace #84, 2026-05-04)
shipped: weak_2_visualization (PyAutoLens #496 — 5 quiver plotters)
shipped: 3_fit (`al.FitWeak` + 4 fit plotters + workspace fit.py) + from_json fix
shipped 2026-07-09 (the "home-straight push", one --auto session):
- 4_modeling — `al.AnalysisWeak` + workspace modeling.py (PyAutoLens #580 + workspace #241; issue #579)
- 5_likelihood_function — workspace likelihood guide (workspace #246; issue #245)
- 6_visualization_profiles — tangential/cross shear profile + Kaiser-Squires maps (PyAutoLens #582 + workspace #244; issue #581)
- 8_strong_lensing — combined SL+WL via FactorGraphModel + mixed-graph viz fix (PyAutoLens #587 + workspace #251; issue #247)
- 9_small_datasets — PYAUTO_SMALL_DATASETS catalogue cap (PyAutoArray #366 + PyAutoLens #584; issue #583)
- 7_real_data — catalog IO + reduced shear + real A2744 pyRRG example (PyAutoLens #589 + workspace #253; issue #588)

Follow-ups shipped 2026-07-09 (user-directed "do all of these"): sigma_crit scaling + FitWeak JAX (step 10, PyAutoLens #591 + workspace_test #156; issue #590); FactorGraphModel per-type visualize_combined dispatch (PyAutoFit #1340; issue #1339). Remaining candidate (not queued): metrology-grade A2744 reproduction if the published DR1 shear catalog is sourced (UNCOVER/MAST or author contact).

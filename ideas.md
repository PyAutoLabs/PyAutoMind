- lens_calc_zero_contour_jax autolens workspace guide.







- [from: ep-review-p1-F10] Adaptive/default EP damping: default `delta < 1` (or `DynamicUpdater` as default) so undamped Laplace-only EP cannot silently collapse; consider a damping schedule that tightens as the KL step shrinks.
- [from: ep-review-p5] Structured (block-Gaussian) mean field: allow correlated message blocks over variable groups instead of the fully-factorised q — directly addresses the exactness-vs-modularity trade-off documented for deterministic variables (z ⊥ parents under the current family).
- [from: ep-review-p1] Power EP / alpha-divergence updates: the damped update is already an EMA on natural parameters; fractional (power-EP) updates are a small generalisation and handle heavy-tailed factors better than KL moment matching.
- [from: ep-review-p4] EP health report: aggregate the new ep_history.csv into a per-factor/per-variable traffic-light summary (BAD_PROJECTION rates, oscillation detection, sigma-collapse flags) — the "single point of reference" view graphical_scoping.md limitation 3 asks for.
- [from: ep-review-p3] Warm-start per-factor searches across EP cycles: each optimization_# currently restarts cold; seeding from the previous cycle's samples/posterior would cut the dominant per-cycle wall-time (ties to ep_scoping.md overhead findings).
- [from: ep-review-p1] Audit + document StochasticEPOptimiser (expectation_propagation/stochastic.py, 117 lines) — out of the Phase 1 audit scope, undocumented, untested status unknown.
- [from: ep-review-p1-F7] Evidence-correct EP model comparison: once the log_norm bookkeeping fixes land, validate EP log-evidence against nested-sampling evidence on toy graphs and expose it as a supported feature (currently unusable).
- [from: ep-review-p6] Hierarchical exact updates: Gaussian parent–child HierarchicalFactor updates have closed forms; currently optimised numerically one factor per drawn variable (natural WP5 after PyAutoFit#1338's WP3).
- [from: ep-review] Resumable EP: checkpoint/restore EPMeanField (+ EPHistory) so long multi-dataset fits survive session/HPC walltime boundaries — cosmology use case runs Nautilus-per-factor and would benefit first.
- [from: ep-review] JAX-native Laplace factor fits: autodiff gradients/Hessians for the tilted distribution instead of quasi-Newton with numeric fallbacks — aligns EP with the wider JAX direction and removes the scipy-private line-search dependency (#1332 F9).
- [from: ep-review-p3] HowToFit chapter 3 refresh: align tutorial 5 with the new step-by-step feature example, the diagnostics outputs (#1335), and swap TruncatedGaussianPrior usage once #1331-04/F6 fixes land (the flagship tutorial currently runs on the buggy truncated path).
- [from: research jax-autodiff-gradients-audit (#87) · delaunay probe] Delaunay frozen-triangulation gradients: wrap `_jax_delaunay_tables` (PyAutoArray delaunay.py pure_callback) in `jax.custom_jvp` with a zero rule so `value_and_grad` stops hard-erroring, then FD-validate the frozen-triangulation gradients like the rectangular mesh; connectivity is piecewise-constant so the zero rule is the correct a.e. derivative. Coordinate with the nnls-solver-optimization claim on PyAutoArray.
- [from: research jax-autodiff-gradients-audit (#87) · source_plane probe] Fix `Grid2DIrregular.grid_2d_via_deflection_grid_from` xp propagation so the point-source likelihood's forward `jax.jit` works (gradients already work; the jit gap blocks fast batched sampling).
- [from: research jax-autodiff-gradients-audit (#87) · interferometer probe] Interferometer MGE FD correctness test: probe is 9/9 finite but no autodiff-vs-finite-difference validation exists for the visibility-space likelihood — add `jax_grad/interferometer_mge.py` on the pattern of the imaging suite.
- [from: research jax-autodiff-gradients-audit (#87) · validated-likelihood set] NUTS/HMC sampler trial on the FD-validated likelihoods (weak lensing, point-source source-plane, imaging with RectangularUniform or parametric sources) via the sampler pipeline — gradients are now certified correct end-to-end, removing the main risk that stalled gradient-based inference.
- [from: PyAutoBuild/to_do_list, evacuated 2026-07-10 by pyautoscientist-phase1] Test different numpy, scipy, scikit-learn, threadpoolctl, joblib versions.
- [from: PyAutoBuild/to_do_list] Tests using full dynesty runs with inversion, BrightnessImageNN pix, with parallel processing.
- [from: PyAutoBuild/to_do_list] Workspace tagging.
- [from: PyAutoBuild/to_do_list] Remove annoying report.log and root.log once and for all.

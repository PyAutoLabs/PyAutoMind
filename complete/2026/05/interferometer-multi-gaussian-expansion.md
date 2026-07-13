## interferometer-multi-gaussian-expansion
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/166
- completed: 2026-05-17
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/168
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/77
- notes: Built scripts/interferometer/features/multi_gaussian_expansion/ in both autolens_workspace (modeling, fit, likelihood_function, slam + README + __init__) and autogalaxy_workspace (modeling, fit, likelihood_function + README + __init__). Key autolens role swap explicitly explained: imaging MGE fits the lens galaxy bulge, but for interferometer the lens light is omitted (no detection in mm/sub-mm) so the MGE is applied to the source galaxy. autolens slam.py mirrors interferometer/features/pixelization/slam.py with SOURCE LP mge_model_from total_gaussians bumped from 5 to 20; pixelized stages identical. autogalaxy uses single-galaxy MGE bulge (no role swap — same as imaging). All scripts use TransformerNUFFT (nufftax) for the per-iteration NUFFT of every Gaussian inside the JAX jit/vmap pipeline. likelihood_function.py walkthroughs reproduce FitInterferometer.figure_of_merit to 3 decimal places — the small mismatch likely from multiple valid positive-only sparse solutions in degenerate Gaussian bases. Both lhfn scripts nicely demonstrate positive-negative solver ringing (autogalaxy returns ±10^15 intensities) vs positive-only solver collapsing to sparse 2-Gaussian solutions — visual teaching moment. Phase 1 sanity sweep of imaging MGE scripts (typos: peforms, algabra, descomposed, double-backtick `Gaussian``, start.here.py, unphysicag×2, physicag, PyAutoGalaxys, lp_Linear) bundled into PRs. SLaM smoke ran all 4 stages in ~30s under PYAUTO_TEST_MODE=2. Tracker now 3 shipped / 6 outstanding. Future audit hint: autogalaxy imaging MGE files had clustered typos (unphysicag/physicag/PyAutoGalaxys) suggesting a bad find/replace was applied at some point — worth a broader sweep across autogalaxy MGE-adjacent scripts.

## Original prompt

The imaging `features/multi_gaussian_expansion` example needs reviewing before adapting to interferometer.

Once the imaging version is in good shape, adapt it to the interferometer context in
`scripts/interferometer/features/multi_gaussian_expansion/` for **both** `autolens_workspace` and
`autogalaxy_workspace`.

Multi-Gaussian Expansion (MGE) decomposes a galaxy's light into many Gaussian components — until
recently infeasible against visibilities because each Gaussian required its own Fourier transform
per iteration. With nufftax (point to its GitHub and credit it), the full MGE basis is transformed
quickly on GPU, so MGE fits to interferometer data are now practical even with millions of
visibilities. The script should mirror the imaging API explanation and call out the nufftax-enabled
performance shift.

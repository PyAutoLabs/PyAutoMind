## potential-correction-port
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/618
- completed: 2026-07-17
- library-pr: PyAutoArray#390, PyAutoGalaxy#505, PyAutoLens#621, PyAutoLens#622 (all MERGED)
- workspace-pr: autolens_workspace#284, autolens_workspace_test#176 (both MERGED)
- summary: Ported caoxiaoyue/lensing_potential_correction (Cao et al. 2025) into the stack as first-class source: PyAutoArray masked-grid derivative operators + CurvatureMask/FourthOrderMask regularizations (parity-certified bit-identical vs upstream), PyAutoGalaxy Input pixelized mass profiles + numpy-FFT GaussianRandomField, the al.pc subpackage (dpsi mesh, FitDpsiImaging, joint FitDpsiSrcImaging, analyses, viz, docs), xp-API dense kernels (al.pc.dense_util — numpy default, jax.numpy/jit verified identical) and the IterFitDpsiSrcImaging LM engine. Workspace layer: guides/advanced/potential_correction.py, features/potential_correction/likelihood_function.py (hand-computed evidence ≡ fit to 8 decimals), wst subhalo_recovery.py + jax_likelihood_functions/imaging/potential_correction.py (smoke-wired). All materials cite Cao et al. 2025 via caoxiaoyue/potential_correction_paper.
- phase-5 verdict: the "unknown bug" preventing the Vegetti-style iterative reconstruction = (1) split_cross_from NaN (percentile over unbounded-Voronoi -1 sentinels → NaN gradient arms in the iterative loop's source-gradient path; FIXED + regression test), (2) coarse-mesh box-search negative-index wrap → KeyError (FIXED + test), (3) demo-2 stored hyper-params (Matern52 c=803465.55 s=0.4497, tuned on pre-fix code) miscalibrated — iterative at them corr 0.18/1.82" vs corr 0.73/0.21" at c=2000/s=4, with the Laplace evidence preferring the recovering solution (1.6901e4 > 1.6598e4) → evidence sampling self-corrects. Iterative engine SOUND; Powell/Vegetti-style reconstruction (B1938+666 papers) reproduces end-to-end.
- traps: al.Kernel2D GONE → al.Convolver.from_gaussian; aa.Settings has no use_w_tilde; al.mesh.Rectangular → RectangularUniform; AdaptImages in autogalaxy.analysis.adapt_images; dense@sparse returns np.matrix (np.asarray at seams); CurvatureMask never localizes the test subhalo at any coefficient — MaternKernel nu=2.5 required (Cao's central claim, reproduced); source of truth was the for_qiuhan_PT_jax.tar tree (API-modern + iterative/jax_ops), NOT the GitHub repo.
- follow-up: interferometer support (al.pc is imaging-only) — draft/feature/autolens/potential_correction_interferometer.md; optional evidence-sampled hyper-param demo run; B1938-scale sensitivity push.

## Original prompt

# Claude Development Prompt: Port lensing_potential_correction into the PyAuto stack

Type: feature
Target: PyAutoLens
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised

## Original request (verbatim)

> This is an implmeentation of the potential corrections, which supports
> PyAutoLens, can you take this and incorporate it proeprly into the PyAuto
> ecosystem source code:
> https://github.com/caoxiaoyue/lensing_potential_correction . It uses a lot
> of linear algebra, so maybe belongs in the autoarray inversion module, but
> its also very lensing specific so could go further down. For now, dont
> worry about JAX, we have a JAX code whichw e can bring in in a future PR,
> or maybe I'll just ask you to do it later. Also make sure docs and other
> materials cite this properly
> https://github.com/caoxiaoyue/potential_correction_paper.

## Goal

Incorporate Xiaoyue Cao's `potential_correction` package (the gravitational-
imaging technique: pixelised corrections dpsi to the lensing potential,
reconstructed jointly with the pixelised source by maximising Bayesian
evidence, Matern-family regularisation) into the PyAuto libraries proper,
replacing its wrapper-over-2024.1.27.4 status with first-class, tested,
maintained source code on the current API.

## Constraints and notes

- NumPy/numba implementation only in this PR — the JAX port is a known
  follow-up (external JAX code exists and will be brought in later).
- The external code targets autolens 2024.1.27.4; the port must modernise to
  the current API (Tracer construction, over-sampling instead of
  SettingsImaging sub_size, aa.decorators, current mask/grid attributes).
- autoarray already ships Gaussian/Exponential/Matern kernel regularizations
  (inversion/regularization/*_kernel.py) — reuse, do not duplicate Cao's
  covariance_reg equivalents.
- Do not adopt the external repo's heavy optional deps (GPy, multiprocess,
  powerbox, numba-scipy) as library requirements.
- Layering: generic masked-grid sparse differential operators and any new
  generic regularizations belong in autoarray's inversion layer; the dpsi
  mesh/pairing, joint source+dpsi fit, Analysis classes and visualization are
  lensing-specific and belong in PyAutoLens (cf. the `autolens/weak`
  subpackage precedent); pixelised Input-deflections/potential mass profiles
  belong in PyAutoGalaxy.
- Citation: docs, docstrings and README materials must cite Cao et al. (2025)
  via https://github.com/caoxiaoyue/potential_correction_paper and credit
  https://github.com/caoxiaoyue/lensing_potential_correction as the origin.

## Acceptance criteria

- Potential-correction fit (dpsi-only and joint source+dpsi) runnable from
  the installed stack on current main, with unit tests (numpy-only, no JAX).
- No duplicated regularization/operator code between autoarray and the port.
- Citations present in the new modules' docstrings and the relevant docs.

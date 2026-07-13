## fft-mixed-precision-fix
- completed: 2026-05-08
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/302
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/38
- repos: PyAutoArray, autogalaxy_workspace_test
- notes: |
    Fixed a real net-loss in `al.Settings(use_mixed_precision=True)` on
    consumer GPUs: `Convolver.convolved_image_from` previously force-cast
    inputs to fp64 then narrowed the result, paying for fp64 FFT plus an
    extra cast. Light-profile path now runs end-to-end complex64 with the
    kernel pre-cached on `ConvolverState.fft_kernel_c64`.

    Headline result on RTX 2060 + i9-10885H (mge.py HST regression):
    GPU mp full pipeline 47 -> 19.6 ms; GPU mp vmap (production sampler
    hot path) 17.4 -> 8.9 ms (49% faster). CPU vmap unchanged-to-slightly-
    faster; CPU single-JIT regresses ~17% but production samplers use vmap.
    Delta log-likelihood ≈ 2.2e-3 absolute, far below chi^2 noise floor
    (sigma ≈ 175 for N=15k pixels).

    `convolved_mapping_matrix_from` intentionally keeps its complex128
    kernel multiply: full fp32 in that path drifted `figure_of_merit` by
    ~10 units (1.9% relative) on the autolens_workspace_test delaunay_mge
    regression (K=780 source mesh). Pixelization NNLS / log-determinant
    needs fp64. Codified the asymmetry in code comments, Settings
    docstring, and a new jax_assertion at
    autogalaxy_workspace_test/scripts/jax_assertions/convolver_mixed_precision.py.

    23/23 JAX likelihood-function integration tests pass across autolens +
    autogalaxy, imaging + interferometer, MGE + rectangular + Delaunay.

    Two follow-ups filed:
    - PyAutoPrompt/autoarray/nnls_gpu_bottleneck.md — GPU-NNLS bottleneck
      (jaxnnls is PDIP with MAX_ITER=50; Cholesky fast-path rejected
      because empirical positivity-hit-rate during sampling is low and
      lax.cond under vmap evaluates both branches).
    - PyAutoPrompt/autolens_workspace_developer/mge_jit_regression_rebaseline.md —
      mge.py's hardcoded EXPECTED_LOG_LIKELIHOOD_HST drifted from 27379.39
      to 27542.08 due to upstream changes (independent of this fix).

## numba-cpu-kernel-cdf-fast-path
- issue: none (draft prompt, never issued)
- completed: 2026-08-28 (superseded; closed at the numba-cpu-likelihood epic close-out)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/458 (MERGED 2026-08-21 — windowed numba kernel-CDF forward transform, numpy branch, ~3x, parity 1e-13)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/462 (MERGED 2026-08-21 — rectangular adaptive mesh split: Bilinear = rank-CDF, RTU = kernel-CDF)
- epic: numba-cpu-likelihood — phase 2a
- verdict: the phase's lever no longer exists on the CPU path users run. The 49-88% "sparse triplets" cost
  the 2026-08-20 hunt attributed to the kernel-CDF transform belonged to the pre-split adaptive
  rectangular mesh. #462 made the default rectangular meshes (`RectangularBilinearAdaptDensity` /
  `RectangularBilinearAdaptImage`, used by every `cpu_fast_modeling.py`) rank-CDF — a sort-based transform
  with no erf sum — and #458 gave the remaining kernel-CDF (RTU) path the windowed numba kernel this
  prompt asked for (`_kernel_cdf_dim_windowed`, `rectangular.py`). Decision (user, 2026-08-28): the RTU /
  kernel-CDF meshes are a GPU (JAX) concern; their CPU run time is not a target.
- original prompt: `draft/feature/autoarray/numba_cpu_likelihood_kernel_cdf_fast_path.md` (retired with this
  record; hunt verdict and legacy-history anchors preserved in git at the commit before this one).
- affected-repos:
  - PyAutoArray

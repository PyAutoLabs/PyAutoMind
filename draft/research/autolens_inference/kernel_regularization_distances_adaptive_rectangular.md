# Kernel regularization on adaptive rectangular meshes: stretched-lattice vs true source-plane distances

Type: research
Target: autolens_inference
Repos:
- @autolens_inference
- @PyAutoArray
Themes:
- pixelization
- regularization
Epic: cluster-strong-lensing
Difficulty: large
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Filed: 2026-10-30
Witness: A results note in autolens_inference compares, over several simulated lenses with known truth and full end-to-end lens-model fits (free mass model, regularization hyper-parameters fitted), the Bayesian evidence, mass-parameter bias and coverage, source-reconstruction error and magnification error of MaternKernel / GaussianKernel (and MaternSparse where applicable) on adaptive rectangular meshes with distances measured on (a) the stretched lattice (current behaviour) and (b) the true source-plane pixel centres, with Delaunay + the same kernels as a reference, and ends in a recommendation (keep lattice / switch / expose as an option) that a human decides.
Review-minutes: 30
Unattended: no

## Original request (human, 2026-10-30)

> ok intake an issue to investigate this thorough using end-to-end lens modeling runs

## Context

Found during PyAutoArray#667 (adaptive rectangular meshes reported a uniform overlay as their pixel positions;
arc phase 4e blocker for autolens_workspace#605). Kernel regularizations (`ExponentialKernel`, `GaussianKernel`,
`MaternKernel`, `MaternAdaptKernel`) build their covariance from pixel-to-pixel distances. On an adaptive
rectangular mesh those distances have always been measured on the regular lattice (the uniform overlay = the
mesh's stretched CDF coordinates), not on the true source-plane pixel centres; Delaunay meshes use true
source-plane distances. On the lattice a kernel's `scale` effectively shrinks in the source plane where the mesh
packs pixels (high magnification), i.e. a resolution-adaptive, non-stationary prior.

Human ruling 2026-10-30: PyAutoArray#667 keeps the lattice **explicitly** (new `regularization_mesh_grid`
attribute; likelihoods unchanged) and fixes only positions (`source_plane_mesh_grid`, CSV, `max_pixel_centre`,
plot zoom, potential correction). The human's prior was that true distances "logically" should be right, as for
Delaunay; this study settles it.

## Evidence so far (one lens, fixed true mass model — NOT end-to-end)

autolens_workspace `imaging/simple__no_lens_light` (SersicCore source, effective radius 0.1″, true tracer, extra
galaxy noise-scaled, 28×28 `RectangularBilinearAdaptDensity`, true magnification 34.92), regularization
(scale, coefficient) optimised separately per distance choice (Nelder–Mead, 3 starts):

| kernel | distances | best scale / coeff | log evidence | mu error |
|---|---|---|---|---|
| Matern nu=0.5 | lattice | 1.15 / 3.6 | 1923.5 | -6.4% |
| Matern nu=0.5 | true centres | 0.108 / 13.8 | 1812.1 | -5.3% |
| Gaussian | lattice | 0.216 / 2.5 | 2105.3 | -4.9% |
| Gaussian | true centres | 0.069 / 8.9 | 1758.6 | -4.5% |

At matched (scale, coeff) true distances usually won; tuned, the lattice wins evidence by 111 / 347 while true
distances are ~1 point better on magnification. Gaussian with true distances collapses at scale >= 0.2
(log evidence to -13,000: near-singular covariance on densely packed central nodes). Scripts and raw outputs:
`/mnt/c/Users/Jammy/Workspace/Science/scratch/kernel_reg_distances_2026-10-30/` (`regopt.py` + `regopt_results.txt`
= the table; `regexp.py` + `regexp_grid_results.txt` = the matched-grid scan; they monkeypatch the pre-#667 mapper,
run from autolens_workspace root). After #667 the switch is one line: return `mesh_geometry.node_centres` instead
of the lattice from `InterpolatorRectangular.regularization_mesh_grid`.

## Questions

1. Over several lenses (compact and extended sources, different magnifications, imaging + interferometer, a
   multi-component source), with full end-to-end fits (free mass model, fitted regularization hyper-parameters,
   the standard SLaM source-pix pipeline), does the evidence preference for the lattice persist?
2. Does either choice bias mass parameters or change their posterior widths / coverage? Source reconstruction
   error and magnification error against truth?
3. Is the lattice's advantage just a resolution-adaptive prior? If so, compare against a deliberately
   non-stationary kernel on true distances (e.g. scale proportional to local pixel spacing) and against the
   adaptive-brightness regularizations.
4. Conditioning: how often do true-distance kernels hit near-singular covariance (jitter needed, log-det
   stability, JAX gradient health)? Same check on Delaunay as a reference.
5. Cost: any runtime / JAX compile difference.

## Work

1. Add the true-distance option behind a private switch for the study only (no library API until the decision).
2. Design the simulation suite and fit configurations in autolens_inference (reuse its campaign/results layout;
   CPU runs on RAL per its HPC rules, never bulk CPU on the `gpu` partition).
3. Run, ingest, write the results note with the comparison tables and a recommendation; human decides.
4. If the decision is "switch" or "option", file the library change as its own task (it changes likelihoods for
   kernel-regularized adaptive-rectangular fits and needs a release note).

## rectangular-kernel-cdf-mesh
- completed: 2026-07-10
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/373 (closed)
- prs: PyAutoArray#374 + autolens_workspace_test#161 + autolens_workspace_developer#90 (all merged 2026-07-10, human-directed, order #375→#374→workspace)
- summary: kernel-density CDF meshes RectangularKernelAdapt{Density,Image} (Enzi RTU) shipped opt-in — strict FD certified on ALL params in every config incl. the two dead corners (imaging os_pix=1 bw=0.1, interferometer sparse production shape); FoM parity beats/2.7e-5/6.3e-4/3.9e-5; FD-step-sweep harness added to jax_grad/util.py (solver branch flips <1e-15 wide, ΔLL 1.6e-3–14, pre-existing); rect-adapt #372/#375 folded in + verified visually (kernel_cdf_alignment.py, node containment + mapper-faithfulness 0.01–0.07 cells); stash@{0} rejected + parked.md retired; 893 library tests green
- followups: kernel-forward chunking + solver branch-flip investigation (starting 2026-07-10); sampler trials (unblocked, unfiled)

## Original prompt

# Kernel-density CDF transform for the adaptive rectangular mesh (differentiable everywhere)

Type: feature
Target: autoarray
Repos:
- PyAutoArray
- autolens_workspace_test
- autolens_workspace_developer
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Replace the empirical point-rank CDF in the adaptive rectangular mesh with a smooth
kernel-density CDF (the Enzi et al. arXiv:2606.30620 RTU formulation) so the mesh
carries correct smooth mass/shear gradients in every configuration — imaging at any
pixelization over-sampling and the interferometer sparse path (which has no
over-sampling and today has zero usable gradients).

Original request (verbatim): "it sounds like you think we can improve the rectangular
gradient method across all use cases? explain how [...]" → recommendation approved:
kernel-CDF leapfrog, one focused task, "drop the nuts stuff for now I only care that
the jax gradient workspace test script shows grad all works and can work on samples
down the line."

## Background (from the 2026-07-09 JAX gradient audit, autolens_workspace_developer#87)

- The linear rank-CDF (`create_transforms` in
  `PyAutoArray/autoarray/inversion/mesh/interpolator/rectangular.py`) makes the
  likelihood exactly piecewise-constant in mass/shear whenever interp queries
  coincide with knots: imaging os_pix=1 and the interferometer sparse path
  (`jax_grad/interferometer.py` variant B documents the staircase). At os_pix=4
  gradients live but every rank swap leaves a micro-kink (~1-3% FD contamination).
- Prior attempt: `RectangularSplineAdapt{Density,Image}` (PyAutoArray PR #289,
  2026-04-22, opt-in, built for gradient samplers). Measured 2026-07-09: breaks the
  rank invariance (AD live on all 14 params at os_pix=1) BUT eager-vs-JIT LL gap
  ~15 and erratic FD (noisy surface — #289's shipped "oscillations" limitation).
  Suspects: `_enforce_strict_monotone` eps-jitter, deg-11 polyfit conditioning,
  Hermite inversion table. Do not build on this chain; keep the spline meshes
  untouched/opt-in.
- A 727-line jax-friendly spline-interpolator refactor is PARKED in PyAutoArray
  `stash@{0}` (parked.md `rectangular-spline-cdf`, 2026-05-08).

## Task

1. **Preamble**: inspect PyAutoArray `stash@{0}` — salvage anything useful, then
   retire the `parked.md` entry either way (keep the stash until a decision is
   recorded on the issue).
2. Implement the kernel-density CDF transform as a new opt-in mesh variant (e.g.
   `RectangularKernelAdaptDensity` / `...AdaptImage`), slotting into the existing
   `transform`/`inv_transform` machinery: per axis
   `F(x) = sum_i w_i * Phi((x - x_i)/h)` evaluated on a small fixed knot grid
   (K ~ 64), inverse via interpolation on the same grid. Strictly monotone by
   construction (no jitter hack), C-infinity in queries AND point positions,
   duplicate-safe (no 1/Delta-knot terms). Weight-map variant uses `w_i` from the
   adapt image. Bandwidth `h` defaults tied to mesh resolution; expose as a mesh
   kwarg.
3. **Certification is the success criterion** (no sampler work in this task):
   - Extend `autolens_workspace_test/scripts/jax_grad/imaging_pixelization.py`
     with kernel-mesh variants at os_pix=1 AND os_pix=4: strict FD assertions on
     ALL parameters (mass/shear included) using the existing `util.py` harness —
     the os_pix=1 variant must NOT be a staircase (that is the point).
   - Extend `autolens_workspace_test/scripts/jax_grad/interferometer.py` with the
     kernel mesh on the sparse-operator path: strict FD on all mass/shear params.
   - Eager-vs-JIT consistency (`util.assert_eager_jit_consistent`) must hold on
     every variant.
   - Fit-quality parity: eager figure_of_merit on the jax_test config within a few
     e-4 relative of the linear AdaptDensity/AdaptImage meshes (mesh geometry
     changes slightly; reconstruction quality must not degrade).
   - Update `autolens_workspace_developer/jax_profiling/gradient/README.md` rows +
     the staircase-section implications once certified.
4. Sampler trials (NUTS/HMC) are explicitly OUT of scope — future task once the
   jax_grad scripts are green.

## Constraints

- PyAutoArray is claimed by `nnls-solver-optimization` (active.md) at time of
  filing — start when the claim releases or coordinate explicitly (different
  files, adjacent territory).
- Spline meshes (PR #289) stay as-is; no deletion/refactor of them in this task.
- Library unit tests numpy-only per repo rules; all JAX validation through the
  workspace_test jax_grad scripts.

<!-- formalised 2026-07-09 from ideas.md bullet [from: research jax-autodiff-gradients-audit (#87) · arXiv:2606.30620 + PyAutoArray#289 archaeology], user-directed (NUTS dropped from scope) -->

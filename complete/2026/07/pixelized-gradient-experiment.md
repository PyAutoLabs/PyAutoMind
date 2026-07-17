# Pixelized gradient-sampler experiment

- Issue: autolens_workspace_developer#100 (closed) · PR #102 (merged 2026-07-17)
- Branch: feature/pixelized-gradient-experiment

Do the multi-start gradient MAP searches work on a pixelized source? Gradients: YES —
kernel-CDF mesh certified on the A100 (FD ~1e-6, all mass/shear params). Enablers shipped
along the way: PyAutoFit#1374 batch_size (lax.map tiling; unbatched 16-start pix jvp = 58 GiB).
Nautilus baseline (job 330513, converged: 27,840 calls, N_eff 1233, logZ +17345) set the
honest bar: max logL +17419 at r_E 1.31 — itself 8k nats under the FD probe's truth point,
i.e. the source-degeneracy mode dominates at n_live=100. The search question resolved under
#101: the adam failure (-39888, 0/16) was trajectory NaN mortality, not tuning. Key lore:
the 1h10m input_reduce_fusion compile is one-time (JAX_COMPILATION_CACHE_DIR); only
completed executables cache; slack 0.3 r_E basin tol over-flags — use the converged-sampler
logL as the bar.

## Original prompt

# Pixelized gradient-sampler experiment — can MultiStartAdam/ADABelief/Lion work for pix?

Type: experiment
Target: autolens_workspace_developer
Repos:
- @autolens_workspace_developer
Difficulty: large
Autonomy: supervised
Priority: normal
Status: issued

Research question: do the newly-promoted multi-start gradient MAP optimizers
(af.MultiStartAdam / MultiStartADABelief / MultiStartLion, Fit#1369) work on a
PIXELIZED source reconstruction, not just the MGE likelihood the benchmark used?

Setup (searches_minimal/, extending the MGE benchmark harness):
- Model = SLaM SOURCE_PIX[1] style: lens MGE linear light with FIXED non-linear
  geometry; lens mass (Isothermal + ExternalShear) FREE; source =
  RectangularSplineAdaptImage (differentiable spline mesh) + adaptive
  regularization (al.reg.Adapt); regularization coefficient FREE. Free non-linear
  params ~= mass + shear + reg (~7-D). Adapt image bootstrapped from a quick
  RectangularAdaptDensity+Constant fit (no adapt image needed), mirroring SLaM.
- FD feasibility gate FIRST (probe_grad_pix.py): reverse-mode jax.grad of the
  spline-pixelized log-evidence, FD-cross-checked. If FAIL_FD_MISMATCH, that IS
  the answer — stop, report, no A100 burn.
- Samplers: af.MultiStartAdam/ADABelief/Lion + af.Nautilus baseline.
- Runs: local CPU smoke, then A100 on RAL (euclid_jump pipeline).
- Deliverable: findings doc (do gradient MAP optimizers recover the mass basin
  with a pixelized source vs Nautilus?).

Decisions (human, 2026-07-14): SplineAdaptImage + adaptive reg; mass+reg free /
light fixed. Checkpoint after the FD probe before samplers/A100.

<!-- research spun off the multi-start gradient promotion; grad harness = searches_minimal -->

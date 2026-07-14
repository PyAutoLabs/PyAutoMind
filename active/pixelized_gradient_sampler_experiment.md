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

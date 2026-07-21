# JAX gradient family: light-profile traceback + all-zero MGE/pixelization gradients (parked NEEDS_FIX)

Type: bug
Target: autoarray
Repos:
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

The `jax_grad/*` family: gradients either raise or come back all-zeros — the known "needs custom_jvp"
lineage ([[project_jax_gradient_audit_shipped]]: smooth likelihoods FD-certified; Delaunay/pix need
custom_jvp).

Affected in autolens_workspace_test (remove NEEDS_FIX from config/build/no_run.yaml once green):
- `jax_grad/imaging_lp` — JAX traceback in light-profile gradient
- `jax_grad/imaging_mge` — AssertionError: Gradient is all zeros (MGE)
- `jax_grad/imaging_pixelization` — Gradient is all zeros (added 2026-07-21; pixelization; the
  PYAUTO_SMALL_DATASETS override is already in env_vars.yaml so it runs at full data)

First step: reproduce imaging_mge on clean main (A100/GPU or CPU fp64) and confirm whether the
zero-gradient is a missing custom_jvp on the mesh/mapper or a broken pytree registration. imaging_lp
(a smooth profile) raising is likely a separate xp-threading gap. May split lp vs mge/pix.

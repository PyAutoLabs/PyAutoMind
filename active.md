# Active Tasks

## profiles-jit-powerlaw-exact-zero-atol
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/291
- issued: 2026-09-04
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/profiles-jit-powerlaw-exact-zero-atol
- repos:
  - autolens_workspace_test: feature/profiles-jit-powerlaw-exact-zero-atol
- summary: |
    Release Integrate run 33847995194 fails scripts/misc/profiles_jit.py on
    mp.PowerLaw deflections: numpy returns exactly 0.0 on-axis (PyAutoGalaxy#598
    exact unit-vector transform), JAX returns 1.2e-16, and the check is
    rtol-only. Add atol=1e-12 on the mp.PowerLaw checks, mirroring
    mp.ExternalPotential.

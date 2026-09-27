# jax.grad NaN at exactly zero components (ExternalShear, multipole_comps, ell_comps)

Type: bug
Target: @PyAutoGalaxy

## Original request (verbatim)

fix this: - jax.grad returns NaN at exactly zero for ExternalShear, the multipole components and ell_comps. So a gradient search starting at prior medians of 0 gets NaN gradients. The benchmark centres those priors on 1e-3 to avoid it.

## Witness (reproduced 2026-09-27 on PyAutoGalaxy main, fp64)

jax.grad of a random-weighted sum of deflections w.r.t. the (c0, c1) component pair:

- ExternalShear (0,0) -> [nan nan]; (1e-6,0) -> [0.1816 0.4004] == central FD at 0
- PowerLawMultipole m=4 (0,0) -> [nan nan]; (1e-6,0) -> [0.5404 0.0910] == central FD at 0
- Isothermal ell_comps (0,0) -> [nan nan]

Cause: `sqrt(c0**2 + c1**2)` in the `autogalaxy/convert.py` polar conversions has an
infinite/NaN derivative at the origin (the `arctan2` already has a forward-value guard).

Origin: carried intake note from the point-source source-plane campaign (active.md).

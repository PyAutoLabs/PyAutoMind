## Summary

`jax.grad` returned NaN at exactly zero for `ExternalShear`, `multipole_comps` and `ell_comps`. Fixed in PyAutoGalaxy #634 (merge c7fc595b), with companion PyAutoLens #754 (merge 897c2f76), both merged 2026-09-27.

- **NaN fix:** `convert._nudge_off_origin` moves the x-component by 1e-8 at the exact origin. It acts on traced JAX values only, via `lax.select`, so NumPy results and jitted graphs with constant components stay bit-identical and the static_lattice tie pin is preserved.
- **Isothermal (human-approved scope extension):** the q <= 0.99999 clamp is removed and replaced by a series form in s² = 1 - q² near q -> 1. `Isothermal(0,0)` now equals `IsothermalSph`, and the `ell_comps` gradient at 0 equals finite differences; with the NaN fix alone it would have been -267 against a true -0.53.
- **PyAutoLens #754:** 6 tests repinned. They had pinned the clamp's artefact (q = 0.99999 at angle 0).
- **Tests:** galaxy 1258 passed; lens 762 passed, 1 xfailed (CI identical). The workspace_test parity scripts `tracer_jax.py` and `profiles_jit.py` pass. Heart YELLOW was acknowledged at ship (unrelated manifest drift and no release rehearsal).

## Pending release

- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/634
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/754

## Follow-ups

- `draft/bug/autogalaxy/q_clamp_and_bare_sqrt_ellipticity_grad_sweep.md`: the same class of clamp in dPIE, chameleon and MGE/Gaussian, plus bare sqrt sites in NFW, dPIE and geometry_profiles
- `draft/feature/autolens_inference/drop_1e3_prior_centring_after_631.md`: drop the benchmark's 1e-3 prior centring once #634 is released
- Lesson: jitted graphs can shift by 1 ULP when any op is added, even on constants. Point-solver tie pins caught this, so the nudge had to become tracer-only `lax.select`.

## Original prompt

# jax.grad NaN at exactly zero components (ExternalShear, multipole_comps, ell_comps)

Type: bug
Target: @PyAutoGalaxy
Issued: 2026-09-27

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

# Give the JAX PowerLaw deflections branch the same exact unit-vector transform as the numpy branch (#598)

Type: bug
Target: autogalaxy
Repos:
- @PyAutoGalaxy
- @autolens_workspace_test
Themes:
- jax
- mass-profiles
Difficulty: small
Autonomy: safe
Priority: low
Status: draft
Consequence: judge
Review-minutes: 10
Filed: 2026-09-04

## Symptom

`autogalaxy/profiles/mass/total/power_law.py` rotates the deflection vector back
to the reference frame by **two different routes**:

- **numpy** (`:213-216`) — the exact unit-vector transform added by
  PyAutoGalaxy#598 (`8aefe5a6`); on-axis grid points come back as exactly `0.0`.
- **JAX** (`:201-206`) — still `arctan2` / `cos` / `sin`; the same on-axis point
  comes back as `1.2e-16`.

Both are correct to one ulp, but the two paths are not bit-identical where the
numpy path is now exactly zero.

## Why it matters (how it surfaced)

`@autolens_workspace_test/scripts/misc/profiles_jit.py` compares the numpy and
JAX paths with `rtol`-only tolerances, so `1.2e-16` against an exact `0.0` is an
*infinite* relative error. It failed PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33847995194. That script
was patched with `atol=1e-12` on the `mp.PowerLaw` checks (mirroring
`mp.ExternalPotential`) — a tolerance, not a fix. The asymmetry itself is still
here.

## Task

Apply the same exact unit-vector transform on the JAX branch as on the numpy
branch, so on-axis deflections are exactly `0` on both paths.

## Acceptance

- Numpy and JAX PowerLaw deflections agree bit-for-bit at on-axis points.
- No measurable JAX/JIT cost regression (the transform is a couple of ops).
- Existing deflection pins unchanged (the numpy path must not move at all).
- Optional once landed: the `atol=1e-12` on the `mp.PowerLaw` calls in
  `profiles_jit.py` could be dropped again — but only with a green run to prove it.

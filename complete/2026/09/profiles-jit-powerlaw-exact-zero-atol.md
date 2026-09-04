# profiles-jit-powerlaw-exact-zero-atol

`atol=1e-12` on the `mp.PowerLaw` checks in `scripts/misc/profiles_jit.py`, so a
one-ulp JAX value compared against an exact numpy `0.0` stops failing an
rtol-only assertion.

- Issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/291 (closed)
- Workspace PR: https://github.com/PyAutoLabs/autolens_workspace_test/pull/292 — MERGED (`72de86c3`)
- corrective-red: the PR was opened while Heart read RED — release validation
  FAILED at stage `integrate`, for the exact failure this PR fixes. Authorized
  on the issue above.

## What shipped

`scripts/misc/profiles_jit.py` passes `atol=1e-12` on both `mp.PowerLaw`
`check_profile_method` calls (irregular + uniform), mirroring the
`mp.ExternalPotential` precedent already in the file, with a comment naming
PyAutoGalaxy#598 so the next reader does not re-diagnose it. `rtol=1e-5` is
unchanged everywhere and no other profile was touched.

## Why

PyAutoHeart's Release Integrate run 33847995194 failed
`mp.PowerLaw.deflections_yx_2d_from (uniform)`: numpy returns exactly `0.0`
on-axis since PyAutoGalaxy `8aefe5a6` (PyAutoGalaxy#598) gave the numpy branch an
exact unit-vector transform, while the JAX branch still rotates via
`arctan2`/`cos`/`sin` and returns `1.2e-16`. With `atol=0.0` that is an
*infinite* relative error; the largest absolute violation is 2.2e-16 — one ulp.
Both paths are correct, so this was a machine-epsilon artefact, not a regression.

## Verification

`scripts/misc/profiles_jit.py` exits 0 locally under the smoke-profile recipe
(failing identically to CI before the change). CI on head `f32e21b7`: Smoke Tests
(pull_request) completed/success on all three jobs — changes, smoke 3.12,
smoke 3.13. `mergeStateStatus` CLEAN.

## Follow-up (still open)

The underlying asymmetry is in the library: the JAX PowerLaw deflections branch
should get the same exact unit-vector transform as the numpy branch. Filed as
`draft/bug/autogalaxy/jax_power_law_deflections_exact_unit_vector_transform.md`
— not covered by this merge.

## Original prompt

# `misc/profiles_jit.py`: `mp.PowerLaw` deflections fail on an exact-zero on-axis point (rtol-only check)

Type: bug
Target: autolens_workspace_test
Repos:
- @autolens_workspace_test
Themes:
- jax
- mass-profiles
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 5
Unattended: ready
Filed: 2026-09-04
Issued: 2026-09-04

## The failure

PyAutoHeart's Release Integrate run
https://github.com/PyAutoLabs/PyAutoHeart/actions/runs/33847995194 fails
`@autolens_workspace_test/scripts/misc/profiles_jit.py`:

```
Not equal to tolerance rtol=1e-05, atol=0
mp.PowerLaw.deflections_yx_2d_from (uniform): numpy vs jax (jit) mismatch
Mismatched elements: 6 / 50 (12%)
Max absolute difference among violations: 2.18507483e-16
Max relative difference among violations: inf
[2, 1]: 1.2117523062002813e-16 (ACTUAL=jax), 0.0 (DESIRED=numpy)
```

## Cause — a machine-epsilon artefact, not a regression

PyAutoGalaxy commit `8aefe5a6` (PyAutoGalaxy#598) gave the **numpy** PowerLaw
deflections an exact unit-vector transform
(`autogalaxy/profiles/mass/total/power_law.py:213-216`), so on-axis grid points
come back as exactly `0.0`. The **JAX** branch (`:201-206`) still rotates via
`arctan2`/`cos`/`sin`, which returns `1.2e-16` at the same point.

`check_profile_method` in `profiles_jit.py` compares with `rtol=1e-5, atol=0.0`
(`:93-94`, `:152`), so any non-zero value against an exact zero is an *infinite*
relative error, however small in absolute terms. The absolute disagreement is
2.2e-16 — one ulp — i.e. both paths are correct.

`mp.ExternalPotential` already hit this exact class of failure and passes
`atol=1e-12` at its two call sites (`:651`, `:660`), with the reason documented
in `check_profile_method`'s `atol` docstring.

## Task

Pass `atol=1e-12` on the two `mp.PowerLaw` `check_profile_method` calls
(around `:504-519`), mirroring the `mp.ExternalPotential` precedent, with a
one-line comment naming PyAutoGalaxy#598.

Do **not** loosen `rtol` — the 1e-5 relative check is what actually certifies the
JAX path, and it must stay armed. Do not touch other profiles unless a local run
shows the same exact-zero artefact for them.

## Acceptance

- `scripts/misc/profiles_jit.py` exits 0 locally under the smoke recipe.
- `rtol` unchanged everywhere; only `atol` added, only on `mp.PowerLaw`.
- The comment names PyAutoGalaxy#598 so the next reader does not re-diagnose it.

## Follow-up (separate, low priority)

The real asymmetry is in the library: the JAX PowerLaw deflections branch should
get the same exact unit-vector transform as the numpy branch, so on-axis
deflections are exactly 0 on both paths. Filed separately as a draft against
@PyAutoGalaxy.

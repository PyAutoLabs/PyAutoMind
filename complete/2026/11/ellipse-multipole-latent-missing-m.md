## ellipse-multipole-latent-missing-m
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/719
- completed: 2026-11-18
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/720
- summary: `af.Model(ag.EllipseMultipole)` / `af.Model(ag.EllipseMultipoleScaled)` built without an explicit `m` made `latent_parameters_from` raise `TypeError: missing 'm'`. Added `m: Constant 4` to `autogalaxy/config/priors/ellipse/ellipse_multipole.yaml` for both classes (as `PowerLawMultipole` already had), plus a regression test in `test_autogalaxy/test_convert.py` and the priors-config test.
- shipped by: shift worker 2026-11-16-pm (glance, PR-open); merged 2026-11-18 from a /health session on the human's explicit "do all the PRs" command, CI GREEN (4 success, 1 skipped non-test leg "Refresh the Heart feed").
- workspace impact: none — every workspace script sets `m` explicitly.
- follow-up (not filed): `EllipseMultipoleScaled` has no prior config for `major_axis`.

## Original prompt

# EllipseMultipole latent parameters raise TypeError when `m` is not set explicitly

Type: bug
Target: PyAutoGalaxy
Repos:
- PyAutoGalaxy
Difficulty: small
Autonomy: safe
Consequence: glance
Priority: medium
Status: draft
Filed: 2026-11-16
Lane: any
Verified: 2026-11-16 2e66e14d (PyAutoGalaxy)

Found while renaming the convert helpers (PyAutoGalaxy#717). It is also on main.
`af.Model(ag.EllipseMultipole)` and `af.Model(ag.EllipseMultipoleScaled)` built without an explicit
`m` make `latent_parameters_from` raise `TypeError: missing 'm'`. Passing `m` works. The latent
declarations pass `m` as an input to the multipole conversion, but when `m` is left at its
default it never reaches the conversion's keyword arguments.

Witness: a test builds both models without `m`, calls `latent_parameters_from` on an instance, and gets
`k_m`/`phi_m` with the default `m`. The same test fails on main.

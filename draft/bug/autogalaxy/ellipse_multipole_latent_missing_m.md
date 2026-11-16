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

Found while renaming the convert helpers (PyAutoGalaxy#717). It is also on main.
`af.Model(ag.EllipseMultipole)` and `af.Model(ag.EllipseMultipoleScaled)` built without an explicit
`m` make `latent_parameters_from` raise `TypeError: missing 'm'`. Passing `m` works. The latent
declarations pass `m` as an input to the multipole conversion, but when `m` is left at its
default it never reaches the conversion's keyword arguments.

Witness: a test builds both models without `m`, calls `latent_parameters_from` on an instance, and gets
`k_m`/`phi_m` with the default `m`. The same test fails on main.

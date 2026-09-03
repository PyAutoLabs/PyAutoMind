# Gaussian precompute phase 3: downstream sweep — SLaM, test_autolens, workspace regressions, doc line

Type: feature
Epic: gaussian-deflections-precompute
Phase: 3
Target: autolens
Repos:
- @PyAutoLens
- @autolens_workspace
- @autolens_workspace_test
Themes:
- numba-cpu
- mass-profiles
- profiling
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-09-03
Parent: draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md

> Phase 3 of the `gaussian-deflections-precompute` epic — ledger
> `draft/feature/autogalaxy/precompute_fixed_geometry_gaussian_deflections.md`. Successor work to the
> completed `numpy-deflections-cpu` epic (`complete/archive/epics/numpy_deflections_cpu_speedup.md`).
> Phases 1 and 2 are hard predecessors — this phase adds no library mechanism, it **verifies** the memo
> on the driver it was built for and documents it where a user meets it.

## Goal

The memo exists for the SLaM `mass_light_dark` shape: a fixed MGE lens light chained into the mass with one
free `mass_to_light_ratio`. Prove nothing downstream moved, and tell the user the switch exists.

## Steps

1. **`test_autolens`** green in full (numpy; and under JAX where the suite runs it).
2. **SLaM smoke** on `autolens_workspace/scripts/imaging/features/advanced/mass_stellar_dark/slam.py` —
   the driver the memo is for. Run it in test mode per the workspace's smoke contract and confirm it
   completes with the memo on and with `AUTOGALAXY_DEFLECTIONS_MEMO=0`.
3. **`autolens_workspace_test` regression scripts** for fixed-MGE lens models: run and compare, report any
   drift rather than re-pinning.
4. **Numba likelihood pins** unchanged (hst rect 27661.910133665442 and siblings).
5. **Doc line** in the SLaM `mass_light_dark` script explaining that fixed-geometry deflections are memoised
   across likelihood evaluations and rescaled by the free ratio, and naming the
   `AUTOGALAXY_DEFLECTIONS_MEMO=0` kill switch.
6. **No PyAutoLens library edit is assumed.** This is a verification phase; if a PyAutoLens change turns out
   to be needed, file it then — do not scope it now.

## Verification

- `test_autolens` green; `ruff check` + `ruff format --check` clean on anything touched.
- SLaM smoke completes both with the memo on and with the kill switch set; runtimes for both recorded.
- `autolens_workspace_test` regression scripts pass with pins unchanged; any shift reported as a finding.
- Numba likelihood pins unchanged at rtol 1e-6.
- The doc line renders correctly in the generated notebook for the SLaM script.

## Ship

Workspace-only expected: `autolens_workspace` PR (doc line) and, if any regression script needed a fix,
an `autolens_workspace_test` PR. Behind the library-first gate — phases 1 and 2 must be merged first.

## Out of scope

Any library mechanism change (phases 1 and 2); re-pinning likelihood or deflection values; new SLaM
features; PyAutoLens source edits not proven necessary by this phase's own runs.

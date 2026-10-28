## lenstwin-p2-mass-budget
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/675
- completed: 2026-10-28
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/676
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/676
- epic: lenstwin (phase 2; ledger draft/feature/autolens/lenstwin_epic.md)
- summary: Phase 2 of the lenstwin epic: the mass-normalisation mathematics, in new module
  `autogalaxy/operate/mass_budget.py` (merge 7701202). `ag.CircularAperture(radius, centre, …)`
  measures projected mass by the 0A grid integrator (its sub-grid settings are plain attributes);
  `Aperture` is the protocol phase 3's Einstein-radius aperture implements in PyAutoLens.
  `ag.mass_to_light_ratio_for_mass_from` and `ag.kappa_s_for_mass_from` solve Υ and κ_s exactly as
  mass / mass-at-unit (both convergences linear in the parameter; no root finder).
  `ag.MassBudget(aperture, fractions).solve(...)` returns the stellar `Basis` of `lmp.Gaussian`,
  the dark profile (`NFWSph`, or `gNFWSph` with `inner_slope` via `**fixed`) and a `derived` dict
  (aperture radius and centre, M_ref, M_light at Υ=1, Υ, r_s, κ_s, f_dark, fixed). Multi-galaxy
  budgets raise `NotImplementedError` (R7). Convention page `docs/api/mass_budget.rst` states R3
  and R4 as ruled 2026-10-28. Public API grew; nothing removed.
- tests: `test_autogalaxy/operate/test_mass_budget.py` (18, 1.7 s): Gaussian closed form for Υ
  (1e-4); NFWSph κ_s target (1e-4), linearity (1e-10), quad and closed-form agreement (1e-3);
  gNFWSph(inner_slope=1) = NFWSph (1e-4); 50/50 budget on IsothermalSph inside θ_E reproduces
  π θ_E² (~5e-5 on 88×88 at 0.025"); validation errors. Full suite 1417 passed / 7 skipped; CI
  green on abcb81b (3.12, 3.13, nojax, docs).
- traps: the isothermal centre cusp limits grid accuracy (~2e-4 at 0.05" with default sub-sizes;
  `sub_size_centre=128` on 0.025" reaches 5e-5). gNFW convergence does one `quad` per point, so
  callers must pass coarse aperture sub-sizes for gNFW. `lmp.Gaussian` floors axis ratio at
  0.9999, ~8e-5 off the circular closed form at large R/σ. r_s is in arcsec; kpc conversion is
  phase 3. The comment near `test_autogalaxy/operate/test_lens_calc.py:41` saying
  `NFWSph.mass_angular_within_circle_from` fails is stale since #674.
- notes: Consequence: judge — human /prm (merged in this session on the human's /prm command;
  freeze clear). Heart STALE for environment reasons only. Implementation by an Opus
  execution-tier worker; plan, review, PR wording in the main session. No task worktree (remote
  clone). Next: phase 3 (PyAutoLens), needs ruling R6.

## Original prompt

# LensTwin phase 2: mass-normalisation mathematics — `MassBudget`, `CircularAperture` and the M/L and κ_s solvers (PyAutoGalaxy)

Type: feature
Target: autogalaxy
Repos:
- PyAutoGalaxy
Themes:
- mge
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a circular-Gaussian `Basis` solved by `mass_to_light_ratio_for_mass_from` reproduces the closed form 2πΥIσ²(1−e^{−R²/2σ²}) to 1e-4; `kappa_s_for_mass_from` for `NFWSph` at fixed r_s reproduces its target mass to 1e-4 and is monotonic in the target; a 50/50 `MassBudget` on an `Isothermal` reference inside its θ_E reproduces M_ref to 1e-4; a budget naming two galaxies raises `NotImplementedError`; a docs page states the convention
Review-minutes: 30
Unattended: never
Epic: lenstwin
Phase: 2
Parent: draft/feature/autolens/lenstwin_epic.md
Filed: 2026-10-28
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/675

Phase 2 of the `lenstwin` epic (ledger `draft/feature/autolens/lenstwin_epic.md`; report `lenstwin_epic_report.md` §2.3 "Mass normalisation", §3 "Phase 2"). Depends on phase 0A, merged as PyAutoGalaxy#672: `mass_angular_within_circle_via_grid_from` (`autogalaxy/operate/lens_calc.py:1945`) is the one aperture-mass definition every component shares, and `Basis.mass_basis_from(mass_to_light_ratio)` (`autogalaxy/profiles/basis.py:279`) turns the solved light basis into a mass basis. Library only; no transformation and no tracer-level aperture here (both are phase 3, PyAutoLens).

Since 2026-10-28 there is no dedicated `Science/twins` project: science use of these primitives happens in ordinary `Science/active` projects, so keep the API small and driven by the phase-3 transformation, not by speculative callers.

## What to build (PyAutoGalaxy, one PR)

1. **Aperture.** An `Aperture` protocol and `CircularAperture(radius, centre)` whose `mass_from(mass_obj, grid)` calls `mass_angular_within_circle_via_grid_from`. Phase 3 adds `EinsteinRadiusAperture` in PyAutoLens against this protocol.
2. **Solvers.**
   - `mass_to_light_ratio_for_mass_from(basis, mass, aperture, grid)` — Υ = mass / M_light(Υ=1), with M_light the grid integral of `basis.mass_basis_from(1.0)` (linear, so no root find).
   - `kappa_s_for_mass_from(dark_cls, mass, aperture, scale_radius, centre, grid, **fixed)` — 1-D root find on κ_s so the dark profile's aperture mass equals `mass`; `NFWSph` first, `gNFWSph` with `inner_slope` passed through `fixed`. Raise clearly when no bracket exists.
3. **`MassBudget(aperture, fractions)`** — per-galaxy fractions (`{"lens": {"stellar": 0.5, "dark": 0.5}}`), fractions summing to 1 validated; `solve(reference_mass, light_basis, dark_cls, scale_radius, centre, grid, **fixed)` returning the stellar mass basis, the dark profile and a plain dict of derived numbers (aperture radius, M_ref, M_light(Υ=1), Υ, r_s, κ_s, f_dark) for phase 3's `TransformationRecord.procedure`. A budget naming more than one galaxy raises `NotImplementedError` (multi-galaxy convention is R7, phase 5).
4. **Docs.** A `docs/` page stating the convention in the words of report §2.3 as ruled (R3, R4), which phase 3's record quotes verbatim.

Placement (implementer chooses and says so in the PR): beside `mass_angular_within_circle_via_grid_from` in `autogalaxy/operate/`, or a small `autogalaxy/profiles/mass/budget.py`; exported at `ag.` top level only if the existing `operate` functions are.

## Tests

Circular-Gaussian closed form for Υ (1e-4); NFWSph κ_s solve hits target mass (1e-4) and is monotonic; gNFWSph with `inner_slope=1` agrees with NFWSph; 50/50 budget on an `Isothermal` reference inside its own θ_E reproduces M_ref = π θ_E² (convergence units) to 1e-4 with stellar + dark summing back; fractions not summing to 1 raise; two-galaxy budget raises `NotImplementedError`; no-bracket κ_s raises. NumPy only; keep the gNFW case analytic or small-grid (per-point `quad` in gNFW `convergence_2d_from` is slow — see complete/2026/10/mass-integral-scalar-radius.md traps).

## Rulings (taken 2026-10-28, accepted as recommended)

- **R3** aperture = circle of radius θ_E,parent (tracer-level, via `LensCalc`) centred on the replaced galaxy's mass centre; M_ref = replaced component(s)' projected mass inside it by grid integration; shear and other galaxies untouched. Phase 2 implements only the circular aperture and the budget; the θ_E aperture is phase 3.
- **R4** first halo `NFWSph` centred on the light with a fixed physical r_s (c(M) as a later parameter).

Out of scope: `EinsteinRadiusAperture`, the transformation, diagnostics (phase 3); multi-galaxy budgets (phase 5); elliptical NFW.

Say explicitly in the PR that the public API grew (AGENTS.md rule).

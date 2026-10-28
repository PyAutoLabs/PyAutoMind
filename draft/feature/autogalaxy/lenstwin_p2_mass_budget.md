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
Blocked-by: rulings R3 (reference aperture and mass convention) and R4 (first halo, fixed r_s) in the epic ledger — `/start_dev` only after both are ruled
Filed: 2026-10-28

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

## Rulings this phase needs (epic ledger; recommendations in report §4)

- **R3** aperture = circle of radius θ_E,parent (tracer-level, via `LensCalc`) centred on the replaced galaxy's mass centre; M_ref = replaced component(s)' projected mass inside it by grid integration; shear and other galaxies untouched. Phase 2 implements only the circular aperture and the budget; the θ_E aperture is phase 3.
- **R4** first halo `NFWSph` centred on the light with a fixed physical r_s (c(M) as a later parameter).

Out of scope: `EinsteinRadiusAperture`, the transformation, diagnostics (phase 3); multi-galaxy budgets (phase 5); elliptical NFW.

Say explicitly in the PR that the public API grew (AGENTS.md rule).

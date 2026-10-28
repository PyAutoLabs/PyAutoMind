# LensTwin phase 3: first transformation `ReplaceTotalMassWithStellarPlusDark`, the Einstein-radius aperture, and twin diagnostics with a library plotter (PyAutoLens)

Type: feature
Target: autolens
Repos:
- PyAutoLens
Themes:
- mge
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: on a fixture SIE(+shear) reference with an MGE lens light, `twin.apply(transform.ReplaceTotalMassWithStellarPlusDark(...))` with a 50/50 budget yields a twin whose stellar and dark projected masses inside θ_E,parent are each 0.5 ± 1e-3 of M_ref, keeps the shear unchanged, and appends a `TransformationRecord` that round-trips through `al.to_dict`/`al.from_dict` and `SimulatedTwin.output_to`/`from_directory`; `al.twins.compare(baseline, twin)` returns Δχ²_image > 0 and Δχ²_image(baseline, baseline) == 0; `aplt.subplot_twin_comparison` writes a PNG
Review-minutes: 45
Unattended: never
Epic: lenstwin
Phase: 3
Parent: draft/feature/autolens/lenstwin_epic.md
Filed: 2026-10-28
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/805

Phase 3 of the `lenstwin` epic (ledger `draft/feature/autolens/lenstwin_epic.md`; report `lenstwin_epic_report.md` §2.2 objects, §2.3 mass normalisation, §2.4 diagnostics, §3 "Phase 3"). Depends on phase 0B (`al.twins`, PyAutoLens#804) and phase 2 (`ag.MassBudget`, `ag.CircularAperture`, `ag.mass_to_light_ratio_for_mass_from`, `ag.kappa_s_for_mass_from`, PyAutoGalaxy#676, record `complete/2026/10/lenstwin-p2-mass-budget.md`), both merged to `main`. Rulings taken: R3 and R4 (2026-10-28, convention page `PyAutoGalaxy/docs/api/mass_budget.rst`), R6 (2026-10-28: the diagnostics plotter lives in the library, following the `aplt` conventions). No `Science/twins` project (ruled 2026-10-28): keep the API driven by this transformation, not speculative callers.

## What to build (PyAutoLens, one PR)

1. **Einstein-radius aperture.** In `autolens/twins/` a helper (e.g. `aperture.py`: `einstein_radius_aperture_from(tracer, grid, centre, **integrator_settings) -> ag.CircularAperture`) computing θ_E,parent tracer-level via `ag.LensCalc.from_tracer(tracer).einstein_radius_from(grid)` over all mass (R3), centred on the replaced galaxy's mass centre. Expose the θ_E for the record.
2. **`transform.ReplaceTotalMassWithStellarPlusDark`** (`autolens/twins/transform/stellar_dark.py`): arguments the galaxy to replace (by the name/role convention `ReferenceModel` already uses — verify how galaxies are addressed in a tracer loaded from `tracer.json` and reuse it), the light component (its MGE `Basis`), `f_dark` (or an `ag.MassBudget`), the dark class (`al.mp.NFWSph` default, `gNFWSph` with `inner_slope`), the scale radius in **kpc** converted to arcsec with the setup cosmology's `arcsec_per_kpc_from(redshift)` at the galaxy's redshift (R4), `keep_shear=True`, and aperture integrator settings (gNFW needs coarse sub-sizes — trap in the phase-2 record). `apply(twin)` returns `(tracer, setup, record)` without mutating the twin: the replaced galaxy's total-mass profile(s) are removed, the stellar `lmp.Gaussian` basis and the dark profile added; light, external shear, other galaxies and the source unchanged. M_ref is the replaced component(s)' mass only (shear excluded). Record: `requested` (all arguments), `procedure` (convention text quoting the docs page plus `MassBudget.solve`'s `derived` numbers, θ_E,parent, r_s in kpc and arcsec, implied redshift/cosmology), `changed` (component paths), `side_effects` (shear kept; the twin's own θ_E recomputed and reported, not asserted), `preserved` (["projected mass of <galaxy> inside θ_E,parent"] — the one deliberate preservation). Flat ground-truth parameters (Υ, κ_s, r_s, slope, f_dark(θ_E)) reach `twin.json` so inference needs no re-derivation. Raise for multi-galaxy budgets (R7) and for light components with no `lmp` counterpart.
3. **Diagnostics** (`autolens/twins/compare.py`): `al.twins.compare(parent, twin, grid=None)` → a small result object with convergence and deflection difference maps, enclosed-mass profiles M(<R) for both on a radius grid, tangential critical curves of both, θ_E of both, and Δχ²_image = Σ(I_twin − I_parent)²/σ² noise-free on the parent's masked grid with the parent PSF (reuse `Twin.noise_free_image_2d`). `compare_to_data(twin, dataset)` → Δχ²_data = χ²(twin|data) − χ²(parent|data) via two `al.FitImaging` (parametric sources only; raise for pixelised sources). The two numbers are different quantities and are named as such.
4. **Plotter** (R6): `autolens/twins/plot/twin_plots.py` with `subplot_twin_comparison(comparison, output_path=None, output_filename=..., output_format=...)` (parent/twin images, residual/noise, convergence difference, M(<R) curves, critical curves), following `autolens/lens/plot/tracer_plots.py` conventions; export it from `autolens/plot/__init__.py`.
5. **Docs**: extend `docs/api/twins.rst` with the transformation, `compare`, `compare_to_data` and the plotter; cite the PyAutoGalaxy convention page.

## Tests (`test_autolens/twins/`, NumPy only)

The witness above; Identity still works; transformation does not mutate the parent twin/tracer; r_s kpc→arcsec uses the setup cosmology; `gNFWSph` with `inner_slope` round-trips; a two-galaxy budget raises `NotImplementedError`; `compare` of a twin with itself is zero everywhere; `compare_to_data` on the 7x7 fixture returns finite numbers; the subplot writes a PNG under `tmp_path`. Keep runtime small (coarse grids; the 7x7 fixtures).

Out of scope: the identifiability experiment (phase 4), library ingestion and multi-galaxy normalisation (phase 5, R7), workspace and assistant (phase 6), other transformations.

Say explicitly in the PR that the public API grew (AGENTS.md rule).

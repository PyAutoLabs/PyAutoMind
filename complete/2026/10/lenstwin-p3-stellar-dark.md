## lenstwin-p3-stellar-dark
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/805
- completed: 2026-10-28
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/806
- epic: lenstwin (phase 3; ledger draft/feature/autolens/lenstwin_epic.md)
- summary: Phase 3 of the lenstwin epic (merge b29ffcc). 3A: `al.twins.einstein_radius_aperture_from`
  (tracer-level θ_E via `LensCalc`, returns an `ag.CircularAperture` centred on the replaced galaxy)
  and `al.twins.transform.ReplaceTotalMassWithStellarPlusDark(galaxy, light, *, scale_radius_kpc,
  f_dark=0.5, budget=None, dark_cls=None→NFWSph, keep_shear=True, aperture_settings=None, …,
  **dark_fixed)` — removes the galaxy's total-mass profiles, re-expresses the MGE light basis as
  `lmp.Gaussian` in place (light bit-identical, not double-counted), adds the dark halo on the light
  centre, split solved by `ag.MassBudget`; r_s in kpc converted with the setup cosmology; shear
  kept and excluded from M_ref; non-mutating. Record: requested, procedure (convention text, derived
  numbers, θ_E parent/twin, r_s kpc/arcsec, cosmology, aperture geometry), changed, side_effects,
  preserved = ["projected mass of <galaxy> inside theta_E,parent"]; flat truth via
  `TransformationRecord.truth` and `twin.json["truth"]`. Galaxies addressed by model name
  (`af.ModelInstance` keys), `galaxy_<i>` for list-built tracers, or reference role. 3B:
  `al.twins.compare` → `TwinComparison` (convergence/deflection differences, M(<R), critical curves,
  θ_E both, Δχ²_image), `al.twins.compare_to_data` (Δχ²_data via two FitImaging; parametric sources
  only), `aplt.subplot_twin_comparison` (2×3, R6). Public API grew; nothing removed.
- tests: test_stellar_dark.py (13) + test_compare.py (7); twins 39 passed under -n 4; full suite
  973 passed / 1 skipped / 1 xfailed; CI green on 9541c87 (3.12, 3.13, nojax, docs).
- traps: the first `import jax` in a process draws 13 numbers from NumPy's global RNG
  (jax/_src/clusters/k8s_cluster.py, evaluated at import), reached lazily via autoarray
  `AbstractNDArray.__getitem__`; the phase-0 global-RNG test now warms the route first. The 0.5 ±
  1e-3 witness is measured on the same aperture/grid as the solve (holds by construction); the
  independent check is `compare`'s M(<θ_E) parent = twin. Coarse aperture sub-sizes give ~1%
  M_ref error from the SIE cusp; `compare` uses the defaults. gNFW integration was slow (one `quad`
  per point) — follow-up PyAutoGalaxy#677. A misspelt `**dark_fixed` keyword surfaces as a
  TypeError from the dark constructor. The PNG test sets `autoarray.plot.utils._FAST_PLOTS=False`.
- notes: Consequence: judge — merged on the human's /prm in this session (freeze clear). R3/R4/R6
  ruled 2026-10-28. Heart STALE for environment reasons only. Implementation by an Opus
  execution-tier worker; plan, review, PR wording in the main session. Next: phase 4 needs a release
  carrying phases 0, 2, 3 (human /review_release) and a compute go.

## Original prompt

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

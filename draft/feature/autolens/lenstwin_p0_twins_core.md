# LensTwin phase 0: `autolens/twins/` core (reference model, baseline twin, seeded simulation, provenance) and the two PyAutoGalaxy primitives it needs

Type: feature
Target: autolens
Repos:
- PyAutoGalaxy
- PyAutoLens
Themes:
- mge
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: a 7x7 fixture fit directory ingests as an `al.twins.ReferenceModel`; its baseline `Twin` simulates bit-identically for the same seed across two runs and differently for another seed; `SimulatedTwin.from_directory` of the written output re-simulates to the same image; `ag` projected mass inside a circular aperture by grid integration matches `mass_angular_within_circle_from` for `Isothermal` and `NFWSph` to 1e-3 and the Gaussian closed form 2πΥIσ²(1−e^{−R²/2σ²}) to 1e-4
Review-minutes: 30
Unattended: never
Epic: lenstwin
Phase: 0
Parent: draft/feature/autolens/lenstwin_epic.md
Filed: 2026-10-28

Phase 0 of the `lenstwin` epic (ledger `lenstwin_epic.md`; report `lenstwin_epic_report.md` §2 architecture, §3 "Phase 0" body; surveys `lenstwin_epic_surveys/01` §2–§6). Rulings R1 (package and names: accepted as written here) and R2 (default twin noise: the observed noise map; Poisson only when exposure time and sky are set) were taken by the human on 2026-10-28, so this prompt is ready for `/start_dev`. Library first: 0A (PyAutoGalaxy) merges before 0B (PyAutoLens); 0B may develop against 0A's same-named branch. One issue per repo.

## 0A — PyAutoGalaxy primitives

1. **Projected mass inside a circular aperture for any mass object.** A function (home: beside `LensCalc` in `@PyAutoGalaxy/autogalaxy/operate/lens_calc.py`, or a small `autogalaxy/quantity`-style module; the implementer chooses and says so) that takes any object exposing `convergence_2d_from(grid)` — a profile, a `Basis` (`@PyAutoGalaxy/autogalaxy/profiles/basis.py`), a `Galaxy`, a `Galaxies` — plus a radius, a centre and a grid, and returns Σ κ · pixel-area inside the circle, with a finer sub-grid near the centre so the cusp of an isothermal profile converges. It is the one aperture-mass definition every twin component shares, because `MassProfile.mass_angular_within_circle_from` (`@PyAutoGalaxy/autogalaxy/profiles/mass/abstract/abstract.py:242`) needs `convergence_func`, which `Basis` does not define (survey 01 §4). Tests: agreement with `mass_angular_within_circle_from` for `Isothermal` and `NFWSph` to 1e-3; the circular-Gaussian closed form to 1e-4; a `Basis` of two Gaussians equals the sum of its members.
2. **Light basis → mass basis at a given mass-to-light ratio, instance level.** `Basis.mass_basis_from(mass_to_light_ratio)` (or a free function in `basis.py`) that maps every `lp.Gaussian` member to an `lmp.Gaussian` (`@PyAutoGalaxy/autogalaxy/profiles/light_and_mass_profiles.py:17`) with the same `centre`, `ell_comps`, `intensity`, `sigma` and the shared `mass_to_light_ratio`, raising for members with no `lmp` counterpart. It is the instance-side twin of `mass_light_dark_basis_from` (`@PyAutoGalaxy/autogalaxy/analysis/chaining_util.py:467-547`), which builds `af.Model`s and needs a `Result`. Tests: the field copy matches what `mass_light_dark_basis_from` would produce for the same solved basis; convergence of the mass basis equals `mass_to_light_ratio × image` of the light basis on a grid.

Say explicitly in the PR that the public API grew (AGENTS.md rule).

## 0B — PyAutoLens `autolens/twins/`

Subpackage `@PyAutoLens/autolens/twins/` with `setup.py`, `reference.py`, `twin.py`, `record.py`, `simulate.py`, `transform/{__init__.py, identity.py}` and an `__init__.py` exporting `ObservationSetup`, `ReferenceModel`, `Twin`, `SimulatedTwin`, `TransformationRecord`, `transform`; `from . import twins` added to `@PyAutoLens/autolens/__init__.py` next to `potential_correction` (line 145). Precedents for a self-contained subpackage: `@PyAutoLens/autolens/weak/`. Every object implements the `autonerves.dictable` contract so `al.to_dict` / `al.from_dict` / `al.output_to_json` / `al.from_json` work unchanged.

- `ObservationSetup`: mask, PSF (`al.Convolver`), observed noise map, pixel scales, origin, over-sample sizes (lp and pixelization), cosmology, optional `exposure_time` and `background_sky_level`. `from_dataset(imaging)` and `from_fit_directory(path)` — the latter reuses `image/dataset.fits` HDU layout and `agg_util.mask_header_from` exactly as `_imaging_from` does (`@PyAutoGalaxy/autogalaxy/aggregator/imaging/imaging.py:29-115`; `@PyAutoLens/autolens/imaging/model/analysis.py:240-279` writes it). `with_(...)` returns a modified copy. `grid` property = the masked lens-plane grid.
- `ReferenceModel` (immutable): `tracer` (from `files/tracer.json` via `al.from_json`, i.e. with solved intensities — survey 01 §2), `setup`, `provenance` (`lens_id`, `labels`, `roles` mapping galaxy name → role, `fit_path`, SHA-256 of `dataset.fits` and `tracer.json`, `ingested_at`, library versions via `importlib.metadata`, Python version). `from_fit_directory(path, lens_id, labels=(), roles=None)`, `from_result(result, dataset, ...)`, `output_to(dir)` / `from_directory(dir)`.
- `Twin`: `reference`, `tracer` (ground truth), `setup`, `records`. `Twin.baseline(reference)`; `apply(transformation)` returns a new `Twin` with the record appended; `with_setup(setup)`; `simulate(seed, noise="observed")` → `SimulatedTwin`. The `"observed"` route draws Gaussian noise from `setup.noise_map` with `numpy.random.default_rng(seed)` on top of the PSF-convolved noise-free image from `al.SimulatorImaging.via_tracer_from` with noise off (`@PyAutoLens/autolens/imaging/simulator.py:25`); the `"poisson"` route passes `exposure_time`, `background_sky_level`, `noise_seed=seed` to `al.SimulatorImaging` and requires both to be set. Verify the `SimulatorImaging` constructor in PyAutoArray first (not surveyed).
- `TransformationRecord`: `name`, `requested`, `procedure` (text + derived numbers), `changed`, `side_effects`, `preserved` (empty by default — preservation is never implicit). `transform.Identity` produces a record with empty changes so the chain and JSON are exercised in phase 0.
- `SimulatedTwin`: `dataset` (`al.Imaging`, masked and over-sampled like the setup), `truth` (the tracer), `seed`, `noise`, `simulator settings`, `twin`. `output_to(dir)` writes `data.fits`, `noise_map.fits`, `psf.fits`, `mask.fits`, `truth_tracer.json`, `twin.json` (reference pointer and provenance, records, setup overrides, seed, noise route, versions); `from_directory(dir)` reloads and `resimulate()` reproduces the image bit-for-bit.
- Docs: `@PyAutoLens/docs/api/twins.rst` listing the exports; a short module docstring stating the three invariants from the ledger.

Tests (`test_autolens/twins/`, NumPy only, config pushed by the existing `conftest.py`): a fixture fit directory built under `data_temp` with `af.DirectoryPaths` as in `@PyAutoLens/test_autolens/analysis/test_analysis.py:157-177` ingests; the baseline twin's noise-free image equals the parent tracer's `image_2d_from` on the setup grid bit-for-bit; seed determinism and seed sensitivity; `output_to` / `from_directory` / `resimulate` round trip; `to_dict` / `from_dict` for every object; `Identity` record serialises; `from_fit_directory` reproduces the dataset `ImagingAgg` would rebuild (data, noise map, PSF kernel, mask equal).

Out of scope here: any mass transformation, `MassBudget`, Einstein-radius apertures, diagnostics (phases 2–3), the science project (phase 1), workspace or assistant changes (phase 6).

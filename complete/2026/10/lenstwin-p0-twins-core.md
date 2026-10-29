## lenstwin-p0-twins-core
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/671
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/803
- completed: 2026-10-28
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/672
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/804
- epic: lenstwin (phase 0; ledger draft/feature/autolens/lenstwin_epic.md)
- summary: Phase 0 of the lenstwin epic, library first. 0A PyAutoGalaxy#672 (merge b072e4d):
  projected mass inside a circular aperture by grid integration for any object with
  `convergence_2d_from` (profile, `Basis`, `Galaxy`, `Galaxies`), and `Basis.mass_basis_from`
  (light-Gaussian basis → `lmp.Gaussian` basis at a shared mass-to-light ratio). 0B
  PyAutoLens#804 (merge 9a85d32): the `autolens/twins/` subpackage exported as `al.twins` —
  `ObservationSetup`, immutable `ReferenceModel` (tracer with solved intensities, setup,
  provenance with SHA-256 hashes and library versions), value-like `Twin`
  (`baseline`/`apply`/`with_setup`/`simulate(seed, noise=...)`), `SimulatedTwin`
  (`output_to`/`from_directory`/`resimulate` bit-identical, `twin.json`),
  `TransformationRecord`, `transform.Identity`. Rulings R1 (names, placement) and R2 (observed
  noise map by default; Poisson only with exposure time and sky) honoured. Public API grew in
  both repos; nothing removed.
- tests: 0A suite 1390 passed / 7 skipped; CI green on b81951a. 0B `test_autolens/twins/` 19
  tests (seed determinism and sensitivity, output → reload → resimulate bit-identity,
  dict round trips, aggregator-equivalent ingest, immutability, global RNG untouched); CI green
  on 1d430dc on every leg (unittest 3.12, 3.13, nojax; docs-build).
- traps: `SimulatorImaging.via_image_from` always draws a Poisson sample from NumPy's global
  random state (even with Poisson noise off) and raises on negative pixels, so the "observed"
  route convolves directly with `tracer.blurred_image_2d_from` and draws Gaussian noise with
  `numpy.random.default_rng(seed)`; `SimulatedTwin.simulator["route"]` records it. PyAutoFit's
  dictable parser bypasses a class's own `from_dict` and drops `None` entries; FITS-loaded
  arrays carry an `aa.Header` that does not round-trip, so `ObservationSetup` stores header-free
  copies. pytest 9.2 rejects nested structures in `pytest.approx`: 0B carried a cherry-pick of
  2b063ca (from unmerged branch `ccr-b1080ef2-0tcwow`) fixing 7 `point/test_dataset.py` tests,
  so that fix is now on PyAutoLens `main`.
- notes: Consequence: judge — both merges human (/prm; #804 merged by the human after CI went
  green). Heart STALE for environment reasons only throughout; not frozen. Implementation by an
  Opus execution-tier worker; plan, judgment and PR wording in the main session. No task
  worktree (remote session clones). Next: phase 1 `Science/twins` birth, after a release carries
  phase 0 (human `/review_release`) and ruling R5.

## Original prompt

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
Issued: 2026-10-28
Issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/671 (0A), https://github.com/PyAutoLabs/PyAutoLens/issues/803 (0B)

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

## Verified at issue time (2026-10-28, read from `main` of PyAutoArray, PyAutoFit, PyAutoGalaxy, PyAutoLens; the surveys did not cover these)

- `aa.SimulatorImaging.__init__(exposure_time, background_sky_level=0.0, subtract_background_sky=True, psf=None, use_real_space_convolution=True, normalize_psf=True, add_poisson_noise_to_data=True, include_poisson_noise_in_noise_map=True, noise_if_add_noise_false=0.1, noise_seed=-1, use_jax=False)` — `exposure_time` is required with no default, so the `"observed"` route either constructs it with `exposure_time=1.0`, `add_poisson_noise_to_data=False`, `include_poisson_noise_in_noise_map=False` (noise map then a constant `noise_if_add_noise_false` to be replaced by `setup.noise_map`) or bypasses the simulator and PSF-convolves the tracer image itself; the implementer chooses and the twin stores which. `al.SimulatorImaging.via_tracer_from(tracer, grid, xp=None)` calls `tracer.set_snr_of_snr_light_profiles` first and pads the grid for the kernel; `via_image_from(image, over_sample_size=None, image_is_convolved=False, xp=None)` exists for a pre-convolved image.
- Poisson route: `noise_seed` seeds via `np.random.seed` in `preprocess.data_eps_with_poisson_noise_added` (global NumPy state, `-1` = random), so it is deterministic for a fixed `seed` but the `"observed"` route must use its own `numpy.random.default_rng(seed)` and never the global state.
- `aa.Imaging.__init__(data, noise_map=None, psf=None, psf_setup_state=False, noise_covariance_matrix=None, over_sample_size_lp=4, over_sample_size_pixelization=4, convolve_over_sample_size_lp=1, convolve_over_sample_size_pixelization=1, use_normalized_psf=True, check_noise_map=True, sparse_operator=None)`; `Imaging.from_fits(pixel_scales, data_path, noise_map_path, data_hdu=0, noise_map_hdu=0, psf_path=None, psf_hdu=0, noise_covariance_matrix=None, check_noise_map=True, over_sample_size_lp=4, over_sample_size_pixelization=4, convolve_over_sample_size_lp=1, convolve_over_sample_size_pixelization=1, psf_pixel_scales=None)`; `apply_mask(mask)` may be called once only (a second call raises — rebuild from arrays to re-mask); `apply_over_sampling(over_sample_size_lp=None, over_sample_size_pixelization=None)`. The PSF is an `aa.Convolver` (`al.Convolver`) everywhere, not a `Kernel2D`.
- `af.ModelInstance.as_model(model_classes=(), excluded_classes=())` exists (`autofit/mapper/model.py:522`) and delegates to `AbstractPriorModel.from_instance`; phase 0 does not need it (the reference tracer is an instance) but `ReferenceModel.from_result` may use `result.instance` directly.
- Reload recipe confirmed: `agg_util.mask_header_from(fit, name="dataset")` and `_imaging_from(fit)` in PyAutoGalaxy's aggregator read `image/dataset.fits` HDUs 0–3 (mask, data, noise map, PSF); `AnalysisImaging` writes it at `paths.image_path / "dataset.fits"`. `al.{to_dict, from_dict, from_json, output_to_json}` are re-exported from `autonerves.dictable`; `autolens/__init__.py` line 145 is `from . import potential_correction as pc`.

Out of scope here: any mass transformation, `MassBudget`, Einstein-radius apertures, diagnostics (phases 2–3), the science project (phase 1), workspace or assistant changes (phase 6).

# LensTwin epic — research report, architecture and detailed phase bodies

Type: feature
Target: autolens
Repos:
- PyAutoLens
- PyAutoGalaxy
Themes:
- mge
- assistants
- hpc-gpu
Difficulty: too-large
Autonomy: human-required
Priority: high
Status: evidence record for the lenstwin epic — never issued; read it from the epic ledger
Consequence: glance
Review-minutes: 0
Unattended: never
Epic: lenstwin
Filed: 2026-10-28

Written 2026-10-28 by the architect session from two read-only Explore surveys in `lenstwin_epic_surveys/` (01 PyAutoLens/PyAutoGalaxy at release 2026.10.26.1; 02 autolens_assistant and autolens_workspace) plus the organism's own records (PyAutoCortex `projects.yaml`, the `subhalo_validation` ledger, PyAutoMemory `wiki/lensing/concepts/bulge-halo-decomposition.md`). No code was edited and nothing was run. The ledger (phase cards, rulings, status) is `lenstwin_epic.md`; this file holds the evidence, the architecture and the detailed phase bodies. Cite the surveys (`surveys/NN §x`) rather than re-surveying. PyAutoFit and PyAutoArray were not on disk; claims about them are from call sites and must be verified in phase 0.

## 0. Summary

Everything a baseline digital twin needs already exists as pieces, and nothing composes them:

1. **A fitted lens is already a reloadable generative model.** Every PyAutoLens imaging fit writes `files/tracer.json` with the solved linear intensities (MGE Gaussians become standard `lp.Gaussian`), plus `image/dataset.fits` whose HDUs carry mask, data, noise map, PSF kernel and the over-sampling maps, with pixel scales in the header (`surveys/01 §2`). `al.from_json` and `al.agg.ImagingAgg` reload them. **Not persisted:** exposure time, background sky level, noise seed, positions.
2. **Simulation from an instance exists only as workspace classes.** `al.SimulatorImaging.via_tracer_from` takes any tracer; the subhalo sensitivity scripts rebuild a tracer from `result.instance` and simulate with the real mask and PSF, but with hard-coded exposure time, sky and `noise_seed=1`, and the noise map is always Poisson-derived from exposure time and sky; no call site simulates from an existing noise map (`surveys/01 §5, §7`; `surveys/02 §6`).
3. **Stellar-plus-dark decomposition exists as model builders, not as instance operations.** `al.util.chaining.mass_light_dark_basis_from` turns a solved MGE light basis into an `af.Model(Basis)` of `lmp_linear.Gaussian` with one shared `mass_to_light_ratio`; `NFW`, `NFWSph`, `gNFW`, `NFWMCRLudlow` are all available with physical helpers; `lmp.Gaussian` carries `(intensity, sigma, mass_to_light_ratio)`. There is no instance-level "this light basis at this M/L" constructor, and `Basis` has no `convergence_func`, so `mass_angular_within_circle_from` fails on an MGE (`surveys/01 §3, §4`).
4. **Einstein radius is tracer-level and profile-independent** (`LensCalc.einstein_radius_from`, area of the tangential critical curve), which is the right aperture definition for multi-galaxy parents; there is no tracer-level projected-mass-inside-R helper (`surveys/01 §4`).
5. **Multi-galaxy and multi-plane are native.** `Tracer` groups galaxies by redshift, `Galaxy(redshift, **components)` takes arbitrary named components, `MassField` carries shear; `extra_galaxies`, `LOSSampler`, `sliced_tracer_from` and `substructure_util` cover extra deflectors, line-of-sight halos and multi-plane (`surveys/01 §2, §7`). The twin representation therefore needs no new container: a twin *is* a `Tracer` plus an observation setup plus provenance.
6. **The science workspace is a Cortex project, not a Mind repo.** Science projects reach the organism through a row in `PyAutoCortex/projects.yaml` and a `projects/<key>.md` ledger (runs, results, lessons); `subhalo_validation` is the model (`hpc/sync` CLI, `wiki/project/state.md`, `run_chain.sh`, witness JSONs, `assistant: autolens_assistant`). The assistant's `start-new-project` skill scaffolds such a project (`project.yaml` with `seed_policy: required`, `hpc/` template, journal run table) (`surveys/02 §4`).
7. **The assistant has no simulate-from-fit, stellar-dark or what-if skill**; `al_simulate_dataset`, `al_load_results`, `init-slam` option F and the `mass_profiles` wiki page are the nearest. A new capability is one flat `skills/al_<task>.md` plus a wiki page and a citation-map row, verified by running its recipe under `PYAUTO_TEST_MODE=1`; it must cite a workspace script (`surveys/02 §1–§3`). The assistant also ships a committed public MGE + SIE + shear + MGE fit of `cosmos_web_ring` (`scripts/cosmos_web_ring/results/good/tracer.json`) with the dataset: a ready-made public reference model.

The plan: a small `autolens/twins/` subpackage (phase 0) whose objects are a frozen `ReferenceModel`, an `ObservationSetup`, a `Twin` that is transformed functionally and simulated with a seed, and a `TransformationRecord`; two profile-level primitives in PyAutoGalaxy (grid-integrated projected mass inside an aperture for any mass object; light-basis-to-mass-basis at a given M/L); the `Science/twins` Cortex project born and the first baseline twin of a real fitted lens run (phase 1); the mass-normalisation mathematics as a reusable `MassBudget` (phase 2); the first transformation with its diagnostics (phase 3); the first identifiability experiment, locally then on RAL (phase 4); library ingestion of the Euclid sample with multi-galaxy support (phase 5); workspace examples and the assistant skill once the workflow is validated (phase 6).

## 1. What exists and what to reuse

### 1.1 Persistence and reload (`surveys/01 §2, §6`; `surveys/02 §8`)

| Need | Exists | Reuse |
|---|---|---|
| Max-likelihood model with solved intensities | `files/tracer.json` written by `save_results` (`autolens/analysis/analysis/dataset.py:170-205`); `ResultImaging.max_log_likelihood_tracer` returns `model_obj_linear_light_profiles_to_light_profiles` | `al.from_json(path/"files"/"tracer.json")` is the ingestion route for a fit directory; a live `Result` also works |
| Observation setup | `image/dataset.fits` (HDU0 mask + header pixel scales/origin, 1 data, 2 noise, 3 PSF, 4–5 over-sample maps), `files/settings.json`, `files/cosmology.json` | `ag.aggregator.agg_util.mask_header_from` + the `_imaging_from` recipe (`autogalaxy/aggregator/imaging/imaging.py:29-115`) rebuild an `Imaging` identically |
| Serialisation of any profile/galaxy/tracer | `autonerves.dictable` (`al.to_dict`, `al.from_dict`, `al.output_to_json`, `al.from_json`) | Twin, record and setup objects implement the same `dictable` contract; no new serialiser |
| Model/instance round trip | `af.Model`, `instance.as_model(...)`, `model.take_attributes`, `result.model` (call sites only; PyAutoFit absent) | Inference models are built from the twin's tracer with existing builders; verify in phase 0 |
| Software versions | `autolens.__version__` is a stale stamp (`surveys/01 §8`); real versions via `importlib.metadata` | Provenance records `importlib.metadata.version` of autolens, autogalaxy, autoarray, autofit, autonerves plus the Python version |

### 1.2 Simulation (`surveys/01 §5`; `surveys/02 §6`)

`al.SimulatorImaging(exposure_time, psf, background_sky_level, add_poisson_noise_to_data, noise_seed, noise_if_add_noise_false, use_jax)` and `via_tracer_from(tracer, grid)` cover the generative step. Two gaps: the noise map is always derived from exposure time and sky (nothing simulates "the observed noise map"); and no simulator example is seeded by default. The sensitivity `SimulateImaging` class (`autolens_workspace/scripts/imaging/features/advanced/subhalo/sensitivity/start_here.py:330-560`) is the only "simulate from a fit" precedent and hard-codes exposure time and sky.

### 1.3 Mass decomposition (`surveys/01 §3, §4`)

- `lmp.Gaussian(centre, ell_comps, intensity, sigma, mass_to_light_ratio)` and `mp.Gaussian` have analytic deflections; `Basis` sums convergence and deflections over members.
- `mass_light_dark_basis_from` (`autogalaxy/analysis/chaining_util.py:467-547`) is the model-side precedent: copy `centre`, `ell_comps`, `sigma`, `intensity=float(solved)` per Gaussian, tie one M/L. The instance-side equivalent is a ~30-line function.
- NFW family: `NFW(centre, ell_comps, kappa_s, scale_radius)`, `NFWSph`, `gNFW(…, inner_slope, …)`, `NFWMCRLudlow(mass_at_200, redshift_object, redshift_source)`; helpers `mass_at_200_solar_masses`, `concentration`, `radius_at_200`; `mass_angular_within_circle_from` works for every analytic profile (scipy quad of `2πr κ(r)`), so NFW mass inside R at fixed `scale_radius` is monotonic in `kappa_s` and a 1-D root find.
- Einstein radius: `LensCalc.from_tracer(...).einstein_radius_from(grid)` (area-equivalent radius of the tangential critical curve) and the `effective_einstein_radius` latent.
- Gap: no projected mass inside a circular aperture for a `Basis`, a `Galaxy` with a basis, or a `Tracer`; the profile route assumes `convergence_func` and elliptical radius. A grid-integrated `Σ κ · pixel area` inside the aperture, with a sub-grid near the centre, is profile-independent and the one definition every component can share.

### 1.4 Multi-galaxy, substructure, line of sight (`surveys/01 §2, §7`)

`Galaxy(redshift, **components)` with arbitrary names; `Tracer.planes` by redshift; `MassField` for shear; `AnalysisLens.tracer_via_instance_from` handles `extra_galaxies`, `scaling_galaxies`, `fields`, `perturb`; `LOSSampler.galaxies_and_fields_from(seed=…)`; `NFWMCRLudlowSph` subhalos in `lens/subhalo.py`. A twin stores galaxies by *name* with an optional *role* (lens, source, extra, dwarf) and never assumes one deflector or one M/L: a `MassBudget` is per galaxy.

### 1.5 Science workspace and HPC (Cortex, `surveys/02 §4, §9`)

`Science/twins` does not exist and is born as a Cortex row (`cortex.py new twins --summary …`; the row itself is a human edit of `projects.yaml`). `subhalo_validation` shows the working shape: `hpc/sync` with push/pull/submit/wait-and-pull, `run_chain.sh` chaining SLURM jobs, witness JSONs under `results/`, `wiki/project/state.md`, CPU arrays on `--partition=ral`, pulls landing in the checkout. The assistant's `start-new-project` scaffold (`project.yaml` with `seed_policy: required`, `default_seed: 42`, `hpc/` copied from the assistant) is the project template. Neither repo mentions PyAutoCortex.

### 1.6 Assistant and workspace integration (`surveys/02 §1–§3, §5`)

Skill = one flat `skills/al_<task>.md` (Orient → Ask → Branch → Combine), wiki page in `wiki/core/concepts/` with `sources` + `pinned_commit`, a row in `skill_citation_map.md`, adapters regenerated by `install.sh --write-project-discovery`, recipe executed under `PYAUTO_TEST_MODE=1` before shipping; benchmark cards in `benchmarks/` with hidden truth. Workspace examples live under `scripts/<topic>/features/advanced/<feature>/` with `simulator.py`, `modeling.py`, README; scripts auto-simulate missing datasets; `cosmos_web_ring` is committed real data. The assistant's `al_simulate_dataset` Further-reading links are already stale (`surveys/02 §11`) and should be corrected in phase 6, not here.

## 2. Architecture

### 2.1 Division of responsibilities

| Layer | Owns | Does not own |
|---|---|---|
| **PyAutoGalaxy** | profile-level physics: projected mass inside an aperture for any mass object (grid-integrated, works for `Basis`), light-basis → mass-basis at a given M/L, halo normalisation solvers (κ_s for a target projected mass at fixed r_s; gNFW inner slope variants), the `MassBudget` dataclass (aperture + per-component fractions) | anything that knows about datasets, tracers, fits or provenance |
| **PyAutoLens** `autolens/twins/` | `ObservationSetup`, `ReferenceModel`, `Twin`, `Transformation`/`TransformationRecord`, `SimulatedTwin`, Einstein-radius apertures (tracer-level), the transformations catalogue, twin diagnostics and their plotter, provenance JSON | experiment scheduling, HPC, inference pipelines, the Euclid library |
| **PyAutoFit** | unchanged in phases 0–3: `Model`/`Instance`, `Result`, `Aggregator`, `samples_summary.json`; phase 4 may add a `recovery` comparison helper only if nothing in `af.Samples` already answers "truth vs posterior" | twin objects |
| **Science/twins** (Cortex project) | `library/` of reference models and labels, experiment configs, inference pipelines, HPC runs, results and reports, the Cortex ledger | reusable transformations or normalisation maths (if a script needs one, it moves to the library first) |
| **autolens_workspace** | `scripts/imaging/features/advanced/twins/` examples on public data (phase 6) | science conclusions |
| **autolens_assistant** | `skills/al_twin_<task>.md`, a `wiki/core/concepts/twins.md`, citation rows, a benchmark card (phase 6) | a new interface or any twin code |

Dependency direction stays PyAutoGalaxy ← PyAutoLens ← workspace ← assistant; `Science/twins` imports PyAutoLens only.

### 2.2 The objects (`al.twins`, names provisional, ruling R1)

```python
setup = al.twins.ObservationSetup.from_fit_directory(path)      # mask, psf, noise_map, pixel_scales, over-sampling, cosmology
ref   = al.twins.ReferenceModel.from_fit_directory(path, lens_id="EUCL-J…", labels=["massive_elliptical"], roles={"lens": "lens", "source": "source"})
ref.tracer                      # frozen al.Tracer with solved intensities (files/tracer.json)
ref.setup                       # ObservationSetup
ref.provenance                  # lens_id, labels, fit_path, dataset identity hashes, library versions, ingested_at
ref.output_to(library_dir)      # tracer.json, setup/ (fits), provenance.json, labels.yaml

twin = al.twins.Twin.baseline(ref)                      # ground truth == reference tracer, setup == reference setup
twin = twin.apply(al.twins.transform.ReplaceTotalMassWithStellarPlusDark(galaxy="lens", budget=…, dark=al.mp.NFWSph, …))
twin.tracer                     # ground truth
twin.records                    # [TransformationRecord, …] — requested, procedure, derived, side_effects, preserved
twin.with_setup(deeper_setup)   # same physics, another observation

sim = twin.simulate(seed=1)     # SimulatedTwin: dataset (al.Imaging), truth tracer, seed, simulator settings
sim.output_to(dir)              # data/noise_map/psf fits, truth_tracer.json, twin.json (reference pointer + records + versions + seed)
al.twins.SimulatedTwin.from_directory(dir)   # reload; re-simulating with the stored seed is bit-identical
```

- `ReferenceModel` is immutable; a `Twin` is a value: `apply` returns a new twin and appends a record. One reference, many twins; one twin, many simulations (different seeds or setups).
- `ObservationSetup` carries the *observed* noise map and PSF (the default twin reproduces the parent observation, ruling R2) and optionally `exposure_time` / `background_sky_level` for the Poisson route; `with_(...)` builds deeper or higher-resolution variants explicitly.
- `TransformationRecord` fields: `name`, `requested` (the parameters the scientist asked for), `procedure` (the normalisation convention as text plus derived numbers: aperture radius, reference mass, solved M/L, solved κ_s), `changed` (galaxy/component paths replaced), `side_effects` (anything else touched, for example shear kept, centre tied), `preserved` (properties deliberately held fixed, empty by default). Preservation is never implicit.
- Ground truth is `twin.tracer` serialised with `output_to_json`; parameters of interest (M/L, κ_s, r_s, slope, f_dark(θ_E)) are also written flat in `twin.json` so inference comparison needs no re-derivation.
- `Transformation` is a protocol with `apply(twin) -> (tracer, setup, record)`. Phase 0 ships only `Identity` (so the record chain and JSON are exercised); phase 3 ships the first real one. Composition is list order; nothing more.

### 2.3 Mass normalisation (the first transformation, phase 2–3)

Convention proposed for ruling R3/R4; all quantities projected, angular (arcsec), convertible with Σcr from the setup's cosmology and the galaxy redshifts.

1. **Aperture:** a circle of radius θ_E,parent centred on the replaced galaxy's mass centre, where θ_E,parent is `LensCalc.from_tracer(parent).einstein_radius_from(grid)` over *all* mass members (tracer-level, so it is defined for multi-galaxy parents and for non-SIE parents). The grid is the setup's lens-plane grid.
2. **Reference mass:** M_ref = projected mass of the *replaced component(s)* inside the aperture, by grid integration of their convergence (not of the whole tracer), so shear and other galaxies are untouched and unaffected.
3. **Stellar component:** `Basis` of `lmp.Gaussian` copied from the galaxy's light basis (centre, ell_comps, sigma, solved intensity per Gaussian), one shared M/L per galaxy: Υ = f_* M_ref / M_light(θ_E) where M_light is the same grid integral of the basis at Υ = 1.
4. **Dark component:** `NFWSph` (phase 2; elliptical NFW is a later transformation parameter) centred on the stellar centre, r_s fixed by the ruling (R4: fixed in kpc from a c(M) relation at the implied M200, iterated once, or a fixed physical value), κ_s solved by 1-D root find so M_NFW(θ_E) = (1 − f_*) M_ref. `gNFW` with a requested `inner_slope` uses the same solver.
5. **Record:** aperture radius, M_ref, M_light(Υ=1), Υ, r_s, κ_s, implied M200 and c, f_dark(θ_E), and the statement that shear, source and all other galaxies were left unchanged.
6. **Multi-galaxy:** `MassBudget` is per galaxy (`{"lens": …, "dwarf": …}`); phase 2 implements and tests the single-galaxy case and raises `NotImplementedError` for a budget naming more than one galaxy; the multi-galaxy convention is ruled in phase 5 with real systems in hand.

Analytic checks available for tests: the projected mass of a circular Gaussian inside R is 2π Υ I σ² (1 − e^{−R²/2σ²}); NFW projected mass inside R has the closed form in `AbstractgNFW`/`NFW` (`mass_angular_within_circle_from` by quad agrees); an SIE's projected mass inside its own θ_E equals π θ_E² in convergence units.

### 2.4 Three effects, three diagnostics (phase 3)

- Physical model: convergence and deflection difference maps, enclosed-mass profiles M(<R) for parent and twin, tangential critical curves and caustics of both (`LensCalc`).
- Predicted observation: Δχ²_image = Σ (I_twin − I_parent)² / σ² on the parent's masked grid with the parent's PSF, noise-free; and separately Δχ²_data = χ²(twin | data) − χ²(parent | data) via two `FitImaging` objects on the observed data (parametric sources only; pixelised sources are out of scope until a source-swap transformation exists). The two are different numbers and are reported as such.
- Recovered parameters: phase 4; a flat truth table in `twin.json` against `samples_summary.json`.

### 2.5 Provenance (lightweight, phase 0)

`twin.json` = `{reference: {lens_id, fit_path, dataset_sha256, ingested_at}, versions: {...}, records: [...], setup_overrides: {...}, seed, simulator: {...}}`, written beside the FITS by `SimulatedTwin.output_to`. The inference run's `Paths` directory gets a copy (`files/twin.json`) by the experiment script in phase 4, so the aggregator can join truth to posterior. No database, no registry service.

## 3. Detailed phase bodies

### Phase 0 — `autolens/twins/` core and the two PyAutoGalaxy primitives (library only)

PyAutoGalaxy (one PR): `ag.quantity`/`operate`-level `mass_angular_within_circle_via_grid_from(mass_obj, radius, centre, grid)` for any object with `convergence_2d_from` (profile, basis, galaxy, galaxies), with a test that it matches `mass_angular_within_circle_from` for `Isothermal` and `NFWSph` to 1e-3 and the closed form for a Gaussian; `Basis.mass_basis_from(mass_to_light_ratio)` (instance-level `lp.Gaussian` → `lmp.Gaussian`), tested against `mass_light_dark_basis_from`'s field copying.

PyAutoLens (one PR, after the PyAutoGalaxy PR merges or against its branch): `autolens/twins/{setup.py, reference.py, twin.py, record.py, simulate.py, transform/{__init__,identity}.py}` with `__init__` exports and `from . import twins` in `autolens/__init__.py`; `ObservationSetup.from_dataset` / `from_fit_directory` (reuse `agg_util.mask_header_from` and the `_imaging_from` recipe); `ReferenceModel.from_fit_directory` / `from_result`; `Twin.baseline`, `apply`, `with_setup`, `simulate(seed, noise="observed"|"poisson")`; `SimulatedTwin.output_to` / `from_directory`; `Identity`; `dictable` round trips. Tests on the 7x7 fixtures: a fixture fit directory (built in `data_temp` with `af.DirectoryPaths` as in `test_autolens/analysis/test_analysis.py:157-177`) ingests; baseline twin's noise-free image equals the parent tracer's image bit-for-bit; two simulations with the same seed are identical and with different seeds differ; reload reproduces; provenance JSON validates. Docs: a `docs/api/twins.rst` stub. Witness: the header witness of the ledger.

### Phase 1 — Birth of `Science/twins` and the first baseline twin of a real fitted lens

Human: adds the `twins` row to `PyAutoCortex/projects.yaml` (code change, human turn) and supplies the first fit directory (MGE light + SIE + shear + MGE source; a Euclid lens, or the assistant's public `cosmos_web_ring` fit as a stand-in). Session: `cortex.py new twins --summary …`; scaffold the project with the assistant's `start-new-project` conventions (`project.yaml` seed policy, `hpc/` template from the assistant, `wiki/project/state.md`); `library/<lens_id>/` from `ReferenceModel.output_to`; `scripts/baseline_twin.py` (ingest → baseline → simulate seed 1 → diagnostic figure: parent model image, simulated image, residual / noise → reload → re-simulate → assert identical); `library/library.yaml` with multi-label entries. Record the run in the Cortex ledger. Witness: `Δχ²_image(parent, baseline) == 0` on the common grid and the seed-1 re-simulation is bit-identical after reload.

### Phase 2 — Mass-normalisation mathematics and `MassBudget` (PyAutoGalaxy)

`MassBudget(aperture, fractions)`; `Aperture` protocol with `CircularAperture(radius, centre)`; solvers `mass_to_light_ratio_for_mass_from(basis, mass, aperture, grid)` and `kappa_s_for_mass_from(dark_cls, mass, aperture, scale_radius, centre, grid, **fixed)`; gNFW slope passes through `fixed`. Tests: closed forms above; monotonicity; a 50/50 budget on an `Isothermal` reference reproduces M_ref to 1e-4; `NotImplementedError` for multi-galaxy budgets. Documentation: `docs/` page stating the convention in the words of §2.3, which the record quotes verbatim.

### Phase 3 — `ReplaceTotalMassWithStellarPlusDark` and the diagnostics (PyAutoLens)

`EinsteinRadiusAperture(parent_tracer, grid)` (tracer-level θ_E via `LensCalc`); the transformation (galaxy name, light component name, budget, dark profile class and fixed parameters, keep-shear flag defaulting to keep-and-record); the record; `al.twins.compare(parent_twin, twin)` returning convergence/deflection difference arrays, M(<R) profiles, critical curves, Δχ²_image, and `compare_to_data(twin, dataset)` for Δχ²_data; a plotter under `autolens/twins/plot/` or the existing `aplt` conventions (ruling R6). Tests on fixtures: the transformed twin has f_dark(θ_E) = 0.5 ± 1e-3; the SIE's θ_E recomputed on the twin is reported, not asserted equal; the record is complete and JSON round trips.

### Phase 4 — First identifiability experiment (Science/twins; local → RAL)

`experiments/stellar_dark_identifiability/`: config (lens_id, budget, dark class, seed list, setup overrides), `simulate.py`, `fit.py` building the inference model from the twin (`Basis` of `lmp_linear.Gaussian` with the intensities fixed to the solved values and one free M/L, `NFWSph` free κ_s and r_s with the centre tied to the light, shear free, MGE source free via `mge_model_from`), Nautilus through the project's `hpc/` template, `recover.py` writing a truth-vs-posterior table (`samples_summary.json`) per seed; second configuration with `gNFWSph` and free `inner_slope`. Local smoke under `PYAUTO_TEST_MODE=1` first; one RAL array (CPU on `--partition=ral`) with an explicit human go; Cortex `run`/`done`/`result` lines; the human writes the lesson. Witness: on the no-misspecification fit the truth M/L and κ_s lie inside the 3σ posterior intervals for every seed; the gNFW run reports the posterior width on `inner_slope`.

### Phase 5 — Library ingestion of the Euclid sample and multi-galaxy twins

As the ~40 fits arrive in batches: `scripts/ingest.py` (one `ReferenceModel.output_to` per fit, labels from a CSV, dataset identity hashes); the library index; baseline twins for every entry as a regression sweep (Δχ²_image = 0); the first dwarf-overlapping-arc and multi-galaxy references exercised through `Twin` (roles, extra galaxies, per-galaxy budgets); the multi-galaxy normalisation convention ruled by the human with real systems (R7) and implemented in PyAutoGalaxy/PyAutoLens as a follow-up library phase. Data stays in the private project; nothing proprietary enters library tests or the workspace.

### Phase 6 — Workspace examples and the assistant skill

`autolens_workspace/scripts/imaging/features/advanced/twins/{start_here.py, transform_stellar_dark.py, README.md}` on `cosmos_web_ring` using the assistant's committed fit (or a fit produced by the example's own `modeling.py` under the smoke profile); smoke rows; notebooks regenerated. Assistant: `skills/al_twin_what_if.md` (Orient: which reference, which transformation, which setup; Ask: budget, dark profile, seed, fit family; Branch: baseline / stellar+dark / deeper observation; Combine: the experiment script), `wiki/core/concepts/twins.md` with pinned sources, a `skill_citation_map.md` row, adapters regenerated, the recipe executed under `PYAUTO_TEST_MODE=1`, the stale `al_simulate_dataset` links fixed in passing; a benchmark card with hidden truth only after the human has used the skill once. Everything the skill does calls `al.twins`; it writes no bespoke physics.

### Later, unscoped (filed as drafts when a phase needs them)

Transformations: cored halo (`cNFW`, `gNFW` slope 0), subhalo injection (`NFWMCRLudlowSph`), line-of-sight halos (`LOSSampler.galaxies_and_fields_from(seed)`), M/L gradient (`lmp.GaussianGradient`), angular complexity (per-Gaussian position-angle twist), source swap, shear change, observing-setup variants (deeper, finer pixels, other PSF). Experiment grids and repeated noise realisations; Insight records for twin experiments; the `hpc-campaign` and `results-library` epics own run-time status and post-run indexing. Pixelised-source references (needs a source-image interpolation route; the `pixelization/fit.py` sketch exists).

## 4. Decisions for the human (recommendations)

- **R1 Package and names.** `autolens/twins/` exported as `al.twins`, objects `ObservationSetup`, `ReferenceModel`, `Twin`, `SimulatedTwin`, `TransformationRecord`; PyAutoGalaxy gets no `twins` package, only primitives. *Recommend: accept.*
- **R2 Default noise model of a twin.** Reproduce the parent observation: Gaussian noise drawn from the observed noise map (new `noise="observed"` route), with the Poisson route available when exposure time and sky are supplied. *Recommend: observed by default.*
- **R3 Reference aperture and mass convention.** Circle of radius θ_E,parent (tracer-level, critical-curve area) centred on the replaced galaxy; M_ref is the replaced component's projected mass inside it by grid integration; shear and other galaxies untouched. *Recommend: accept; document in PyAutoGalaxy.*
- **R4 Halo shape and scale radius in the first transformation.** `NFWSph` centred on the light; r_s fixed. Options: a fixed physical value (e.g. 10 × the light's half-mass radius), or from a Ludlow c(M200) relation at the M200 implied by the solved κ_s, iterated once. *Recommend: fixed physical r_s for phase 2–4 (one fewer moving part); the c(M) route as a later transformation parameter.*
- **R5 First real lens.** A Euclid fit the human supplies, or the public `cosmos_web_ring` fit as a stand-in until one exists. *Recommend: phase 0 tests on fixtures, phase 1 on whichever fit exists first, phase 6 on `cosmos_web_ring`.*
- **R6 Plotting home.** `autolens/twins/plot/` following the `aplt` conventions versus bare matplotlib in the science project. *Recommend: library plotter, since the diagnostics are a reusable capability the assistant will cite.*
- **R7 Multi-galaxy normalisation.** Deferred to phase 5 with real systems; phase 2 raises for multi-galaxy budgets rather than guessing.
- **R8 Where the library lives and what is public.** Reference models and Euclid data in the private `Science/twins` project; only public data (`cosmos_web_ring`) in workspace and assistant examples. *Recommend: accept.*

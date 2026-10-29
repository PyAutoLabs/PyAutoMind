- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/810
- completed: 2026-10-29
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/811
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/811
- epic: lenstwin (phase 4a; ledger draft/feature/autolens/lenstwin_epic.md)
- summary: Merge bf18d5c (human lifted the draft HOLD 2026-10-29). `al.twins.stellar_dark_model_from(twin, galaxy=None, *, source_model, free_scale_radius=True, free_inner_slope=None, free_shear=True, priors=None)` builds the no-misspecification af.Collection from the last ReplaceTotalMassWithStellarPlusDark record (lmp.Gaussian basis, fixed geometry + intensities, one tied M/L; dark on the light centre, free kappa_s/scale_radius, gNFW inner_slope; MassField shear layout as DR1; other galaxies fixed). `truth_paths_from`, `DEFAULT_PRIORS` (never truth-derived), `recovery_table_from(samples, truth, sigma=3)` → RecoveryTable (all_inside, to_csv). Also fixed `keep_shear=False` for shear held inside a MassField field (49c365504).
- tests: twins 56 passed; full suite 1013 passed / 1 xfailed; CI green on 49c365504 (3.12, 3.13, nojax, docs).
- traps: index samples with `samples.paths` (grouped tied paths), never `model.paths` (one entry per tied path → mis-indexed columns); synthetic SamplesPDF need weights 1/N; NFWSph exposes inner_slope=1 so gNFW-ness is read from the constructor signature.

## Original prompt

# LensTwin phase 4a: build the inference model from a twin (`al.twins.model`) and compare posteriors with the injected truth (`al.twins.recovery`)

Type: feature
Target: autolens
Repos:
- PyAutoLens
Themes:
- mge
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: (1) `al.twins.model.stellar_dark_model_from(twin, galaxy="lens", ...)` returns an `af.Collection` whose lens galaxy carries a `Basis` of `lmp.Gaussian` models with centre, ell_comps, sigma and intensity fixed to the twin's solved values and ONE shared free `mass_to_light_ratio`, a dark profile (`NFWSph` by default, `gNFWSph` with free `inner_slope` on request) centred on the light with free `kappa_s` and `scale_radius`, free shear when the twin has one, and the caller's source model; `model.instance_from_prior_medians()` builds, and the model instance at the truth values reproduces the twin tracer's convergence to 1e-10. (2) `al.twins.recovery.recovery_table_from(samples, truth, sigma=3.0)` lists each truth parameter's value, median PDF and the lower/upper bounds at `sigma`, with an `inside` flag; a unit test on synthetic samples covers in and out. (3) A test-mode (`PYAUTO_TEST_MODE=1`) end-to-end run on a simulated reference (simulate → twin → model → Nautilus → recovery table) runs in under a minute
Review-minutes: 30
Unattended: never
Epic: lenstwin
Phase: 4
Parent: draft/feature/autolens/lenstwin_epic.md
Blocked-by: none (library phases 0, 2, 3 are on `main`). Human instruction 2026-10-29: open the PR as a DRAFT and do not merge until the human says so
Filed: 2026-10-29
Issued: 2026-10-29
Issue: https://github.com/PyAutoLabs/PyAutoLens/issues/810

Library prep for phase 4 (`draft/research/autolens/lenstwin_p4_identifiability.md`, step 3 says "if it is a reusable gap, file a small library prompt rather than writing it into the science script"). It is a reusable gap: `ag.analysis.chaining_util.mass_light_dark_basis_from` builds the equivalent model from a light-pipeline `Result`, but a twin has no `Result`; it has an instance tracer and a flat `truth`. Without this, every science script hand-builds the same no-misspecification model.

## Scope (PyAutoLens `autolens/twins/`)

- `model.py`: `stellar_dark_model_from(twin, galaxy, *, source_model, dark_cls=None, free_inner_slope=None, free_scale_radius=True, free_shear=True, priors=None)`. Reads the stellar basis and dark profile the stellar-dark transformation put on the twin (via the last `ReplaceTotalMassWithStellarPlusDark` record's `procedure`, not by guessing attribute names), ties one `mass_to_light_ratio` across members exactly as `mass_light_dark_basis_from` does, fixes the dark centre to the light centre, and keeps every other galaxy as a fixed instance. Default priors are broad, fixed and documented in the docstring, and never centred on the truth (a prior that knows the answer defeats the experiment). Pick them from each parameter's units (e.g. M/L and κ_s log-uniform over several decades; r_s uniform over a physically sensible arc-second range; inner_slope uniform 0–2) and accept a `priors` override dict.
- `recovery.py`: `recovery_table_from(samples, truth, paths=None, sigma=3.0)` → a list of rows (or a small `RecoveryTable` with `to_csv` and `all_inside`), mapping truth keys (`mass_to_light_ratio`, `kappa_s`, `scale_radius_arcsec`, `inner_slope`) to model paths through a default map that `stellar_dark_model_from` also publishes (one source of truth for the paths). Uses `samples.median_pdf()` and `samples.values_at_sigma(sigma)` from PyAutoFit; reads `twin.json` truth with `al.twins.SimulatedTwin`'s loader if one exists, else plain JSON.
- Export both under `al.twins`; tests under `test_autolens/twins/`; a short section in the `al.twins` module docstring.

Out of scope: the Science experiment (phase 4 proper), multi-galaxy models (phase 5), workspace example (phase 6).

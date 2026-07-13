## latent-module-autogalaxy
- issue: https://github.com/PyAutoLabs/PyAutoGalaxy/issues/439
- completed: 2026-05-23
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/441
- notes: Shipped the first-class latent variable API in PyAutoGalaxy — the dependency root of the broader `z_features/latent_refactor.md` epic. New module `autogalaxy/imaging/model/latent.py` houses helpers (`ab_mag_via_flux_from`, `flux_mujy_via_ab_mag_from`), a flat `LATENT_FUNCTIONS` registry, the `latent_keys_enabled()` config reader, and one concrete latent (`total_galaxy_0_flux_mujy`). New `autogalaxy/config/latent.yaml` provides the user-facing on/off toggle. `AnalysisImaging` gains a `LATENT_KEYS` `@property` (reads `conf.instance["latent"]` at call time) and a `compute_latent_variables(parameters, model)` method that returns a tuple positionally aligned to keys, with a `NotImplementedError` short-circuit when the enabled set is empty so autofit's existing `except NotImplementedError: return None` path skips cleanly. Library tests 917/917 pass; cross-workspace smoke sweep 42 pass / 0 fail / 2 pre-existing skips across all six workspaces with the worktree active. Three gotchas worth the memory writes: (1) autoconf lowercases yaml dict keys at read time, so the latent ships as `total_galaxy_0_flux_mujy` (lowercase j) — that leaks through to the latent.csv column header (saved as `feedback_autoconf_lowercases_yaml_keys`); (2) `compute_latent_samples` runs on every fit (`latent_after_fit: true` default in `output.yaml`), so on-by-default would have crashed every existing fit that doesn't pass `magzero` — flipped library default to `false` mid-PR, only the test config keeps it on; (3) library module placement landed on `<dataset>/model/latent.py` (with the model API) rather than a top-level `<lib>/latent.py`, per user clarification — also saved as `feedback_latent_modules_colocate_with_model_api`. Workspace impact analysis: zero migration needed — all existing subclasses of `ag.AnalysisImaging` (csv_make/png_make/fits_make under `autogalaxy_workspace/scripts/guides/results/workflow/`) shadow the new attribute/method, and `al.AnalysisImaging` doesn't inherit from ag's, so the euclid pipeline and autolens workspace are unaffected. Follow-up sub-prompts still pending in `PyAutoPrompt/z_features/latent_refactor.md`: PyAutoLens lensing latents, euclid migration, workspace tutorials, smoke test, profiling package, prior-mapping investigation.

## Original prompt

# Add first-class latent-variable modules to PyAutoGalaxy

## Context

Parent epic: [`PyAutoPrompt/z_features/latent_refactor.md`](../z_features/latent_refactor.md).

Currently, anyone who wants latent variables out of a PyAutoGalaxy fit must subclass `AnalysisImaging`, hand-write a `LATENT_KEYS` list, and hand-write a `compute_latent_variables` method (see `autogalaxy_workspace/scripts/guides/results/workflow/csv_make.py:140-160` and the heavier reference in `euclid_strong_lens_modeling_pipeline/util.py:306-490`). This task promotes that into first-class library API so users can opt into a curated catalogue of galaxy latents via config, and so each latent has a single home with docstrings + unit tests.

This is the **library dependency root** of the broader latent-refactor epic. Sub-prompts #2, #3, #5, #7, #8 all build on what's defined here.

## Task

1. **Create `autogalaxy/analysis/latent.py`** — galaxy-level / tracer-agnostic latents (anything that derives only from a `Plane` / galaxies list, not from imaging arrays). Each latent is a single function taking `(instance, xp)` (or similar — finalize during implementation), with a one-paragraph docstring explaining what it is and when it's useful.

2. **Create `autogalaxy/imaging/model/latent.py`** — imaging-derived latents (need the image array from a `FitImaging`). Examples from the euclid reference: total galaxy flux from image, magzero-converted muJy fluxes (see `ab_mag_via_flux_from` / `flux_mujy_via_ab_mag_from` helpers in `euclid_strong_lens_modeling_pipeline/util.py` — port these into PyAutoGalaxy where they belong).

3. **Create `autogalaxy/config/latent.yaml`** — flat dict of `latent_key: bool` toggles, all defaulting `True`. Mirror the structure of `autogalaxy/config/output.yaml`.

4. **Wire `AnalysisImaging`** (`autogalaxy/imaging/model/analysis.py`):
   - At init (or as a cached `@property`), read `config/latent.yaml`.
   - Build `LATENT_KEYS = [k for k, on in latent_yaml.items() if on]` — filtered, ordered.
   - `compute_latent_variables` must return a dict containing **only the enabled keys**, in the **same order as `LATENT_KEYS`** (critical — PyAutoFit zips positionally with vmap output at `autofit/non_linear/analysis/analysis.py:285`).

5. **Unit tests** at `test_autogalaxy/analysis/test_latent.py` (and an imaging-flavour counterpart). Minimum coverage:
   - One test per latent category that values are sensible against a known toy model.
   - Toggle behaviour: disabling a key removes it from both `LATENT_KEYS` and the dict.
   - **No JAX in unit tests** — per memory `feedback_no_jax_in_unit_tests`. Cross-xp checks belong in workspace_test (sub-prompt #7).

## Where to look

- **PyAutoFit hook (do not modify):** `autofit/non_linear/analysis/analysis.py` lines 34 (`LATENT_KEYS`), 170 (`compute_latent_samples`), 285 (vmap positional zip).
- **Existing JAX-aware latent helper to delegate to:** `PyAutoGalaxy/autogalaxy/operate/lens_calc.py:1520` (`einstein_radius_jit_from`). Reuse, do not reimplement.
- **`LATENT_BATCH_MODE` constraint:** `PyAutoGalaxy/autogalaxy/analysis/analysis/dataset.py:28` is `"jit"`. Do not change; lensing latents downstream depend on it (also for sub-prompt #2).
- **Reference implementation to mine:** `euclid_strong_lens_modeling_pipeline/util.py:306-490` — the full LATENT_KEYS list + `compute_latent_variables` body. Pick the galaxy-only / image-derived bits here; the lensing-only bits (magnification, effective Einstein radius, lensed source flux) belong in sub-prompt #2.
- **Config dir layout to mirror:** `PyAutoGalaxy/autogalaxy/config/output.yaml`.

## Verification

```bash
source ~/Code/PyAutoLabs-wt/<task-name>/activate.sh
cd PyAutoGalaxy
pytest test_autogalaxy/analysis/test_latent.py -x -v
pytest test_autogalaxy/imaging/test_latent.py -x -v
```

Then a quick end-to-end manual check using `autogalaxy_workspace/scripts/guides/results/workflow/csv_make.py` (or similar) — confirm that with the new yaml, the user no longer needs to subclass `AnalysisImaging` to get a sensible default latent set; the same csv is produced.

## Affected repos

- PyAutoGalaxy (primary)

## Suggested branch

`feature/latent-module-autogalaxy`

## Notes

- Start as single `.py` files (~5-6 latents on this side, per the euclid reference). If either grows past ~150 lines, convert to a `latent/` package with one file per latent category.
- **No PyAutoFit changes.** The config-driven on/off lives in `AnalysisImaging` subclass logic; PyAutoFit core stays dataset-agnostic.
- Order matters in `LATENT_KEYS` because of the vmap positional zip. Sort keys deterministically (yaml insertion order or alphabetical — pick one and document it).
- Workspace configs override library defaults (per memory `feedback_workspace_config_default_true`): the new library `latent.yaml` defaults need mirroring into each workspace's `config/latent.yaml` in their respective workspace sub-prompts. Note this for follow-up.

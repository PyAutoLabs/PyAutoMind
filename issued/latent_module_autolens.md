# Add first-class lensing latent-variable modules to PyAutoLens

## Context

Parent epic: [`PyAutoPrompt/z_features/latent_refactor.md`](../z_features/latent_refactor.md).
Depends on the PyAutoGalaxy spine in [`autogalaxy/latent_module.md`](../autogalaxy/latent_module.md).

PyAutoGalaxy gets galaxy-level / image-flux latents. This task adds the **lensing-specific** latents that need a `Tracer` (mass model + sources): magnification, effective Einstein radius, lensed source flux, total source flux. Today these live in `euclid_strong_lens_modeling_pipeline/util.py:306-490` as part of a bespoke `AnalysisImaging` subclass. After this task lands, the euclid pipeline (sub-prompt #3) can drop its custom subclass and inherit the curated set.

## Task

1. **Create `autolens/analysis/latent.py`** — tracer-derived, dataset-agnostic latents. Examples from the euclid reference:
   - `magnification` — derived from the `Tracer` mass model
   - `effective_einstein_radius` — **must delegate to `LensCalc.einstein_radius_jit_from()`** at `PyAutoGalaxy/autogalaxy/operate/lens_calc.py:1520`. Do not reimplement the ZeroSolver loop here.

2. **Create `autolens/imaging/model/latent.py`** — lensing imaging-derived latents that need a `FitImaging`:
   - `total_lens_flux`, `total_lens_flux_{N}_fwhm` (aperture fluxes — port the FWHM aperture logic from `euclid_strong_lens_modeling_pipeline/util.py`)
   - `total_lensed_source_flux`, `total_source_flux`
   - Use the magzero → muJy helpers added to PyAutoGalaxy in sub-prompt #1 (`ab_mag_via_flux_from`, `flux_mujy_via_ab_mag_from`).

3. **Create `autolens/config/latent.yaml`** — flat dict of `latent_key: bool`, default `True`. Mirror `autolens/config/output.yaml`.

4. **Wire `AnalysisImaging`** (`autolens/imaging/model/analysis.py`):
   - Same pattern as sub-prompt #1: read `config/latent.yaml`, build `LATENT_KEYS`, filter the `compute_latent_variables` return dict.
   - The lens `AnalysisImaging` should also include the **PyAutoGalaxy latents inherited via composition** (so users get galaxy + lens latents together without having to subclass twice). Choose between `LATENT_KEYS = autogalaxy_keys + lens_keys` at the subclass level, vs explicit super().compute_latent_variables() merge. Final shape is up to the implementer — document the choice.
   - **Preserve `LATENT_BATCH_MODE = "jit"`** (`autogalaxy/analysis/analysis/dataset.py:28`). Lensing latents go through `ZeroSolver` and cannot use vmap.

5. **Unit tests** at `test_autolens/analysis/test_latent.py` (+ imaging counterpart). Same coverage shape as sub-prompt #1, plus:
   - Test that `effective_einstein_radius` actually calls into `LensCalc.einstein_radius_jit_from` (mock or spy).
   - Test the closure-caching at `lens_calc.py:1580-1586` is not broken by repeat calls (verify cache hit on second invocation with same tracer shape).

## Where to look

- **PyAutoFit hook (do not modify):** `autofit/non_linear/analysis/analysis.py:34, 170, 285`.
- **Einstein radius JAX helper to delegate to:** `PyAutoGalaxy/autogalaxy/operate/lens_calc.py:1520-1537` and the cache at 1580-1586.
- **`LATENT_BATCH_MODE` constraint:** `PyAutoGalaxy/autogalaxy/analysis/analysis/dataset.py:28` — `"jit"`, not `"vmap"`. Do not change.
- **Reference implementation:** `euclid_strong_lens_modeling_pipeline/util.py:306-490`. The lensing-specific bits are what move here. Galaxy-only bits live in sub-prompt #1.
- **Config layout:** `PyAutoLens/autolens/config/output.yaml`.

## Verification

```bash
source ~/Code/PyAutoLabs-wt/<task-name>/activate.sh
cd PyAutoLens
pytest test_autolens/analysis/test_latent.py -x -v
pytest test_autolens/imaging/test_latent.py -x -v
```

End-to-end manual check: run any `autolens_workspace/scripts/imaging/modeling/start_here.py` example with the new yaml; confirm `latent.csv` contains the curated key set.

## Affected repos

- PyAutoLens (primary)
- PyAutoGalaxy (only if sub-prompt #1 left helper utilities or composition seams that need a small follow-up — should be rare; if so, ship as part of this branch)

## Suggested branch

`feature/latent-module-autolens`

## Notes

- **Do not start until sub-prompt #1 has shipped.** It defines the helper functions (`ab_mag_via_flux_from` etc.) and the config-reading pattern this task depends on.
- Same single-file-per-side starting point as #1 (~4 latents on the lensing tracer side, ~5 on the imaging side). Split into `latent/` package only if growth warrants.
- Per memory `feedback_jax_closure_cache_busts`: when delegating to `einstein_radius_jit_from`, ensure the same `(closure, solver)` pair is reused across calls — don't construct a fresh closure inside `compute_latent_variables`.
- Per memory `feedback_no_silent_guards`: if `magzero` (or any required kwarg) is missing for a latent, raise loudly. Don't return `None` or `nan` silently.

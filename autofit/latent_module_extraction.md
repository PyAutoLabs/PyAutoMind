# Extract latent-variable machinery out of analysis.py into a dedicated latent.py

## Problem

`autofit/non_linear/analysis/analysis.py` has grown bulky, and a large fraction
of its size is the generic latent-variable engine — which is conceptually a
self-contained concern. PyAutoGalaxy and PyAutoLens already keep their latent
*registries* in dedicated `analysis/latent.py` modules
(`autogalaxy/imaging/model/latent.py`, `autolens/analysis/latent.py`); the
PyAutoFit-side generic *machinery* has no such home and instead lives inline in
the `Analysis` base class.

This makes `analysis.py` harder to read and the latent logic harder to test in
isolation. Two recent bug-fix passes (per-batch NaN masking; quantile n=1 /
latent-exception / anti-correlated-NaN salvage) both had to surgically edit a
long method buried in `analysis.py`.

## What currently lives in analysis.py (the latent surface to move)

- `Analysis.compute_latent_samples(self, samples, batch_size=None)` — the big
  batched method: vmap/jit/numpy dispatch (`LATENT_BATCH_MODE`), the
  test-mode NaN injection hook call, accumulation, and the global
  col-then-row masking + greedy salvage. This is the bulk.
- `Analysis.compute_latent_variables(self, parameters, model)` — abstract stub
  (raises `NotImplementedError`); subclasses override it.
- Class attributes `LATENT_KEYS` (default `[]`) and `LATENT_BATCH_MODE`
  (default `"vmap"`), plus the comment block explaining the jit override.
- Helpers it depends on: `simple_model_for_kwargs`, `Sample`, `skip_latents`
  (already in `autoconf.test_mode`), `inject_latent_nans`
  (`autoconf.test_mode`), `exc.FitException`.

Callers to keep working:
- `autofit/non_linear/search/updater.py::SearchUpdater._compute_latent_samples`
  calls `analysis.compute_latent_samples(...)` and `latent_samples.summary()`.
- PyAutoGalaxy/PyAutoLens `AnalysisImaging` override `compute_latent_variables`
  and set `LATENT_BATCH_MODE = "jit"` / `LATENT_KEYS` — these overrides must
  keep working unchanged.

## Requested change

Move the generic latent engine into a new module, e.g.
`autofit/non_linear/analysis/latent.py`, mirroring the per-package
`analysis/latent.py` convention. Pick whichever shape is cleanest and keeps the
public surface identical:

- **Option A (free function):** `compute_latent_samples(analysis, samples, batch_size=None)`
  in `latent.py`, and have `Analysis.compute_latent_samples` become a thin
  delegating wrapper (`return latent.compute_latent_samples(self, samples, batch_size)`).
  `compute_latent_variables`, `LATENT_KEYS`, `LATENT_BATCH_MODE` stay on `Analysis`
  (they're the per-analysis interface), but the heavy batching/masking logic moves out.
- **Option B (helper class):** a `LatentComputer`/`LatentSamples` helper in
  `latent.py` that takes the analysis and does the work; `Analysis.compute_latent_samples`
  instantiates and calls it.

Prefer the option with the smallest blast radius on subclasses. The
`Analysis`-level public API (`compute_latent_samples`, `compute_latent_variables`,
`LATENT_KEYS`, `LATENT_BATCH_MODE`) must remain importable/overridable exactly as
today so PyAutoGalaxy/PyAutoLens need no changes.

## Tests to move

Relocate the latent tests out of the general analysis test file into a
dedicated test module mirroring the new source layout:

- Move the latent tests currently in
  `test_autofit/analysis/test_latent_variables.py` (and any latent cases that
  ended up elsewhere) into e.g. `test_autofit/non_linear/analysis/test_latent.py`
  (or keep `test_latent_variables.py` but co-locate with the new module — match
  whatever the source move implies).
- Keep the existing coverage intact: per-batch consistency, FitException skip,
  arbitrary-exception skip, anti-correlated-NaN salvage, single-survivor
  summary (quantile n=1), complex/dotted keys, `LATENT_BATCH_MODE` validation.
- The `quantile` n=1 test stays in `test_autofit/non_linear/samples/test_pdf.py`
  (it's a `pdf.py` concern, not latent-specific).

## Acceptance

- `analysis.py` no longer contains the batching/masking body (only the thin
  interface), measurably slimmer.
- `pytest test_autofit` green (excluding the pre-existing `nss` optional-dep
  ImportErrors).
- No changes required in PyAutoGalaxy/PyAutoLens; their `AnalysisImaging`
  latent overrides and the three `*_workspace_test/latent_nan_robustness.py`
  integration guards still pass.
- Pure refactor — no behaviour change.

## Notes / context

This is a follow-up to the latent NaN-robustness fixes (PyAutoFit #1310, #1311).
Sequence it AFTER those have landed (they have) so the move starts from the
fixed code. Pure-mechanical execution is a good Sonnet-delegation candidate once
the module shape (Option A vs B) is decided in Opus.

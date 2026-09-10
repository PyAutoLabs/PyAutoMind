## latent-integration-smoke
- issue: https://github.com/PyAutoLabs/autolens_workspace_test/issues/315
- completed: 2026-09-10
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/316 (merge 30799944)
- summary: |
    Two first-class latent smokes under `scripts/misc/latent/`, both listed in
    `smoke_tests.txt` (29 -> 31 entries), plus a stale-pointer fix in the
    `config/latent.yaml` header comment.

    **`misc/latent/latent_integration_smoke.py` (NumPy).** `ENV: real_search full_datasets`.
    A real `af.Nautilus` search on `al.AnalysisImaging(use_jax=False)` writes a real latent
    block to disk, then a `af.Drawer` pixelized stage (`RectangularUniform` + `reg.Constant`)
    exercises `_pixelized_source_flux`. It asserts on disk and through the catalogue path:
    `Aggregator.from_directory(..., completed_only=True, unzip_temporary=True)` round-trips both
    stages; `af.AggregateCSV(agg, strict=True)` saves and reloads with the exact enabled key set
    from `config/latent.yaml` (a NaN latent is a missing key, not a null); 3-sigma strictly
    brackets 1-sigma; MaxLogLikelihood differs from the Median (the PyAutoFit#1598 defect);
    pixelized `magnification` is finite and positive (PyAutoLens#727/#728); the retired
    `latent.` prefix raises `KeyError` under `strict=True` (pipeline#65); and a sibling
    `<hash>/files/` directory beside the zip does not hide the completed zip (PyAutoFit#1602).

    **`misc/latent/latent_integration_smoke_jax.py` (JAX).** `ENV: real_search full_datasets jax`.
    The model carries a real `model.add_assertion(...)`; the latent block is written and
    `search.log` carries no "raised on N of M samples" engine warning (PyAutoLens#734 /
    PyAutoFit#1600).

    Runtimes 14.3 s and 19.6 s measured through the CI resolver after a speed pass
    (30.0 -> 14.3 s NumPy, 20.0 -> 19.6 s JAX), well under the 300 s CI cap. `n_networks=1`
    was the decisive lever. Two alternatives were tried and rejected: **Emcee** as the cheap
    real search — its auto-correlation check slices a fixed 100-step window, so it cannot be
    shortened below that; and **PDF latent draws** as a cheaper 3-sigma source — equal-weight
    draws collapse the 3-sigma tails onto the 1-sigma ones and the bracketing assertion
    stops discriminating.

    Witness met: all four guarded regressions were reintroduced by monkeypatch and each failed
    its script as designed; the local `run_smoke.py` summary count rose by exactly 2 with a
    `[PASS]` line each (31/31); CI green on every leg (`smoke / changes`, `smoke (3.12)` 6m33s,
    `smoke (3.13)` 5m57s).
- trap: |
    **Any `PYAUTO_TEST_MODE` level skips latent writes.** `autonerves.test_mode.skip_latents()`
    suppresses all latent writing at `PyAutoFit/autofit/non_linear/search/updater.py:249`, so
    `PYAUTO_TEST_MODE=1` is as useless as `2` here. The `ENV: real_search full_datasets`
    declaration is mandatory, and both scripts assert `not skip_latents()` and
    `PYAUTO_SMALL_DATASETS != "1"` up front so a misconfigured profile cannot pass vacuously.

    **`SearchOutput.id` is not the on-disk identifier directory.** The obvious way to join the
    `AggregateCSV` rows back to the two stages does not work; the rows are keyed by an explicit
    label column added to the CSV instead.

    **`af.Drawer` returns plain `Samples`** — no median, no sigma bounds — so only the
    MaxLogLikelihood columns can be asserted non-blank on the pixelized stage's row, and that
    is asserted explicitly rather than assumed.

    **Under `remove_files: true` the aggregator must run with `unzip_temporary=True`**, or the
    in-place extraction litters the output tree for the next run.
- notes: |
    Bug found and filed rather than fixed here: `af.Model.from_instance` writes non-constructor
    attributes into `model.json`, which then fail to round-trip —
    `draft/bug/autofit/model_from_instance_roundtrip_unexpected_kwargs.md`.

    The old bypass-mode `scripts/misc/latent/latent_variables_smoke.py` is kept as-is; it runs
    under the smoke profile's `PYAUTO_TEST_MODE=2` and catches a different (much weaker) class
    of failure.

    Sibling tasks of the same plan, both merged: A1, the PyAutoFit aggregator sibling-dir /
    `preserve_in_zip` fix (PyAutoFit#1602, `complete/2026/09/aggregator-sibling-dir-zip.md`);
    A2, the euclid pipeline's sibling-dir aggregator assertion
    (euclid_strong_lens_modeling_pipeline#67). This task was the library-first gated third.

## Original prompt

# autolens_workspace_test: a first-class latent-variable integration smoke that writes, aggregates and catalogues real latents

Type: test
Target: autolens_workspace_test
Repos:
- autolens_workspace_test
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: `misc/latent/latent_integration_smoke.py` and `misc/latent/latent_integration_smoke_jax.py` are listed in `smoke_tests.txt`, the local `/smoke_test autolens_workspace_test` summary count rises by exactly 2 with a `[PASS]` line each, each runs in under 150 s locally and passes both CI Python legs under the 300 s cap, and each is shown to FAIL when its guarded regression is reintroduced (recorded in the PR).
Review-minutes: 25
Unattended: ready
Filed: 2026-09-10
Issued: 2026-09-10

## Why

Between June and September 2026 four latent-variable defects shipped or sat unnoticed,
each invisible to every existing test: the euclid catalogue requested latents under a
retired `latent.` prefix and got silent blanks (pipeline#65); `AggregateCSV` wrote the
1-sigma values into every latent 3-sigma column and seeded max-likelihood from the
median (PyAutoFit#1598); the JAX `vis_lp` stage wrote no latent block because a model
assertion could not be traced inside the latent engine's per-sample `jax.jit`
(PyAutoLens#734, PyAutoFit#1600); and `magnification` was `inf`/`0.0` for every
pixelized source (PyAutoLens#727/#728). The human's ask: "it seems common for these to
break so we need this and make it a first class smoke test".

The existing `scripts/misc/latent/latent_variables_smoke.py` cannot catch any of them.
It runs under the smoke profile's `PYAUTO_TEST_MODE=2`, where
`autonerves.test_mode.skip_latents()` suppresses all latent *writing*
(`PyAutoFit/autofit/non_linear/search/updater.py:249`), so it hand-calls
`analysis.compute_latent_samples`, never touches `files/latent/latent_summary.json`, the
aggregator or `af.AggregateCSV`, and accepts `effective_einstein_radius == 0`.

## What

Two new scripts under `scripts/misc/latent/`, both declaring an `__Env__` docstring
section (form: `scripts/point_source/visualization/modeling_visualization_jit.py:45`)
so the smoke runner unsets the profile vars, and both asserting up front that
`not skip_latents()` and `PYAUTO_SMALL_DATASETS != "1"` so a misconfigured profile
cannot pass vacuously.

`latent_integration_smoke.py` — `ENV: real_search full_datasets`. Pushes a config
overlay (copy of `config/` with `output.latent_draw_via_pdf_size: 8`,
`output.latent_csv: true`, `output.remove_files: true`) via `conf.instance.push`,
wipes `output/latent_integration_smoke/`, simulates in-script a ~40x40 0.1"/pixel
image of an SIE (theta_E ~1.0") + shear lens and a Sersic source with a ~1.6" mask,
and truth-anchored Gaussian priors. Stage 1: `af.Nautilus(n_live=25, n_batch=25,
n_like_max=150, iterations_per_quick_update=1e9)` on `al.AnalysisImaging(use_jax=False,
magzero=25.0)` — a real search, a `SamplesPDF`, a real latent block on disk. Stage 2:
mass fixed from stage 1, `al.mesh.RectangularUniform(shape=(10, 10))` + `al.reg.Constant`
source, `af.Drawer(total_draws=6)` — the cheapest real search — to exercise
`_pixelized_source_flux`. Assertions on disk: each stage's `latent_summary.json` holds
exactly the enabled key set from `config/latent.yaml` (a NaN latent is a missing key,
not a null), every value finite and non-zero; stage 1 `values_at_sigma_3` strictly
brackets `values_at_sigma_1`; stage 2 `magnification` finite and positive,
`total_source_flux` positive. Assertions through the catalogue path:
`Aggregator.from_directory(root, completed_only=True, unzip_temporary=True)` returns 2;
`af.AggregateCSV(agg, strict=True)` with `effective_einstein_radius`, `magnification`,
`total_lens_flux`, `total_source_flux` at (Median, MaxLogLikelihood, ValuesAt1Sigma,
ValuesAt3Sigma) plus one model path, saved and reloaded: no blank cell on the stage-1
row, the stage-2 row's MaxLogLikelihood cells populated (Drawer has no PDF, asserted
explicitly), `*_lower_3_sigma < *_lower_1_sigma` and `*_upper_3_sigma > *_upper_1_sigma`,
MaxLogLikelihood equals the `max_log_likelihood_sample` value in `latent_summary.json`
and differs from the Median; `add_variable("latent.effective_einstein_radius")` raises
`KeyError` under `strict=True` and only warns otherwise. Sibling-dir regression: create
`<hash>/files/dummy.json` beside the stage-1 zip and assert the aggregator still returns
2 (PyAutoFit aggregator fix of 2026-09-10, `aggregator_sibling_dir_shadows_completed_zip`).

`latent_integration_smoke_jax.py` — `ENV: real_search full_datasets jax`. Same
simulated dataset; the model carries a real `model.add_assertion(...)` (two Gaussian
sigmas ordered, mirroring `order_bases`); `al.AnalysisImaging(use_jax=True)`;
`af.Nautilus` as above with `n_like_max=100`; overlay `latent_draw_via_pdf_size: 6`.
Asserts `files/latent/latent_summary.json` exists with the full enabled key set and
finite values, and `search.log` carries no "raised on N of M samples" warning.

Housekeeping in the same PR: two `smoke_tests.txt` entries (paths relative to
`scripts/`), fix the stale `scripts/latent/…` pointer in `config/latent.yaml`'s header
comment, keep the old bypass-mode `latent_variables_smoke.py`.

## Traps

- Any `PYAUTO_TEST_MODE` level skips latent writes; only the `real_search` token
  (which unsets it) produces a latent block. `PYAUTO_TEST_MODE=1` is useless here.
- `af.Drawer` returns plain `Samples`: no median, no sigma bounds. Only the
  MaxLogLikelihood columns can be asserted non-blank on its row.
- Verify the new `smoke_tests.txt` entries by the summary COUNT rising, not by green.
- Under `remove_files: true` the aggregator must be run with `unzip_temporary=True` or
  the in-place extraction litters the output tree for the next run.

<!-- formalised by the Fable architect session 2026-09-10 from the approved plan -->

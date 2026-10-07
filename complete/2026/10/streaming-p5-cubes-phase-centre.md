## streaming-p5-cubes-phase-centre
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/600
- completed: 2026-10-01
- epic: streaming-visibilities (phase 5 of 5 — last development phase; the Discussion #13 follow-up post closes the epic)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/601
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/643
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/582

### What shipped
- **PyAutoArray#601** (merge ffd13ba6; commits d3069dbd + review fix 8a2332f7) — `SparseTerms.phase_centre` provenance (arcsec, `(y, x)`; unshifted accumulations record `(0.0, 0.0)`, `None` = unrecorded) checked in `__add__` alongside `transformer_class_name`; `SparseTerms.__radd__` so `sum(list_of_terms)` works; `sparse_terms_from_chunks(..., phase_centre=)` multiplies each chunk's visibilities by `exp(+2πi(u l0 + v m0))` (l0 = x0, m0 = y0 in radians) before the dirty image AND the data term; `Interferometer.from_stream(phase_centre=)`; `apply_sparse_operator_from_chunks(phase_centre=)` raises (it would shift the operator but not the retained data). Sum of per-channel terms == one-shot accumulation == in-memory MFS `apply_sparse_operator` at rel 1e-12 (numpy and the JAX brute-force kernel path, spy-asserted); array-free dataset from summed terms matches the in-memory MFS inversion / `log_evidence` at 1e-10. `test_autoarray` 1917.
- **PyAutoGalaxy#643** (merge f15570b0; 6c6c8755) — `phase_centre` persisted through `dataset.fits`: `SPARSE_TERMS_SCALARS` HDU gains `phase_centre_y` / `phase_centre_x` (NaN = unrecorded) + `PHCENTY` / `PHCENTX` cards; aggregator loader rebuilds it; pre-change files load with `None`. PyAutoLens reuses this writer/loader. `test_autogalaxy` 1307.
- **autolens_workspace#582** (af91121d + ecc5f2e6) — `scripts/interferometer/features/datacube/modeling_array_free.py` (+ notebook, README row, `smoke_tests.txt`, navigator catalogue): each channel streamed through `from_stream` (memory-mapped FITS generator, 2 chunks/channel) into the existing FactorGraph fit; MFS section via `sum()` of per-channel `SparseTerms` → `from_sparse_terms` (`n_vis` 760 = 4 × 190 asserted; channel-0 `log_evidence` at the true model identical on array-free and in-memory datasets, −3163.931147738987); `phase_centre` demo moves the natural dirty-image peak from (1.85, 0.35) to (0.05, 0.05) with its value 205.300135 preserved; shifted + unshifted sum raises. Full profile ≈ 13 min (`n_live=50`), smoke 6 s; `pyauto-heart smoke autolens` 42/42 scripts + 2/2 notebooks PASS.
- Witness (prompt header): per-channel sum == MFS at 1e-12 (numpy, jax); `phase_centre` accumulation == in-memory on data shifted by `exp(2πi(u l0 + v m0))` at 1e-12; datacube example gains an array-free variant under the smoke profile.
- **Sign pin:** DFT point source at (y, x) = (1.0, −1.5) = native (3, 2) on an 11×11 / 0.5" mask peaks at the mask centre (5, 5) after `phase_centre=(1.0, −1.5)`; the opposite sign puts it at (8, 0); swapped (x, y) order misses the centre.

### Review and override
- Codex gpt-6-astra review (PyAutoArray branch), all reproduced before editing: **F1** (high, introduced) FITS round trip dropped `phase_centre` — reloaded `None` summed with anything → persisted (PyAutoGalaxy#643); **F2** (high, introduced) `apply_sparse_operator_from_chunks(phase_centre=)` shifted the operator but not retained data (sparse χ² 0 vs residual χ² 2 on a one-visibility case) → typed raise; **F4** (medium) `data_term` from unshifted data while the dirty image used shifted data (1e8 vs 99998200.02, Δχ² 1800 with σr≈σi inside the 1e-5 guard) → shift before every data-dependent term; the MFS jax test leg was a no-op under `method="nufft"` → parametrised on `(numpy, use_jax=True)` with a spy; `__add__` now checks `transformer_class_name`. **F3/F5** pre-existing → `draft/bug/autoarray/sparse_terms_nufft_origin_and_mask_compatibility.md` (NUFFT `_shift` ignores `real_space_mask.origin`; provenance cannot see masks with equal geometry but different masked pixels).
- Fifth human-authorized Heart RED development override of the epic ("Yes: library now, workspace when its run passes"; RED: integrate failure, `rectangular.py` timeout, front-door manifest drift — none related). Recorded on issue #600, PR bodies, `active.md`, `autonomy_log.md`. Merged Array → Galaxy → workspace on a separate human `/prm`, every CI leg green (unittest 3.12 / 3.13 / nojax, Docs; workspace Smoke 3.12 / 3.13, Script Size Guard, Navigator Check).

### Deferred / follow-ups
- `draft/bug/autoarray/interferometer_log_evidence_large_regularization_coefficient_cholesky.md` — the search's max-likelihood point on the low-S/N cube (regularization coefficient ≈ 9.7e5) makes eager `FitInterferometer.log_evidence` raise `LinAlgError` / NaN on both dataset types while the jit/vmap search path accepted it; the example evaluates the MFS fit at the true model.
- `scripts/multi_dataset/plot.py:212` writes an untracked `dataset.fits` into the workspace root on every smoke run (not this branch).
- FactorGraph `visualize_before_fit` warm-up logs a non-fatal "no fit_from" warning (in-memory too).
- PyAutoLens has no test asserting `phase_centre` after the aggregator round trip (works via the shared ag loader).
- Phase-centre demo target is the dirty-image arc peak minus half a pixel (even-sized masks put the origin on a pixel corner), not the source-plane centre.
- Epic close: post the Discussion #13 follow-up (draft `reply_discussion13_followup.md`; rewrite its "Not yet" paragraph — P4 ordinary light, P5 cubes + phase centre are in; mention `pending release`); then the profiling campaign `draft/research/autolens_profiling/interferometer_streaming_scaling.md`.

## Original prompt

# Streaming phase 5: per-channel cubes and phase-centre shifts in sparse_terms_from_chunks

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- autolens_workspace
Themes:
- interferometer
- sparse-operator
- memory
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/600
Epic: streaming-visibilities
Phase: 5
Difficulty: small
Consequence: glance
Witness: summing per-channel `SparseTerms` equals the MFS terms accumulated over all channels at rel 1e-12 (numpy and jax); `sparse_terms_from_chunks(..., phase_centre=(l0, m0))` applied per chunk equals the in-memory result on data shifted by `exp(2πi(u l0 + v m0))` at 1e-12; the `autolens_workspace` datacube example gains an array-free variant that runs under the smoke profile.
Review-minutes: 4
Unattended: ready
Parent: draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md
Blocked-by: none

Source: https://github.com/orgs/PyAutoLabs/discussions/13 phase 2, sliced 2026-09-30. No phase-centre code exists today; `SparseTerms.__add__` exists and is tested; datacube examples live in `autolens_workspace/scripts/interferometer/features/datacube/`.

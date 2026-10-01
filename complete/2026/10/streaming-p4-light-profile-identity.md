## streaming-p4-light-profile-identity
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/598
- completed: 2026-10-01
- epic: streaming-visibilities (phase 4 of 5)
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/599
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/642
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/762
- pending-release: PyAutoArray@https://github.com/PyAutoLabs/PyAutoArray/pull/599
- pending-release: PyAutoGalaxy@https://github.com/PyAutoLabs/PyAutoGalaxy/pull/642
- pending-release: PyAutoLens@https://github.com/PyAutoLabs/PyAutoLens/pull/762

### What shipped
- **PyAutoArray#599** (merge 176f61e7) — `aa.DatasetInterface(data_term=)`: per-interface χ² data term that `AbstractInversionInterferometer.fast_chi_squared` reads in preference to `sparse_operator.data_term` when `data is None`; `aa.util.inversion_interferometer.sparse_profile_terms_from(sparse_operator, image, extent_index, xp)` → `(W̃i, d̃−W̃i, data_term−2iᵀd̃+iᵀW̃i)` from one `operated_matrix_slim_from` product; `aa.FitInterferometer.sparse_chi_squared` hook (`None` by default) consulted by `chi_squared` on an array-free dataset before the `DatasetException`; maps still raise. `test_autoarray` 1903.
- **PyAutoGalaxy#642** (merge 574743ab) — `ag.FitInterferometer` with ordinary (non-linear) light profiles runs on an array-free (`from_stream` / `from_sparse_terms`) dataset, with or without an inversion, numpy and `jax.jit`, matching the in-memory dense fit at rel 1e-15: `sparse_profile_terms_from(dataset, galaxies, image, xp)`, `sparse_chi_squared_from(fit, galaxies)` (identity on the TOTAL model image `profile_image + inversion.mapped_reconstructed_data`), `uses_precomputed_data_term_from` array-free rule, `galaxies_to_inversion` passes `data=None` + subtracted dirty image + `data_term`; `profile_visibilities` returns `None` array-free (no raise); `_require_transformer` (typed raise on `model_data`, `galaxy_model_visibilities_dict`), `_require_no_array_free_overrides` (typed raise when a fit overrides `data`/`noise_map` on an array-free dataset). In-memory sparse + ordinary light keeps the subtracted-visibilities path, bit-for-bit unchanged. `test_autogalaxy` 1305.
- **PyAutoLens#762** (merge bcf2ab6f) — mirror for lens light anywhere in the tracer (source none / Sérsic / pixelization / MGE); `tracer_to_inversion`, `sparse_chi_squared`, typed raises on `model_data`, `galaxy_model_visibilities_dict`, `model_visibilities_of_planes_list`. `test_autolens` 793 + 1 xfailed.
- Witness: LP-only and LP+pixelization fits on a streamed dataset match the in-memory fit at ≤ 1e-8 (measured 1e-15) in numpy and under `jax.jit`; a `TransformerNUFFT`/`TransformerDFT.visibilities_from` spy is never called; aggregator round-trip and visualizer pass with an ordinary light profile in the model.

### The trap (red-checked)
`fast_chi_squared` takes term 3 from `sparse_operator.data_term` whenever `dataset.data is None`. Removing the array-free raise without the per-interface override made the inversion pair the profile-subtracted dirty image with the UNSUBTRACTED data term: LP+pixelization log_evidence −37.0125 vs dense −37.9117 (−2.4 %), LP+linear −24.3192 vs −25.2183 (−3.6 %), lens-light+pixelization −37.1294 vs −38.0285 — silently. Any future path that passes `data=None` after subtracting something must supply `data_term`.

### Review and override
- Codex gpt-6-astra review, 3 independent runs (one per repo), identical findings, all reproduced before editing: F1/F2 (high, introduced) — a fit subclass overriding `noise_map`/`data` on an array-free dataset silently mixed the subtracted dirty image with the raw scalar (fom −37.0125 vs −37.9117), or without an inversion ignored a doubled noise map while `noise_normalization` switched (χ² 5.2983 vs 1.3246) → typed guard; F3 (medium) — array-free `log_likelihood` with an inversion carried `eps·Σs²` from `no_regularization_add_to_curvature_diag_value` (packaged 1e-3, test config 1e-8; −0.25 nats at ×100 data) → identity on the total model image, rel 1e-15 vs dense `log_likelihood`, `fast_chi_squared`/`log_evidence` untouched; F4 (medium, pre-existing on main, also `fit_imaging.py` and `galaxy_model_visibilities_dict`) — `{**galaxy_image_dict, **galaxy_linear_obj_image_dict}` overwrites a mixed ordinary+linear galaxy's ordinary image, feeding `adapt_images_from` → filed `draft/bug/autogalaxy/galaxy_image_dict_mixed_galaxy_overwrites_ordinary_light.md`, not fixed.
- Fourth human-authorized Heart RED development override of the epic ("Yes, ship (push + PR-open)"; RED: `release validation FAILED (stage integrate)`, workspace timeout `autolens_test scripts/multi_dataset/rectangular.py`, front-door manifest drift — none related). Recorded on the issue, PR bodies, `active.md`, `autonomy_log.md`. Merged Array → Galaxy → Lens on a separate human `/prm`, every CI leg green (unittest 3.12 / 3.13 / nojax, Docs), mergeability CLEAN.

### Deferred / follow-ups
- F4 above (Mind draft filed).
- In-memory sparse fits with ordinary light could also take the identity and skip the N_vis NUFFT (would relax the exact-equality tests `..._light_profile__unchanged_vs_data_passed`).
- Dense map-based `chi_squared` and `fast_chi_squared` still differ by `sᵀ(εI)s` for unregularised linear objects on the in-memory path (pre-existing convention; one consistent convention would be cleaner).
- Root `activate.sh` was rewritten by a parallel session mid-implementation (known trap); the subagent switched to a private env copy — give subagents one up front.
- Epic next: Discussion #13 follow-up post (draft needs its "Not yet: ordinary light profiles" paragraph rewritten, then human text approval); phase 5 `draft/feature/autoarray/streaming_p5_cubes_phase_centre.md`; profiling campaign `draft/research/autolens_profiling/interferometer_streaming_scaling.md`.

## Original prompt

# Streaming phase 4: non-linear light profiles array-free via the data-term identity

Type: feature
Target: PyAutoArray
Repos:
- PyAutoArray
- PyAutoGalaxy
- PyAutoLens
Themes:
- interferometer
- sparse-operator
- memory
Autonomy: supervised
Priority: medium
Status: active
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoArray/issues/598
Epic: streaming-visibilities
Phase: 4
Difficulty: medium
Consequence: judge
Witness: fits with a non-linear light profile plus a pixelization, and with non-linear light profiles only, run on an array-free dataset with chi-squared computed as `data_term − 2 i_pᵀd̃ + i_pᵀW̃i_p` (one `operated_matrix_slim_from` product shared with `sparse_dirty_image_from`), matching the in-memory fit at rel 1e-8 in numpy and under `jax.jit`; `profile_visibilities` is never formed.
Review-minutes: 8
Unattended: ready
Parent: draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md
Blocked-by: none

Source: https://github.com/orgs/PyAutoLabs/discussions/13 phase 2, sliced 2026-09-30.

## What
1. `aa.DatasetInterface` gains an optional precomputed data term (e.g. `sparse_data_term`) that `fast_chi_squared` term 3 reads when set
   (`abstract.py` ~L218-225), replacing the `profile_subtracted_visibilities` reduction.
2. autogalaxy computes it next to `sparse_dirty_image_from` (`fit_interferometer.py` ~L58-111) from `profile_image`; extend
   `uses_precomputed_data_term_from` so non-linear light profiles also pass `data=None`; autolens mirror.
3. No-inversion fits: override `chi_squared` in ag/al `FitInterferometer` on the same identity (`figure_of_merit` → `log_likelihood`).
4. Tests mirror the phase-1 sparse-vs-dense set for LP+pix and LP-only, numpy + jit; `profile_visibilities` spy stays empty.

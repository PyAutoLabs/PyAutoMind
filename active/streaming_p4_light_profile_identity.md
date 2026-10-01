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

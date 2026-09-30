# Sparse data=None path: guard data_subtracted_dict, harden noise check and data-term dtype (Discussion #13 review fixes)

Type: bug
Target: PyAutoArray
Repos:
- PyAutoArray
- autogalaxy_workspace
- autolens_workspace
Themes:
- interferometer
- sparse-operator
- visualization
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-09-30
Consequence: glance
Witness: on a sparse-operator dataset with the precomputed-data-term gate on (`fit.inversion.dataset.data is None`), `fit.inversion.data_subtracted_dict` raises `InversionException` naming `inversion_with_data` (no TypeError, no `{mapper: None}`), and `InversionPlotter.subplot_of_mapper` / `subplot_mappings` on that inversion skip cleanly instead of raising; `check_noise_map_real_imag_equal` rejects sigma 1e-9 vs 2e-9; `apply_sparse_operator` on complex64 data gives `data_term` equal to the complex128 value and to `sparse_terms_from_chunks`; the two workspace `interferometer/features/pixelization/fit.py` scripts run under the smoke profile using `fit.inversion_with_data`.
Review-minutes: 5
Unattended: ready
Parent: complete/2026/09/interferometer-streaming-visibilities.md

Source: Codex gpt-6-astra review of PyAutoArray#589 / PyAutoGalaxy#637 / PyAutoLens#757
(record: https://github.com/PyAutoLabs/PyAutoLens/pull/757#issuecomment-5907806825), all four
claims reproduced 2026-09-30.

## Why

Phase 1 of https://github.com/orgs/PyAutoLabs/discussions/13 builds the sparse inversion with
`data=None` when no galaxy has a non-linear light profile. Three review findings follow from
the merged code:

- **B (introduced, user-facing).** `AbstractInversion.data_subtracted_dict`
  (`autoarray/inversion/inversion/abstract.py` ~L868-885) does `copy.copy(self.data)` then
  `-=`; with `data=None` a multi-object inversion raises
  `TypeError: unsupported operand type(s) for -: 'NoneType' and 'complex'` and a single-mapper
  inversion yields `{mapper: None}`, which makes `subplot_of_mapper` fail with a `ValueError`
  in `plot/array.py`. The handlers in `autoarray/plot/.../inversion_plots.py` (~L87, ~L397)
  catch only `(AttributeError, KeyError)`. The library visualizers already pass
  `fit.inversion_with_data`, but `autogalaxy_workspace/scripts/interferometer/features/pixelization/fit.py`
  (~L321) passes `fit.inversion` and now fails on PyAutoGalaxy main; the autolens_workspace copy
  (~L293) fails once PyAutoLens#757 lands.
- **D (pre-existing, hardening).** `check_noise_map_real_imag_equal`
  (`inversion_interferometer_util.py` ~L58, L61) uses `np.allclose`/`np.isclose` at default
  `atol=1e-8`, so sigma 1e-9 vs 2e-9 passes and the sparse curvature is 1.5x wrong. Unreachable
  with Jy-unit data but a scale-dependent check is wrong on principle.
- **A (edge, pre-existing path).** `Interferometer.apply_sparse_operator`
  (`autoarray/dataset/interferometer/dataset.py` ~L391-394) squares `data.real`/`data.imag` in
  the data's own dtype; complex64 data + complex128 noise gives `data_term` 700140000.0 vs exact
  700140007.0 (log_evidence +3.5), and disagrees with `sparse_terms_from_chunks`, which promotes
  to complex128. Loaders always yield complex128, so only hand-built complex64 arrays hit it.

Finding C (noise map mutated after `apply_sparse_operator` stales the operator) predates phase 1
and is out of scope; document only if convenient.

## What

1. `AbstractInversion.data_subtracted_dict`: when `self.data is None`, raise
   `exc.InversionException` with a message pointing at `fit.inversion_with_data` (and `fit.data`).
2. `inversion_plots.py` handlers around `data_subtracted_dict` reads: also catch
   `exc.InversionException` (and `TypeError`), so the mapper subplots skip that panel cleanly.
3. `check_noise_map_real_imag_equal`: `atol=0.0` on both calls (keep the default rtol).
4. `apply_sparse_operator`: cast data (and noise) to float64 components before squaring so
   one-shot == chunked for any input dtype.
5. Tests in `test_autoarray`: (1) raises with the named message; (2) plotter skips; (3) the
   1e-9/2e-9 rejection; (4) complex64 data_term == complex128 == chunked.
6. Workspace: both `interferometer/features/pixelization/fit.py` scripts → `fit.inversion_with_data`
   in the inversion plotter call, with a one-line prose note on why; regenerate notebooks per
   each workspace's convention. Library first (`/ship_library`), workspace follows
   (`/ship_workspace`).

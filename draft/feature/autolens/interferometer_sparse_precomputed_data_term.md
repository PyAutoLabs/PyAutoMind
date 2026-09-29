# PyAutoLens parity: precomputed data term on the sparse interferometer path (streaming phase 1)

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
Themes:
- interferometer
- sparse-operator
- memory
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Consequence: glance
Witness: `al.FitInterferometer` on a sparse-operator dataset with a pixelization-only source (no non-linear light profiles) builds its inversion with `data=None`, never evaluates `profile_visibilities` / `profile_subtracted_visibilities` during `figure_of_merit` (spy on `aa.Visibilities.zeros` and `transformer.visibilities_from`), log_evidence is bit-equal to the data-passed path, and `test_autolens/interferometer` is green.
Review-minutes: 3
Unattended: ready
Parent: active/interferometer_streaming_visibilities.md

Source: GitHub Discussion https://github.com/orgs/PyAutoLabs/discussions/13 (HRSAstro,
"Streaming visibilities for memory efficiency"); phase 1 = PyAutoArray#588 (PRs on
PyAutoArray + PyAutoGalaxy, branch `feature/interferometer-streaming-visibilities`).

## Why

Phase 1 made the pixelization-only sparse path skip the two N_vis allocations per
likelihood call in PyAutoGalaxy: `fast_chi_squared` / `noise_normalization` read the
scalars carried by `InterferometerSparseOperator`, and
`autogalaxy/interferometer/fit_interferometer.py` passes `data=None` into
`DatasetInterface` when `uses_precomputed_data_term_from(dataset, galaxies, data,
noise_map)` holds. PyAutoLens has its own `FitInterferometer`, whose
`tracer_to_inversion` (`autolens/interferometer/fit_interferometer.py` ~L155) still passes
`data=self.profile_subtracted_visibilities` unconditionally — so lens fits, the main
consumer, still allocate `Visibilities.zeros` + `data - profile_visibilities` over N_vis
on every call.

## What

- In `autolens/interferometer/fit_interferometer.py` `tracer_to_inversion`, reuse
  `ag.interferometer.fit_interferometer.uses_precomputed_data_term_from(self.dataset,
  self.tracer.galaxies, self.data, self.noise_map)` (verify the import path on the
  shipped autogalaxy) and pass `data=None` when it holds; keep `sparse_dirty_image`
  as is.
- Add `inversion_with_data` mirroring autogalaxy's (an inversion rebuilt with the real
  `profile_subtracted_visibilities`, for consumers that need `inversion.data`).
- Switch `autolens/interferometer/model/visualizer.py` (~L139-160) to
  `fit.inversion_with_data` where it plots inversion quantities that read data.
- Tests in `test_autolens/interferometer/test_fit_interferometer.py` mirroring
  autogalaxy's phase-1 additions: the `data=None` gate, the spy, bit-equal log_evidence,
  and the light-profile case still passing data.
- Check `autolens/aggregator/` and `autolens/plot/` (and `al.agg` fit reconstruction) for
  `inversion.data` / `inversion.data_vector` reads that would break on `data=None`.

Blocked on the phase-1 PyAutoArray + PyAutoGalaxy PRs merging (library-first).

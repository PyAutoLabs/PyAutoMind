## interferometer-sparse-precomputed-data-term
- issue: https://github.com/PyAutoLabs/PyAutoLens/issues/756
- completed: 2026-09-30
- source: https://github.com/orgs/PyAutoLabs/discussions/13
- parent: complete/2026/09/interferometer-streaming-visibilities.md
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/757

### What shipped
- **PyAutoLens#757** (merge 092897e4) — PyAutoLens parity for Discussion #13 phase 1: `FitInterferometer.tracer_to_inversion` gated on autogalaxy's `uses_precomputed_data_term_from` (sparse operator with `data_term`, dataset's own data/noise map, no non-linear light profile) and passes `data=None`, so sparse pixelization-only lens fits never allocate `profile_visibilities` / `profile_subtracted_visibilities` per likelihood call; `FitInterferometer.inversion_with_data` (shallow copy carrying `fit.data`, shares the reconstruction) for output paths; the interferometer visualizer uses it; `profile_visibilities` / `profile_subtracted_visibilities` are `cached_property`. Tests mirror autogalaxy's phase-1 additions plus a bit-equality control against the gate forced off.
- Witness (1e5-vis NUFFT, 616-pixel mask, Isothermal + 15x15 rectangular source): figure_of_merit gated vs ungated differs by exactly 0.0; tracemalloc peak per evaluation 3.20 MB at 1e5 and 4e5 (flat) vs 7.59 / 21.99 MB ungated; 16.2 ms vs 18.0 / 26.6 ms.

### Review
- Independent Codex gpt-6-astra review of this PR + phase 1 (record: https://github.com/PyAutoLabs/PyAutoLens/pull/757#issuecomment-5907806825): 4 reproduced findings; the one with real exposure (`data_subtracted_dict` on `data=None` breaking `subplot_of_mapper` in two workspace scripts) plus two hardenings shipped as `sparse-data-none-guard` (PyAutoArray#591, autogalaxy_workspace#253, autolens_workspace#581). Finding C (noise map mutated after `apply_sparse_operator`) is pre-existing and documented only.

### Notes
- Heart YELLOW acknowledged at ship (workspace validation 1 timeout on autolens_test multi_dataset/rectangular.py; manifest drift 1; HowToGalaxy/HowToLens PR age; no rehearsal). Freeze expired at merge.
- Parallel claim on PyAutoLens with workspace-config-cleanup (#441, PR #751 merged, test files only) approved with the plan.
- The bundle `activate.sh` is a symlink to the root file, which a parallel session rewrote during this task; later phases used a private env file. CI green is the independent evidence.

## Original prompt

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
Status: active
Issued: 2026-09-30
Consequence: glance
Witness: `al.FitInterferometer` on a sparse-operator dataset with a pixelization-only source (no non-linear light profiles) builds its inversion with `data=None`, never evaluates `profile_visibilities` / `profile_subtracted_visibilities` during `figure_of_merit` (spy on `aa.Visibilities.zeros` and `transformer.visibilities_from`), log_evidence is bit-equal to the data-passed path, and `test_autolens/interferometer` is green.
Review-minutes: 3
Unattended: ready
Parent: complete/2026/09/interferometer-streaming-visibilities.md

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

Blocked on the phase-1 PyAutoArray + PyAutoGalaxy PRs merging (library-first). (merged 2026-09-30)

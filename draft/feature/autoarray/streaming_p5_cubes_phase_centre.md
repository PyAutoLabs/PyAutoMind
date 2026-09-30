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
Status: draft
Epic: streaming-visibilities
Phase: 5
Difficulty: small
Consequence: glance
Witness: summing per-channel `SparseTerms` equals the MFS terms accumulated over all channels at rel 1e-12 (numpy and jax); `sparse_terms_from_chunks(..., phase_centre=(l0, m0))` applied per chunk equals the in-memory result on data shifted by `exp(2πi(u l0 + v m0))` at 1e-12; the `autolens_workspace` datacube example gains an array-free variant that runs under the smoke profile.
Review-minutes: 4
Unattended: ready
Parent: draft/feature/autoarray/interferometer_from_stream_array_free_dataset.md
Blocked-by: draft/feature/autoarray/streaming_p3_visualizer.md

Source: https://github.com/orgs/PyAutoLabs/discussions/13 phase 2, sliced 2026-09-30. No phase-centre code exists today; `SparseTerms.__add__` exists and is tested; datacube examples live in `autolens_workspace/scripts/interferometer/features/datacube/`.

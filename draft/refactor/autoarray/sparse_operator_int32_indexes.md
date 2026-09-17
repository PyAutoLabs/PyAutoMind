# Sparse CPU operator: shrink the 172 MB per-dataset payload (int32 indexes, compressible precision operator)

Target: PyAutoArray
Type: refactor
Autonomy: supervised
Consequence: notify
Witness: `indexes` (and every other index array on `SparseLinAlgImagingNumba`) is int32 behind an overflow guard, the payload of `Imaging.apply_sparse_operator_cpu()` at HST/3.5" is measured before and after and recorded in the PR (172 MB before), and the existing sparse-operator tests plus the `cpu_fast_modeling` parity check give bit-identical results.
Review-minutes: 0
Unattended: ready

## Context

`Imaging.apply_sparse_operator_cpu()` attaches a `SparseLinAlgImagingNumba` of ~172 MB at HST/3.5" (measured
2026-08-30, `subhalo_validation/scripts/scratch/memory_growth.py`): `psf_precision_operator_sparse` 84.5 MB and
`indexes` 84.5 MB. `indexes` is almost certainly int64 where int32 suffices (n_pixels ≪ 2^31), halving it;
the precision operator may be compressible too. Beyond the per-process RSS (×8 workers), the size made the
dataset hostile to any path that serialises it (PyAutoFit #1547 pickled it per task; fixed in #1548, but a
lean operator is a defence in depth). Also worth checking why the per-call inversion under the pool cost
1.7 s vs 0.25 s serial in the harness — if that gap survives #1548, profile it.

## Acceptance

- `indexes` (and any other index arrays) stored as int32 with a guard; numba kernels accept the dtype.
- Payload measured before/after (`pickle.dumps` size or `nbytes` sum) and recorded in the PR.
- Existing sparse-operator tests + `cpu_fast_modeling`-style parity check unchanged in results.

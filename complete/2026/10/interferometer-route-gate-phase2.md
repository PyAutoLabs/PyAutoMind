- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/419
- completed: 2026-10-15
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/420 (MERGED 2026-10-15T22:55:26Z, merge `33779e46`, head `32372865`)
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/632 (`17caf228`); also #631 (`0377eeaa`), #630 (`7cc71238`)
- campaign: https://github.com/PyAutoLabs/PyAutoPulse/issues/62 (task `interferometer_large_mask_aris`; Pulse knowledge write-up PR #65 + decision records)

## What shipped

Phase 2 (workspace record) of `interferometer-numba-route-gate`
(`complete/2026/10/interferometer-numba-route-gate.md`). There were no script changes:

- `results/notes/interferometer_route_gate_aris_2026_10.md` (new): the six-cell Aris routing table
  under PyAutoArray#632's default cost model, plus the owed numba-vs-JAX log-det after-measurement
  following PyAutoArray#631.
- `wiki/campaigns/interferometer_likelihood.md`: the verdict line (the fixed gate is superseded by
  the cost model), the ledger and library-PR lines, a new phase row, the gate caveat and a
  2026-10-15 journal entry.

## Six-cell table (default settings, PyAutoArray `17caf228`)

| Mask (extent) | Vertices | nnz/col | Route | Pred. t_fft/t_dc | Measured FFT s/call | Measured `direct_conv` s/call | JAX jit s/call | log-det numba | log-det JAX | Δ |
|---|---|---|---|---|---|---|---|---|---|---|
| 125×125 (83²) | 1,405 | 11.7 | `direct_conv` | 26.4 | not measured | 0.396 | 1.96 | 2468.4463180 | 2468.4463180 | 3.9e-8 |
| 125×125 (83²) | 2,947 | 5.57 | `direct_conv` | 55.5 | not measured | 2.08 | 6.84 | 4350.2973995 | 4350.2973995 | 2.1e-8 |
| 125×125 (83²) | 5,526 | 2.98 | `direct_conv` | 103.7 | not measured | 6.12 | 12.0 | 10157.1564483 | 10157.1564483 | 4.0e-8 |
| 512×512 (341²) | 1,459 | 187.6 | FFT | 0.89 | 28.3 | 38.4 | 18.3 | 2573.1669411 | 2573.1669411 | 4.1e-8 |
| 512×512 (341²) | 2,577 | 106.2 | `direct_conv` | 1.57 | 44.1 | 34.2 | 32.2 | 4610.2972527 | 4610.2972526 | 2.6e-8 |
| 512×512 (341²) | 5,746 | 47.7 | `direct_conv` | 3.49 | 97.3 | 41.2 | not run (~72 extrapolated) | 10625.0105708 | 10625.0105708 | 4.4e-8 |

Measured s/call is a prior laptop measurement (PROGRESS3/PROGRESS4, PyAutoArray `ccddfba6`) and was
not re-timed. The full table, with predicted seconds and inversion classes, is in the note.

## Outcome

- **Routing.** In all six cells the factory now picks the faster measured arm. The old gate of 60
  misrouted the 512 / 2,577 cell to FFT (nnz/col 106), although `direct_conv` measured 1.29×
  faster. The kill-gate question is answered by the cost model's extent-dependent crossover
  (~309 nnz/col at 83², ~166 at 341²), not by retuning the constant.
- **Aris log-det after-measurement.** numba and JAX `log_det_regularization_matrix_term` now agree
  to ≤ 4.4e-8 in every cell. The investigation's original 125 vector moved from 2443.22 (numba)
  vs 2561.98 (JAX) to 2468.4463180 on both.

## Decision taken

The s/call values are carried from the prior laptop measurement, not re-timed. This was the human's
compute decision ("Laptop, routing + log-det only"). The rejected alternative was to re-time on the
loaded laptop (~2.5× documented clock drift). Revert: delete the note and revert the wiki hunk.

## Stated limits

- The three 512 timing pairs are calibration points of the cost model, so agreement there is
  in-sample.
- The 125 FFT arm was never timed in NumPy. The JAX-jit FFT route is used as a proxy.

## Gate

Review CLEAN after F1/F2 were fixed in `3237286`. tests/smoke n/a (markdown-only; lint.yml checks
pass). Heart was RED (`release validation FAILED (stage integrate)`) and a development-only
override was authorized by the live human in session 3e3dea38 ('Yes, override for both
(Recommended)'), covering commit/push/PR-open only. The merge was the human's `/prm`, recorded as
merged-unchanged. Heart remains RED for release purposes.

Scope merged = scope filed.

## Where to pick up

1. Review F3 follow-up: `draft/docs/autolens_profiling/decision_matrix_note_gate_wording.md`.
   `results/notes/interferometer_likelihood_decision_matrix_2026_09.md` may still describe gate 60
   as current. The draft also adds a link from the campaign wiki to the Pulse task's Knowledge
   section and its two decision records.
2. At the next Pulse check-in, copy the six-cell table into
   `PyAutoPulse/tasks/interferometer_large_mask_aris.md`.

## Original prompt

# Interferometer route gate phase 2: re-measure the Aris routing table with the default cost model

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: glance
Status: formalised
Issued: 2026-10-15
Compute: laptop; routing + log-det only; timings not re-measured

- Status: split out of `interferometer-numba-route-gate` at close-out — the library
  phase shipped in `complete/2026/10/interferometer-numba-route-gate.md`
  (https://github.com/PyAutoLabs/PyAutoArray/issues/628,
  https://github.com/PyAutoLabs/PyAutoArray/pull/632); this is the workspace record that remains.

PyAutoArray#632 replaced the fixed `interferometer_numba_nnz_per_source_max: 60` gate with a
two-constant cost model (`t_fft = c_fft·S·pocketfft-work(padded 2ny×2nx)`,
`t_dc = c_dc·nnz·ny·nx`, c_fft 7.62e-10, c_dc 1.77e-09). The packaged default is now `null`
(cost model); a positive value is a hard gate, 0 turns numba off, and a new
`interferometer_route` setting forces a route.

Re-measure both Aris masks' routing table (125x125, extent 83²; 512x512, extent 341²) with the
default cost model at the campaign's vertex counts (125: 1,405 / 2,947 / 5,526; 512: 1,459 /
2,577 / 5,746), recording for each cell the chosen route, both measured timings and the
predicted t_fft / t_dc. Record the table in the campaign results/wiki in the
autolens_profiling#226 bake-off format, and link #628 / #632 and
https://github.com/PyAutoLabs/PyAutoPulse/issues/62 (task `interferometer_large_mask_aris`).
This also supplies the campaign's owed Aris after-measurements.

Note: the three autolens_profiling scripts that set
`interferometer_numba_nnz_per_source_max` explicitly keep hard-gate meaning — leave them
unchanged unless the re-measurement is meant to exercise the default (then drop the explicit
value in the run, not in the committed script).

- The record ALSO carries the campaign's owed Aris log-det after-measurement: for each cell,
  `log_det_regularization_matrix_term` on numba vs JAX at the same parameter vector on
  PyAutoArray main ≥ 17caf228 (post-#631), plus the 125×125 figure at the original vector
  (pre-fix numba 2443.22 vs JAX 2561.98). Timings (s/call) are carried from the prior laptop
  measurement (PROGRESS4 table), not re-timed — the laptop is shared (load 2–14).

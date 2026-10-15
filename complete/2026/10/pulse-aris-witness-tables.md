## Summary

Shipped in PyAutoPulse#64 (merge fc092a9a, 2026-10-15). The three Aris large-mask before/after
witness tables (PyAutoArray #630 sparse data vector, #631 AdaptSplit log-det backend parity,
#632 numba route-gate cost model) landed under `## Results 2026-10-15` in
`tasks/interferometer_large_mask_aris.md`, with the Reviewed line updated. The `campaigns.yaml`
task-row and interferometer campaign-row `next` lines were refreshed, and the board was
re-rendered. Anchor issue PyAutoPulse#62 stays open as the campaign anchor.

## Ship notes

- Heart RED override: granted by the live human in session 3e3dea38 on 2026-10-15 (late),
  "Yes, override for both".
- Consequence: notify, so no shadow row. PyAutoPulse is not in the published set, so there is
  no pending-release.

## Where to pick up

The autolens_profiling phase-2 record (in flight) will add its table to the same task file,
`tasks/interferometer_large_mask_aris.md`, through a later Pulse PR. The Aris log-det
after-measurement is also still in flight.

## Original prompt

# Pulse: record the three Aris large-mask before/after witness tables

Type: docs
Target: PyAutoPulse
Repos:
- PyAutoPulse
Difficulty: small
Autonomy: safe
Consequence: notify
Status: formalised
Issued: 2026-10-15
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/62

All three PyAutoArray members of the PyAutoPulse interferometer campaign task
`interferometer_large_mask_aris` merged on 2026-10-15: #630 (sparse data vector, 7cc71238),
#631 (AdaptSplit log-det backend parity, 0377eeaa) and #632 (numba route-gate cost model,
17caf228). Each PR asked for its before/after witness to be copied into the Pulse task file at
close-out.

Do: append `## Results 2026-10-15` to `tasks/interferometer_large_mask_aris.md` with one
subsection per member (short table + 1-3 lines), sourced from the PR bodies and the Mind
completion records `complete/2026/10/{interferometer-sparse-data-vector,adaptsplit-logdet-backend-parity,interferometer-numba-route-gate}.md`.
Update the file's Reviewed line (2026-10-15; status stays active). In `campaigns.yaml` set the
task row's `updated`/`next` (members merged, pending release; phase-2 autolens_profiling record
and the Aris log-det after-measurement in flight) and refresh the interferometer campaign row's
`next` first sentence. Do not stamp `last_checkin`. Anchor issue #62 stays open; reuse it, open
no new issue.

Witness: `bin/pyauto-pulse check --offline` prints OK and `pytest tests` passes.

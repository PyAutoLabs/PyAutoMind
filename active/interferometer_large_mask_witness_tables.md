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

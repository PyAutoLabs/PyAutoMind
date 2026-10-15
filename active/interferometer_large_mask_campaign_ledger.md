# Pulse ledger: log the Aris interferometer large-mask tasks under the interferometer campaign

Type: docs
Target: PyAutoPulse
Repos:
- PyAutoPulse
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Issued: 2026-10-15
Consequence: notify
Witness: `bin/pyauto-pulse check --offline` OK and `pytest -q tests` green with the new task row rendered on the board
Review-minutes: 1
Unattended: ready
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/62

Human request (2026-10-15): "can we make this part of a PyAutoPulse speed up campaign as in log and monitor it under that organ".

Add task `interferometer_large_mask_aris` (campaign `interferometer`, status active, priority high) to
`campaigns.yaml` with `tasks/interferometer_large_mask_aris.md` holding the campaign intent, the 512×512
baseline table and the check-in log for PyAutoArray#626/#627/#628; refresh the interferometer campaign
row's `updated`/`next`; re-render `dashboard.md`/`dashboard.html` offline. The task file and a ledger
patch script were prepared in session 3e3dea38 (scratchpad `pulse_patch/`, temporary) and dry-run
green (board --offline, check --offline, pytest); the content is also the body of PyAutoPulse#62.

PyAutoPulse is free (the `ral-category-paths` claim was released 2026-10-15); apply on a
`feature/pulse-interferometer-large-mask` branch.

## pulse-interferometer-large-mask
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/62
- completed: 2026-10-15
- library-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/63
- merge: 24749975a794f60d06534e38ff41f1f23ad3755d
- summary: Ledger task `interferometer_large_mask_aris` added to the PyAutoPulse interferometer campaign (linking PyAutoArray#626/#630 and the follow-ups #627/#628) and the Pulse board re-rendered. Ledger/docs only — no producer, pin, qualification or Heart readiness change.
- anchor: PyAutoPulse#62 remains OPEN as the campaign anchor for check-ins (GitHub auto-closed it on merge because the PR body's "Closes #62 is not claimed" sentence matched the closing keyword; reopened at close-out).
- heart: Heart RED under the same live-human development override as the PyAutoArray Aris tasks (session 3e3dea38; reasons on PyAutoArray#626; permitted commit/push/PR-open, merge separate — merged by human /prm 2026-10-15).

## Original prompt

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

# Organ cockpit: PyAutoHands release board emits state.json

Type: feature
Target: PyAutoHands
Repos:
- PyAutoHands
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: notify
Witness: release_board.yml run on main is green including the new validate step logging 'state: ok', and curl https://pyautolabs.github.io/PyAutoHands/state.json passes python board/_state.py from a PyAutoBrain checkout.
Review-minutes: 0
Unattended: ready
Epic: organ-cockpit

Phase 1 (PyAutoBrain#416, shipped 2026-09-26) defined the per-organ state.json v1 cockpit feed (contract board/state_schema.json, validator + CLI board/_state.py in PyAutoBrain) and made the Brain and Heart boards emit it. This prompt makes the Hands release board emit it too, mirroring the Heart pattern exactly.

1. autohands/board.py: a to_state()/render for fmt 'state' and a --state flag beside --badge: status from the badge colour (red/orange/lightgrey/brightgreen -> red/yellow/grey/green, or the board's own verdict if it has one), headline = the badge message, updated = the snapshot timestamp normalised to ISO-8601 Z, pages_url = https://pyautolabs.github.io/PyAutoHands/, items = the actionable rows the board already renders (failed release legs, stale wheels, pending human release decisions) with their GitHub links and any existing copy-for-Claude prompt.
2. .github/workflows/release_board.yml: render --state > _site/state.json in the render step, then a step running python3 PyAutoBrain/board/_state.py _site/state.json (PyAutoBrain is already checked out at ./PyAutoBrain in the job) that fails the job on drift.
3. Tests beside the existing board tests: required keys, status enum, updated ends with Z, items carry url; the no-snapshot path yields grey. Hands tests must not import Brain.

Witness: release_board.yml run on main is green including the new validate step logging 'state: ok', and curl https://pyautolabs.github.io/PyAutoHands/state.json passes python board/_state.py from a PyAutoBrain checkout.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->

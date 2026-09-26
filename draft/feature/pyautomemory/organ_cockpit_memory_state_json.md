# Organ cockpit: PyAutoMemory knowledge board emits state.json

Type: feature
Target: PyAutoMemory
Repos:
- PyAutoMemory
Difficulty: small
Autonomy: safe
Priority: high
Status: formalised
Consequence: notify
Witness: knowledge_board.yml run on main green with the validate step logging 'state: ok'; curl https://pyautolabs.github.io/PyAutoMemory/state.json passes the validator CLI.
Review-minutes: 0
Unattended: ready
Epic: organ-cockpit

Phase 1 (issue 416 in the Brain, shipped 2026-09-26) defined the per-organ state.json v1 cockpit feed (contract board/state_schema.json, validator + CLI board/_state.py in the Brain checkout the board job already has at ./PyAutoBrain). This prompt makes the Memory knowledge board emit it, mirroring the Heart pattern.

1. scripts/board.py in PyAutoMemory: a --state flag beside --badge rendering the v1 feed: status from the badge colour (red/orange/lightgrey/brightgreen -> red/yellow/grey/green), headline = the badge message, updated = the render timestamp as ISO-8601 Z, pages_url = https://pyautolabs.github.io/PyAutoMemory/, items = the actionable rows the board already renders (stale wiki pages, unprovenanced entries, reading-queue waits) with GitHub links.
2. .github/workflows/knowledge_board.yml: python scripts/board.py --state > _site/state.json in the render step, then a validate step python3 PyAutoBrain/board/_state.py _site/state.json that fails the job on drift.
3. Tests beside the existing board tests in PyAutoMemory: required keys, status enum, updated ends with Z; Memory tests must not import the Brain.

Witness: knowledge_board.yml run on main green with the validate step logging 'state: ok'; curl https://pyautolabs.github.io/PyAutoMemory/state.json passes the validator CLI.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->

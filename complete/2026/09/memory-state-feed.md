- issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/104 (closed)
- completed: 2026-09-26
- library-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/105 (MERGED)
- epic: organ-cockpit (bundle organ-cockpit-feeds with hands-state-feed; contract from PyAutoBrain#416)
- heart-red-override: "Heart RED `release validation FAILED (stage integrate)`; live human 'ok io authorize you to continue' 2026-09-26 — development shipping + merge on green checks; recorded on the issue, PR body, active.md, autonomy_log.md"
- witness: knowledge_board.yml run 36240211686 green with `state: ok`; https://pyautolabs.github.io/PyAutoMemory/state.json validates (yellow | arXiv inbox digest stale · 166 pages · 40% cited | 7 items).
- gotchas: Memory has no red condition by design (nothing can break); the live yellow is REAL — arXiv inbox digest stale since 2026-09-23 and interests since 2026-09-16, nightly filing may be broken (not filed yet); `test_theme_finds_grouped_brain_from_outer_workspace` fails whenever activate.sh exports PYAUTO_BRAIN (on main too) — one-line `monkeypatch.delenv` fix, not filed; Memory PR CI has only a `validate` leg, pytest ran locally; `pages_url` falls back to `./` for remote-less checkouts.
- follow-ups (not filed): arXiv nightly filing staleness; the PYAUTO_BRAIN theme-test env leak.
- summary: Memory knowledge board emits the organ-cockpit state.json v1 feed (`to_state`, `--state`) and knowledge_board.yml publishes + validates it against the Brain contract. Memory pytest 219 (9 new).

## Original prompt

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
Issued: 2026-09-26
Issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/104
Epic: organ-cockpit

Phase 1 (issue 416 in the Brain, shipped 2026-09-26) defined the per-organ state.json v1 cockpit feed (contract board/state_schema.json, validator + CLI board/_state.py in the Brain checkout the board job already has at ./PyAutoBrain). This prompt makes the Memory knowledge board emit it, mirroring the Heart pattern.

1. scripts/board.py in PyAutoMemory: a --state flag beside --badge rendering the v1 feed: status from the badge colour (red/orange/lightgrey/brightgreen -> red/yellow/grey/green), headline = the badge message, updated = the render timestamp as ISO-8601 Z, pages_url = https://pyautolabs.github.io/PyAutoMemory/, items = the actionable rows the board already renders (stale wiki pages, unprovenanced entries, reading-queue waits) with GitHub links.
2. .github/workflows/knowledge_board.yml: python scripts/board.py --state > _site/state.json in the render step, then a validate step python3 PyAutoBrain/board/_state.py _site/state.json that fails the job on drift.
3. Tests beside the existing board tests in PyAutoMemory: required keys, status enum, updated ends with Z; Memory tests must not import the Brain.

Witness: knowledge_board.yml run on main green with the validate step logging 'state: ok'; curl https://pyautolabs.github.io/PyAutoMemory/state.json passes the validator CLI.

<!-- formalised by the Intake (Conception) Agent on 2026-09-26 from user-intake -->

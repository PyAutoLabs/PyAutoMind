# Trim the start_dev and /prm mandatory reads

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: `scripts/token_load.py report` shows start_dev and prm line totals under their CI budgets (400 / 450) and as close to the 350 / 300 targets as possible with no gate, refusal or rule removed; the Brain suite passes.
Review-minutes: 10
Parent: draft/maintenance/organs/reduce_session_token_load.md
Filed: 2026-11-06 (slice of the parent: levers 5-6; human "Do 2", 2026-11-06)

Shorten what a session must read to run `/start_dev` and `/prm` (entry +
body + CONTEXT.md + WORKFLOW.md). Move conditional material verbatim into the
reference files the skills already point at; tighten shared prose in place,
keeping every test-pinned phrase.

- issue: none (PR is the tracking surface)
- completed: 2026-11-07
- prs: PyAutoBrain#597
- summary: start_dev procedure 499 -> 360 lines, /prm 456 -> 338 (CI budgets 400 / 450 now pass; targets 350 / 300 not met by 10 / 38). WORKFLOW.md and CONTEXT.md compacted; start_dev --auto contract and prm incident history moved verbatim to each skill's reference.md. Re-verified on main with #599/#600: Brain suite 1643 passed, every skill <= 200 lines.
- parent: draft/maintenance/organs/reduce_session_token_load.md (stays draft; remaining: the 350 / 300 procedure targets)
- merged-by: human /prm 2026-11-07 (cloud session)

## Original prompt

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

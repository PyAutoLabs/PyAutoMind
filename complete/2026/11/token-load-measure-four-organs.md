- issue: none (PR is the tracking surface)
- completed: 2026-11-06
- prs: PyAutoMind#544
- summary: scripts/token_load.py now reports the four organs' AGENTS.md total (Brain/Mind/Cortex/Memory) and the newest month's completion-record median, report-only unless --organ-agents-budget / --record-median-budget is passed. Measured at merge: four-organ total ~8,690 tokens (~5,460 excluding the shared generated blocks, which the human ruled stay); 2026/11 median 55 lines (target <= 60, met).
- parent: draft/maintenance/organs/reduce_session_token_load.md (stays draft; remaining scope: procedure-line budgets, levers 5-6)
- merged-by: human /prm 2026-11-06 (cloud session)

## Original prompt

# token_load.py measures the prompt's three targets

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: `token_load.py report` prints the four-organ total and the record median in a cloud (flat) root; tests pin both totals, the budgets and the absent-organ case; the Mind suite passes.
Review-minutes: 5
Parent: draft/maintenance/organs/reduce_session_token_load.md
Filed: 2026-11-06 (slice of the parent, split in the 2026-11-06 cloud queue session)

Lever 0 (measure first): the parent prompt's numbers were only partly measured — the script counted Brain + Mind + the laptop-only workspace AGENTS.md, so a cloud session printed `AGENTS total: unknown` and Cortex/Memory were never counted.

`scripts/token_load.py` reports the four organs' AGENTS.md total (Brain, Mind, Cortex, Memory) and the newest month's median completion-record length beside the existing procedure lines; both are report-only unless `--organ-agents-budget` / `--record-median-budget` is passed, so Mind-only CI still passes `check`.

Grouped by the human's request "find 4 grouped tasks and do them" (2026-11-06)
with `token_load_measure_four_organs`, `organism_map_compact`,
`cortex_agents_slim` and `mind_agents_trim` — one cloud session, one branch per
repo (`ccr-c113837c-0ulthv`).

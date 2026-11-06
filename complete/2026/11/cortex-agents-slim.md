- issue: none (PR is the tracking surface)
- completed: 2026-11-06
- prs: PyAutoCortex#87
- summary: Cortex AGENTS.md 21.5 kB -> 10.9 kB with no rule removed: verb listing, conductor and workflow tables and the verbatim out-of-scope quote replaced by pointers to REFERENCE.md, pyauto-brain help cortex and the shelved prompt. Merged without CI on human say-so: cortex_check.yml does not trigger on AGENTS.md; local cortex.py check OK and suite 104 passed.
- parent: draft/maintenance/organs/reduce_session_token_load.md (stays draft; remaining scope: procedure-line budgets, levers 5-6)
- merged-by: human /prm 2026-11-06 (cloud session)

## Original prompt

# Cortex AGENTS.md points to REFERENCE.md instead of restating it

Type: maintenance
Target: PyAutoCortex
Repos:
- PyAutoCortex
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: Cortex AGENTS.md falls from 21.5 kB to ~10.9 kB with no rule removed; `cortex.py check` OK and the Cortex suite passes.
Review-minutes: 5
Parent: draft/maintenance/organs/reduce_session_token_load.md
Filed: 2026-11-06 (slice of the parent, split in the 2026-11-06 cloud queue session)

Lever 3 of the parent prompt.

The verb-by-verb `cortex.py` listing, the conductor verb table, the workflow table and the 16-line verbatim out-of-scope quote are replaced by pointers to REFERENCE.md / the shelved prompt; every rule stays (projects.yaml is code except births, no inferred results, nothing submits by itself, CPU arrays on `ral`, workspace-paths exception, the six hard rules).

Grouped by the human's request "find 4 grouped tasks and do them" (2026-11-06)
with `token_load_measure_four_organs`, `organism_map_compact`,
`cortex_agents_slim` and `mind_agents_trim` — one cloud session, one branch per
repo (`ccr-c113837c-0ulthv`).

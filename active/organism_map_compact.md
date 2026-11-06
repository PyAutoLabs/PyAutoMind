# one-clause organism map in every organ AGENTS.md

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
- PyAutoBrain
- PyAutoCortex
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: The map block shrinks from ~4.4 kB to ~2.0 kB; `repos_sync.py --check` reports no map drift on the checked-out organs; a test bounds every organ's `map_role`; Mind + Brain suites pass.
Review-minutes: 5
Parent: draft/maintenance/organs/reduce_session_token_load.md
Filed: 2026-11-06 (slice of the parent, split in the 2026-11-06 cloud queue session)

Lever 2 of the parent prompt.

Organ rows in `repos.yaml` gain `map_role` (one clause, ≤100 chars); `system_map()` renders it (falling back to `role`) with a two-line preamble and a one-paragraph invariant line. Regenerated into Brain and Cortex AGENTS.md; the other six organ copies (Heart, Hands, Nerves, Gut, Eyes, …) regenerate on the next laptop `repos_sync.py --write` after merge (absent from this cloud session).

Grouped by the human's request "find 4 grouped tasks and do them" (2026-11-06)
with `token_load_measure_four_organs`, `organism_map_compact`,
`cortex_agents_slim` and `mind_agents_trim` — one cloud session, one branch per
repo (`ccr-c113837c-0ulthv`).

# Reconcile inference documentation with the current Cortex ledger contract

Type: docs
Target: @autolens_inference
Repos:
- autolens_inference
Difficulty: small
Autonomy: supervised
Priority: normal
Consequence: judge
Filed: 2026-10-01
Status: draft

## Original user direction (verbatim)

Adopt the terminology and reconcile existing documentation (recommended)

## Scope

Follow the discrepancies documented by Brain#441 and
`PyAutoBrain/docs/research/ecosystem_levels.md`. After the existing
`point-source-search-nautilus-leaf` claim is released, inspect current Cortex
AGENTS.md/REFERENCE.md and the project registry row, then update inference
`CORTEX.md` and affected passages of `AGENTS.md` to describe the current
Now / Runs / Log model, science/development boundary and actual ledger locations.
Remove live instructions that route to archived tasks/rulings; preserve legitimate
historical references as historical. Results and lessons remain the human's words.

Do not edit Cortex state, science results, run tooling or historical archives.
Do not move ledgers or infer the live ledger path from a stale instruction.
Validate every changed path against the owning contract. This task complements
`complete/2026/10/ecosystem-role-docs.md` but has its own
repo, issue and PR. Existing claim is a scheduling constraint, not merge authorization.

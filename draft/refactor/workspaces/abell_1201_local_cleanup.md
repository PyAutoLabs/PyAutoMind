# Repo cleanup: retire the Abell 1201 worktree and local raw data

Type: refactor
Target: workspaces
Repos:
- autolens_assistant
Themes:
- hygiene
Difficulty: small
Autonomy: human-required
Priority: low
Status: draft
Consequence: judge
Review-minutes: 5
Unattended: needs-input
Blocked-by: PyAutoMind/active/cosmos_web_ring_greeting.md (autolens_assistant#136)
Filed: 2026-09-26

## Why

The Abell 1201 demonstration was superseded by the COSMOS-Web Ring greeting (#136; task
`abell-1201-point-mass` closed 2026-09-26). Left in place on purpose, for a human decision:

- `/home/jammy/Code/PyAutoLabs/.worktrees/abell-1201-point-mass/` — retained worktree on
  `feature/abell-1201-point-mass` (merged as PR #134) with ~4.2 MB of ignored plots/reports
  under `scripts/scratch/abell_1201`.
- canonical `lens/autolens_assistant/dataset/abell_1201/` — 29 MB of untracked raw
  scientist data (image variants, PNGs); never committed anywhere.
- canonical `lens/autolens_assistant/scripts/cluster_model_composition.py` — unrelated
  untracked scratch script.

## Plan

Run `/repo_cleanup`: archive the worktree branch via PyAutoGut, move the raw data out of the
checkout to the user's chosen archive location (never delete without the human), decide the
scratch script's fate.

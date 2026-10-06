# Add evidence-qualified profiling setup lookup

Type: feature
Target: autolens_assistant
Repos: autolens_assistant
Difficulty: medium
Consequence: judge
Autonomy: human-required
Filed: 2026-10-06
Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/150

Primary repo: @autolens_assistant. Workspace-only; no scientific library API changes.
Parent: draft/feature/pyautopulse/profiling_setup_browser.md, approved Phase 5.
Branch: feature/profiling-setup-advice
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-advice

## Approved plan

1. Add a stdlib catalogue lookup in autoassistant/ with explicit dataset/model, size, masked pixels, source resolution, PSF, precision, hardware and revision matching; read versioned index and hash-verified shards without scientific imports.
2. Return exact match / approximate analogue / no applicable evidence with known mismatches, unknown metadata, validation status, source revision, concrete record citations and bounded recommendations. Never combine incompatible timing axes or promote archived records.
3. Add skills/al_profiling_setup.md and relevant discovery/routing links; regenerate existing skill adapters. Distinguish per-likelihood timings from conditional fit-time arithmetic with explicit evaluations, concurrency, setup/compile and overhead assumptions.
4. Add contract/lookup tests covering applicable, incompatible, absent, malformed and unknown evidence, plus examples checked against the project catalogue. Use the project Phase5 producer in an isolated checkout. No jobs, acceptance, baseline campaign or temporal charts.

Tier: judge — merge mode: human /prm.

## Survey and authorization

Parent design and suggested Phase5 branches already approved. User now says start phase 5.
Both canonical target repos are main at origin/main; preserve existing untracked datasets
and assistant scripts. No active Mind claims conflict. Older unregistered worktrees remain
untouched under the previously approved isolation; no new shared-checkout coordination.
Phase4 project PR381 and Brain PR478 confirmed MERGED. Entry Heart STALE permits planning;
read fresh shipping gates, no RED override or merge authority carried forward.

## Original request (verbatim)

start phase 5

The complete approved Phase5 requirements and original redesign request remain in the parent.

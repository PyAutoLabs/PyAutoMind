# Local minimal Mind seed

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/498
Epic: scientist-adoption-pilot
Difficulty: medium
Consequence: judge
Parent: scientist_minimal_starter.md

## Original request

$prm and then conitnue

## Plan

Add opt-in --minimal-mind mode to @PyAutoMind scripts/spawn.py for a local, empty task-state seed. Reuse existing generator privacy rules and lifecycle index generation. No Memory, satellite family or GitHub workflows; canonical repos.yaml begins empty. Preserve default full-family generation byte-for-byte. Dry-run by default, --write creates only a new destination; reject existing directories/symlinks and incompatible --check/--stamp-family flags. Validate warnings and canaries before copying generated files to the user destination.

Detailed: generate_mind gains keyword-only minimal=False and selects an empty body-map constant and skips .github outputs only in that mode. New CLI branch stages generation in a temporary directory, fails closed on unclassified/canary output, and uses exclusive destination creation. Document local-only scope and canonical map population in docs/pyautobrain/spawn_spec.md and generated seed guidance. Test synthetic source privacy, unchanged defaults, invalid combinations and nonoverwrite; verify real generated lifecycle record/close. No installer, git initialization, remote changes, full bootstrapping claim or automatic upgrades.

Survey: canonical Mind main clean; no active claims. Source worktree feature/scientist-minimal-mind-seed under .worktrees/scientist-minimal-mind-seed. Mind lifecycle administration stays canonical main. Routine implementation authorized by ongoing epic request. Tier judge, human /prm.

Routing refinement: only Mind source changes; Scientist is the epic domain, not a second source claim.

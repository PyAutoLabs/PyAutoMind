# Workspace-local starter skill discovery

Type: feature
Epic: scientist-adoption-pilot
Difficulty: medium
Consequence: judge
Parent: scientist_minimal_starter.md

## Original request

continue

## Plan

Add starter-check/starter-write modes to @PyAutoBrain bin/project_discovery.py using its canonical skill discovery and Mind repo-path resolver. Install only Brain and Mind directory skills as relative links under the chosen workspace root .claude/skills, never into user-wide harness homes or source repos. Require both registered and present; reject duplicate names and any destination symlink/ownership conflict before writes; preserve unrelated local skills. Existing regular discovery modes remain unchanged.

Docs: add a minimal local Claude walkthrough in docs/adoption/guide.md using current Mind seed, explicit identities in repos.yaml, Scientist initializer, root-local discovery and PYAUTO_ROOT-scoped launch. No harness download/authentication, hidden optional organs, remote provisioning or shipping gate bypass. Show connect-project instructions and explain human fresh-chat acceptance remains necessary.

Tests: missing or ambiguous registrations/sources, collision preflight, protected parent paths, idempotence, relative links, and no user-home mutation. Integration exercise with a generated Mind seed and a differently named synthetic Scientist, one project without assistant, offline validation and rendering. Independent review before PR. Tier judge; human /prm.

Survey: Brain main clean, no active Brain claim. Existing unrelated worktrees left untouched. Branch feature/scientist-local-discovery; task .worktrees/scientist-local-discovery. Framework changes Brain only; user instance data stays separate.

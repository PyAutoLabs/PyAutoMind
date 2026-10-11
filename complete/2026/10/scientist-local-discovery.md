# Workspace-local starter discovery

Epic: scientist-adoption-pilot

Merged https://github.com/PyAutoLabs/PyAutoBrain/pull/518; issue #517 closed. Adds workspace-local Brain/Mind skill discovery and a minimal local Claude walkthrough. CLI integration verifies an empty Mind seed,40 relative skills,a differently named Scientist and an assistant-free synthetic project. This completes the implementation slice; fresh-session conversational acceptance remains a separate parent checkpoint.

Validation:30 discovery/installer tests,strict docs,independent CLEAN review at4db12a8. Exact-head Actions38158537089 (Python3.12/3.13) and38158537863 (docs) all pass. Merge7ef9e23 contains head4db12a8. Human authorized merge by “continue” following the explicit PR518 approval request.

Evidence archived at tmp/scientist-local-discovery/evidence/. No release obligation or irreplaceable science data.

## Original prompt

# Workspace-local starter skill discovery

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/517
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

Routing refinement: Brain source only; Scientist is the epic domain, not a second source claim.

## Implemented; awaiting merge

PR https://github.com/PyAutoLabs/PyAutoBrain/pull/518 at 4db12a8. 30 discovery/installer tests independently pass; strict docs pass. Actual generated Mind + 40 workspace-local skills + named Scientist + project without assistant validates/renders. Independent review CLEAN after fixing workspace-alias relative links. Fresh Heart STALE only absent current-source rehearsal, no RED/YELLOW. Evidence .worktrees/scientist-local-discovery/evidence/. Human /prm.

No Claude model session invoked. Real fresh-session conversational acceptance remains the next checkpoint in the parent, followed by optional organs and upgrades.

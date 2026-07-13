# Normalize profiling skill metadata for Codex

Type: maintenance
Target: autolens_profiling
Repos:
- @autolens_profiling
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised

Depends on: `maintenance/pyautobrain/codex_brain_skill_wrappers.md`

## Original request

> yes, make SKILL.md wrappers for PyAutoBrain and any other repos you see a Claude bias

## Scope

Change the existing `profile_likelihood` skill's frontmatter name to the
Codex-compatible `profile-likelihood`, validate the skill, and verify that the
dual-harness installer keeps the existing Claude directory while creating the
hyphenated Codex directory.

This task must remain queued until current `autolens_profiling` worktree claims
clear; do not override profiling work for a metadata-only change.

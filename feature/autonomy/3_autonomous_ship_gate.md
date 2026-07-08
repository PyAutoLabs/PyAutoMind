# Autonomous-ship gate — audit and define what an unattended ship must verify

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
- PyAutoHeart
Difficulty: medium
Autonomy: supervised
Priority: high
Status: draft

## Why

Heart's readiness verdict measures **organism state** — repo state, CI status,
open PRs in the cheap tick; verify_install-class deep checks on demand
(@PyAutoHeart/AGENTS.md). It never looks at a feature branch. Branch-level
signal today comes from `ship_*`'s own worktree pytest + smoke run, and the gap
is papered over by the human eyeballing the diff at PR sign-off. Remove the
human and the gap is live: an autonomous run could ship on "Heart GREEN" that
says nothing about the change being shipped.

## What

1. **Audit** what an unattended `ship_library` / `ship_workspace` run actually
   verifies on the branch today: which test scope (changed-repo pytest? full?),
   which smoke subset, what the Heart verdict does and does not cover, where
   "never modify code to make tests pass" is enforced.
2. **Define the autonomous-ship gate** in the autonomy contract's terms —
   proposal to validate or amend:
   `worktree pytest (affected repos, full suite) AND smoke subset AND review
   faculty CLEAN AND Heart GREEN` — all four, no substitutions; YELLOW is a
   human checkpoint at every autonomy level.
3. **Fix the gaps found** — e.g. if smoke coverage keys off main rather than
   the worktree, or if the tested repo set misses downstream dependents of the
   changed API.

## Boundaries

- Heart stays untouched as the release authority; if any branch-level check is
  genuinely a health check, it still runs from the dev workflow, not Heart
  (Heart is an observer of the organism, not of task branches).
- Smoke tests remain the small curated subset — do not mass-promote
  integration scripts to make the gate feel stronger.
- Keep the gate definition in `AUTONOMY.md` (one place), with `ship_*` skills
  pointing at it.

Blocked-by: 1_autonomy_contract.md, 2_review_faculty.md.

# Add a /morning start-of-day routine (PyAutoBrain composition skill)

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: high
Status: formalised

## What

A human-driven `/morning` door you run each morning that brings the workspace to
a clean, current, known-good state and surfaces the day's actionable items. It
**composes existing doors** (`/health`, `/hygiene`) plus the two workspace
scripts, and **owns no new state** — so it is a **skill** (like `/route`), not a
conductor or organ. Lives in PyAutoBrain alongside `/health` and `/hygiene`.
**Interactive/terminal only** — no Slack post; the existing automated morning
webhook is unchanged and complementary (passive notification vs. active driver).

## Phases

1. **Sync** *(auto — non-destructive)* — run `pull_all_main.sh`: every repo →
   `main`, ff-only. Report off-main / dirty / behind / **diverged** repos (the
   "out-of-date repos" signal).
2. **Clean slate** *(auto)* — run `clean_slate.sh`: restore shipped datasets,
   clear `output/`/`scratch/` cruft.
3. **Health & release** *(report)* — consult `/health`: Heart readiness verdict,
   **nightly-release status** (blocked ↔ green + the blocking issues, e.g.
   PyAutoBuild#126), red CI workflows, worktree status.
4. **Drift & hygiene** *(report)* — version-pin/stamp consistency across
   libraries + workspaces (e.g. the `2026.7.6.649 → 2026.7.9.1` drift), stale
   branches/worktrees, then consult `/hygiene` for cleanup candidates (dead
   files, git debris, dep/doc drift).
5. **Morning digest** — a short **prioritized terminal checklist**: 🚨 blocking ·
   ⚠️ drifted · 🧹 cleanable · ✅ clear-to-work, with a one-line verdict.

## Guardrails

- **Auto-run only the non-destructive steps** (sync, clean-slate). Everything
  that deletes/edits/bumps (stray cleanup, branch deletion, version bumps) is
  **surfaced for human approval**, never automatic.
- Compose, don't duplicate: call the real `/health` and `/hygiene` doors rather
  than reimplementing their checks. New logic is limited to the sync/clean-slate
  orchestration, the version-pin drift sweep, and the digest.

## Open decision for start_dev

`pull_all_main.sh` and `clean_slate.sh` currently live **untracked at the
workspace root**. To ship a shared, versioned skill they need a home: either move
them into a repo (PyAutoBrain `bin/`, or admin_jammy tooling) or reimplement the
orchestration inside the skill. Decide at start_dev.

## Origin

Distilled from a manual start-of-day cleanup pass on 2026-07-13 (repo sync,
clean-slate, org-wide version bump, stale-file/branch/worktree cleanup, release
+ CI status) — this feature packages that routine into one repeatable door.

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake; body restructured + Repos trimmed to PyAutoBrain by hand -->

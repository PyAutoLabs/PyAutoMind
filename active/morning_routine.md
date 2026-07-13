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
**Interactive/terminal only** — no Slack post; the two existing automated morning
webhooks are unchanged and complementary (passive notification vs active driver).

## Core principle: compose/read, don't recompute (anti-bloat)

The main risk is duplicating checks that already exist. Most candidate signals
are **already covered** and must be *read*, not rebuilt:

- **PyAutoHeart checks** (surfaced via `/health`): `ci_status`, `open_prs`,
  `version_skew`, `worktree_drift`, `url_check`, `profiling_drift`, `repo_state`,
  `manifest_drift`, `verify_install`.
- **Existing morning Slack jobs**: `morning_health.yml` (GREEN/YELLOW/RED verdict
  from Heart's badge.json) and `morning_status.yml` (24h main-activity digest).
  `/morning` reads Heart's badge/verdict and can reference the digest — never
  recomputes them.

## Phases

1. **Sync** *(auto — non-destructive)* — `pull_all_main.sh`: every repo → `main`,
   ff-only. Report off-main / dirty / behind / **diverged** repos.
2. **Clean slate** *(auto)* — `clean_slate.sh`: restore shipped datasets, clear
   `output/`/`scratch/` cruft.
3. **Overnight & health** *(report)* — consult `/health` for the Heart readiness
   verdict, nightly-release status (blocked ↔ green + blocking issues, e.g.
   PyAutoBuild#126), red CI, worktrees. **Plus an overnight-cron sweep**: the
   latest scheduled-run conclusions across `nightly-release`, `heart-health`,
   matrix CI, `workspace-validation`, `wiki-currency`, `spawn-drift`,
   `arxiv-digest` — the "what ran while I slept and did it pass" glance.
4. **Drift & hygiene** *(report)* — version-pin/stamp consistency across
   libraries + workspaces (e.g. the `2026.7.6.649 → 2026.7.9.1` drift), stale
   branches/worktrees, then consult `/hygiene` for cleanup candidates.
5. **Resume context** *(report)* — pick up where you left off: in-flight
   (`active.md`), parked (`parked.md`), queued (`queue.md`), open
   **pending-release PRs** (from `autonomy_log.md` / Heart `open_prs`), and
   worktrees with unpushed commits.
6. **Morning digest** — a short **prioritized terminal checklist**: 🚨 blocking ·
   ⚠️ drifted · 🧹 cleanable · 🔄 resume · ✅ clear-to-work, with a one-line
   verdict.

## Guardrails

- **Auto-run only the non-destructive steps** (sync, clean-slate). Everything
  that deletes/edits/bumps (stray cleanup, branch deletion, version bumps) is
  **surfaced for human approval**, never automatic.
- Compose, don't duplicate (see the core principle above).

## Deliberately out of scope (keep it lean)

- Security/Dependabot alerts → weekly, or fold into `/hygiene`'s dep-audit
  (Heart already flags yanked releases).
- Disk / venv / env health checks → noise.
- Triage-backlog grooming → weekly (`intake census`), not a daily-morning item.
- Re-deriving anything `/health` or the morning webhooks already produce.

## Open decision for start_dev

`pull_all_main.sh` and `clean_slate.sh` currently live **untracked at the
workspace root**. To ship a shared, versioned skill they need a home: either move
them into a repo (PyAutoBrain `bin/`, or admin_jammy tooling) or reimplement the
orchestration inside the skill. Decide at start_dev.

## Origin

Distilled from a manual start-of-day cleanup pass on 2026-07-13 (repo sync,
clean-slate, org-wide version bump, stale-file/branch/worktree cleanup, release
+ CI status) plus a follow-up scoping/research pass on the same day — this
feature packages that routine into one repeatable door.

<!-- formalised by the Intake (Conception) Agent on 2026-07-13 from user-intake; body restructured + enriched with research-backed additions (overnight-cron sweep, resume-context) and an explicit anti-bloat out-of-scope list -->

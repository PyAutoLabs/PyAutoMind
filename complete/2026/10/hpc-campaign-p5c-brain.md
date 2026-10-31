# hpc-campaign phase 5c — Cortex pull reads campaign digests; scheduler allowlist + action guard

Merged 2026-10-31: PyAutoBrain#548 (issue PyAutoBrain#547). Tier judge, human /prm, under the Heart RED development override for hpc-campaign phase 5 (2026-10-30).

## What shipped
- Cortex conductor `pull`: a project row with `campaign_file:` runs `<sync_cli> status <campaign_file>` instead of `jobs`/squeue; a row with `digest:` previews `cortex sync-runs <key> --dry-run` (PyAutoCortex#83). Pull writes nothing (human ruling 2026-10-31); recording stays `cortex.py sync-runs <key>`. The digest lives where `hpc/sync status` pulls it: `hpc/campaign/<name>/digest.json` with `tasks.jsonl` beside it.
- AUTONOMY.md "Scheduler actions" + skills/cortex/cortex.md: a campaign's jobs start and change only through `hpc/sync act <submit|resubmit|hold|release|throttle|update-pending|cancel>` (logged to `<project_root>/campaign/<name>/actions.log`); `hpc/sync submit|push-submit` sbatch one hand-written script outside any campaign; reading is free.
- `bin/scheduler_action_guard.py`: PreToolUse(Bash) hook for Claude and Codex, the same contract as mind_commit_guard. Refuses raw sbatch, scancel, srun, salloc (human ruling), mutating scontrol and raw `autofit.campaign submit`, including over ssh, inside bash -c/eval, behind wrappers (xargs, parallel, find -exec), and in heredocs fed to a shell. Allows `scontrol show`, help/usage/version and `sbatch --test-only`. The escape hatch `PYAUTO_SKIP_SCHEDULER_GUARD=1` is kept (human ruling) and works only from the environment or as the clause's leading assignment.
- The clone profile classifies `skills/hpc_campaign.md` as autolens_assistant domain content.

## Review
- Independent review (a different model from the author's): 4 findings, all fixed with tests: quote/backslash pre-filter, ssh options after the host, escape hatch matched anywhere, read-only sbatch flags. 175 guard and conductor tests.
- Pre-existing failures on main: test_hygiene_conductor (6) and test_skill_install (10).

## Registration (human-approved 2026-10-31)
- Claude: workspace-root `.claude/settings.json` Bash hooks (local, untracked). Live-tested: a raw `scancel` was denied in-session.
- Codex: PyAutoMind#520, which adds `scheduler-action-guard` to CODEX_HOOK_DEFINITIONS and to Brain's codex_hooks. After merge, session_hook_propagate regenerates Brain's `.codex/hooks.json`, and the human trusts the new hook hash with Codex `/hooks`.

## Original prompt

Issued: 2026-10-30
Epic: hpc-campaign
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/547
Phase: 5c
Blocked-by: phases 2–4 (COMPLETE 2026-10-30); ruling F3 (yes)
Consequence: judge
Autonomy: human-required
Merge-order: after 5a v2 and 5b (uses their verb/CLI names)

# HPC campaign phase 5c — Brain cortex conductor digest + scheduler governance hook

Original request (human, 2026-10-30): "spread across grid bases, prm on those and then we do next phase 5"; plan
approved with "Override + approve" (5a assistant, 5b Cortex, 5c Brain in parallel; 5d pipeline adoption deferred
until DR1 v1.0 ships).

Lane prompt: Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/PROMPT_hpc_campaign.md §Phase 5.
@PyAutoBrain: Cortex conductor pull reads the digest (hpc/sync status) instead of raw squeue; scheduler action allowlist in AUTONOMY.md and skills/cortex/cortex.md; PreToolUse hook for Claude and Codex (F12) blocking raw sbatch|scancel|scontrol over ssh outside hpc/sync act/submit; audit-log contract; hook tests.

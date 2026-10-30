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

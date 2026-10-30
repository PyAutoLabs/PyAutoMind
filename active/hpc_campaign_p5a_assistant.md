Issued: 2026-10-30
Epic: hpc-campaign
Issue: https://github.com/PyAutoLabs/autolens_assistant/issues/172
Phase: 5a
Blocked-by: phases 2–4 (COMPLETE 2026-10-30); ruling F3 (yes)
Consequence: judge
Autonomy: human-required
Merge-order: step-0 PR first; v2 PR stacked

# HPC campaign phase 5a — assistant hpc template v2, sync verbs, skill

Original request (human, 2026-10-30): "spread across grid bases, prm on those and then we do next phase 5"; plan
approved with "Override + approve" (5a assistant, 5b Cortex, 5c Brain in parallel; 5d pipeline adoption deferred
until DR1 v1.0 ships).

Lane prompt: Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/PROMPT_hpc_campaign.md §Phase 5.
@autolens_assistant: step 0 fold euclid pipeline hpc/sync drift (pull [dir…]/restrict_pull_dirs, sbatch passthrough, skip-missing-dirs, help-before-conf) into the template as its own PR; then template v2 (per-stage batch template, EXIT/USR1 traps writing the task record, set -euo pipefail, campaign.yaml example), hpc/sync verbs status/plan/act{hold,release,throttle,update-pending,resubmit,cancel}/report (one ssh each, python -m autofit.campaign on the cluster, act audit log), skills/hpc_campaign.md, wiki operations/hpc.md in WRITING_STYLE register. Offline tests with a fake ssh.

- issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/82
- completed: 2026-10-30
- organ-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/83
- epic: hpc-campaign (phase 5b; ledger draft/research/autofit/hpc_campaign_epic.md)
- summary: `cortex sync-runs <project> --digest <path> [--dry-run]` — run lines open→running (with a `run` log entry)
  and `done` with counts when every named task index is terminal; compound pending slices expanded; one validated
  write; never result/lesson/## Now; never adds/removes runs; idempotent. projects.yaml `campaign_file`/`digest`
  validated by `cortex check`. Schema decision 64 (ledger's "62"; 62/63 taken); REFERENCE boundary paragraph.
- tests: 91 passed; cortex check OK; CI `check` green. Independent review FINDINGS (HIGH premature done on pending
  slices, MEDIUM partial write, LOW newest-first) fixed in d590eac with tests; fixes not re-reviewed.
- note: dry run vs the real DR1 digest closes 58 euclid_dr1 runs — applying it to the live ledger is a human ask.
- heart: shipped and merged under the human-authorized Heart RED development override; merge by separate /prm.

## Original prompt

Issued: 2026-10-30
Epic: hpc-campaign
Issue: https://github.com/PyAutoLabs/PyAutoCortex/issues/82
Phase: 5b
Blocked-by: phases 2–4 (COMPLETE 2026-10-30); ruling F3 (yes)
Consequence: judge
Autonomy: human-required

# HPC campaign phase 5b — cortex sync-runs from a campaign digest

Original request (human, 2026-10-30): "spread across grid bases, prm on those and then we do next phase 5"; plan
approved with "Override + approve" (5a assistant, 5b Cortex, 5c Brain in parallel; 5d pipeline adoption deferred
until DR1 v1.0 ships).

Lane prompt: Workspace/Science/scratch/pyautolens_ii_campaign_results_scoping_2026-10-28/PROMPT_hpc_campaign.md §Phase 5.
@PyAutoCortex: `cortex sync-runs <project> --digest <file>` flips open→running and calls done with finished/failed counts (never result/lesson); projects.yaml campaign_file + digest fields; decision 62 text per ruling F3; REFERENCE boundary paragraph (status is a cluster fact; result/lesson stay human). Tests + cortex check.

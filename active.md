# Active Tasks

## timing-noise-audit-p8-phase3b-intervals
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- prompt: active/timing_noise_audit_phase8_phase3b_intervals.md
- session: Claude Code CLI (Opus 5.5 main + Opus worker under --auto, supervised)
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/410 (judge tier; human /prm; flagged decisions: C1 5-round minimum on 4 repeats, C5 jit_profile estimator)
- autonomy: --auto launch 2026-10-09 ("prm and then do 3b and leftovers fully wrap up --auto"); effective supervised (bug, Consequence judge); decide-and-flag at ship
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p8-phase3b-intervals
- repos:
  - autolens_profiling: feature/timing-noise-audit-p8-phase3b-intervals
- tier: judge (human /prm)
- heart-ack: Heart reason set of 2026-10-09 human-acknowledged 2026-10-09 ("work on heart will fix later") for the timing-noise phase PRs

## timing-noise-audit-p9-familywise-policy
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- prompt: active/timing_noise_audit_phase9_familywise_policy.md
- session: Claude Code CLI (Opus 5.5 main + Opus worker under --auto, supervised)
- status: awaiting-merge
- pr: https://github.com/PyAutoLabs/autolens_profiling/pull/411 (judge tier; human /prm AFTER #410; flagged: C11 kill gate INCONCLUSIVE on 4 rounds (--reps >= 6 or 4-round rule), GPU memo "below MDI" at 0.94 % paired MDI, P2 drift tolerances)
- autonomy: --auto launch 2026-10-09 ("do all work until complete --auto"); effective supervised (bug, Consequence judge); decide-and-flag at ship
- stacked-on: timing-noise-audit-p8-phase3b-intervals (PR #410; claim guard reports that sibling's autolens_profiling claim — deliberate stack, merges after #410)
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p9-familywise-policy
- repos:
  - autolens_profiling: feature/timing-noise-audit-p9-familywise-policy
- tier: judge (human /prm)
- heart-ack: Heart reason set of 2026-10-09 human-acknowledged 2026-10-09 ("work on heart will fix later") for the timing-noise phase PRs

## timing-noise-audit-p10-headline-completion
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/362
- issued: 2026-10-02
- prompt: active/timing_noise_audit_phase10_headline_completion.md
- session: Claude Code CLI (Opus 5.5 main + Opus worker under --auto, supervised)
- status: workspace-dev
- autonomy: --auto launch 2026-10-09 ("do all work until complete --auto"); effective supervised (bug, Consequence judge); decide-and-flag at ship
- stacked-on: timing-noise-audit-p9-familywise-policy (PR #411; deliberate stack, merges after #411)
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p10-headline-completion
- repos:
  - autolens_profiling: feature/timing-noise-audit-p10-headline-completion
- tier: judge (human /prm)
- heart-ack: Heart reason set of 2026-10-09 human-acknowledged 2026-10-09 ("work on heart will fix later") for the timing-noise phase PRs


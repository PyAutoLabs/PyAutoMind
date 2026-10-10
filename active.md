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
- status: awaiting-merge
- prs:
  - autolens_profiling: https://github.com/PyAutoLabs/autolens_profiling/pull/412 (stacked on #411 → #410; merge after both)
- autonomy: --auto launch 2026-10-09 ("do all work until complete --auto"); effective supervised (bug, Consequence judge); decide-and-flag at ship
- stacked-on: timing-noise-audit-p9-familywise-policy (PR #411; deliberate stack, merges after #411)
- worktree: ~/Code/PyAutoLabs-wt/timing-noise-audit-p10-headline-completion
- repos:
  - autolens_profiling: feature/timing-noise-audit-p10-headline-completion
- tier: judge (human /prm)
- heart-ack: Heart reason set of 2026-10-09 human-acknowledged 2026-10-09 ("work on heart will fix later") for the timing-noise phase PRs
- heart-red-override:
  - authorization: live human, 2026-10-09 (AskUserQuestion in the main session) — proceed under AUTONOMY.md "Human override for Heart RED (development only)" for phase 10's PR; recorded on https://github.com/PyAutoLabs/autolens_profiling/issues/362 (latest comment)
  - red reasons: `release validation FAILED (stage integrate)` (+ 8 manifest-drift yellow reasons)
  - branch gates passed: tests 1405 passed / 6 skipped; smoke import of edited cells OK; all lint.yml checks locally; independent Opus review FINDINGS (7) fixed → re-review CLEAN
  - scope: commit / push / PR-open only; merge needs a separate human /prm with all checks green; no release

## heart-fitness-dispatch
- issue: https://github.com/PyAutoLabs/autofit_workspace_test/issues/109
- issued: 2026-10-10
- prompt: active/heart_fitness_dispatch_refactor_adoption.md
- session: Codex GPT-6; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/heart-fitness-dispatch
- repos:
  - autofit_workspace_test: feature/heart-fitness-dispatch
- tier: judge (human /prm)
- heart-red-override: live user 2026-10-10 authorized named repair scopes for `release validation FAILED (stage integrate)`; development/PR only, no merge/release/rehearsal; quote on issue.

## heart-hierarchical-backend
- issue: https://github.com/PyAutoLabs/autolens_workspace/issues/588
- issued: 2026-10-10
- prompt: active/heart_hierarchical_backend_adoption.md
- session: Codex GPT-6; session ID unavailable
- status: workspace-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/heart-hierarchical-backend
- repos:
  - autolens_workspace: feature/heart-hierarchical-backend
- tier: judge (human /prm)
- heart-red-override: live user 2026-10-10 authorized named repair scopes for `release validation FAILED (stage integrate)`; development/PR only, no merge/release/rehearsal; quote on issue.

## heart-manifest-drift
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/497
- issued: 2026-10-10
- prompt: active/heart_generated_manifest_drift.md
- session: Codex GPT-6; session ID unavailable
- status: library-dev
- worktree: /home/jammy/Code/PyAutoLabs/.worktrees/heart-manifest-drift
- repos:
  - PyAutoBroca: feature/heart-manifest-drift
  - PyAutoDNA: feature/heart-manifest-drift
  - PyAutoCortex: feature/heart-manifest-drift
  - PyAutoEyes: feature/heart-manifest-drift
  - PyAutoEars: feature/heart-manifest-drift
  - PyAutoPulse: feature/heart-manifest-drift
  - PyAutoInsight: feature/heart-manifest-drift
  - PyAutoNerves: feature/heart-manifest-drift
  - PyAutoGut: feature/heart-manifest-drift
  - PyAutoScientist: feature/heart-manifest-drift
  - .github: feature/heart-manifest-drift
  - pyautolabs.github.io: feature/heart-manifest-drift
- tier: judge (human /prm)
- heart-red-override: live user 2026-10-10 authorized generated-guidance repair under `release validation FAILED (stage integrate)`; non-causal development scope only, no merge/release/rehearsal.

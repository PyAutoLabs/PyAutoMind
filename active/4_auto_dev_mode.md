# --auto mode through start_dev → ship_* — consume the Autonomy header

Type: feature
Target: autonomy
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: large
Autonomy: supervised
Priority: high
Status: draft

## Why

This is the payoff task: the dev workflow gains an explicit autonomous mode so
`Autonomy: safe` tasks run start-to-PR without interactive checkpoints, and the
human's job moves to validating an open PR instead of approving every step.

## What

Add `--auto` to the `start_dev → start_library/start_workspace → ship_*`
lifecycle (skill bodies + any `bin/pyauto-brain` plumbing):

1. **Activation** — only when the human launches with `--auto`; the task's
   `Autonomy:` header (subject to the per-work-type caps in `AUTONOMY.md`)
   then selects the behaviour. Default invocations are byte-for-byte today's
   flow.
2. **`safe` behaviour** — the plan is written to the GitHub issue (and Mind
   `active.md` summary) instead of being held for Plan-Mode approval;
   implementation proceeds; ship is gated by the autonomous-ship gate
   (`3_autonomous_ship_gate.md`); the run ends at **PR open**, with the PR body
   carrying the plan, the review-faculty verdict, test/smoke counts, and a
   short validation checklist for the human.
3. **Stop-at-PR is hard** — merge and issue-close remain human acts regardless
   of level (standing preference). An explicit additional flag may extend to
   merge later; do not build it in this task.
4. **Calibration hook** — every `--auto` run appends its outcome row to the
   calibration log defined in `1_autonomy_contract.md`.
5. **Failure behaviour** — a failed gate (tests, review FINDINGS, Heart
   YELLOW/RED) downgrades the run to a human checkpoint: state written to the
   issue, session ends cleanly, nothing force-shipped. Never modify code to
   make tests pass remains absolute.

## Boundaries

- `supervised` behaviour (checkpoint-and-continue) is `5_checkpoint_and_continue.md`,
  not this task — here `supervised` simply means today's interactive flow.
- No new conductor: this is the existing dev-workflow skills consuming the
  contract, per the growth rule (no new agents without demonstrated need).

Blocked-by: 1_autonomy_contract.md, 2_review_faculty.md, 3_autonomous_ship_gate.md.
First consumer: `6_refactor_conductor.md` work-type runs.

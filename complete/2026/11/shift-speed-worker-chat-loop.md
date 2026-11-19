# Shift speed: worker chat loop (M3.7a)

Completed 2026-11-19. Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/686

M3.7a of the autonomous-orchestrators epic. Added rulings S1 and S3 to `AUTONOMY.md` under "Shift speed — 2026-11-19". The shift worker template now runs the changed test modules, the witness, the targeted smoke and one independent review, with no adversary pass; leg 5 is kept for batch launches outside a shift, and the Heart leg is stated unchanged. The `ship_library` skill and its reference follow the rulings. 6 new tests.

## Merge receipts

- PyAutoBrain#687: 66ae0cf3758f1ff800799c1e41e1e58cde49b610 (merged by the human's /prm, 2026-11-19)

Feature head 9ea459871 is an ancestor of origin/main. Organ repo: no release obligation.

## Validation and review

Review by Fable 5.2: round 1 FINDINGS (leg 5 kept for batch launches outside a shift; Heart leg stated unchanged), fixed. One CI red on the skill line budget, fixed. Tier: judge (no shadow row).

## Original prompt

# M3.7a Shift worker runs the chat loop: changed tests, witness, targeted smoke, one review

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: high
Status: draft
Filed: 2026-11-19
Epic: autonomous-orchestrators
Phase: 10
Consequence: judge
Witness: (1) `AUTONOMY.md` has a section dated 2026-11-19 recording rulings S1 and S3 below, and legs 1 and 5 of "The autonomous-ship gate" point to it; (2) the prompt rendered from `agents/conductors/batch/worker_template.md` for a library task tells the worker to run the changed test modules and the `Witness:`, not the full suite, and contains no instruction to run `pyauto-brain review ... --adversary`; a test asserts both; (3) the same prompt still requires one independent review with verdict CLEAN and the targeted smoke; (4) the same prompt requires the dependants' full suites when the review surface flags a public API change; (5) the Brain suite passes
Lane: any
Unattended: ready

## Request (verbatim)

Human, 2026-11-19, in chat, on the orchestrator speed review (`Science/scratch/orchestrator_speed_review_2026-11-19/review.md`): "When I implement features in a claude chat we run the smokes quick, probably like a minute. [...] we still seem to be normalizing 18 minutes of testing plus 10+ minutes to merge. What would a solution which is much closer to the faster turn over look like?" Then, on the fast design and its rulings: "approved, all rulings yes".

## Why

Measured over shifts 2026-11-18-pm, -pm2 and 2026-11-19-am (7 workers): the real work takes 10 to 16 minutes per task. The full local unit suite added 5 to 19 minutes, and 10 to 15 more when laptop load caused false failures and a rerun. PR CI runs the same suite on Python 3.12 and 3.13 and is the verdict the merge reads. The worker adversary pass cost 60 to 130k tokens per task; the close-out session (unattended) or the human (`/prm`) is already the second reader.

## Rulings (human, 2026-11-19)

- **S1, leg 1 in a shift.** The worker runs the test modules its diff changes or that cover the changed code, plus the `Witness:`. PR CI is the full-suite verdict for the shipped repo. The dependants' full suites still run locally when the diff changes public API (they are not in the PR's CI). A red CI after the worker has ended sends the PR to `/prm`, as now.
- **S3, leg 5 in a shift.** The worker runs one independent review (leg 3) and no adversary pass. The adversary is the close-out session for an unattended merge ("Stage-2 adversary amendment — 2026-11-04") and the human at `/prm` for everything else.

Outside a shift (an `--auto` chat) nothing changes.

## Shape

- `AUTONOMY.md`: a "Shift speed — 2026-11-19" section with S1 and S3 (M3.7b and M3.7e add S2 and S4 to S7 to the same section); one-line pointers from legs 1 and 5.
- `agents/conductors/batch/worker_template.md`: changed test modules and witness; the review subagent starts beside the tests and the targeted smoke; the PR opens as soon as they pass; no adversary step.
- `skills/ship_library/ship_library.md`: the shift-worker branch of the tests step and the adversary line (about line 105) follow the same rule.
- Workers cap any pytest they do run at `-n 4`.

## Order

First of M3.7. M3.7b and M3.7c touch the same `AUTONOMY.md` section and `_orchestrator.py`, so they follow one at a time.

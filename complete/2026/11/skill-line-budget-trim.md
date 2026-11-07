- issue: none (PR is the tracking surface)
- completed: 2026-11-07
- prs: PyAutoBrain#600 PyAutoMind#548
- summary: batch skill 274 -> 200 lines, cortex 232 -> 199, Mind create_issue 203 -> 197, with no rule removed (detail moved verbatim to skills/batch/reference.md and skills/cortex/reference.md). Brain tests.yml prints token_load.py report on every PR. With #597 also merged, check_skill_line_counts.sh reports all 40 skills within budget. PyAutoMind#548 also retired the witness-campaign queue entry (human, 2026-11-07).
- parent: draft/maintenance/organs/reduce_session_token_load.md (stays draft)
- merged-by: human /prm 2026-11-07 (cloud session)

## Original prompt

# Bring batch, cortex and create_issue under the 200-line skill budget

Type: maintenance
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Witness: `bin/check_skill_line_counts.sh` reports batch, cortex and Mind's create_issue at <= 200 lines with no gate, refusal or rule removed; Brain CI prints `token_load.py report`; both suites pass.
Review-minutes: 10
Parent: draft/maintenance/organs/reduce_session_token_load.md
Filed: 2026-11-07 (slice of the parent, picked in the cloud queue session: "Find 4 grouped tasks and do them"; prompt file written at close-out, the claim ran from the parent)

Four grouped items, none touching PyAutoBrain#597's files: trim Brain `batch`
(274) and `cortex` (232) and Mind `create_issue` (203) under 200 lines by
moving detail verbatim into `reference.md`; print `token_load.py report` in
Brain `tests.yml`.

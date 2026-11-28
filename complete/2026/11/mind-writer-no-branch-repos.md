## mind-writer-no-branch-repos
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/745
- completed: 2026-11-28
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/746
- `_mind_writer.validate_op` refuses an `active.md` append, or the lines an `active.md` edit adds, carrying a `(no branch …)` repos bullet (`no_branch_repo_errors`, beside `pr_key_errors`). Bare `  - Repo` and unchanged legacy lines are still accepted.
- Writer side of `complete/2026/11/parked-claim-not-a-claim.md` (PyAutoBrain#742, PR #744).
- Trap: `test_questions_inbox.py::test_the_question_add_op_lands_through_minds_own_add_text` asserts no `sys.path` entry contains "mind-writer-", so it fails in any local worktree whose folder name contains that string; pick task names without it.

## Original prompt

# The Mind writer refuses a `(no branch …)` repos entry in an active.md row

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: medium
Status: draft
Filed: 2026-11-28
Issued: 2026-11-28
Epic: autonomous-orchestrators
Consequence: judge
Witness: a test that fails on the base commit: `validate_op` refuses an `active.md` append (and an `active.md` edit whose new text adds one) carrying a `  - <Repo>: (no branch …)` or `  - <Repo> (no branch …)` bullet, with a message telling the worker a park before the first edit writes no `- repos:` block; a row with a real branch is still accepted
Review-minutes: 5
Lane: any
Unattended: never

Human request (2026-11-28, verbatim): "do this Still open: the idea of refusing a (no branch entry in _mind_writer.validate_op is noted in the record but not filed."

Follow-up to `complete/2026/11/parked-claim-not-a-claim.md` (PyAutoBrain#742, PR #744). That fix made the claim readers ignore a `(no branch …)` entry and told the worker template not to write one. This closes the writer side: `agents/conductors/batch/_mind_writer.py` `validate_op` already refuses a bare `pr:` key in an `active.md` append via `pr_key_errors`; a sibling check refuses a no-branch repos bullet, both when `bin/shift_ledger.py` queues the op and when the writer applies it.

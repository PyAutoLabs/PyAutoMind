# PyAutoBrain size reduction: retire superseded batch paths, dead code, test consolidation

Type: refactor
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: medium
Status: active
Filed: 2026-11-22
Issued: 2026-11-22
Lane: any

A refactor review of @PyAutoBrain (2026-11-22) found the code is not bloated by
copy-paste; the size that can go is superseded features plus scattered dead
code, and the test suite can shrink by consolidation. The human approved, in
chat on 2026-11-22:

1. Remove the August `batch collect` flow (the hand-dispatched batch record,
   `collect` scoring, the review packet and `--integration`), superseded by the
   shift orchestrator: the collect code in `_batch.py`, `_integration.py`,
   `packet.js`, their tests and docs.
2. Remove the per-worker @mention path, unreachable since M3.5
   (`_mention_triggers` returned `[]`); keep the event-comment retry.
3. Remove the one-off `batch questions --backfill`.
4. Remove the caller-less board overnight functions and their tests.
5. Sweep confirmed dead code and unused imports.
6. Move dated incident history out of code comments and docstrings.
7. Consolidate duplicated test setup, parametrize same-body tests, and drop
   tests that are strictly redundant.

Not approved, so untouched: doctrine and prompt-wording pin tests, and the
"tombstone" absence tests.

Items 1 to 4 remove CLI surface (`batch collect`, `batch questions`), so this
is not a pure refactor; nothing else changes CLI behaviour.

Witness: the full suite passes; `bin/pyauto-brain batch collect` and `batch
questions` exit 2 (unknown verb); for the comment-only pass, every touched
file's AST with docstrings stripped equals its AST before the pass.

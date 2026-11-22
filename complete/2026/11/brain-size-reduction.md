# PyAutoBrain size reduction: retired batch paths, dead code, test consolidation

Shipped as PyAutoBrain#701 (issue PyAutoBrain#700), merged 2026-11-22.

- Removed the August `batch collect` flow (collect code in `_batch.py`, `_integration.py`, `packet.js`, three test files), superseded by the shift orchestrator.
- Removed the per-worker @mention path; the retry for needs-you event comments stays.
- Removed `batch questions --backfill`, and with it the `questions` verb.
- Removed the caller-less board overnight functions.
- Swept dead code and unused imports across Python and shell.
- Moved dated incident history out of comments and docstrings (comment-only, AST-checked).
- Consolidated test setup into `tests/_helpers.py` and `tests/_shift_fixtures.py`; parametrized same-body tests; removed redundant ones.

Python source 46,657 → 42,971 lines; tests 40,294 → 37,314; test functions 2,106 → 1,899; collected cases 2,560 → 2,451.

Witness: full suite 2,448 passed, 3 skipped; CI green on 3.12 and 3.13; the surviving batch verbs print byte-identical output before and after against a real Mind. A live watcher tick was not run.

Left for follow-up: the dashboard batch status box still keys its review button on `collected:`; `plan` still reads a "carried" outcomes block only collect wrote; PyAutoMind (`batches/AGENTS.md`, `REFERENCE.md`, packet template) and PyAutoHeart (`bin/pyauto-heart` help) still mention `batch collect`; about 18 `--help` docstrings still carry history; the nine pure launcher scripts and the `repos.yaml` parser unification from the review were not done.

## Original prompt

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

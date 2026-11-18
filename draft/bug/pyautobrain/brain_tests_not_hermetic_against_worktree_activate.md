# Brain test suite is not hermetic against a task worktree's activate.sh organ paths

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: normal
Status: formalised
Consequence: notify
Witness: with a task worktree's `activate.sh` sourced (PYAUTO_ROOT, PYAUTO_BRAIN, PYAUTO_MIND, PYAUTO_HEART, PYAUTO_HANDS, PYAUTO_TASK exported), `pytest tests/` in PyAutoBrain passes in full, including `tests/test_grouped_organ_consumers.py::test_hygiene_map_and_heart_board_find_grouped_checkouts`; CI stays green
Review-minutes: 0
Unattended: ready
Lane: any

## Bug

Running the PyAutoBrain suite from a task worktree after `source <wt>/activate.sh`
(as `start_library` / `ship_library` instruct) fails
`tests/test_grouped_organ_consumers.py::test_hygiene_map_and_heart_board_find_grouped_checkouts`:
`_hygiene_repos.resolve_map()` returns `$PYAUTO_MIND/repos.yaml` (the worktree's
Mind) instead of the test's tmp tree. `candidate_map_paths()` treats `PYAUTO_MIND`
as a hard override by design; the test only sets `PYAUTO_ROOT`. CI has none of
these variables, so it passes there; the gap shows only locally, and it forced
`env -u PYAUTO_MIND` during the PyAutoBrain#676 ship (2026-11-18). The same failure
reproduces on origin/main.

`bin/worktree.sh` writes `activate.sh` exporting PYAUTO_TASK, PYAUTO_ROOT,
PYAUTO_BRAIN, PYAUTO_MIND, PYAUTO_HEART and PYAUTO_HANDS.

## Fix

- `tests/conftest.py` gains one autouse fixture that `monkeypatch.delenv`s those
  organ-path variables (raising=False), matching CI. Tests that need one set it
  themselves (autouse runs first, so their `setenv` still wins). Keep it
  alongside the existing isolation fixtures, with a docstring saying why.
- Run the full suite twice: plain, and with a task worktree's `activate.sh`
  sourced. Both must pass with no deselects.

<!-- formalised by the Intake (Conception) Agent on 2026-11-18 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/b01cd956-03bd-4fd1-b437-0416381bb071/scratchpad/raw2.md -->

- summary: fixed in commit 748f8c0bb (this PR). The module's autouse `forget_the_resolver` fixture now deletes `PYAUTO_ROOT` and `PYAUTO_ROOT_REASON` via monkeypatch. `test_an_explicit_override_is_never_second_guessed` still sets its own value.
- witness: `PYAUTO_ROOT=/home/user pytest tests/test_repos_sync_root_default.py` passes. The full suite gives 728 passed, 1 skipped, with and without the variable exported.

## Original prompt

# `test_repos_sync_root_default` inherits an exported `PYAUTO_ROOT` and fails

Type: bug
Target: PyAutoMind
Repos:
- PyAutoMind
Themes:
- ci
Difficulty: small
Autonomy: safe
Priority: low
Status: formalised
Filed: 2026-11-05
Consequence: glance
Witness: `PYAUTO_ROOT=/somewhere pytest tests/test_repos_sync_root_default.py` passes.
Review-minutes: 2
Unattended: ready

`workspace_root()` treats an exported `PYAUTO_ROOT` as "the operator's word" and never second-
guesses it, so `test_a_root_that_does_not_hold_this_checkout_is_refused` fails whenever the shell
running the suite has it exported — which the Brain CLI does for its children (observed
2026-11-05 after a `pyauto-brain intake` run in the same shell). Fix: the module's autouse fixture
clears `PYAUTO_ROOT` / `PYAUTO_ROOT_REASON` via monkeypatch; the override test sets its own.

<!-- formalised by the Intake (Conception) Agent on 2026-11-05 from file:/tmp/claude-0/-home-user/ad8c6486-73f7-504b-b742-a7b629366ade/scratchpad/intake/b_root_env_leak.md -->

# smoke-tests.yml cache-state step uses `warnings` without importing it — every workspace smoke leg goes red

Type: bug
Target: pyautoheart
Repos:
- PyAutoHeart
Themes:
- ci
- smoke-tests
Difficulty: small
Autonomy: supervised
Priority: high
Status: formalised
Consequence: notify
Review-minutes: 2
Witness: a workspace PR whose smoke scripts all pass gets a green smoke leg (the cache-state step exits 0 and writes cache_state.json).
Filed: 2026-11-09

## Symptom

`PyAutoHeart/.github/workflows/smoke-tests.yml` (reusable workflow called by every workspace's
`smoke_tests.yml@main`), the cache-state `python - <<'PY'` heredoc at ~line 771-777 imports only
`json, os, subprocess, Path` but calls `warnings.simplefilter("ignore", SyntaxWarning)` — copied from the step at
~line 288-291, which does `import ast, os, sys, warnings`. Result:

    File "<stdin>", line 6, in <module>
    NameError: name 'warnings' is not defined. Did you mean: 'Warning'?
    ##[error]Process completed with exit code 1.

Seen on autolens_workspace_test#358 run 42595455314 (2026-11-09), both smoke legs, after the smoke scripts had
already run. Likely introduced with the recent `smoke-tests: carry the numba cache …` change (#328 / 419f348).

## Fix

Add `import warnings` to that heredoc (or drop the line — the step parses no scripts), and extend
`tests/test_workflow_wiring.py`, which already runs some workflow heredocs verbatim, to execute this one too.

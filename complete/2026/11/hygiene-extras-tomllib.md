`pyauto-brain hygiene extras` (and the default scan's extras row) crashed with ModuleNotFoundError: tomllib because
hygiene.sh ran the helper on the bare python3 (3.10 on the WSL laptop). Fixed in PyAutoBrain#582 (merged 2026-11-04):
hygiene.sh runs it on the newest python3.13/3.12/3.11 present; the helper falls back to tomli and otherwise emits a
skipped row (json status error, summary count -1 → advisory). Live scan now runs: no exposure drift.

## Original prompt

# hygiene extras crashes on Python 3.10 (no tomllib)

Type: bug
Target: PyAutoBrain (agents/conductors/hygiene)
Consequence: glance
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/581

Found 2026-11-04 (health/hygiene review): `pyauto-brain hygiene` prints a `ModuleNotFoundError: tomllib`
traceback for the extras mode on the WSL laptop (system python3 = 3.10). Human: "Continue to next tasks".

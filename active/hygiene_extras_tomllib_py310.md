# hygiene extras crashes on Python 3.10 (no tomllib)

Type: bug
Target: PyAutoBrain (agents/conductors/hygiene)
Consequence: glance
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/581

Found 2026-11-04 (health/hygiene review): `pyauto-brain hygiene` prints a `ModuleNotFoundError: tomllib`
traceback for the extras mode on the WSL laptop (system python3 = 3.10). Human: "Continue to next tasks".

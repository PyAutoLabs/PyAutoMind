# install.sh --check/--write-project-discovery rejects repo names (argparse ordering)

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: easy
Autonomy: supervised
Priority: medium
Status: formalised
Filed: 2026-11-03
Issued: 2026-11-03
Consequence: glance
Witness: `pytest PyAutoBrain/tests/test_skill_install.py` goes from 10 failed (on main) to 22 passed.

## Finding

Measured on the PyAutoBrain#564 test run (2026-11-03): `tests/test_skill_install.py`
fails 10–11 tests on main with `project_discovery.py: error: unrecognized arguments:
<repo>`. `bin/install.sh` calls `project_discovery.py check --root "$PYAUTO_ROOT" "$@"`;
with the names after `--root`, `parse_args()` has already bound the `nargs='*'`
`repos` positional to an empty list, so the trailing names are rejected.

## Fix

`parse_intermixed_args()` in `bin/project_discovery.py main()`. Filed and fixed at the
human's request; shipped on the shared organs-batch Brain PR.

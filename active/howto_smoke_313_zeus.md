# HowTo smoke (3.13) red: `tutorial_searches.py` cannot import `zeus`

Type: bug
Target: HowToGalaxy
Repos:
- HowToGalaxy
Difficulty: small
Autonomy: supervised
Priority: high
Status: active
Consequence: judge
Filed: 2026-10-22
Issued: 2026-10-22
Issue: https://github.com/PyAutoLabs/HowToGalaxy/issues/88

## Original request (verbatim)

"yeah fix it" / "yes do both go"

## Cause (diagnosed 2026-10-22)

PyAutoHands bfb4887 (2026-10-16) added a smoke dependency preflight. At `PYAUTO_TEST_MODE=2` it imports the backend of every search a script constructs. The HowToLens and HowToGalaxy 3.13 smoke legs deliberately install no `[optional]` extras. As a result, `chapter_optional/tutorial_searches.py` (`af.Zeus`) fails with `Zeus requires importable module zeus: No module named 'zeus'`. This was not a cache problem.

autofit_workspace fixed the same failure in 3a23985 (2026-10-21) by adding `pip install zeus-mcmc==2.5.4` to the 3.13 branch of `.github/scripts/smoke_install.sh`. autolens_workspace and autogalaxy_workspace are unaffected: their `smoke_tests.txt` subsets skip their Zeus scripts.

## Fix

- **HowToLens:** committed b63072f on the `point-plots-yaml-keys` branch (PR HowToLens#99), because that task claims HowToLens. This also unblocks #99 and later #100.
- **HowToGalaxy:** the same one-line installer fix, on its own branch and PR (this task).

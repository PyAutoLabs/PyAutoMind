# verify_install Check F: assumes a bundled dataset (no auto-simulate) and resolves a mixed dev/released stack

Type: bug
Target: health_fixes
Repos:
- PyAutoHeart
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

PyAutoHeart's `verify_install` **Check F** driver fails on a missing dataset, so the whole
`verify_install_release` job reports FAIL even though the real new-user install path is
healthy. Surfaced by the 2026-07-13 release-validation Stage-3 run (workspace-validation
`run_id=29266305445`, TestPyPI `2026.7.13.1.dev65501`). Check status was:

```
A  PASS  pip install + start_here.py + welcome.py
C  PASS  conda(python=3.12) + start_here + welcome
D  PASS  autolens[optional]==2026.7.13.1.dev65501 resolved + imports
F  FAIL  driver rc=1
```

Two distinct problems in Check F only:

1. **Missing auto-simulate (primary).** `F_driver.py:36` calls
   `Imaging.from_fits('dataset/imaging/simple/data.fits')` from its CWD, but never simulates
   that dataset first, so it crashes `FileNotFoundError: dataset/imaging/simple/data.fits`.
   Datasets are meant to be auto-simulated at run time, never bundled/committed (only a few
   select example `.fits` ship with a workspace) — this gap was exposed by the 2026-07-13
   release dataset `-f` leak fix (PyAutoBuild#150) that stopped force-adding `dataset/`.
   Check A's `start_here.py` passes because it simulates its own dataset; Check F must do the
   same (run the matching simulator, or simulate to the exact folder it then loads) instead
   of assuming a bundled file. This is a HARNESS gap, not a library defect.

2. **Mixed dev/released stack (secondary).** Check F's env resolved
   `autolens 2026.7.13.1.dev65501` (the rehearsal dev wheel) but its dependencies came from
   released PyPI — `autoarray/autoconf/autofit/autogalaxy 2026.7.9.1` — so Check F is not
   even exercising a coherent dev stack. Pin all five PyAuto packages to the TestPyPI dev
   version (or install with the TestPyPI index for the whole family) so Check F tests the
   same wheels as Checks A/C/D.

Fix both in the Check-F driver, then re-run `verify_install` against a TestPyPI rehearsal
version to confirm F PASS. Keep the core new-user path (A/C/D) untouched — it is green.

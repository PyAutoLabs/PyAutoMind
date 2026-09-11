# EP test suite is not xdist-safe: tests share one on-disk output directory

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: 'python -m pytest test_autofit/graphical -q -n auto' passes with the same count as the serial run (279 on main e331e33, 281 after PyAutoFit#1608).
Review-minutes: 3
Unattended: ready

EP test suite is not xdist-safe: tests share one on-disk output directory
Type: bug
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Priority: medium
Witness: 'python -m pytest test_autofit/graphical -q -n auto' passes with the same count as the serial run (279 on main e331e33, 281 after PyAutoFit#1608).

Measured 2026-09-11 on clean main e331e33: 'python -m pytest test_autofit/graphical -q -n auto' gives 17 failed / 268 passed, while the same suite serial gives 279 passed. Signature: FileNotFoundError on test_autofit/output/<identifier>/mean_field_evolution.png inside PIL Image.save (e.g. test_autofit/graphical/gaussian/test_optimizer.py::test_default; also hierarchical/test_optimise.py::test_optimise, regression/test_linear_regression.py::test_exact_updates and test_laplace, stochastic/test_regression.py::test_stochastic_linear_regression, gaussian/test_optimizer.py::TestDynesty::test_null_paths). Several EP tests write their visualisation output under the same search-identifier path in test_autofit/output/, so one xdist worker's teardown removes the directory another worker is still writing into. The remote-session doctrine says to run suites with -n auto, so this suite silently cannot follow it and PyAutoFit#1608 had to be judged serially.

Fix: give every EP test that writes output its own tmp_path-rooted output directory (a conftest fixture pointing the conf output path at tmp_path, or a unique_tag per test), so the suite is parallel-safe.

Related: draft/bug/autofit/xdist_collection_ids_unstable_in_test_prior.md covers the other xdist breakage (collection-id mismatch in test_prior_properties), a separate cause.

<!-- formalised by the Intake (Conception) Agent on 2026-09-11 from user-intake -->

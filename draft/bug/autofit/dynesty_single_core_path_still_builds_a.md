# Dynesty single-core path still builds a Pool(1) instead of running serially

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Consequence: judge
Witness: a number_of_cores=1 DynestyStatic fit over a use_jax=True analysis completes under PYAUTO_TEST_MODE=1 with fork_context monkeypatched to raise, i.e. without forking.
Review-minutes: 20
Unattended: ready

Dynesty single-core path still builds a Pool(1) instead of running serially
Type: bug
Target: PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Witness: a number_of_cores=1 DynestyStatic fit over a use_jax=True analysis completes under PYAUTO_TEST_MODE=1 with fork_context monkeypatched to raise, i.e. without forking.

Found 2026-09-11 while adding test__ep_single_core_search_unchanged for PyAutoFit#1608: af.DynestyStatic(number_of_cores=1) still enters its own _fork_pool_cls() Pool(1) (autofit/non_linear/search/nest/dynesty/search/abstract.py, the fork-context subclass from PyAutoFit#1439), falling back to serial only if the pool raises RuntimeError. This is the same shape as PyAutoFit#1442/#1443 for Nautilus: a real Pool(1) forces every likelihood call into a forked worker, which deadlocks in XLA compilation when the likelihood touches JAX (a forked child of a JAX-initialised parent cannot compile), and a dead worker is silently replaced with its task never re-issued. Nautilus was fixed to pass pool=None at number_of_cores<=1 (#1443); Dynesty was not.

Fix: at number_of_cores<=1 build no pool at all and run dynesty serially, keeping the fork-context pool for genuine multi-core runs. Regression test mirroring test__single_core_builds_no_pool in test_autofit/non_linear/search/nest/test_nautilus.py (monkeypatch fork_context to raise; a number_of_cores=1 DynestyStatic fit must complete without touching it). The EP single-core test in test_autofit/graphical/test_ep_no_multiprocessing.py can then also use its no_forking fixture.

<!-- formalised by the Intake (Conception) Agent on 2026-09-11 from user-intake -->

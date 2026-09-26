- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1630 (closed completed 2026-09-15)
- completed: 2026-09-15
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1632 (merged `b82fb3f69851ab9a6d68e8b80dd782e42ff48726`)
- branch: `feature/dynesty-single-core-no-pool`, feature commit `b404cd36d2579f8d27061958483a2b7433023226`
- summary: |
    At `number_of_cores <= 1`, DynestyStatic and DynestyDynamic use the existing
    serial branch and build no fork-context pool. Multi-core pool behavior and
    the Windows `RuntimeError` fallback remain unchanged. The docstrings explain
    that a search started single-core cannot resume multi-core because
    `check_pool` raises, as on the existing `force_x1_cpu` path. The EP
    single-core test now uses its `no_forking` fixture.
- validation: |
    The new regression test for both Dynesty samplers was red on unfixed source
    and green after the change. The full PyAutoFit suite passed (2854 passed,
    2 skipped). The autofit workspace smoke passed 10/10, though its test mode 2
    bypasses the sampler; the unit test at test mode 1 exercises the no-pool path.
    PR CI passed Docs and Tests on Python 3.12, 3.13, and nojax; Heart freeze
    was clear before merge. The feature commit is an ancestor of origin/main.
- witness-correction: |
    The filed `use_jax=True` witness already ran serial on main. The effective
    witness used a plain analysis at one core with `fork_context` patched to
    raise. This correction was recorded on the issue.
- parallel-claim: |
    `howtofit-mode` also claimed PyAutoFit, but its branch had zero diff versus
    main and touched README prose only. This task used its own worktree after
    the approved plan.

## Original prompt

# Dynesty single-core path still builds a Pool(1) instead of running serially

Type: bug
Target: PyAutoFit
Repos:
- PyAutoFit
Difficulty: small
Autonomy: supervised
Priority: medium
Status: formalised
Issued: 2026-09-15
Issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1630
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

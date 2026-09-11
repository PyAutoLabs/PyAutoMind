# Remove ParallelEPOptimiser and its tests

Type: refactor
Target: PyAutoFit
Repos:
- PyAutoFit
- PyAutoMemory
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: 'grep -rn ParallelEPOptimiser autofit test_autofit docs' returns nothing; test_autofit/graphical passes serially with the same count minus any removed tests; no public export changes (the class was never exported from autofit, autofit.graphical or the EP package).
Review-minutes: 3
Unattended: ready

Remove ParallelEPOptimiser and its tests
Type: refactor
Target: PyAutoFit
Difficulty: small
Autonomy: safe
Priority: medium
Witness: 'grep -rn ParallelEPOptimiser autofit test_autofit docs' returns nothing; test_autofit/graphical passes serially with the same count minus any removed tests; no public export changes (the class was never exported from autofit, autofit.graphical or the EP package).

Human decision 2026-09-11 (after PyAutoFit#1608 / PR #1610): ParallelEPOptimiser has never been used, adds complexity, and if it ever had a use it can be re-added from git history. It is dead code already: not exported from any __init__ (reachable only by deep import), its only test helper _test_parallel_laplace in test_autofit/graphical/regression/test_linear_regression.py is underscore-prefixed and never collected, and PyAutoMemory records it crashing at completion when paths=None (#1332 F3). It is EP's own opt-in process pool across factors (fork_context().Pool(n_cores-1) + starmap(factor_step, ...)), which shares the dead-worker hang fixed for Nautilus in #1610 and the JAX-in-a-forked-child deadlock of #1442; the ruling of 2026-09-09 is that EP never combines with Python multiprocessing, so the class contradicts the ruling by existing.

Scope (one PR): delete class ParallelEPOptimiser from autofit/graphical/expectation_propagation/optimiser.py (~lines 666-830, including the docstring note #1610 added) and the now-unused fork_context import if nothing else in the module uses it; delete _test_parallel_laplace from test_autofit/graphical/regression/test_linear_regression.py and its import; rewrite the F3 comments in test_autofit/graphical/functionality/test_diagnostics.py (~lines 178-202) that reference ParallelEPOptimiser so they describe EPOptimiser.run only; remove README section '7. Parallel EP' from autofit/graphical/README.md and renumber section 8 (the lowering contract) to 7, fixing any '§7'/'§8' cross-references in the README and in test_autofit/graphical (the EP seam rule in AGENTS.md names §8); grep docs/ for the name. Record the removal in the PR's API Changes as Removed (internal, never exported). Also update the PyAutoMemory line in wiki/methods/concepts/expectation-propagation.md that describes ParallelEPOptimiser (#1332 F3) to say it was removed in this PR — that is a separate PyAutoMemory commit, ledger-style.

<!-- formalised by the Intake (Conception) Agent on 2026-09-11 from user-intake -->

# bfgs-checkpoint-resume

- completed: 2026-10-25
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1724
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1731
- head: 05cc77c3ba49e070b321a93f591b0908f0d1cec1
- merge-commit: be4d8bb3497d1644589cdec28d37b3dac2dcfed6
- authorization: human "Yes I authorise" for development after disclosed RED; subsequent human "Prm" for merge and closeout. No release authorized or performed.

## Outcome and validation

Full library suite: 3919 passed, 1 skipped, 1 xfailed (Python 3.12.14). Broader search/conformance/clipper tests: 201 passed. Six new regressions pass for real interrupted BFGS/LBFGS fits, legacy checkpoint counts, and exhausted budgets; all six fail on unchanged main. Author diff review passed. Real scipy fits resume at the saved point and match uninterrupted runs.

Every workflow and job at the published head passed, including Python 3.12, Python 3.13 and no-JAX, plus docs where applicable. Freeze clear. Source and output identifier logic unchanged during PRM. Author review only; no independent adversary claimed. Published head is an ancestor of origin/main. Local authored commit has an identical tree to the API-published head (different commit metadata); no implementation changes between shipping and merge.

## Closeout

Issue closed as completed. Lifecycle close folds the original prompt, removes the active claim and refreshes the index. Dashboard regenerated with the records. Pending-release key repaired from the verified GitHub label before closeout and carried forward. All four worktrees and their local feature branches removed after verifying identical published trees and merged ancestry. Stage-1 shadow row appended from observed unchanged heads; count after the four closeouts: 53/20. Mind ledger branch will land through the repository ledger automation.

Original Heart RED disclosure retained (not cleared by this task): install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty.

## Original prompt

# `@PyAutoFit` BFGS/LBFGS resume reads `["x0"]` from the saved scipy result and cannot resume an interrupted run

Issued: 2026-10-25
Type: bug
Target: autofit
Repos:
- PyAutoFit
Difficulty: low
Autonomy: safe
Priority: normal
Status: active
Consequence: glance
Witness: an Emcee-style interrupt/resume test for BFGS and LBFGS (run with a small `maxiter`, kill after the first checkpoint, re-run the same `search.fit`) completes without `KeyError` and reaches the same optimum as an uninterrupted run; a resume with `total_iterations >= maxiter` leaves `search_internal` populated so `Samples` build.
Filed: 2026-10-14

Found by the A5 library worker (PyAutoFit#1689–#1692) and verified identical on main df6d218f1, so it is not an A5 regression and was deliberately left unchanged there. `autofit/non_linear/search/optimize/bfgs/search.py` resumes by reading `["x0"]` from its dill-saved scipy `OptimizeResult`, which has no such key, so every resume of an interrupted BFGS/LBFGS run raises `KeyError: 'x0'`. Separately, when the saved `total_iterations` already meets `maxiter`, the resume path skips the optimiser and never sets `search_internal`, so samples cannot be built. Fix on top of the A5 `run(ctx)` version of the search (after #1692 merges); keep Zeus/BFGS's own dill save/resume (A5 decision 2) rather than introducing `resume_state`.

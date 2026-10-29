# emcee-jax-dispatch-guard

- completed: 2026-10-25
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1727
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1729
- head: ffa70b0d9712e2796ee841b5806d9f9b69179936
- merge-commit: 8cb533a605f556d85012d5eb7ed8d4f3c2a4dcf6
- authorization: human "Yes I authorise" for development after disclosed RED; subsequent human "Prm" for merge and closeout. No release authorized or performed.

## Outcome and validation

Focused JAX dispatch tests: 3 passed, 1 skipped (opt-in profiling). Full library suite: 3912 passed, 2 skipped, 1 xfailed, with one /tmp/summary.csv collision from concurrently running isolated checkouts (the existing fixture hardcodes that global filename). Re-ran the entire affected aggregate-CSV module alone: 17 passed. No remaining failing tests. Python 3.12.14. Author diff review passed. No production changes.

Every workflow and job at the published head passed, including Python 3.12, Python 3.13 and no-JAX, plus docs where applicable. Freeze clear. Source and output identifier logic unchanged during PRM. Author review only; no independent adversary claimed. Published head is an ancestor of origin/main. Local authored commit has an identical tree to the API-published head (different commit metadata); no implementation changes between shipping and merge.

## Closeout

Issue closed as completed. Lifecycle close folds the original prompt, removes the active claim and refreshes the index. Dashboard regenerated with the records. Pending-release key repaired from the verified GitHub label before closeout and carried forward. All four worktrees and their local feature branches removed after verifying identical published trees and merged ancestry. Stage-1 shadow row appended from observed unchanged heads; count after the four closeouts: 53/20. Mind ledger branch will land through the repository ledger automation.

Original Heart RED disclosure retained (not cleared by this task): install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty.

## Original prompt

# `@PyAutoFit` `test_emcee_call_path_runs_at_jitted_speed` is a wall-clock ratio assertion that flakes on shared CI runners

Issued: 2026-10-25
Type: test
Target: autofit
Repos:
- PyAutoFit
Difficulty: trivial
Autonomy: safe
Priority: normal
Status: active
Consequence: glance
Witness: the test no longer asserts a wall-clock ratio between the wrapped call path and the raw jitted function on CI; it asserts structurally that the Emcee call path dispatches to the compiled objective (e.g. the wrapper calls the jitted callable exactly once per evaluation with no Python-side re-tracing), with the timing comparison kept only under an opt-in env flag for local profiling.
Filed: 2026-10-14

`test_autofit/non_linear/search/mcmc/test_emcee_jax_timing.py::test_emcee_call_path_runs_at_jitted_speed` failed on PyAutoFit main df6d218f1 (run 38577574188, `unittest (3.12)` only: "call_wrap 0.116 ms vs jit 0.055 ms") while the same code passed on #1687's PR CI and on the previous main run 5bf057f28; `gh run rerun --failed` on the same run went green. A failure on main turns Heart RED and stops every `--auto` ship gate (it parked B4b on 2026-10-14). Sub-millisecond ratio assertions cannot be stable on shared runners; replace with a structural assertion.

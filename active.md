
## likelihood-lifecycle-p2a-imaging-campaign
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/456
- issued: 2026-10-24
- session: claude-code (local CLI, Opus 5.5)
- status: workspace-dev
- worktree: ~/Code/PyAutoLabs-wt/likelihood-lifecycle-p2a-imaging-campaign
- prompt: active/likelihood_lifecycle_p2a_imaging_campaign.md
- epic: likelihood-lifecycle
- merged: https://github.com/PyAutoLabs/autolens_profiling/pull/457 (PR A: standard-size production cells + parity.json + submits; review CLEAN after 3 rounds)
- next: 2026-10-25 BATCH 0 COMPLETE: 32/34 legs (reruns 412911/412915 clean; 2 ao jax_gpu_dense breakdowns = A100 OOM limitation, human ruling; rect ao one found on rerun). #459 guard-test MERGED 510b9556. Batch-1 walls PR #460 OPEN (ac566251+931b11be; RAL arrays 1h, mem ao 64 / others 32; A100 3h, hst 3.5h). NEXT: human /prm 460 → ff private RAL checkout /mnt/ral/jnightin/profiling/autolens_profiling_p2a (nohup; slow FS) → HUMAN GO → submit 4 RAL arrays (hpc/batch_cpu/submit_campaign_p2a_imaging_ral_cpu_<inst>_fp64) + 4 A100 jobs (hpc/batch_gpu/submit_campaign_p2a_imaging_a100_<inst>_fp64) → PR B.
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/458 (MERGED 7679f564; p2a breakdown fixes, branch feature/likelihood-lifecycle-p2a-breakdown-fixes)
- workspace-pr: autolens_profiling https://github.com/PyAutoLabs/autolens_profiling/pull/460 (batch-1 measured walls)
- repos:
  - autolens_profiling: feature/likelihood-lifecycle-p2a-imaging-campaign

## matrix-free-interferometer-inversion
- issue: https://github.com/PyAutoLabs/PyAutoArray/issues/638
- issued: 2026-10-21
- user-facing: true
- community: https://github.com/PyAutoLabs/.github/discussions/39 (@HRSAstro)
- prompt: active/matrix_free_interferometer_inversion.md

## bfgs-checkpoint-resume
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1724
- issued: 2026-10-25
- session: ChatGPT Work; session ID unavailable
- status: library-shipped, awaiting-merge
- prompt: active/bfgs_resume_reads_x0_from_scipy_result.md
- worktree: /workspace/scratch/31f19494df78-wt/bfgs-checkpoint-resume
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: Full library suite: 3919 passed, 1 skipped, 1 xfailed (Python 3.12.14). Broader search/conformance/clipper tests: 201 passed. Six new regressions pass for real interrupted BFGS/LBFGS fits, legacy checkpoint counts, and exhausted budgets; all six fail on unchanged main. Author diff review passed. Real scipy fits resume at the saved point and match uninterrupted runs.
- repos:
  - PyAutoFit: feature/bfgs-checkpoint-resume
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1731
- next: required CI and human /prm; no merge or release authorized
- head: 05cc77c3ba49e070b321a93f591b0908f0d1cec1

## mcmc-short-chain-guards
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1725
- issued: 2026-10-25
- session: ChatGPT Work; session ID unavailable
- status: library-shipped, awaiting-merge
- prompt: active/mcmc_thin_zero_and_check_size_short_chain.md
- worktree: /workspace/scratch/31f19494df78-wt/mcmc-short-chain-guards
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: Full library suite: 3922 passed, 1 skipped, 1 xfailed (Python 3.12.14). Focused MCMC tests: 14 passed, including real Emcee/Zeus reduced fits with default check_size=100. Additional real Emcee smoke: 10 walkers, 50 steps, test mode disabled, samples built and previous_times=None. Six new regression cases fail on unchanged main (zero thin and empty previous chain), while ordinary thinning remains unchanged. Author diff review passed.
- repos:
  - PyAutoFit: feature/mcmc-short-chain-guards
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1730
- next: required CI and human /prm; no merge or release authorized
- head: 6830c2ee1b1df53dcce96784186c1cd04f31d535

## ep-test-output-isolation
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1726
- issued: 2026-10-25
- session: ChatGPT Work; session ID unavailable
- status: library-shipped, awaiting-merge
- prompt: active/ep_test_suite_is_not_xdist_safe.md
- worktree: /workspace/scratch/31f19494df78-wt/ep-test-output-isolation
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: Full library suite: 3913 passed, 1 skipped, 1 xfailed. Graphical suite: 329 passed serially and 329 passed with four xdist workers; unchanged main reproduced 13 failures / 316 passed under xdist. Python 3.12.14. Author diff review passed; production code and output identifier generation untouched.
- repos:
  - PyAutoFit: feature/ep-test-output-isolation
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1728
- next: required CI and human /prm; no merge or release authorized
- head: 775e41c81f254d513068241d0715039912d67f87

## emcee-jax-dispatch-guard
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1727
- issued: 2026-10-25
- session: ChatGPT Work; session ID unavailable
- status: library-shipped, awaiting-merge
- prompt: active/emcee_jax_timing_test_flaky_on_ci.md
- worktree: /workspace/scratch/31f19494df78-wt/emcee-jax-dispatch-guard
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: Focused JAX dispatch tests: 3 passed, 1 skipped (opt-in profiling). Full library suite: 3912 passed, 2 skipped, 1 xfailed, with one /tmp/summary.csv collision from concurrently running isolated checkouts (the existing fixture hardcodes that global filename). Re-ran the entire affected aggregate-CSV module alone: 17 passed. No remaining failing tests. Python 3.12.14. Author diff review passed. No production changes.
- repos:
  - PyAutoFit: feature/emcee-jax-dispatch-guard
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1729
- next: required CI and human /prm; no merge or release authorized
- head: ffa70b0d9712e2796ee841b5806d9f9b69179936

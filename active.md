
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
- status: library-dev
- prompt: active/bfgs_resume_reads_x0_from_scipy_result.md
- worktree: /workspace/scratch/31f19494df78-wt/bfgs-checkpoint-resume
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: pending; will record measured tests at PR-open
- repos:
  - PyAutoFit: feature/bfgs-checkpoint-resume

## mcmc-short-chain-guards
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1725
- issued: 2026-10-25
- session: ChatGPT Work; session ID unavailable
- status: library-dev
- prompt: active/mcmc_thin_zero_and_check_size_short_chain.md
- worktree: /workspace/scratch/31f19494df78-wt/mcmc-short-chain-guards
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: pending; will record measured tests at PR-open
- repos:
  - PyAutoFit: feature/mcmc-short-chain-guards

## ep-test-output-isolation
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1726
- issued: 2026-10-25
- session: ChatGPT Work; session ID unavailable
- status: library-dev
- prompt: active/ep_test_suite_is_not_xdist_safe.md
- worktree: /workspace/scratch/31f19494df78-wt/ep-test-output-isolation
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: pending; will record measured tests at PR-open
- repos:
  - PyAutoFit: feature/ep-test-output-isolation

## emcee-jax-dispatch-guard
- issue: https://github.com/PyAutoLabs/PyAutoFit/issues/1727
- issued: 2026-10-25
- session: ChatGPT Work; session ID unavailable
- status: library-dev
- prompt: active/emcee_jax_timing_test_flaky_on_ci.md
- worktree: /workspace/scratch/31f19494df78-wt/emcee-jax-dispatch-guard
- coordination: user requested four grouped tasks; isolated branches, sequential implementation in this session
- heart-red-override:
  - authorization: "Yes I authorise" after disclosed RED reasons; development and PR-open only; no merge/release
  - reasons: install verification FAILED (testpypi; checks F); release validation FAILED (stage integrate); PyAutoHeart/workflows/Release Integrate: failure; manifest_drift/checks/workspace checkouts (manifest ↔ disk): red; Release readiness: release validation FAILED (stage integrate); Release readiness: install verification FAILED (testpypi; checks F); PyAutoArray/test_autoarray/inversion/inversion/interferometer/test_interferometer.py::test__interferometer_sparse_operator__mapped_reconstructed_data_dict_matc…; Unit-test timing: 1 test regressions (>3× baseline), 11 slow (>1.5×); Release validation: NOT release_ready — v2026.10.25.1.dev83701 profile=release (2026-10-25T07:21:05+00:00); validation_report/stages/integrate: fail; verify_install FAILED: verify_install FAILED; F: colab gate: finufft (declared by autoarray, absent on Colab, imported); Install verification: FAILED (testpypi; F) (2026-10-25T07:42:48.134987+00:00); verify_install: red; PyAutoBrain: red; PyAutoLens: red; autolens_profiling: red; Worktree drift: 1 orphan / 0 missing / 3 dirty
  - validation: pending; will record measured tests at PR-open
- repos:
  - PyAutoFit: feature/emcee-jax-dispatch-guard

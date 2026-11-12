## Outcome (phase 1 shipped; phase 2 re-filed)

Removed the `--xla_cpu_multi_thread_eigen=false` workarounds for the jax>=0.12 floor
(PyAutoNerves#215). Merged 2026-11-12: PyAutoHeart#336 (7cfaf6c),
autolens_workspace_test#365 (75e3069), autogalaxy_workspace_test#136 (d76b9d4).

- Workspaces: smoke/release profiles set `XLA_FLAGS: ""`, explicitly empty because the
  runner never clears inherited keys; autonerves still appends its defaults.
- Heart: the release-mode validation leg and the jax-compatibility job no longer set
  it. The FFT witness passed BARE on jax 0.12.0 and 0.12.0.1. Kept:
  release-diagnostic.yml's flag arm (0.10.2 incident replay) and the autolens_profiling
  research matrix arm.
- Evidence: PR smoke on jax 0.12.0.1 without the flag (alwt 39 / agwt 43 scripts, 0
  failures); a no-flag release-fidelity integrate on the 2026.11.12.1 candidate wheels
  (PyAutoHeart run 43238247828) gave 818 pass / 0 fail / 0 timeout, identical to the
  flagged run 43210505844. CI wall time did NOT show a speed-up (46 jobs: 248 -> 262
  min, +6 %, mixed per job). Shared runners and setup/compile dominate, so this is
  inconclusive about the per-call cost; the controlled per-call numbers are in PyAutoDNA
  decisions/jax-cpu-policy-2026-11.md.
- The only integrate red was verify_install check F (Colab), a separate regression:
  draft/bug/autonerves/colab_restart_only_when_upgraded_module_imported.md.

Not done: phase 2 re-filed as
draft/maintenance/autolens_profiling/remove_d12_eigen_flag_after_remeasure.md (deferred by
the human until the autolens_profiling claims are released). Private RAL job scripts are
the human's to update.

## Original prompt

# Remove the per-place --xla_cpu_multi_thread_eigen=false workarounds once the jax 0.12 floor is released

Type: maintenance
Target: workspaces
Repos:
- autolens_workspace_test
- autogalaxy_workspace_test
- PyAutoHeart
- autolens_profiling
Priority: low
Consequence: glance
Issued: 2026-11-12

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## Why
On jax 0.12 no reproducer needs the flag, and it slows pixelized likelihoods by 18-50 % per call (RAL 415009), so carrying it costs CI and release-validation time.

## What
After the PyAutoNerves floor jax>=0.12.0 is RELEASED: re-check each site on 0.12, then drop the flag from the test-workspace smoke/release profiles (PyAutoFit#1528), PyAutoHeart workspace-validation release mode / release-diagnostic / jax-compatibility (ad9bbc4, keep its test meaningful), autolens_profiling galaxy_group_standard.py XLA_CPU_WORKAROUND_FLAG (D12; new rows record no flag, so note the like-for-like break in Pulse), and private RAL job scripts. Un-quarantine the multi_dataset/jax_likelihood scripts if they pass.

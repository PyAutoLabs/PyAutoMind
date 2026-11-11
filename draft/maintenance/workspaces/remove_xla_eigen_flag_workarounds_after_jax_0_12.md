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

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## Why
On jax 0.12 no reproducer needs the flag, and it slows pixelized likelihoods by 18-50 % per call (RAL 415009), so carrying it costs CI and release-validation time.

## What
After the PyAutoNerves floor jax>=0.12.0 is RELEASED: re-check each site on 0.12, then drop the flag from the test-workspace smoke/release profiles (PyAutoFit#1528), PyAutoHeart workspace-validation release mode / release-diagnostic / jax-compatibility (ad9bbc4, keep its test meaningful), autolens_profiling galaxy_group_standard.py XLA_CPU_WORKAROUND_FLAG (D12; new rows record no flag, so note the like-for-like break in Pulse), and private RAL job scripts. Un-quarantine the multi_dataset/jax_likelihood scripts if they pass.

# Point Pulse's XLA:CPU deadlock notes at the DNA JAX CPU policy

PyAutoPulse#95, merged as PyAutoLabs/PyAutoPulse#96 (c96fdad8) on 2026-11-11. Tier notify (auto-merge on
green after the human acknowledged Heart YELLOW). Follow-up of jax-version-policy (PyAutoNerves#213).

- knowledge/xla_cpu_deadlock_jaxlib_0_11_2.md: policy banner → PyAutoDNA decisions/jax-cpu-policy-2026-11.md;
  RAL question answered (0.11.2 no flag: 25/25 hang at 4 cores, 0/25 at 16); re-test answered (0.12 clean,
  eigen flag +18-50 % on pixelized at 0.12). Timing-row guidance unchanged.
- decisions/xla-cpu-deadlock-eigen-workaround.md (D12): dated status update; scope unchanged, revisit test
  done, flag removal queued (draft/maintenance/workspaces/remove_xla_eigen_flag_workarounds_after_jax_0_12.md).
- tasks/pair_jax_xla_env_vars_with_measured.md: policy is DNA's; row pairing stays Pulse's.

## Original prompt

# Point PyAutoPulse's XLA:CPU deadlock knowledge and D12 decision at the DNA JAX CPU policy

Type: docs
Target: PyAutoPulse
Repos:
- PyAutoPulse
Priority: low
Consequence: notify
Issued: 2026-11-11

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## What
Human 2026-11-10: JAX version / environment-variable policy belongs to PyAutoDNA, not Pulse. Add a short "Superseded for policy by PyAutoDNA decisions/jax-cpu-policy-2026-11.md" note to knowledge/xla_cpu_deadlock_jaxlib_0_11_2.md and decisions/xla-cpu-deadlock-eigen-workaround.md, answering their open questions (RAL without the flag: hangs at 4 cores, not at 16; re-test on a jax upgrade: done, 0.12 clean). Keep the timing-row guidance (flagged rows are not like-for-like) in Pulse.

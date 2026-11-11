# Point PyAutoPulse's XLA:CPU deadlock knowledge and D12 decision at the DNA JAX CPU policy

Type: docs
Target: PyAutoPulse
Repos:
- PyAutoPulse
Priority: low
Consequence: notify

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## What
Human 2026-11-10: JAX version / environment-variable policy belongs to PyAutoDNA, not Pulse. Add a short "Superseded for policy by PyAutoDNA decisions/jax-cpu-policy-2026-11.md" note to knowledge/xla_cpu_deadlock_jaxlib_0_11_2.md and decisions/xla-cpu-deadlock-eigen-workaround.md, answering their open questions (RAL without the flag: hangs at 4 cores, not at 16; re-test on a jax upgrade: done, 0.12 clean). Keep the timing-row guidance (flagged rows are not like-for-like) in Pulse.

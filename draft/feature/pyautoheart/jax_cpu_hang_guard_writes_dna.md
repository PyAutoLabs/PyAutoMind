# Heart guard: run the XLA:CPU hang reproducers on every allowed jax version and write DNA records

Type: feature
Target: PyAutoHeart
Repos:
- PyAutoHeart
- PyAutoDNA
- autolens_profiling
Priority: medium
Consequence: glance

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## Why
The deadlock recurred five times because test-mode smokes never call a compiled likelihood enough times, and the 0.11.2 hang is invisible on big nodes (16 cores: 0/25) but certain at 4 cores (25/25).

## What
A scheduled Heart check: for each jax version the PyAutoNerves requirement allows, run autolens_profiling scripts/misc/jax_version_policy (hang_case.py on the exported modules + fft) for 300 calls pinned to 4 cores, then `dna import-matrix` the rows as PyAutoHeart (or PyAutoDNA research) validation records so the DNA board's JAX CPU policy panel and its yellow "hanging setup" item stay current. Exported modules must be re-exported with the oldest allowed jax (0.9.2 could not read 0.11.2 exports).

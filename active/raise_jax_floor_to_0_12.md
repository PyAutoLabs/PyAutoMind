# Raise the JAX floor to 0.12.0 (jax and jaxlib) after a Heart validation

Type: feature
Target: PyAutoNerves
Repos:
- PyAutoNerves
- PyAutoHeart
Priority: high
Consequence: judge
Issued: 2026-11-11

Source: research PyAutoNerves#213 (decision PyAutoDNA decisions/jax-cpu-policy-2026-11.md, evidence RAL 415009 + laptop pilot, DNA research records). Filed 2026-11-10/11 from the research close-out; needs /intake to formalise.

## Why
jax/jaxlib 0.11.2 (today's resolved version and "recommended baseline") deadlocks XLA:CPU likelihoods: on RAL at 4 cores every reproducer hung on the first call (25/25 cells), intermittent at 8 cores, none at 16. jax 0.12.0 and 0.12.0.1 passed 100/100 cells per setting (0 hangs in 30,000 calls) with no flag. The FFT-pool part is upstream jax#41265, fixed by openxla/xla#50091 in 0.12.0.

## What
1. Heart validation on jax 0.12 first: full library unit suites + workspace smoke on CPU and GPU (CUDA 12/13 plugins), including blackjax, optax, nufftax, jaxnnls; rerun autolens_workspace_test multi_dataset/jax_likelihood/delaunay_mge.py, delaunay.py, shared_preloads.py, rectangular.py (all hung in release-integrate on 0.11.2, delaunay_mge even with the eigen flag).
2. PyAutoNerves pyproject: `jax>=0.12.0,<0.13` AND `jaxlib>=0.12.0,<0.13` (both: jax 0.12.0 accepts jaxlib 0.11.2), replacing the 0.7 floor and the 0.10.*/0.11.0 exclusions; README "JAX compatibility" + "recommended baseline" updated. numpy floor becomes 2.2; x86-64 needs Haswell+.
3. Do NOT add a default XLA:CPU flag: the eigen flag costs +18-50 % per call on pixelized likelihoods on 0.12.

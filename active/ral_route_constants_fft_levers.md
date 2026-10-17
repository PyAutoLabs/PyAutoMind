# RAL route-gate constants and A100 FFT size levers (interferometer)

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoArray (only if part A yields an implementable change; stacked on PyAutoArray#636)
Themes:
- interferometer
- likelihood-profiling
- jax-gpu
Difficulty: medium
Autonomy: supervised
Consequence: judge
Epic: interferometer-likelihood-campaign
Filed: 2026-10-17
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/429

Campaign: PyAutoPulse#62 (tasks `interferometer_large_mask_aris` and
`interferometer_w_tilde_fft_size_levers`, the latter's original prompt below its separator).
Human authorisation (2026-10-17, to the architect session): "Do all that, I authorise all" — RAL
A100 and CPU compute for this phase and the development flow to record it. Merge stays human.

## Request (from the architect, verbatim scope)

A. Cost-model constants on RAL (CPU). Measure `t_fft` and `t_dc` arms on euclid-ral-compute-1-class
nodes (`--partition=ral --exclusive`, serial numba, 2026.10.17.1 stack + the #636 patch in a private
checkout). Fit per-host constants from the measured arms on both Aris masks (125 and 512) across the
available vertex counts, keep κ as shipped unless the data contradicts it, and report predicted vs
measured for every cell, in-sample vs out-of-sample marked. Then propose: (i) keep laptop
constants, (ii) replace with RAL constants, or (iii) make the constants a settings/config override
with documented per-host values. Implement ONLY if one option is clearly supported by the data and
stays inside the existing cost-model design; otherwise record the evidence and the open choice.

B. A100 FFT size levers (measurement only, no library change). The witness the Pulse task defines:
pruned padded FFT vs library F at alma / alma_high / jvla with max rel diff and the figure-of-merit
shift, and the real-space pixel-scale row at jvla (0.01 / 0.015 / 0.02 / 0.025″) with log-evidence
shift vs 0.01″. Compile separate from execution; fp64; host, GPU, driver/JAX versions, dataset, SHAs.

## Summary
A100 W~ FFT size-levers witness (autolens_profiling#433, issue #429; RAL job 412515 on euclid-ral-gpu-1, `--gres=gpu:1 --exclusive`, A100 80GB PCIe, jax/jaxlib 0.10.2, nufftax 0.6.1, fp64; private 2026.10.17.1 stack: Nerves 7f3055b7, Fit 4b183e22, Array e59d5fa9, Galaxy 35100def, Lens c90eceb0; compile timed separately; A-B-B-A medians within 0.3 %).

- Pruned padded FFT vs library F (Delaunay-1500, batch 128): alma 140² 17.97→14.49 ms (19.4 %, whole-likelihood 1.08×); alma_high 280² 65.45→50.96 ms (22.1 %, 1.18×); jvla 700² 499.6→351.2 ms (29.7 %, 1.41×). F max rel diff ≤1.7e-15, figure-of-merit shift 0. jvla clears the task's 10 %-of-F bar for a library change.
- Real-space pixel scale at jvla (mask 3.5″): 0.015″/0.02″/0.025″ shift the log evidence by +1,310/+1,807/+2,757 nats vs 0.01″ — every coarser scale fails the 0.5-nat bar (source mesh rebuilt per scale, so the shift mixes pixel scale with mesh change). No docs prompt filed.
- Part A (RAL CPU route-constant refit) was dropped before any CPU job ran: the human closed the interferometer CPU lane on 2026-10-17. Evidence already in hand recorded as a deferred note: RAL FFT/full direct_conv 0.68 measured vs 0.89 predicted by the laptop-calibrated PyAutoArray#632 constants; the 1,459-vertex Aris cell routes to direct_conv at ~1.02× over FFT.

**Human decision 2026-10-17 (Pulse chat):** interferometer GPU levers filed as wiki research, no source changes for now; the JAX `apply_operator` FFT-pruning prompt is NOT filed. Pulse task `interferometer_w_tilde_fft_size_levers` parked (PyAutoPulse#67). Issue/PR titles still name the dropped route constants.

Files: `scripts/interferometer/delaunay/fft_size_levers.py`, `hpc/batch_gpu/submit_fft_size_levers_interferometer_a100_fp64`, `results/breakdown/interferometer/jvla/delaunay_hpc_a100_fp64_fft_prune.json`, `results/notes/interferometer_w_tilde_fft_size_levers_2026_10.md`, journal in `wiki/campaigns/interferometer_likelihood.md`. Merged under human `/prm` after main merge + regeneration (head 14e275c0). Heart STALE at ship, no override. RAL scratch owed cleanup: `/mnt/ral/jnightin/scratch/fft_levers_*`, `fft_levers_stack.tgz`, `fft_levers_jobs/`, `fft_levers_results/`.

## Original prompt

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

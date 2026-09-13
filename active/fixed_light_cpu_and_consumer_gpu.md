# Fixed lens light — the same profiling on CPU and on the laptop RTX 2060 consumer GPU

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- pixelization
- hpc-gpu
Difficulty: large
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Witness: results/notes per-hardware table (A100 / CPU / RTX 2060 fp64 / RTX 2060 fp32-mp) carrying the same S0-PDIP / S3-PDIP / S3-certified / S3-unconstrained rows as phase 1, plus the fp32 evidence deltas
Review-minutes: 20
Unattended: ready
Epic: fixed-lens-light-profiling
Phase: 2
Filed: 2026-09-13
Issued: 2026-09-13

Phase 2 of the `fixed-lens-light-profiling` epic. Gated on phase 1 landing its
library-path rows — "one step at a time".

## Why

Phase 0 (#248) and phase 1 measured the fixed-lens-light likelihood only on the RAL A100.
The human's point is that as the solution converges it has to be optimised for the
hardware most users actually own: a CPU, and a consumer GPU. A certified active-set that
wins on an A100 may lose on a GeForce card, where fp64 runs at 1/32 rate, or on a CPU
where a masked full-size Cholesky per pass is a different cost entirely.

## What to do

Run the same cell and the same rows as phase 1 on:

**(a) CPU, with CPU-appropriate methods** — numpy/scipy `cho_factor`/`cho_solve` for the
unconstrained and certified passes, scipy NNLS or the library's own CPU NNLS path for the
positivity reference, JAX-CPU for the jit/library rows. Record the thread count used for
every timing.

**(b) The laptop RTX 2060 (6 GB)** through the existing `PyAutoGPU` venv at
`/home/jammy/venv/PyAutoGPU` (JAX 0.10.2 + jax-cuda12-plugin). Traps: the session shell
exports `JAX_PLATFORMS=cpu` and `JAX_PLATFORM_NAME=cpu`, which MUST be unset; set
`XLA_PYTHON_CLIENT_PREALLOCATE=false` (only 6 GB). GeForce fp64 runs at 1/32 rate, so run
**both** an fp64 leg and an fp32 / mixed-precision leg and report the evidence delta the
lower precision costs.

Pins (pass budgets, tolerances, seed zero sets) must be **re-derived per precision** —
a pin calibrated in fp64 is not a pin in fp32.

Rows, meshes and dataset as phase 1 (HST; rect / delaunay / delaunay_nn; single + vmap16),
so the phase-1 A100 table and this one stack into one per-hardware comparison.

Cell `@autolens_profiling/scripts/imaging/likelihood_breakdown/fixed_light.py`; kernels
`@autolens_profiling/scripts/misc/likelihood_breakdown/active_set_steps.py`.

Out of scope for the whole epic: the sparse operator and JWST. Dense inversion only.
## Original request (2026-09-13, verbatim — the epic request)

"Ok these are the takss to now queue up: 1) Perform profiling of positive-negative solver for completeness albeit S3 certified
active-set seems like the lead forward; 2) Perform the same profiling on CPU (using CPU appropriate methods) and on m laptop GPU as
its important now we are converging on a solutiopn we also optimizze for consumer GPUs; 3) Confirm that S3 certified active-set is
ver fast on solutions which give low likelihoods, as maybe the fast run times here are a result of the model being good and giving
high likelihoods or an easier to solve solution; 4) Provide profiling information over number of source pixels with the new approach
on difernet hardware 5) For all hardware types and likelihood variants (e.g. sparse operator) give an assessment of the overall
likelihood function on JWST (0.03" pixel scale), HST and Euclid data for 500, 1250 and 2500 source pixels. For each take one step
at a time, and try do it all in --auto."

Clarification (same day): "For positive-negative I want you to use a positive negative solve (e..g. np.linalg.solve) but DO NOT include the
MGE in the matrices or solution, so it sould use normal light porfiles which subtract the MGE beforehand. PyAutoGPU is avirtual
enviroment which already exists on this laptop for running GPU JAX so use that. Rest of plan sonds good. Only use HST and Euclid
for now, drop JWST. Skip the sparse operator for now."

<!-- formalised by the Intake (Conception) Agent on 2026-09-13 from the fixed-lens-light-profiling epic brief -->

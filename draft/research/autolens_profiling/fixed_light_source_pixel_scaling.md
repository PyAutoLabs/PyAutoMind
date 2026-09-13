# Fixed lens light — source-pixel scaling of the new approach across hardware

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
Witness: results/notes ms-versus-N table and figure per hardware (A100 / CPU / RTX 2060) for S3-certified, S3-unconstrained and S3-PDIP, rect and Delaunay
Review-minutes: 20
Unattended: needs-slicing
Epic: fixed-lens-light-profiling
Phase: 4
Filed: 2026-09-13

Phase 4 of the `fixed-lens-light-profiling` epic. Gated on phase 3 — "one step at a time".

## Why

Every fixed-lens-light number so far is at one source-pixel count. The choice that actually
sets production cost is how many source pixels a fit can afford, and the three solvers scale
differently: the unconstrained Cholesky is one factorisation, the certified active-set is a
masked full-size Cholesky per pass (so it multiplies by pass count), and PDIP is an iteration
count times a solve. Whether the certified route stays the lead at 4000 pixels — on an A100,
on a CPU and on a 6 GB consumer GPU — is unmeasured, and phase 5's assessment grid depends on
the answer.

## What to do

Sweep source pixels — e.g. 500, 1000, 1500, 2500, 4000 — for the new approach:
S3 certified active-set, S3 unconstrained, and S3 PDIP as the reference row.

Hardware: A100 (RAL gpu-2, fp64), CPU (CPU-appropriate methods and thread count from phase 2)
and the laptop RTX 2060 through the `PyAutoGPU` venv (fp64 and fp32/mp legs; prealloc off;
`JAX_PLATFORMS` / `JAX_PLATFORM_NAME` unset). Meshes rect and Delaunay, HST dataset.

Record where each hardware runs out of memory as well as where it runs out of speed — the
2060's 6 GB is a real ceiling in this sweep, and a leg that does not fit is a result.

Cell `@autolens_profiling/scripts/imaging/likelihood_breakdown/fixed_light.py`
(`--source-pixels`, `--mesh`, `--pass-budget-max`). The A100 submit → wait → harvest step is
a human resume point, not a park.

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

- summary: |
    Phase 1: the row phase 0 could only project - the whole `AnalysisImaging.log_likelihood_function`
    under `jax.jit`, five routes, all through the library. Three A100 legs 342908-342910 (gpu-2, fp64).
    The call falls 50.97 -> 25.10 ms on rectangular (2.03x), 65.10 -> 25.39 ms on Delaunay (2.56x) and
    72.95 -> 36.26 ms on DelaunayNN (2.01x) against what the library runs today, at a log likelihood
    identical to the library's own PDIP answer to 1e-15...1e-11 relative. Fixing the light alone pays
    1.31x with no solver change. Phase 0's projection (23.7/25.0/33.1 ms) held to within 6-9 %.
- finding: |
    THE FINDING THAT REDIRECTED THE PROGRAMME: once the solve is 4-11 ms it is no longer the call.
    Of the 25.39 ms certified Delaunay call, only 4.21 ms is the solve; 4.92 ms is the curvature+reg
    build, 2.38 ms both log-dets, and ~13.9 ms is unattributed mesh, mapper and weights - larger than
    everything else put together, and 69 % of the call on DelaunayNN. Another factor of two on the
    solver buys almost nothing on Delaunay. This is the row the follow-on optimisation programme
    (non-solver residue, HST GPU) is built on.
- trap: |
    Two, both recorded in the JSONs. (1) The library subsets `F + lambda*H` and `D` to
    `solve_ids_to_keep` BEFORE invoking its positive-only solver and scatters zeros back after
    (`abstract.py:607-618`), so on rectangular the solver sees n=1369, not 1521 - which is why phase 0's
    budgets transfer as a fact rather than an assumption. (2) `lax.cond` becomes `select` under `vmap`
    and evaluates BOTH branches, so a batched route-d row is the certified solve PLUS the library PDIP
    (33.85 vs 21.35 ms measured). A production implementation must not put a `cond` fallback inside a
    batched path - pad-and-mask, or run a fixed budget with no fallback branch in the batched code.
- note: |
    results/notes/fixed_lens_light_library_path_2026_09.md.

## Original prompt

# Fixed lens light — library-path timing of the S3 positive-negative and certified active-set solvers

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
Witness: results/notes note table of per-call ms for S0-PDIP / S3-PDIP / S3-certified / S3-unconstrained library calls per mesh (rect, delaunay, delaunay_nn), single and vmap16
Review-minutes: 20
Unattended: needs-slicing
Epic: fixed-lens-light-profiling
Phase: 1
Filed: 2026-09-13
Issued: 2026-09-13

Phase 1 of the `fixed-lens-light-profiling` epic. Run strictly after phase 0 (#248) and
strictly before phase 2 — "one step at a time".

## Why

Phase 0 (autolens_profiling #248, Mind `active/fixed_lens_light_source_only_inversion.md`,
note `results/notes/fixed_lens_light_source_only_2026_09.md`) measured on the A100 the
pixelized-imaging likelihood with the lens light FIXED after SLaM light[1]: the MGE
(60 linear Gaussians) converted to regular light profiles at their solved intensities
("S3"), so only source pixels remain in the linear system. Kernel timings: S0 PDIP
positivity solve 37 ms → S3 PDIP 26-28 ms → S3 certified active-set (seed zero set from
the unconstrained solve, masked full-size Cholesky per pass, KKT certification) 4.2 ms on
Delaunay (pass 2) / 11 ms on rectangular (pass 7), the SAME positive solution to 1e-10
nats; S3 unconstrained Cholesky 1.5 ms but +6 nats (Delaunay) / +335 nats (rect) of
evidence. Library calls only moved S0→S3: rect 51.7→38.4 ms, Delaunay 70.4→49.2 ms.

The library-path rows carrying the certified and unconstrained solvers were never
measured — the ~24 ms/call projection for the certified route is arithmetic, not a
measurement. Phase 1 closes that gap and profiles the positive-negative solver for
completeness, as the human asked, even though the certified active-set is the lead.

## What to do

Time the whole `FitImaging.figure_of_merit` jit (library path, not the kernel harness):

- **S3 positive-negative (unconstrained) solve.** The MGE must NOT be in the matrices or
  the solution: use regular light profiles at the solved intensities and subtract them
  from the image beforehand. Positivity off routes to the library's `xp.linalg.solve`.
  **Positivity off silently disables edge zeroing** — record the Δlog-evidence and the
  negative-pixel count beside every timing, never a bare ms.
- **S3 certified active-set** library-path row: fixed pass budget = the certifying budget
  per mesh from phase 0, with PDIP fallback when the budget is exhausted.
- Reference rows: S0-PDIP and S3-PDIP library calls.

Hardware/config: A100 on RAL gpu-2 (fp64), HST dataset, meshes rect / delaunay /
delaunay_nn, single call and vmap16.

Cell `@autolens_profiling/scripts/imaging/likelihood_breakdown/fixed_light.py`
(`--mesh`, `--source-pixels`, `--pass-budget-max`, `--vmap-batch`, `--library-row`);
kernels `@autolens_profiling/scripts/misc/likelihood_breakdown/active_set_steps.py`;
A100 legs via `hpc/batch_gpu/submit_breakdown_imaging_fixed_light_*` + `submit_fixed_light.sh`.
The submit → wait → harvest step is a human resume point, not a park.

Out of scope for the whole epic: the sparse operator (PyAutoArray weight-map bug,
`draft/bug/autoarray/sparse_inversion_ignores_profile_subtracted_image.md`) and JWST.
Dense inversion only.
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

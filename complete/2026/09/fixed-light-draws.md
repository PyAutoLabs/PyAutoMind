- summary: |
    Phase 3: what the certified scheme costs on models that are NOT the fiducial one - a seeded 41-model
    graded draw set. Four legs: A100 343011 (rect, 00:07:49) and 343012 (Delaunay, 00:08:51) on gpu-2
    with every fiducial pin PASS, plus two local JAX-CPU legs. New cell
    `scripts/imaging/likelihood_breakdown/fixed_light_draws.py` plus an importable steps module and
    30 numpy tests (suite 286).
- finding: |
    THE PHASE-0 PASS BUDGETS DO NOT HOLD. Delaunay's pass 2 falls back on 67.5 % of the draw set
    (95.8 % of the random draws) and rectangular's pass 7 on 27.5 %; the smallest zero-fallback budgets
    are 7 (Delaunay) and 11 (rectangular), so phase 4 had to sweep those, not 2 and 7. The two meshes
    fail OPPOSITELY - pass count grows with model error on Delaunay (Spearman +0.698) and falls on
    rectangular (-0.535), because a worse model has a bigger active set that pass 0's 152-pixel
    edge-zero seed already mostly finds. The lever survives at about half its fiducial headline
    (median 2.6x / 5.4x over PDIP on the A100; the worst certified draw still beats the best PDIP call),
    and PDIP's own cost barely moves with the model (15->17, 17->21 iterations), so budget-plus-fallback
    stays a bounded worst case.
- trap: |
    Pass counts, PDIP iterations and seed-set sizes are IDENTICAL on the A100 and the CPU for all 41
    draws - the fallback rate is a property of the problem, not of the device, so it cannot be tuned
    away per hardware. Dropping positivity became unambiguously out here: the A2 error grows to
    +4.07e4 nats (rect) / +6339 (Delaunay) on bad models.
- note: |
    results/notes/fixed_lens_light_low_likelihood_draws_2026_09.md.

## Original prompt

# Fixed lens light — is the certified active-set fast only because the model is good?

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
Witness: results/notes table of certified pass count and ms versus Δlog L across the graded draw set, plus the PDIP-fallback rate at fixed pass budgets 2 / 4 / 6
Review-minutes: 20
Unattended: needs-slicing
Epic: fixed-lens-light-profiling
Phase: 3
Filed: 2026-09-13
Issued: 2026-09-13

Phase 3 of the `fixed-lens-light-profiling` epic. Gated on phase 2 — "one step at a time".

## Why

Every certified active-set timing so far (4.2 ms Delaunay at pass 2, 11 ms rect at pass 7)
was measured at the fiducial model — essentially the truth, after SLaM light[1]. The
certified scheme's cost is the number of passes it needs, and a good model may simply have
an easy active set: few negative pixels, a zero set that barely moves. If poor models need
many more passes, the production win shrinks or disappears, because a non-linear search
spends most of its evaluations far from the truth.

## What to do

Build a draw set of deliberately poor models at graded log-likelihood offsets from the
truth — e.g. Δlog L ≈ −10, −100, −1000, −1e4 — by perturbing θ_E, ellipticity, centre and
slope, plus a set of early-search-like random draws from the SLaM priors so the offsets are
not all one-parameter walks.

For every draw record: certified pass count, certified ms, PDIP iteration count and ms, and
the unconstrained solve's Δlog-evidence (its error at that model, which may itself vary
with model quality). Hardware A100 (RAL gpu-2) and CPU; meshes rect and Delaunay.

Then answer the question the phase exists for: does pass count grow with |Δlog L|, and at
fixed pass budgets 2 / 4 / 6 how often does the certification fail and fall back to PDIP?
The fallback rate is what decides whether a fixed budget is safe in production.

Cell `@autolens_profiling/scripts/imaging/likelihood_breakdown/fixed_light.py`
(`--pass-budget-max`); kernels
`@autolens_profiling/scripts/misc/likelihood_breakdown/active_set_steps.py`. The A100
submit → wait → harvest step is a human resume point, not a park.

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

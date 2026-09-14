- summary: |
    Phase 5 and the LAST of the `fixed-lens-light-profiling` epic - the whole likelihood on real survey
    data, per hardware, and the first time the programme touched Euclid. 24 local legs, all rc=0, no
    timeouts, 45 minutes: Delaunay x {hst,euclid} x {500,1250,2500} on RTX 2060 fp64, RTX 2060 mp and
    JAX-CPU, plus 6 rectangular RTX fp64 legs added when the A100 could not be reached. Cell gains
    --dataset {hst,euclid} (default hst byte-identical), --pass-budget auto, --routes and a
    `reference_recorded` block; 30 tests (suite 398).
- finding: |
    EUCLID IS WHERE POSITIVITY EARNS ITS KEEP, AND HST NEVER SHOWED IT. Dropping it costs
    +3.5 -> +24.3 -> +109.1 nats as N goes 500 -> 2500 on Euclid against a FLAT +8.4 -> +6.4 on HST
    (129 negative source pixels vs 6), because at N=2500 Euclid has 1.5 image pixels per source pixel
    where HST has 6.1. The trend with N REVERSES between the datasets. Any pipeline that reached for the
    unconstrained solve because "Delaunay only costs six nats" was reading an HST number.
    The certified active set is the production solver on every hardware and both datasets - 1.20-1.59x
    over the library today on HST, 1.43-2.28x on Euclid where the lead GROWS with N - and returns the
    library's own answer (every equivalence pin PASS, max 5.6e-10), so its cost in nats is ZERO.
- finding-budget: |
    THE PASS BUDGET IS DATASET-DEPENDENT: rectangular certifies at 6/9/11 passes on Euclid against
    5/7/10 on HST, exhausting phase 3's safe budget of 11 EXACTLY at N=2500, from a single model.
    Delaunay keeps its margin (Euclid 2/4/4, HST 1/2/1, budget 7) and stays the production mesh. The
    rectangular budget of 11 must not be fixed on Euclid without a draw-set sweep of its own.
- production: |
    Per hardware, with affordable N: 4000 HST (A100, carried from phase 4) / 1500 HST + 2500 Euclid
    (RTX 2060) / 1000 HST + 1250 Euclid (8 CPU threads). fp64 everywhere - mixed precision buys 4-9 %
    for <= 1.3e-4 nats with an identical certifying budget on Delaunay, too small to be worth a
    withdrawn pin. Memory is never the wall (2.70 GB of 6 GB worst).
- open: |
    THE 12 A100 LEGS WERE NOT RUN - the RAL jump host refused publickey all session and the direct route
    times out. The four arrays are written, validated and committed; resume is one command on the RAL
    login node: `hpc/batch_gpu/submit_fixed_light_verdict.sh --node euclid-ral-gpu-2`. Every A100 number
    in the note is carried from phases 1 and 4 and labelled as such; nothing was extrapolated.
- epic: |
    `fixed-lens-light-profiling` is COMPLETE - all six phases merged 2026-09-14 (PRs #250, #252, #254,
    #256, #258, #260, a stack of six merged in base order). Follow-ups filed as ideas.md bullets: the
    library implementation of the certified solver, the matched-injection witness, re-deriving the
    rectangular budget on Euclid, and the unrun A100 legs. Two of the verdict's implications were filed
    as fresh research programmes on the same day: the same programme on the numba CPU path, and an
    optimisation campaign against the non-solver residue of the HST GPU breakdown.
- note: |
    results/notes/fixed_lens_light_verdict_2026_09.md.

## Original prompt

# Fixed lens light — whole-likelihood assessment on HST and Euclid at 500 / 1250 / 2500 source pixels

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
Witness: results/notes 2 datasets x 3 source-pixel counts x 3 hardware table per solver (S3-certified / S3-unconstrained / S0-today), and a stated production configuration per hardware
Review-minutes: 25
Unattended: needs-slicing
Epic: fixed-lens-light-profiling
Phase: 5
Filed: 2026-09-13
Issued: 2026-09-13

Phase 5 of the `fixed-lens-light-profiling` epic — the programme's verdict. Gated on
phase 4 — "one step at a time".

## Why

Phases 1-4 measure solvers, hardware and scaling one axis at a time. Phase 5 is the
assessment the human actually asked for: for each hardware type, what does the whole
likelihood function cost on real survey data, and which configuration should production
use. Nothing else in the epic answers "which one do we ship".

## What to do

Whole-likelihood assessment on the **library path** (`FitImaging.figure_of_merit` call, not
the kernel harness) across the grid:

- Datasets: HST (0.05", `autolens_profiling/dataset/imaging/hst`) and Euclid (0.1",
  `.../euclid`). JWST is dropped by human decision.
- Source pixels: 500, 1250, 2500.
- Hardware: A100 (RAL gpu-2, fp64), CPU, RTX 2060 via the `PyAutoGPU` venv (fp64 and
  fp32/mp).
- Solvers: S3 with certified positivity, S3 unconstrained, and S0 as it stands today.

Dense inversion only — the sparse operator is out of scope for this epic (the PyAutoArray
weight-map bug, `draft/bug/autoarray/sparse_inversion_ignores_profile_subtracted_image.md`),
even though the human's original text named it as a variant.

The note is the programme's deliverable: the full table, and then a written verdict naming
the production configuration per hardware — solver, pass budget, precision, and the source
pixel count each hardware can actually afford — with the evidence cost of every shortcut
stated in nats, not just in ms.

Cell `@autolens_profiling/scripts/imaging/likelihood_breakdown/fixed_light.py`
(`--library-row`). The A100 submit → wait → harvest step is a human resume point, not a park.
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

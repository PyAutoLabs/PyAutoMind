# Phase 5: CPU NNLS memo robustness across graded draws

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Epic: fixed-lens-light-numba-cpu
Phase: 5
Difficulty: large
Autonomy: human-required
Priority: high
Consequence: judge
Review-minutes: 25
Filed: 2026-09-18
Witness: Replay all 41 graded models through the production single-threaded CPU likelihood with memo enabled and disabled; report per-model evidence agreement at <= 1e-9 relative, active-set equality, reconstruction differences, whole-call times, seed sources, memo invalidations, cold retries and solver iteration counts. An incomplete or numerically failing run cannot certify robustness.

## Original user request (verbatim)

> continue

Conversation context: the user asked for the next phase after phase 4b and accepted
continuation of phase 5, the warm-start robustness study. Earlier request:

> We have done lots of work profiling and speeding up the numba CPU likelihood function which uses a _sparse API, can you check this work and continue it

The user approved the phase-4b factor check
`max(2e-12 nats, 32 floating-point spacings)` with relative factor-reconstruction
residual <= 1e-12. This approval does not relax active-set equality or the 1e-9
relative evidence gate. Apply that factor criterion only if factors are compared.

## Overview

Measure whether the production `fnnls` passive-set memo helps when successive
models have progressively worse likelihoods. Phase 4b found no qualifying
permutation speedup (PR #277); this study uses production main and does not
depend on its prototype. Primary repository: @autolens_profiling. No library
algorithm change is proposed.

## High-level plan

1. Reuse the existing 41-model graded draw manifest and validate its provenance.
2. Compare independent memo-on and memo-off traversals using the production CPU
   source-only likelihood, with setup and compilation outside timing.
3. Observe memo behaviour and iterations in separate diagnostic traversals, and
   check warm/cold numerical agreement for every model.
4. Run matched, single-threaded CPU measurements and publish JSON, figures and a
   verdict identifying where warm starts help, invalidate, retry or become cold.

## Detailed implementation plan

### Branch survey and coordination

On 2026-09-18, `autolens_profiling` main is clean at `92f1fad`; phase-4b PR #277
is open and lint passes. Mind main is current, with unrelated dirty prompts
`active/fields_api_top1000.md` and `active/mass_field_bare_fields_slot.md`.

`worktree_check_conflict fixed-light-numba-s5 autolens_profiling` exits 1:
`hst-gpu-residue-p2` (#273) and `fixed-light-numba-s4b` (#276) both claim the
repository. Proposed branch: `feature/fixed-light-numba-s5`, based on origin/main,
in `~/Code/PyAutoLabs-wt/fixed-light-numba-s5/`.

Coordination approval is pending. All phase-5 implementation and result files
below are new; existing helpers are read-only. No edit to either active task's
files, shared README surfaces, or shared solver helpers is planned. Record the
human's explicit coordination decision before creating the worktree.

### Implementation

1. Add `scripts/misc/likelihood_breakdown/fixed_light_numba_draws_steps.py` for
   manifest validation, isolated memo lifetimes, sequence replay, production
   solver observation and result summaries. Reuse the pure-NumPy
   `fixed_light_draws_steps.py` helpers; do not import the JAX draw cell.
2. Add `scripts/imaging/likelihood_breakdown/fixed_light_numba_draws.py`. Freeze
   the 41 offsets from
   `results/breakdown/imaging/fixed_light_draws_delaunay_hpc_a100_fp64_fixed_light_draws.json`
   (1 fiducial, 16 walks, 24 random draws, seed 0), storing its SHA256 and validating
   names, families and membership. Recompute S0 likelihoods on current CPU code;
   preserve requested targets separately from achieved likelihood drops.
3. Match the graded-draw study's per-model S0-to-S3 construction: solve lens light
   for each model, subtract and build its source-only analysis before timing.
   Explicitly report this construction; it differs from holding one subtraction
   fixed across all models. Report preparation cost separately. Use each mass
   family's own fiducial for likelihood drops. Preserve the existing slope-family
   promotion check; failed promotion yields an incomplete study, not a 41/41 pass.
4. Time complete traversals in the original order and one recorded seeded
   permutation, alternating memo-on/off order across repeats. Clear the memo at
   each traversal boundary. Warm compilation outside timing, then clear its memo;
   never prime a measured draw from its own solution. Each likelihood evaluation
   must execute afresh, without reusing cached fit results. Production thread
   counts are one for BLAS, Numba and likelihood process; record observed settings.
5. Run separate observed traversals through the unchanged production entrypoint.
   Record `seed_source`, `warm_start_fallback`, warm-start errors, outer/inner
   iterations, final passive set and each kernel attempt. Distinguish memo guard
   invalidation (affects the next solve), exception-triggered cold retry, and an
   ordinary cold miss. Do not call these PDIP fallbacks. Keep instrumentation out
   of headline timing; verify observed and unobserved results agree.
6. Compare memo-on with independent memo-off results for every draw and order:
   finite values, exact active-set equality, reconstruction difference and
   <= 1e-9 relative evidence difference (also report absolute nats). Record any
   failure without suppressing difficult models. Snapshot and restore any memo
   state touched by diagnostics; no state may cross comparison lanes.
7. Add a dedicated CPU submit under
   `hpc/batch_cpu/submit_breakdown_imaging_fixed_light_numba_draws_delaunay_ral_hst_fp64`.
   Run local correctness smoke first; then RAL CPUs-only, HST Delaunay N=1500,
   fp64, at least five complete timed traversals per lane/order. Record library
   revisions, source hashes, hardware, job ID, settings and cold-start conventions.
8. Publish task-specific JSON/PNG under `results/breakdown/imaging/` and
   `results/notes/fixed_lens_light_numba_memo_2026_09.md`: per-draw paired costs,
   medians/tails, likelihood-quality relationships, iteration/fallback tables,
   numerical gates and limitations. State whether the memo helps and where it
   loses its benefit; no mandatory speedup threshold or library promotion.

### Validation

Add `scripts/misc/test/test_fixed_light_numba_draws.py` with meaningful tests for
memo isolation at traversal boundaries, retry-versus-invalidation classification,
manifest completeness, sequence alignment and numerical gate failure reporting.
Run focused tests, changed-cell import smoke, Ruff check/format, shell syntax,
README idempotence and artifact completeness/provenance checks. Review the branch
before shipping through start-workspace / ship-workspace.

### Scope and remaining gates

No source-pixel scaling, Euclid run, GPU timing, library solver edit or merge is
part of phase 5. Sparse API assembly is the production CPU route; this is not
promotion of the separately deferred sparse linear operator. Phase-4b's Heart
RED shipping exception applies only to #276; evaluate phase-5 shipping readiness
when its concrete deliverable is ready.

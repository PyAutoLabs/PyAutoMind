# Phase 7: HST and Euclid numba CPU configuration verdict

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Epic: fixed-lens-light-numba-cpu
Phase: 7
Difficulty: large
Autonomy: human-required
Consequence: judge
Priority: high
Review-minutes: 30
Status: shelved by user — 2026-09-18
Filed: 2026-09-18

## Original user request

> do phase 7

## Context and objective

Phase6 is merged as PR283, record complete/2026/09/fixed-light-numba-s6.md.
N4000 nearby cold/memo2.138/1.289s; broad4.312/10.783s. NNLS dominates larger
systems. Phases5/5b found no promotable residual-precheck policy. Phase7 must
produce a qualified HST+Euclid production-configuration verdict, not infer a
global memo default from short synthetic sequences. Existing source files and
library behavior remain unchanged. This is likelihood profiling, not a sampler
benchmark or a converged scientific inference campaign.

## High-level plan

1. Measure simulated HST and Euclid imaging with the production numba `_sparse`
   assembly, Delaunay, fp64, positive-only NNLS, one CPU/BLAS/Numba thread.
   Use N1500 and N2500, recording actual mapper and solve dimensions.
2. Obtain real evaluation-order histories from bounded serial Nautilus pilots
   on each instrument at N1500, with two fixed seeds701/702. Preserve rejected
   evaluations and original order. Store all proposals/evidence and immutable
   metadata; never relabel a synthetic draw set as a sampler history.
3. Replay predeclared contiguous early and later windows through cold and
   production-memo lanes at both sizes. Six fresh-cache repetitions, balanced
   order, clean whole-Analysis timing and separate exclusive diagnostics.
4. Re-measure joint-light/source and source-only fiducial baselines for each
   instrument/size using the existing route definitions. Report subtraction/
   preparation separately from source-only likelihood timing; no multiplication
   of speedups measured in different historical stacks or workloads.
5. Apply unchanged active-set/evidence checks, report failures and timing
   reconciliation honestly, and publish runtime distributions, memory, memo
   hits/fallbacks and provenance. Recommend only configurations supported by
   the tested histories; an inconclusive or workload-dependent verdict is valid.

## Detailed plan

New files only, based on origin/main containing merged PR283:
- scripts/imaging/likelihood_breakdown/fixed_light_numba_verdict.py:
  CLI modes for bounded trace capture, frozen replay cells and aggregation.
  Parameterize instrument in new preparation code while reusing established
  phase5/6 helpers read-only. Preserve model/priors/mask/oversampling/adapt-image
  conventions, record them in each artifact; instrument-specific settings must
  be explicit. Use the installed sampler API, not assumed kwargs.
- scripts/misc/likelihood_breakdown/fixed_light_numba_verdict_steps.py:
  trace schema, fixed window selection, replay orchestration, reporting and
  qualified verdict logic. Reuse phase6 exclusive timers and phase5 comparator.
- scripts/misc/test/test_fixed_light_numba_verdict.py:
  original-order/all-evaluation capture, nonoverlapping fixed windows, truncated
  pilot handling, hash immutability, lane cache isolation, numerical failures,
  missing/failed cells and no unsupported global verdict.
- hpc/batch_cpu/submit_breakdown_imaging_fixed_light_numba_verdict_ral_fp64:
  bounded CPU-only trace then dependent replay jobs, one allocated CPU,64GiB,
  maximum4h per job; serialized array to limit load. Pin environments before
  imports. No GPU allocation or shared-library refresh.
- results/breakdown/imaging/: frozen trace/declaration JSON, per-cell raw
  timings/numerical evidence, aggregateJSON/PNG and source/job/hash sidecar.
- results/notes/fixed_lens_light_numba_verdict_2026_09.md:
  campaign synthesis with current-stack HST/Euclid comparisons, configuration
  table, memo regime sensitivity, preparation/RSS limitations and open questions.

Trace protocol: serial Nautilus, n_live100, fixed seeds701/702, cold reference
lane, up to2048 attempted likelihood evaluations per pilot and a2h capture
budget. Stop at the declared limit; retain partial/censored histories. Instrument
at the actual likelihood entry so rejected/invalid proposals remain in the log.
No stopping/tuning based on favorable speedups. Use the same source-only target
and per-proposal light preparation as replay, recording preparation separately.
Select first64 and final64 evaluations only when at least128 were captured;
otherwise record insufficient coverage, without extending the pilot after
seeing lane timings. Label windows by call indices and actual sampler stage;
"later" does not mean posterior-converged. The N2500 replay intentionally uses
N1500-generated proposals and must be labeled as a cross-resolution replay,
not a native N2500 search. Each window starts cold; cache resets and the limited
history scope remain visible. Invalid evaluations are retained, excluded only
from finite-solution parity with explicit reasons/counts, never silently dropped.

Numerical gates: exact active-set membership and unchanged1e-9relative evidence
for memo/cold at the same instrument,N,model; finite same-shaped reconstruction
with error reported. Every timed evaluation agrees with its diagnostic lane.
Do not compare different discretizations or joint vs source-only routes as if
they solve the same optimization problem. Positivity is never relaxed. Any
factor diagnostics reuse the approved roundoff criterion max(2e-12nats,
32floating-point spacings) plus1e-12relative reconstruction residual; no new
numerical tolerance without approval. Breakdown is interpretable only at<=5%
clean/observed median discrepancy, with raw exclusive closure. Clean likelihood
results remain separately labeled if breakdown fails.

Validation: HST/Euclid small-N numerical smoke and parent N1500 parity;
focused helper and inherited numerical tests; Ruff/format, shell and submit
contracts, API audit/import smoke, README idempotence; independent code review
before RAL and independent empirical/note/provenance review before shipping.
Source hashes, library revisions/cleanliness, dataset hashes, hardware/thread
observations, peakRSS and completed/failed job states captured before/after.
Unobservable runtime BLAS count must say unavailable; envpins are not proof.
RSS includes preparation and retained analyses, not per-worker guidance.

## Survey and authorization boundary

Canonical autolens_profiling is clean on main (six commits behind origin/main
at initial survey); read the current remote main for planning, create new
worktree from current origin/main. Proposed task/branch fixed-light-numba-s7 /
feature/fixed-light-numba-s7; root ~/Code/PyAutoLabs-wt/fixed-light-numba-s7.
Active claims: hst-gpu-residue-p2 and fixed-light-numba-s4b. The new phase must
use disjoint new files and its own RAL snapshot. Explicit parallel-worktree
approval is required by start-dev; prior phase6 authorization does not cover
phase7. Plan/issue body approval is also required before implementation.
PyAutoMind is main; unrelated untracked draft/bug/pyautomind/ is preserved.
No issue, worktree, implementation, compute submission or Heart shipping
exception has yet been authorized for this detailed plan.

## User decision — 2026-09-18

> for now, lets assume memo is not possible and sampler order changes. It is out of scoep to try and put off memo currently, vbut I am glad we research it, so maybe shelve phase 7?

Phase7 is shelved before issue creation, worktree setup, source edits or compute
submission. For current design/runtime planning, assume no usable memo benefit
and changing sampler order. Further memo policy, sampler ordering and trace
studies are out of scope. Preserve phases5/5b/6 findings; do not disable or
otherwise change production memo defaults. This is a planning assumption, not
proof memo never helps. Resume only if the user explicitly reopens phase7 and
approves a newly scoped plan. The proposal above is historical, not authorized.

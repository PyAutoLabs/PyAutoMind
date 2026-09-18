# fixed-light-numba-s5b

Merged PR: https://github.com/PyAutoLabs/autolens_profiling/pull/281
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/280

The locked pre-solve residual policy fails promotion: nearby holdout is 11.66% slower than memo, broad holdout 5.28% slower than cold. NO_LEVER; no production changes.

Validation: 24 focused tests; full-size numerical and matched-state smokes; independent review CLEAN; 276 evaluation and 224 calibration comparisons pass. All GitHub workflow runs and jobs on the shipped head passed.

The live user explicitly approved merging both #279 and #281 in dependency order on 2026-09-18. Both merged with merge commits, #279 first and #281 retargeted to main. Heart RED remains acknowledged: `release validation FAILED (stage integrate)`; YELLOW: `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`. This was development merge authority, not release authority.

Local worktree retained pending permission to remove ignored output/data products. Committed research artifacts are on main; additional local scratch and smoke products remain in the worktree.

## Original prompt

# Phase 5b: reject unsuitable CPU memo seeds before the expensive solve

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
Epic: fixed-lens-light-numba-cpu
Phase: 5b
Difficulty: large
Autonomy: human-required
Priority: high
Consequence: judge
Review-minutes: 25
Filed: 2026-09-18
Issued: 2026-09-18
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/280
Witness: A profiling-only pre-solve memo eligibility prototype is compared with unchanged production memo-on and memo-off likelihoods on broad and nearby model sequences, with independent holdouts, gate overhead included, exact active-set equality and <=1e-9 relative evidence agreement. Publish a qualified go/no-go verdict; no production default changes in this task.

## Original request (verbatim)

> ok continue

Context: after phase 5 found memo-on 56–60% slower on broad-proposal stress
sequences, the assistant proposed investigating rejection of unsuitable memo
seeds before paying for their warm solve, while preserving nearby-model gains.
The user approved continuation. This task formalizes that investigation.

## Evidence and scope

Primary repository: @autolens_profiling. Phase-5 issue #278 / PR #279 records
RAL job 343398: graded cold/warm 382.888/611.286 ms per call, permuted
381.977/594.973 ms, 82/82 numerical comparisons passing. There were 18/22 and
19/21 post-solve memo invalidations, no exception retries, and substantially
more warm solver iterations. The present error guard is retrospective:
`warm_start_errors` counts disagreement with the final passive set, so it cannot
be checked before solving. Simply lowering its threshold cannot prevent the
first expensive seeded solve.

Prior work (PyAutoArray #498/#501) demonstrated large nearby-walk benefits and
showed that absolute seed-error counts did not separate useful from harmful
seeds. Do not reverse that decision based solely on the new stress set.

Read-only follow-up of phase-5 artifacts: 15/22 graded memo hits and 19/21
permuted hits were >3% slower than cold; 7 and 2 hits were >3% faster. Selecting
the faster measured lane with hindsight would save only about 9.64 and 2.96 ms
per model over cold on those respective sequences. This is a descriptive
hindsight comparison of existing samples, NOT a rigorous bound, realizable policy
or predicted whole-call speedup: changing decisions also changes future memo state.
The immediate target is avoiding the large losses, not promising a large gain
over cold on this particular stress distribution.

## High-level plan

1. Prototype one cheap pre-factorisation eligibility score in the profiling
   harness; preserve the production NNLS algorithm and cold fallback.
2. Calibrate a small, declared threshold grid on separate training sequences,
   then lock the policy before examining holdout performance.
3. Compare cold, unchanged memo, and guarded memo on the original graded set,
   a nearby-model walk and independent broad/nearby holdouts.
4. Include every precheck and cache-maintenance cost in whole-likelihood timings;
   publish numerical gates, false acceptance/rejection, runtime and a go/no-go.

## Detailed plan

### Prototype

Store the previous reconstruction alongside a profiling-only memo entry. For
current matrix A and vector b, compute g = A @ x_previous - b before requesting
a memo seed. Test a dimensionless KKT-residual score: passive coordinates use
absolute residual; inactive coordinates use only the negative residual, with
normalisation by current A @ x_previous and b magnitudes and an explicit zero
case. This is an O(N²) matrix-vector operation, not a factorisation. It is a
candidate signal, not an assumed predictor of iteration cost.

Reject missing, incompatible, nonfinite or high-score entries and run the
unchanged production cold path. Acceptable entries use the unchanged production
warm path and existing post-solve guard. The score must never use the current
cold solution, current final active set, final evidence, or timing outcome at
runtime. Preserve separate rejection, invalidation and exception-retry counters.

Implement through task-local context-managed wrappers around the production
entrypoint/memo lookup; restore all functions, environment and caches on exit.
Maintain complete-traversal memo isolation as in phase 5. No PyAutoArray source,
public API, packaged config or default is edited here. Any eventual library
promotion is a separate approved development task.

### Calibration and evaluation

Declare seeds, walk scale, threshold candidates and selection rule in the
artifact before tuning. Use a short nearby walk and broad random calibration
sequence (seed 278), disjoint from the seed-0 phase-5 models and seed-1 holdouts.
Select a single threshold using calibration timings and numerical gates only.
Record all candidates, including an unhelpful or inseparable score. Do not pick
separate favourable thresholds after seeing each evaluation sequence.

Evaluate the locked candidate on:
- The frozen original 41 models, graded and seed-278 permuted order.
- A 32-model nearby random walk, with per-step offsets expressed in original
  prior-sigma units; seed 1, step scale 0.05, parameters and clipping recorded.
- 24 new broad random draws using the original 5-sigma recipe and seed 1.

Use the phase-5 per-model S0-to-S3 subtraction convention on all lanes and
sequences. Setup remains separate. All production, cold and prototype lanes
receive identical models and begin with empty independent caches; clear after
compilation. Source-only N=1500 HST Delaunay, fp64, CPU sparse API, threads pinned
one. Record runtime thread observations accurately, including an unavailable
BLAS pool count rather than treating an empty inspection list as an observation.

Short calibration can use extracted systems, but no kernel-only result becomes
a whole-call speedup claim. Final selection is assessed with at least five
counterbalanced complete traversals per lane, including precheck and cache
costs. Record precheck overhead separately in diagnostics. Report both absolute
nats and relative evidence differences, reconstruction differences, active sets,
iteration counts, decisions and sequence totals. Preserve the <=1e-9 relative
evidence and exact active-set gates. If factors are inspected, use the already
approved max(2e-12 nats, 32 spacings) plus <=1e-12 relative reconstruction residual.

Proposed performance targets (go/no-go, not correctness relaxations): at least
5% faster than unchanged memo on both original stress orders; at most 3% overhead
versus cold on broad evaluations and versus unchanged memo on the nearby holdout.
Show repeat scatter. Failure is a valid NO_LEVER verdict, not permission to tune
against the holdout or change the numerical criteria.

### Files and validation

New files only:
- `scripts/imaging/likelihood_breakdown/fixed_light_numba_memo_policy.py`
- `scripts/misc/likelihood_breakdown/fixed_light_numba_memo_policy_steps.py`
- `scripts/misc/test/test_fixed_light_numba_memo_policy.py`
- A dedicated `hpc/batch_cpu/submit_breakdown_imaging_fixed_light_numba_memo_policy_delaunay_ral_hst_fp64`
- Task-specific JSON/PNG/source sidecar and
  `results/notes/fixed_lens_light_numba_memo_policy_2026_09.md`.

Reuse phase-5 helpers read-only. Tests cover pre-solve ordering, no oracle leakage,
invalid/zero-scale inputs, memo state transitions and restoration, cold fallback,
locked calibration and holdout separation. Run live full-size numerical smoke,
Ruff, import smoke, shell/API/README checks, then RAL and independent review.
No changes to #277, #279 or GPU-study source files or shared generated surfaces.

## Branch survey and coordination

Proposed task/branch: `fixed-light-numba-s5b` / `feature/fixed-light-numba-s5b`.
On 2026-09-18 the profiling repo is still claimed by `hst-gpu-residue-p2` (#273),
`fixed-light-numba-s4b` (#276, PR #277), and `fixed-light-numba-s5` (#278, PR #279).
The conflict guard reports all three. PyAutoArray has no conflicting registry
claim, but is read-only reference material for this research task.

PR #279 is open, so use an isolated worktree based on its `cd68548` head, with
only the new files above changed. This is a stacked dependency: #279 must land
before merging the follow-up; do not merge #279 as an implicit side effect.
If #279 has merged before setup, use updated origin/main instead. Record the
base revision and scope the follow-up diff against it.

Explicit coordination approval received 2026-09-18:
> contnue   May I create another disjoint worktree, based on PR #279, for this prototype? yes

This approves the concrete file-disjoint plan and waives the three existing
worktree claims above for this task. Base: cd685483b4f819801231bef0e1e9102be54f9fa5.
The #278 Heart override remains task-specific; any phase-5b shipping override
will be requested separately after implementation and validation.

## Result and shipping checkpoint — 2026-09-18

RAL job 343413 completed successfully in 01:01:18, peak RSS8155204KiB.
The declared calibration selected threshold0.5 before evaluation. The prototype
passes all numerical gates (276 evaluation and224 calibration comparisons),
but records NO_LEVER: nearby holdout is11.66% slower than existingmemo and broad
holdout is5.28% slower than cold, exceeding the respective3% limits. Original
stress orders improve35–38% over existingmemo and remainwithin3% ofcold.
Matched diagnostics find1 harmful acceptance and14 missed useful seeds.

The ten task-specific files, including complete JSON/PNG, declaration, lock,
source/job sidecar and resultsnote, are committed in the approved worktree. No
production library or existing task file changed. Independent full review is
CLEAN;24tests plus full-size smoke, Ruff/format/import/API/shell/README and
artifact/source checks pass. The study is complete and not a production policy
promotion. See `results/notes/fixed_lens_light_numba_memo_policy_2026_09.md` in
the worktree for exact tables and limitations.

Heart remains RED: `release validation FAILED (stage integrate)`;
YELLOW: `manifest drift: remote-session blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`.
The live user replied **“yes go”** to the task-specific #280 commit/push/PR
request on 2026-09-18. Approval is recorded on issue #280 and the PR.

Committed and pushed as `a18cb7481d9a33d26f1145144af150a86a3d3bf7`.
[PR #281](https://github.com/PyAutoLabs/autolens_profiling/pull/281) is open,
labelled pending-release, stacked on `feature/fixed-light-numba-s5` (#279).
The diff contains only the ten new phase-5b files. Post-commit import smoke
passed; lint CI was in progress when checked. Await CI and a separate human
merge command, with parent #279 merged first. No merge or release grant.

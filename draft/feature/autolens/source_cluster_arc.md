# Source & Cluster arc — magnification science, PointSolver trust, cluster extended sources

Type: feature
Target: PyAutoLens
Repos:
- PyAutoLens
- PyAutoArray
- PyAutoGalaxy
- autolens_workspace
- autolens_workspace_test
- autolens_profiling
- HowToLens
Themes:
- cluster
- point-source
- pixelization
Difficulty: too-large
Autonomy: supervised
Priority: high
Status: draft
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing
Epic: cluster-strong-lensing
Filed: 2026-08-19 (backfilled from git)

Parent tracker for a 12-phase arc (2026-08-19 intake; deep-research grounded). This
file is never routed to start_dev directly — each phase below is its own prompt,
issued ONE AT A TIME as its predecessor nears shipping (no bulk issue queues).

Science anchors: LEGGOS II (arXiv:2606.20804 — point μ = map value at pixel; area
μ_arc = A_img/A_src with A_src = Σ A_pix,i/μ_i, Eq. 6-7; errors from ~300 posterior
draws; Fig. 4 fractional-uncertainty map with constant-μ contours; critical curve as
arc-segmentation boundary), Richard+17 (HFF magnification-map deliverables), Atek+15
(magnification as source-science tool), Jullo+08 (multi-z cluster cosmography).

## Current ownership and dependencies — approved 2026-10-01

The Source & Cluster arc now owns magnification/source-science capabilities.
Remaining PointSolver correctness/settings/performance work and the old phase-2
profiling scope belong to `cluster-pointsolver-speed` (display title: Cluster
PointSolver — robustness and performance). Canonical planning contract:
`https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/cluster_pointsolver_speed.md`.

Phase 1a–1d are completed evidence/fixes; remaining phase-1 scope is TRANSFERRED,
not solved or declared safe. Phase 2 is TRANSFERRED, not completed. Historical
entries below saying phase 1 blocks the entire arc or phase 2 remains gated are
superseded by this approved split. Preserve original numbering for cross-links.
**Next arc step: phase 3, critical-curve dispatch**, sliced through start_dev.
No next-phase issue is opened by this reorganisation.

- Phases 3–8 retain their explicit intra-arc dependencies, with no blanket
  PointSolver-health prerequisite. Magnification at supplied/observed image
  coordinates, pixel-based arc areas, and associated maps do not require a
  forward point solve. Phase 6's forward ShapeSolver scope transfers too.
- Phase 9 depends on 3 and 5–8. Examples using supplied image positions and
  independently validated fit/model inputs can proceed. Any path discovering
  images or consuming solver-dependent posteriors must pass the specific
  coverage/accuracy/overflow checks for that workload; known-invalid fit results
  cannot become valid merely because post-processing avoids a solver call.
- Phases 10 and 12 retain their declared dependencies and workload-specific
  validation. No generic solver completion gate is added. Phase 11 stays dropped.
- `autolens_profiling` owns robustness/settings investigations and cost evidence;
  stable numerical witnesses become integration tests in
  `autolens_workspace_test`, with an explicit PR-smoke or scheduled/release CI
  lane. Research-cell success alone never establishes production correctness.

## Phases (original numbers retained; dependencies below govern)

1. **Transferred remainder** — `draft/bug/autolens/point_solver_error_bisect_health.md`
   now belongs to `cluster-pointsolver-speed`. Subphases 1a–1d shipped; unresolved
   overflow, accuracy/identity and regression work remains there.
2. **Transferred scope** — `https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/point_solver_profiling_cells.md`
   now belongs to the solver programme. Reconcile existing cells and single-source
   campaign ownership before issuing missing coverage; no duplicate campaign.
3. `draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md` — context-aware
   engine dispatch, dedupe twin plot_utils, cluster plots honor the flag. Before all
   map/segmentation phases.
4. `draft/test/workspaces/mesh_magnification_correctness.md` — areas + magnification
   recovery across every mesh variant (rectangular/delaunay/delaunay_nn/knn).
5. `draft/feature/autolens/point_magnification_api.md` — μ at a point, documented in
   source_science + point package; parity decision; multi-plane.
6. `draft/feature/autolens/area_magnification_leggos.md` — LEGGOS Eq. 6-7 pixel-
   inversion area μ as primary; wiki ingest. Forward ShapeSolver work transferred.
   Gates: 3, 5.
7. `draft/feature/autolens/magnification_errors_posterior_draws.md` — standalone
   posterior-draw errors in source_science; latent decision. Gates: 5, 6.
8. `draft/feature/autolens/magnification_maps_visualization.md` — image-plane contour
   maps, source-plane mesh maps, Fig-4 uncertainty map, pretty pass. Gates: 3-7.
9. `draft/feature/workspaces/cluster_source_science.md` — new cluster/source_science.py
   (point-source tier). Gates: 3, 5-8; workload-specific solver checks only.
10. `draft/feature/workspaces/cluster_pixelized_analysisfactor.md` — per-source-mask
    pixelized refinement via AnalysisFactor; implements the extended_source plan in
    `draft/docs/workspaces/cluster_regime_narrative.md`. Gates: 4, 9.
11. → **Cortex** `PyAutoCortex/archive/tasks/inference_programme/cluster_extended_source_inference.md`
    — JAX-gradient joint-inference feasibility verdict (go/no-go only). Moved out of the
    Mind on 2026-09-01 in the Cortex phase-4 migration (was
    `draft/research/autolens/cluster_extended_source_inference.md`). **Dropped** by human
    ruling `R-20260907-05` when `inference_programme` was retired on 2026-09-07.
    History: `PyAutoCortex/projects/inference_programme.md`; ruling:
    `PyAutoCortex/archive/rulings/2026/09/R-20260907-05.md`.
    Any future science project/task needs a fresh Cortex birth; do not revive the
    retired project implicitly. Original dependency remains phase 10.

    **Known drift, not fixed here:** two different prompts both declare `Phase: 10` under
    two different parents — `draft/feature/workspaces/cluster_pixelized_analysisfactor.md`
    (this arc's phase 10) and `draft/docs/workspaces/cluster_regime_narrative.md` (a
    different parent). Different parents, so nothing is ambiguous inside this ledger, but a
    reader searching on `Phase: 10` will hit both. Recorded, deliberately left alone.
12. `draft/docs/howtolens/cluster_pixelized_source.md` — HowToLens cluster tutorial
    pixelized source + fix the already-stale cross-reference (the stale-claim fix may
    land early if a HowToLens release precedes phase 10). Gate: 10.

## Reconciliation — 2026-09-30

- Last completed numbered phase: none found. Phases 1-10 and 12 remain drafts;
  no matching active.md row or open phase issue/PR was found. No adjacent
  DECISIONS/RESULTS file was present. Phase 11 is dropped as recorded above.
- Cross-checked open issues/PRs in PyAutoLens, PyAutoArray, PyAutoGalaxy,
  PyAutoNerves, autolens_workspace, autolens_workspace_test, autolens_profiling
  and HowToLens. Related open autolens_workspace_test#106 concerns cluster
  likelihood scripts and precision-floor sensitivity; it does not complete phase 1.
- Separately shipped evidence to reuse: PyAutoLens#710 (dataset-cap guard),
  PyAutoLens#480 (source-plane selection in magnification filtering),
  PyAutoGalaxy#591 (adaptive Richardson Hessian), PyAutoArray#584 and
  PyAutoLens#753 (merged 2026-09-27; cap now 20). Point-source CPU campaign
  records are sibling work, not completion of this arc's phase 2.
- Brain classifies the existing phase-1 umbrella as too large. Next bounded step:
  `complete/2026/09/point-solver-error-audit.md` (phase 1a). This is
  an audit-only workspace PR before evidence-driven library hardening; phase 1
  stays incomplete until the audit and required hardening are accepted.
- Full phase-1 repo claims conflict: PyAutoArray is claimed by
  `raw-pdip-forward-polish`; autolens_profiling by that task and
  `interferometer-decision-matrix`. Phase 1a writes only autolens_workspace_test;
  the worktree conflict guard passes for that repo. Its open #106 is related but
  targets different cluster scripts. Other repositories are read-only inputs.
- start_dev: Heart STALE (no report.json); planning may continue. Phase 1a plan approved 2026-09-30; issued as autolens_workspace_test#328
  on feature/point-solver-error-audit. No issues queued for later phases.

## Phase 1a execution — 2026-09-30 (historical session log; now shipped)

- User approved the plan with “go”; issued only autolens_workspace_test#328.
  Worktree: `/home/jammy/Code/PyAutoLabs/.worktrees/point-solver-error-audit`;
  workspace branch `feature/point-solver-error-audit`, base `7a47bac`.
- Implemented audit scripts, RESULTS.md and three JSON witnesses under
  `autolens_workspace_test/scripts/point_source/solver/`. 24 full-data CPU
  NumPy/eager-JAX/JIT rows; 16 historical-Hessian replay comparisons;
  capacity/dtype checks; existing image-plane parity passes; workspace smoke
  **32 passed, 0 failed**. Formatting and staged diff whitespace checks pass.
- Historical attribution is limited: pre-March stack import lacks autoconf.
  The report explicitly distinguishes historical-method replay on current
  deflections from a full historical-stack bisect.
- Findings: call-time xp override uses the constructor's padding default and
  fails under jit; symmetric quad returns duplicate centroids on NumPy/eager
  JAX at scale 0.05; synthetic capacity overflow silently truncates. Float32
  NaN placeholders preserve float64 vertices in the tested paths. Actual
  fixture containment counts peak at 13. Local point magnification remains
  the appropriate filter quantity; buffer changes do not explain a positional
  regression at threshold 0.1 in these fixtures.
- Corrected chronology: cap argument removed in 2024-12 (`5c42d8133`), not
  April 2026; JAX jacfwd added 2026-03-02 (`ee92bebe`), NumPy Richardson in
  April. The parent bug prompt carries these corrections and hardening scope.
- **Not shipped:** staged local changes, no feature commit/push/PR. Latest
  Heart RED: “release validation FAILED (stage integrate)” at
  2026-09-30T17:54:24Z. Earlier PyAutoGalaxy CI RED cleared on refresh.
  Await live development-only override for #328, then ship_workspace.
  Progress: https://github.com/PyAutoLabs/autolens_workspace_test/issues/328#issuecomment-5916747192
- Phase 1 is still incomplete. Do not start phase 2 or revive the dropped
  Cortex project; review the audit and resolve required hardening first.

- Shipping update: live user authorized RED override and green-CI merge.
  PR https://github.com/PyAutoLabs/autolens_workspace_test/pull/329 opened
  at `c54fcf8`; all CI legs pending judgment. No later phase issued.

## Current state — phase 1a shipped, 2026-09-30

PR https://github.com/PyAutoLabs/autolens_workspace_test/pull/329 MERGED as
`bf3f7532ac780b682e64207c1a94394bbe5a1819`; issue #328 CLOSED.
All jobs in Actions run 36756347920 passed at `c54fcf8`, including Python
3.12 and 3.13 smoke. Live human authorized development-only Heart RED override
and merge on green checks; exact RED remained “release validation FAILED
(stage integrate)”. No release authorized.

Record: `complete/2026/09/point-solver-error-audit.md`. The task claim is released;
worktree removal and generated-artifact deletion were explicitly authorized.
The previous ship-blocked notes above are historical, not the current state.

Next: return to the parent phase-1 bug prompt for a bounded padding-default
fix/regression, then settle duplicate-image handling and containment overflow.
Phase 1 as a whole is NOT complete; phase 2 remains gated. No new issues queued.

## Phase 1b prepared — 2026-09-30

User approved the next padding-default fix with “go”. Filed the single bounded
plan `complete/2026/09/point-solver-padding-backend.md`: choose omitted
remove_infinities from resolved call-time xp; preserve explicit overrides;
NumPy and JAX regressions. No repo claims conflict. No issue or source edits.
Full Vitals refresh at 18:22:29Z reports RED “release validation FAILED
(stage integrate)”; await a task-specific development-only override. The
completed #328 grant does not carry over. No other phase prompts/issues queued.

Phase 1b authorized and issued as PyAutoLens#759. User granted the task-specific
RED development override; implementation on feature/point-solver-padding-backend.

## Phase 1b validation — 2026-09-30

PyAutoLens#759 now selects omitted padding from the effective call-time backend.
The new NumPy regression failed before the fix; the JAX override also failed
before the fix. All 12 constructor/backend/tracer combinations pass after it,
including registered-tracer JIT and explicit padding options. Full library and
workspace validation are running. Fresh main-checkout Heart at 18:35:14Z has
the authorized RED reason only: “release validation FAILED (stage integrate)”.
The prior blocked/prepared notes are historical. No merge or release authorized.

## Phase 1b PRs open — 2026-09-30

- Library: https://github.com/PyAutoLabs/PyAutoLens/pull/760 (`9c747c069`).
- Workspace: https://github.com/PyAutoLabs/autolens_workspace_test/pull/330 (`9cbcc37`).
- Both pending-release. Library merges first; workspace release-gate: PyAutoLens.
- Complete library rerun: 776 passed, 1 xfailed, 34 warnings. First attempt was
  terminated; no success inferred from it. Focused matrix 12/12 and smoke 32/32
  passed. Black/diff checks and in-session review passed.
- Live development-only RED override and validation recorded in issue #759,
  both PRs, active.md and autonomy_log.md. No merge or release authorized.

Current deliverable is these open PRs. Parent phase 1 remains incomplete:
next, after phase 1b ships, settle duplicate-image and containment-overflow
policy in the parent bug prompt. No later phase issue has been queued.

## Phase 1b merged — 2026-09-30

PyAutoLens#760 merged as `73dc5d275`; autolens_workspace_test#330 merged as
`7f75f6c2`, library first, after all seven GitHub jobs passed. Issue #759 closed.
Completion: `complete/2026/09/point-solver-padding-backend.md`; active claim
released. The PR-open/validation notes above are historical. PyAutoLens release
obligation retained in the completion record; no release authorized.

Next logical step remains bounded duplicate-image / containment-overflow policy
work within parent phase 1. Phase 2 remains gated; no further issue queued.

## Reconciliation and phase 1c plan — 2026-10-01

- GitHub confirms phase 1b merged: PyAutoLens#760 at `73dc5d275` and
  autolens_workspace_test#330 at `7f75f6c2`, on 2026-09-30. The latest
  completed subphase is 1b; numbered phase 1 remains incomplete.
- Cross-checked epics.md, all active.md entries, and open issues/PRs in
  PyAutoLens, PyAutoArray, PyAutoGalaxy, PyAutoNerves, autolens_workspace,
  autolens_workspace_test, autolens_profiling and HowToLens. No arc task is
  currently in flight. workspace_test#106 is separate cluster likelihood work;
  PyAutoGalaxy#641 and autolens_workspace#579 concern Scribbler. No adjacent
  DECISIONS/RESULTS file exists beside this ledger; shipped audit evidence is
  workspace_test `scripts/point_source/solver/RESULTS.md` and its JSON files.
- Next bounded step filed: `complete/2026/10/point-solver-duplicate-policy.md`
  (phase 1c). Reproduce the duplicate quad witness, test boundary and close-pair
  controls across backends, and establish a safe production policy before a
  library patch. The audit's distance grouping is explicitly diagnostic only.
- Brain FeatureDecision: direct research, autolens_workspace_test only; declared
  medium versus heuristic large. Scope is bounded to existing two fixtures,
  CPU diagnostics and a policy report; no production algorithm/default change.
  Memory consultation included the prior CPU campaign's accepted vertex-tie
  witness and capacity finding. Conflict guard passes. Workspace main is clean
  but six commits behind origin/main; use fresh main during setup.
- Heart entry feed: STALE, "test run status unknown (no report.json)"; planning
  may proceed. Plan is awaiting explicit approval under start_dev/AGENTS.md.
  No phase issue or implementation worktree has been created, no tests/source
  edited, and no later phase issue queued. The separate Mind worktree holds
  planning records only.
- Next after approval: create_issue for this single task, start_workspace,
  implement the evidence cell, then ship_workspace. Containment-overflow policy
  remains in parent phase 1; phase 2 stays gated. Cortex's project ledger and
  R-20260907-05 still record phase 11 as dropped; no successor is implied.

## Phase 1c issued — 2026-10-01

User approved the detailed plan with "I approve". Only issue
https://github.com/PyAutoLabs/autolens_workspace_test/issues/331 was opened.
Prompt: `complete/2026/10/point-solver-duplicate-policy.md`. Workspace worktree:
`/home/jammy/Code/PyAutoLabs/.worktrees/point-solver-duplicate-policy`, branch
`feature/point-solver-duplicate-policy`, base `7f75f6c2`. Heart entry STALE;
conflict guard clear. Implement duplicate-policy evidence then ship_workspace.

## Phase 1c validated, awaiting development ship gate — 2026-10-01

- #331 has a complete local research deliverable (54 scalar rows + 6 vmap
  controls): `scripts/point_source/solver/{duplicate_policy.py,
  duplicate_policy_evidence.json,DUPLICATE_POLICY.md}` in its task worktree.
- Decision: NO-GO for promoting distance/shared-edge/root-polishing heuristics.
  They repair the 36 quad rows, but all 18 near-cusp rows exceed cap 20;
  uncapped counts reach 87. Fine NumPy finds four images where eager/JIT JAX
  find three (observed after capped selection; no sole-cause cap-size A/B).
  Grouping independent true roots by 2×precision can collapse four to two.
- Recommended next bounded library work: observable containment-overflow
  contract, then revisit image identity on capacity-clean close-pair evidence.
  This refines the prior ordering; no new follow-up issue has been created.
- Validation: full smoke 32/32; padding matrix 12/12; image-plane/JIT regression,
  saved-matrix and analytic reference checks, Black/compile/JSON/diff checks
  and in-session review passed. No production code changed.
- Current blocker: Heart RED "release validation FAILED (stage integrate)".
  Work remains local/uncommitted on `feature/point-solver-duplicate-policy`;
  no PR yet. Await a live development-only RED override for #331, then
  ship_workspace. No merge/release authorized. Details and logs in active prompt.
- Last shipped subphase remains 1b. Phase 1c is validated but NOT shipped;
  parent phase 1 remains incomplete and phase 2 gated. Cortex unchanged.

## Phase 1c Fable review and PR open — 2026-10-01

Independent `claude-fable-5-1` review initially returned FINDINGS; all six
resolved, then re-review CLEAN (session
`2eb5a6d4-323e-4a3f-bd9b-6506a6de2b0f`). This supersedes the earlier inference
that close-pair work should simply wait for capacity-clean evidence: NumPy
is uncapped and already exhibits substantial image-position errors near the
cusp. Small residuals also let root polishing accept inaccurate positions.
The report now separates these accuracy/identity problems from JAX truncation,
adds per-root coverage and polishing errors, and makes summarize read-only.

Final exact-script rerun: 54 scalar + 6 vmap; script SHA pinned, explicit
before/after library/environment/script provenance PASS. 18 rows exceed JAX
capacity 20, but only 12 JAX rows truncate; four resolved untruncated NumPy
controls fail each rule. All 36 quad rows meet the grouping criterion. Existing
padding 12/12, image-plane/JIT, smoke 32/32, Black/compile/JSON/diff pass.
One rerun failed provenance because the shared activation symlink was clobbered
by another task and its bundle removed; discarded, then rerun successfully
with a task-owned activation file. Final log: task scratch/duplicate-policy-final-stable.log.

User "ok review with fable" granted the requested development-only override
for #331 with review first. Heart RED remained exactly "release validation
FAILED (stage integrate)" at 2026-10-01T08:46:35.028848+00:00. Recorded on issue,
PR, active.md and autonomy_log.md. PR
https://github.com/PyAutoLabs/autolens_workspace_test/pull/332 is open at
`2941721`, labelled pending-release. No merge/release authorized. Last shipped
subphase remains 1b; 1c is PR-open, parent phase 1 incomplete, phase 2 gated.
Do not repeat successful validation without changed inputs or a new concern.

## Phase 1c merged and closed — 2026-10-01

This entry supersedes the historical local-only / PR-open states above.
Human `/prm` authorized merge after all three GitHub jobs passed on 2941721.
autolens_workspace_test#332 merged at 13c9d1ff58b56716f63766e6409a9ee8e870f95f;
issue #331 closed. Completion: `complete/2026/10/point-solver-duplicate-policy.md`.
Independent Fable CLEAN; final 54 scalar + 6 vmap/provenance, padding 12/12,
image-plane/JIT and smoke 32/32 passed. Research verdict remains NO-GO for the
tested grouping heuristics: uncapped NumPy accuracy/identity failures and JAX
truncation require separate contracts. Last completed subphase is now 1c.
Parent phase 1 remains incomplete; phase 2 gated; no later issue queued.
Next bounded plan must use the shipped report to distinguish conditioning-aware
image-position accuracy/identity from observable containment overflow. No
production default or capacity change was shipped. No release authorized.
The phase-1b PyAutoLens pending-release obligation remains in its own record.
Cortex phase 11 stays dropped under R-20260907-05; no science project born.


## Phase 1d prepared — 2026-10-01

Reconciled fresh Mind main with GitHub: latest completed subphase is 1c,
workspace_test#332 merged 13c9d1f, #331 closed, all three CI jobs SUCCESS.
No arc task is active and no adjacent DECISIONS/RESULTS files exist. Checked
open issues/PRs in PyAutoLens, PyAutoArray, PyAutoGalaxy, PyAutoNerves,
autolens_workspace, autolens_workspace_test, autolens_profiling and HowToLens.
workspace_test#106 remains separate cluster-likelihood work; Array#600 claims
PyAutoArray for streaming phase 5. Cortex ruling R-20260907-05 remains in force.

Next bounded prompt: `complete/2026/10/point-solver-image-accuracy.md`
(phase 1d). Use the shipped report's uncapped NumPy counterexamples to trace
image-position accuracy and test conditioning-aware diagnostics against its
independent root reference. This progresses a separate necessary contract
while Array is claimed; it does not resolve or defer away overflow observability.
Only autolens_workspace_test will be edited. No production changes proposed.
Brain FeatureDecision: direct research, declared medium / heuristic too-large
(score 11). Retain medium because the scope is two existing fixtures, CPU fp64,
a bounded three-level refinement extension and one evidence/report cell; API,
gradient, GPU and general-lens completeness work are excluded. Memory consulted.
Workspace main clean, eight commits behind origin/main; fresh-main setup planned.
Conflict guard passes. Proposed branch feature/point-solver-image-accuracy.

Entry feed was STALE; full Vitals at 2026-10-01T09:18:46.359669+00:00 is RED:
- release validation FAILED (stage integrate)
Additional readiness reasons:
- workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)
- manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml

Await explicit approval of the filed plan and a task-specific development-only
RED override before issue creation/start_workspace. Previous overrides applied
to completed tasks only. No phase-1d issue, implementation worktree or source
edits; no later phase queued. Parent phase 1 incomplete; phase 2 gated.

## Phase 1d issued — 2026-10-01

User “I approve” granted the plan and task-specific development-only RED override. Only autolens_workspace_test#333 issued; prompt complete/2026/10/point-solver-image-accuracy.md. Worktree .worktrees/point-solver-image-accuracy, branch feature/point-solver-image-accuracy at 13c9d1f. Implement and validate through PR creation; no merge/release authorized.


## Phase 1d PR open — 2026-10-01

Implemented and validated autolens_workspace_test#333; PR
https://github.com/PyAutoLabs/autolens_workspace_test/pull/334 open at
`4bec6a72a20659dca5bd08c8348142ab2c64d5c4`, labelled pending-release.
Files: scripts/point_source/solver/{image_accuracy.py,
image_accuracy_evidence.json,IMAGE_ACCURACY.md}. No production changes.

Final exact-script matrix: 32/32 CPU fp64 rows, zero resource limits,
geometry correspondence 32/32, before/after script/helper/library/environment
provenance PASS. 10/32 raw rows miss per-root coverage; three non-converged
polished candidates falsely pass the conditioning screen, one in a resolved
reference-pair row. Requiring convergence removes all three false accepts but
covers only one or two of four images in every closest-cusp row. NO-GO for
production promotion; neither extra refinement nor this local correction
screen establishes safe image identity. See report for the exact counterexample.

Validation: saved-matrix/read-only summary, coordinate-metric recomputation,
four corrupt-evidence controls and empty-candidate controls PASS; existing
padding 12/12, image-plane/JIT PASS; full workspace smoke 32/32; Black,
compile/JSON/diff checks and in-session review PASS (not independent review).
Logs: .worktrees/point-solver-image-accuracy/scratch/{image-accuracy-final.log,
evidence-validation.log,summary.log,padding.log,image-plane.log,smoke.log,
review.md,vitals.log,readiness.json}. Task-owned activation avoids shared-link
clobbering. Earlier development passes are not the shipped evidence.

Live user “I approve” authorized the plan and task-specific development-only
Heart RED override through PR creation. Ship-time readiness re-read at
2026-10-01T10:10:03.098482+00:00 retains “release validation FAILED (stage integrate)”.
Additional reasons unchanged: “workspace validation not passing (0 failed, 1 timeout, cloud#36404726969: autolens_test scripts/multi_dataset/rectangular.py)”;
“manifest drift: public front-door organ tables (generated) — 1 mismatch(es) vs PyAutoMind/repos.yaml”.
Recorded on issue, PR, active.md and autonomy_log.md. No merge/release authorized.
GitHub changes gate passed; Python 3.12/3.13 smoke queued at handoff.
Last completed subphase remains 1c; 1d awaits review/merge. Phase 1 remains
incomplete; phase 2 gated; no later issue queued. Next production scope is an
observable containment-overflow contract once Array's claim clears, with
separate accuracy/identity work still required. Cortex phase 11 stays dropped.

## Phase 1d merged — 2026-10-01

Human `$prm` authorized merge after all three jobs in run 36847665642 passed
at 4bec6a7. PR autolens_workspace_test#334 MERGED as
26da5b1458490fbf0f01d4c5d4a7e7c99eee3fc4; issue #333 CLOSED.
Completion: complete/2026/10/point-solver-image-accuracy.md; active claim released.
Earlier PR-open statements are historical. Last completed subphase is 1d;
NO-GO findings retained, parent phase 1 incomplete and phase 2 gated.
No later issue queued, no release authorized; Cortex phase 11 stays dropped.
The prior streaming #600 Array claim is closed; recheck all claims at the next
start_dev before planning the observable-overflow contract.

## Human-approved extraction — 2026-10-01

User request (verbatim):

> Ok  I agreem autolens_profiling is evolving into "make autolens fast" but also "these are the settings I need to ensure the analysis is robust" so this work is also more and more belonging there, albeit we need numerical integration tests in autolens_workspace_test which ensure this all makes it way into CI. Update accordingly and then wrap up

Applied to campaign ownership, phase prompts and dependencies. No production
code moved, no new issues queued, no release or Cortex project authorized.

## Retired from epics.md (2026-10-01)

## cluster-strong-lensing
- title: Cluster strong lensing — Source & Cluster arc
- ledger: draft/feature/autolens/source_cluster_arc.md
- status: Completed evidence/fixes 1a–1d (latest workspace_test#334, 26da5b1; #333 closed). On 2026-10-01 the human transferred remaining phase-1 repairs, phase-2 profiling and forward ShapeSolver work from phase 6 to cluster-pointsolver-speed (robustness and performance). Transferred is not solved. Blanket PointSolver gate removed; next arc step is phase 3 critical-curve dispatch, sliced via start_dev. Supplied-coordinate magnification and pixel-based areas can proceed; solver-discovered images and solver-dependent inference retain workload-specific correctness gates. Cortex phase 11 stays dropped under R-20260907-05; phase-1b PyAutoLens pending-release obligation retained.
- notes: Original phase numbers retained for history; phases 1 remainder and 2 transferred, phase 6 narrowed. Issue ONE bounded phase at a time as predecessors near shipping; no bulk queue. autolens_profiling owns robustness/settings/performance evidence; autolens_workspace_test owns numerical integration regressions wired into CI. Science project birth still requires a fresh explicit Cortex decision.

## Reconciliation and phase 3a plan — 2026-10-02

Restored the canonical draft ledger and epics.md entry. Automation commit
5c0dea2e retired this unfinished epic because its status opened with
"Completed evidence/fixes" and lifecycle.py matches the COMPLETE prefix.
The retirement was not a human decision to finish the arc. Historical retirement
text above is retained; current status now starts "In progress".

GitHub confirms latest completed subphase 1d: workspace_test#334 MERGED as
26da5b1458490fbf0f01d4c5d4a7e7c99eee3fc4; #333 CLOSED. No current arc claim
in active.md and no matching open phase issue/PR across PyAutoLens, PyAutoArray,
PyAutoGalaxy, autolens_workspace, autolens_workspace_test, autolens_profiling,
and HowToLens. workspace_test#106 is separate cluster-likelihood work;
Galaxy#641 and workspace#579/#583 are Scribbler; profiling#359/#360 is Pulse.
No adjacent DECISIONS/RESULTS files found at either ledger location.

Phase 3 is next under the approved ownership split. Current-source read shows
that the duplicate plot/plot_utils.py no longer exists; util/plot_utils.py is
canonical. Static config dispatch, wrong default docstrings, and cluster
bypass remain. The zero-contour wrapper constructs NumPy/list outputs, so
internal JIT and an externally jittable plotting API must be distinguished.
Do not implement the old automatic-JIT proposal from historical timings alone.

Filed one bounded research prompt:
complete/2026/10/critical-curves-dispatch-audit.md (phase 3a).
Evidence first: current dispatch/call boundaries, two synthetic fixtures,
per-source-plane curve/caustic geometry, bounded cold/warm/disabled-JIT timings,
and an explicit dispatch contract. Production/default changes remain phase 3
follow-up work; no further prompts or issues queued.

Heart entry GREEN (feed updated 12h ago). Workspace main clean; active-claim
guard clear. Proposed feature/critical-curves-dispatch-audit; implementation
worktree only after plan approval. No issue or implementation edits yet.
Cortex projects/inference_programme.md and R-20260907-05 retain phase 11 as
DROPPED; no implicit science-project birth or revival.

## Concurrent unissued implementation proposal — 2026-10-02


The old `draft/feature/autolens/source_cluster_arc.md` path was retired by Mind's
epic lifecycle; this archived file is the live arc ledger. No adjacent
DECISIONS/RESULTS file exists. Confirmed workspace_test#334 merged and #333
closed; PyAutoLens#760 merged and #759 closed. No related phase-3 open issue or
PR appears in the affected repos, and no active.md row claims its repos. The
old phase-1 remainder and phase-2 profiling remain transferred, not complete.
The Cortex phase-11 task remains dropped under R-20260907-05.

The next arc work is phase 3. Current source invalidates one historical defect:
`autogalaxy/plot/plot_utils.py` is gone, leaving one
`autogalaxy/util/plot_utils.py`. The config selector still defaults to marching
squares; PyAutoLens cluster plots still call marching-squares LensCalc methods
directly for each plane. Filed the first bounded subphase at
`draft/feature/autolens/cluster_curves_engine_dispatch.md` to make those plots
honor configured engine selection while preserving multi-plane geometry.
Brain classifies that slice as a direct library feature (declared medium,
heuristic large); Heart entry feed GREEN, conflict guard clear. Plan and branch
name await human approval. No issue or implementation worktree has been created,
no source edited, and no later phase issue queued. Context-aware JIT dispatch,
doc fixes and cluster-scale performance/accuracy remain phase-3 work.

## Approved sequence — 2026-10-02

Human “go” in this session approves critical_curves_dispatch_audit (phase 3a).
The concurrent cluster_curves_engine_dispatch draft has no issue or approval
record; preserve it as an implementation candidate to reconcile after the audit.
Its historical phase-3a label does not authorize a second issue. The canonical
ledger is restored under draft/; the archived-location statement above is
superseded. Only the approved audit is issued now.

Phase 3a issued as autolens_workspace_test#337 after human approval “go”.
Workspace branch feature/critical-curves-dispatch-audit; implementation and
validation in progress. Heart entry GREEN. No merge/release authorized.

## Research ownership clarified — 2026-10-02

Human directed phase-3 research into autolens_profiling, building a cumulative
wiki as experiments accumulate, with bounded CI examples in workspace_test.
Phase 3a issue #337 now covers both repos; no extra issue. Concurrent separate
scope alongside profiling#361 explicitly authorized. Research: lens/critical_curves
and linked results/wiki. CI: cluster/critical_curves.py in required smoke.
Initial audit found fixed ±3 arcsec auto seeds miss cluster components, the
far-source explicit path is incomplete at default tracing budget, outer-JIT
list wrappers fail, and the capped evaluation-grid formula changes field extent.
Final evidence and PRs pending; no production fix or phase completion claimed.


## Phase 3a evidence — 2026-10-02

Research implemented in autolens_profiling/scripts/lens/critical_curves/dispatch.py,
results/notes/critical_curves_dispatch.md, versioned JSON/PNG and the indexed
wiki/campaigns/critical_curves.md. Small independent analytic per-plane CI example
implemented in autolens_workspace_test/scripts/cluster/critical_curves.py and its
required smoke list. Both task worktrees remain feature/critical-curves-dispatch-audit.

Pinned CPU fp64 matrix: 14 workers, four 120s timeouts retained as incomplete,
with partial quantities preserved. All marching-squares controls/convergence
checks pass. Automatic seeds miss cluster components; explicit far-source
critical curve has a 20.65 arcsec closing chord and 6.16 arcsec reference distance.
A near-reference caustic cannot rescue its invalid parent curve. Outer-JIT list
wrappers raise NonConcreteBooleanIndexError. Capped grid witness expands a
60 arcsec field to ~8333 arcsec; selector-only dispatch remains NO-GO.
Next candidate is one bounded field-preserving grid-cap fix, not yet issued.

Measured driver hash is archived alongside the evidence. Post-processing fixed
CPU-device validation (TFRT_CPU_0), recording separate collector provenance and
verifying identical numerical ASTs; no measurement rerun/replacement. Read-only
validation and four corrupt-evidence controls pass. Profiling suite: 1002 passed,
5 skipped; lint/wiki/results/dashboard checks pass. New CI example passed both
source JAX 0.10.2 and isolated JAX 0.11.2; existing zero-contour example passed.

Initial full smoke attempt timed out existing delaunay.py and delaunay_mge.py at
300 seconds under concurrent host load, then was stopped. One sequential retry
is in progress; its first script passed (165.2s). No PR or phase completion yet.
Heart GREEN does not waive the full smoke gate. No source/library default changed,
no later issue queued, no Cortex project revived.


## Shipping checkpoint — 2026-10-02

Heart refreshed at 2026-10-02T09:49:31.721134+00:00 returned RED, score 45:
`PyAutoFit: 1 commit(s) behind origin`; `PyAutoGalaxy: 1 commit(s) behind origin`;
`PyAutoLens: 1 commit(s) behind origin`. These are release Colab-link updates.
Also YELLOW: `manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml`.
STALE: `release validation incomplete: no rehearsal for current source`.

Ship-workspace therefore stopped before PR creation. Full smoke retry passed
five scripts (Delaunay, Delaunay MGE, rectangular, MGE, LP), then our process tree
was stopped at the Heart gate; remaining smoke scripts unrun. The small new
example independently passed both runtimes. Profiling 1002 passed/5 skipped,
artifact negative controls and lint/docs checks remain valid.

Both implementation worktrees are uncommitted and preserved under
.worktrees/critical-curves-dispatch-audit/ on feature/critical-curves-dispatch-audit.
Scratch holds raw workers/logs/PR drafts; profiling results hold frozen measured
source, JSON/PNG and the cumulative research ledger/wiki. No job remains running.
Resume: resolve Heart via the normal workflow, complete full workspace smoke,
then ship both companion PRs for #337. No successor issue or phase completion.


## Resume authorized — 2026-10-02

Human requested "prm and continue", authorizing the two phase-3a PR merges when
all CI passes. No PR yet; resume ship-workspace first. Library-behind RED reasons
have cleared. Human explicitly acknowledged the remaining Heart YELLOW reason:
`manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml`
(the separately active PyAutoPulse registration). Full smoke is running again;
profiling fast-forwarded unrelated merged PR #361 and its changed test passed
46 cases. No measurement evidence was altered. Next cap-fix plan is prepared in
task scratch, unissued pending predecessor shipping/review.


## Phase 3a PRs opened — 2026-10-02

Research: autolens_profiling#364 @89b6d00; CI: autolens_workspace_test#341 @06f7b8f.
Full workspace smoke 33/33 passed (new example 2.9s). Heart YELLOW acknowledged;
all RED reasons cleared after clean canonical PyAutoLens fast-forward. Both PRs
pending-release, cross-linked; /prm awaiting all workflow/matrix legs.
Next single prompt filed, unissued: phase 3b cap fix (now recorded at
complete/2026/10/evaluation-grid-cap-field.md). Includes explicit effective-Zoom2D footprint/rounding contract; does
not silently absorb the independent masked-caustic discrepancy draft. No bulk queue.


## Phase 3a merged; phase 3b approved — 2026-10-02

Both PRs merged after all exact-head CI jobs passed: profiling#364 (97f24eb),
workspace_test#341 (121f9b9). Issue #337 closed; completion record
complete/2026/10/critical-curves-dispatch-audit.md replaces its active prompt/claim.
Evidence worktree retained by explicit human request; no cleanup deletion.
Human approved phase 3b plan plus separate-scope concurrency on Galaxy,
workspace_test and profiling. Next: issue the one filed cap-fix prompt and enter
start_library; no additional successor queue. Original overall phase 3 remains open.

Phase 3b issued: PyAutoGalaxy#645, feature/evaluation-grid-cap-field in the
isolated task bundle. Approved concurrency recorded; implementation underway.


Phase 3b implementation: corrected capped physical spacing and both-axis limit,
with conservative subpixel padding and unchanged existing zoom centre/mask policy.
Before: six new test failures; after: 49 focused and 1315 full Galaxy tests pass.
Same probe now spans 60 arcsec at 0.06 arcsec/pixel. Human acknowledged the two
current Heart YELLOW map/table drift reasons and authorized shipping. Library PR
creation and linked workspace smoke underway; no next phase issued.

Phase 3b library PR: PyAutoGalaxy#646 (f19a3377), pending-release. Linked
workspace CI and profiling-ledger changes are prepared; full smoke running.


## Phase 3b shipped to PRs — 2026-10-02

- PyAutoGalaxy#646 @f19a3377: field-preserving cap; all exact-head CI green.
- autolens_workspace_test#343 @fcd6bd5: draft required-CI invariant, waiting for
  a library dependency containing the fix; library-first/release gate retained.
- autolens_profiling#365 @d8a46c3: cumulative before/after ledger/wiki.

Full Galaxy tests 1315 passed; focused 49 passed; full companion smoke 33/33
in 501.91s, new cap example 2.2s. Same cap probe records 60 arcsec field at
0.06 arcsec/pixel; original phase-3a artifacts unchanged. Exact current Heart
map/table YELLOW reasons acknowledged. Issue #645 remains open, active task
retained, all worktrees clean and available for review. No phase-3b merge or
release performed. No later phase issued. Phase 3a evidence worktree retained
as explicitly requested; its claim/issue closed and dashboard regenerated.

Next handoff: review/merge the library fix and research PR when green; release
availability then permits the draft workspace regression to pass installed-stack
CI and merge. Only after this phase nears completion should seed/path coverage
be scoped as the next single issue. Separate masked-caustic prompt remains open.


## Phase 3b merged — 2026-10-04

All three PRs merged: PyAutoGalaxy#646 (2e36de4e, 2026-10-02; released in
2026.10.4.1), autolens_profiling#365 (9d0b1317, 2026-10-02) and
autolens_workspace_test#343 (ebb9c866, 2026-10-04). Issue #645 closed via /prm.
Record: complete/2026/10/evaluation-grid-cap-field.md. No later phase issued;
seed/path coverage remains the next single-issue candidate, and the separate
masked-caustic prompt is still open.

## New child filed: cluster fit visualizer — 2026-10-18

Filed from the Pulse `cluster-pointsolver` chat (autolens_profiling#436 pilot running as RAL job
412567). `draft/feature/autolens/cluster_fit_visualizer_cluster_wide_model_fit.md` is a new child
of this arc (Epic cluster-strong-lensing), NOT phase 8: phase 8 remains magnification maps only.
It depends only on shipped phase 3. Scope: a cluster-aware model-fit visualizer (cluster-wide
model-vs-observed positions figure, per-plane critical curves, per-system zooms with cluster-scale
defaults) reusing `autolens/cluster/plot/cluster_plots.py` and absorbing the unfiled
PyAutoLens#577 follow-ups. Paired Eyes surface:
`draft/feature/autolens_visualization/eyes_cluster_visualization_group_render_every_cl.md`.
The campaign's oracle-verification figure stays in autolens_profiling (measurement artefact).
Human note 2026-10-18: galaxy-scale visualization defaults "will look awful on cluster scales";
expect bespoke figures or updated tool defaults. No phase issued by this note.

## Reconciliation and phase 5a plan — 2026-10-23

- Last completed phase: 3b (merged 2026-10-04; `complete/2026/10/evaluation-grid-cap-field.md`).
  Nothing in flight: no active.md row, no open arc issue/PR in PyAutoLens, PyAutoArray,
  PyAutoGalaxy, autolens_workspace, autolens_workspace_test, autolens_profiling or HowToLens
  (workspace_test#106, PyAutoArray#377, profiling#128 are unrelated). No DECISIONS/RESULTS
  file beside this ledger. Phase 11 stays dropped (R-20260907-05).
- Phase 3 remainder (`draft/feature/autolens/cluster_curves_engine_dispatch.md`: cluster plots
  honor the configured engine; its `Phase: 3a` label and archived-parent path are stale and
  need relabelling to 3c before issue) is DEFERRED, not dropped: phase 3a found the
  `zero_contour` engine's automatic seeds miss cluster components, so routing cluster plots to
  that engine is entangled with seed-coverage robustness, which the human has moved to separate
  issues (2026-10-23: optimisation, profiling and robustness are separate; not this arc's focus).
- Next step chosen: **phase 5** (magnification at a point). It has no intra-arc gate, is
  high priority, is pure magnification science, and phases 6–8 depend on it. Brain Feature
  Agent: feature/autolens, library workflow, declared large / derived too-large →
  split-into-phases. Sliced into 5a (library, PyAutoLens only) and 5b (workspace
  `source_science.py` docs + multi-plane example, after 5a is pending-release).
- Filed `draft/feature/autolens/point_magnification_signed_surface.md` (phase 5a): signed
  per-image magnification accessor with the unsigned default unchanged, `ResultPoint`
  magnification accessors, multi-plane `plane_j` witness and parity witness. The parent's
  stale `Tracer.magnification_2d_from` claim is already gone from source; recorded, no edit.
- Heart at the door: GREEN (release GREEN; monitoring RED on dirty canonical checkouts and
  worktree drift). Conflict guard clear for PyAutoLens; main clean at `b273f9c7d`.
  Proposed branch `feature/point-magnification-signed-surface`. Plan awaits human approval;
  no issue, worktree or source edit yet; no later phase queued.
- Human approved the 5a plan 2026-10-23 ("sounds good") and directed that the feature be
  documented in autolens_workspace for users: `source_science.py` AND a guide. Phase 5b scope
  therefore = source_science.py (both tiers) + `guides/lens_calc.py` + `guides/advanced/multi_plane.py`
  + point-source `guides/results/` surface. Recorded in the 5a prompt; 5b prompt filed after 5a ships.

Phase 5a issued as PyAutoLens#797 (2026-10-23) after human approval; prompt moved to
`active/point_magnification_signed_surface.md`; claim registered in active.md on
`feature/point-magnification-signed-surface`. Entering start_library; execution delegated to Opus.

## Phase 5a implemented, awaiting Heart YELLOW acknowledgement — 2026-10-23

Opus worker implemented PyAutoLens#797 in the task worktree; Fable reviewed the diff, moved a
misplaced docstring paragraph, and restored `dataset.py` to base plus the docstring edit after
black reformatted it. Committed locally on `feature/point-magnification-signed-surface` (not
pushed). Full suite 941 passed / 1 xfailed; focused point tests 308 passed / 1 xfailed; black
clean on changed files. No workspace consumer of the accessor (ship option iii). Heart YELLOW:
`manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml`
and `release validation incomplete: no rehearsal for current source`. Stopped for the human's
acknowledgement; next: push, PR (judge tier, human /prm), smoke_test, then file phase 5b
(source_science.py both tiers + guides/lens_calc.py + guides/advanced/multi_plane.py +
point-source results guide).

Human acknowledged both YELLOW reasons and authorized /prm on green, then phase 5b under --auto
(2026-10-23). PR https://github.com/PyAutoLabs/PyAutoLens/pull/798 @6cb5eed0f, pending-release.

## Phase 5a merged — 2026-10-23

PyAutoLens#798 merged as `f791ac77d` after all CI jobs passed (docs, unittest 3.12/3.13/nojax)
and autolens_workspace_test smoke 37/37 against the branch. Issue #797 closed via /prm.
Record: `complete/2026/10/point-magnification-signed-surface.md` (pending-release PyAutoLens#798).
The 5a prompt now lives in that record; the filed/active paths above are historical.
Human direction 2026-10-23: "prm and then auto mode do all of phase 5" → phase 5b
(`draft/docs/autolens_workspace/point_magnification_workspace_docs.md`, Difficulty medium,
Autonomy safe, Consequence glance with Witness) is launched next under `--auto`. No other phase
queued; phase 3 remainder stays deferred; phase 11 stays dropped.

## Phase 5b queued (claim conflict) — 2026-10-23

Issued as https://github.com/PyAutoLabs/autolens_workspace/issues/596; Brain Feature Agent: docs/autolens_workspace,
workspace workflow, direct (declared medium). Heart GREEN. Conflict guard: autolens_workspace is
claimed by `assistant-ai-options-page` (PyAutoScientist#87; its workspace branch has no commits
yet), so 5b is registered in planned.md as blocked, not started. Human --auto authorization for
phase 5 is recorded on the planned row; when the claim is released, run /start_dev on the prompt
with --auto (effective safe, tier glance) → start_workspace → ship_workspace. No source edits.

## Phase 5b started under --auto — 2026-10-23

Human: "start 5b now i doubt theres much clash" → autolens_workspace claim released from
assistant-ai-options-page (branch had no commits; note left on its row). 5b promoted
planned → active (ws#596), worktree feature/point-magnification-workspace-docs. Effective
autonomy safe, tier glance: ships through the four-leg autonomous gate, auto-merges on green if
the Witness passes; PR pending-release until PyAutoLens#798 is released.

## Phase 5b PR open — 2026-10-23

autolens_workspace PR https://github.com/PyAutoLabs/autolens_workspace/pull/598 @51b9a898 (ws#596).
Four-leg gate: tests n/a (15/15 edited scripts run clean); smoke curated autolens 43/43; independent
Fable review CLEAN (Opus-authored branch; four claims basis-cited); Heart YELLOW 85 within ack —
the new reason `release validation stale: source moved since rehearsal (PyAutoLens)` acknowledged by
the human at PR-open. Witness PASS. Calibration row appended to autonomy_log.md. Glance tier →
in-turn CI watch then /prm merge + close-out. Release-gate: PyAutoLens#798 unreleased (the two
point_source scripts use its accessors). Review side-finding for a later one-liner: PyAutoGalaxy
`lens_calc.py` docstring of `magnification_2d_via_hessian_from` says `abs(...)` but returns signed.

## Phase 5b merged; phase 5 complete — 2026-10-23

autolens_workspace#598 merged as `0f8b4db5a` under the glance tier after all CI green (size guard,
navigator ×4, smoke 3.12/3.13 at 51b9a898). Issue #596 closed. Record
`complete/2026/10/point-magnification-workspace-docs.md`; shadow row appended (merged-unchanged,
stage 1). Release gate: PyAutoLens#798 unreleased (two point_source scripts). Phase 5 (5a + 5b)
COMPLETE. No later phase issued. Next candidates, one at a time: phase 4 (mesh magnification
correctness tests), phase 6 (LEGGOS area magnification; nominal gates 3 and 5 — phase 3 remainder
deferred, needs a human call on whether 6 may proceed on marching-squares only), or the deferred
phase-3 engine-dispatch slice. Phase 11 stays dropped.

## Wrap-up — 2026-10-23

Review side-finding fixed: PyAutoGalaxy PR https://github.com/PyAutoLabs/PyAutoGalaxy/pull/657
(docstring-only; `magnification_2d_via_hessian_from` documents signed 1/det(A); pending-release;
human "do the quick thing" authorized ship + merge on green). PyAutoLens 2026.10.23.1 was released
at 12:11Z today and contains #798 (`f791ac77d`), so the 5a pending-release obligation is satisfied
by that release; clearing the key is /review_release's act, not recorded here.

Galaxy#657 merged 2026-10-23 (docstring only); pending-release PyAutoGalaxy until its next release.

2026-10-28 — phase-3a subtask `cluster-curves-engine-dispatch` issued as PyAutoLens#807 (cluster plots honour the configured critical-curve engine); in library-dev.
2026-10-28 — `cluster-curves-engine-dispatch` shipped as PyAutoLens#808 (pending-release); awaiting human /prm. Limit for the remaining phase-3 scope: `zero_contour` seeds only from LensCalc's ±3" coarse scan, so cluster-scale curves outside it are not drawn.
2026-10-28 — `cluster-curves-engine-dispatch` MERGED: PyAutoLens#808 (`1faa99a`, CI green on a0666e7); #807 closed; record `complete/2026/10/cluster-curves-engine-dispatch.md` (pending release). Remaining phase-3 scope unchanged, plus the zero_contour ±3" seeding limit at cluster scale.
2026-10-28 — CORRECTION (session_016nhQ8NtZ6QtuqxKKAnhhdg): `cluster_curves_engine_dispatch` was issued (PyAutoLens#807) and merged (PyAutoLens#808) from the Feature Agent's backlog pick WITHOUT reading this ledger, which marked it DEFERRED (lines above: "Phase 3 remainder … is DEFERRED, not dropped" — entangled with zero_contour seed-coverage robustness, moved to separate issues by the human 2026-10-23) and its `Phase: 3a` label stale (should have been 3c). Impact: default `marching_squares` behaviour is unchanged; with `zero_contour` configured, cluster curves outside LensCalc's ±3" seed box are silently not drawn (documented in the docstrings) — exactly the entanglement the deferral named. Not reverted; revert (`git revert -m 1 1faa99a` on PyAutoLens main) or keep is the human's call. The seed-coverage robustness work remains separate and unissued.
2026-10-28 — human ruled KEEP for PyAutoLens#808 (cluster plots honour the configured engine; zero_contour ±3" seeding limit documented). No revert. Seed-coverage robustness stays separate and unissued.
2026-10-28 — Phase 4a issued as PyAutoArray#659 (now `complete/2026/10/mesh-magnification-areas.md`, child of the phase-4 prompt): per-mesh `areas_for_magnification` correctness tests on all 8 meshes + autolens_workspace_test area + magnification integration check. Human launched with --auto ("make sure we have a robust integration test or sanity check in autolens_workspace_test … area but also magnification values"); effective supervised → ends at PR-open, judge → human /prm. Re-audit: rectangular lead likely closed by PyAutoArray#608; NN/KNN inherit Delaunay dual areas (untested approximation); `areas_for_magnification` now consumed by PyAutoLens `analysis/latent.py`. 4b (library flux-ratio μ) and 4c (source_science recovery sweep) not issued.
2026-10-29 — Phase 4a (PyAutoArray#659) extended before PR-open by human pick "Fix adaptive rect first": adaptive rectangular `areas_for_magnification` now exact per-axis hat quadrature (`adaptive_rectangular_hat_areas_from`; numpy = JAX to 1e-14, grad finite). Lensed workspace check vs simulator truth: all four adaptive meshes within 0.61% lensed / 0.49% identity (were up to +14.43% / +11.23%); tolerances tightened to 1% (RTUAdaptDensity lensed 3%, -1.82% unchanged by areas). Old midpoint areas also zeroed a live bottom row on coarse meshes; fixed as a side effect. Phase 4b re-scoped to KNN / KNNBarycentric only. Branch rebased on main; not yet pushed.
2026-10-29 — Phase 4a PRs OPEN: PyAutoArray#664 (RectangularUniform + adaptive rectangular exact areas, per-mesh tests) and autolens_workspace_test#348 (simulator-truth integration check; merge after #664). Heart GREEN; full Array suite 2251 passed; targeted smoke 5/5. Awaiting human /prm (judge).
2026-10-29 — Phase 4a MERGED + CLOSED via /prm: PyAutoArray#664 (`7fb38053`, pending release) and autolens_workspace_test#348 (`6a7990d5`); #659 closed; record `complete/2026/10/mesh-magnification-areas.md`. Next: phase 4b (KNN / KNNBarycentric exact areas, `draft/feature/autoarray/mesh_magnification_exact_quadrature_areas.md`), or phase 6 (LEGGOS) — human pick, one at a time.
2026-10-29 — Phase 4b issued as PyAutoArray#665 (now `complete/2026/10/mesh-magnification-knn-areas.md`): KNN / KNNBarycentric exact quadrature areas + fix #609 partial-block neighbour search (found to corrupt KNN interpolation; folded in). Phase 6 queued after 4b per human "do both", one at a time.
2026-10-29 — 4b re-scoped by human: #609 split back out (fix breaks jax_grad/knn.py KNN+AdaptSplit gradients; finding + patch on #609, prompt re-sized medium/judge). 4b = exact KNN / KNNBarycentric areas only.
2026-10-29 — Filed phase 4e docs prompt `draft/docs/autolens_workspace/pixelization_source_science_py_document_mesh_mag.md` (pixelization source_science.py magnification docs after 4a/4b). Human: must land BEFORE phase 6; phase 6 not tonight.
2026-10-29 — Phase 4b PRs OPEN: PyAutoArray#666 (exact kNN areas; closes #665) + autolens_workspace_test#349 (merge after). Suites green (Array 2251, Galaxy 1452, Lens 1015, nojax 278). Awaiting human /prm. Next: 4e docs prompt, then phase 6 (not tonight).
2026-10-29 — Phase 4b MERGED + CLOSED via /prm: PyAutoArray#666 (`e71feafd`, pending release) + autolens_workspace_test#349 (`5a41b981`); #665 closed; record `complete/2026/10/mesh-magnification-knn-areas.md`. Phase 4 remaining: 4c (library flux-ratio μ), 4d (source_science recovery sweep), 4e docs (filed, before phase 6). #609 open separately.

## Phase 4e shipped; phase 6 started — 2026-10-30

4e docs merged (autolens_workspace#606, record `complete/2026/10/pixelization-mesh-mag-docs.md`). Smoke against
simulator truth exposed wrong answers: imaging extra galaxy not scaled out, interferometer over-regularised, and a
library bug — adaptive rectangular `source_plane_mesh_grid` was the uniform overlay, not the pixel centres (fixed
PyAutoArray#668, record `complete/2026/10/adaptive-rect-mesh-node-positions.md`, pending release). Kernel
regularizations kept on the lattice explicitly (human ruling); end-to-end study filed
`draft/research/autolens_inference/kernel_regularization_distances_adaptive_rectangular.md`.

Phase 6 sliced (human "do phase 6"): 6a LensCalc area magnification (PyAutoGalaxy#684 → #685 MERGED 2026-10-30,
pending release; record `complete/2026/10/area-magnification-lenscalc.md`) → 6b MERGED 2026-10-30
(autolens_workspace_test#352, record `complete/2026/10/area-magnification-validation.md`; fix PyAutoGalaxy#687) → 6c source_science docs
→ 6d autolens_assistant LEGGOS II ingest.


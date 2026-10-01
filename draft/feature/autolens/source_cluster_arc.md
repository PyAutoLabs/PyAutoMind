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

## Phases (order is load-bearing)

1. `draft/bug/autolens/point_solver_error_bisect_health.md` — bisect the error-behavior
   change (prime suspect: magnification-filter Hessian buffer=self.scale → hardcoded
   0.01, Mar 2026) + health-harden. Blocks everything point/cluster.
2. `draft/research/autolens_profiling/point_solver_profiling_cells.md` — quasar /
   cluster-runtime / single-source / factor-graph profiling cells. Gate: 1.
3. `draft/refactor/autogalaxy/critical_curves_dispatch_cluster.md` — context-aware
   engine dispatch, dedupe twin plot_utils, cluster plots honor the flag. Before all
   map/segmentation phases.
4. `draft/test/workspaces/mesh_magnification_correctness.md` — areas + magnification
   recovery across every mesh variant (rectangular/delaunay/delaunay_nn/knn).
5. `draft/feature/autolens/point_magnification_api.md` — μ at a point, documented in
   source_science + point package; parity decision; multi-plane.
6. `draft/feature/autolens/area_magnification_leggos.md` — LEGGOS Eq. 6-7 pixel-
   inversion area μ as primary; ShapeSolver rehabilitate-or-retire; wiki ingest.
   Gates: 3, 5.
7. `draft/feature/autolens/magnification_errors_posterior_draws.md` — standalone
   posterior-draw errors in source_science; latent decision. Gates: 5, 6.
8. `draft/feature/autolens/magnification_maps_visualization.md` — image-plane contour
   maps, source-plane mesh maps, Fig-4 uncertainty map, pretty pass. Gates: 3-7.
9. `draft/feature/workspaces/cluster_source_science.md` — new cluster/source_science.py
   (point-source tier). Gates: 1, 3, 5-8.
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

Next bounded prompt: `active/point_solver_image_accuracy.md`
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

User “I approve” granted the plan and task-specific development-only RED override. Only autolens_workspace_test#333 issued; prompt active/point_solver_image_accuracy.md. Worktree .worktrees/point-solver-image-accuracy, branch feature/point-solver-image-accuracy at 13c9d1f. Implement and validate through PR creation; no merge/release authorized.


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

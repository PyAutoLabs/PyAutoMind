# Profiling catalogue routing in Brain

Completed: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/477
PR: https://github.com/PyAutoLabs/PyAutoBrain/pull/478
Merge commit: fb82b9da490ad282ad6fa21e728c9e84aa2c1adc

Added stdlib routing from the project's local manifest or published v2 catalogue. Legacy AST fallback applies only when the new producer is absent. Invalid/missing routes retain explicit unknown coverage; unsafe identities are rejected. Runtime cell/output identities and CPU caps are preserved. Missing sources and unavailable compile builders suppress dispatch; available compile probes use their declared source path.

Validation: full Brain suite 1,230 passed; final conductor suite 48 passed; tenant firewall, discovery and syntax passed. Live old/new project integration matched runtime decision fields across 22 grid cells. Independent review CLEAN after its compile-path finding was fixed. Exact-head CI run 37436134919 passed every job/step on Python 3.12 and 3.13 at 9021e632de8b584094ce47efc6a13672f3f91d7e.

Heart STALE: release validation stale: source moved since rehearsal (PyAutoNerves). Current dev-ship policy allowed shipping; no RED override. Human /prm authorized merge on 2026-10-06. Branch ancestry proved against fetched origin/main after merge. Isolated Brain coordination was explicitly authorized.

Archive presence is unreviewed evidence, never an accepted baseline. Generic compile builder remains unavailable. No jobs, campaigns, baseline acceptance or temporal charts. Parent phases 5–6 remain unstarted. Project migration merged first as autolens_profiling#381.

Validation evidence archived locally under .worktree-archives/profiling-phase4-20261006/profiling-catalogue-routing/ with copy hashes verified.

Reconciliation: retained unrelated `draft/feature/pyautobrain/batch_slice.md` on resemblance-only evidence; follow-up door `/intake reconcile draft/feature/pyautobrain`. Retained the profiling parent because phases 5–6 are unshipped.

## Original prompt

# Route profiling through the project source catalogue

Type: feature
Target: PyAutoBrain
Repos: PyAutoBrain
Difficulty: medium
Consequence: judge
Autonomy: human-required
Filed: 2026-10-06
Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/477

Primary repo: @PyAutoBrain. Standalone organ task, no library changes.
Parent: draft/feature/pyautopulse/profiling_setup_browser.md, approved Phase 4.
Dependency: autolens_profiling#380 source manifest, available in isolated worktree;
retain compatibility with the current main producer until project migration merges.
Branch: feature/profiling-catalogue-routing
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-catalogue-routing

## Approved high-level plan

1. Read the versioned project script catalogue without scientific imports.
2. Replace sweep CELLS AST assumptions when the producer is available, retaining
   explicit legacy fallback for pre-migration checkouts only.
3. Keep dry-run decisions, CPU caps, output identities and evidence qualifications.
4. Test current/legacy/malformed/missing producers and local migration integration;
   review and evaluate current shipping gates in a separate PR.

Tier: judge — merge mode: human /prm.

## Detailed plan

- agents/conductors/profiling/_profiling.py: stdlib reader for local
  catalogue/script_routes.json or published dashboard/catalogue.json script_routes.
  Validate schema/version, safe source paths, unique cell IDs and instrument lists.
  Fail explicitly on malformed/unknown data rather than invent empty coverage or
  silently fall back. Missing new producer may use existing legacy AST reader.
- Surface source/provenance/qualification on campaign decisions. Existing archive
  presence is unreviewed coverage, never accepted baseline/current performance.
  Preserve compile/runtime distinction, pins and unavailable compile builder status.
- Keep CPU per-run timeout and dry-run behavior. No execution or new baseline steps.
  Update affected profiling agent/skill docs and tests only. No ownership changes.
- Exercise legacy/new producer fixtures, unknown schema, unsafe paths, duplicates,
  missing producer and CLI decision integration against the Phase4 project tree.

## Coordination

Human explicitly answered "Allow isolated Brain coordination" on 2026-10-06 for
active Brain claims #469–472. Work is isolated from those branches and touches only
profiling conductor, its tests and related docs. Existing main clean; no merge or
Heart RED override carried forward. Project migration is independently tracked #380.

## Original request (verbatim)

Resume the profiling redesign at Phase 4: dataset/model script migration and Brain routing.

Read PyAutoMind/draft/feature/pyautopulse/profiling_setup_browser.md and the completion records for profiling-setup-page and profiling-setup-browser. Project PR autolens_profiling#379 and Pulse PR #13 are merged; verify current state before proceeding.

The overall redesign plan is already approved. Follow start-dev and create the next task/worktree without asking me to approve the same scope again.

Inventory scripts and callers, then migrate toward:
scripts/<dataset>/<model>/<measurement>.py

Preserve numerical behavior, CLI arguments, output destinations and existing results. Keep thin compatibility wrappers for old paths. Update imports, sweep/compile dispatch, HPC scripts, tests and documentation. Validate without submitting profiling jobs. Then update Brain's profiling routing in a separate task/PR.

Keep evidence qualification and unknowns explicit. Do not launch a baseline campaign, accept archived measurements as baselines, or restore temporal charts.

Continue through implementation, testing and review. Apply current shipping gates; do not infer a new Heart RED override or merge authorization from previous sessions.

## Phase 4b implementation checkpoint — 2026-10-06

PR https://github.com/PyAutoLabs/PyAutoBrain/pull/478 OPEN at
9021e632de8b584094ce47efc6a13672f3f91d7e; branch/worktree above, not merged.
Implemented stdlib local/published catalogue routing, qualified legacy fallback,
invalid/missing-producer errors, unchanged historical cell IDs and CPU caps,
source availability checks and declared compile-probe dispatch/unavailability.
Only profiling conductor, its agent/skill docs and tests changed.
Validation: full Brain suite1,230 passed; final conductor suite48 passed;
tenant firewall, discovery, syntax and whitespace pass. Existing unrelated
skill line-count overruns remain report-only. Independent Sol CLEAN after fixing
its P2: compile source availability now includes and dispatches the declared path.
Live old/new project integration matches runtime coverage/usability/dispatch exactly;
22 grid cells, unreviewed archive qualification, no generic compile builder invented.
Heart STALE: `release validation stale: source moved since rehearsal (PyAutoNerves)`;
no RED/YELLOW reasons, no override invoked. Current dev-ship policy permits this.
Exact-head GitHub CI3.12/3.13 pending at handoff. No compute/baseline/merge performed.
Logs: `.worktrees/profiling-catalogue-routing/{brain-full-tests.log,
profiling-tests-reviewed.log,live-project-runtime.json,live-project-compile.json,
legacy-project-runtime.json,heart-readiness.json,tenant.log,discovery.log}`.
Next: human reviews both PRs and runs /prm once required checks are green.

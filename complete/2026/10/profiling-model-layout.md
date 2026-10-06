# Profiling scripts: dataset/model migration

Completed: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/380
PR: https://github.com/PyAutoLabs/autolens_profiling/pull/381
Merge commit: a36590ac41f5708a546fd5e35e81f8124d646c5c

Migrated 80 scientific scripts/helpers to scripts/<dataset>/<model>/<measurement>.py with thin legacy wrappers. Added an explicit route manifest and catalogue export; updated imports, runtime/latent/compile dispatch, HPC, CI, documentation and tests. CLI arguments, output identities and numerical bodies are preserved. Shared tooling/components retain documented homes.

Validation: 1,071 tests passed, 6 skipped; final catalogue/routing 37 passed; 52 import smokes, 182 HPC shell syntax checks, eight-leg HPC and full runtime/latent dry-runs passed. Numerical ASTs matched after path normalization and all 1,388 result files remained byte-identical. Browser, Ruff, formatting and producer contract checks passed. Independent review CLEAN. Exact-head CI run 37435473812, job 112176093067, all steps successful at 4dedf1a63469dd77ccd5e78338491d77c05e65cf.

Heart STALE: release validation stale: source moved since rehearsal (PyAutoNerves). Current dev-ship policy allowed shipping; no RED override. Human /prm authorized merge on 2026-10-06. Branch ancestry proved against fetched origin/main after merge.

Generic compile builder remains explicitly unavailable. Archives remain unreviewed evidence, not baselines. No profiling jobs, campaign, baseline acceptance or temporal charts. Parent phases 5–6 remain unstarted. Brain routing shipped separately in PyAutoBrain#478.

Validation evidence archived locally under .worktree-archives/profiling-phase4-20261006/profiling-model-layout/ with copy hashes verified. Committed inventory: catalogue/migration.md.

## Original prompt

# Migrate profiling scripts to dataset/model/measurement

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: large
Consequence: judge
Autonomy: human-required
Filed: 2026-10-06
Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/380

Primary repo: @autolens_profiling. Standalone workspace, no library API changes.
Parent: draft/feature/pyautopulse/profiling_setup_browser.md (approved Phase 4).
Branch: feature/profiling-model-layout
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-model-layout

## Approved plan

1. Inventory scientific scripts and callers, recording explicit legacy/canonical routes.
2. Migrate to scripts/<dataset>/<model>/<measurement>.py with thin compatibility wrappers.
3. Update imports, runtime/compile dispatch, HPC commands, tests and documentation.
4. Validate numerical-body/default preservation, CLI and output routes, unchanged results,
   import smokes and all applicable tooling tests without submitting profiling jobs.
5. Review and apply fresh shipping gates. Brain routing follows in a separate task/PR.

Tier: judge — merge mode: human /prm.

## Detailed implementation

- Preserve legacy sweep cell IDs/instrument matrix and output names; publish explicit
  script routes through a stdlib catalogue/manifest reader. Rectangular is the canonical
  model name; pixelization remains a legacy alias, not a scientific equivalence claim.
- Inventory imaging, interferometer, datacube, point-source, cluster and multi-dataset
  leaves, experimental controls and helpers. Keep components under scripts/lens and
  shared tooling under documented scripts/misc. Map variant measurements distinctly.
- Preserve numerical bodies and configuration defaults; change only location/import
  plumbing. Compatibility entry points forward CLI and imports to one implementation.
- Update sweep, compile probes, cross-script imports and path joins, HPC scripts, CI
  smoke commands and current docs. Historical results and provenance remain untouched.
- Add dispatch/wrapper/import regression checks, freeze result hashes and compare
  numerical AST/defaults before/after; run Ruff, relevant/full tests and tooling checks.
- Unknown evidence stays unknown; archives remain unreviewed. No campaign, baseline
  acceptance, temporal chart restoration, submission, or merge is authorized.

## Current survey

2026-10-06: project main and origin/main at merged PR379 4832679a; Pulse PR13
MERGED 4b00106c. Project only untracked dataset/abell_1201 preserved. No active
Mind project claim. Existing unrelated worktrees preserved. Brain has four active
claims (#469–472); separate routing task requires coordination before it starts.
Heart entry STALE (monitoring RED); no prior override carried forward.

## Original request (verbatim)

Resume the profiling redesign at Phase 4: dataset/model script migration and Brain routing.

Read PyAutoMind/draft/feature/pyautopulse/profiling_setup_browser.md and the completion records for profiling-setup-page and profiling-setup-browser. Project PR autolens_profiling#379 and Pulse PR #13 are merged; verify current state before proceeding.

The overall redesign plan is already approved. Follow start-dev and create the next task/worktree without asking me to approve the same scope again.

Inventory scripts and callers, then migrate toward:
scripts/<dataset>/<model>/<measurement>.py

Preserve numerical behavior, CLI arguments, output destinations and existing results. Keep thin compatibility wrappers for old paths. Update imports, sweep/compile dispatch, HPC scripts, tests and documentation. Validate without submitting profiling jobs. Then update Brain's profiling routing in a separate task/PR.

Keep evidence qualification and unknowns explicit. Do not launch a baseline campaign, accept archived measurements as baselines, or restore temporal charts.

Continue through implementation, testing and review. Apply current shipping gates; do not infer a new Heart RED override or merge authorization from previous sessions.

## Phase 4a implementation checkpoint — 2026-10-06

Project PR https://github.com/PyAutoLabs/autolens_profiling/pull/381 is OPEN at
4dedf1a63469dd77ccd5e78338491d77c05e65cf (not merged). Worktree and branch above.
80 canonical scientific scripts/helpers, thin legacy wrappers, stdlib route manifest
and catalogue export; runtime/latent/compile capability, imports, HPC/CI/docs updated.
Numerical ASTs match after path normalization; all 1,388 result hashes unchanged.
1,071 full tests passed, 6 skipped, 17 warnings; final37 catalogue/routing tests passed.
52 import smokes, full dry-run matrices,182 shell syntax checks/eight-leg HPC dry-run,
Ruff/format, README/dashboard/wiki/layout/wall, Pulse schema and Chromium checks pass.
Independent Sol CLEAN; full review includes compatibility globals and dispatch sets.
Heart current verdict STALE: `release validation stale: source moved since rehearsal
(PyAutoNerves)`; no RED/YELLOW reasons and dev-ship passes. No override invoked.
PR CI lint pending at first exact-head inspection. No compute/baseline/merge performed.
Evidence: `.worktrees/profiling-model-layout/{before.json,caller-inventory.json,
check_preservation.py,pytest-green.log,smokes.log,generation-final.log,browser-final.log,
heart-readiness.json}`; inventory also committed as catalogue/migration.md.
Next: finish separate Brain #477 review/shipping, then human reviews/merges project PR.

Final exact-head CI: project head4dedf1a lint run37435473812/job112176093067
SUCCESS, GitHub mergeStateStatus CLEAN. Separate Brain PR478 is now open.
Both remain unmerged. Parent later phases remain unstarted.

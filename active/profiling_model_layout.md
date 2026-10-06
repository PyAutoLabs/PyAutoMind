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

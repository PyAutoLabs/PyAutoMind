Likelihood lifecycle phase 3, day-zero write 4/4: setup-baseline closed by day zero (R10), coverage confirmed, runtime_estimates exported. Phase 3's day-zero write is complete.

- Merged: https://github.com/PyAutoLabs/autolens_profiling/pull/504 (`709c8d0`, 2026-11-01, human /prm; lint green on `b511854`) and https://github.com/PyAutoLabs/PyAutoPulse/pull/86 (`6c18f9e`, 2026-11-01, human /prm; lint + refresh green on `42d1075`). Issue https://github.com/PyAutoLabs/autolens_profiling/issues/503 closed. Heart RED development override invoked by the human 2026-11-01.
- Human rulings 2026-11-01 (AskUserQuestion): retire `baseline_readiness.py` and its tests; export `catalogue/runtime_estimates.yaml` (stdlib YAML).
- Deviation from the issue text: the 1,044-slot draft manifest and its readiness contract live in `baseline/superseded/`, not `archive/2026/11/` (the catalogue registry scans `archive/**/*.json` as evidence).
- autolens_profiling: `baseline/campaign.json` = the `setup-baseline-closure` manifest (superseded by day zero 2026.10.25.1; Pulse snapshot at `60d5a96` from `e4811a2`; counts; each of the six unknowns answered). `export_runtime_estimates.py --pulse ../PyAutoPulse` verifies the snapshot's records_sha256 and writes 116 cells (71 optimal, 41 secondary, 4 held provisional; all 39 decision_ids) with ms per eval, resources, workers and projected calls/s per node, parallel efficiency 1.0 declared; CI `--check`. Coverage witness test: 0 of 148 optimal planned cells not measured. Wiki ledger, index row, timing-audit P10 row and results-destinations test updated.
- PyAutoPulse: `setup-baseline` campaign and `setup_baseline_campaign` task → complete with a closure table; board re-rendered offline; `check --offline` OK; the control-room escape test now probes the first open campaign.
- Next (epic): phase 4 (inference wall-time validation on RAL; needs compute) and phase 6 (gradient, may run alongside 4–5); phase 5E consumes catalogue/runtime_estimates.yaml.

## Original prompt

# Likelihood lifecycle phase 3, day-zero write 4/4: close setup-baseline, confirm coverage, runtime_estimates export

Type: research
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
Themes:
- profiling
Difficulty: medium
Autonomy: supervised
Priority: high
Status: issued
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/503
Consequence: judge
Witness: autolens_profiling baseline/campaign.json is the closed setup-baseline manifest superseded by day zero (old 1,044-slot draft archived; baseline_readiness.py retired); catalogue/runtime_estimates.yaml is exported from PyAutoPulse snapshots/day_zero/lens.json with a CI --check; a test asserts no optimal planned cell is not_measured; PyAutoPulse campaigns.yaml marks the setup-baseline campaign and task complete and the board shows no not_measured Optimal cell
Review-minutes: 30
Unattended: never
Epic: likelihood-lifecycle
Phase: 3
Parent: draft/research/autolens_profiling/likelihood_lifecycle_epic.md
Filed: 2026-11-01

## Request (human, 2026-10-31, verbatim)

"4. Adopt and close the Pulse setup-baseline campaign (R10), replacing its 1,044-slot manifest; confirm coverage shows no not_measured Optimal cell; add the runtime_estimates export (for phase 5E)." — then "Yes go".

## Human rulings (AskUserQuestion, 2026-11-01)

- Heart RED: "Override + create issue" (development only; merge via /prm).
- `baseline_readiness.py` and its tests are retired (git history keeps them); the draft manifest is archived under `archive/2026/11/setup_baseline_draft/`.
- Export: `catalogue/runtime_estimates.yaml` (YAML via a stdlib emitter), checked against ../PyAutoPulse's frozen snapshot in CI.

## Research (2026-11-01)

- Coverage is already clean: PyAutoPulse `setup_browser.not_measured` → 0 of 148 optimal planned cells; autolens_profiling coverage 232/232 current.

## Plan

1. autolens_profiling: replace baseline/campaign.json with the closure manifest (status closed; superseded by day zero: tag, catalogue/day_zero.json, Pulse snapshot path + commit, counts; R10's answers to the six unknowns); archive the draft; retire baseline_readiness.py + tests; baseline/README.md, wiki ledger and index row updated; `export_runtime_estimates.py --pulse ../PyAutoPulse` writes catalogue/runtime_estimates.yaml (`--check` in CI); coverage witness test. PR, human /prm.
2. PyAutoPulse: campaigns.yaml setup-baseline campaign + task → complete with the closure note; tasks/setup_baseline_campaign.md closure; board regenerated; check passes. PR, human /prm.

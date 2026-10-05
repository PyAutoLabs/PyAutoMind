## profiling-setup-contract
- issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/10 (CLOSED)
- completed: 2026-10-05
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/11 (MERGED)
- head: d9d2377995c37550cf09de765cae7faf84c60a98
- merge: caa500fa0a3976bf10209fdf7b34a826c9f8eff2
- summary: Phase 1 reader of the full setup-first profiling refactor. Adds profiling-summary v2 setup/record/selection/hazard/recommendation validation, typed axes and exact selection identity checks while retaining v1 and the live v1 registry. Documents the producer grammar and tests corrupt/incompatible evidence and cached-snapshot preservation. No dashboard redesign or producer migration shipped in this phase.
- validation: 184 tests passed locally; Ruff lint/format and pyauto-pulse check --offline passed. Exact-head GitHub lint run 37285494916 and Dashboard Refresh run 37285495040: both jobs successful; every test/validation step passed. Only dashboard write step skipped, intentionally disabled for PRs. Branch head proven ancestor of fetched origin/main.
- heart-red-override: user "I authorize" allowed development shipping despite exact RED `release validation FAILED (stage integrate)`; recorded on issue, PR, active.md and autonomy_log.md. User subsequently invoked $prm to authorize this merge after CI passed. No release or rehearsal authorized; no claim Heart cleared.
- release: no library dependency; pending-release label retained on the organ PR.
- next: parent draft/feature/pyautopulse/profiling_setup_browser.md phase 2: autolens_profiling setup catalogue and exporter, then project/Pulse browsing, source taxonomy, wiki/assistant integration and baseline preparation. The full epic is not complete.
- cleanup: no uncommitted code or scientific data in task worktree; disposable Python/pytest/Ruff caches only. Shipping scratch evidence archived under .worktree-archives/profiling-setup-contract-2026-10-05 in the workspace before removal.
- session: Codex; session ID unavailable.

## Original prompt

# Accept setup-based profiling evidence

Type: feature
Target: pyautopulse
Repos: PyAutoPulse
Difficulty: medium
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-05
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/PyAutoPulse/issues/10

Primary repo: @PyAutoPulse
Classification: workspace/organ; no library changes.
Branch: feature/profiling-setup-contract
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-contract

## Approved high-level plan

1. Add the v2 setup/evidence exchange contract while retaining v1 support.
2. Validate typed measurements, setup links, explicit selections, coverage,
   hazards and recommendation applicability without scientific judgement.
3. Exercise both versions through the existing ingestion/rendering pipeline,
   document the producer contract and test invalid/mismatched evidence.

Tier: judge — merge mode: human /prm.

## Detailed plan

### Phase 1: Pulse contract reader (PyAutoPulse)

Suggested issue: `feat: accept setup-based profiling evidence`
Suggested branch: `feature/profiling-setup-contract`

- Extend `pulse/summary.py`, `REFERENCE.md`, and contract fixtures/tests with a
  new version for setup-oriented multi-axis evidence. Continue accepting v1
  during migration; deploy the reader before the new producer.
- Separate setup identity (dataset family, model family, instrument, exact
  dataset/configuration identity) from measurement identity (axis, method,
  hardware, backend, precision, measured revision, run ID).
- Include explicit units, statistic/repetitions where available, configuration
  dimensions, evidence anchors, validation status, missing-data reasons,
  recommendations and their applicability. Preserve captured commit semantics.
- Keep runtime seconds, compile seconds, component timings, host memory and
  VRAM as different typed metrics. A component is never a full likelihood;
  device total/allocated memory is not inferred to be peak process VRAM.
- Selection belongs to the project: a reference maps each setup/metric to a
  specific record. Expose absent/unreviewed evidence honestly. Do not silently
  join different solvers, regularizations, revisions or hardware configurations.
- Test v1/v2 coexistence, unknown versions, empty projects, invalid references,
  units, non-finite values, unsafe evidence paths, duplicate IDs and mismatches.


## Parent and authorization

The complete architecture and original verbatim request are in
`draft/feature/pyautopulse/profiling_setup_browser.md`. User approved the full
plan and continuation on 2026-10-05. The reader must land before the producer
begins publishing v2. Keep the registry on v1 until the producer migration;
the setup browser itself is a later phase. No measurements are submitted.

Original follow-up authorization (verbatim):

> yeah I authorize you to contonue, can you even remove its worttree?

Routing correction: the Feature CLI inferred library for this single-organ task.
PyAutoPulse is a stdlib/YAML organ, not a scientific library; use the approved
standalone workspace/organ route. This is the bounded reader phase of the epic.

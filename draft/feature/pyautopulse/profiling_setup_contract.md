# Accept setup-based profiling evidence

Type: feature
Target: pyautopulse
Repos: PyAutoPulse
Difficulty: large
Consequence: judge
Autonomy: human-required
Priority: high
Filed: 2026-10-05

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

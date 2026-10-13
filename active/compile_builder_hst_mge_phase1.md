# Compile builder phase 1: explicit HST/MGE likelihood construction

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
- compile
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: high
Status: active
Filed: 2026-10-13
Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/413
Pulse task: https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/jax_compile_probe_needs_own_cell_builder.md
Witness: The supported HST/MGE fp64 jit setup is built without importing an executing benchmark; its objective agrees with the shared current runtime-cell objective on a small deterministic test fixture, all unsupported combinations fail before measurement, and a new record cannot enter legacy pin comparisons. Existing pins/results remain unchanged.

## Original user request (verbatim)

ok go

## Conversation context

The user approved profiling priority order and all four preceding timing-audit/Pulse merges. After those completed, the proposed next task was: "scope the missing compile-builder repair." This draft is the bounded implementation phase proposed from that scope. No new implementation plan, collection or historical-pin rerun has yet been approved. Pulse owns the broader builder/baseline campaign.

## Verified findings

- At autolens_profiling 6108d029, scripts/misc/jax_compile/probe.py:build_objective raises NotImplementedError after searches._setup.build_for_cell was retired.
- Existing CLI accepts --dataset-class, --model-type and --instrument, not the old Pulse witness's --cell.
- The old docstring describes a physical-vector negative log posterior; historic imaging MGE records say ndim=15, pixelization ndim=12. Current runtime cells use ModelInstance pytrees, different model construction and a likelihood objective. No equivalence to the legacy workload has been established.
- scripts/imaging/mge/likelihood_runtime.py executes dataset/model construction, timings and writes at module scope. Do not import or runpy it to obtain an objective.
- _production_config.py describes CPU numba production presets; it is not a ready-made builder for this JAX cell.
- export_probe.py and trace_profile.py consume build_objective and assume a flat array. They must not silently inherit a new pytree or objective definition.
- The routing contract's builder_status is global. Marking it available after only one cell works would advertise all 22 runtime-grid cells and seven transforms. Keep global automatic dispatch unavailable in this bounded phase.
- Brain and project pin keys omit objective/model/dataset fingerprints. Do not append new semantics into the old results tree or move old pins. Broader reader/identity integration belongs to a separately reviewed phase.

## Proposed high-level plan

1. Extract reusable HST/MGE setup construction from the current runtime cell into a project-owned factory; retain the runtime cell's existing settings, measured callable and output semantics.
2. Add one explicitly identified fp64/jit compile route using that current likelihood workload. Carry the objective definition and parameter representation as new metadata; unsupported cells, precision modes and transforms fail clearly before measurement.
3. Keep new probe output isolated from the legacy compile-results/pin readers. Preserve the trace/lower, compile, first-call and steady-call split. Require an explicit new output destination; no historical record or pin rewrite.
4. Keep legacy callers safe: trace/export consumers either explicitly opt into the supported representation with truthful metadata or fail before producing an artifact; do not broaden their scope here. Keep global builder_status unavailable and explain the partial manual capability.
5. Test construction, objective parity on a small deterministic fixture, unsupported requests, side-effect-free imports, CLI/output isolation and continued legacy pin-reader behavior. Update probe usage and the campaign's capability notes. Regenerate/check generated project surfaces as required.

Tier: judge — merge mode: human /prm.

## Detailed implementation surface

- New scripts/misc/cell_builders/imaging_mge.py (or a minimal equivalent after inspection): separate model/dataset/analysis setup from execution. Inputs include explicit dataset root and the existing configuration; output includes the current model/analysis/instance and complete supported setup metadata. No auto-simulation on import, timing loops or artifact writes.
- scripts/imaging/mge/likelihood_runtime.py: consume the shared factory while retaining the same setup, masks, over-sampling, priors/fixed parameters, precision behavior and likelihood/pytree timing boundary. Use targeted edits, not a wholesale script rewrite.
- scripts/misc/jax_compile/probe.py: expose the single supported setup clearly (actual CLI flags, no guessed --cell), separate construction and measurement, validate supported precision/transform before expensive setup, add explicit output isolation and objective/representation identity. Never restore the retired inference programme.
- scripts/misc/jax_compile/{export_probe,trace_profile}.py: audit build_objective call sites; preserve legacy semantics or reject incompatible use explicitly. Their measurement campaigns are out of scope.
- catalogue/script_routes.json: retain builder_status unavailable for general dispatch, with a precise reason naming the bounded manual path and remaining coverage gap. This is not availability of the full compile matrix.
- scripts/misc/test/test_compile_cell_builder.py plus relevant existing cache-state/pin tests: verify the actual contracts, including no legacy pin match or legacy result append. Use small local CPU correctness fixtures only, not performance thresholds.
- scripts/misc/jax_compile/README.md and wiki/campaigns/compile_time.md: describe supported scope, new identity, historical non-comparability and next phase. Regenerate catalogue/dashboard if source/route metadata changes.

## Validation and resources

After implementation approval: ordinary local tests and a small CPU correctness fixture, bounded to at most 60 seconds per test process; no full HST timing sweep, GPU/RAL allocation, release run, baseline freeze/promotion or historical-pin timing reproduction. Run the repo's lint, relevant tests and required generated-surface checks. Report missing scientific-stack support rather than treating mocked tests as end-to-end scientific evidence.

## Deferred phases

Extend cell/transform/precision coverage only after reviewing each model/data contract. Before automatic dispatch or mixed old/new comparisons, add per-cell capability and objective/configuration identity to the project and Brain readers through a coordinated contract change. Scientific baseline collection then requires frozen software/environment, exact hardware/affinity, input hashes, settings, witnesses/tolerances, methods and separate compute authorization.

## Planning checkpoint

Current autolens_profiling main has only untracked dataset/abell_1201/; preserve it and implement in an isolated worktree. Mind active.md is empty after timing-audit close-out. Proposed branch feature/compile-builder-hst-mge. Source edits await explicit plan approval under workspace AGENTS.md. No issue or worktree claimed yet.

## Approval and execution

2026-10-13: human approved this bounded implementation plan ("yeah go"). No compute collection authorized. Worktree `.worktrees/compile-builder-hst-mge`, branch `feature/compile-builder-hst-mge`.

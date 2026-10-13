## compile-builder-hst-mge
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/413
- completed: 2026-10-13
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/414
- workspace-pr: https://github.com/PyAutoLabs/PyAutoPulse/pull/51
- summary: Shipped one explicit, isolated HST/MGE fp64 jit current-runtime compile workload; broader profiling campaign remains active in Pulse.

## Merged scope

Project #414 merged at `b8b3b23cd1f0aabc2d7d4ce1cd297f7420b14f76`; Pulse #51 at
`4544365e9b28f837c7331438c8058e9cf275e62a`. All three exact-head jobs passed,
both branches were proven contained in origin/main, and the human authorized
merge in this conversation after the explicit two-PR merge question.

Shared dataset/model/analysis construction preserves the runtime cell's model
and timing boundary. The new imaging-mge-runtime-v1 likelihood/pytree objective
is explicitly different from the retired flat-vector posterior. It rejects
unsupported cells, transforms and precision and requires isolated new output.
Historical results/pins and baseline files are unchanged; global routing remains
unavailable. Cache file counts remain an unqualified heuristic.

## Verification

Project CI: 1,424 tests passed, 6 skipped; browser, links, smoke, inventory,
formatting and generated contract checks passed. Pulse final lint and refresh
jobs passed at `185e97b`. Independent review CLEAN at project `05c5c49` and Pulse
`a76a769`: 40 focused tests, bounded tiny-FITS CPU end-to-end verification, and
24 byte-identical baseline/registry/historical files. Temporary verification
artifacts were removed. Heart was STALE only for missing current-source release
rehearsal, allowed for development; no release or override was involved.

## Decisions and remaining domain work

The registry's exact hash is pinned by the baseline draft. A text-only reason
edit initially invalidated that guard, so the registry was restored rather than
re-freezing the baseline; partial support is documented in the instrument/wiki.
No production measurement, GPU/RAL submission, pin promotion, scientific
acceptance or performance conclusion occurred.

Pulse owns the remaining domain work at
https://github.com/PyAutoLabs/PyAutoPulse/blob/main/tasks/jax_compile_probe_needs_own_cell_builder.md:
broader cell/transform support, coordinated per-cell routing/evidence identity,
and a separately authorized production experiment or baseline plan. This record
completes only the bounded implementation; no new Mind draft duplicates the
Pulse queue. No background follow-up was scheduled.

## Post-merge ledger receipt

[Pulse #52](https://github.com/PyAutoLabs/PyAutoPulse/pull/52) records the final
merge receipts, completion link and remaining domain work. It merged after
both exact-head jobs passed at `6b30e41765722d705d9d77ac1960e41ec1f9b0fd`.
The original migrated task text remains byte-identical (206 Pulse tests pass).
Pulse now ingests project commit `b8b3b23c`; its 112 records remain unqualified
with unknown evidence freshness and no comparisons. No new measurement follows
from the refreshed producer commit.

## Original prompt

# Compile builder phase 1: explicit HST/MGE likelihood construction

Type: maintenance
Target: autolens_profiling
Repos:
- autolens_profiling
- PyAutoPulse
Themes:
- profiling
- compile
Difficulty: medium
Autonomy: supervised
Consequence: judge
Priority: high
Status: awaiting-merge
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


## Review handoff — 2026-10-13

- Implementation PR: https://github.com/PyAutoLabs/autolens_profiling/pull/414
  (`05c5c49a514db1c3dc2b92d1126cf39d7f4cd68a`).
- Pulse ledger PR: https://github.com/PyAutoLabs/PyAutoPulse/pull/51
  (`685e1b8`). Both remain open; judge tier requires human merge direction.
- Shared runtime construction, explicit imaging-mge-runtime-v1 identity, pytree
  input, isolated outputs, and separated compile/execution costs implemented.
  Legacy consumers fail closed. No production dataset was profiled; no pins,
  baseline or scientific acceptance changed.
- Local validation: 19 targeted tests (including tiny CPU compiled/eager parity),
  full suite 1,378 passed / 6 skipped plus 45 baseline-only failures all passing
  on rerun after restoring the registry. Pulse 206 tests passed; lint, format,
  smoke, catalogue/Pulse contracts, generated boards, wiki/README, results layout,
  timing inventory and wall-submit checks passed. GitHub lint jobs pending.
- Plan refinement from verification: preserve the route registry byte-for-byte
  because baseline/campaign.json pins its hash. Partial support is documented in
  the probe README and campaign journal instead of re-freezing that inventory.
- Brain compile conductor still produces no dispatch. Heart at the canonical
  root is STALE solely for "release validation incomplete: no rehearsal for
  current source", permitted for development. An initial task-root manifest
  warning was resolved by evaluating the canonical workspace; no waiver used.
- Broader builder coverage, gradient/batched paths, output-reader capability work
  and production experiment/baseline choices remain domain work in Pulse. End at
  review handoff; no background follow-up scheduled.


## Verified CI and independent review — 2026-10-13

- Project exact-head CI passed at `05c5c49`: 1,424 tests / 6 skipped plus browser,
  links, smoke, catalogue and generated artifacts. Source:
  https://github.com/PyAutoLabs/autolens_profiling/actions/runs/38426218793
- Pulse original head `685e1b8` passed lint and dashboard refresh:
  https://github.com/PyAutoLabs/PyAutoPulse/actions/runs/38426360330 and
  https://github.com/PyAutoLabs/PyAutoPulse/actions/runs/38426360116.
  Later ledger commits record these facts and the independent review; their
  current-head checks must be judged before merge.
- Independent reviewer `/root/compile_builder_review` returned CLEAN at project
  `05c5c49a514db1c3dc2b92d1126cf39d7f4cd68a` and Pulse
  `a76a7690eeb0e627eb944a602f7d5f9ec1360f09`. Verified 40 focused tests, the real
  tiny-FITS -> workload -> AOT -> provenance -> output path on CPU within 60s,
  24 unchanged registry/baseline/historical files, and empty Brain compile dispatch.
  Temporary verification files removed. No source defects or unresolved findings.
- Claim dispositions: shared runtime construction, current likelihood/pytree
  semantics, fail-before-setup guards, output isolation, unchanged historical
  evidence, disabled global dispatch and unqualified cache warmth are basis-cited
  to the reviewed implementation and verification. ReviewSurface had no lifted
  commit-message claims. No production measurements or timing improvement claimed.
- User said "continue"; review and CI verification completed. Previous explicit
  merge approval named #410, #411, #412 and Pulse #48, not this new judge-tier pair.
  Await merge command for #414 then Pulse #51; no background follow-up.

# Publish the complete profiling setup catalogue

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: large
Consequence: judge
Autonomy: human-required
Filed: 2026-10-05
Issued: 2026-10-05
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/376

Primary repo: @autolens_profiling
Classification: standalone workspace. Branch: feature/profiling-setup-catalogue.
Worktree: /home/jammy/Code/PyAutoLabs/.worktrees/profiling-setup-catalogue
Parent: draft/feature/pyautopulse/profiling_setup_browser.md (full approved design and original request).
Upstream: PyAutoPulse#11 MERGED; v2 reader and grammar available.

## Approved plan

1. Declare the scientific families, benchmark matrix, script routing and explicit
   reference selections in a versioned project registry.
2. Implement stdlib adapters for runtime/sweep, breakdown, compilation, memory,
   streaming and hazard evidence with exact source anchors and configuration
   identities. Retain experimental/off-grid and unmapped evidence visibly.
3. Publish deterministic dashboard/catalogue.json (profiling-summary v2) alongside
   v1 summary.json. Preserve existing dashboards, historical artifacts and pins.
4. Validate generation in existing checks and CI, including the independent Pulse
   reader; document metadata, missing coverage, reference selection and adapters.

Tier: judge — merge mode: human /prm.

## Detailed plan

- Add catalogue/registry.json (versioned explicit family/model aliases, script
  routes, declared cells/measurement slots, source adapters and references) and
  documentation. Source paths remain in their present layout until phase 4.
- Add scripts/misc/tooling/build_catalogue.py and a stdlib catalogue module as
  needed. Inventory registered scientific scripts; tooling folders are not
  datasets. Include components, cluster, point-source and multi-dataset work.
- Parse committed evidence only, never import scientific scripts/libraries or
  launch measurements. Retain source path plus JSON pointer anchors, measured
  revision/backend/precision/hardware and method metadata. Missing fields remain
  null with reasons. Never substitute current instrument settings for old runs.
- Exact configuration identity includes recorded scientific settings and source
  context where insufficient metadata prevents a reliable join. No silent
  merging of regularization variants, arm experiments, hardware or methods.
- Separate measurements by axis; component totals are not full likelihood costs,
  static buffer estimates/device capacity are not measured peak VRAM, and failed
  streaming runs are not valid runtime observations. Explicit adapters refuse
  unsupported shapes with an indexed reason and evidence link.
- Selected references are declared by source/pointer/metric, never latest or
  fastest. Existing evidence defaults unreviewed; accepted records require an
  explicit scientific acceptance with provenance. Coverage slots come from the
  declared matrix and carry missing/failed/unusable/inapplicable status.
- build_dashboard.py integrates the catalogue into --check/build when the
  registry is present. Stage catalogue.json in Pages. Keep v1 live since Pulse
  registry pins v1; switching consumers belongs to phase 3.
- Tests cover representative real shapes, type/units/identity errors, unknown
  metadata, non-finite values, unsafe paths, failed runs, explicit selection,
  complete inventory, deterministic --check and the merged Pulse v2 validator.
  Run relevant tooling/full misc suite, Ruff, existing layout/wiki/README checks
  and existing smoke scripts as appropriate. Assert old artifacts unchanged.
- Existing untracked dataset/abell_1201/ in canonical checkout is untouched.
  No active repo claim; recent branches inspected. No library API change.

## Authorization

The complete parent plan was approved earlier in this session. The human now
explicitly requested this phase; no new scientific scope or compute dispatch.

## Original request (verbatim)

Do the next phase

Routing correction: no PyAutoLens library edit or dependency; standalone workspace
phase per the parent approved plan. The CLI heuristic is not the scope authority.

## Implementation checkpoint — 2026-10-05

Implemented in the registered worktree: catalogue registry and stdlib adapters,
exact metric JSON pointers checked against original sources, explicit reference
candidates, metadata with unknown reasons, baseline matrix and source inventory.
The index exports 20,709 measurements through 508 independently v2-valid shards;
708 evidence files and 183 script entry points are inventoried. It retains 8
static memory estimates and 12 hazards with unknown applicability separately.
435 baseline slots remain explicitly not measured. No acceptance, recommendation,
baseline run or temporal comparison is manufactured.

Transport refinement: a monolithic export was too large for initial browser
loading. The root index (about 2.2 MB) contains setups, candidate references,
inventory and manifests; detailed measurement shards total about 44 MB and are
loaded only for a chosen setup. Consumers resolve shard paths relative to the
index, evidence paths relative to the same repository revision, and deduplicate
records by ID. Hashes/counts verified across every source and shard.

Contract constraint found during implementation: v2 selections require a measured
software identity even for missing slots. Future baseline coverage therefore
uses the `planned_cells` extension until a measured stack exists; no fake software
version is supplied to satisfy the validator. coverage.expected.cells counts only
v2 selections, with planned_slots separate. A later reader iteration may promote
this extension, but current independent v2 validation passes.

Existing v1 dashboard files and all historical evidence are byte-unchanged.
Integration covers build_dashboard regeneration/check, lint workflow independent
Pulse validation, and Pages staging. No library API or scientific script changes.

26 targeted catalogue tests pass. Full misc suite: 1,055 passed, 5 skipped, 17 warnings. All seven existing section
smokes pass; final rerun log is in the task worktree. Ruff, README, wiki, result
layout, wall-submit contracts, deterministic generation and independent Pulse
validation pass. Inline review covered provenance, selection/failure semantics,
source anchors, shard transport and deployment. No claim of independent review.

Ship gate: Heart still returns RED, exact reason `release validation FAILED
(stage integrate)` (2026-10-05). Freeze is clear. The earlier override covered
Pulse#10 only. Source commit/push/PR await a new live override for #376 under
Brain AUTONOMY.md "Human override for Heart RED (development only)". PR body is
prepared at `.worktrees/profiling-setup-catalogue/phase2-pr-body.md`.

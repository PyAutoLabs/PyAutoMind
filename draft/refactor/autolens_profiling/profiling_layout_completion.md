# Finish profiling source and hazard layout consolidation

Type: refactor
Target: autolens_profiling
Repos: autolens_profiling
Consequence: judge
Autonomy: human-required
Filed: 2026-10-07

Primary: @autolens_profiling. Standalone workspace, no library changes.
Parent: draft/feature/autolens_profiling/profiling_redesign_completion.md
Approval: Phase B approved with "ok go"; continued after Phase A merge with "ok thats good, continue".

## Overview
Finish the approved dataset/model source layout, retiring obsolete wrappers after caller audits while preserving scientific bodies and historical identities/results.

## Plan
- Audit legacy routes and callers before removal.
- Retire compatibility source hierarchy and keep alias lookup working.
- Put model-specific hazard guidance beside its likelihood and document shared probes.
- Validate routing, imports, HPC dry runs, documentation and unchanged scientific evidence.

Tier: judge — merge mode: human /prm.

## Detailed approved plan

 finish source/documentation consolidation (autolens_profiling)

Suggested branch: feature/profiling-layout-completion; follows Phase A.

1. Audit all 80 legacy routes and active callers in project scripts, HPC, CI,
   tests, README/wiki, Brain profiling and assistant lookup. Preserve historical
   result/provenance text; update current usage guidance.
2. Retire thin wrapper files and obsolete measurement-first directories once
   their active callers use canonical paths. Keep legacy aliases in
   catalogue/script_routes.json for historical identity/output mapping.
   Change _script_routes.load_routes so aliases need not exist on disk;
   remove wrapper execution support only after import/caller audit proves safe.
3. Move model-specific hazard documentation beside mge/ and rectangular/;
   retain shared detector/framework documentation in misc/hazards and deliberately
   document dataset-free component probes. Do not duplicate scientific bodies.
4. Update tests/migration docs, run routing/import/HPC dry-run checks plus
   appropriate full lint/tooling checks, and prove archived results unchanged.


Additional implementation detail: validate canonical files in _script_routes.load_routes without requiring alias files; remove run_legacy after confirming it has no non-wrapper callers. Update routing tests for historical aliases and missing canonical targets. Preserve catalogue/script_routes.json legacy keys and tracked results. Generated documentation must come from its builders. Audit Brain and assistant consumers read-only first; include another repo only if an active caller requires a change.

## Original requests (verbatim)


We rrecently did a lot of work restructing autolens_profiling in order to improve its dashboard. First, I think there are aspects of the refacotr which are incomplete, for example there is still a "hazards" folder with mge / pixelization stuff in, but all hazards stuff should be specific to each likleihod function. Same for imaging/likelihood_runtime and imaging_likelihood_breakdown and similar packages, It feels like the refactor only got half way through?

ok yeah then lets continue, and before we start review the process, previous work and remaining work with Fable. Also, the dashboard does not contain any of the expected output and information att he moment, so maybe it never fully finished and got ot that?

Review-routing answer: Prepare a review handoff for Fable


Continuation: ok thats good, continue

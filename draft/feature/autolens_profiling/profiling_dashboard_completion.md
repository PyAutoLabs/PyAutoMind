# Make profiling measurements and hazards discoverable

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: large
Consequence: judge
Autonomy: human-required
Filed: 2026-10-07

Primary: @autolens_profiling. Standalone workspace; no library API changes.
Parent: draft/feature/autolens_profiling/profiling_redesign_completion.md
Approval: Human approved the concrete three-phase plan with "ok go" on 2026-10-07.
Scope: Phase A only; later layout cleanup and Pulse changes have separate tasks.

## Overview

Both live dashboards default MGE/HST to a breakdown-only archive row, open an empty runtime panel and collapse all nine measured values. Six runtime shards exist. All twelve unbound hazards are hidden by a dataset-in-filename filter. Expose available axes/devices and related findings while keeping exact-run provenance and scientific qualifications.

## Plan

- Show model/instrument measurement availability and named axis navigation.
- Choose useful evidence deterministically and open populated panels.
- Publish explicit hazard discovery scopes separately from exact applicability.
- Regenerate documentation/artifacts and verify real browser journeys and contracts.

Tier: judge — merge mode: human /prm.

## Detailed approved plan

 useful project dashboard (autolens_profiling)

Suggested branch: feature/profiling-dashboard-completion.

1. Add a model/instrument overview in catalogue/browser.js and browser.css.
   Enumerate available measurement axes and recorded devices from evidence_shards;
   show counts and labelled run choices before asking users to choose one exact
   historical configuration. Keep unknown devices explicit. Preserve exact-run
   deep links, URL history and lazy hash-verified loading.
2. Make initial selection prefer available runtime evidence deterministically,
   retaining explicit reference preferences within that axis; never rank by
   speed or pretend that reference candidates are scientifically accepted.
   Open a populated panel if the chosen evidence lacks runtime. Clearly
   distinguish 'absent in this run; other runs available' from no recorded
   evidence anywhere in this model/instrument scope. Other axes should be
   directly reachable without hunting through dozens of opaque run options.
3. Fix hazard discovery using explicit registry metadata in catalogue/registry.json
   and scripts/misc/tooling/build_catalogue.py, not filename substring guesses.
   Separate related/unverified findings from exact version-qualified bindings.
   Audit raw findings before adding any exact binding; no required binding count
   if historical evidence cannot establish exact applicability. Expose shared
   component findings under an explicit shared scope rather than every model.
4. Update catalogue/README.md and generated setup wiki/dashboard via their
   builders. Preserve v2 identity/provenance semantics; any additive discovery
   metadata must be optional for existing consumers. Do not fuse historical rows.
5. Extend scripts/misc/test/browser_setup_page.cjs and relevant catalogue/UI
   tests with MGE and rectangular examples that lack reference candidates,
   axis navigation, visible values, related hazards, unknown metadata, failed
   loads, keyboard/history and responsive checks. Retain raw-result hashes.


## Branch survey

Repository: lens/autolens_profiling; main fef5f28; matches origin/main.
Only untracked dataset/abell_1201/; preserve. No active claim or existing worktree.
Branch: feature/profiling-dashboard-completion.
Worktree: .worktrees/profiling-dashboard-completion/autolens_profiling.

## Original request



We rrecently did a lot of work restructing autolens_profiling in order to improve its dashboard. First, I think there are aspects of the refacotr which are incomplete, for example there is still a "hazards" folder with mge / pixelization stuff in, but all hazards stuff should be specific to each likleihod function. Same for imaging/likelihood_runtime and imaging_likelihood_breakdown and similar packages, It feels like the refactor only got half way through?

ok yeah then lets continue, and before we start review the process, previous work and remaining work with Fable. Also, the dashboard does not contain any of the expected output and information att he moment, so maybe it never fully finished and got ot that?

Review-routing answer: Prepare a review handoff for Fable


Latest authorization: ok go

# Profiling dashboard completion — Phase A

Merged: 2026-10-07
PR: https://github.com/PyAutoLabs/autolens_profiling/pull/388
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/387 (closed)
Merge commit: a5966a32d5217316ab82ee6a3a517e250d5c7611

Added axis/device/run availability navigation, useful initial selections and populated measurement panels. Added explicit, qualified hazard discovery and generated setup documentation. Scientific records and all 1379 tracked result artifacts are unchanged. The draft baseline inventory checksum was refreshed without changing scientific configuration or acceptance.

Validation: 1136 Python tests passed across the full run and focused checksum rerun; 6 skipped. Expanded real Chromium checks, seven import smoke checks, lint/format, generated-artifact idempotence and Pulse contract validation passed. Independent Sol review CLEAN. GitHub head CI completed successfully, all 36 steps passed; merge state CLEAN. Human acknowledged the existing Heart YELLOW before shipping and authorized merge with /prm.

This closes only Phase A. Approved source-layout consolidation (Phase B) and Pulse browser parity (Phase C) remain in draft/feature/autolens_profiling/profiling_redesign_completion.md. No new profiling campaign or scientific baseline acceptance occurred.

Review logs and screenshots archived under .worktree-archives/profiling-dashboard-completion-20261007 in the workspace before worktree cleanup.

## Original prompt

# Make profiling measurements and hazards discoverable

Type: feature
Target: autolens_profiling
Repos: autolens_profiling
Difficulty: large
Consequence: judge
Autonomy: human-required
Filed: 2026-10-07
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/387

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

## Implementation checkpoint — 2026-10-07

Phase A implemented in .worktrees/profiling-dashboard-completion/autolens_profiling,
feature/profiling-dashboard-completion. No source commit/push/PR yet: ship gate
requires acknowledgement of current Heart YELLOW warning:
`manifest drift: shared-standards blocks (generated) — 2 mismatch(es) vs PyAutoMind/repos.yaml`.
No RED reasons. Release validation stale because all five listed library sources
moved since rehearsal; no release authorization is sought.

1136 Python tests pass across full run plus focused checksum rerun, 6 skipped.
The initial full run's only failures were 3 failures/42 errors from the draft
campaign's registry digest; after metadata-only registry review all 46 baseline
tests pass. Expanded Chromium, Ruff, format, generated dashboard/catalogue,
independent Pulse v2 contract, README/wiki/layout/wall checks pass. All 1379
tracked result artifacts unchanged. Independent Sol review CLEAN after repairing
device-filter persistence and testing incompatible exact-run links.

Review and reproduction evidence: task bundle review-verdict.md, browser-check.log,
pytest-full.log, baseline-tests.log, catalogue-check.log, dashboard-check.log,
other *-check.log, browser-artifacts/setup-1280.png. Draft PR body: pr-body.md.
Generated shard metadata was refreshed, but setup/record payloads remain unchanged.
The draft baseline campaign changed only its registry integrity digest; no
scientific settings, state, accepted results or runs changed.

Next action: obtain the named Heart YELLOW acknowledgement, then follow
ship_workspace commit/push/PR steps and update this record. Later phases remain
in the parent; Phase B follows A and Phase C must coordinate the live Pulse claim.

## Heart acknowledgement — 2026-10-07

Human: "I acknowledge, go". The readiness re-query returns the same YELLOW
warning and no RED reasons. Development commit/push/PR is authorized; merge
and release remain separate. Continue ship_workspace; record PR below.

## Development PR open — 2026-10-07

PR: https://github.com/PyAutoLabs/autolens_profiling/pull/388
Commit: 4c0961c (feature/profiling-dashboard-completion), pushed; pending-release label.
Seven repository import smokes pass. Prior Python/browser/contract/lint results
remain valid; source worktree clean. Heart YELLOW acknowledgement recorded above.
Committed review surface is review-surface.json in the task bundle (explicit
--repo resolver; default task resolution did not find the workspace-root worktree).
Independent working-diff verdict still applies to the identical committed changes.

No merge or publication performed. Next: human /prm when required CI is green,
then continue approved Phase B; Phase C must first resolve the Pulse repository claim.

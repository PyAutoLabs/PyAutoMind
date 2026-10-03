# Community delivery follow-through

Completed 2026-10-03 under explicit human "Merge if ci is green" authorization.

Merged Brain#459 (566106d71cb7adb6724e82d2bbdd5b98d9034418), then
Ears#7 (cb33814bc0591bc5ce48555df6a44a3f3b597f91). Both published heads
are merge ancestors, verified through GitHub compare (merge base equals head,
behind_by=0). All five exact-head jobs passed: Brain Python 3.12/3.13 and
Ears Python 3.12/3.13 plus browser. No skipped job or failing gate bypass.

Ears derives explicit maintainer Discussion -> issue -> required PR -> release
links, respects Mind pending-release obligations, and surfaces update owed.
Missing, stale, partial, private and reverted evidence stays unknown. Closed
Discussions stay settled. Brain validates evidence and drafts for approval;
no automatic posting, release promises, task-state duplication or raw-body export.

Validation: Ears 59 tests; local Brain 1132 passed / 42 environment skips;
48 focused adapter/community tests; tenant firewall and cockpit schema pass.
Exact-head CI supplied complete matrix and browser evidence after local Chromium
download failed. Browser covered responsive widths/themes and clipboard actions.

Limitations: explicit Delivery-* evidence links required; later reverts need
source revert evidence or issue reopening. No semantic audit of all later history.
Heart's previously authorized RED development state remains; this human turn
separately authorized merge, not release. Production deployment is a main-branch
workflow and is not claimed complete by this record. Standalone clones retained.
Phase 6 recurring themes remains unissued and requires real report evidence.

## Original prompt

# Community follow-through

Type: feature
Target: PyAutoEars
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Epic: community-organ-birth
Filed: 2026-10-03
Issued: 2026-10-03
Issue: https://github.com/PyAutoLabs/PyAutoEars/issues/6

## Overview
Implement community-organ-birth phase 5 after assistant feedback distribution merged. Original request: "Merge and continue". Ears derives delivery evidence; Brain drafts contributor updates; Mind remains the task and pending-release authority.

## Plan
- Follow explicit maintainer-authored links from a Discussion to target issues, required PRs and published releases.
- Distinguish accepted, in development, merged but unreleased, available, declined and unknown; fail closed on incomplete or private evidence.
- Keep settled discussions settled while separately exposing delivery and update-owed evidence.
- Surface linked evidence and a Brain draft prompt on the board; never post updates.
- Test partial/multiple PRs, unavailable evidence, pending releases, reverts, already-reported delivery and safe rendering.
Tier: judge — merge mode: human /prm. This turn's merge authorization covered the five existing phase-4 PRs; new phase-5 PRs stop at PR-open.

## Detailed design
PyAutoEars ears/followthrough.py parses explicit standalone Delivery-issue: URL, Delivery-PR: URL, Delivery-release: URL and Delivery-revert: URL lines from configured maintainers' source bodies/comments. These are evidence links in existing GitHub conversations, not a state registry or acceptance of arbitrary body instructions. Ordinary ambiguous mentions are not delivery claims. Discussion comments that link each verified release after publication evidence the contributor update. Source bodies are transient and never exported.

Verify each target repo is public before reading or exporting its links. Read issue state/state_reason and complete comments, PR merged state and merge SHA, published non-draft/non-prerelease release tags and compare ancestry. Multiple required PRs must all be delivered; missing/failed evidence is unknown. Explicit revert evidence and a reopened issue after merge block availability. Read Mind pending-release keys without changing or clearing them. No release link means merged-unreleased; unavailable declared release evidence means unknown.

Extend snapshot v1 with a strictly validated optional follow_through projection, preserving old snapshots. Gather public Discussion body/comment evidence (including replies and closed discussions), discard bodies after projection. Render delivery evidence and portable draft prompts in ears/board.py and forward validated follow-through in Brain's _ears_feed.py; skill tells Brain to compose updates for approval from evidence only. Tests cover live collector wiring and schema safety, not just the reducer.

Fresh standalone clones /tmp/ears-followthrough; branch feature/ears-followthrough in Ears and Brain. No active claim conflicts. Memory consulted: no existing follow-through implementation found. Existing whole-programme development authorization continues. Heart has the same previously acknowledged RED reasons; no release or CI bypass.


## PR handoff
- https://github.com/PyAutoLabs/PyAutoBrain/pull/459 — 65af04a025333a68aff5db00e65b4405f8d09931
- https://github.com/PyAutoLabs/PyAutoEars/pull/7 — 1c421a785bd919ed5f4168835be0222de01fb2da

59 Ears tests passed. Brain: 1132 passed, 42 environment skips; 48 focused community/adapter tests passed. Tenant firewall and cockpit state contract pass. Existing Ears browser CI must validate rendering/copy; local Chromium download returned a corrupt archive. Source PRs await human /prm, Brain first. No posting, release, or current production deployment claimed.

Evidence convention also includes explicit Delivery-update: <release URL> after publication. Ordinary release mentions do not clear update owed. Later branch reverts require a source revert link or reopened issue; not a semantic audit of all future commits.

Ship-time Heart RED reasons (existing programme development authorization):
```
  [red] release validation FAILED (stage integrate)
  [red] PyAutoHeart/workflows/Release Integrate: failure
  [red] PyAutoArray/Tests: red
  [red] PyAutoArray/Tests: red
  [red] PyAutoFit/Tests: red
  [red] autofit_workspace_test/Smoke Tests: red
  [red] autogalaxy_workspace_test/Smoke Tests: red
  [red] autolens_workspace_test/Smoke Tests: red
  [red] CI wall-clock: 26 gates · slowest PyAutoBrain Nightly Release 83m · 1 slowed · 6 hang events
  [red] Release readiness: release validation FAILED (stage integrate)
  [red] PyAutoCTI/test_autocti/extract/two_d/parallel/test_parallel_fpr.py::test__estimate_capture: red
  [red] PyAutoNerves/test_autonerves/test_fitsable.py::test__output_to_fits: red
  [red] Unit-test timing: 3 test regressions (>3× baseline), 1 slow (>1.5×)
  [red] autolens_test: red
  [red] Release validation: NOT release_ready — v2026.10.3.1.dev79901 profile=release (2026-10-03T07:43:31+00:00)
  [red] validation_report/stages/integrate: fail
  [red] autolens_assistant: red
  [red] autolens_profiling: red
  [red] autolens_workspace_test: red
  [red] Worktree drift: 0 orphan / 0 missing / 4 dirty
  [red] euclid_strong_lens_modeling_pipeline: red
```

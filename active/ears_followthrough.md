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

# Heart publication coverage

Merged PyAutoHeart #271 on 2026-10-02, merge commit e57425943c3eccad04c6d02f8da6049210a4e960.
Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/270
PR: https://github.com/PyAutoLabs/PyAutoHeart/pull/271

Exports all observed monitoring families with complete public inventories and original timestamps. Missing legacy sections receive fallback observations; cloud observations take precedence. Missing, malformed or expired evidence remains unresolved, with private findings retained as redacted records. Release gates are unchanged.

Validation: 1177 local tests passed; tenant firewall passed; real-snapshot replay exported 16 families. CI run 37002521370 passed both Python 3.12 and 3.13 jobs at head 0c1b7d6e98a620082e6f47c133db438e04fb51f2. All head runs checked; one pull_request run exists.

Human acknowledged the exact two generated-map/front-door Heart YELLOW reasons before shipping and invoked /prm to authorize merge and closeout.


The merged code needs the next local publication and Pages render to update live evidence. No scientific workspace API changes; scientific smoke not applicable.

## Original prompt

# Publish all observed Heart monitoring families

Type: bug
Target: @PyAutoHeart

## Original request

do next bit of work

## Context

Follow-up to heart-monitoring-coverage (Heart #268, Brain #446). The expanded sweep found locally collected checks absent from the live dashboard. Close this publication gap before tackling unrelated scientific script failures.

## High-level plan

- Export locally observed monitoring families that the cloud cannot measure, including manifest and required-workflow drift, URL observations and PyPI floor evidence when unavailable in cloud.
- Preserve each observation timestamp, source, findings and remediation action through publication; redact private paths.
- Let fresh cloud observations remain authoritative for families measured there. Missing, malformed or expired evidence must remain unresolved.
- Validate a local-to-published round trip, including non-green findings, stale/missing evidence and privacy; ship one focused Heart PR.

## Detailed plan

- heart/publish.py: replace the narrow LOCAL_ONLY_FAMILIES export assumption with an explicit publishable coverage contract. Include observation-only families absent from rendered sections using structured monitoring checks, without transporting raw private filesystem evidence.
- heart/dashboard.py: render fallback observations for eligible missing families; retain cloud precedence and freshness labels. Do not synthesize a green section from empty data.
- heart/monitoring.py: consume published coverage consistently when a local section is absent, preserve source observation timestamps and finding identities, and prevent publication time from refreshing old evidence.
- tests/test_publish.py, tests/test_monitoring.py and applicable dashboard tests: exercise round-trip findings and score, missing/expired timestamps, malformed payloads, cloud precedence and path redaction.
- Inspect whether the scheduled workflow needs producer wiring; prefer existing observations with explicit provenance to duplicating collectors or installing the ecosystem in Pages CI.

## Boundaries and survey

Infrastructure task using start-library / ship-library. No changes to release gates, scientific scripts, or score weights. Proposed branch: feature/heart-publication-coverage. Proposed worktree inside workspace: .worktrees/heart-publication-coverage/PyAutoHeart.

Heart canonical checkout: main, clean at survey. Prior claim: pyautopulse-organ-row, Heart PR #269 (merged 2026-10-02, claim released). Its changed files are .claude/hooks/session-start.sh, config/repos.yaml, heart/_workspace.py, heart/_workspace.sh and tests/test_repo_config.py; no planned file overlap. Explicit coordinated concurrency approval is required before worktree setup.

Heart at entry: Release STALE; monitoring RED, 46/100, 90 unresolved. Planning is permitted; no release dispatch is part of this work.

Approved by the human: "yeah do that" (2026-10-02), including concurrent isolated Heart work alongside pyautopulse-organ-row.

Issue: https://github.com/PyAutoLabs/PyAutoHeart/issues/270
Issued: 2026-10-02

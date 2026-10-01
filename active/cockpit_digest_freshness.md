# Structured arXiv digest freshness in the cockpit

Type: feature
Target: PyAutoMemory
Difficulty: medium
Autonomy: supervised
Priority: high
Status: active
Issued: 2026-10-01
Issue: https://github.com/PyAutoLabs/PyAutoMemory/issues/111

@PyAutoMemory only; follow-up to #109 / PR #110 and Brain #434.

## Original user request (verbatim)

ok then go

## Approved scope

Apply the shared structured state/action contract to arXiv digest freshness, distinguishing stalled delivery from overdue human catch-up. Include evidence, last recorded run date and next action. A successful quiet day remains healthy. User “ok then go” approves this increment; no agent, automatic retries or paper ingestion.

## Plan

1. Reuse the two digest stamps and existing two-weekday rule; return healthy/stale/unknown for each digest without equating empty lists with failed runs.
2. Publish both records with provenance and explicit actions, and enrich cockpit attention rows.
3. Keep the Memory board's freshness wording consistent, including unknown/malformed/future dates, while retaining its browser-side ageing of static pages.
4. Test quiet days, weekday/weekend boundaries, independent digests, invalid/missing evidence and shared feed compatibility; browser-smoke both surfaces.

## Implementation details

- `scripts/board.py`: extend `_inbox_freshness` as the shared pure model while preserving stamp/weekdays/stale keys. Parse source dates and snapshot time honestly; malformed/future dates are unknown. Add stable id, canonical state, threshold_weekdays, checked_at, reason, date evidence link and workflow link. Stamp means last recorded filing/heartbeat, not proof of the whole workflow's success or an invented run ID.
- `to_state`: expose both models under `digests` even when healthy; stale/unknown attention rows use v1 state/reason/id/actions/recommended_action_id. Known healthy empty lists create no attention warning. Use snapshot owner for GitHub links to the existing Mind arxiv_papers.yml/arxiv_interests.yml workflow and Memory arxiv-inbox.md/arxiv-interests.md date stamp.
- Actions: read-only Inspect workflow link, stamp evidence link, existing `/bug` manual investigation prompt with requires_approval semantics. Never dispatch/rerun or post to Slack. Missing owner means no invented URL.
- HTML/Markdown freshness: unknown text instead of false successful-empty claims; valid date browser ageing retains the owner threshold. Action prompts independent of rendering. No new shared schema or website edits needed.
- `tests/test_board.py`: timestamps, weekday boundaries, scopes, empty healthy case, action/evidence links, renderer parity and feed validation. Update README documentation. Run `make test`, `make validate`, shared Brain validator and browser checks.

Branch survey: Memory clean main at dc9c3b5; no active Memory claims. Worktree feature/memory-digest-state created from origin/main. Mind isolated codex/memory-digest-state. Approval is the user's current “ok then go”; no new scope/merge authority inferred.

## Validation / shipping checkpoint

Implemented in feature/memory-digest-state, uncommitted pending task-specific Heart override. 272 tests pass; make validate passes; shared Brain v1 validation accepts healthy/stale/unknown; Chromium mobile/desktop light/dark checks pass including evidence links and clipboard. Diff review found no issues. Heart RED: `release validation FAILED (stage integrate)`. Evidence and PR draft: `.worktrees/memory-digest-state/checks/` under workspace root.

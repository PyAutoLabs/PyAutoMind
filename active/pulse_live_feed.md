# Pulse Live Feed coverage and collection fairness
Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/85
Difficulty: medium
Consequence: judge
Status: approved

Target: @PyAutoScientist. Pulse is read-only evidence owner.

## Original request
looks like a good start, I think pulse work is missing so do we need to get support for more boards up?

## Approved three-step proposal
1. Check collection is progressing reliably.
2. Route profiling development work to Pulse.
3. Add dated campaign/run updates, grouped by campaign so individual measurements do not flood the feed.

User approval (verbatim): yeah do all 3
Interpretation stated to user: the three Pulse steps, not a simultaneous Insight/Cortex rollout.

## Plan
- Bound per-repository collection work as well as whole-cycle request/time limits; retain partial normalized history and rotate fairly. Confirm existing deployment/schedule evidence, without inventing a scheduler guarantee.
- Configure explicit profiling-repository-to-Pulse board routing using body-map identities. Reuse existing board UI/grouping and source links.
- Read Pulse campaigns.yaml, registry.yaml and captured snapshots from one verified public Pulse commit. Publish factual campaign check-in updates using the recorded last_checkin, stable IDs and deduplication by meaningful content; no refresh-as-event. Keep active distinct from running and needs-decision distinct from failed. Group associated task updates under campaign IDs.
- Support dated run evidence grouped through explicit campaign association only. Current 112 measurements have null measured_at and no universal campaign association: omit them from timeline and expose coverage counts/reasons, never substitute ingest/render/commit time. Do not infer speedups, acceptance or run submission.
- Keep first-load seed and unchanged polling distinct; same-content check-ins do not create repeated events. Existing registered GitHub work stays visible and actor links stay public.
- Validate fairness, repeated unchanged check-ins, invalid/undated evidence, stale fallbacks, campaign grouping, existing grouped UI and live read-only Pulse ingest. No Pulse/project edits or profiling execution.
Tier: judge — human /prm.

## Files and tests
scripts/activity_feed.py: per-source API allowance, source routing from config, integrate separate Pulse collector coverage and normalized rows without breaking cache schema migration.
scripts/pulse_activity.py (new): pinned public read adapter, campaign/task normalization and dated explicitly associated run groups. Source statuses and timestamps are evidence, not scientific verdicts.
config/activity_sources.json (new): explicit registered profiling repo routing; configured Pulse owner identity, no guessed project campaign associations.
REPORTING.md and collector tests: coverage semantics, fairness budgets, continuity, privacy, timestamp honesty. Reuse live_feed.js UI contract; only label adjustments if the source scope needs it.

## Findings / branch survey
Current publication is initial manual run38469411015; no subsequent scheduled run listed at inspection. This alone is not proof of broken scheduler. Initial collection covered four sources fully, one partially; Pulse awaited collection. Existing global budget can be consumed by one busy repository. Pulse campaign ledger has12 campaigns and recorded last_checkin2026-10-13T17:51:40Z; measurement snapshot112 records has unknown measured_at. Review/ingest times cannot become measurement times.
Scientist main clean, Pulse main clean, no active claims. Preserve existing unregistered DNA Scientist worktree. Proposed feature/pulse-live-feed at .worktrees/pulse-live-feed/PyAutoScientist. Heart entry STALE permits development planning; readiness rechecked at ship.

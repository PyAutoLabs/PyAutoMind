# Pulse Live Feed coverage and collection fairness

Shipped all three approved Pulse steps in PyAutoScientist PR #86: https://github.com/PyAutoLabs/PyAutoScientist/pull/86
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/85
Merged 2026-10-13 at 36ee0ca553b621fe62f157c6b746f3c4fd21d70c; head 1196bee29d1df25b3f45943a3077b219cc7d1526. Every task branch commit is contained in origin/main.

Added a 12-request per-repository allowance so busy sources yield, explicit profiling repository routes to Pulse, and pinned public Pulse campaign/task collection. Meaningful updates are deduplicated and grouped by campaign; unchanged check-ins do not create events. Live validation found 12 campaign rows. Run evidence requires actual measurement dates and explicit campaign/run association. The inspected snapshot contains 100 undated measurements and 12 dated measurements without explicit association; these remain coverage gaps, not invented feed events. Existing five-minute collection delivery remains best effort.

Validation: Python suite 171 passed before two final regressions; final collector/adapter suite 25 passed; JavaScript suite 7 passed; six browser viewport/theme cases plus no-JS passed. Read-only pinned adapter returned 12 campaigns; integrated production CLI returned 26 Pulse-labelled rows including those campaigns. CI Board tests run 38471290462 and its tests job passed for the exact head. Heart was STALE solely for missing current-source rehearsal, with no red/yellow reasons.

Publication dispatched on merged main: https://github.com/PyAutoLabs/PyAutoScientist/actions/runs/38471616619 . Publication and live verification receipt: tmp/pulse-live-feed/publication.json. Test, browser and collection evidence: tmp/pulse-live-feed/.

Pulse and project repositories remained read-only; MyScientist was unchanged. No inference, production profiling, scientific acceptance or new science collection was performed.

## Original prompt

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

## Shipping handoff — 2026-10-13
PR https://github.com/PyAutoLabs/PyAutoScientist/pull/86; head1196bee29d1df25b3f45943a3077b219cc7d1526. Source worktree .worktrees/pulse-live-feed/PyAutoScientist is committed/pushed on feature/pulse-live-feed. Issue85. Human judge-tier /prm required; no merge/publication yet. CI run38471290462 tests job in progress at handoff.

All three Pulse steps addressed: checked enabled Dashboard workflow and schedule history (only initial manual publication observed, no new schedule yet; delivery remains best effort); added 12-request per-repo fairness; explicit profiling-to-Pulse routes; pinned Pulse campaign/task adapter, deduplicated/grouped changes and strict dated-run association support. Pulse/project repos remained read-only. No scientific execution/interpretation/acceptance. MyScientist unchanged.

Correction to initial local-data estimate: live public Pulse snapshot at e47c0f727a53c9aa40af6e68b647071cca062256 has100 undated records and12 dated records without explicit campaign/run associations, not112 all undated. It supplies12 valid campaign rows. Those measurement gaps are explicit and excluded from the timeline. Association can be supplied by Pulse campaigns[].runs records with Mind repo identity and stable producer run_id; producer campaign_id also supported where schema allows. No associations guessed or owner records edited.

Validation: full Python171 passed before two final regressions; final collector/adapter25 passed; JS7 passed; six real browser width/theme cases and no-JS snapshot passed with Pulse fixtures; pinned public adapter7 requests ->12 campaigns; integrated production CLI30-call pilot ->26 Pulse-labelled rows including12 campaigns, partial-source receipts intact. Large4MB snapshot required pinned Git blob fallback, regression tested. JS syntax/diff checks pass. Evidence in tmp/pulse-live-feed/{tests.log,final-tests.log,node.log,pilot.json,integration-feed.json,integration-cache.json,browser/,heart-readiness.json}. Heart STALE solely missing source rehearsal; no red/yellow readiness reasons.

After human /prm: judge all source CI legs; merge; dispatch Scientist organism_board.yml on main; verify activity.json includes pulse:campaign:* rows and profiling sources use board pulse, explicit undated/unassociated coverage, grouped UI. First cycles can remain incomplete. Close issue/lifecycle, regenerate dashboard, remove worktree. Only disposable Python/test caches are expected in worktree; inspect before removal.

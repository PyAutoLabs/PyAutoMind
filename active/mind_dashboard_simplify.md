# Simplify Mind dashboard and retire persistent bundles

Type: feature
Target: PyAutoMind
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/488

Update @PyAutoMind and its renderer/workflow in @PyAutoBrain.
Remove persistent and automatically proposed task bundles and their workflow wiring;
retain the ability to request grouping explicitly when starting work.
Remove Parked from the dashboard, retain underlying lifecycle records, put Human
Review under Backlog, and show seven desktop navigation buttons with accurate counts.

## Original user request (verbatim)

PyAutoMind dashboard: - Remove Bundles, we now specify if we want a task to bundle stuff at the start and its easier than keeping
track of bundles int he way we do which becomes outdated. Remove it from dashbpard and any other functionality.

- Start here should have numerical counter in button. 
- Epics should have numerical counter
- Pending release needs number.

- Remove "Parked", I dont want to be constantly reminded of something which is old news. 

- Lets not have "Human Review" as its own deediciated section and have it a sub category in "Backlog", which then
- means its button disappearss and we have 7 buttons (1 row)

## Implementation plan (approved 2026-10-07)

1. In Brain `agents/conductors/intake/_intake.py`, remove `parse_bundles`,
   automatic bundle generation, bundle cards/copy payloads and census membership
   handling. Remove the Bundles sections in Markdown and HTML. Remove the
   persistent `Bundle:` header contract while retaining unrelated theme metadata.
2. In both dashboard renderers, remove Parked presentation while preserving
   parked lifecycle data and claim guards. Move human-review rendering beneath
   Backlog as a nested category, preserving review-specific copy actions and the
   `human-review` anchor. Include reviews in the displayed Backlog count exactly
   once without making them development recommendations.
3. Render seven navigation destinations: Start here, In flight, Planned,
   Backlog, Pending release, Recent, Epics. Supply Start here's unique displayed
   recommendation count, Epics' displayed group count and Pending release's
   displayed repository count. Keep empty destinations with zero/empty states
   so seven links always resolve. Use the shared theme's layout mechanism to
   fit seven cards on one desktop row, with responsive wrapping on narrow screens.
4. Retire Brain `skills/start_bundle/` and its installation/discovery/docs
   references, plus Mind `bundles.md`, registry guidance in `AGENTS.md` and
   `REFERENCE.md`, template entries in `scripts/spawn.py`, ledger classification
   in `scripts/ledger_merge.py`, and bundle-specific workflow triggers. Preserve
   historical completion records and unrelated worktree/batch uses of "bundle".
   Explicit grouping at task launch remains a normal task-scoping request.
5. Update `tests/test_intake_dashboard.py` and affected template/ledger/skill
   discovery tests. Validate HTML and Markdown parity, empty/nonempty counters,
   unique recommendations, nested Human Review, seven valid navigation anchors,
   and removal of active Bundles dependencies. Inspect the rendered desktop and
   narrow layout and check shared-theme consumers if its implementation changes.
6. Regenerate Mind `dashboard.md`, `dashboard.html`, and `state.json` with the
   canonical intake command after implementation. Ship coordinated Brain and
   Mind PRs via start_library / ship_library.

Tier: undeclared — merge mode: human /prm.

## Initial survey

- Primary repo: PyAutoMind; renderer/workflow repo: PyAutoBrain.
- Both canonical checkouts on clean `main` before prompt creation.
- No active claims conflict. Three unregistered linked worktrees were reported
  for pending-release work; preserve them and use isolated task checkouts.
- Proposed branch: `feature/mind-dashboard-simplify`.
- Feature Agent: medium, direct, library workflow; no Memory matches.
- Heart at entry: STALE (release stale; monitoring red); reassess at ship.

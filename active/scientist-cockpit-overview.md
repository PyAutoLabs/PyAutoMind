# Scientist cockpit overview

Type: feature
Issued: 2026-10-09
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/52
Difficulty: medium
Consequence: judge

Targets: @pyautolabs.github.io @PyAutoScientist

Existing dependency: PyAutoBrain shared theme and state contract; reuse without changing the shared contract in this task.

Merge the cockpit Overview and Scientist entry surface using the existing Scientist branding and orchestration panel. Show compact expandable organ summaries from owner-published evidence. Keep task execution and detailed records with each organ. Prefer three collapsed cards per desktop row and a full-row expansion; adapt to narrower screens. No fabricated completion history or refresh-as-completion timestamps.

Heart entry gate: after reporting the RED reasons, the user authorized planning this specific task with “yeah go ahead”. The user subsequently approved the implementation plan.

## Original request (verbatim)

The "Overview" tab should be Scientist and correspond to PyAutoScientist -- it is where the scientist goes to monitor and work on
all aspects of their work (e.g. check the Brian, Mind, Pulse). I can imagine I would go to PyAutoScientist to get a high
level summary of the last 24 hours work across all organs, or to coordinate tasks over multiple organs (albeit I think in
general I would go to indiviusal organs to do task).

This tab should have the same PyAutoScientist banner and logo at the top, and it should have the "Work with your Scientist"
panel. The PYAutoScientist page already has this, key point is we are merging this into the overview.

Remove the buttons that are there (Brain, Mind, ) I dont think having buttons for this board is useful.

On the overview page, there is wayy too much text and information, firstly, we should keep 3 organ buttons per row,
but they should be clickable to drop down. I can then more easily see them all. Second, when we click on them, I think
up to 3 items should be displayed for each, which should really fall down into 3 categories:

1) Is there something which needs to be done? e.g. is the heart red and we need to fix it? IS there an active / unifished task?
This could say "nothing to do", but think of more concise and clear ways to show this.

2) Maybe another last hting that was done???

3) What is the last thing that was done? e.g. what was the last task completed, and when was it completed? This should be a concise
10 words or something with a link, high level summary.

Take these 1), 2), 3) as guidance, I think different boards will have different things to show, so think hard about how to
make the buttons as coordinated as possible with one another but also suitably bespoke to their organ. Remember it should be
concise when we click down not to overload information.

It stands to reason we could have 2 organs per row or just all of them in rows if that makes the click down text
and informaiton much easier to read (having only a third of the screen is quite restrictive).

## Approved plan

### High-level

1. Make PyAutoScientist the canonical home dashboard, embedded as the cockpit's first tab, labelled Scientist. Preserve old Overview bookmarks as aliases.
2. Retain the existing Scientist banner/logo and shared Work with your Scientist panel. Remove redundant organ shortcut buttons and long explanatory/router text; retain top-level organ tabs and concise evidence links.
3. Show every configured organ as a collapsed card: three per desktop row, two at intermediate widths, one on phones. Opening a card reveals a full-row detail area, so summaries are readable. Preserve keyboard focus and expansion during refresh.
4. Limit expanded content to three useful lines: attention/next step, active work or current position, and latest result where published. Prefer roughly ten-word linked summaries; use domain-specific labels, omit duplicates and absent optional rows.
5. Preserve source ownership, freshness, missing-data handling and ordinary organ navigation. Make the Scientist prompt explicitly support a last-24-hours summary and multi-organ coordination without adding a persistent activity collector.
6. Validate fixture data, browser navigation, disclosure controls, clipboard, refresh and responsive light/dark layouts. Ship coordinated PRs; merge remains a human action.

Tier: judge — merge mode: human /prm.

### Detailed implementation / proposed issue body

Primary repository: PyAutoScientist. Companion repository: pyautolabs.github.io.
Branch: feature/scientist-cockpit-overview.
Classification: workspace / organ presentation; FeatureDecision recommended direct execution at medium difficulty. The automatic repo classifier omitted the dotted website name; explicitly include it in claims and setup.

- PyAutoScientist/scripts/organism_board.py: replace the fixed six-board badge/Markdown router with canonical organ membership and owner-published state.json collection using the existing Brain schema. Reuse shared hero and orchestration_panel; remove navigation_cards for organs and the redundant verbose route banner. Keep Markdown/badge outputs compatible or deliberately update their tests where the current headline parser is superseded by structured Heart status. Update CHECKIN_PROMPT to request significant changes in the previous 24 hours when appropriate, with evidence dates and gaps; retain focused follow-ups and cross-organ routing.
- Scientist summary adapter: distinguish source status from transport/freshness state; prioritize explicit decisions and actionable failures before ordinary active work; deduplicate summaries; at most three content rows per organ. Domain labels: Heart checks/readiness; Mind tasks/review; Cortex runs/check-ins; Pulse/Insight evidence/campaigns; Hands release; Memory knowledge; Eyes figures; Ears conversations; DNA compatibility; Nerves configuration; Gut cleanup; Brain coordination; Broca assistant evidence. Do not infer a decision from colour alone. Use current owner headlines where no richer typed data exists, without inventing work state.
- Latest result: use an explicitly published result/release/completion and its evidence link/date when available. Existing Hands headline supplies a release version and age. Current shared feeds generally contain attention items, not completion records, and the sampled Mind/Hands/Pulse board.json URLs are absent. Do not scrape prose to invent completed history or substitute feed.updated for event time. Omit unsupported latest-result rows; report this coverage limit. No cross-organ producer migration is hidden inside this UI task.
- Scientist presentation assets, inline in generated output: accessible collapsed organ controls, three/two/one-column layout, full-row expanded content, small status labels and a concise link to the owning board. Preserve expansion/focus across data updates. Keep long prompts in the existing work panel rather than repeating them within organ cards. Maintain truthful unavailable/stale/last-known states and freshness timestamps; no successful empty-state claim after a failed read.
- pyautolabs.github.io/cockpit/index.html: replace the separate native Overview surface with the canonical Scientist board through the existing known-board iframe mechanism. Default route and first tab become #scientist; #overview remains an alias. Keep Scientist distinct from monitored organ feeds so it does not recursively aggregate itself. Retain canonical organ tabs, hash/history handling, safe internal-link routing, header/feed notifications and polling without reloading the selected frame. Remove retired overview-only rendering and oversized pinned Heart content. Verify Scientist is never reported as a missing-feed organ.
- pyautolabs.github.io/cockpit/sw.js: bump shell cache version for the changed shell; continue excluding feeds from cache. Update cockpit README/AGENTS guidance and Scientist guidance only where this change makes existing descriptions stale.
- Tests: update Scientist renderer/collector fixtures and website Node tests for route aliases, summary cap and priority, missing/stale feeds, escaping and genuine event dates. Browser preview at 390/768/1440px, light/dark, expanded cards, keyboard controls, copied check-in prompt, same-origin inter-board links and Back/Forward. Verify a refresh preserves open cards, focused controls and the selected board. Render with matching checkouts; preview is not a claim of deployed publication or physical-device testing.
- Delivery order: validate both repositories together; open coordinated pending-release PRs. Scientist publication must be available before the shell points at it. No merge, release or recurring jobs authorized by this plan.

### Branch and claim survey

2026-10-09: website, Scientist and Brain canonical checkouts are clean on main. Mind was fast-forwarded to origin/main before this draft was written. No matching active task and no active claim conflict for the two implementation repositories.

Website recent branches: main, docs/restore-organ-sentence. Scientist: main, feature/pyautodna-stack-management, feature/map-block-autolens-visualization. Scientist has an unregistered linked worktree at .worktrees/pyautodna-stack-management/PyAutoScientist; preserve it. Brain also has unrelated unregistered worktrees, but Brain source edits are not planned.

Proposed worktree bundle: .worktrees/scientist-cockpit-overview/ inside /home/jammy/Code/PyAutoLabs, respecting the workspace path constraint. Recheck claims and use start_workspace setup after plan approval. No source files edited and no issue created yet.

## Approval and additional direction

2026-10-09: User approved the plan and added (verbatim):

I approve, I think a normal thing to do with this is to ask the Scientist for a high level summary of all work over all organs over 24 hours or a given time period. I'm not sure this needs to go into the dashboawrd design (it should be included in the copyable text of the prompt thing) but worth also thinking if the repo or something should be updated to be designed more carfully around it

Implementation includes a Scientist-owned reporting guide, referenced from the copied prompt and repo entry instructions: resolve the reporting window/timezone; inspect owner records for all organs; summarize outcomes, active/blocked work and decisions; separate event dates from observation dates and disclose unavailable coverage. Default to the previous 24 hours, honor another requested period. No new dashboard history service.

## Implementation checkpoint — 2026-10-09

- Implemented in `.worktrees/scientist-cockpit-overview/{PyAutoScientist,pyautolabs.github.io}`, both on `feature/scientist-cockpit-overview`. Source remains uncommitted pending the Heart RED shipping override.
- Scientist is now the canonical home; cockpit default/legacy Overview routes embed it. Fourteen organ disclosures, three/two/one columns, full-row expansion, at most three concise rows, validated live owner feeds and preserved controls/focus. Shared banner and work panel retained; redundant navigation removed.
- Copyable prompt defaults to the previous 24 hours, accepts a requested period and points at new REPORTING.md. Repo guidance covers all-organ evidence, event dates, deduplication and missing coverage without inventing completion history.
- Tests: 13 Python renderer/collection tests + 6 Scientist Node tests + 9 cockpit Node tests pass; both diff checks clean.
- Browser: Chromium at 390/768/1440px in light/dark passes columns, full-row expansion, keyboard focus, actual copied payload, typed direction/open-card preservation, selected-frame persistence, organ links and Back/Forward. No page errors or horizontal overflow. Physical devices not tested.
- Evidence: `.worktrees/scientist-cockpit-checks/{browser-results.json,browser-check.cjs,scientist-*-*.png,scientist.html,snapshot.json}`. The browser uses a captured published snapshot (14 organs, 11 valid feeds; Ears/DNA/Broca unavailable), not a claim of deployment.
- PR drafts: `.worktrees/scientist-cockpit-checks/scientist-pr.md` and `website-pr.md`. Scientist publication precedes the shell merge.
- Ship gate: vitals refreshed Heart, then `pyauto-heart readiness --json` at 2026-10-09T14:14:19.748312+00:00 returned RED (60). Exact RED reason: `release validation FAILED (stage integrate)`. Full readiness and vitals evidence are in the checks directory.
- Next: obtain the task-specific live shipping override after this passed evidence; record it and exact reasons in the four required sinks, then commit/push/open coordinated pending-release PRs. Tier judge; no merge/release authority.

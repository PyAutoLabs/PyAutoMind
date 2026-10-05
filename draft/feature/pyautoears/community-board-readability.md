# Community board readability and orchestration

Type: feature
Difficulty: medium
Priority: normal

Target: @PyAutoEars. Redesign the community board with readable expandable tables, author and evidence-backed maturity columns, prominent summary metrics and hub action, and a single-chat orchestration prompt. Match Heart/Pulse presentation patterns. Preserve evidence freshness and read-only boundaries.

## Original user request (verbatim)

- Make this more appealing on the eye and larger: 12 need attention · 0 unknown · 1 source gaps · 0 updates owed · 9 delivery unknown

- Remove this "Observed 2026-10-04T12:25:48.699026+00:00. Response states are heuristics; accepted does not mean delivered."

- Make Open Community Hub a more clickable button again more appealing on eyes.

- Each thing under "Needs you attention" is fine but its not pretty, this stuff should be formatted as lines I can reasd off
easily: PyAutoLabs/PyAutoGalaxy · Waiting since 2026-10-01T02:44:53+00:00, the copy triage prompt htings are greay and disgusting
just make them an icon, In fact I think the whole of thi ssection should display as table with drop down stuff in the style
of whats on heart which will make it way more readable. 

- I would like to see GitHub issue author names in the table above.

- Similar to PyAutoPulse There should be a go to all encompassing prompt at the top which is to deal with all the communtiy stuff
in one orchestrator AI chat with delegation wtc.

- good to have Community activity, means I can see history of complete stuff, but agian add author names and make it the same
table format as above. 

- Put this at very bottom also I guess more colorful easy to read table: Listening coverage

- The "Following through" seems broken? Whats is for at the very least it should take up a lot less space. 

- I think for the table displaing all active issues chats and whatnot on the discussions, along side author name
an entry which also gives a sense of maturity (E.g. issue versus plan versus PR is raised) would also be good.

## Proposed plan — awaiting approval

1. Larger colored metric tiles, a prominent Community Hub button and top-level single-chat community check-in prompt with optional direction and bounded delegation.
2. Heart-style expandable conversation tables for attention, unknowns and activity: topic, repository, author, type, progress, readable waiting age and icon actions.
3. Display evidence-backed maturity (discussion/issue, plan recorded where explicitly linked, PR open, merged awaiting release, available). Keep source type, response state and delivery progress distinct. Missing evidence stays unknown; no maturity inferred from accepted answers or prose.
4. Put delivery evidence in expandable row details and reduce Following through to a collapsed summary. Put a colored coverage table last. Remove the requested observation/heuristic sentence; retain stale alerts and machine-readable freshness.
5. Validate rendering, evidence semantics, accessibility, clipboard fallback, mobile layouts and light/dark themes; open a reviewable PR.

Tier: undeclared — merge mode: human /prm.

### Detailed implementation

- `ears/board.py`: extract reusable metric, conversation-table, icon-copy, date and maturity presentation helpers from `render`. Reuse Brain's theme and Heart's expandable-row visual pattern locally. Render escaped author usernames already in snapshots. Put exact timestamps in details/tooltips and short dates/ages in rows. Keep all prompt text selectable when clipboard access fails. Preserve state/badge contracts and stale handling while replacing the old paragraph status selector with a dedicated target.
- Add a top check-in prompt using Brain's Community conductor: inspect all attention items, unknown coverage, activity and delivery updates; prioritize and delegate independent investigations when appropriate; collect findings and draft replies in one ongoing chat; route implementation through the existing workflow. The copied prompt does not itself post replies or launch work.
- `ears/followthrough.py`, `ears/collect.py`, `REFERENCE.md`, only as needed for maturity: expose linked-plan evidence through an optional, validated, backward-compatible projection; consume explicit public links and authoritative Mind records rather than guessing from titles. Keep delivery semantics unchanged, including merged versus released and stale suppression. Existing issue/PR kinds remain available even without a delivery link.
- `tests/test_ears.py`, `tests/test_followthrough.py`, `tests/test_listening.py`: targeted coverage for author rendering/escaping, no false plan/PR advancement, optional-field compatibility, stale/unknown handling and table grouping.
- `tests/board_browser.py`: adapt existing browser smoke to expandable tables/icon actions; check keyboard access, clipboard success/denial, mobile/desktop overflow and light/dark screenshots.
- Run repository pytest suite, validate generated `state.json` using Brain `board/_state.py`, and inspect browser screenshots. Update README/REFERENCE only where user interaction or the projection contract changes.

### Workflow and branch survey

Feature Agent: direct, medium task; library workflow (`start_library` then `ship_library`); no matching Memory context returned.
Primary repo: PyAutoEars, `/home/jammy/Code/PyAutoLabs/organs/PyAutoEars`.
Survey: main, clean, up to date with origin/main; only local branch is main; one canonical worktree; conflict guard returned clear.
Proposed branch: `feature/community-board-readability`.
Use the standard worktree helper after approval, honoring the workspace path constraint.
Heart at entry: STALE — Release STALE; monitoring RED; planning allowed by entry gate. Re-read at ship time.
No implementation files edited and no issue or PR created before plan approval.

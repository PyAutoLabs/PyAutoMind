# Scientist Live Feed
Issued: 2026-10-13
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/83
Difficulty: medium
Consequence: judge
Status: approved

Target: @PyAutoScientist only for first implementation; MyScientist adoption later.

## Original request
next on both PYAuto and My I want to put a new section on the Scientist Dashboard between Projects and Dashboards called Live Feed. This would be a single live feed of all activity, which therefroe updates frequenrly when any work is done. It should say what board it is associate with and as the name suggestions really act as a live feed to know what work is being done. only implement on PYAutoScietist for now and first do some planning and back and forth with me on how we should set it up noting we need to avoid walls of text and information overload

## Discussion draft, not implementation approval
Place Live Feed between Projects and Dashboards. Propose five concise newest-first rows with board label/link, short factual activity text and event time; expand details on demand. Group repeated progress updates for the same task. Include starts, meaningful progress, blockers and completions; exclude routine refreshes and unchanged checks. Propose one-minute foreground refresh with last-checked time, freshness/coverage disclosure and stable reading position.

Existing Scientist REPORTING.md distinguishes owner event timestamps from feed generation times and current status from history. overview.js currently polls state feeds every 60 seconds; these are not universal event streams. Determine which owner records offer durable IDs, timestamps and deep links before promising all-activity coverage. Scientist can aggregate existing published evidence first; any missing producer event contracts require separately agreed scope, not hidden cross-organ changes. Do not manufacture history from snapshot refresh timestamps. Preserve private-source boundaries on public Pages.

Open choices: default activity granularity, five versus more visible rows, grouping and history depth, refresh latency and behavior on new entries, and honest first-version coverage. No source changes, deployment, collectors or recurring workflows authorized in this planning conversation. Route agreed design through start-dev branch survey and setup before implementation.

## Agreed design — 2026-10-13
The user chose ongoing work, grouped by task, and approved five newest-first rows with Show more, expandable history, one-minute browser refresh and a New updates button while reading expanded/older entries. Implementation is still limited to PyAutoScientist, not MyScientist/Embryo deployment.

## Evidence and proposed first implementation
Audited all 14 current public state.json feeds; none includes per-item event timestamps. These are current-state feeds and cannot supply a true event timeline. Supplemental board.json probes found DNA records with precise created times; Brain history and Gut voided lists were empty. Other missing board.json endpoints do not prove their repositories lack records. GitHub issue81 and its Shipped comment demonstrate durable IDs, event timestamps and evidence links for development history. Evidence snapshots are in tmp/scientist-live-feed/ (not for public republication).

High-level plan for approval:
1. Implement the agreed grouped feed in canonical Scientist only, between Projects and Dashboards.
2. Start with public recorded development tasks: issues, linked PR stages, recognized progress reports, blockers and merges. Resolve registered organ repositories to their own board; library/workspace development belongs to Mind with a separate repository label. Unproven issue/PR associations remain separate. Do not claim issue creation is execution start, closed PR is merged, or merge is publication.
3. Collect in Scientist at a proposed five-minute cadence; the browser checks the resulting static feed every minute while visible. Collection is best effort, not a one-minute delivery guarantee. Show last successful collection and per-source gaps. No client credential or per-viewer GitHub polling.
4. Publish bounded public evidence only, keeping owner records authoritative. No private checkout material, prompts or raw comment transcripts. Include recognized structured progress as concise factual summaries; unstructured comments become a generic Progress update recorded link, never an invented summary.
5. First-version label: Recorded development activity. Scientific run progress, full organ operations and DNA audit adaptation remain explicitly outside this initial PR. Later phases require dated owner records and separate scope approval. No claim of all-activity coverage.
6. Test event grouping and ordering, duplicate suppression, incomplete collection, privacy boundaries, stale data, reading-position stability, keyboard access and responsive layout.
Tier: judge — merge mode: human /prm.

Detailed implementation proposal:
- scripts/activity_feed.py (new): explicit public source allowlist derived from registered body-map identities; bounded issue/PR collection and event normalization (event ID, task key, board, repository, event time, kind, short summary, source URL). Group through explicit links only. Keep created/started, closed/merged and published distinctions; no timestamps inferred from feed rebuilds. Authenticate only within trusted CI; verify visibility of every GitHub repository before export. Fail partial with coverage receipts, never replace a failed source with empty success.
- Persist a bounded derived cache on a dedicated Scientist artifact branch to retain observed task history and conditional-fetch cursors across runner lifetimes; retain 30 days with explicit item caps/truncation coverage. This is a rebuildable index, not another authoritative task registry. Include current active tasks when source budgets allow; initial backfill covers seven days and labels its cutoff. Exact API/request budget to be fixture-tested before enabling collection.
- scripts/organism_board.py: render initial accessible feed snapshot in canonical mode between project resources and dashboards; leave independent-instance rendering unchanged this phase.
- scripts/live_feed.js (new), integrated beside overview.js: static same-origin activity.json, foreground 60-second refresh, stable task IDs/disclosures, five rows then paginated Show more, New updates buffer whenever focus/scroll/expansion indicates reading. No reordering underneath an expanded task; pause hidden-tab fetches.
- .github/workflows/organism_board.yml: approved five-minute collection/publication schedule replacing the current six-hour cadence; reuse existing Pages pipeline and explicit least-permission public read access. Never treat repeated no-change collections as activity. Explain best-effort freshness and collection failures.
- REPORTING.md/README.md: specify coverage, source ownership, collection-versus-event times, public-only export, retention and latency. No model-generated prose on refresh.
- Tests: offline recorded fixtures for issue/PR linkage, reopening, comments edited versus newly posted, merged versus closed, duplicate events, invalid times, missing/private sources, pagination/caps, malicious strings and safe links. Browser fixtures exercise stable updates, expanded history, focus, Show more, mobile/desktop, light/dark and no-JavaScript snapshot. No scientific compute or production profiling.

## Preliminary branch survey
PyAutoScientist main is clean; origin/main contains PR82 but local main needs fast-forward before setup. No active repo claim. Existing unregistered DNA worktree is preserved. Recent branches: main, feature/pyautodna-stack-management, feature/map-block-autolens-visualization. Proposed branch feature/scientist-live-feed and workspace-contained bundle .worktrees/scientist-live-feed/PyAutoScientist. No source edits, issue or task worktree created during planning. Recheck claims after implementation-plan approval.

## Planning gate
Read-only Heart entry: STALE (release STALE; monitoring RED); entry helper exit1 permits planning. No ship readiness claimed. Implementation-plan approval must settle the reduced first-version coverage and five-minute collector before create-issue/start-workspace. Design preferences already approved above remain approved.

## Implementation approval
2026-10-13: User approved the presented development-activity scope, five-minute collection and human /prm merge mode with “yeah do it”. Earlier design choices remain approved.

## Shipping handoff — 2026-10-13
PR: https://github.com/PyAutoLabs/PyAutoScientist/pull/84
Head: c1eeff1a3926ecc122587950e04ed065827566b7
Issue: PyAutoScientist#83. Branch feature/scientist-live-feed; clean pushed worktree .worktrees/scientist-live-feed/PyAutoScientist. Canonical Scientist only; MyScientist/Embryo unchanged. Five grouped rows, expanding task history, Show more, stable reading buffer and same-origin minute polling implemented.

Collector supports 50 registered repo identities, verifies current public visibility from owner catalogs, normalizes issue/comment/PR records without exporting raw comments, groups explicit same-repository closing references only, and bounds collection at 120 seconds plus request limits (PAT180/default-token60). Source gaps are explicit. Live initial multi-repo pilot found busy-source budget exhaustion; fixed by retaining partial verified events and reusing normalized PR revisions, without advancing incomplete source cursors. Source catalog pagination cap and issue/comment cap remain explicit coverage limitations. Scientific run progress is outside this PR.

Validation: 162 full Python tests before final mapping regression; 49 final targeted collector/renderer/instance tests (including added regression); 7 existing JS tests; six real-browser viewport/theme cases plus no-JS snapshot; workflow YAML, JS syntax and diff checks. Read-only PyAutoScientist API pilot: 37 tasks, complete source coverage, 37 calls. This is not full-organism production validation. Source CI Board tests run38468322699 in progress at handoff; no CI waiter.

Evidence: tmp/scientist-live-feed/{python-tests.log,final-targeted-tests.log,node-tests.log,heart-readiness.json,pilot-feed.json,pilot-cache.json,preview.html,preview-feed.png,browser/}. Preview uses only the Scientist repository pilot. Heart readiness STALE solely `release validation incomplete: no rehearsal for current source`, no red/yellow reasons; ordinary development ship permitted. No production profiling or science executed.

After human /prm: judge every source CI leg, merge, dispatch Scientist organism_board.yml on main (approved five-minute publication feature), verify its artifact-cache branch and Pages activity.json. Initial backfill may span multiple collections and must show honest gaps. Verify live canonical section placement and no instance rollout, then close issue/lifecycle, regenerate Mind dashboard, remove worktree. No source merge, schedule activation or live publication occurred during implementation.

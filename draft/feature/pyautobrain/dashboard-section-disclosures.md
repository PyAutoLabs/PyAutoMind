# Dashboard slogan order and collapsible sections

Type: feature
Consequence: judge

Primary owner: @PyAutoBrain. Consumers: @PyAutoMind @PyAutoCortex @PyAutoMemory @PyAutoHeart @PyAutoHands @PyAutoPulse @PyAutoNerves @PyAutoGut @PyAutoScientist @PyAutoEyes @PyAutoInsight @PyAutoEars.

## Original request (verbatim)

- All dashboards have adopted a standard API now where they have big buttons at the top,
corresponding to the titled sections that come in the dashboard. I want to make two changes across the
standard layout of all dashboards:

1) I want the box which has the slogan (e.,g. "Ship with your Hands) to be above the buttons, so swap them round
across all dashboards.

2) I want each header (e.g. on PyAutohands its Libraries, Release train) to be clickable to drop down. Currently,
there are dashboards where a given head is a huge amount of text and this means navigating it is cumbersome.
These headers, where possible, can include information that informs us if we should check it. For example on 
PyAutoHeart "Observed checks" could have a yellow or red tick if any item is yellow or red, others could have 
the number of tasks (e.g. "Start Here" on PyAutoMind could have an 18 to say there are 18 task under it).

## Proposed acceptance criteria

- All 13 boards registered in Brain's board policy show their slogan/context box before section navigation.
- Major titled sections use a shared accessible disclosure, initially collapsed; headers retain their anchors and meaningful counts/status while closed.
- Navigation and direct fragment links reveal the target section, including nested targets. Keyboard interaction and existing copy controls continue to work.
- Counts are computed by owning renderers, including Mind Start Here. Heart Observed checks exposes worst observed status without conflating monitoring with release readiness. Missing evidence is never shown as green or zero.
- Update Brain's navigation contract and track adoption and regenerated/published artifacts for every consumer.
- Validate representative populated/empty/unknown states, anchor navigation, keyboard operation, narrow/wide screens and light/dark themes.

## Delivery

Plan approval required before source edits. Shared Brain implementation first, then owner migrations in bounded dependent PRs; human merge via /prm. Preserve unrelated dirty files and resolve repository claims before implementation.

## Detailed plan awaiting approval

1. Extend `PyAutoBrain/board/_theme.py` with a shared top-layout composition that emits hero, orchestration panel, then navigation cards. Keep existing callers compatible until migrated; preserve panel copy payloads and freshness controls. The requested slogan box is the orchestration panel, distinct from the logo masthead tagline.
2. Add a shared native `details`/`summary` section component with heading semantics, stable IDs, chevrons, optional owner-supplied counts and labelled status badges. Default major content sections to collapsed. Keep the slogan panel visible. Shared JavaScript opens ancestor disclosures for initial URL fragments, hash changes and navigation clicks (including repeat clicks on the current fragment); preserve nested copy/disclosure behavior. Use native keyboard interaction, visible focus, and a print rule that exposes content.
3. Adopt in Brain `board/_board.py`, Mind `agents/conductors/intake/_intake.py`, and Cortex `agents/conductors/cortex/_cortex.py`. Derive Mind Start Here count from the actual rendered collection. Update `docs/board-navigation.md` with composition, section, count and status contracts, plus affected-consumer coverage.
4. Migrate owner renderers in dependent, bounded PRs: Heart `heart/dashboard.py`; Hands `autohands/board.py`; Memory/Nerves/Gut `scripts/board.py`; Pulse `pulse/board.py`; Ears `ears/board.py` and `ears/presentation.py`; Eyes `eyes/board.py`; Insight `insight/board.py` and `insight/theme.py`; Scientist `scripts/organism_board.py`. Audit each owner's major headings and existing details to avoid double wrapping. Heart aggregates observed-check status using existing owner semantics: red takes precedence over yellow, with stale/unknown explicit; do not substitute the release verdict. Counts/status without a reliable source are omitted or explicitly unknown.
5. Test shared ordering and disclosure behavior, meaningful owner count/status fixtures and retained anchors. Run applicable renderer suites and browser checks at 390, 768, 820, 1024 and 1440px in light/dark, with keyboard, direct/nested anchors, copy actions, empty/unknown states and page overflow. Regenerate consumer artifacts using their existing renderers; after human merges, refresh and verify each published board. Track source, artifact and publication adoption separately.

Tier: judge — merge mode: human /prm.

## Initial survey (2026-10-07)

All 13 owner checkouts are on main. Brain has an untracked delegation log; Mind has this new prompt; Cortex has seven unrelated modified/untracked paths; Eyes has three untracked directories. Other owner checkouts are clean. Several local mains trail their cached origin refs and must be refreshed in task setup. No existing active task matches this request.

`worktree_check_conflict` reports Scientist claimed by `community-pages` (PR 48). Defer that consumer until the claim clears; do not bypass it. It also reports unregistered Brain/Mind/Heart/Hands worktrees that must be reconciled or shown unrelated before claiming those repos. Suggested branch: `feature/dashboard-section-disclosures`; use an isolated task checkout within the permitted workspace during setup.

FeatureDecision routes through start_workspace/ship_workspace and recommends phased delivery due to the 13-repository scope. Proposed phases are shared component plus Brain-owned renderers, downstream owner migrations, then publication verification. Heart entry result: STALE (release STALE, monitoring RED); development planning permitted by the entry contract. Plan approval and issue registration remain pending; no dashboard source edits made.

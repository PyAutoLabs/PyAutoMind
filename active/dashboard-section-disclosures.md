# Dashboard slogan order and collapsible sections

Type: feature
Issued: 2026-10-07
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/490
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

## Implementation handoff — 2026-10-07

Plan approved by the human (“I approve, go”). Implementation is staged, not committed or pushed, on `feature/dashboard-section-disclosures` in `/home/jammy/Code/PyAutoLabs/.worktrees/dashboard-section-disclosures`.

- Implemented 12 boards: Brain, Mind, Cortex, Heart, Hands, Memory, Nerves, Gut, Pulse, Eyes and Insight plus Ears. Scientist remains deferred: `community-pages` owns that repo (PR 48).
- Brain `board/_theme.py::section_layout` composes the slogan panel above navigation and wraps major heading groups in native collapsed disclosures. Owners retain IDs/content, meaningful counts, status and copy payloads. Footer navigation stays outside disclosures. Shared JS handles initial/repeated/deep links and print state; keyboard controls are native.
- Mind counts unique actually displayed Start Here tasks. Heart aggregates check states separately from release readiness. Hands omits counts when collection failed. Multiple navigation metrics keep their labels.
- Renderer-owned artifacts regenerated in Mind, Cortex, Eyes, Pulse and Insight. Other owners render at publish time; local fixtures/real Nerves snapshots validate their adoption. Nothing has been published.

### Validation

- Brain full suite: 1,284 passed, six initial failures. Five Node clipboard failures fixed by guarding browser-only initialization; the grouped-checkout fixture failure was inherited `PYAUTO_MIND`. A rerun of both affected files plus disclosure regressions with that override unset passed all 15 tests. Focused renderer/theme suite: 289 passed before final added regressions; later layout/Mind/Hands tests passed.
- Heart: 166 dashboard tests passed; seven disclosure tests passed including new status precedence coverage.
- Hands: full suite 475 passed; final board suite 27 passed including failed-collection count coverage.
- Memory 275; Gut 25; Pulse 193; Eyes 82; Insight 79; Ears 97; Nerves full suite 241 passed.
- Chromium: 120 cases across 12 boards, five widths and light/dark. Order, collapsed defaults, anchor/deep-link/repeated navigation, keyboard, clipboard and overflow passed. Representative screenshot inspected.
- Sphinx build passed with zero warnings. Ruff check/format passed for Pulse, Eyes, Insight. Pulse/Insight offline artifact+contract checks passed; Eyes live manifest/figure URL and cockpit checks passed. Cortex structural check passed. All diffs passed whitespace checks.
- Evidence: workspace `tmp/dashboard-sections/` contains individual test logs, `browser-final/browser-results.json`, screenshots, renderer fixtures, `canonical-readiness.json`, and 12 prepared PR descriptions under `pr-drafts/`.

### Shipping gate and next steps

Canonical-workspace Heart readiness is **RED**. Exact RED reasons:
- PyAutoFit: 5 commit(s) behind origin
- PyAutoGalaxy: 12 commit(s) behind origin
- PyAutoLens: 8 commit(s) behind origin

No override has been granted. The earlier plan approval predates these reasons and is not the required contemporaneous development-shipping override. Source commits, pushes and PR-open are blocked by `skills/ship_workspace/ship_workspace.md` and `AUTONOMY.md` → Human override for Heart RED (development only). Leave the staged implementation intact.

Next: obtain a task-specific override for Brain #490, record it in the four required sinks, refresh branch/claim state, commit and open the prepared dependent PRs (Brain API first; consumer CI needs it). Human /prm remains the merge mode. Update generated artifacts after any intervening ledger changes. Resume Scientist only after community-pages releases its claim. After merges refresh the existing publishers and verify all 13 live boards before closing the initiative.

No unrelated local files, science ledgers or active campaigns were edited. Canonical Mind has unrelated untracked research drafts; do not stage them.

## Heart RED override — authorized 2026-10-07

The human replied “I authorize” to the explicit development-only Heart RED override request for Brain #490. Authorized: commit, push and open the task PRs. Merge/release are not authorized.

Exact current RED reasons:
- PyAutoFit: 5 commit(s) behind origin
- PyAutoGalaxy: 12 commit(s) behind origin
- PyAutoLens: 8 commit(s) behind origin

Validation: renderer and owner suites passed (Brain full-run failures resolved by focused reruns); 120 Chromium cases passed; Sphinx zero warnings; applicable Ruff, artifact and contract checks passed. Full evidence is recorded in the implementation handoff.

## PR-open handoff — 2026-10-07

The human-authorized development ship is complete for the 12 unblocked dashboards. The implementation is committed and pushed; no PR was merged and no page was published.

| Repository | PR | Commit | Review state |
|---|---|---|---|
| PyAutoBrain | https://github.com/PyAutoLabs/PyAutoBrain/pull/491 | `cbe0701f` | Ready for review |
| PyAutoMind | https://github.com/PyAutoLabs/PyAutoMind/pull/479 | `91c4f058` | Draft; depends on Brain #491 |
| PyAutoCortex | https://github.com/PyAutoLabs/PyAutoCortex/pull/58 | `7bfcbaeb` | Draft; depends on Brain #491 |
| PyAutoMemory | https://github.com/PyAutoLabs/PyAutoMemory/pull/123 | `c65eebc8` | Draft; depends on Brain #491 |
| PyAutoHeart | https://github.com/PyAutoLabs/PyAutoHeart/pull/291 | `6eb36641` | Draft; depends on Brain #491 |
| PyAutoHands | https://github.com/PyAutoLabs/PyAutoHands/pull/307 | `fd9ad49f` | Draft; depends on Brain #491 |
| PyAutoPulse | https://github.com/PyAutoLabs/PyAutoPulse/pull/24 | `fdabed32` | Draft; depends on Brain #491 |
| PyAutoNerves | https://github.com/PyAutoLabs/PyAutoNerves/pull/193 | `e68ab996` | Draft; depends on Brain #491 |
| PyAutoGut | https://github.com/PyAutoLabs/PyAutoGut/pull/27 | `aefd1afd` | Draft; depends on Brain #491 |
| PyAutoEyes | https://github.com/PyAutoLabs/PyAutoEyes/pull/23 | `3965eced` | Draft; depends on Brain #491 |
| PyAutoInsight | https://github.com/PyAutoLabs/PyAutoInsight/pull/11 | `fba6864b` | Draft; depends on Brain #491 |
| PyAutoEars | https://github.com/PyAutoLabs/PyAutoEars/pull/21 | `0fb3d02a` | Draft; depends on Brain #491 |

Merge Brain #491 first through human /prm. The 11 dependent drafts require that shared API on Brain main; then rerun their checks, refresh generated artifacts if ledger/evidence inputs moved, and mark them ready for review. Core CI was checked once: docs passed; Python 3.12 and 3.13 tests were running. No CI watcher or scheduled continuation was armed.

After merging current upstream refreshes, 40 additional Chromium cases passed for Mind, Pulse, Eyes and Insight. Pulse/Insight offline checks passed again. Earlier validation and exact authorized RED reasons remain recorded above and in every PR body.

Scientist remains deferred under the community-pages claim. The umbrella issue remains open until that consumer is migrated and all 13 published boards are verified. Worktrees are retained under `/home/jammy/Code/PyAutoLabs/.worktrees/dashboard-section-disclosures` for review and /prm.

## Scientist migration — 2026-10-07

The human released PyAutoScientist from `community-pages` (PyAutoScientist#48 merged 2026-10-07T10:05Z) and moved it under #490. Brain #491 and the 11 dependent PRs are merged and their 12 live boards verified.

| Repository | PR | Commit | Review state |
|---|---|---|---|
| PyAutoScientist | https://github.com/PyAutoLabs/PyAutoScientist/pull/49 | `433538b3` | Ready for review |

`scripts/organism_board.py` passes through `section_layout`. The slogan panel sits above the organ-board cards, and the verdict banner stays visible. Organ rows live in a collapsed "Organ dashboards" section (`#dashboards`, rows `#board-<organ>`). Its header shows `N of M reporting` and the Heart's own word, which is "unknown" when the Heart can't be read. Validation: 13 tests passed against Brain main, and 40 Chromium cases passed (4 fixtures × 5 widths × light/dark). Next: human /prm, then verify the published Scientist board and close #490.

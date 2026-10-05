# Standard board banner and navigation rollout

All 13 published boards now use the shared logo banner followed by prominent section navigation. Counts are optional, and each board retains its own evidence and action meanings. Ears no longer shows the unclear "STALE — refresh required before judging the queue" wording; it shows a readable last-checked timestamp and a plain explanation below the cards when needed.

## Merged implementation

- PyAutoBrain#464: shared API and Brain, Mind, Cortex adoption.
- PyAutoEars#12: https://github.com/PyAutoLabs/PyAutoEars/pull/12
- PyAutoMemory#116: https://github.com/PyAutoLabs/PyAutoMemory/pull/116
- PyAutoHeart#283: https://github.com/PyAutoLabs/PyAutoHeart/pull/283
- PyAutoHands#299: https://github.com/PyAutoLabs/PyAutoHands/pull/299
- PyAutoPulse#15: https://github.com/PyAutoLabs/PyAutoPulse/pull/15
- PyAutoNerves#186: https://github.com/PyAutoLabs/PyAutoNerves/pull/186
- PyAutoGut#22: https://github.com/PyAutoLabs/PyAutoGut/pull/22
- PyAutoScientist#43: https://github.com/PyAutoLabs/PyAutoScientist/pull/43
- PyAutoEyes#17: https://github.com/PyAutoLabs/PyAutoEyes/pull/17
- PyAutoInsight#5: https://github.com/PyAutoLabs/PyAutoInsight/pull/5

## Validation and publication

1,186 core tests and 2,655 consumer tests passed. Every CI workflow and job on each PR head passed before merging. Browser evidence covers five viewport widths and light/dark for all owners, plus keyboard section navigation. The Ears browser suite also checks clipboard actions, expiry and overflow. Heart was GREEN before shipping.

All 13 live Pages URLs were fetched after publication and contain the shared navigation. Their actual published HTML passed 130 Chromium cases (five widths × two themes): header order, card geometry, anchor targets, keyboard activation and no page overflow. Cortex was explicitly regenerated through its existing dashboard refresh workflow. Local raw evidence is retained at `tmp/board-navigation/`, including CI results, test logs, rendered pages, screenshots and `live-status.json`.

Core and consumer issues closed; claims released; dashboards regenerated as part of this close-out. Existing prompt panels retain their payloads and remain a separate task.

Reconciliation left the unrelated `draft/feature/pyautobrain/batch_slice.md` suspect unchanged: resemblance is not proof of coverage. Its follow-up door is `pyauto-brain intake reconcile draft/feature/pyautobrain`.

## Original prompt

# Standard board banners and Ears-style navigation

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoEars
- PyAutoMemory
- PyAutoEyes
- PyAutoHeart
- PyAutoHands
- PyAutoPulse
- PyAutoInsight
- PyAutoNerves
- PyAutoGut
- PyAutoScientist
Difficulty: large
Autonomy: supervised
Priority: normal
Status: draft
Consequence: judge
Filed: 2026-10-05

## Original user request (verbatim)

I like the Ears format, we have the banner and logo at the top, but then remove "STALE — refresh required before judging the queue" which is unclear text. Then it has the big buttons under it with all the individual tabs you can go to and click. I want every board to now adopt this format, you prob cant always put numbers in a tbutton but thats fine, its a nice API and standarizes all boards which is a severely lacking aspect

## Objective

Adopt a consistent Ears-inspired top structure across all 13 organism boards: each organ's logo/banner, then prominent linked navigation cards for its sections, with optional meaningful counts. Ship real renderer adoption, including independent layouts, rather than only a theme API or audit.

## Proposed behavior

- Reuse each organ's identity and the shared responsive sizing standard from PyAutoBrain PR #462.
- Navigation cards are semantic links to existing board sections/pages, matching Ears. Keep all sections available and preserve deep links; do not turn the content into hidden JavaScript-only tab panels.
- Cards have a clear label, optional count and optional short context. Unknown/missing/stale counts must not become a misleading zero; count-free cards are valid and visually balanced.
- Extract shared presentation into Brain with an explicit, small renderer API. Board owners supply labels, destinations and evidence-backed counts; the shared theme does not collect or reinterpret data.
- Remove the exact prominent Ears string "STALE — refresh required before judging the queue" and place readable freshness metadata after the navigation, e.g. "Last checked [time]. These figures may be out of date." Preserve existing stale/unknown machine semantics and response/action safeguards.
- Cover all 13 registry entries: Brain, Mind, Cortex, Memory, Eyes, Ears, Heart, Hands, Pulse, Insight, Nerves, Gut, Scientist. Mind/Cortex renderers are Brain-owned; the other owners need explicit adoption work.
- Existing orchestration-panel draft `draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md` remains separate; this task does not duplicate its prompt/payload redesign.

## Proposed phases for approval

1. Brain shared card renderer/CSS and adoption in its Brain, Mind and Cortex renderers. Brain merges first so downstream workflows can consume the API.
2. Adopt the reference in Ears (including freshness wording), then Memory, Heart, Hands, Pulse, Nerves, Gut and Scientist, preserving component semantics and organ-specific actions.
3. Adapt Eyes and Insight independent renderers, including their required sizing/overflow integration, then verify every board's published appearance after approved rollout. Keep cockpit shell/navigation unchanged while checking embedded behavior.

One issue/PR per affected repo or independently shippable phase. This prompt is the planning anchor; split execution prompts and record explicit dependencies before claiming implementation repos. Tier judge throughout; merge remains human /prm.

## Acceptance

- All 13 boards use the banner → navigation cards order; no stale banner interrupts it.
- Shared implementation covers cards with/without counts, safe escaped labels, useful destinations, optional context and visual status that does not confuse organ identity with health.
- Consistent desktop/tablet/phone and light/dark layout; accessible names, keyboard focus, touch targets and usable dense content. No new whole-page horizontal overflow.
- Existing deep links, tables, disclosures, copy payloads, data/freshness contracts and human approval requirements remain valid.
- Board-by-board completion matrix plus before/after browser evidence at 390, 768/820, 1024 and 1440px. Verify regeneration and publication, not merely source merge, before claiming a board is live.

Plan approval is required before source changes. The user has requested the feature but has not yet approved this proposed design/phasing or any merge/deployment.

## Planning survey

All source repos are on main; no active claims conflict. Memory and Hands are two commits behind their tracking refs and must refresh before worktree setup. Eyes has untracked dataset/, output/ and scripts/: preserve all of them and work in an isolated checkout. Brain's recent feature branches (tiered-auto-merge, abell-1201-point-mass, cortex-may-submit) do not claim Brain in active.md. Ears retains its merged community-board-readability branch. Proposed first branch: feature/board-navigation-core. Worktrees stay under .worktrees/ in this workspace.

## Detailed component plan

- `PyAutoBrain/board/_theme.py`: add a reusable navigation-card renderer accepting owner-supplied destinations, labels, optional counts and context, plus shared card CSS. Reuse hero, organ palettes and sizing tokens. Labels are escaped; destinations are validated local anchors or ordinary safe links. Counts are optional; missing data is not coerced to zero.
- `PyAutoBrain/board/_board.py`, `agents/conductors/intake/_intake.py`, `agents/conductors/cortex/_cortex.py`: put the cards directly after the banner, link to existing sections, preserve stable anchors and avoid competing duplicate metric rows. Add explicit IDs only where needed. Place freshness metadata below navigation with readable wording.
- `PyAutoEars/ears/board.py` and `ears/presentation.py`: replace duplicated metric markup with the shared component, preserve existing destinations, and remove the quoted stale banner. Coordinate the browser expiry handler as well as server-rendered wording so it cannot reinstate the removed text. Preserve snapshot and stale/unknown action semantics.
- Remaining shared consumers: `PyAutoMemory/scripts/board.py`, `PyAutoHeart/heart/dashboard.py`, `PyAutoHands/autohands/board.py`, `PyAutoPulse/pulse/board.py`, `PyAutoNerves/scripts/board.py`, `PyAutoGut/scripts/board.py`, `PyAutoScientist/scripts/organism_board.py`. Add section cards from each board's own current navigation/data; retain renderer ownership and domain actions.
- Independent consumers: `PyAutoEyes/eyes/board.py`, `PyAutoInsight/insight/board.py` and `insight/theme.py`. Adopt shared banner/card presentation without replacing their data models or disguising gallery/table overflow. Preserve locally owned content styling where compatible.
- Document the contract and a completion matrix in Brain. Add focused renderer tests for escaping, optional counts, live link targets and freshness semantics; browser checks for card navigation, keyboard focus, long labels, mobile reflow, light/dark, copied prompts and existing deep links.
- Source merging and live adoption are separate milestones. Existing refresh/publication workflows must regenerate HTML after Brain is available. Never report all boards live from the Brain merge alone; actual rollout is subject to its explicit authorization and existing publication mechanics.

## Approved execution

User approved this plan and authorized /prm on 2026-10-05. Core merged as PyAutoBrain#464; ten per-organ consumer tasks are active.

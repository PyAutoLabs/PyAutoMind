# Scientist board navigation

Epic: scientist-adoption-pilot

Merged 2026-10-11 following explicit human `$prm`: canonical Scientist-first footer order plus shared organ footers on Scientist, Broca, Eyes, Insight, Pulse and Ears. Scientist footer sits below dashboard cards. Existing records and evidence preserved. Brain merged first; every claimed feature head is an ancestor of origin/main.

- PyAutoBrain: https://github.com/PyAutoLabs/PyAutoBrain/pull/515
- PyAutoScientist: https://github.com/PyAutoLabs/PyAutoScientist/pull/60
- PyAutoBroca: https://github.com/PyAutoLabs/PyAutoBroca/pull/6
- PyAutoEyes: https://github.com/PyAutoLabs/PyAutoEyes/pull/28
- PyAutoInsight: https://github.com/PyAutoLabs/PyAutoInsight/pull/25
- PyAutoPulse: https://github.com/PyAutoLabs/PyAutoPulse/pull/50
- PyAutoEars: https://github.com/PyAutoLabs/PyAutoEars/pull/29

Validation: 932 Python tests,6 Node,60 cross-consumer footer browser cases and6 Scientist interaction/theme cases plus no-JS, strict Sphinx, required organ checks. Independent review CLEAN. Every exact-head CI test/build/matrix job passed. Broca deploy was intentionally skipped on its PR by the main-only condition; build/tests passed. Heart at ship: STALE solely for absent release rehearsal.

Implementation complete. Publication across all15 boards is not claimed: owning main workflows may deploy automatically; remaining dispatch/live verification is recorded in draft/maintenance/pyautoscientist/publish_scientist_board_navigation.md under the same epic. No package release obligation.

Evidence: tmp/scientist-board-navigation/evidence/ (local, untracked), including merge-ci.json and merge-proof.json.

## Original prompt

# Scientist-first board navigation

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/59
Epic: scientist-adoption-pilot
Consequence: judge
Difficulty: small

Sizing rationale: the automated estimate counts seven repositories; this is one canonical order change and six existing-footer call sites, shipped as dependent per-repository PRs. No new API or domain capability. Keep one bounded coordinated task.

## Original request

Next, quick polish put the list of all organs at the bottom of Scientist and make sure Scientist is first in all the other boards

## Plan

- Put Scientist first in the canonical board registry owned by @PyAutoBrain.
- Add the existing shared board footer below content in @PyAutoScientist, @PyAutoBroca, @PyAutoEyes, @PyAutoInsight, @PyAutoPulse and @PyAutoEars. Other consumers already render it from the canonical registry.
- Preserve owner-provided URLs, content, evidence timestamps, project cards and current-board exclusion; keep instance configuration separate.
- Validate existing renderer suites, canonical ordering, bottom placement and mobile layout. Regenerate required tracked board artifacts without collecting new evidence.
- Open dependent PRs, Brain first; record board refresh/publication as the post-merge step.

Tier: judge — merge mode: human /prm.

## Detailed implementation

Brain config/policy.yaml board.boards supplies ordering; move organism first and update existing order assertions in tests/test_board_theme.py plus docs/board-navigation.md. Use board/_theme.py boards_footer and board_links in each missing consumer renderer (scripts/organism_board.py, broca/board.py, eyes/board.py, insight/board.py, pulse/board.py, ears/board.py). Keep footer outside content disclosures. Use each owner’s existing hosting configuration; add an explicit defaulted option only where no board base exists. Scientist continues to derive its base from snapshot owner. No new registry, health semantics, automatic activation or source ownership changes.

Branch survey: canonical main checkouts; Eyes has untracked dataset/output/scripts, left untouched. No active claims. Old unregistered worktrees remain untouched. Use isolated .worktrees/scientist-board-navigation and branch feature/scientist-board-navigation. Existing initiative authorization covers routine implementation. Tests: affected Brain board/render tests and each consumer suite, checks mandated by repo instructions, browser footer wrapping and no-JS links. Capture fresh Heart verdict and independent review before ship.

## Implemented — awaiting merge and publication

- [PyAutoBrain](https://github.com/PyAutoLabs/PyAutoBrain/pull/515)
- [PyAutoScientist](https://github.com/PyAutoLabs/PyAutoScientist/pull/60)
- [PyAutoBroca](https://github.com/PyAutoLabs/PyAutoBroca/pull/6)
- [PyAutoEyes](https://github.com/PyAutoLabs/PyAutoEyes/pull/28)
- [PyAutoInsight](https://github.com/PyAutoLabs/PyAutoInsight/pull/25)
- [PyAutoPulse](https://github.com/PyAutoLabs/PyAutoPulse/pull/50)
- [PyAutoEars](https://github.com/PyAutoLabs/PyAutoEars/pull/29)

Merge Brain first, then the six consumers. Independent review CLEAN; 932 Python tests,6 Node,60 footer browser cases,6 Scientist responsive/theme interaction cases plus no-JavaScript, strict Sphinx, Ruff and owner record/contract checks passed. Four regenerated tracked dashboards differ only by their new footer; evidence bytes preserved. Heart STALE: `release validation incomplete: no rehearsal for current source`, no RED/YELLOW reasons. Ears Python browser runner lacked the playwright module; its changed footer was verified with the available Node Playwright runtime and full Python suite.

### Publication checklist (after human /prm and publish)

- Brain: `brain_board.yml`.
- Mind/Cortex: `dashboard_refresh.yml`, then confirm `pages_dashboard.yml`.
- Memory: `knowledge_board.yml`.
- Eyes/Pulse/Insight: `pages_dashboard.yml` publishes regenerated tracked HTML; their normal refresh also adopts the new Brain policy.
- Ears/Broca/DNA: `pages.yml`.
- Heart: `heart-health.yml` (includes checks and board publication).
- Hands: `release_board.yml`; Nerves: `nerves_board.yml`; Gut: `gut_board.yml`.
- Scientist: `organism_board.yml`.
- Verify live footer first link Scientist on the other14 boards and all14 organ links below Scientist’s dashboard cards. Retain task until merge/publication outcome is recorded; do not mistake open PRs for a live change.

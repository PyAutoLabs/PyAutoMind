# Scientist-first board navigation

Type: feature
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

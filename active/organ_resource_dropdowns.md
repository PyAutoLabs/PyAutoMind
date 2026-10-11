# Heart and Broca resource destinations

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/65
Epic: scientist-adoption-pilot
Difficulty: medium
Consequence: judge

## Original request

do these next, and then we'll do the intedepent thing

## Plan

Implement the recorded Heart test-workspace and Broca communication-resource dropdown slices as one coordinated presentation contract across @PyAutoHeart, @PyAutoBroca and @PyAutoScientist. No Brain source changes: its local-discovery PR#518 remains a separate pending task. Broca documents expanded communication ownership locally; canonical role-description rollout remains its separate contract task pending Brain availability.

Scientist exports an offline public resource catalogue from its existing project relationship model plus canonical Mind identities. Consumers retain a derived catalogue snapshot for offline rendering, never a second hand-maintained relationship map; refresh commands and provenance documented. Shared resource IDs deduplicate shared dependencies. Private projects/resources never enter the catalogue. Stable resource-ID anchors connect Scientist to owning boards.

Heart renders a native resource details row per tests relationship, grouping context by explicit project names and linking source/CI evidence from existing cached repo observations. Show unknown and stale honestly, no invented counts or readiness change. Broca similarly renders docs/tutorial/workspace/assistant resources, preserving existing assistant evidence/history and separating recorded evaluations from unknown explanatory quality for other resource types. Source material stays project-owned. Use shared theme and hash opening that opens ancestor disclosures; no-JS remains usable.

Detailed files: Scientist scripts/project_resources.py and organism_board.py (offline export and deep links); Heart heart/dashboard.py plus resource renderer/module and public catalogue fixture; Broca broca/board.py plus resource renderer/module and public catalogue fixture, ownership guidance. Refresh mirrors from canonical source using exported JSON; board publishing renders saved catalogue without collection. Tests cover projection/privacy/deduplication, absent/failed/stale evidence, anchors and deep-link opening; browser responsive/keyboard/no-JS checks, existing suites, independent review. No release policy, science scripts, paid runs or deployment dispatch. Tier judge; human /prm.

Branch survey: three clean main checkouts, Heart fast-forwarded; no active claims for these repos. feature/organ-resource-dropdowns in .worktrees/organ-resource-dropdowns. Independent-starter continuation deferred until these destination views are complete. Original detailed acceptance remains in the Heart and Broca draft prompts, which this task implements together to avoid duplicate Scientist integration claims.

## Implemented and verified

Four Heart test-workspace dropdowns and 18 Broca communication-resource dropdowns are implemented with stable resource anchors. Scientist exports the public catalogue and links to these destinations while retaining source links. Local Broca ownership documentation is expanded; canonical role-map rollout and broader evidence ingestion remain separate.

Validation: Heart 142 targeted tests; Broca 22 tests plus 4-assistant/18-record contract check; Scientist 76 tests and 7 JavaScript tests; 12 responsive/theme browser cases plus two no-JavaScript cases. Keyboard, hash opening, no horizontal overflow, public projection equality and all 22 unique anchors checked. Evidence resides in the task worktree. Heart readiness STALE only for absent current-source release rehearsal, with no RED/YELLOW reasons.

Merge and publish Heart/Broca before Scientist so deep-link destinations exist. No deployment was dispatched. Independent review and source PRs precede human /prm.

PRs: Heart#295, Broca#7, Scientist#66. Independent review found a cached CI identity mismatch edge case; Heart now requires canonical run provenance. The corrected implementation passed re-review. Human /prm remains required; publication is not dispatched.

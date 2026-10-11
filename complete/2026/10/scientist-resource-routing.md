# Scientist project resources grouped by dashboard

- issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/57
- completed: 2026-10-11
- workspace-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/58
- merge: ec8f51d0208533ce8680a425052081f0f91e2074
- tier: judge; explicit human /prm and publish

Projects and Dashboards now have separate visible headings. Cards route communication resources to Broca, profiling to Pulse, inference to Insight, visualization to Eyes, and test workspaces to Heart. Organ names link to dashboards; resource names link to their sources. The shared Broca assistant inventory is removed. Optional routes remain instance configuration and preserve typed snapshot relationships, public visibility and backwards compatibility.

Validation: 46 Python tests, 6 Node tests, six responsive/theme browser cases plus no-JavaScript passed; independent review CLEAN. Exact-head Actions run 38147034915 and tests job 114492457558 completed successfully. Feature head 8b9c67a proven ancestor of origin/main; no upstream or sibling PR. Heart shipping verdict STALE: release validation incomplete: no rehearsal for current source.

Publication explicitly authorized and dispatched: https://github.com/PyAutoLabs/PyAutoScientist/actions/runs/38147892921. Publication succeeded. Live HTML verified separate headings, all five organ routes, Heart test-workspace links and absence of the old Broca inventory. Local validation evidence preserved in `PyAutoMind/tmp/scientist-resource-routing/evidence/`. Worktree contains only reproducible test caches, no scientific data products.

Broader adoption/Broca phases remain draft; grey available-to-add resources belong to the starter/optional-organ phase discussed with the user. This refinement does not implement those placeholders.

Close-out: record/prompt-scoped lifecycle check passed; three pre-existing profiling-registry warnings and one batch warning remain out of scope. No sibling prompts retired. Scientist reconciliation found no suspects; dashboard regenerated with this record.

## Original prompt

# Scientist project resource routing

Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/57
Type: feature
Target: PyAutoScientist
Repos:
- PyAutoScientist
Difficulty: small
Autonomy: safe
Consequence: judge

## Original request

Have Projects be a separate header to Dashboards below (which start with Brain). Next, remove the Organ records (
Broca assistant evidence (shared inventory) ) which seems like too much information. But I do see Organ records has proifling, inference, visualization for autolens which should be on this list. I think linking thse to the name of the dashboards, so Pulse     autolens_profiling,        Insight       autolens_inference is ok. Broca for assistant and workspace. Heart should capture workspace_test

## Plan

1. Add a visible Dashboards heading above Brain, with Projects retained as a separate preceding section.
2. Remove the shared Broca assistant evidence resource. Replace current generic record associations with typed profiling/inference/visualization relationships routed to Pulse/Insight/Eyes dashboard links.
3. Group documentation/tutorials/workspaces/assistants under Broca, preserving resource types internally, and add explicit workspace_test resources under Heart. Resource names themselves link to their source.
4. Keep routes in instance configuration using canonical resource references; missing/private dashboard routes fall back to ordinary category groups, with no invented evidence or ownership transfer.
5. Extend resolver/render tests, validate the shipped configuration, run existing Python/Node tests and responsive browser checks. Ship one PR.

Tier: judge — merge mode: human /prm.

## Detailed implementation

`config/projects.json`: optional relation-to-dashboard resource mapping; explicit dashboard destinations; no shared assistant inventory entry. Add workspace_test identities already in Mind. `scripts/project_resources.py`: additive schema-v1 support for routes and profiling/inference/visualization/tests categories; combine groups sharing a public dashboard; safe linked organ/resource names in HTML and Markdown. `scripts/organism_board.py`: visible Dashboards heading, retain #dashboards grid anchor and refresh behavior. `PROJECTS.md`: document routing and first-class categories. Tests cover routing, private fallbacks, backwards compatibility and section order.

Branch survey: Scientist and Mind main clean after fetch; no active Scientist claim/open PR. Old merged DNA worktree remains untouched. Routine implementation authorized as ongoing dashboard refinement; no merge/deploy implied.

## Handoff

Implemented in 8b9c67a, PR https://github.com/PyAutoLabs/PyAutoScientist/pull/58. 46 Python tests, 6 Node tests and 6 browser/theme cases plus no-JS passed; independent CLEAN. Heart STALE (release validation incomplete: no rehearsal for current source) passes development gate. No merge or deployment. User requested separate headings and organ-linked project resource rows; broad Broca/starter roadmap unchanged. Next: human /prm and dashboard publication.

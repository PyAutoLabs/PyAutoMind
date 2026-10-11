# Scientist project resource routing

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

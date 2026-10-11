# Collaborator-led PyAutoScientist adoption pilot

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoScientist
Repos:
- PyAutoBrain
- PyAutoBroca
- PyAutoCortex
- PyAutoMind
- PyAutoScientist
- workspaces
Difficulty: too-large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing

James has an interested collaborator who can use an initial version while we design and develop it. Make PyAutoScientist usable by other researchers through a small starter, explicit connections to their own projects, and organs added as their needs grow. This is the intake plan for later work, not authorization to begin implementation now or contact the collaborator. The collaborator's identity, project, access requirements and working environment have not yet been supplied.

## Intended experience

A user starts with one small Scientist repository, connects existing projects, and works primarily through an AI agent with a dashboard and brief high-level documentation explaining what to ask. Existing project repositories remain where they are. The starter may be called PyAutoEmbryo, but that name is provisional. Their instance and organs may use a personal or lab prefix such as NameScientist. The dashboard shows connected projects and available organs; inactive organs explain their purpose and provide a setup prompt. An organ becomes usable after setup and validation.

Develop this incrementally with the collaborator's real use. Do not require them to recreate James's mature repository ecosystem before gaining value.

## Existing foundations to inspect afresh

- @PyAutoScientist/AGENTS.md, README.md, dashboard renderer, reporting and ChatGPT route.
- @PyAutoMind/repos.yaml: canonical repository identity; extend or reference it rather than inventing a competing inventory.
- @PyAutoBrain/ORGANISM.md: responsibility boundaries and the rule that a new organ must own distinct state or effects.
- @PyAutoBrain/docs/adoption/guide.md and config_surfaces.md: current configurable-fork adoption model, naming assumptions, templates and instance-isolation checks.
- @PyAutoBrain/docs/standards.md and the applicable shared dashboard, navigation and orchestration contracts.
- Existing Mind/Memory templates and PyAutoProject family before creating another starter mechanism.
- @PyAutoBroca assistant evaluation and upkeep ownership; @PyAutoCortex scientific project records.

The current adoption guide expects several framework repos with retained names and a specific harness/workspace layout. The proposed experience changes that contract; audit actual implementation rather than assuming arbitrary names, missing organs or harness portability already work.

## Proposed phases (slice before issuing implementation tasks)

1. Define explicit project relationships and demonstrate them in James's existing Scientist dashboard. Expandable project cards should link software, shared dependencies, workspaces/tutorials, published docs and source, assistants, and relevant campaigns/activity. Resources are optional lists and may be folders, external docs or multiple repositories. Shared libraries can serve multiple projects. Distinguish software families from Cortex scientific investigations. Keep detailed records authoritative with their current owners.
2. Build the smallest viable starter and onboarding path using existing reusable machinery. Connect one collaborator project and achieve one useful task before expanding. Decide the minimal built-in coordination/task state and supported harness after inspecting dependencies. Separate framework code, user configuration/policy and empty user-owned state. Include no James-specific task history, private data, owners, cluster paths or deployment assumptions.
3. Add progressive organ activation using one supported repository layout initially. Use stable capability identifiers mapped to repository/path locations and optional display names; do not infer identity from a PyAuto prefix or suffix. Multiple organ repos remain valid when they earn their operational cost; do not require one repo per capability merely because PRs and CI are used. Support available, setup-incomplete, active, paused and needs-attention states, with missing/stale evidence distinct from uninstalled. Validate one organ end to end before marking it active; make retries resumable.
4. Prove maintenance and upgrades on the pilot. Record framework versions and generate reviewable upgrade changes preserving configuration and user records. Do not promise conflict-free pulls. Demonstrate one upgrade and recovery/rollback path before broadening adoption.
5. Refine using collaborator feedback: capture friction and missing capability requests, improve question-led docs and setup, and only then widen the organ catalogue or support more layouts.

## Dashboard and assistant design

Show active capabilities prominently, with all available organs discoverable in an expandable catalogue. Pair anatomical names with plain-language purposes. Setup prompts should work from goals such as understanding slow code rather than requiring users to learn organ names. Show connected resources, blockers, evidence freshness and what needs a human decision. Persist working state in repositories so a new chat/agent can resume.

Workspaces and docs belong under project cards and in Broca's cross-project communication/documentation view. James confirmed on 2026-10-10 that Broca should encompass all communication and documentation, including workspaces/tutorials; assistants are one part of that responsibility. Scope this through the linked draft `draft/feature/pyautobroca/broca_communication_documentation_and_workspaces.md`. Preserve project ownership of source material and existing evidence; do not create another organ merely for documentation navigation. The expanded Broca capability is planned, not already implemented.

Keep human docs short and question-led: what can this Scientist do; connect this project; recommend a capability for a problem; what needs attention; resume in a fresh chat; explain or undo setup changes. Provide sufficient agent-readable contracts for reliable operation.

## Confirmed pilot direction and future collaboration

James confirmed that the collaborator works on independent projects of their own. This pilot creates their own Scientist, ideally spanning their projects with shared organs within that instance; it is not onboarding them as a contributor to PyAutoLabs. Framework improvements should be reusable across instances while configuration, tasks, scientific records and knowledge remain independently owned. Let the collaborator attempt a small real task through the onboarding instructions and record where James's help is needed; turn implicit maintainer knowledge into reliable onboarding.

Shared PyAutoLabs use is a separate later milestone, not an initial pilot dependency. Preserve room for explicit instance/project/contributor ownership, one authoritative home per project record and several connected views rather than copied backlogs. A future shared Scientist should support individual chats over shared repository state, ordinary non-AI contributions, action-specific decision rights and concurrent task claims. Cortex may be shared per scientific project where appropriate; it is not intrinsically personal. Do not build full multi-user permissions or concurrency infrastructure as part of the initial independent pilot.

## Pilot decisions to resolve when work starts

- Which collaborator project and one useful first outcome?
- Owners, visibility and approval boundaries within the collaborator's independent instance; whether they need to share it with their own group?
- Available agent harness, GitHub access, local/remote execution and deployment environment?
- Minimum dependencies for a useful starter; optional organ prerequisites and safe failure states?
- Exact starter name, naming portability and upgrade distribution approach?

Avoid generalising every topology/provider upfront. Use the real pilot to decide what warrants support. Connecting a project must not silently change its permissions or publish private information.

## Acceptance evidence

- James's Scientist presents explicit, accurate project/resource relationships without duplicating organ-owned state.
- A clean, differently named instance connects a non-PyAuto collaborator project without copying James's state or requiring all organs.
- The collaborator completes one useful workflow, resumes it from a fresh chat, and can inspect the persistent outcome.
- One optional organ is activated with a working dashboard/evidence path; incomplete, absent and stale states remain distinguishable.
- One framework upgrade preserves local configuration and records with a documented recovery path.
- Capture collaborator feedback and remaining constraints honestly; do not describe the full ecosystem as generally supported on the strength of one pilot.

This is a programme-sized draft. At start-dev, agree the first bounded phase and split implementation prompts/PRs according to the one-prompt/one-task workflow. Preserve this broader intent while tracking the phases; do not dispatch the entire programme unattended.

<!-- formalised by the Intake (Conception) Agent on 2026-10-10 from file:/workspace/scratch/e0d7811f4dcc/adoption-pilot.md -->

## Development breakdown — 2026-10-11

James authorized implementation of the first coherent phase, with routine decisions autonomous and human merge. Current-state audit: Scientist cockpit/organ cards shipped in #53; Broca assistant evidence and Pages shipped in #2/#4. This was the initial audit; the completed phase and current follow-ups are recorded below.

- `complete/2026/10/scientist-project-resources.md` — phase 1 merged in PyAutoScientist#56; remaining phases stay unclaimed.
- `scientist_minimal_starter.md` — planned follow-up; remains unissued and unclaimed.
- `scientist_optional_organ_activation.md` — planned follow-up; remains unissued and unclaimed.
- `scientist_record_preserving_upgrades.md` — planned follow-up; remains unissued and unclaimed.
- `scientist_collaborator_validation.md` — planned follow-up; remains unissued and unclaimed.

Scientist phase 1 consumes canonical identities and exposes links only. Broca expanded communication ownership is agreed intent; inventory/evidence migration is deferred to its contract and pilot tasks. Shared multi-contributor operation remains later.

## Epic membership and dashboard follow-through — 2026-10-11

Canonical epic: `scientist-adoption-pilot` in `epics.md`. All member prompts carry `Epic: scientist-adoption-pilot`; work is selected through this programme, not as unrelated standalone backlog. This file is the programme ledger, not a single implementation task.

Completed foundations:
- `complete/2026/10/scientist-project-resources.md` — Scientist PR #56, explicit relationships and project cards.
- `complete/2026/10/scientist-resource-routing.md` — Scientist PR #58, separate headings and organ-linked resources, published and verified.

The following owner-board work is part of this same epic:
- `complete/2026/10/heart-test-workspace-resource-dropdowns.md` — each test workspace gets meaningful Heart detail and a clear Scientist destination.
- `complete/2026/10/broca-communication-resource-dropdowns.md` — docs, HowTo tutorials, workspaces and assistants get meaningful Broca detail and clear Scientist destinations.
- `draft/feature/pyautobroca/broca_communication_contract.md` — prerequisite responsibility/inventory contract for expanded Broca implementation.
- `draft/feature/pyautobroca/broca_communication_pilot.md` — complementary inventory/evidence work; reuse the dropdown slice instead of implementing it twice.
- `draft/feature/pyautobroca/broca_communication_documentation_and_workspaces.md` — supporting Broca scope map, not an additional duplicate implementation task.

Heart presentation can be scoped independently. Broca dropdowns coordinate with its contract and available evidence; the starter must not wait for the entire Broca roadmap. Remaining starter, optional-organ, upgrade and collaborator-validation phases above retain their dependencies. Grey available-to-add resources are captured in `scientist_optional_organ_activation.md`. This membership update starts no implementation and changes no merge authority.

### Navigation polish — 2026-10-11

`complete/2026/10/scientist-board-navigation.md` (Scientist#59) records the merged navigation polish: organ footer below Scientist cards and Scientist first across other boards. Seven coordinated PRs merged after CI and independent CLEAN review. Cross-board publication/live verification remains in `complete/2026/10/publish-scientist-board-navigation.md`, under this same epic.

## Current priority — 2026-10-11

The human requested Heart test-workspace and Broca communication dropdowns next, before continuing the independent Scientist. `complete/2026/10/organ-resource-dropdowns.md` (Scientist#65) records both destination slices and Scientist deep links merged in Heart#295, Broca#7 and Scientist#66. Brain#518 is merged; independent-starter continuation is now next. Publication/live checks remain recorded separately. Broca broader evidence ingestion and canonical role rollout remain separately recorded.

Dashboard polish merged: `complete/2026/10/broca-resource-categories.md` covers Broca, Hands, Insight and DNA. Publication is tracked separately. `complete/2026/10/scientist-overnight-review.md` now implements the clarified on-demand Scientist review (Brain#519, Scientist#70): retire Brain dashboard polling, reuse Scientist check-in and owner evidence. No second activity ledger.

## Starter continuation — 2026-10-11

`complete/2026/10/scientist-available-resources.md` (Scientist#67, PR#68) implements the next bounded standardization slice: explicit public available-to-add capabilities, independent naming hints and AI setup prompts in project cards. Validated on a fictitious differently named Scientist with no connected organs. Live connected relationships remain unchanged. This is discovery, not activation or a published release.

Sequence from here:
1. Discovery merged in Scientist#68. Local-discovery Brain#518 merged; complete a fresh-session starter handoff acceptance run.
2. Prove resumable activation and evidence validation for one optional organ (`scientist_optional_organ_activation.md`), including incomplete versus stale/absent evidence.
3. Record framework versions and demonstrate an upgrade/rollback preserving configuration and user records (`scientist_record_preserving_upgrades.md`).
4. Run the collaborator acceptance task once their project/access choices are supplied; retain independent ownership. Shared multi-contributor operation stays later.

Nerves' final Markdown icon removal is tracked separately as `complete/2026/10/nerves-markdown-link.md`, PR#201. No unrelated package release is dispatched by these development tasks.

## Independent local acceptance recorded — 2026-10-11

Mind#502 / PR#503 (`complete/2026/10/scientist-starter-acceptance.md`) verifies local skill provenance for a sampled skill, AI-led synthetic project connection with no assistant/organs, and fresh-conversation recovery without losing records. All 532 fixture files were preserved in the confirmation resume; profile/project validation and rendering passed. This bounded local acceptance supersedes the earlier pending diagnostic for these criteria, while pristine installation/full dev workflow and real collaborator validation remain unproven. The detailed report is `docs/scientist-starter-acceptance.md` in merged PR#503.

Next: `scientist_optional_organ_activation.md` — select one useful organ, implement resumable setup with its owner validation, and show it connected only after validation. Then `scientist_record_preserving_upgrades.md`; retain `scientist_collaborator_validation.md` for actual owner choices/access. Reporting PRs Brain#519 and Scientist#70 are merged.

## Optional-organ connection boundary — 2026-10-11

Scientist#71 / PR#72 (`complete/2026/10/scientist-organ-connection.md`) implements validated connection preview/apply, failure-preserving retry and unchanged repeats. Independent review CLEAN; 113 Python / 7 JS tests. Full organ provisioning remains later. Live checking discovered Broca lacks the shared published state feed, so `complete/2026/10/broca-state-feed.md` is the next explicit prerequisite, ahead of real Broca connection acceptance. Existing reporting and local starter acceptance PRs Brain#519, Scientist#70 and Mind#503 are merged and closed out; Scientist#72 is now merged and closed out.

## Broca feed live acceptance complete — 2026-10-11

Broca#15 merged and issue#14 closed; `complete/2026/10/broca-state-feed.md` records the result. Pages run 38172715636 built/deployed exact merge 0204cd5. The real HTTPS state.json returns 200 and validates; Scientist successfully connected, retried without changes and rendered it using a new synthetic profile with records preserved. Earlier missing-feed and pending-publication statements above are historical and superseded. Existing red evidence and October 8 collection time remain unchanged.

The published-feed/validated-connection prerequisite is complete. Next: resumable optional-organ provisioning and owner-specific setup validation, then record-preserving upgrades and actual collaborator acceptance. No real collaborator access or full activation workflow is implied.

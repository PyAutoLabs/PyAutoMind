# Collaborator-led PyAutoScientist adoption pilot

Type: feature
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

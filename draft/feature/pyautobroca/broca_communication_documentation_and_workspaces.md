# Broca communication documentation and workspaces

Type: feature
Target: PyAutoBroca
Repos:
- PyAutoBrain
- PyAutoBroca
- PyAutoMind
- PyAutoScientist
- workspaces
Difficulty: large
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Review-minutes: 25
Unattended: needs-slicing

James explicitly agreed on 2026-10-10 that @PyAutoBroca should cover all communication and documentation, including workspaces, with assistants as one part of that scope. File and scope this expansion for later development. Do not implement it during intake or describe it as already live.

Broca should be the organism's communication and explanation organ: how its software, methods and capabilities are explained and made usable by humans and agents. Its current assistant evaluation and upkeep board is the starting point, not its eventual entire remit. Documentation and workspaces are first-class surfaces even when no assistant exists.

## Scope to design

- Published documentation, API/reference docs, installation and onboarding guidance, examples, tutorials, notebooks and user-facing workspaces.
- Assistants and their definitions, documentation/workspace/knowledge dependencies, evaluation history and upkeep needs.
- Other outward communication surfaces such as release explanations, project/community guidance and announcements; inventory and coordinate these in the design without requiring every format in the first implementation.
- Cross-project visibility of audience, purpose, source location, published location where applicable, maintainer, freshness, evidence and next useful action.
- Relationships between a software revision/release, its docs and workspace examples, and assistants built from those sources. Show potential downstream upkeep needs when sources change without treating every change as a proven defect.

## Ownership and boundaries

Broca owns the communication/documentation inventory relationships, upkeep/evaluation evidence and cross-project board; source repositories retain their documentation, scripts, notebooks, assistant definitions and reproducible runners. It can coordinate improvements through Brain and Mind without centralising every source file. Reuse @PyAutoMind/repos.yaml identity and the proposed Scientist project relationships, not a second repository-identity registry.

Define boundaries in @PyAutoBrain/ORGANISM.md before implementation and update canonical body-map descriptions and generated discovery surfaces through their existing mechanisms. @PyAutoScientist should expose project resource links and route to Broca for communication upkeep; it must not duplicate Broca's evidence ledger.

Ears retains community listening and feedback collection; Broca concerns how the organism explains and communicates its work. Specify the handoff from feedback to communication improvements and preserve Brain's routing/judgment, Mind's implementation state and explicit authorisation for actual external messages/publication. This scope decision does not authorise sending messages or announcements.

Memory retains scientific knowledge and citations; Cortex retains scientific records and human conclusions; Eyes retains figure/gallery evidence; Heart retains authoritative validation/readiness; Hands retains build/release execution. Broca may consume and link their evidence without issuing competing verdicts or taking over workspace test/build execution. Treat workspaces here as examples/tutorials/user learning surfaces; do not absorb arbitrary local checkout environments or every analysis campaign merely because it is called a workspace.

## Evidence and initial implementation plan

Inspect @PyAutoBroca/README.md, AGENTS.md, CHECKIN.md, assistants.json, record/receipt contracts, renderer and tests before designing a compatible extension. Preserve existing immutable assistant evaluation history and independently usable assistants.

First scope and slice the work, then pilot one project's docs plus a representative workspace alongside its assistant where available. Add a separate example with docs/workspaces but no assistant to prove these are not second-class dependencies. Inventory source/published locations and revision relationships, ingest existing cheap build/link/example evidence, and expose concrete upkeep actions through the shared board/check-in design. Add richer quality evaluation and wider communication formats only when the pilot establishes a need.

Keep inventory presence, technical execution/build success, freshness and human-facing explanatory quality as separate evidence dimensions. A successful docs build does not prove correctness or clarity; runnable examples do not establish coverage; missing evidence remains unknown. Record sources, revisions and collection dates; preserve historical records and distinguish cached renders from fresh collection. Do not invent a universal communication score.

The current Broca repo/dashboard are public. Future adopter instances may differ: respect each source's access and visibility, exclude private messages/transcripts/project metadata from public snapshots, and preserve existing no-default-paid-or-scheduled-execution boundaries. A dashboard refresh must not launch model evaluations, publish communications or run costly examples.

## Acceptance for the scoped plan

- A clear expanded Broca responsibility and boundary map, with a phased implementation sequence and affected consumers.
- Documentation, tutorials/workspaces and assistants appear as first-class communication surfaces; no assistant is required for documentation upkeep.
- Project-owned sources remain authoritative, with explicit relationships and a cross-project view rather than copied content.
- Existing assistant history and contracts have a deliberate compatibility/migration strategy.
- Distinct inventory/freshness/validation/quality evidence and concrete human/agent actions, using shared board standards.
- Bounded prompts/PRs before implementation; no unrelated organ creation or multi-user infrastructure expansion.

Related: @PyAutoMind/draft/feature/pyautoscientist/collaborator_led_pyautoscientist_adoption_pilot.md. The first adopter has independent projects and their own Scientist. Reusable Broca improvements should support those projects without copying PyAutoLabs-specific state. Coordinate schemas with that pilot, but do not make the smallest starter wait for the whole Broca roadmap.

<!-- formalised by the Intake (Conception) Agent on 2026-10-10 from file:/workspace/scratch/e0d7811f4dcc/broca-scope.md -->

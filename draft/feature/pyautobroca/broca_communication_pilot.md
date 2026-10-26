# Broca documentation and workspace upkeep pilot

Type: feature
Epic: scientist-adoption-pilot
Target: PyAutoBroca
Difficulty: medium
Autonomy: supervised
Consequence: judge
Status: needs-slicing

Parent: `broca_communication_documentation_and_workspaces.md`.

After the communication contract: inventory one project with docs/workspace/assistant plus another without an assistant. Preserve immutable assistant history; link project-owned sources and revisions. Ingest existing cheap build/link/example evidence, distinguish presence, execution, freshness and quality; no universal score. Expose useful actions on shared board without publishing messages or executing evaluations on refresh.

Next: inspect current owners and split cross-repository rollout into bounded PRs at start-dev. Not a dependency of Scientist project-card implementation.

## Filed presentation slice — 2026-10-11

`complete/2026/10/broca-communication-resource-dropdowns.md` captures resource-specific dropdowns for docs, HowTo tutorials, workspaces and assistants, with useful evidence and Scientist deep links. Treat it as the presentation slice of this pilot; do not duplicate its implementation when planning inventory/evidence ingestion.


## Addition (human, 2026-10-26): skill ↔ workspace linkage evidence

PyAutoHands#324 links assistant skills into workspace notebooks via each assistant's
`colab/contexts.yaml` (folder glob → skills, embedded as Colab Gemini instructions at release). Human:
"make sure that our skill building assistant maintenance ... knows to also have tools or features which
link assistant skills to workspace ... routinely ... a refresh and AI scan."

Broca's share (evidence only, refresh reads committed files, never runs models): per assistant, ingest
the deterministic coverage report from #324 phase 4 — workspace folders matched only by `default`,
mapped skills that no longer exist, max per-notebook context size vs the 20k cap, and staleness
(mapping commit older than the newest skill or workspace-folder change) — and show a "refresh needed"
action pointing at the assistant's `*_refresh_colab_contexts` maintainer skill. The AI scan itself
lives in each assistant.

# Discover optional project resources

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/67
Epic: scientist-adoption-pilot
Target: PyAutoScientist
Consequence: judge

## Original requests

then continue work on scientist release and stadnardization

Ok, I dont if we should do now or wait until we add "greying out" but I think the repos that are missing under porjects "e.g. Tutorials : HowToFit", "Broca : autolens_assistant and autolens_workspace" should be greyed out to a new user using this from scatch. This is again a way to flag tot he user what is goin to be possible and elude to how the Scientist fills out. By greying them out in a way which adopts the api (e.g. _inference, _workspace) they will know roughly what they fill.

## Bounded phase and plan

Build the discovery/presentation slice of scientist_optional_organ_activation.md. Add explicit, public opt-in project opportunities keyed by stable capability identifiers, with instance-owned naming hints. Existing connected resources remain canonical identity references and are never greyed out based on unavailable evidence. No suffix inference, repo creation, activation, deployment or upgrades.

1. Extend scripts/project_resources.py with validated optional project `available` entries for workspaces, tutorials, documentation, assistants, tests, profiling, inference and visualization. Each entry carries a suggested name and explicit public flag; no invented repository URL. Reject opportunities for a relationship already connected to avoid misleading duplication.
2. Render grey but accessible disclosures under matching dashboard/category rows, with a concise purpose and plain selectable AI-led setup prompt. Reuse shared details and prompt controls. Keep opportunities out of connected owner-board catalogue exports.
3. Add a synthetic differently named, assistant-free starter example with naming hints and canonical map identities. Do not alter live connected repositories to pretend they are absent. Document configuration and boundaries in PROJECTS.md/STARTER.md.
4. Verify privacy, invalid states, identity renaming, old configurations, connected catalogue exclusion and offline render. Check responsive browser layout and existing Python/JS suites. Open a judge-tier PR.

Follow-up: actual resumable activation of one organ and evidence validation; record-preserving upgrade and rollback; collaborator acceptance. Brain#518 remains a separate outstanding starter handoff task.

Tier: judge — merge mode: human /prm.

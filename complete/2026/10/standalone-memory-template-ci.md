# Self-contained Memory template validation and template backlog closure

Completed 2026-10-26 under explicit human approval for all non-Pulse PR backlog resolution.

- Canonical fix: PyAutoMind#517 (issue #516), merge f0fc8f77fa6e4528bc0841b6eb86c2fc39eed898, head974ee7a4621fbc276c1ed09c1dcf3656776456c6. Replaces copied Brain-dependent validation with generated standalone content validation.
- PyAutoMind-template#4 merge80b6e44506c2707d036876f541c3eae7077252bc, head181785c8a75d722513ba6db07bb2ab55025a8c78.
- PyAutoMemory-template#3 merge9fd3879fcb07b9529447af618c5e105a7a19cc3e, headc5611dec62aa729f896502230ed3d88ce2bd2d54.

Validation: canonical111 spawn contract/privacy tests; generated Memory make validate, wikilink report and28 validator tests; generated Mind98 pending-release/privacy tests and retained lifecycle/index checks. Both generated trees match spawn --check with no unmatched files or canary hits, checked again against current canonical source. Every current-head workflow/job passed except the intentionally PR-excluded regeneration job in canonical Spawn Drift. Templates each passed current-head CI. Source generator contract tests are not runnable in the stripped Mind template because they reference the deliberately omitted spawn_drift workflow; no full generated-tree test-suite claim.

Generated from Mindad7c5e2d and Memory48fe2433 with normal commits preserving branch history. Weekly automation remains enabled: present drift is resolved, future source changes can legitimately create new sync PRs. RED development override recorded; Heart not declared healthy, no release. Issue516 auto-closed by merged canonical PR. Scratch template clones and validation evidence retained inside workspace; canonical development worktree cleanup follows.

## Original prompt

# Generate self-contained Memory template validation

Issued: 2026-10-26
Type: bug
Target: pyautomind
Repos: @PyAutoMind
Consequence: judge

## Original user request

I dont want any open PRs, including community stuff, scan all repos and work out if we need to do anything to reach this state

ok do all that, but note that Pulse we are working on so ignore

## Approved scope

Fix Memory-template #3's checkout of YOURORG/PyAutoBrain at the canonical generator in PyAutoMind. Generate a self-contained workflow retaining content validators and their tests. Update the spawn specification and regression fixture. Regenerate both existing template PRs after the canonical change merges; preserve history. User authorized development under the surfaced Heart RED reasons on 2026-10-26; this does not authorize release through RED. User authorized in-turn green merges. Pulse #79 is excluded.

## Plan

- Add a dedicated Memory validation workflow generator in scripts/spawn.py, avoiding sibling checkout and Brain-dependent board tests.
- Update docs/pyautobrain/spawn_spec.md and tests/test_spawn_template_contract.py with a realistic Brain-dependent source fixture and assertions for standalone validation.
- Run spawn tests and generated validators, check canaries and generated drift; ship and merge on green CI.
- Regenerate Mind-template #4 and Memory-template #3 from merged sources and merge both after validation.

Tier: judge — merge mode: explicit human approval in this session, on green CI.

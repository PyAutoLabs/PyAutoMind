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

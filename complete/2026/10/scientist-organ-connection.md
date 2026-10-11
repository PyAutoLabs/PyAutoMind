# Validated optional-organ connections

- issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/71
- shipped: 2026-10-11
- epic: scientist-adoption-pilot
- pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/72

Merged after explicit human /prm. Exact head 13ced9edf689d770df55f04de865b07c25282f91 is an ancestor of origin/main. CI run 38171330434: tests passed, no other exact-head runs or skipped legs. Local 113 Python and 7 JS tests; final focused 22 connection tests passed. Independent review CLEAN.

Adds scripts/connect_organ.py and STARTER guidance: preview then validate/apply an explicit connection to an already prepared organ; canonical identities and shared state contract; failed validation preserves records; repeated identical connections are no-ops; atomic profile replacement preserves permissions and refuses detected input changes. Valid red/old evidence is not confused with unconfigured capability. No provisioning, publication, owner-quality validation or release is claimed.

Live Broca dashboard was HTTP 200 but state.json HTTP 404; the helper correctly refused connection without modifying the synthetic profile. Next prerequisite: draft/feature/pyautobroca/broca_published_state_feed.md, then real feed connection acceptance and owner-specific resumable setup. Record-preserving upgrades and actual collaborator validation remain separate epic phases.

Heart at ship: STALE only — release validation incomplete: no rehearsal for current source; no RED/YELLOW. Evidence archived under tmp/scientist-organ-connection/. Task claim and worktree released during close-out.

## Original prompt

# Validated, repeatable optional-organ connection

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/71
Target: PyAutoScientist
Epic: scientist-adoption-pilot
Difficulty: medium
Consequence: judge

## Original request

> ok great, conitnue work

The human authorized continued optional-organ setup after merging Brain#519, Scientist#70 and Mind#503.

## Bounded phase

@PyAutoScientist: add an AI-friendly CLI to preview and apply one explicit connection to an already prepared organ. Broca is the first exercised fixture. Reuse canonical identities, instance/profile/project validation and Brain's state contract. Fetch only the supplied HTTPS state endpoint, validate the feed and exact organ/repo/location before connecting. Do not infer access or naming. No creation/deployment of organs, project source copying, remote writes or assistants required.

Validate before any profile write; errors leave original records intact. Repeating an identical connection is a no-op; different existing connections require explicit manual review. Guard against stale plan overwrite, preserve file mode and other config/projects/records, and replace atomically. Candidate choices and incomplete work stay in the existing Mind task; no new lifecycle ledger. A valid feed can be red or old: connecting is not a health verdict. Subsequent missing/stale evidence stays a connected organ, never an uninstalled capability.

Add scripts/connect_organ.py, focused failure/retry/preservation tests and concise STARTER.md setup/resume instructions. Validate full Scientist Python + JS suites and a Broca feed fixture rendered through the existing dashboard. Follow-up phases remain organ provisioning, setup/paused lifecycle presentation, owner-specific capability validation, upgrades and real collaborator validation. This first phase proves the connection boundary only, not complete organ activation.

Tier: judge — merge mode: human /prm.

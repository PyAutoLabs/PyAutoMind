## env-profile-validator
- issue: https://github.com/PyAutoLabs/PyAutoBuild/issues/161
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoBuild/pull/163 (merged)
- summary: env-profile redesign migration step 1 (campaign #155 Phase 3): validate_env_profiles PR-time config check (schema, dead patterns; strict flags for steps 4-5). First real run found 3 dead patterns (ag quantity/ set) + 15 vacuous-JAX scripts (11 al + 4 ag) outside every enumerated folder — 3x the brief's estimate; recorded on #161 for step 4. Next: wire into the 3 workspace_test PR gates; step 2 single resolver.

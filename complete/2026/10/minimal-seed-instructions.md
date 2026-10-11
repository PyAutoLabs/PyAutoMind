# Instance-neutral minimal seed instructions

Epic: scientist-adoption-pilot

Merged https://github.com/PyAutoLabs/PyAutoMind/pull/501; issue #500 closed. Minimal generation now writes neutral AGENTS.md rather than inheriting the live instance's community routing and optional-organ/automation assumptions. Existing user records and full-family output remain unchanged.

Validation: 116 local spawn/privacy/template tests; actual seed canary/lifecycle checks; real read-only Claude follow-up; independent CLEAN review at 29de2d08 with full-family byte identity. Exact-head Actions38168255339 privacy job passed (entire tests directory); published-template drift job intentionally excluded on pull_request, not a test skip. Human /prm authorized merge.

Full fresh-session skill provenance, project connection/resumption and optional-organ activation remain in the Scientist parent. Evidence archived under tmp/minimal-seed-instructions/.

## Original prompt

# Instance-neutral instructions for a minimal Mind seed

Type: bug
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/500
Epic: scientist-adoption-pilot
Target: PyAutoMind
Consequence: judge

## Original request

ok next task

conintue

## Observed problem

A real fresh Claude read-only diagnostic on the synthetic Mira Scientist seed found that generated Mind AGENTS.md retains live PyAutoLabs community routing and assumed Pulse/Insight instructions. The minimal seed deliberately has no optional organs or GitHub automation. Those directions can misroute an independent adopter. Evidence: tmp/scientist-local-discovery/acceptance-corrected-result.json. This diagnostic does not establish local skill provenance or complete fresh-chat project connection acceptance.

## Plan

- Generate minimal-seed-specific AGENTS.md from framework-owned neutral text, preserving canonical identity, task lifecycle, ownership, explicit approvals and non-overwrite principles.
- Never assume optional organs, configured community destinations, remote access, installed hooks, auto-merge workflows or a complete release environment. Project source stays with its owner; a project connection does not require any organ or assistant.
- Change only scripts/spawn.py minimal=True output, its focused regression tests and minimal seed documentation. Preserve full-family template behavior and existing user directories.
- Test generation with hostile/stale source instructions, default compatibility, privacy and no-overwrite. Generate a fresh seed and run a read-only conversational follow-up against the changed instructions. Record remaining acceptance limitations honestly.

Detailed changes: MINIMAL_AGENTS constant and minimal branch in generate_mind; tests/test_minimal_mind_seed.py source fixture plus regression assertions; README minimal-seed guidance. Validate targeted spawn/privacy/template tests and relevant broader checks. One Mind code PR; lifecycle records remain canonical main.

Tier: judge — merge mode: human /prm.

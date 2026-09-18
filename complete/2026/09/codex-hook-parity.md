## codex-hook-parity

- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/407
- merged: 2026-09-18
- PRs: https://github.com/PyAutoLabs/PyAutoBrain/pull/385 ; https://github.com/PyAutoLabs/PyAutoMind/pull/408 ; https://github.com/PyAutoLabs/autofit_assistant/pull/47 ; https://github.com/PyAutoLabs/autogalaxy_assistant/pull/26 ; https://github.com/PyAutoLabs/autolens_assistant/pull/128 ; https://github.com/PyAutoLabs/autocti_assistant/pull/29
- shipped: Manifest-driven Codex project safety-hook registration and drift checks across Mind, Brain and four assistants; shared Mind commit guard and assistant API-gate payload coverage; project-trust documentation and explicit Claude-only remote SessionStart bootstrap boundary.
- CI corrections: paired Brain-ref support in Mind firewall CI, static spawn template schema alignment, current-main reconciliation and dashboard refresh. Regenerated stale remote-session instructions in Heart (c307d80) and Hands (22bf65f); full drift check and firewall CI then passed.
- validation: 145 focused Mind tests passed; independent review CLEAN. Every current-head workflow and matrix leg succeeded before merge (Spawn Drift's non-PR job skipped by design); all six feature branches proven ancestors of their remote main branches.
- authorization: human prm on 2026-09-18 authorized merge and close-out. Prior Heart RED override authorized development shipping; no release or release-readiness claim.
- follow-up: Phase 3 remains PyAutoBrain#386, draft/maintenance/assistants/codex_skill_discovery_parity.md. This task's six repo claims are released; the separately active mass-field-workspace-sweep claim remains. The broader agent_harness_agnostic_setup parent remains open for phases 3–4.

## Original prompt

# Register safety hooks for Claude and Codex

Type: maintenance
Target: organs
Repos:
- @PyAutoMind
- @PyAutoBrain
- @autofit_assistant
- @autogalaxy_assistant
- @autolens_assistant
- @autocti_assistant
Difficulty: large
Autonomy: supervised
Priority: high
Status: issued
Filed: 2026-09-17
Issued: 2026-09-17
Parent: draft/maintenance/organs/agent_harness_agnostic_setup.md

## Request

> Can you check that all Agent setup (skills, md files, etc) is agnostic to whether its claude or codex, been using claude for a while but gonna codex for the forseeable so worth an agnostic sweep

## Scope

Extend the manifest-driven hook generator and drift tests to create tracked
Codex project-hook registration alongside Claude registration. Use generated
`.codex/hooks.json` as the Codex adapter. Reuse the compatible
end-at-deliverable, shared-Mind commit and assistant API-gate implementations;
test them with representative Codex hook payloads. Do not register the current
Claude-remote session bootstrap unchanged: either give it an explicitly
harness-aware entry point or document it as a separate follow-up.

## Acceptance

- Expected Claude and Codex safety-hook registrations are generated and
  drift-checked from one manifest/source.
- Allow, deny and malformed-input fixtures cover Codex `PreToolUse` payloads.
- Project trust and any remaining session-bootstrap asymmetry are stated
  accurately in setup documentation.

# Portable Scientist instance profile

Type: feature
Issued: 2026-10-11
Issue: https://github.com/PyAutoLabs/PyAutoScientist/issues/61
Epic: scientist-adoption-pilot
Difficulty: medium
Consequence: judge
Parent: scientist_minimal_starter.md

## Original request

ok, next task for the overall PyautoScientist work

## Selection and scope

First bounded slice of the minimal independent starter. Existing adoption guidance assumes the full organ family and dashboard code fixes Scientist branding/host conventions. No current task claims Scientist or Brain. Dashboard navigation already merged; publication remains its separate follow-up.

## Plan

- Add a versioned opt-in instance profile in @PyAutoScientist: display name, canonical Scientist repo ID, explicit HTTPS Pages URL and selected organ connections. Resolve repo identities from the existing Mind repos.yaml, never a second identity map.
- Add an escaped optional display name to @PyAutoBrain's shared hero; unchanged callers retain their existing wordmark.
- Collect only configured organs; an empty list makes no network requests. Omitted organs are not failed/stale. Footer matches connected organs, with explicit Pages locations and existing feed identity validation. Preserve legacy rendering when no profile is supplied.
- Provide an empty synthetic starter example, local render/connect-project instructions and a configurable check-in prompt. No copied personal records, real collaborator assumptions, remote provisioning or automatic activation.
- Verify an independently named empty instance, a renamed connected organ, custom hosting paths, failed versus unconfigured organs, invalid identities/URLs and legacy tests; browser check and independent review before PRs.

Tier: judge — merge mode: human /prm. Routine implementation continues under the ongoing epic authorization.

## Detailed plan and branch survey

Add scripts/instance_profile.py and --instance flag to scripts/organism_board.py. The resolved profile is included in snapshots so renderers use the same identity and membership as collection. Projects still consume config/projects.json and canonical --repos. Profile points to its own project config relative to itself, preventing accidental fallback to James's project records. Add examples/starter/{instance.json,projects.json,repos.yaml} as fictitious offline inputs, not a replacement for a complete Mind template. Add STARTER.md with AI-led connect-project instructions and explicit limits. Update README and Brain adoption guidance to point to this bounded preview without claiming a fully supported bootstrap. Brain board/_theme.py hero gains one keyword-only display_name option; tests cover escaping and unchanged defaults. No shared-module mutation or copied theme.

Canonical repos are clean main; old unregistered worktrees remain untouched. Use feature/scientist-instance-profile in .worktrees/scientist-instance-profile for Brain and Scientist. Tests: affected board/theme and Scientist suites, Node/browser checks, strict docs and fresh Heart. Remaining minimal starter bootstrap, optional-organ activation/grey hints and upgrade handling remain separate epic tasks.

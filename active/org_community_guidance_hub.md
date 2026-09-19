# Publish organization community guidance and welcome

Type: docs
Target: .github
Repos:
- .github
Difficulty: medium
Autonomy: supervised
Priority: high
Consequence: judge
Issued: 2026-09-19
Issue: https://github.com/PyAutoLabs/.github/issues/17
Approved: 2026-09-19 — user: "go"

Implement the .github canonical contribution/conduct/support documents and
public welcome/signpost actions from active/org_community_guidance_and_welcome.md.
The full original user request and approved plan are preserved there and in
the linked issue. Keep AI_POLICY, licenses and repository-specific rules intact.

## Progress — 2026-09-19

- Welcome published: https://github.com/orgs/PyAutoLabs/discussions/18 — manual GitHub Pin discussion action remains.
- All 45 eligible repositories have verified closed, pinned issue signposts. Full inventory and root-file audit summary: https://github.com/PyAutoLabs/.github/issues/17#issuecomment-5745919883
- Canonical documents and bug-form clarification committed locally at b7c3376 (includes b2dd69b); independent review CLEAN. YAML validation and diff checks passed; Scientist tests: 8 passed.
- Awaiting live development-only Heart RED override before source push/PR: PyAutoFit: 4 commit(s) behind origin; PyAutoArray: 3 commit(s) behind origin; PyAutoGalaxy: 3 commit(s) behind origin; PyAutoLens: 3 commit(s) behind origin.
- Merge organization canonical guidance before Scientist compatibility pointers. No merge or release authorized.

## PR-open checkpoint — 2026-09-19

Live user authorized the issue-specific development-only override: "Yes, open both documentation PRs". Authorization, exact RED reasons and passed gates are recorded on both issues, in both PR bodies, active.md and autonomy_log.md.

- Canonical guidance: https://github.com/PyAutoLabs/.github/pull/20
- Dependent Scientist pointers (draft): https://github.com/PyAutoLabs/PyAutoScientist/pull/32
- Both labeled pending-release; no checks reported at PR-open. Neither merged. Manual welcome pin remains.

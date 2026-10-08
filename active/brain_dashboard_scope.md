# Simplify Brain to agents and workflows

Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/507
Type: feature
Target: @PyAutoBrain
Consequence: judge

## Original request

PyAutoBrain Dashboard: - Remove community

- remove: "4 need you · partial view (2 legs unread)
generated 2026-10-07 18:07 UTC · trend ██▆▅▇▇▆▇▅▆▅▇▇▅"

- Remove "GitHub Page"

I am unsure what PyAutoBrain should or should not do anymore. It has loads of tasks and buttons -- too many --
many of which feels like they are outside of scope for Brain or could bewithin their own scope, for example:

- Moring sync is now defunct as its been replaced with dashboard use. Remove it and associated functionality.
- Review overnight, I think this belongs here but maybe its got bloat and things we dont use
- Readiness & release feels like its redundant and now an out of date piece ofi fo I got to the heart and hands dashboards for.
- Test performance I'm not sure what I am meant to do with this? I do feel like no other organ has this so
maybe we need to keep it here, but it feels like it needs a refresh and update to be useable.
- Version consistency, I think that versining an dependancies are going to be managed by a new organ soon. sp
remove this as this is going to become its own thing.
- Community Ears: Remove now we have PyAutoEars
- Resume: Remove as we just use individual boards and would never go via this brain drop down.
- Upkeep, keep as it seems to not be elsewhere currently, same for Hygeine but I am left wondering if these two
are their own concern with their own organ and own dashboard, doesnt feel very brain-y
- Autonomous runs, remove, doesnt feel like information I would ever look at and use.
- All doors, keep and move to top, this really feels like the core of what Brain actually is, also keeps like we shouldnt
call it All Doors but call it Agetnts, Confudctors and Workflows or something more description. 
- Degraded: Remove as again its pointless.

I think the point is that Brain doesnt need much of a dashboard, its mostly just a grouping of agents which
manage different tasks. When it does build up functionality it normally motivates a new organ and dashboard,
so its purpoise could also be to be an abstract starting point for unspecified tasks. What is your  opinion on
Brain should it do anything else or is this sensible?

## Approved scope

- Make Agents & workflows the first primary section, generated from the existing registry, with conductors, faculties and workflows explained in plain language. Focus the orchestration prompt on unspecified requests, planning and routing.
- Remove the requested community surfaces, need-you/generated/trend banner, GitHub Page link, readiness/release, version consistency, resume, autonomous runs and global Degraded section from Brain's page and matching markdown.
- Keep a compact overnight review of actionable failures/blocked work with evidence and next actions. Preserve local unavailable-evidence notices where retained sections need them.
- Combine Upkeep and Hygiene under Maintenance. Keep test/CI performance as an actionable entry using Heart-owned evidence; avoid duplicating Heart's full timing tables. No new organ in this task.
- Retire morning.sh, its timer and wake-up entry points plus obsolete installation/docs/tests wiring. Audit all callers first: morning.sh currently publishes Heart dev-box observations as well as Brain observations. Preserve independently used sync/cleanup tools and arrange an explicit owner for required local evidence before removing the wrapper.
- Update board/_board.py collection, HTML, markdown and machine-feed consumers coherently; config/policy.yaml; board/AGENTS.md and relevant command/skill documentation. Reuse shared presentation components without changing sibling boards. Validate retained action targets, unavailable evidence, published feed compatibility and absence of retired sections.

## Planning evidence

- Brain AGENTS.md already defines Brain as planning/coordination with no task state, health checks or release mechanics.
- board/AGENTS.md confirms Test performance is a projection of Heart's performance block.
- Heart entry check on 2026-10-08: STALE (release STALE, monitoring RED); planning permitted, shipping requires its own check.
- Existing repo claim: board-one-click-update, PyAutoBrain#504, feature/board-one-click-update; shared Update service prototype, awaiting hosting preference. Do not modify or cancel it. Serialize or obtain explicit coordination authorization before starting this task.
- Suggested branch: feature/brain-dashboard-scope.
- Tier: judge — merge mode: human /prm.

Approval: user said "ok beghin" after the scope and concurrent-work coordination question. Shared theme and board_update service stay with #504.

## Implementation checkpoint — 2026-10-08

Implementation complete locally on feature/brain-dashboard-scope, based on 142ddef; source is intentionally uncommitted while ship-time Heart YELLOW awaits human acknowledgement.

Reduced Brain to Agents & workflows, task routing, overnight exceptions and Maintenance. Removed retired source collectors and morning/wake-up/timer functionality, retaining independent local evidence commands and feed compatibility. Shared theme and #504 Update service untouched.

Validation: 1,250 passed in full suite; one inherited-PYAUTO_MIND grouped-checkout fixture failure, then 4/4 passed with PYAUTO_MIND/PYAUTO_BRAIN unset. Ten browser cases passed. Agent surface, Brain project discovery, tenant firewall and diff checks passed. Logs and synthetic preview under task worktree tmp/; PR body prepared in tmp/pr-body.md.

Heart YELLOW reasons (2026-10-08T11:33:17.112822+00:00):
- manifest drift: workspace checkouts (manifest ↔ disk) — 1 mismatch(es) vs PyAutoMind/repos.yaml
- release validation incomplete: no rehearsal for current source

Next: obtain acknowledgement of the exact reason set, then commit/push/create PR via ship-library. No scientific workspace migration required; merge stays human /prm. Live dashboard unchanged until merge/publication.

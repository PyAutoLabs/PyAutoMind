# One-click board Update

Issued: 2026-10-08
Issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/504
Type: feature
Target: @PyAutoBrain
Consequence: judge

## Original request

Can the update button on a board automatically jsut run githib actions in one click? It took me 3 clicks previously!

Follow-up approval: "ok do it"

## Approved direction

Replace the shared board Update link's multi-click workflow with a small authenticated service. After signing in once, Update dispatches the owning refresh workflow and displays a queued acknowledgement and run link. GitHub credentials stay server-side. Reuse the shared component across organ boards, preserving owner refresh targets and timestamps. Hosting/account configuration is still to be established; implementation and local validation may proceed independently.

## Plan

- Implement a portable service with GitHub OAuth sign-in, server-side sessions and a fixed allowlist of board refresh workflows on main.
- Verify the signed-in user's permission for the target repository before dispatch; enforce origin/CSRF protection, safe return destinations, expiry, and duplicate-click protection.
- Extend the shared board component with authenticated dispatch and accessible pending/error feedback, retaining the existing workflow link when the service is unconfigured.
- Test authentication, denied access, dispatch failures, allowed targets, duplicate clicks, and shared browser behavior; document deployment configuration and verify adoption.
- Configure and deploy once the hosting account and GitHub OAuth app are available; validate a real refresh before claiming the feature live.

Tier: judge — merge mode: human /prm.

Suggested branch: feature/board-one-click-update

## Checkpoint — 2026-10-08

Task issue: PyAutoBrain#504. Worktree `.worktrees/board-one-click-update/PyAutoBrain`, branch `feature/board-one-click-update`, source base 896103a. Initial portable Flask/Gunicorn service is uncommitted under `board_update/` (GitHub App OAuth with PKCE, expiring in-memory sessions, allowlisted refresh dispatch, popup interface, container). Shared button integration, durable tests, deployment documentation, full validation and shipping remain incomplete. No service is deployed, no credentials/account were created, no workflow was dispatched and live boards are unchanged.

Ad hoc mocked Flask-client checks passed for OAuth/PKCE, CSRF denial, arbitrary-ref denial, authenticated dispatch, duplicate suppression, OAuth replay denial and logout. This is prototype evidence only, not ship readiness. Virtualenv is in the task bundle `service-venv/`. No independent review or ship-time Heart assessment has occurred.

User clarified they do not think they have hosting and asked what setup entails. Explained hosting account plus restricted GitHub App, possible hosting cost and maintenance. Asked whether to retain the existing button or finish and guide hosting setup; answer pending. Preserve all work. Do not select/provision a hosting account or charge without the user's choice. Resume approved implementation if the user opts to continue, then obtain host/app configuration; otherwise close out as cancelled using lifecycle workflow.

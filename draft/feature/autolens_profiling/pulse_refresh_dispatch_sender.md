# autolens_profiling: tell the PyAutoPulse board to refresh (repository_dispatch pulse-refresh)

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: draft
Consequence: notify
Witness: a `pages_dashboard.yml` run on main ends with a `repository_dispatch` to `PyAutoLabs/PyAutoPulse` (event `pulse-refresh`, payload repo/sha/summary path); the Pulse `dashboard_refresh.yml` run it triggers is green and its receipt names the new commit
Review-minutes: 2
Unattended: ready
Filed: 2026-10-02
Epic: profiling-organ-birth
Blocked-by: evaluation-grid-cap-field (claims autolens_profiling)

The receiving side shipped in phase 2 (`PyAutoPulse/.github/workflows/dashboard_refresh.yml`,
`repository_dispatch: types: [pulse-refresh]`). This is the one-step sender the spec calls a project
follow-up. Blocked on the current claim of `autolens_profiling`; combine with
`draft/feature/autolens_profiling/cockpit_feed_project_identity.md` in one task when it clears.

## Task

`.github/workflows/pages_dashboard.yml`: after `deploy-pages`, add the step from
`autolens_visualization/.github/workflows/render.yml:85-99` renamed for Pulse —
`GH_TOKEN: ${{ secrets.PAT_PYAUTOLABS }}` (org secret), warn-and-exit-0 when absent,
`gh api repos/PyAutoLabs/PyAutoPulse/dispatches -f event_type=pulse-refresh
-f "client_payload[repo]=${{ github.repository }}" -f "client_payload[sha]=$(git rev-parse HEAD)"
-f "client_payload[summary]=dashboard/summary.json"`. `AGENTS.md` one sentence naming the dispatch.

## Out of scope

`build_state()` identity (sibling prompt); any change to `summary.json`.

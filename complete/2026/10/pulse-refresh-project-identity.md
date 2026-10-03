## pulse-refresh-project-identity
- issue: https://github.com/PyAutoLabs/autolens_profiling/issues/366
- completed: 2026-10-03
- epic: profiling-organ-birth
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/367
- merge: efcece3ea39c622e62cc61518f58394ee3986d4c
- summary: Combined producer follow-ups: project badge identifies as autolens_profiling; successful Pages deployment dispatches pulse-refresh to PyAutoPulse using PAT_PYAUTOLABS with repo, SHA and summary path. Preserved drift/triage links and byte-identical summary.json. Documentation and existing tests updated.
- validation: 14 focused tests, Ruff, dashboard idempotence (145 series), Brain state validator and mocked sender missing-token/success/error paths passed. Exact-head PR lint workflow passed all jobs before merge, including full misc tests, link checks and section smoke.
- witness: Pages run 37113415404 succeeded; repository_dispatch Pulse refresh 37113444767 succeeded; receipts/lens.json resolved the merge SHA above, fetched 2026-10-03T09:33:29Z, outcome ok, 159 records and no schema errors.
- authorization: Human requested /prm and continuation if possible on 2026-10-03. No release. Ship-time published Heart was STALE, scoped GREEN; /prm preserves that gate and does not re-judge it.
- next-phase: Phase 4 deferred. Organisation repository inventory on 2026-10-03 contains only autolens_profiling among *_profiling repositories; no real second producer exists. No empty sibling or phase-4 prompt created.
- traps: Mind only recognises one registered active prompt for this task; fold companion scope into it. Use workspace-pr, not pr, for the resume key. Shell pushes unavailable; connected GitHub tree/commit/ref operations preserve the same validated tree and trigger Mind Ledger Merge.
- cleanup: Session used dedicated clones, no task worktree. Profiling checkout is clean on merged main; local feature branch removed after ancestry proof.

## Original prompt

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
Status: active
Issued: 2026-10-03
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/366
Consequence: notify
Witness: a `pages_dashboard.yml` run on main ends with a `repository_dispatch` to `PyAutoLabs/PyAutoPulse` (event `pulse-refresh`, payload repo/sha/summary path); the Pulse `dashboard_refresh.yml` run it triggers is green and its receipt names the new commit
Review-minutes: 2
Unattended: ready
Filed: 2026-10-02
Epic: profiling-organ-birth
Unblocked: 2026-10-03 — #365 merged; autolens_profiling claim explicitly released

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

## Combined companion scope (same task and PR)

The handoff explicitly combines the following identity work into this task; it supersedes the sibling exclusions in both original prompts.

# autolens_profiling: cockpit feed stops claiming `organ: profiling`

Type: feature
Target: autolens_profiling
Repos:
- autolens_profiling
Themes:
- profiling
Difficulty: small
Autonomy: supervised
Priority: normal
Status: active
Issued: 2026-10-03
Issue: https://github.com/PyAutoLabs/autolens_profiling/issues/366
Consequence: notify
Witness: `dashboard/state.json` validates with `PyAutoBrain/board/_state.py`; its `organ` is no longer `profiling`; `scripts/misc/test/test_build_dashboard.py` green; the project's own Pages badge still renders
Review-minutes: 3
Unattended: ready
Filed: 2026-10-02
Epic: profiling-organ-birth
Unblocked: 2026-10-03 — #365 merged; autolens_profiling claim explicitly released

Split out of phase 3 (`complete/…/pyautopulse-brain-board-cockpit` once shipped; PyAutoBrain#450) on
2026-10-02 because `autolens_profiling` was claimed by another task. The organ **PyAutoPulse**
(key `pulse`) now owns the cockpit card and feed (`PyAutoPulse/state.json`); the Brain board never
read the project feed, so nothing on the Brain side transitions.

## Task

`scripts/misc/tooling/build_dashboard.py` `build_state()` (~:410-447): the project feed stops
claiming to be an organ. `board/_state.py` accepts any non-empty `organ` string, so write
`organ: "autolens_profiling"` (a project label; `repo` unchanged), keep `pages_url`, keep the
drift items and their `/profiling triage …` prompts for the project's own Pages badge. Update
`scripts/misc/test/test_build_dashboard.py:226,372` (`["organ"] == "profiling"`) and the contract
test at :166-185 accordingly. `dashboard/README.md:13` and `AGENTS.md:44-46`: say the feed is the
project's own badge feed and that the Brain/cockpit read the PyAutoPulse organ feed. Record the
choice in `PyAutoPulse/REFERENCE.md` is NOT needed here (the organ doc covers it in phase 3).

## Out of scope

Any change to `summary.json` (the `profiling-summary@1` contract); the `pulse-refresh` dispatch
sender (separate prompt).

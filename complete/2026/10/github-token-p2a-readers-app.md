## github-token-p2a-readers-app
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/531
- completed: 2026-10-23
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/532
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/317
- library-pr: https://github.com/PyAutoLabs/PyAutoScientist/pull/89
- library-pr: https://github.com/PyAutoLabs/PyAutoMemory/pull/141
- summary: Phase 2a of the GitHub token consolidation (parent prompt `github_token_and_secret_setup_full_review`; phase 1 = complete/2026/10/github-token-p1-hands-app.md). The organ readers/dispatchers moved off `PAT_PYAUTOLABS` and the never-created `HEART_TIMINGS_TOKEN` / `QUEUE_PR_TOKEN` onto per-job `actions/create-github-app-token@v3` mints of the org-owned `pyautolabs-bot` App, with every silent `||` fallback deleted. Brain `nightly-release.yml`: owner-wide token (actions write, contents read, issues read, variables write) — the window anchor `NIGHTLY_LAST_WINDOW_END` is read/written with the App (human granted the App "Variables: read and write" 2026-10-23, verified `actions_variables: write` on the installation); read and write failures are now loud (exit 1 + Slack driver error), the 24 h silent fallback is gone. Brain `repo_settings.yml` retired (needs Administration, which the App deliberately lacks); local loop documented in `skills/repo_cleanup/reference.md`. Heart `heart-health.yml`: read-only owner-wide App token (actions, contents, pull-requests read). Scientist `organism_board.yml`: read-only owner-wide App token (issues, pull-requests, metadata read), budget fixed at 180. Memory `queue_filing.yml`: App token scoped to PyAutoMemory (contents + pull-requests write) pushes the filing branch and opens the PR as `pyautolabs-bot[bot]`, so the PR triggers CI; compare-link fallback removed.
- evidence: all four PR CI legs green (Brain pytest 3.12/3.13, Heart pytest 3.12/3.13, Scientist tests, Memory validate). None of those legs exercise the edited workflows: post-merge dispatches on main issued 2026-10-23 — Heart heart-health run 39971435680, Scientist organism_board run 39971440448, Brain nightly dry_run run 39971454356 — results reported on Brain#531; Memory proves on its next real filing.
- traps: `GITHUB_TOKEN` cannot read or write Actions variables at all (no `permissions:` key reaches `/actions/variables`; Variables is its own App permission) — do not plan own-repo variable writes on the job token. `actions/create-github-app-token@v3` does not declare a `permission-variables` input (upstream #231) but passes every `INPUT_PERMISSION-*` through; the runner prints an "Unexpected input" warning. The nightly token must be owner-wide: the driver also polls Heart integrate and reads commits/tags/issues on ~11 repos. Brain `tests/test_grouped_organ_consumers.py::test_hygiene_map_and_heart_board_find_grouped_checkouts` fails under a task worktree's `PYAUTO_MIND` (pre-existing, deselected). Owner-wide read tokens are the right shape for board/health readers; narrow `repositories:` only for writers.
- deferred: phase 2b owner-wide writers (`draft/release/pyautobrain/github_token_phase2b_owner_wide_writers_app_token.md`, now unblocked); `bin/branch_sweep_targets.py --outside-owner` path is dead code since `repo_settings.yml` went (hygiene); Hands `docs/nightly_release_design.md` secrets list (phase 5 policy page).
- heart: YELLOW acknowledged by the human 2026-10-23 (manifest drift on one workspace checkout; PyAutoLens release validation stale) — unrelated.

## Original prompt

# GitHub token consolidation phase 2a: organ readers and dispatchers (Brain nightly, Heart, Scientist, Memory) on the App

Type: release
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoHeart
- PyAutoScientist
- PyAutoMemory
Difficulty: hard
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Parent: draft/release/pyautohands/github_token_and_secret_setup_full_review.md (surveys in `_surveys/`; phase plan in 03_target_design_and_phases.md); phase 1 = complete/2026/10/github-token-p1-hands-app.md; sibling 2b = draft/release/pyautobrain/github_token_phase2b_owner_wide_writers_app_token.md
Witness: `grep -rl PAT_PYAUTOLABS .github/workflows` empty in Brain (except branch_sweep_all/branch_archive, 2b), Heart, Scientist, Memory; no `|| github.token` / `|| secrets.GITHUB_TOKEN` fallback on any cross-repo credential; `repo_settings.yml` gone; one green run of each migrated workflow in a side-effect-free mode
Review-minutes: 20
Unattended: never
Issued: 2026-10-23

Phase 1 proved the App (Heart#316, Hands#322). Move the organ workflows that
READ across repos, DISPATCH, or OPEN A PR off `PAT_PYAUTOLABS` / never-created
secrets onto per-job `actions/create-github-app-token@v3`
(`client-id: ${{ vars.APP_CLIENT_ID }}`, `private-key: ${{ secrets.APP_PRIVATE_KEY }}`,
`owner: PyAutoLabs`, narrowest `repositories:`/`permission-*:`); `GH_TOKEN` env
for gh, `actions/checkout` `token:` for clones. Missing credentials fail the job
loudly: delete every silent fallback. One PR per repo.

- Brain `nightly-release.yml`: dispatch + poll Hands `release.yml` → actions write + contents read on PyAutoHands. Repo variables `NIGHTLY_*` unchanged.
- Brain `repo_settings.yml`: RETIRE (needs Administration, which the App deliberately lacks). Delete the workflow; record the equivalent local `gh api -X PATCH repos/PyAutoLabs/<repo> -f delete_branch_on_merge=true` loop in whichever Brain skill/reference pointed at it (grep `repo_settings`).
- Heart `heart-health.yml`: replace the never-created `HEART_TIMINGS_TOKEN` with an App token (actions read, owner-wide = no `repositories:`) so cross-repo artifact reads stop 403ing; delete the `|| secrets.GITHUB_TOKEN` fallback; update the inline comment.
- Scientist `organism_board.yml`: cross-repo activity reads → contents read + metadata, owner-wide; delete the `|| github.token` fallback and the silent 180→60 budget drop (update `REPORTING.md`).
- Memory `queue_filing.yml`: replace the never-created `QUEUE_PR_TOKEN` with an App token (pull-requests write + contents write on PyAutoMemory) so the PR actually opens and triggers CI instead of the compare-link fallback; update README.

Validation: YAML parse + actionlint (ignore the known `client-id` false
positive); each repo's own tests; dispatch each migrated workflow in a
side-effect-free mode after merge to main (Heart health render, Scientist board
render, Brain nightly with its dry/inspect input if one exists — never a live
release) and report; for Memory, a PR-trigger path filter is acceptable proof of
the mint. Keep PRs to `.github/`, skills/docs; another session's unregistered
`pyautodna-stack-management` branch exists on Brain and Scientist.

Out of scope: 2b owner-wide writers (Brain sweep/archive, Gut void, Mind pushers), phase 3 dispatchers, phase 4 secret deletion, phase 5 policy page.

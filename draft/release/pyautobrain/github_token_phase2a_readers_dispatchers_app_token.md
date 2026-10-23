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

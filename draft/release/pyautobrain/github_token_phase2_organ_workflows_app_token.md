# GitHub token consolidation phase 2: organ cross-repo workflows on the pyautolabs-bot App

Type: release
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoGut
- PyAutoScientist
- PyAutoMemory
- PyAutoHeart
Difficulty: hard
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Parent: draft/release/pyautohands/github_token_and_secret_setup_full_review.md (surveys in `_surveys/`; phase plan in 03_target_design_and_phases.md); phase 1 = complete/2026/10/github-token-p1-hands-app.md
Witness: `grep -rl PAT_PYAUTOLABS .github/workflows` is empty in all six repos; no `|| github.token` / `|| secrets.GITHUB_TOKEN` fallback on any cross-repo credential; one green dispatch of each migrated workflow that can run without side effects
Review-minutes: 30
Unattended: never

Phase 1 proved the App (Heart#316, Hands#322). Move every organ cross-repo
writer off `PAT_PYAUTOLABS` onto per-job `actions/create-github-app-token@v3`
(`client-id: ${{ vars.APP_CLIENT_ID }}`, `private-key: ${{ secrets.APP_PRIVATE_KEY }}`,
`owner: PyAutoLabs`, narrowest `repositories:`/`permission-*:`), auth via
`gh auth setup-git` or `actions/checkout` `token:` — never URL userinfo, never
an `extraheader` env trick. Missing credentials fail the job loudly: delete every
silent fallback. Bot identity `pyautolabs-bot[bot]` /
`346909844+pyautolabs-bot[bot]@users.noreply.github.com`. One PR per repo.

Per workflow (from `_surveys/01_inventory.md`):
- Brain `nightly-release.yml`: dispatch + poll Hands `release.yml` → actions write + contents read on PyAutoHands.
- Brain `repo_settings.yml`: RETIRE (needs Administration, which the App deliberately lacks). Delete the workflow; record the equivalent local `gh api -X PATCH` one-liner in the Brain skill/reference that pointed at it.
- Brain `branch_sweep_all.yml`: delete stale branches on siblings → contents write, owner-wide (no `repositories:` = all installed repos).
- Brain `branch_archive.yml`: push archived refs into PyAutoGut, including history containing workflow files → contents write + workflows write on PyAutoGut; remove the extraheader guard; memory `feedback_branch_archive_pat_lacks_workflow_scope` becomes obsolete.
- Gut `void.yml`: delete held refs on siblings → contents write, owner-wide; drop `GIT_CONFIG_KEY_0` extraheader plumbing and its guard; own-repo steps keep `github.token`.
- Mind `spawn_drift.yml`: `*-template` repos → contents write + pull-requests write.
- Mind `session_hook_propagate.yml`, `smoke_bootstrap_propagate.yml`: direct commits to every manifest repo's default branch → contents write, owner-wide (new repos need no per-token step any more — update `policy/smoke_bootstrap.md` and `docs/pyautobrain/spawn_spec.md` wording).
- Mind `arxiv_papers.yml`, `arxiv_interests.yml`: push into PyAutoMemory → contents write on PyAutoMemory. `CLAUDE_CODE_OAUTH_TOKEN` and webhook URLs unchanged.
- Scientist `organism_board.yml`: cross-repo activity reads → contents read / metadata, owner-wide; delete the `|| github.token` fallback and the silent 180→60 budget drop (update `REPORTING.md`).
- Memory `queue_filing.yml`: replace the never-created `QUEUE_PR_TOKEN` with an App token (pull-requests write + contents write on PyAutoMemory) so the PR actually opens and triggers CI; update README.
- Heart `heart-health.yml`: replace the never-created `HEART_TIMINGS_TOKEN` with an App token (actions read, owner-wide) so cross-repo artifact reads stop 403ing; delete the fallback.

Validation per repo: YAML parse + actionlint (ignore the known `client-id` false
positive); each repo's own tests; where a workflow has a side-effect-free mode
(dry-run inputs, `--check`, read-only board renders), dispatch it on the branch
via a `pull_request` path-filtered trigger or after merge and report. For
writers with no safe mode (propagators, void, branch_archive) prove the token
scope with a `git push --dry-run` step added to the workflow's own log, not a
live run. Mind is the shared state checkout: work in the task worktree and
keep the PR to `.github/`, `policy/`, `docs/`.

Out of scope: dispatchers in the viz/profiling/inference repos (phase 3), secret
deletion (phase 4), the policy page (phase 5).

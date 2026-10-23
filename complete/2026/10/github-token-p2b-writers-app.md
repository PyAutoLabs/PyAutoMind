## github-token-p2b-writers-app
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/534
- completed: 2026-10-23
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/537
- library-pr: https://github.com/PyAutoLabs/PyAutoGut/pull/31
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/509
- summary: Phase 2b of the GitHub token consolidation (parent prompt `github_token_and_secret_setup_full_review`; phase 1 = complete/2026/10/github-token-p1-hands-app.md; 2a = complete/2026/10/github-token-p2a-readers-app.md). The eight organ workflows that WRITE across repos moved off `PAT_PYAUTOLABS` onto per-job `pyautolabs-bot` App tokens: Brain `branch_sweep_all.yml` (owner-wide contents write + pull-requests read, minted right before the loop; audit mode now `git push --dry-run`s every repo) and `branch_archive.yml` (source repo + PyAutoGut, contents + workflows write — archiving history containing workflow files now works; extraheader guard and URL-embedded PAT gone; `dry_run` input); Gut `void.yml` (owner-wide contents write for sibling deletes, own-repo deletes on `github.token`; `GIT_CONFIG_KEY_0`/extraheader plumbing, masks, global-extraheader guard and the "skipped: no PAT" path removed; `dry_run` probe job); Mind `spawn_drift.yml` (the two `*-template` repos, contents + pull-requests write; reads are plain public clones), `session_hook_propagate.yml` + `smoke_bootstrap_propagate.yml` (owner-wide contents write; their dry runs now `push --dry-run`), `arxiv_papers.yml` + `arxiv_interests.yml` (PyAutoMemory contents write; silent "PAT not set" skip removed; `dry_run` probe jobs). Docs reworded: Brain `skills/repo_cleanup/reference.md`, Gut README/AGENTS/board text, Mind `policy/smoke_bootstrap.md`, `docs/pyautobrain/spawn_spec.md`. Brain sweep also got a foreground-gc fix (`gc.autoDetach false`) for the cleanup race that had failed the 2026-09-27 scheduled sweep.
- evidence: PR CI green (Brain pytest 3.12/3.13; Gut tests; Mind privacy). Dry-run dispatches on the branch, all green: sweep audit 39976236635 (32/32 push credential ok), archive 39975942351 (PyAutoFit branch untouched, no Gut ref created), void 39975947470 (9 due refs ls-remote + push --dry-run --delete, refs still present), spawn_drift 39975952646, session_hook_propagate 39975957778, smoke_bootstrap_propagate 39975963392 (12/12), arxiv_papers 39975968608, arxiv_interests 39975974280. Witness grep (`PAT_PYAUTOLABS`, `x-access-token`, `GIT_CONFIG_KEY`, `|| github.token`) empty in all three repos' `.github/workflows`.
- traps: `git push --dry-run` sends no pack, so dry runs prove contents write but NOT the archive's workflows write — only a real archive exercises that. A workflow can be dispatched on a branch when the file exists on main even if main's copy lacks `workflow_dispatch` (Gut void). Long push loops: mint immediately before the loop (1 h token). Mind `tests/test_session_hook_sync.py` asserted the literal secret name; a Mind PR may need that one test file beside `.github/`/`policy/`/`docs/`. `scripts/spawn.py` comments still mention the PAT (hygiene). Memory `feedback_branch_archive_pat_lacks_workflow_scope` is obsolete.
- deferred: phase 3 dispatchers (4 `*_visualization/render.yml`, 2 `*_profiling/pages_dashboard.yml`, `autolens_inference/inference-summary.yml`) — the only remaining `PAT_PYAUTOLABS` readers; phase 4 secret retirement; phase 5 policy page (`PyAutoMind/policy/github_tokens.md`); phase 1b PyPI trusted publishing (blocked on the human's PyPI login).
- heart: YELLOW pre-acknowledged by the human 2026-10-23 (manifest drift on one workspace checkout; PyAutoLens release validation stale) — unrelated.

## Original prompt

# GitHub token consolidation phase 2b: owner-wide writers (Brain sweep/archive, Gut void, Mind pushers) on the App

Type: release
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
- PyAutoGut
Difficulty: hard
Unblocked: 2026-10-23 (2a merged — complete/2026/10/github-token-p2a-readers-app.md)
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Parent: draft/release/pyautohands/github_token_and_secret_setup_full_review.md (surveys in `_surveys/`; phase plan in 03_target_design_and_phases.md); phase 1 = complete/2026/10/github-token-p1-hands-app.md
Witness: `grep -rl PAT_PYAUTOLABS .github/workflows` is empty in all six repos; no `|| github.token` / `|| secrets.GITHUB_TOKEN` fallback on any cross-repo credential; one green dispatch of each migrated workflow that can run without side effects
Review-minutes: 30
Unattended: never
Issued: 2026-10-23

Phase 1 proved the App (Heart#316, Hands#322). Move every organ cross-repo
writer off `PAT_PYAUTOLABS` onto per-job `actions/create-github-app-token@v3`
(`client-id: ${{ vars.APP_CLIENT_ID }}`, `private-key: ${{ secrets.APP_PRIVATE_KEY }}`,
`owner: PyAutoLabs`, narrowest `repositories:`/`permission-*:`), auth via
`gh auth setup-git` or `actions/checkout` `token:` — never URL userinfo, never
an `extraheader` env trick. Missing credentials fail the job loudly: delete every
silent fallback. Bot identity `pyautolabs-bot[bot]` /
`346909844+pyautolabs-bot[bot]@users.noreply.github.com`. One PR per repo.

Per workflow (from `_surveys/01_inventory.md`):
- Brain `branch_sweep_all.yml`: delete stale branches on siblings → contents write, owner-wide (no `repositories:` = all installed repos).
- Brain `branch_archive.yml`: push archived refs into PyAutoGut, including history containing workflow files → contents write + workflows write on PyAutoGut; remove the extraheader guard; memory `feedback_branch_archive_pat_lacks_workflow_scope` becomes obsolete.
- Gut `void.yml`: delete held refs on siblings → contents write, owner-wide; drop `GIT_CONFIG_KEY_0` extraheader plumbing and its guard; own-repo steps keep `github.token`.
- Mind `spawn_drift.yml`: `*-template` repos → contents write + pull-requests write.
- Mind `session_hook_propagate.yml`, `smoke_bootstrap_propagate.yml`: direct commits to every manifest repo's default branch → contents write, owner-wide (new repos need no per-token step any more — update `policy/smoke_bootstrap.md` and `docs/pyautobrain/spawn_spec.md` wording).
- Mind `arxiv_papers.yml`, `arxiv_interests.yml`: push into PyAutoMemory → contents write on PyAutoMemory. `CLAUDE_CODE_OAUTH_TOKEN` and webhook URLs unchanged.



Validation per repo: YAML parse + actionlint (ignore the known `client-id` false
positive); each repo's own tests; where a workflow has a side-effect-free mode
(dry-run inputs, `--check`, read-only board renders), dispatch it on the branch
via a `pull_request` path-filtered trigger or after merge and report. For
writers with no safe mode (propagators, void, branch_archive) prove the token
scope with a `git push --dry-run` step added to the workflow's own log, not a
live run. Mind is the shared state checkout: work in the task worktree and
keep the PR to `.github/`, `policy/`, `docs/`.

Out of scope: 2a workflows (readers/dispatchers — own task), dispatchers in the viz/profiling/inference repos (phase 3), secret
deletion (phase 4), the policy page (phase 5).

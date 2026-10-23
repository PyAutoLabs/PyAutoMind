## github-token-p1-hands-app
- issue: https://github.com/PyAutoLabs/PyAutoHands/issues/321
- completed: 2026-10-23
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/316
- library-pr: https://github.com/PyAutoLabs/PyAutoHands/pull/322
- summary: Phase 1 of the GitHub token consolidation. Hands `release.yml` no longer reads `PAT_PYAUTOLABS`: nine per-job `actions/create-github-app-token@v3` mints (scoped to the repos and permissions each job needs, the tag-push token minted immediately before use) replace it; every URL-embedded credential is gone (the #319 class: git clears URL userinfo on any redirect); git auth goes through `gh auth setup-git` or `actions/checkout` `token:`; bot commits/tags are authored as `pyautolabs-bot[bot]`. PyPI/TestPyPI uploads stay on the `PYPI`/`TEST_PYPI` tokens with the trusted-publishing switch as a commented `TODO(token-phase-1b)` block in `release.yml` and `publish_tombstone.yml`. PyAutoHeart gained `token_push_check.yml` (daily, dispatch, and on PRs that touch it) + `heart/checks/token_push.py`: mints an App token and `git push --dry-run`s each release library, commits `state/token_push.json` on main; readiness reports a refused push as RED and a missing/>48 h sidecar as STALE.
- evidence: Heart PR run 39964652005 minted a real App token (scope from `config/repos.yaml`) and pushed dry-run to all five libraries, push=true ×5. Hands pytest 3.12/3.13/3.14 green; Heart pytest 3.12/3.13 green (1307 local).
- traps: Heart's tenant firewall rejects literal org/repo names in organ code — owner from `config/repos.yaml` via `dashboard._repo_owners()`, libraries from `readiness.load_release_gate_names()`; the workflow's `repositories:` input is emitted by `python -m heart.checks.token_push --print-repos`. A branch-only workflow cannot be `workflow_dispatch`ed (404 until on main) — the `pull_request` path-filtered trigger is what proves a token check before merge. Hands `rehearsal=true` still uploads to TestPyPI and skips every App leg, so it proves nothing about tag auth; first live proof is the next release. Brain `repo_settings.yml` needs Administration permission the App deliberately lacks (phase 2: retire, run locally).
- deferred: phase 1b PyPI trusted publishing (blocked on the human's PyPI login — new-device email goes to a defunct address); phases 2–5 in `draft/release/pyautohands/github_token_and_secret_setup_full_review_surveys/03_target_design_and_phases.md`.
- heart: YELLOW acknowledged by the human 2026-10-23 (manifest drift on one workspace checkout; PyAutoLens release validation stale) — unrelated.

## Original prompt

# GitHub token consolidation phase 1: Hands release path on the pyautolabs-bot App

Type: release
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoHeart
Difficulty: hard
Autonomy: supervised
Priority: high
Status: formalised
Parent: draft/release/pyautohands/github_token_and_secret_setup_full_review.md (surveys in the sibling `_surveys/` dir; phases in 03_target_design_and_phases.md)
Witness: a release.yml with zero `secrets.PAT_PYAUTOLABS`, zero `secrets[matrix.project.pat]`, zero URL-embedded tokens and zero `TWINE_PASSWORD`; a Heart read-only check that mints an App token and proves `git push --dry-run` to all five release libraries; a dry-run release dispatch green
Review-minutes: 30
Unattended: never
Issued: 2026-10-23

Phase 0 is DONE on GitHub (2026-10-23): org App `pyautolabs-bot` installed on all
repos (actions/contents/issues/pull_requests/workflows write, metadata read),
org variable `APP_CLIENT_ID` and org secret `APP_PRIVATE_KEY` set. Dead secrets
deleted. `PAT_PYAUTOLABS`, `PYPI`, `TEST_PYPI` still exist and must keep working
until this phase merges (phase 4 retires the PAT).

Scope (PyAutoHands `.github/workflows/release.yml` and `publish_tombstone.yml`):
1. Replace every `PAT_PYAUTOLABS` use (clone, tag push, `gh release`, Mind
   checkout, workspace/library clones, release-notes and label jobs, nightly
   polling inputs) with a per-job `actions/create-github-app-token@v3` step
   (`client-id: ${{ vars.APP_CLIENT_ID }}`, `private-key: ${{ secrets.APP_PRIVATE_KEY }}`,
   `owner: PyAutoLabs`, narrowest `repositories:` and `permission-*:` per job).
   Auth via `gh auth setup-git` (credential helper, survives redirects) or
   `actions/checkout` `token:`; `GH_TOKEN` env for gh. No URL userinfo anywhere.
   Tokens live 1 h: mint in the job that pushes, immediately before use where
   the job is long. Drop the `pat:` matrix field and the `secrets[...]` lookup.
2. Git identity for bot commits/tags: `pyautolabs-bot[bot]` /
   `<app-id>+pyautolabs-bot[bot]@users.noreply.github.com`.
3. PyPI: `pypa/gh-action-pypi-publish@release/v1` with job-level
   `permissions: id-token: write`, `environment: pypi` (TestPyPI job:
   `environment: testpypi`, `repository-url`). Remove twine + `TWINE_PASSWORD`.
   PRE-CONDITION: the human has registered trusted publishers on PyPI and
   TestPyPI for autofit/autoarray/autogalaxy/autolens/autonerves pointing at
   PyAutoLabs/PyAutoHands release.yml. If not confirmed, keep the twine step
   behind the token and leave a TODO; do not break publishing.
4. PyAutoHeart: new read-only check (`heart/checks/` pattern) that mints an App
   token and runs `git ls-remote` + `git push --dry-run` to the five libraries,
   reporting push=true per repo; wire it into the readiness board as a release
   gate input. No live push.
5. Dry-run proof: dispatch release.yml in whatever dry-run/test mode it offers
   (or a `workflow_dispatch` input added for the purpose) and show the tag-push
   leg authenticates. Never a live release from this task.

Out of scope: Brain/Mind/Gut/Scientist/Memory/Heart-health workflows (phase 2),
dispatchers (phase 3), secret deletion (phase 4), policy page (phase 5).
Do not land while a release run is live.

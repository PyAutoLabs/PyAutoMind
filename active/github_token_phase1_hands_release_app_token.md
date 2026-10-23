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

# Survey 3 — target design and phase plan (proposed 2026-10-23, awaiting human approval)

Inputs: `01_inventory.md` (ground truth, read-only) and `02_best_practice.md`.
Memory corroborates the drift: the one org token has been scope-chased three
times (missing `workflow` 2026-08-26, fine-grained repo list too short 2026-09-03,
missing `read:org` at every release label sweep).

## What the inventory says (the headline)

- **16 secret names, 26 consuming workflows, 4 different auth mechanisms for the
  same token.** 19 workflows across 13 repos depend on `PAT_PYAUTOLABS`, a
  person-owned token with no recorded expiry, scope list or owner page.
- **7 secrets are dead** (`PYAUTO` on 9 repos, `PAT_JAMES`, `PAT_RICH`,
  `COPILOT_PAT`, `SLACK_BOT_TOKEN`, Hands' unused `SLACK_WEBHOOK_URL`) and
  **2 are referenced but never created** (`HEART_TIMINGS_TOKEN`,
  `QUEUE_PR_TOKEN`), so those code paths silently degrade every run.
- **#319 is structural, not transient.** Git wipes URL-embedded credentials on
  any redirect (`remote-curl.c` rewrites the base URL from `Location`, then
  `credential_from_url` clears the auth). Any future redirect breaks the
  Hands tag push again whatever token is in the URL.
- **PyPI still uses 2022 API tokens**; trusted publishing is the current norm.
- **Locally** the `gh` OAuth token sits in plaintext `~/.config/gh/hosts.yml`
  and `~/.git-credentials` (credential.helper=store), both mode 600.

## Target design (fewer credentials, one mechanism)

| # | Credential | Type | Owner / store | Replaces |
|---|-----------|------|---------------|----------|
| 1 | `pyautolabs-bot` GitHub App: `APP_CLIENT_ID` (org variable) + `APP_PRIVATE_KEY` (org secret) | GitHub App, org-owned | GitHub org; private key also in password manager | `PAT_PYAUTOLABS` in all 19 workflows, `HEART_TIMINGS_TOKEN`, `QUEUE_PR_TOKEN` |
| 2 | PyPI trusted publishing (OIDC, no secret) | OIDC | PyPI project settings ×5 (+TestPyPI) | `PYPI`, `TEST_PYPI` |
| 3 | `gh auth login` OAuth token | gh device flow | laptop (keyring if available, else the existing 600 file) | any personal "CLI" PATs |
| 4 | One fine-grained PAT for headless use (RAL HPC, Colab), minimal read scope, 366-day expiry | fine-grained PAT, resource owner PyAutoLabs | password manager; Colab Secrets; `pass`/`bws run` on RAL | ad-hoc HPC/Colab PATs |
| — | Webhook URLs (`PYAUTO_*_WEBHOOK_URL`, `HEART_NTFY_URL`, `SLACK_WEBHOOK_URL` on the 10 repos that post) and `CLAUDE_CODE_OAUTH_TOKEN` | unchanged | password manager for recovery | — |

App permissions: contents write, actions write, metadata read, pull-requests
write (spawn_drift, queue_filing), issues write (release notes), workflows write
(branch_archive pushes history containing workflow files; the scope gap memory
records). Add "organization personal access tokens: read" so the App can audit
fine-grained PATs later.

**One mechanism everywhere.** Per job that needs cross-repo write:
`actions/create-github-app-token@v3` with `owner: PyAutoLabs`, narrowest
`repositories:` and `permission-*:`, then `gh auth setup-git` (credential
helper, survives redirects) or `actions/checkout` `token:`. Dispatches via
`gh workflow run`. **No URL-embedded tokens, no extraheader env tricks, no
`|| github.token` fallbacks**: a missing credential fails the job loudly.
Tokens last 1 hour, so mint inside the step group that uses them (Hands tag
push happens late in a long job; mint right before it).

**Password manager: Bitwarden (free tier).** Native Linux CLI works in WSL2 and
over SSH on RAL, no Windows bridging, zero cost; Secrets Manager free tier
covers machine-account injection (`bws run`) if ever wanted. 1Password only if
the Windows app + WSL bridge is preferred (paid, service accounts unconfirmed
on Individual). Every item records: purpose, scopes, expiry, where it is stored
(which org/repo secret, which machine).

**Net: 1 App key + 1 OAuth login + 1 headless PAT**, down from 1 org PAT +
2 legacy PATs + 2 PyPI tokens + an unknown number of personal PATs.

## Phases (supervised; each is its own start_dev task with a PR)

**Phase 0 — human admin, no code** (nothing else can start until done)
1. github.com/settings/tokens and /settings/personal-access-tokens: export the
   list (name, last used, expiry) into the password manager; revoke anything
   unused 90 days. Record which token is `PAT_PYAUTOLABS`.
2. Create org App `pyautolabs-bot` (permissions above), install on all repos,
   store `APP_CLIENT_ID` (org variable) + `APP_PRIVATE_KEY` (org secret).
3. Install Bitwarden; file the App private key, the headless PAT, webhook URLs.
4. PyPI: add a trusted publisher for the 5 projects pointing at
   `PyAutoLabs/PyAutoHands` `release.yml` (environment `pypi`); same on TestPyPI.
Witness: `gh api orgs/PyAutoLabs/actions/variables` lists `APP_CLIENT_ID`.

**Phase 1 — Hands release path** (PyAutoHands, closes the #319 class)
- `release.yml`: App token per job, `gh auth setup-git`, drop
  `secrets[matrix.project.pat]` and the URL-userinfo push; PyPI via
  `pypa/gh-action-pypi-publish@release/v1` with job-level `id-token: write`.
- Heart: a read-only readiness check `token_push.sh` that proves the App
  identity can push (`git push --dry-run`) to all five libraries; wired into
  the release gate. Satisfies the prompt's witness.
- Must not land while a release run is live (run 39949199574 was in progress
  on 2026-10-23).

**Phase 2 — organ cross-repo writers** (Brain nightly-release, repo_settings,
branch_sweep_all, branch_archive; Mind spawn_drift, the two propagators,
arxiv_*; Gut void; Scientist organism_board; Memory queue_filing; Heart
heart-health). Same mechanism; remove every silent fallback; delete the
extraheader guard code in Gut/Brain that existed to defend the URL trick.

**Phase 3 — dispatchers** (4 `*_visualization/render.yml`, 2
`*_profiling/pages_dashboard.yml`, `autolens_inference/inference-summary.yml`):
App token, fail loud instead of warn-and-skip.

**Phase 4 — retire.** Delete `PAT_PYAUTOLABS` (org), `PAT_JAMES`, `PAT_RICH`,
`PYPI`, `TEST_PYPI`, `PYAUTO` ×9, `COPILOT_PAT`, `SLACK_BOT_TOKEN`, Hands'
`SLACK_WEBHOOK_URL`; revoke the underlying PATs. Then org settings: restrict
classic PATs, keep fine-grained approval on. Fix `secrets: inherit` callers
that never held `SLACK_WEBHOOK_URL` (either add it or stop posting).

**Phase 5 — policy page** `PyAutoMind/policy/github_tokens.md`: the inventory
table (secret → consumers → mechanism), the one mechanism, the App's
permissions, who owns what, rotation procedure, and the "new repo born"
checklist (install App on it; that is all). The prompt's other witness.
Memory: supersede `feedback_propagate_pat_lacks_autoreduce_workspace`,
`feedback_branch_archive_pat_lacks_workflow_scope`.

## Decisions needed from the human

1. GitHub App as the single CI identity (recommended) vs keep one classic PAT
   and only fix the mechanism.
2. Bitwarden free (recommended) vs 1Password vs `pass`.
3. Local `gh`: accept the mode-600 plaintext file on WSL2, or install a keyring.
4. Approve phasing; phase 0 is yours and blocks the rest.

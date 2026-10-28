## GitHub tokens and CI secrets

Read this before touching any CI credential. Cross-repo work in Actions uses one
credential: the org-owned GitHub App `pyautolabs-bot`, minted per job or step
into a short-lived token scoped to the narrowest `repositories:` and
`permission-*:` the step needs. Own-repo work stays on `github.token`. No PATs
in CI, no shared long-lived tokens. Never put credentials in URL userinfo
(`https://x:$TOKEN@github.com/...`), never use `extraheader` env tricks, never
fall back with `|| github.token`, and never warn-and-skip when a credential is
missing: fail loudly. The token lives 1 h, so mint it right before a long loop,
not at the top of the job.

### The mechanism

```yaml
- uses: actions/create-github-app-token@v3
  id: app
  with:
    client-id: ${{ vars.APP_CLIENT_ID }}
    private-key: ${{ secrets.APP_PRIVATE_KEY }}
    owner: PyAutoLabs
    repositories: PyAutoMemory        # omit only for genuinely owner-wide work
    permission-contents: write
- env:
    GH_TOKEN: ${{ steps.app.outputs.token }}
  run: gh auth setup-git && git push   # or actions/checkout with token:
```

Commits made with it are authored as `pyautolabs-bot[bot]` /
`346909844+pyautolabs-bot[bot]@users.noreply.github.com`.

### Inventory (live state, 2026-10-23)

| Credential | Where | Consumers | Owner | Rotation |
|---|---|---|---|---|
| `APP_PRIVATE_KEY` | org secret, visibility `all` | every App mint (table below) | org owner | App key rotation (below) |
| `APP_CLIENT_ID` | org variable, visibility `all` | every App mint | org owner | changes only if the App is recreated |
| `PYPI`, `TEST_PYPI` | PyAutoHands repo secrets | Hands `release`, `publish_tombstone` (twine) | maintainer | regenerate on PyPI; retire at trusted publishing (Owed) |
| `CLAUDE_CODE_OAUTH_TOKEN` | PyAutoMind, PyAutoMemory repo secrets | Mind `arxiv_papers`, `arxiv_interests`, `morning_status`; Memory `queue_filing` | maintainer | `claude setup-token`, update both repos |
| `PYAUTO_PAPERS_WEBHOOK_URL` | PyAutoMind repo secret | Mind `arxiv_papers` | maintainer | webhook rotation (below) |
| `PYAUTO_UPDATE_WEBHOOK_URL` | PyAutoMind repo secret | Mind `morning_health`, `morning_status` | maintainer | webhook rotation |
| `PYAUTO_RELEASE_WEBHOOK_URL` | PyAutoBrain, PyAutoHands repo secrets | Brain `nightly-release`; Hands `release` | maintainer | webhook rotation, update both repos |
| `HEART_NTFY_URL` | PyAutoHeart repo secret | Heart `heart-health` | maintainer | new ntfy topic, update secret |
| `SLACK_WEBHOOK_URL` | org secret, visibility `all` (Slack `#builds`, channel `C03S98FEDK2`) | Heart reusable `lib-tests` / `smoke-tests` failure notify, via the caller's `secrets: inherit` | maintainer | webhook rotation (below) |
| `github.token` | per run | own-repo work: boards, Heart `url-check` and own-repo `heart-health` steps, Pulse/Insight `lint`, viz `render` and profiling `profile` checkouts | GitHub | automatic |

`NIGHTLY_RELEASES` / `NIGHTLY_LAST_WINDOW_END` are PyAutoBrain repo variables
(nightly-release switch and cursor), not credentials.

Local: the laptop `gh` uses OAuth (`~/.config/gh/hosts.yml`); git goes over SSH
or gh's credential helper. Headless hosts need no token (checked 2026-10-23):
RAL has no GitHub credential and its checkouts are anonymous HTTPS clones of
public repos (results come back by the laptop's pull, never a git push), and the
Colab bootstrap (`autonerves/setup_colab.py`) clones only public workspaces. If
one ever needs a private repo or a push, it gets one fine-grained PAT, owned by
the maintainer, kept in the password manager and recorded here.

### App mints

| Workflow | `repositories:` | Permissions |
|---|---|---|
| Brain `nightly-release` | owner-wide | actions write, actions-variables write, contents read, issues read |
| Brain `branch_sweep_all` | owner-wide | contents write, pull-requests read |
| Brain `branch_archive` | PyAutoGut + the source repo | contents write, workflows write |
| Gut `void` (2 mints) | owner-wide | contents write |
| Hands `release` (9 mints) | per matrix library / workspace; PyAutoLens; Mind + the five libraries; three assistants | contents read/write, issues write, pull-requests read/write (each mint only what its step uses) |
| Heart `heart-health` | owner-wide | actions, contents, pull-requests read |
| Heart `token_push_check` | the library repos | contents write (`git push --dry-run` proof) |
| Memory `queue_filing` | PyAutoMemory | contents write, pull-requests write |
| Mind `arxiv_papers`, `arxiv_interests` | PyAutoMemory | contents write |
| Mind `session_hook_propagate`, `smoke_bootstrap_propagate` | owner-wide | contents write |
| Mind `spawn_drift` | PyAutoMind-template, PyAutoMemory-template | contents write, pull-requests write |
| Scientist `organism_board` | owner-wide | issues, pull-requests, metadata read |
| four `*_visualization` `render` | PyAutoEyes | contents write (`repository_dispatch`) |
| `autolens_profiling`, `autofit_profiling` `pages_dashboard` | PyAutoPulse | contents write (`repository_dispatch`) |
| `autolens_inference` `inference-summary` | PyAutoInsight | contents write (`repository_dispatch`) |

### The App

`pyautolabs-bot`, org-owned, installed on all repositories. Granted: actions
write, actions_variables write, contents write, issues write, metadata read,
organization_personal_access_tokens read, pull_requests write, workflows write.
A mint can only narrow these. The org owner administers the App (settings,
keys, permission changes); widening a permission needs the org owner to accept
it on the installation.

### Rotation

- **App private key:** App settings → generate a new private key → update the
  org secret `APP_PRIVATE_KEY` → verify with a dry-run dispatch (Heart
  `token_push_check`, or Brain `branch_sweep_all` in audit mode) → delete the
  old key in App settings.
- **Webhook URLs** (`PYAUTO_*_WEBHOOK_URL`, `SLACK_WEBHOOK_URL`, `HEART_NTFY_URL`):
  regenerate at the provider, update the secret where the inventory row says
  it lives (org or repo), delete the old hook.
- **PyPI** (`PYPI`, `TEST_PYPI`): new project-scoped token on PyPI / TestPyPI,
  update the Hands secret, revoke the old one. Until trusted publishing lands.

### New repo born

Nothing to do: the App is installed on all repos and `APP_PRIVATE_KEY` /
`APP_CLIENT_ID` have visibility `all`. Only if the repo needs a repo-level
secret, add it here in the same PR.

### Adding a credential

Prefer an App permission (or a wider `repositories:` on one mint) over a new
secret. A new secret or permission updates this page in the same PR.

### Owed

- **Org settings (org owner):** restrict classic PATs; keep fine-grained PAT
  approval on.
- **Phase 1b, PyPI trusted publishing:** retires `PYPI` / `TEST_PYPI`; blocked
  on the maintainer's PyPI login.

History: the GitHub token and secret setup review epic
(`github_token_and_secret_setup_full_review`), phases
[1](../complete/2026/10/github-token-p1-hands-app.md),
[2a](../complete/2026/10/github-token-p2a-readers-app.md),
[2b](../complete/2026/10/github-token-p2b-writers-app.md),
[3](../complete/2026/10/github-token-p3-dispatchers-app.md),
[4](../complete/2026/10/github-token-p4-retire-pat-mentions.md).

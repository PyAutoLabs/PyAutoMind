# Survey 2 — GitHub App / PAT / PyPI / password-manager best practice (2026-10-23)

## Report: lighter credential design for PyAutoLabs (as of Oct 2026)

No repo edits were made. Each finding is marked [V] if I checked it in official docs or source this session, or [U] if it comes from memory, a third party, or is otherwise uncertain.

### 1. GitHub App vs fine-grained PAT vs classic PAT

**GitHub's recommendation [V]**
- Use `GITHUB_TOKEN` for anything inside the workflow's own repo.
- For other repos or org resources, "register a GitHub App and use an installation access token" through `actions/create-github-app-token@v3`. https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow
- GitHub's PAT docs say the same for org or long-lived integrations: use an App, not a personal token. https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

**Minting a token in a workflow [V]** (https://github.com/actions/create-github-app-token)
- Store the App's **client ID** (not the app ID; `app-id` is legacy) as a variable, e.g. `vars.APP_CLIENT_ID`.
- Store the full PEM private key as a secret, e.g. `secrets.APP_PRIVATE_KEY`.
- Inputs:
  - `owner: PyAutoLabs` with an empty `repositories` gives a token for every repo in the installation.
  - `repositories: a,b,c` narrows it to those repos.
  - `permission-contents: write`, `permission-actions: write` and similar request only what you need (default is all installation permissions).
- The token expires after **1 hour** and is revoked in the action's post step, so it cannot be passed to another job (`skip-token-revoke` overrides this). Mint it in each job that needs it.
- The README's push recipe:
  - set git user to `<slug>[bot]` / `<id>+<slug>[bot]@users.noreply.github.com`
  - run `gh auth setup-git`
  - check out with `persist-credentials: false` so `GITHUB_TOKEN` doesn't shadow the App token.

**Recursive triggers [V]**
- Events created with `GITHUB_TOKEN` do not start new workflow runs, except `workflow_dispatch` and `repository_dispatch`.
- GitHub says to use "a GitHub App installation access token or a personal access token instead". So a tag pushed with an App token does trigger the target repo's `on: push: tags` workflow. https://docs.github.com/en/actions/concepts/security/github_token

**Comparison**
| | GitHub App | Fine-grained PAT | Classic PAT |
|---|---|---|---|
| Owner | Org (survives maintainer leaving) | A person | A person |
| Expiry | 1 h tokens; the private key doesn't expire | Org default max 366 days [V], settable 1–366 | No expiry required by default [V] |
| Granularity | Per-permission, per-repo | Per-permission, per-repo, **one resource owner only** | Broad scopes (`repo` = every repo you can reach) |
| REST rate limit [V] | 5,000/h, +50 per repo over 20, max 12,500 | 5,000/h shared across all of the user's tokens | Same as fine-grained |
| Ruleset bypass | Apps can be on bypass lists [V] | Only via the user's role | Only via the user's role |

- Rate limits for reference: `GITHUB_TOKEN` gets 1,000/h per repo. https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- Fine-grained PAT gaps [V]: no Packages, no Checks API, no multi-org, no outside-collaborator repos. They went GA in March 2025. https://github.blog/changelog/2025-03-18-fine-grained-pats-are-now-generally-available/
- PAT lifetime policies (Oct 2024): admins can cap each token type separately at 1–366 days; non-compliant member tokens are blocked, not revoked. https://github.blog/changelog/2024-10-18-new-pat-rotation-policies-preview-and-optional-expiration-for-fine-grained-pats/ and https://docs.github.com/en/organizations/managing-programmatic-access-to-your-organization/setting-a-personal-access-token-policy-for-your-organization
- No official classic-PAT deprecation date [V, searched; none found].

**Rulesets and the free plan**
- Bypass actors can include GitHub Apps and deploy keys. A Sept 2025 "exempt" bypass type also exists for high-volume automation. https://github.blog/changelog/2025-09-10-github-ruleset-exemptions-and-repository-insights-updates/
- **Free plan [V, from GHES docs]:** rulesets apply only to *public* repos on Free orgs, and org-wide rulesets need Team or Enterprise. https://docs.github.com/en/enterprise-server@3.20/organizations/managing-organization-settings/creating-rulesets-for-repositories-in-your-organization
- GitHub Apps and fine-grained PATs scoped to the org work on Free [U: no plan restriction is stated; widely used].

**Free-plan gotcha [V]**
- "Organization-level secrets and variables are not accessible by private repositories for GitHub Free." https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- So `PAT_PYAUTOLABS` as an org secret only reaches public repos.
- Any private-repo workflow needs a repo-level secret. This is probably why legacy per-repo secrets exist; worth checking.

### 2. Why the redirect dropped the credentials

**Mechanism [V, read in git source]**
1. When the first request (`info/refs`) is redirected, `remote-curl.c` prints `warning: redirecting to %s` and git rewrites the remote's base URL to curl's effective URL. That URL comes from the `Location` header, which has no `user:token@`.
2. Git then runs `credential_from_url(&http_auth, options->base_url->buf)` (http.c, about lines 2468–2473). That call starts with `credential_clear()`, so the URL-embedded token is wiped.
3. The next request (the `git-receive-pack` POST) gets a 401 and git asks for credentials. With no helper and no TTY you get "could not read Username".

`http.followRedirects` defaults to `initial`: follow redirects only on the first request. https://raw.githubusercontent.com/git/git/master/Documentation/config/http.adoc

**How robust each alternative is**
- `http.extraHeader="AUTHORIZATION: basic <b64 x-access-token:TOKEN>"` (what `actions/checkout` does): the header goes on every request whatever the URL, so it survives redirects. **Most robust.** Caveat: it would also go to an off-host redirect target, which is harmless for github.com→github.com.
- A credential helper (`gh auth setup-git`, or checkout's persisted credentials): git looks up credentials by protocol and host after the redirect, so it gets them again for github.com. Robust, and it's the pattern GitHub's own App-token recipe uses.
- `gh` CLI or REST for dispatches and tag creation: not affected by git redirects at all.
- URL-embedded tokens: fragile. They also leak into `.git/config` and process listings. Retire them.

**Why a redirect on a URL that looks right [U]**
- GitHub redirects renamed or transferred repos and owner/repo case mismatches. https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository
- Likely culprits: the URL in the workflow differs from the canonical name by case (e.g. `pyautolabs`, or a repo-name case like `PyAutoFit` vs `pyautofit`), or it points at a pre-transfer owner such as `Jammy2211/...`.
- Compare the printed redirect target byte-for-byte with the URL in the workflow.
- The trailing `.git/` in the message is normal formatting, not the cause.
- I found no GitHub incident tied to this.

### 3. PyPI Trusted Publishing [V]
- This is the recommended way to drop PyPI API tokens. https://docs.pypi.org/trusted-publishers/using-a-publisher/
- Requirements:
  - `permissions: id-token: write` at the **job** level (workflow level is discouraged).
  - An environment (e.g. `pypi`) is optional but strongly encouraged, and must match the publisher config if set.
  - `pypa/gh-action-pypi-publish@release/v1`; latest is v1.14.2 per the Marketplace. https://github.com/marketplace/actions/pypi-publish
- TestPyPI needs its own publisher registration and `repository-url`.
- PEP 740 attestations are generated by default since v1.11.0. https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/
- **Reusable workflows are still unsupported:** the publish step must run in the top-level workflow, and a reusable workflow can build artifacts. Per the v1.13.0 notes the fix is blocked on PyPI with no ETA, and one Aug 2026 report saw attestation 400s via `workflow_call` [U]. https://github-actions-workflows.openastronomy.org/en/latest/trusted_publishing.html
- A project can have more than one trusted publisher, and "pending publishers" exist for new projects [U, from memory; not re-fetched].
- Hands' release workflow layout matters here: publish must happen in each library repo's top-level workflow, or in one central top-level workflow registered as the publisher for all 5 projects.

### 4. Password managers for personal tokens
- **`gh` itself [V]:** `gh auth login` (browser or one-time-code flow) stores an OAuth token in the system credential store and only falls back to a plaintext file if none exists. https://cli.github.com/manual/gh_auth_login
  - So **local `gh` needs no PAT**; run `gh auth setup-git` to cover git as well.
  - WSL2 often has no keyring, so it falls back to `~/.config/gh/hosts.yml` in plaintext [U]. Check with `gh auth status`.
  - Fix: install gnome-keyring/libsecret, or use 1Password's plugin.
- **1Password:**
  - `op run --env-file` / `op read op://vault/item/field` / `op inject` keep secrets out of files.
  - The gh shell plugin (`op plugin init gh`) injects a PAT per command after biometric unlock; it supports bash, zsh and fish on Mac and Linux. https://www.1password.dev/cli/shell-plugins/github/
  - Note it still needs a PAT, whereas gh's own OAuth login doesn't.
  - WSL2 [U]: the common setup calls Windows `op.exe` via alias, symlink or wrapper; env-var passing and biometrics are flaky. https://www.1password.community/developers-69/wsl2-1password-cli-23745
  - Headless HPC needs a service account token (`OP_SERVICE_ACCOUNT_TOKEN`). Whether Individual plans include service accounts is unconfirmed; one third party says Teams/Business [U].
  - Individual plan is about $47.88/yr after the Mar 27, 2026 increase [U, press]. https://www.techradar.com/pro/security/1password-is-getting-more-expensive-soon-says-change-is-despite-the-fact-pricing-has-remained-largely-unchanged-for-many-years
- **Bitwarden:**
  - `bw` CLI covers the vault (`bw get password X` after `bw unlock`, which exports `BW_SESSION`).
  - Secrets Manager free tier has 2 users, 3 projects and 3 machine accounts; `bws run -- cmd` injects env vars on headless hosts. https://bitwarden.com/help/secrets-manager-plans
  - Premium went from $10 to $19.80/yr in Jan 2026 [U, trackers]. https://pricingsaas.com/companies/bitwarden/diffs/2026Q1
  - Good fit for HPC: native Linux binaries, no desktop app needed.
- **KeePassXC / pass (free):**
  - `pass` (GPG) works fine over SSH (`export GH_TOKEN=$(pass gh/hpc)`).
  - KeePassXC has `keepassxc-cli` but no secret-injection tooling.
  - Both mean manual syncing (git for pass).
- **Colab:** use the Secrets sidebar (key icon) with per-notebook access, read via `from google.colab import userdata; userdata.get('GH_TOKEN')`. No password-manager integration needed. https://labs.thinktecture.com/secrets-in-google-colab-the-new-way-to-protect-api-keys/
- **No plaintext files, generally:** `op run -- cmd`, `bws run -- cmd`, or direnv with `export GH_TOKEN=$(op read ...)` in `.envrc` (evaluated at cd-time, nothing stored).

### 5. Least-privilege pattern for a small org
- I found no single canonical reference design. GitHub docs plus guides converge on one org-owned App for bot automation, installed on all repos, with each job requesting only the permissions it needs. https://runs-on.com/github-actions/triggering-a-workflow-from-another-workflow/
- A second App is only worth it for a very different trust level, e.g. an App that may modify `.github/workflows` (needs the `workflows` permission [U]).
- Typical small-org total: 1 App, zero PATs in CI, zero PyPI tokens.
- **Org PAT controls [V]:**
  - Owners can restrict PAT access to org resources (classic and fine-grained separately), require approval for fine-grained PATs (default on), and cap lifetimes.
  - The docs mention no plan restriction [U: presumably available on Free].
- **Auditing secret use:** secret *values* can never be read back. Map usage by grepping workflows: `gh search code 'secrets.PAT_' --owner PyAutoLabs` or a clone-and-grep of `.github/workflows`, plus `gh secret list --org PyAutoLabs` / `gh secret list -R repo` for names and updated dates.
- **Secret scanning / push protection** is free on public repos [U]. GitHub emails before PAT expiry [U, well known; not re-fetched].
- **Bus factor [V]:** PATs "become inactive if the user loses access". If the maintainer leaves, every PAT-driven release, dispatch and dashboard push stops. An org-owned App does not; keep at least two org owners anyway.

### 6. Auditing existing PATs
- **Your own tokens:** there is no API to list them [U: none found]. Use the settings pages, github.com/settings/tokens (classic) and /settings/personal-access-tokens (fine-grained). Both show a "Last used within …" indicator [U, UI behaviour] and the expiry.
- GitHub auto-deletes PATs unused for a year [V], so the 2022 PAT_JAMES and PAT_RICH are either in use or already dead. A secret holding a deleted token simply fails auth.
- **Org view:** `GET /orgs/{org}/personal-access-tokens` lists approved fine-grained PATs with `token_last_used_at` and `last_used_before/after` filters, but "Only GitHub Apps can use this endpoint" [V]. It's another use for the new App, and it doesn't cover classic PATs. https://docs.github.com/en/rest/orgs/personal-access-tokens
- **Which secret holds which PAT:** not retrievable [V by design]. Trace it instead:
  1. Revoke or rotate a candidate token and see which workflow breaks, or
  2. Regenerate it, write it to one secret, and note it in the password-manager item ("used by: org secret X").
- **Approach:**
  1. Export the token list with last-used and expiry dates.
  2. Revoke anything not used in 90 days.
  3. For the rest, record purpose and secret name in the password manager.
  4. Migrate CI to the App and revoke CI PATs last.

### Recommended target design (my synthesis)
1. **One GitHub App, `pyautolabs-bot`, owned by the org and installed on all repos.**
   - Permissions: contents write (tags, dashboard commits), actions write (dispatch), metadata read, plus workflows write only if workflows edit `.github/workflows`; add organization personal-access-tokens read if you want the audit endpoint.
   - Store `APP_CLIENT_ID` (variable) and `APP_PRIVATE_KEY` (secret). Use repo-level copies or a sync script for private repos, because of the Free-plan org-secret limit.
   - Mint per job with `create-github-app-token@v3`, using `owner` plus the narrowest `repositories` and `permission-*`.
   - Push via `gh auth setup-git` or checkout's `token:` with persisted credentials; dispatch via `gh workflow run`. **No URL-embedded tokens.**
   - Add the App to tag/branch ruleset bypass lists where needed (public repos).
2. **PyPI:** Trusted Publishing for all 5 projects, from a top-level workflow, job-level `id-token: write`, `environment: pypi`. Delete all PyPI API tokens.
3. **Delete** PAT_PYAUTOLABS, PAT_JAMES and PAT_RICH after migration. Then restrict classic PAT access and keep fine-grained approval on at org level.
4. **Personal side:**
   - Local `gh`/git: `gh auth login` OAuth with a working keyring; no PAT.
   - HPC: one fine-grained PAT (org owner PyAutoLabs, read-only or minimal, 90–366 day expiry), injected with `bws run`, `op` (if a service account is available) or `pass`; never in dotfiles.
   - Colab: one read-only fine-grained PAT in Colab Secrets.
   - MCP: reuse the gh OAuth token (`gh auth token`) where the client accepts it, otherwise one fine-grained PAT.
   - Track every item in the password manager with purpose, scope, expiry and where it's stored.
   - Net: about **1 App key + 2–3 personal fine-grained PATs**, down from about 4 CI PATs + PyPI tokens + ad-hoc PATs.
5. **Manager choice:** Bitwarden (free vault + free Secrets Manager machine accounts; best fit for HPC and WSL) or `pass` if zero cost and GPG are fine. Choose 1Password only if the Windows desktop app plus WSL bridging works for you and service accounts are confirmed on your plan.

**Open items to verify:**
- The exact Free-plan availability of the org PAT restriction.
- Whether 1Password Individual includes service accounts.
- The exact URL difference behind the redirect (inspect the failed log's redirect target against the workflow's URL).

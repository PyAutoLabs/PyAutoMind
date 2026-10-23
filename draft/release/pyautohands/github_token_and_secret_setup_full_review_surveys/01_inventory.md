# Survey 1 — token and secret inventory (read-only, 2026-10-23)

I took the token inventory read-only across 48 local repos with workflows (140 workflow files) and 66 GitHub repos in the PyAutoLabs org. Nothing was edited, filed or pushed, and no token value was printed. Duplicate copies under `worktrees/` were dropped.

**Totals**
- **Secret names:** 16 distinct. 14 exist on GitHub (1 org-wide, 13 per-repo) and 2 are referenced by workflows but never created (`HEART_TIMINGS_TOKEN`, `QUEUE_PR_TOKEN`).
- **Repos holding secrets:** 16, plus the org.
- **Consuming workflows:** 26 read a secret other than the built-in `GITHUB_TOKEN`. 19 of those, across 13 repos, use `PAT_PYAUTOLABS`. Another 24 caller workflows pass `secrets: inherit` into three shared Heart workflows: `lib-tests` (8 callers), `smoke-tests` (11) and `docs-build` (5).

## 1. Workflow consumers

| Repo | Workflow | Secret | Used for | How it authenticates |
|---|---|---|---|---|
| PyAutoHands | `release.yml` | `PAT_PYAUTOLABS` | Clone the 5 libraries and the workspaces; push release tags; `gh release`/issue calls; checkout of PyAutoMind to clear `pending-release` labels | Token in the URL (`https://$PAT@github.com/…`, no username); `git remote set-url --push origin https://$PAT@…`; `GH_TOKEN` env; `actions/checkout token:`. The secret name is looked up per project via `secrets[matrix.project.pat]` |
| PyAutoHands | `release.yml`, `publish_tombstone.yml` | `PYPI`, `TEST_PYPI` (from 2022) | PyPI / TestPyPI upload | twine `TWINE_PASSWORD` API token. No trusted publishing |
| PyAutoHands | `release.yml` | `PYAUTO_RELEASE_WEBHOOK_URL` | Slack announcement | Webhook URL |
| PyAutoBrain | `nightly-release.yml` | `PAT_PYAUTOLABS`, `PYAUTO_RELEASE_WEBHOOK_URL` | Nightly driver: dispatch and poll Hands `release.yml`; the `NIGHTLY_LAST_WINDOW_END` variable lives on Brain | `GH_TOKEN` env |
| PyAutoBrain | `repo_settings.yml` | `PAT_PYAUTOLABS` | `gh api -X PATCH` on sibling repos (`delete_branch_on_merge`) | `GH_TOKEN` env |
| PyAutoBrain | `branch_sweep_all.yml` | `PAT_PYAUTOLABS` | Clone siblings and delete stale branches | `GH_TOKEN` plus `x-access-token:$PAT@` in the URL |
| PyAutoBrain | `branch_archive.yml` | `PAT_PYAUTOLABS` | Push archived refs into PyAutoGut | `x-access-token` URL; `persist-credentials: false`; guard that fails if an `extraheader` is set |
| PyAutoGut | `void.yml` | `PAT_PYAUTOLABS` (plus `github.token` for the Gut repo itself) | Delete held refs on sibling repos | `GIT_CONFIG_KEY_0=http.https://github.com/.extraheader` with base64 `x-access-token`; refuses if a global extraheader exists |
| PyAutoMind | `spawn_drift.yml` | `PAT_PYAUTOLABS` (plus `GITHUB_TOKEN` in the URL for read clones) | Clone, push and open PRs on the `*-template` repos | `x-access-token` URL; `GH_TOKEN` |
| PyAutoMind | `session_hook_propagate.yml`, `smoke_bootstrap_propagate.yml` | `PAT_PYAUTOLABS` | Commit a file straight to each sibling's default branch | `x-access-token` URL / `GH_TOKEN`; `persist-credentials: false` |
| PyAutoMind | `arxiv_papers.yml`, `arxiv_interests.yml` | `PAT_PYAUTOLABS`, `CLAUDE_CODE_OAUTH_TOKEN`, `PYAUTO_PAPERS_WEBHOOK_URL` | Push the inbox into PyAutoMemory; Claude action; Slack | `x-access-token` URL |
| PyAutoMind | `morning_status.yml`, `morning_health.yml` | `CLAUDE_CODE_OAUTH_TOKEN`, `PYAUTO_UPDATE_WEBHOOK_URL` | Claude action; Slack | Action input / webhook |
| PyAutoMemory | `queue_filing.yml` | `CLAUDE_CODE_OAUTH_TOKEN`, `QUEUE_PR_TOKEN` | Claude action; opening a PR | `PR_TOKEN` env; pushes with `x-access-token:${GH_TOKEN}` (the job token) because the Claude action rewires checkout credentials |
| PyAutoHeart | `heart-health.yml` | `HEART_TIMINGS_TOKEN`, `HEART_NTFY_URL` | Read other repos' artifacts (needs actions:read there); ntfy alert | `GH_TOKEN` env |
| PyAutoHeart | `lib-tests.yml`, `smoke-tests.yml` (shared, reached via `secrets: inherit`) | `SLACK_WEBHOOK_URL` | Slack on failure | Webhook, supplied by the calling repo |
| PyAutoScientist | `organism_board.yml` | `PAT_PYAUTOLABS` | Read the activity feed across repos | `GH_TOKEN` env |
| 4 visualization repos (autolens, autogalaxy, autofit, autocti) | `render.yml` | `PAT_PYAUTOLABS` | `gh workflow run` on PyAutoEyes | `GH_TOKEN`; prints a warning and skips if the secret is absent |
| autolens_profiling, autofit_profiling | `pages_dashboard.yml` | `PAT_PYAUTOLABS` | Dispatch the PyAutoPulse refresh | `GH_TOKEN`; warns and skips if absent |
| autolens_inference | `inference-summary.yml` | `PAT_PYAUTOLABS` | Dispatch the PyAutoInsight refresh | `GH_TOKEN`; errors if absent |

**Silent fallbacks (each one is quiet about losing access):**
- `organism_board.yml`: `GH_TOKEN: ${{ secrets.PAT_PYAUTOLABS || github.token }}`, and the request budget silently drops from 180 to 60 without the PAT.
- `heart-health.yml`: `${{ secrets.HEART_TIMINGS_TOKEN || secrets.GITHUB_TOKEN }}`. The secret is not set, so it always falls back and gets 403 on cross-repo artifacts.
- `queue_filing.yml`: `QUEUE_PR_TOKEN` is empty, so no PR is opened and the issue gets a compare link instead.
- The 6 visualization and profiling dispatchers warn and skip rather than fail when the PAT is missing.

**Same-repo only:** the rest of the Cortex, Mind, Pulse, Insight, Eyes and Memory refresh, merge and pages workflows (`*_refresh`, `*_merge`, `*_board`, `queue_*`, `arxiv_refs`) push, dispatch or comment with `github.token` / `secrets.GITHUB_TOKEN` on their own repo. None of them crosses repos.

**Auth mechanisms in use:** at least four different ones for the same PAT:
- token in the URL with no username (Hands), which is the pattern that broke in #319;
- token in the URL as `x-access-token:` (Brain, Mind);
- an `extraheader` passed through environment variables (Gut);
- `GH_TOKEN` env or `actions/checkout token:` (everywhere else).

## 2. GitHub-side secrets

- **Org plan:** free. Under this plan org secrets don't reach private repos. All 19 PAT consumers are public, so this doesn't bite today.
- **Org secret:** `PAT_PYAUTOLABS`, visibility all, updated 2026-09-29.
- **Other org-level items:** no org variables and no Dependabot secrets.
- **GitHub Apps:** claude, chatgpt-codex-connector, read-the-docs-community and slack, all with access to every repo. No PyAutoLabs-owned app exists for CI auth.
- **Repo variables:** only PyAutoBrain has any (`NIGHTLY_RELEASES`, `NIGHTLY_LAST_WINDOW_END`).

**Repo secrets:**

| Secret | Repos holding it | Updated |
|---|---|---|
| `PYAUTO` | autolens_workspace, autofit_workspace, autolens_workspace_test, PyAutoLens, PyAutoFit, PyAutoGalaxy, PyAutoArray, PyAutoNerves, PyAutoCTI | 2021–2022 |
| `SLACK_WEBHOOK_URL` | PyAutoLens, PyAutoFit, PyAutoGalaxy, PyAutoArray, PyAutoNerves, PyAutoCTI, autolens_workspace, autogalaxy_workspace, autocti_workspace, PyAutoHands | 2022 |
| `SLACK_BOT_TOKEN` | PyAutoFit | 2022 |
| `COPILOT_PAT` | autofit_workspace | 2026-04 |
| `PAT_JAMES`, `PAT_RICH` | PyAutoHands | 2022-08 |
| `PYPI`, `TEST_PYPI` | PyAutoHands | 2022-08 |
| `PYAUTO_RELEASE_WEBHOOK_URL` | PyAutoHands, PyAutoBrain | 2026-07 |
| `CLAUDE_CODE_OAUTH_TOKEN` | PyAutoMind (2026-10-04), PyAutoMemory (2026-08-21) | 2026 |
| `PYAUTO_PAPERS_WEBHOOK_URL`, `PYAUTO_UPDATE_WEBHOOK_URL` | PyAutoMind | 2026-07 |
| `HEART_NTFY_URL` | PyAutoHeart | 2026-09 |

- **Jammy2211's personal repos:** 46 repos, none referenced by any workflow.
- **Who owns the PAT:** the token owner looks like Jammy2211 (GitHub Releases are authored by Jammy2211, per the Mind draft below). Workflow comments suggest it is a fine-grained PAT limited to selected repos:
  - `void.yml` warns that "a repo born after the PAT was minted may be missing";
  - `arxiv_papers.yml` says it was scoped to the `*-template` repos and push to PyAutoMemory may be denied.
- **Can't tell from the API:** its expiry and exact repo list.

## 3. Local machine

- **`gh`:** logged in as Jammy2211 with an OAuth token (`gho_`, length 40), stored in plain `~/.config/gh/hosts.yml` (mode 600), not the keyring. Scopes are `admin:org`, `delete_repo`, `gist`, `repo`, `workflow`.
- **Git credentials:** `credential.helper=store`. `~/.git-credentials` (600) holds two lines: the same `gho_` token for github.com (Jammy2211) and an Overleaf token (`olp_`) for git.overleaf.com.
- **Not present:** no `~/.netrc` and no `~/.pypirc`. No `GH_TOKEN`, `GITHUB_TOKEN`, `PAT_*`, `TWINE_*` or `PYPI*` in the environment or in `.bashrc`, `.profile`, `.zshrc` or `.bash_profile`. No `.env` files in the workspace root or organs. No literal tokens found in organs `md`/`sh`/`py`/`yml` files.
- **Mentions in docs and skills (variable names only):** `PyAutoBrain/skills/GITHUB_ACCESS.md` (`GH_TOKEN`), `skills/prm/reference.md`, `skills/repo_cleanup/{SKILL,reference}.md`, `PyAutoMind/policy/community_surface.md` (`GH_TOKEN` for remote sessions), `policy/smoke_bootstrap.md`, `PyAutoHands/docs/nightly_release_design.md`.

## 4. Existing docs and policy on tokens

There is no single token or secret policy page, and nothing documents rotation, expiry or the PAT's repo list.

- `PyAutoMind/draft/release/pyautohands/github_token_and_secret_setup_full_review.md` is the formalised prompt for this exact review (written 2026-10-23, supervised, too-large). Its witness is an inventory table committed under `PyAutoMind/policy/` plus a check that the PAT or App identity has push access on all five libraries.
- `PyAutoMind/draft/feature/pyautomemory/reading-queue-token-management.md` is a deferred task covering the browser-stored fine-grained token used for one-tap issue creation in PyAutoMemory.
- `PyAutoMind/draft/feature/pyautohands/release_fires_visualization_dispatch.md` notes the prerequisite that the PAT must include both visualization repos.
- `PyAutoBrain/skills/GITHUB_ACCESS.md` covers the client contract (local `gh` vs the MCP server in remote sessions vs read-only surfaces). It does not cover secrets.
- `PyAutoBrain/skills/repo_cleanup/reference.md` explains why own-repo sweeps use `GITHUB_TOKEN` and cross-repo sweeps use `branch_sweep_all` with the PAT.
- `PyAutoHands/docs/nightly_release_design.md` lists the secrets the nightly uses (PAT for dispatch and poll, the webhook).
- `PyAutoMemory/README.md` documents the one-tap fine-grained token (owner PyAutoLabs, PyAutoMemory only) and `QUEUE_PR_TOKEN`.
- `PyAutoGut/README.md` and `PyAutoGut/AGENTS.md` describe the PAT reuse in `void.yml`.
- `PyAutoScientist/REPORTING.md` covers the PAT-or-fallback budget.
- `PyAutoMind/policy/smoke_bootstrap.md` says propagation goes via the PAT.
- `PyAutoMind/docs/pyautobrain/spawn_spec.md` explains why `spawn_drift` is dropped from templates (it depends on the PAT).
- Heart: only inline comments in `heart-health.yml`, nothing under `PyAutoHeart` docs.

## 5. Dead or legacy candidates

**On GitHub but referenced by no workflow:**
- `PYAUTO` on 9 repos (2021–22).
- `PAT_JAMES` and `PAT_RICH` on Hands. The `secrets[matrix.project.pat]` lookup is left over from them, but every matrix entry now says `PAT_PYAUTOLABS`.
- `COPILOT_PAT` on autofit_workspace.
- `SLACK_BOT_TOKEN` on PyAutoFit.
- `SLACK_WEBHOOK_URL` on PyAutoHands. No Hands workflow uses it; Hands posts through `PYAUTO_RELEASE_WEBHOOK_URL`.

**Referenced but missing (each falls back silently):**
- `HEART_TIMINGS_TOKEN` (Heart).
- `QUEUE_PR_TOKEN` (Memory).
- `SLACK_WEBHOOK_URL` is passed via `secrets: inherit` by repos that don't hold it: autofit_workspace, HowToFit/HowToGalaxy/HowToLens, the `*_workspace_test` repos, PyAutoReduce, euclid_strong_lens_modeling_pipeline. Slack posts from those runs are simply empty.

**Legacy publishing:** the 2022 PyPI and TestPyPI API tokens could move to PyPI trusted publishing (OIDC). Today `id-token: write` appears only for Pages and the Claude action.

## 6. PyAutoHands#319

1. "Partial release 2026.10.22.1": the Tag push failed for Nerves, Fit and Galaxy with `fatal: could not read Username` (labelled release-blocker). Array and Lens published.
2. The Mind draft's diagnosis: git followed a `redirecting to …` response and dropped the token embedded in the URL. There was no rename, ruleset or PAT change, and local push `--dry-run` worked. It is probably a transient GitHub-side redirect, but that's unproven.
3. The issue was closed (COMPLETED) on 2026-10-23 at 10:18Z with no comments.
4. Release run 39935267695 (09:54Z) succeeded. Tag `2026.10.23.1` now exists on PyAutoNerves, PyAutoFit and PyAutoGalaxy.
5. A newer release run, 39949199574, is in progress (one in between, 39948344031, was cancelled). The fragile pattern is still in `release.yml`: token in the URL with no username, and the token dropped on redirect. It's the obvious first target for the consolidation, using an `extraheader` or `gh auth setup-git`.

**Biggest risk:** one PAT that is probably personal, owned by Jammy2211, carries all cross-repo writes in 19 workflows, including tag pushes and direct commits to default branches. Its expiry and repo scope aren't recorded anywhere visible.

Scratch file (the org repo list): `/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/c837f591-2150-4cb8-a2f8-47680007e1a9/scratchpad/repos.tsv`

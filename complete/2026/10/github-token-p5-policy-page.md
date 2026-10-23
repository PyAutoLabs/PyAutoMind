- summary: Phase 5, the last phase of the GitHub token consolidation (parent prompt `github_token_and_secret_setup_full_review`, retired the same day into complete/2026/10/github-token-consolidation-epic.md). Added `policy/github_tokens.md`, the authoritative CI-credential page:
  - the rule (the `pyautolabs-bot` App is the only cross-repo identity; own-repo work stays on `github.token`) and the four forbidden patterns;
  - the mint snippet;
  - the live inventory (10 credential names, owners, rotation) and the table of App mints;
  - the App's permissions and administration, rotation steps, and the new-repo checklist (nothing to do);
  - "adding a credential" and the Owed list.
  The page is instance-specific, so `scripts/spawn.py` drops it from the fresh-org templates beside `policy/hpc_ral.md` (spawn_spec row 8 + `test_instance_github_tokens_policy_page_is_dropped`).
- evidence: Mind suite 704 passed. PR CI: `privacy` (full pytest) green; `drift` skipped on PRs by design (`if: github.event_name != 'pull_request'`), not a test leg. Witness checked independently by the session: the set of live org secrets, org variables and repo secrets across all non-archived repos equals the set of credential names on the page. The only page-only names are the PyAutoBrain repo variables `NIGHTLY_RELEASES` / `NIGHTLY_LAST_WINDOW_END`, which the page labels as non-credentials. Tiered merge (glance), merged-unchanged.
- findings: Heart `lib-tests` / `smoke-tests` post to Slack only for callers holding a repo `SLACK_WEBHOOK_URL`; 10 callers post nothing (PyAutoReduce, HowToFit, HowToGalaxy, HowToLens, autofit_workspace, autofit_workspace_test, autogalaxy_workspace_test, autolens_workspace_test, autocti_workspace_test, euclid_strong_lens_modeling_pipeline).
- deferred: the human's org settings (restrict classic PATs, keep fine-grained approval; one org-level `SLACK_WEBHOOK_URL`, then delete the 9 repo copies); phase 1b PyPI trusted publishing; the headless RAL/Colab PAT state; the autocti_visualization phase-3 proof (draft/bug/autocti_visualization/render_fails_no_module_autonerves.md). All are listed under the page's Owed.
- heart: YELLOW acknowledged by the human 2026-10-23 (manifest drift on one workspace checkout; PyAutoLens release validation stale), unrelated.

## Original prompt

# GitHub token consolidation phase 5: the policy page `policy/github_tokens.md`

Type: docs
Target: pyautomind
Repos:
- PyAutoMind
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Parent: draft/release/pyautohands/github_token_and_secret_setup_full_review.md (phase plan in `_surveys/03_target_design_and_phases.md`); phase 4 = complete/2026/10/github-token-p4-retire-pat-mentions.md
Witness: `policy/github_tokens.md` exists; `scripts/spawn.py` maps it to DROP (a test asserts it); the full Mind suite passes; every secret/variable name the page lists matches `gh api orgs/PyAutoLabs/actions/secrets|variables` and the repo-secret inventory on the day it merges
Review-minutes: 15
Unattended: never
Filed: 2026-10-23
Issued: 2026-10-23

Write the one page a session or human reads before touching CI credentials, per
the phase plan: the inventory table (secret → consumers → mechanism), the one
mechanism, the App's permissions, who owns what, rotation, and the "new repo
born" checklist. Keep it short and table-first, in the voice of
`policy/end_at_deliverable.md` / `policy/hpc_ral.md`.

Ground truth (2026-10-23, after phases 0–4):

- **Org secrets:** `APP_PRIVATE_KEY` only. **Org variables:** `APP_CLIENT_ID`.
  Both visibility `all`. `PAT_PYAUTOLABS` deleted; personal PATs revoked.
- **The App** `pyautolabs-bot` (org-owned, installed on all repos), granted:
  actions write, actions_variables write, contents write, issues write,
  metadata read, organization_personal_access_tokens read, pull_requests write,
  workflows write. Bot identity `pyautolabs-bot[bot]` /
  `346909844+pyautolabs-bot[bot]@users.noreply.github.com`.
- **The one mechanism:** `actions/create-github-app-token@v3`, per job/step,
  `client-id: ${{ vars.APP_CLIENT_ID }}`, `private-key: ${{ secrets.APP_PRIVATE_KEY }}`,
  `owner: PyAutoLabs`, narrowest `repositories:` + `permission-*:`; consume via
  `GH_TOKEN`, `gh auth setup-git` or `actions/checkout` `token:`. Never URL
  userinfo, never an `extraheader` env trick, never `|| github.token`
  fallbacks, never warn-and-skip; mint right before long loops (1 h token).
  Own-repo work stays on `github.token`.
- **Mint inventory** (workflow → scope): Brain `nightly-release` (owner-wide:
  actions write, actions-variables write, contents read, issues read),
  `branch_sweep_all` (owner-wide contents write, PRs read), `branch_archive`
  (source + PyAutoGut, contents + workflows write); Gut `void` (owner-wide
  contents write); Hands `release` (several mints: library repos, assistants,
  Mind — contents/issues/PRs); Heart `heart-health` (actions/contents/PRs read),
  `token_push_check` (contents write, PR-trigger proof); Memory `queue_filing`
  (PyAutoMemory contents + PRs write); Mind `arxiv_papers`/`arxiv_interests`
  (PyAutoMemory contents write), `session_hook_propagate`/`smoke_bootstrap_propagate`
  (owner-wide contents write), `spawn_drift` (`*-template` contents + PRs write);
  Scientist `organism_board` (issues/metadata/PRs read); four viz `render`
  (PyAutoEyes), two profiling `pages_dashboard` (PyAutoPulse),
  `autolens_inference/inference-summary` (PyAutoInsight) — contents write for
  `repository_dispatch`. Re-derive from the workflows when writing; don't trust
  this list blindly.
- **Other secrets (repo-level):** Hands `PYPI`, `TEST_PYPI` (twine; retire when
  PyPI trusted publishing lands — phase 1b, blocked on the human's PyPI login);
  `CLAUDE_CODE_OAUTH_TOKEN` (Mind, Memory); `PYAUTO_PAPERS_WEBHOOK_URL`,
  `PYAUTO_UPDATE_WEBHOOK_URL` (Mind), `PYAUTO_RELEASE_WEBHOOK_URL` (Brain, Hands),
  `HEART_NTFY_URL` (Heart); `SLACK_WEBHOOK_URL` ×9 library/workspace repos, read
  by Heart's reusable `lib-tests`/`smoke-tests` via `secrets: inherit` (callers
  without it — `*_workspace_test`, HowTo* — post nothing; owed human fix: one
  org-level secret, then delete the repo copies).
- **Local / headless:** laptop `gh` uses OAuth (`gho_`, `~/.config/gh/hosts.yml`);
  git over SSH or gh's credential helper. Headless hosts (RAL, Colab) — one
  fine-grained PAT if needed, owner the human, kept in Bitwarden; record the
  current state honestly (unknown after the 2026-10-23 revocation → say so).
- **Org settings (owed human, 2026-10-23):** restrict classic PATs; keep
  fine-grained approval on.

Sections: Rule (one paragraph) · The mechanism (YAML snippet) · Inventory table
(credential → where → consumers → owner → rotation) · App permissions + who
administers it · Rotation (App private key: generate new key in App settings →
update `APP_PRIVATE_KEY` → delete old key; webhooks; PyPI) · New repo born
(App already covers all repos and org secrets are visibility `all`: nothing to
do unless it needs a repo-level secret; add it here) · Adding a credential
(prefer an App permission over a new secret; update this page in the same PR) ·
Owed (the human items above + 1b). Link the parent epic's record trail.

Also: `scripts/spawn.py` MIND_RULES — add `("policy/github_tokens.md", "DROP")`
before the `policy/` KEEP (same reason as `policy/hpc_ral.md`: instance-specific),
`docs/pyautobrain/spawn_spec.md` row 8 exception, and a test in
`tests/test_spawn_template_contract.py` asserting it is dropped. Memory: the
two obsolete feedback memories (`feedback_propagate_pat_lacks_autoreduce_workspace`,
`feedback_branch_archive_pat_lacks_workflow_scope`) are superseded — that is the
session's local memory, not this PR.

Closing this phase closes the parent epic prompt
`draft/release/pyautohands/github_token_and_secret_setup_full_review.md`
(retire it with its `_surveys/` into complete/ at close-out, recording 1b and
the human-owed settings as deferred).

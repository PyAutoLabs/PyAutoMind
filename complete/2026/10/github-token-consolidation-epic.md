- summary: The GitHub token and secret consolidation epic, complete 2026-10-23. Before: 16 secret names, 26 consuming workflows and 4 auth mechanisms, with 19 workflows in 13 repos riding the person-owned `PAT_PYAUTOLABS`. After: one org-owned GitHub App `pyautolabs-bot` (org-level `APP_CLIENT_ID` / `APP_PRIVATE_KEY`) minting a narrow per-job token for every cross-repo workflow; the personal PATs revoked; `PAT_PYAUTOLABS` and 7 dead secrets deleted. The policy is `policy/github_tokens.md`.
- phases:
  - 0, human (App created and installed, dead secrets deleted, password manager set up);
  - 1, Hands release (complete/2026/10/github-token-p1-hands-app.md);
  - 2a, readers (complete/2026/10/github-token-p2a-readers-app.md);
  - 2b, writers (complete/2026/10/github-token-p2b-writers-app.md);
  - 3, dashboard dispatchers (complete/2026/10/github-token-p3-dispatchers-app.md);
  - 4, PAT secret deleted and its mentions retired (complete/2026/10/github-token-p4-retire-pat-mentions.md);
  - 5, the policy page (complete/2026/10/github-token-p5-policy-page.md).
- surveys: the epic's three surveys moved to complete/2026/10/github-token-consolidation-epic_surveys/ (01 inventory, 02 best practice, 03 target design + phases). Phase records that cite `draft/release/pyautohands/..._surveys/` refer to this folder.
- deferred:
  - phase 1b, PyPI trusted publishing (blocked on the maintainer's PyPI login; `PYPI` / `TEST_PYPI` twine tokens stay until then);
  - the human's org settings (restrict classic PATs, keep fine-grained approval; one org-level `SLACK_WEBHOOK_URL`);
  - the headless RAL/Colab PAT state;
  - the autocti_visualization phase-3 proof.
  All are listed under Owed in `policy/github_tokens.md`.

## Original prompt

# GitHub token and secret setup: full review and consolidation

Type: release
Target: PyAutoHands
Repos:
- PyAutoHands
- PyAutoBrain
- PyAutoMind
- PyAutoHeart
- PyAutoGut
- PyAutoScientist
Difficulty: too-large
Autonomy: supervised
Priority: high
Memory: reading-queue.md; wiki/galaxies/sources/massive-ellipticals.md; wiki/lensing/log.md
Status: formalised
Consequence: judge
Witness: a single inventory table (secret → consumers → auth mechanism) committed under PyAutoMind policy/, and a read-only check that reports push=true for PAT/App identity on all five release libraries
Review-minutes: 25
Unattended: never

Full top-to-bottom review of the PyAutoLabs GitHub token / secret setup, then consolidate it into one consistent, documented pattern.

Human request (2026-10-23): "Lets intake a prompt to fully go over the whole token setup from top to bottom as small fixes here and there are making it more complex."

Trigger: PyAutoHands release run 39749945942 (2026.10.22.1). The release-job Tag step (release.yml ~line 507) pushes with `git remote set-url --push origin "https://$PAT@github.com/<repo>.git"`. It succeeded for PyAutoArray and PyAutoLens, but failed for PyAutoNerves, PyAutoFit and PyAutoGalaxy with "warning: redirecting to https://github.com/PyAutoLabs/<repo>.git/" then "fatal: could not read Username for 'https://github.com'". When git follows a redirect it discards credentials embedded in the URL. Tracked as PyAutoHands#319 (release-blocker).

Diagnosis 2026-10-23 (read-only):
- No repo rename, transfer, visibility or archive change.
- No rulesets or tag protection; the org is on the free plan, so org rulesets don't exist.
- The token owner is Jammy2211 (GitHub Releases are authored by Jammy2211), who has admin on all five libraries.
- The org secret PAT_PYAUTOLABS is unchanged since 2026-09-29 (visibility=all).
- Jammy2211's local token uses the same URL pattern with no redirect, and push --dry-run succeeds on all five today.
- Most likely a transient GitHub-side redirect; unproven, not on githubstatus.

Scope:
- Inventory every secret: the org secret PAT_PYAUTOLABS; legacy repo secrets PAT_JAMES and PAT_RICH (2022) and PYPI/TEST_PYPI on PyAutoHands; webhook secrets.
- Inventory every consumer across all repos. Known PAT_PYAUTOLABS users: Hands release.yml; Brain nightly-release.yml, repo_settings.yml, branch_sweep_all.yml and branch_archive.yml; Mind spawn_drift, session_hook_propagate, smoke_bootstrap_propagate and arxiv_*; Gut void.yml; Scientist organism_board.yml (which silently falls back to github.token); the *_visualization render.yml files; the *_profiling pages_dashboard.yml files; autolens_inference inference-summary.yml.
- Record how each consumer authenticates: URL userinfo, actions/checkout token, GH_TOKEN, or extraHeader.
- Decide one pattern:
  - credential helper or http.extraHeader instead of URL-embedded tokens;
  - fail loudly on redirect;
  - no silent fallbacks to github.token;
  - classic PAT vs fine-grained PAT vs GitHub App (installation tokens, no personal ownership, no expiry surprises);
  - least-privilege scopes, and one token per purpose vs a single shared token;
  - rotation/expiry ownership and a Heart readiness check that the token can push to every release repo before a live release;
  - retire dead secrets.
- Document the result in one policy page (Mind policy/) and apply it across workflows as a phased plan, not piecemeal fixes.

<!-- formalised by the Intake (Conception) Agent on 2026-10-23 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/45424148-6a9e-468a-a45c-30a48f345a23/scratchpad/token_setup_review.md -->

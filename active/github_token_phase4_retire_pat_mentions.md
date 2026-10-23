# GitHub token consolidation phase 4: retire every remaining PAT_PYAUTOLABS mention

Type: maintenance
Target: pyautomind
Repos:
- PyAutoMind
- PyAutoHands
- autolens_visualization
- autogalaxy_visualization
- autofit_visualization
- autocti_visualization
Difficulty: easy
Autonomy: supervised
Priority: high
Status: formalised
Consequence: glance
Parent: draft/release/pyautohands/github_token_and_secret_setup_full_review.md (phase plan in `_surveys/03_target_design_and_phases.md`); phase 3 = complete/2026/10/github-token-p3-dispatchers-app.md
Witness: `grep -rn PAT_PYAUTOLABS` over each of the six repos' tracked files, excluding `complete/` records and the parent prompt's `_surveys/`, is empty
Review-minutes: 10
Unattended: never
Filed: 2026-10-23
Issued: 2026-10-23

Done on GitHub 2026-10-23: the human revoked the personal PATs and the
`PAT_PYAUTOLABS` org secret was deleted (`APP_PRIVATE_KEY` is now the only org
secret; `APP_CLIENT_ID` the only org variable). No workflow reads the PAT
(phase 3). What is left is prose and one test fixture that still describe it:

- `autolens|autogalaxy|autofit|autocti_visualization/AGENTS.md`: the render
  paragraph says the `eyes-refresh` dispatch uses `secrets.PAT_PYAUTOLABS` and
  "warns and skips". Now: a per-step `pyautolabs-bot` App token scoped to
  PyAutoEyes; a missing credential fails the job.
- `PyAutoHands/docs/nightly_release_design.md` line ~81: "Secrets:
  `PAT_PYAUTOLABS` (dispatch/poll …)" → the App token
  (`vars.APP_CLIENT_ID` / `secrets.APP_PRIVATE_KEY`).
- PyAutoMind `scripts/spawn.py` rule-9b/9c comments (~160, ~188) and
  `docs/pyautobrain/spawn_spec.md` rows 9b/9c: "depends on
  `secrets.PAT_PYAUTOLABS`" → the org App secret. The DROP decisions do not
  change (a fresh org still has no App secret configured).
- PyAutoMind `tests/test_spawn_template_contract.py`: line 123's
  `arxiv_interests.yml` miniature uses `secrets.PAT_PYAUTOLABS` as "a
  configured secret"; switch it to `secrets.APP_PRIVATE_KEY` (what the real
  workflow reads) — the test's meaning is unchanged. Leave the line-85
  historical comment about #125 as history, rewording only if it reads as current.
- PyAutoMind `draft/feature/pyautohands/release_fires_visualization_dispatch.md`:
  its plan tells a future session to dispatch with `secrets.PAT_PYAUTOLABS` and
  "skip cleanly when the secret is empty", with a human prerequisite on the PAT's
  repo list. Rewrite to: mint an App token (`repositories:` both viz repos,
  `permission-contents: write`) as Hands `release.yml` already does elsewhere;
  drop the prerequisite (the App is installed org-wide).

Not in scope (human, GitHub settings): org → Personal access tokens policy
(restrict classic PATs, keep fine-grained approval), and creating one org-level
`SLACK_WEBHOOK_URL` (visibility all) to replace the nine repo copies, so Heart's
`secrets: inherit` callers that never held it (`*_workspace_test`, HowTo*) post
too; delete the repo copies after. PyPI tokens stay until phase 1b. Phase 5 =
`PyAutoMind/policy/github_tokens.md`.

Validation: Mind `python3 -m pytest -q tests/test_spawn_template_contract.py`
(and the full suite), Hands' and the viz repos' own PR CI; witness grep.
One PR per repo.

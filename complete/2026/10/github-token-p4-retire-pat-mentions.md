- summary: Phase 4 of the GitHub token consolidation (parent prompt `github_token_and_secret_setup_full_review`; phase 3 = complete/2026/10/github-token-p3-dispatchers-app.md). On GitHub the same day, the human revoked the personal PATs and the `PAT_PYAUTOLABS` org secret was deleted (`APP_PRIVATE_KEY` is now the only org secret, `APP_CLIENT_ID` the only org variable). In code, the prose still describing the PAT as current was retired: four viz `AGENTS.md` render paragraphs (eyes-refresh uses a per-step App token scoped to PyAutoEyes and fails loudly); Hands `docs/nightly_release_design.md` (the Brain nightly driver's owner-wide App token: actions write, contents read, issues read, variables write); Mind `scripts/spawn.py` rule 9b/9c comments and `docs/pyautobrain/spawn_spec.md` asides (DROP decisions unchanged); the `tests/test_spawn_template_contract.py` arxiv_interests miniature now uses `secrets.APP_PRIVATE_KEY`; and the draft `release_fires_visualization_dispatch.md` now plans an App-token mint (both viz repos, contents write; no silent skip; the dispatch failure stays non-fatal) instead of the PAT, with its human PAT prerequisite removed and the autofit/autocti release receivers noted.
- evidence: Mind tests 703 passed locally. PR CI green on every leg: Mind privacy and Dashboard Refresh (drift skipped on PRs, as always); Hands pytest 3.12/3.13/3.14; viz lint ×4. Witness grep empty in Hands and the four viz repos. In Mind it fails as worded: a negative guard (`tests/test_session_hook_sync.py:391` asserts the literal is absent) and historical lines (#125 test comment, `condemned.md`, a dated search-extensibility survey, the parent prompt's premise). The witness was unpassable by construction, so the merge went through human /prm, not a tiered merge.
- traps: a "grep is empty" witness must exclude negative-assert guard tests and dated history (registries, surveys, parent prompts), or it can never pass.
- deferred: human GitHub settings: org PAT policy (restrict classic PATs, keep fine-grained approval) and one org-level `SLACK_WEBHOOK_URL` (visibility all) so Heart's `secrets: inherit` callers that never held it (`*_workspace_test`, HowTo*) post too, then delete the nine repo copies. Phase 5: policy page `PyAutoMind/policy/github_tokens.md`. Phase 1b: PyPI trusted publishing (blocked on the human's PyPI login); `PYPI` / `TEST_PYPI` stay until then. autocti_visualization phase-3 leg still unproven (draft/bug/autocti_visualization/render_fails_no_module_autonerves.md).
- heart: YELLOW acknowledged by the human 2026-10-23 (manifest drift on one workspace checkout; PyAutoLens release validation stale), unrelated.

## Original prompt

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

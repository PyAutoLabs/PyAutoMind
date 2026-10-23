- summary: Phase 3 of the GitHub token consolidation (parent prompt `github_token_and_secret_setup_full_review`; phases 1/2a/2b = complete/2026/10/github-token-p1-hands-app.md, -p2a-readers-app.md, -p2b-writers-app.md). The seven producer→organ refresh steps, the last `PAT_PYAUTOLABS` readers, moved to a per-step `actions/create-github-app-token@v3` mint (`vars.APP_CLIENT_ID` / `secrets.APP_PRIVATE_KEY`, org-level visibility all; `owner: PyAutoLabs`, `repositories: <organ>`, `permission-contents: write`): four `*_visualization/render.yml` → PyAutoEyes, two `*_profiling/pages_dashboard.yml` → PyAutoPulse, `autolens_inference/inference-summary.yml` → PyAutoInsight. The missing-credential warn-and-skip (`exit 0`) is gone in the six that had it; inference's redundant `::error::` guard was dropped. `autofit_inference` has no such step and was left alone.
- evidence: PR CI (lint) green on all seven. Post-merge proofs, each with mint + dispatch steps successful and an organ-side refresh run: inference-summary 39996518155 (self-triggered on merge) → Insight; render 39996554052 / 39996558589 / 39996563032 → 3 Eyes eyes-refresh runs; pages_dashboard 39996571172 / 39996574531 → 2 Pulse pulse-refresh runs. Org-wide code search: no workflow reads `PAT_PYAUTOLABS` (a stale index hit on autolens_profiling, where main has 0; one prose line in `PyAutoHands/docs/nightly_release_design.md`).
- unproven: autocti_visualization's Eyes leg. Render 39996567008 failed before the mint step (`ModuleNotFoundError: No module named 'autonerves'` under the released PyPI stack; the 09-29 render also failed). The diff is identical to the three proven viz repos. Follow-up: draft/bug/autocti_visualization/render_fails_no_module_autonerves.md.
- traps: `gh pr create` fails in a worktree whose remote is a `git@github.com` alias gh doesn't recognise; pass `--repo`. `gh search code` lags merges, so verify hits against main contents.
- deferred: phase 4 (delete `PAT_PYAUTOLABS` + three personal fine-grained PATs, org PAT policy, Hands design-doc line); phase 5 policy page `PyAutoMind/policy/github_tokens.md`; phase 1b PyPI trusted publishing (blocked on the human's PyPI login).
- heart: YELLOW acknowledged by the human 2026-10-23 (manifest drift on one workspace checkout; PyAutoLens release validation stale), unrelated.

## Original prompt

# GitHub token consolidation phase 3: the seven dashboard dispatchers on the App

Type: release
Target: autolens_visualization
Repos:
- autolens_visualization
- autogalaxy_visualization
- autofit_visualization
- autocti_visualization
- autolens_profiling
- autofit_profiling
- autolens_inference
Difficulty: medium
Unblocked: 2026-10-23 (2b merged — complete/2026/10/github-token-p2b-writers-app.md)
Autonomy: supervised
Priority: high
Status: formalised
Consequence: judge
Parent: draft/release/pyautohands/github_token_and_secret_setup_full_review.md (surveys in `_surveys/`; phase plan in 03_target_design_and_phases.md); phases 1/2a/2b = complete/2026/10/github-token-p1-hands-app.md, -p2a-readers-app.md, -p2b-writers-app.md
Witness: `grep -rn PAT_PYAUTOLABS .github/workflows` is empty in all seven repos (and owner-wide, `gh search code PAT_PYAUTOLABS org:PyAutoLabs` finds no workflow reader); no warn-and-skip on a missing credential; one green dispatch per repo whose organ refresh run is visible in PyAutoEyes / PyAutoPulse / PyAutoInsight
Review-minutes: 20
Unattended: never
Issued: 2026-10-23

The last `PAT_PYAUTOLABS` readers are seven producer→organ refresh steps. Each
sends one `repository_dispatch` to an organ repo:

- `autolens_visualization`, `autogalaxy_visualization`, `autofit_visualization`,
  `autocti_visualization` — `.github/workflows/render.yml`, step "Tell the
  PyAutoEyes dashboard to refresh" → `repos/PyAutoLabs/PyAutoEyes/dispatches`
  (`eyes-refresh`). Currently warns and `exit 0` without the PAT.
- `autolens_profiling`, `autofit_profiling` — `.github/workflows/pages_dashboard.yml`,
  step "Tell the PyAutoPulse dashboard to refresh" → PyAutoPulse (`pulse-refresh`).
  Currently warns and skips.
- `autolens_inference` — `.github/workflows/inference-summary.yml`, step
  "Refresh PyAutoInsight after successful publication" → PyAutoInsight
  (`insight-refresh`). Already fails loud; just swap the credential.
  (`autofit_inference` has no such step — confirm, leave it alone.)

Per step: add a preceding `actions/create-github-app-token@v3` step
(`client-id: ${{ vars.APP_CLIENT_ID }}`, `private-key: ${{ secrets.APP_PRIVATE_KEY }}`,
`owner: PyAutoLabs`, `repositories: <the one organ repo>`,
`permission-contents: write` — what `POST /repos/{o}/{r}/dispatches` needs), feed its
`token` output to `GH_TOKEN`, delete the empty-token warn-and-skip branch (the mint
step fails loudly on its own), and rewrite the header comments that describe the PAT.
`APP_CLIENT_ID` / `APP_PRIVATE_KEY` are org-level with visibility `all` (checked
2026-10-23), so no per-repo secret wiring. One PR per repo.

These are workspace-shaped repos with no library dependency, so no library-first
gate. Watch the known traps: viz `lint` clones library mains and runs
`ruff format --check` (memory `vizLintMains`); profiling `build_dashboard --check`
(memory `profThemeRed`) — a workflow-only PR should not touch either, but read the
PR CI rather than assume.

Validation per repo: YAML parse + actionlint (ignore the known `client-id` false
positive); each repo's own PR CI. Proof: after merge (or on the branch if the
workflow can be dispatched there without publishing anything wrong), one dispatch per
repo whose refresh step succeeds and whose organ-side run appears. A render/publish
dispatch on main is the producer's normal operation, so it is safe; prefer the
cheapest input (e.g. a single-surface render) where the workflow offers one.

After this phase `PAT_PYAUTOLABS` has no readers; phase 4 deletes it, the three
personal fine-grained PATs and sets the org PAT policy; phase 5 writes
`PyAutoMind/policy/github_tokens.md`.

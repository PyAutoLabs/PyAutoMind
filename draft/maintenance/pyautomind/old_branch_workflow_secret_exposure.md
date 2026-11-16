# Old Mind branches carry injectable workflows that hold org secrets

Type: maintenance
Target: PyAutoMind
Repos:
- PyAutoMind
Difficulty: medium
Autonomy: human-required
Priority: high
Status: draft
Filed: 2026-11-13
Epic: autonomous-orchestrators
Consequence: judge
Witness: `gh api repos/PyAutoLabs/PyAutoMind/environments` lists an environment, restricted to deployment branch `main`, that holds `CLAUDE_CODE_OAUTH_TOKEN` and `APP_PRIVATE_KEY`, and every workflow using them declares it; a `workflow_dispatch` of `arxiv_papers.yml` at an old `claude/*` ref fails to read the secrets; old heads carrying pre-`5a5d9dd80` workflows are pruned or listed with an owner
Review-minutes: 20
Unattended: never
Lane: local-dev

Source: independent security review of PyAutoMind#565 (2026-11-13). Anyone with Actions write on PyAutoMind (today: org admins/maintainers; design B's browser token would have added more) can dispatch a workflow **at any ref**. `git ls-remote` shows 244 heads (claude/*, ccr-*, chatgpt/*, archive/*) predating the injection hardening (`5a5d9dd80`): e.g. `arxiv_papers.yml:90` `override="${{ github.event.inputs.lookback_hours }}"`, `mind_ledger_merge.yml:87` `BRANCH="${{ inputs.branch }}"` → a shell in a job holding `CLAUDE_CODE_OAUTH_TOKEN` (and the org `APP_PRIVATE_KEY` on newer branches), or with `contents:write` on an unprotected `main` (→ `.claude/hooks/session-start.sh` → code on laptop and RAL). No Environment gates the secrets today.

Fix (human acts, admin): move the Claude and App secrets into an Environment with deployment branch policy `main`; protect Mind `main` (M2.2 deferred Mind to M4.3 — revisit); prune or archive the old heads (after checking none is in use); correct `policy/github_tokens.md`'s table to say "safe on main; old refs exposed until pruned".

## Progress
- 2026-11-16: the lead created the `mind-main` environment (deployment branch `main`, `can_admins_bypass: false`). PyAutoMind#573 merged (f4bd95435): 10 jobs in 8 workflows declare it; `tests/test_workflow_environment.py`; `policy/github_tokens.md` gains an "Old refs" paragraph. The independent security review (FINDINGS) found that old heads can still push to an unprotected `main` through a pre-hardening `mind_ledger_merge.yml`, so the move alone does not close the hole.
- Human acts pending: `Science/scratch/mind_secrets_move_2026-11-16/step1_set_env_secrets.sh`, then a lead dry run of `spawn_drift` on main, then `step2_remove_old_copies.sh`, then the human's choice to prune the pre-`5a5d9dd80` heads (recommended) or protect `main`.
- 2026-11-16 (human: "b for November branches, a for the rest"): 193 merged pre-hardening heads deleted. Of the 50 unmerged, the 28 from November were brought up to main's hardened workflows (1 merged main; 27 conflicted, so they took main's `.github/workflows/` only) and the 22 older ones were deleted. A backup bundle of every head is in `Science/scratch/mind_branch_prune_2026-11-16/` (with lists). Witness: PyAutoMind has 32 heads; running `test_workflow_input_injection.py` on each head's workflows finds 0 unsafe. **Remaining:** the human's step 2 (repo-level Claude token still present; org `APP_PRIVATE_KEY` still visibility `all`, holding the OLD key; do not delete the old App key before step 2).

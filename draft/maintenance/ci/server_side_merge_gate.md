# A server-side merge gate on the repos that have real checks

Type: maintenance
Target: PyAutoLabs org (repository settings) — GitHub config, plus a doctrine edit in PyAutoBrain
Repos:
- (org-level) PyAutoLabs — the libraries, workspaces and tested organs
- PyAutoBrain
Difficulty: medium
Autonomy: human-required
Priority: normal
Status: draft
Filed: 2026-11-10
Epic: autonomous-orchestrators
Consequence: judge
Witness: `gh api repos/PyAutoLabs/<repo>/rulesets` shows an active ruleset on the default branch requiring the named checks, for every repo on the agreed list; a test PR with a failing required check is refused by `gh pr merge`, and `gh pr merge --auto` merges it once the check is green
Review-minutes: 30
Unattended: never
Lane: local-dev

Source: the ecosystem review of 2026-11-10, finding PR-3, confirmed by an independent verifier. Report: https://claude.ai/artifact/4A94P1cevvkESoM22QoMWm (private) and `Science/scratch/ecosystem_review_2026-11/REPORT.md`, section B4 and Appendix A. Data: `evidence/pr_history/repo_settings.csv`.

**What was measured.** None of the 51 manifest repos has a server-side merge gate on its default branch. The only ruleset present, "Default Copilot PR review" in 23 repos, is disabled. `allow_auto_merge` is false in all 51. Of 1,952 PRs merged between 2026-09-01 and 2026-11-09, 0 carry an approving GitHub review. The green-before-merge rule is enforced only on the client, by the `/prm` skill and the tiered-merge rules in `AUTONOMY.md`; `gh pr merge` is pre-approved in the permission allow-list and no hook checks CI state.

The discipline has held with one human merging: 11 PRs (0.57%) merged with a failing check. With 5 to 20 unattended workers, one that merges on a red or pending check breaks `main` for every other worker cloning it.

**The change.**
1. Agree the list: the libraries, the workspaces and the organs with real PR checks. For each, name the required checks.
2. Apply a ruleset on the default branch requiring those checks. Exempt the bot identities that push self-heal and ledger commits.
3. Enable `allow_auto_merge`, so a worker can merge with `gh pr merge --auto` and GitHub enforces green.
4. Record the independent review verdict as a PR review or a required status, so that it is visible and enforceable.

**Two things that make this the human's.**
- The `pyautolabs-bot` App deliberately has no repo admin, and the old `repo_settings.yml` sweep was retired, so rulesets must be applied with the human's own admin credential. Hence `Lane: local-dev` and `Autonomy: human-required`.
- `AUTONOMY.md:521-523` explicitly defers `gh pr merge --auto` pending its own doctrine edit. Adopting it is a doctrine change, so this is `judge`.

Related, and different: `draft/maintenance/ci/copilot_auto_review.md` is about requesting a review, not about gating a merge.

<!-- filed 2026-11-10 by the ecosystem review (draft/research/pyautobrain/ecosystem_review_for_autonomous_runs.md); headers mirror intake's -->

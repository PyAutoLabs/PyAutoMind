## standards-discovery-deferred
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/474
- completed: 2026-10-06
- library-pr: https://github.com/PyAutoLabs/PyAutoArray/pull/614
- workspace-pr: https://github.com/PyAutoLabs/euclid_strong_lens_modeling_pipeline/pull/110
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/476

Final wave of `standards-discovery` (`complete/2026/10/standards-discovery.md`, 44/46). With it, the generated shared-standards discovery block is on main in **46/46** registered destinations. Mind#474 was closed as completed with a final Shipped comment.

Merged 2026-10-06 via human /prm (tier `judge`, so no shadow row):
- PyAutoArray#614 (merge f2ced12e): generated `AGENTS.md` block only. It ran alongside the `nnls-memo-scattered-backoff` claim with the human's approval.
- euclid_strong_lens_modeling_pipeline#110 (merge c22fda97): generated `AGENTS.md` block only. Its pytest and smoke legs were **not run**. The Heart reusable-workflow relevance gate skips them on an `AGENTS.md`-only diff, so they were structurally inapplicable. The legs were skipped, not passed, and that counts as untested rather than green.
- PyAutoMind#476 (merge ce3a7611): restores universal standards grading in `.github/workflows/firewall_gate.yml`. It removes the staged-rollout comment and the `--skip "shared-standards blocks (generated)"` from the broad clone-main legs. The post-merge push run of Tenant Firewall Gate on ce3a7611 passed (`firewall` check success).

All three `feature/standards-discovery-deferred` heads were proven ancestors of `origin/main` with `git merge-base --is-ancestor`.

Universal completion audit: I ran `repos_sync.py` against fresh clones of all 46 registered `origin/main`s. `--check --only "shared-standards blocks (generated)"` reported OK on 46/46, with no deferred targets and no missing clones. The full `--check` passed on every leg. Evidence is in `tmp/standards-discovery/deferred/`: `universal-mains.log`, the per-repo write/check logs and diffs, and `ci_conclusions.log`.

Instruction-only change; no pending-release obligation.

Parent initiative `draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md` is now fully shipped and was retired with its own record, `complete/2026/10/standardize-dashboard-orchestration-prompt-panel.md`.

## Original prompt

# Finish the generated standards-discovery rollout: PyAutoArray and the Euclid pipeline

Type: feature
Target: PyAutoMind
Repos:
- PyAutoArray
- euclid_strong_lens_modeling_pipeline
- PyAutoMind
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised
Consequence: judge
Blocked-by: active.md claims `nnls-memo-scattered-backoff` (PyAutoArray, PyAutoLabs/PyAutoArray#613) and `vis-lp-inspection-bundle` (euclid_strong_lens_modeling_pipeline, PyAutoLabs/euclid_strong_lens_modeling_pipeline#102) — start each destination only once its claim has cleared from active.md
Witness: `python3 scripts/repos_sync.py --check --only "shared-standards blocks (generated)"` over all available registered checkouts reports 46/46 present and current with no deferred targets; Mind `firewall_gate.yml` broad legs no longer `--skip "shared-standards blocks (generated)"` and are green on main.
Review-minutes: 10
Unattended: needs-slicing
Filed: 2026-10-06
Issued: 2026-10-06

- Status: split out of `standards-discovery` at close-out — 44/46 destinations shipped in
  `complete/2026/10/standards-discovery.md` (generator PyAutoMind#475, contract PyAutoBrain#483,
  33 consumer PRs) and `complete/2026/10/orchestration-panel-consumers.md` (nine panel consumers).
  Initiative issue: https://github.com/PyAutoLabs/PyAutoMind/issues/474 (left OPEN for this remainder).
  Parent initiative: `draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md`.

## What remains (already approved under the parent plan — finish it, do not re-plan)

1. **PyAutoArray** — once `nnls-memo-scattered-backoff` is gone from `active.md`, ff-pull main and
   run the bounded generator for that repo only, in an isolated `feature/standards-discovery-deferred`
   worktree:
   `python3 scripts/repos_sync.py --write --only "shared-standards blocks (generated)" --repo PyAutoArray`
   Validate that only `AGENTS.md` changed, that everything outside the generated markers is
   preserved byte-for-byte, and that `--check --only "shared-standards blocks (generated)" --repo PyAutoArray`
   is clean. One instruction-only PR.
2. **euclid_strong_lens_modeling_pipeline** — same procedure once `vis-lp-inspection-bundle` clears
   (`--repo euclid_strong_lens_modeling_pipeline`). Note the pipeline's PR CI relevance gate skips
   pytest on non-code diffs; skipped legs are not green — judge them as structural explicitly.
3. **Restore broad firewall checking** — only after both destination PRs merge: remove the staged
   rollout scope in Mind `.github/workflows/firewall_gate.yml` (the "Standards rollout is staged across
   consumer PRs (#474)" comment, the `skip=(--skip "shared-standards blocks (generated)")` and the
   `--skip "shared-standards blocks (generated)"` in the broad clone-main legs) so the standards leg is
   checked against sibling mains like every other leg. Keep the hermetic generator tests and the
   Mind-owned `--repo PyAutoMind` check.
4. **Universal completion audit** — run the default `--check --only "shared-standards blocks (generated)"`
   across all available registered checkouts; record the denominator (46), any missing clones by
   name/reason, and confirm zero deferred targets remain. Then close Mind#474 and retire the parent
   initiative prompt if nothing else remains in it.

Each destination is independently shippable: if only one claim has cleared, ship that one and
leave this prompt open for the other (record the partial scope at close-out as before).
Tier: judge; merge mode: human /prm.

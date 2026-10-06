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

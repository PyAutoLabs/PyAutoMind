## standards-discovery
- issue: https://github.com/PyAutoLabs/PyAutoMind/issues/474
- completed: 2026-10-06
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/475
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/483
- library-pr: https://github.com/PyAutoLabs/PyAutoCortex/pull/57
- library-pr: https://github.com/PyAutoLabs/PyAutoHeart/pull/287
- library-pr: https://github.com/PyAutoLabs/PyAutoFit/pull/1660
- library-pr: https://github.com/PyAutoLabs/PyAutoGalaxy/pull/648
- library-pr: https://github.com/PyAutoLabs/PyAutoLens/pull/769
- library-pr: https://github.com/PyAutoLabs/PyAutoReduce/pull/80
- library-pr: https://github.com/PyAutoLabs/PyAutoCTI/pull/113
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace/pull/166
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace/pull/255
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace/pull/584
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace/pull/36
- workspace-pr: https://github.com/PyAutoLabs/autoreduce_workspace/pull/4
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_test/pull/106
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/127
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_test/pull/344
- workspace-pr: https://github.com/PyAutoLabs/autocti_workspace_test/pull/23
- workspace-pr: https://github.com/PyAutoLabs/autofit_workspace_developer/pull/28
- workspace-pr: https://github.com/PyAutoLabs/autolens_workspace_developer/pull/146
- workspace-pr: https://github.com/PyAutoLabs/HowToFit/pull/70
- workspace-pr: https://github.com/PyAutoLabs/HowToGalaxy/pull/84
- workspace-pr: https://github.com/PyAutoLabs/HowToLens/pull/95
- workspace-pr: https://github.com/PyAutoLabs/autocti_assistant/pull/35
- workspace-pr: https://github.com/PyAutoLabs/autofit_assistant/pull/54
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_assistant/pull/33
- workspace-pr: https://github.com/PyAutoLabs/autolens_assistant/pull/152
- workspace-pr: https://github.com/Jammy2211/euclid_assistant/pull/14
- workspace-pr: https://github.com/PyAutoLabs/autolens_profiling/pull/386
- workspace-pr: https://github.com/PyAutoLabs/autolens_inference/pull/19
- workspace-pr: https://github.com/PyAutoLabs/autolens_visualization/pull/2
- workspace-pr: https://github.com/PyAutoLabs/autogalaxy_visualization/pull/2
- workspace-pr: https://github.com/PyAutoLabs/autofit_visualization/pull/2
- workspace-pr: https://github.com/PyAutoLabs/autocti_visualization/pull/2
- workspace-pr: https://github.com/PyAutoLabs/pyautolabs.github.io/pull/29
- library-pr: https://github.com/PyAutoLabs/PyAutoMind/pull/475
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/483
- partial: 44/46 destinations shipped; PyAutoArray and euclid_strong_lens_modeling_pipeline deferred
- remainder: draft/feature/pyautomind/standards_discovery_deferred_destinations.md

**Partial close — merged scope only.** Issue Mind#474 stays OPEN (progress comment posted) until the two deferred destinations land.

Merged 2026-10-06 via human /prm (tier `judge`; no shadow row): generator Mind#475 (72087111), contract docs Brain#483 (bdebd4e1) and 33 consumer PRs — Cortex#57, Heart#287, Fit#1660, Galaxy#648, Lens#769, Reduce#80, CTI#113, autofit_workspace#166, autogalaxy_workspace#255, autolens_workspace#584, autocti_workspace#36, autoreduce_workspace#4, autofit_workspace_test#106, autogalaxy_workspace_test#127, autolens_workspace_test#344, autocti_workspace_test#23, autofit_workspace_developer#28, autolens_workspace_developer#146, HowToFit#70, HowToGalaxy#84, HowToLens#95, autocti_assistant#35, autofit_assistant#54, autogalaxy_assistant#33, autolens_assistant#152, Jammy2211/euclid_assistant#14, autolens_profiling#386, autolens_inference#19, autolens_visualization#2, autogalaxy_visualization#2, autofit_visualization#2, autocti_visualization#2, pyautolabs.github.io#29. Every feature/standards-discovery head (35 worktree repos) proven an ancestor of origin/main; all 35 PRs `merged=true` via the API. The nine panel consumers' generated blocks shipped on their own branches (`complete/2026/10/orchestration-panel-consumers.md`). Total: **44/46** registered destinations carry the generated block on main.

What shipped: Mind `policy/shared_standards.md` (one canonical universal discovery text plus a board-owner addition selected from explicit manifest board-owner metadata for the 13 owners); `scripts/repos_sync.py` bounded standards writer/checker (`shared-standards blocks (generated)`) with repeatable `--repo NAME`, flag/identity/marker validation before any mutation, partial-checkout denominator reporting and explicit deferred-target reporting; `tests/test_repos_sync_standards_block.py`; Brain `docs/standards.md` contract docs. Validation: 652 generator tests, 33 adversarial/standards cases, independent re-review CLEAN, strict Brain docs build passed. RTD `standards.html` + `board-orchestration.html` live 14:40:08 UTC.

CI judged once at each exact head; skipped legs structural (Heart smoke relevance gate on AGENTS.md-only diffs; Reduce unittest-nojax excluded for autoreduce; Mind Spawn Drift push-only). Cortex, both *_workspace_developer repos and pyautolabs.github.io have no applicable CI and passed local `repos_sync.py --check --only "shared-standards blocks (generated)"`. Evidence: `tmp/ci-census/20261006T142801Z/`, `tmp/standards-discovery/` (audit.md, shipped.md, worktree-tmp/).

**Deferred (not shipped, re-filed):** PyAutoArray (held by active claim `nnls-memo-scattered-backoff`, PyAutoArray#613) and euclid_strong_lens_modeling_pipeline (held by active claim `vis-lp-inspection-bundle`, euclid_strong_lens_modeling_pipeline#102). Mind `.github/workflows/firewall_gate.yml` keeps its staged standards rollout scope (target-owned check + `--skip "shared-standards blocks (generated)"` in the broad clone-main legs) until both land. Remainder: `draft/feature/pyautomind/standards_discovery_deferred_destinations.md`.

Instruction-only change; no pending-release obligation.

## Original prompt

# Generate and distribute shared standards discovery

Type: feature
Target: PyAutoMind
Difficulty: medium
Autonomy: supervised
Consequence: judge
Review-minutes: 10
Unattended: needs-slicing
Status: active
Issued: 2026-10-06
Issue: https://github.com/PyAutoLabs/PyAutoMind/issues/474

## Original user request (verbatim)

ok do those next tasks

## Approved scope and plan

This is the approved instruction-discovery phase of draft/feature/pyautobrain/standardize_dashboard_orchestration_prompt_panel.md. Reuse Brain docs/standards.md as canonical contract and preserve all existing guidance.

1. Add one concise Mind policy source, canonical GitHub standards link and explicit manifest board-owner metadata for thirteen board owners. Universal text asks agents to consult applicable standards on demand, identify consumers and validate adoption; only board owners get board component guidance.
2. Extend scripts/repos_sync.py with a bounded standards writer/checker and repeatable --repo filter. Validate flags, identities and marker integrity before mutation; scoped standards writes must not touch any unrelated generated artifacts. Report missing/stale guidance and partial-checkout coverage honestly. Default universal audit remains strict for available registered checkouts; no permanent exceptions for temporarily claimed repos.
3. Cover idempotence, preservation, missing/malformed/stale blocks, owner/nonowner variants, invalid selections with zero writes, and partial grouped/flat checkouts using meaningful synthetic fixtures. CI checks the generator and target-owned block without requiring not-yet-merged consumer mains to have migrated; document that scope explicitly.
4. Generate blocks into all eligible repository worktrees. There are 46 registered repositories. PyAutoArray and euclid_strong_lens_modeling_pipeline are deferred because of active claims. Nine panel consumers receive generated guidance on their existing panel task branches; Brain follows after sizing #480 clears. All others get isolated standards-discovery worktrees and instruction-only PRs. Preserve unrelated dirty canonical checkouts.
5. Record coverage and exact generated diffs. Run generator tests and relevant drift checks, open tested PRs for source plus eligible destinations, and leave human /prm. Deferred destinations remain recorded work, not completed rollout. No RTD source move.

## Branch survey

All 46 registered repositories exist on main with tracked clean AGENTS.md. Some have unrelated canonical changes; use isolated task branches. Initial claims: 34 repositories excluding the nine panel consumers, Brain sizing, and two external active claims. Branch feature/standards-discovery.

Tier: judge; merge mode: human /prm.

## PRs opened — 2026-10-06

35 tested PRs open, plus nine generated consumer blocks carried by orchestration-panel-consumers. Generator 652 tests, 33 adversarial/standards cases, independent re-review CLEAN; strict Brain docs build passed. Combined source audit: 44/46 blocks present. Array and Euclid pipeline deferred for nnls-memo-scattered-backoff / vis-lp-inspection-bundle claims. Human /prm; do not close entire parent initiative until deferred destinations and publication verification are complete.

| Repository | PR |
|---|---|
| PyAutoCortex | https://github.com/PyAutoLabs/PyAutoCortex/pull/57 |
| PyAutoHeart | https://github.com/PyAutoLabs/PyAutoHeart/pull/287 |
| PyAutoFit | https://github.com/PyAutoLabs/PyAutoFit/pull/1660 |
| PyAutoGalaxy | https://github.com/PyAutoLabs/PyAutoGalaxy/pull/648 |
| PyAutoLens | https://github.com/PyAutoLabs/PyAutoLens/pull/769 |
| PyAutoReduce | https://github.com/PyAutoLabs/PyAutoReduce/pull/80 |
| PyAutoCTI | https://github.com/PyAutoLabs/PyAutoCTI/pull/113 |
| autofit_workspace | https://github.com/PyAutoLabs/autofit_workspace/pull/166 |
| autogalaxy_workspace | https://github.com/PyAutoLabs/autogalaxy_workspace/pull/255 |
| autolens_workspace | https://github.com/PyAutoLabs/autolens_workspace/pull/584 |
| autocti_workspace | https://github.com/PyAutoLabs/autocti_workspace/pull/36 |
| autoreduce_workspace | https://github.com/PyAutoLabs/autoreduce_workspace/pull/4 |
| autofit_workspace_test | https://github.com/PyAutoLabs/autofit_workspace_test/pull/106 |
| autogalaxy_workspace_test | https://github.com/PyAutoLabs/autogalaxy_workspace_test/pull/127 |
| autolens_workspace_test | https://github.com/PyAutoLabs/autolens_workspace_test/pull/344 |
| autocti_workspace_test | https://github.com/PyAutoLabs/autocti_workspace_test/pull/23 |
| autofit_workspace_developer | https://github.com/PyAutoLabs/autofit_workspace_developer/pull/28 |
| autolens_workspace_developer | https://github.com/PyAutoLabs/autolens_workspace_developer/pull/146 |
| HowToFit | https://github.com/PyAutoLabs/HowToFit/pull/70 |
| HowToGalaxy | https://github.com/PyAutoLabs/HowToGalaxy/pull/84 |
| HowToLens | https://github.com/PyAutoLabs/HowToLens/pull/95 |
| autocti_assistant | https://github.com/PyAutoLabs/autocti_assistant/pull/35 |
| autofit_assistant | https://github.com/PyAutoLabs/autofit_assistant/pull/54 |
| autogalaxy_assistant | https://github.com/PyAutoLabs/autogalaxy_assistant/pull/33 |
| autolens_assistant | https://github.com/PyAutoLabs/autolens_assistant/pull/152 |
| euclid_assistant | https://github.com/Jammy2211/euclid_assistant/pull/14 |
| autolens_profiling | https://github.com/PyAutoLabs/autolens_profiling/pull/386 |
| autolens_inference | https://github.com/PyAutoLabs/autolens_inference/pull/19 |
| autolens_visualization | https://github.com/PyAutoLabs/autolens_visualization/pull/2 |
| autogalaxy_visualization | https://github.com/PyAutoLabs/autogalaxy_visualization/pull/2 |
| autofit_visualization | https://github.com/PyAutoLabs/autofit_visualization/pull/2 |
| autocti_visualization | https://github.com/PyAutoLabs/autocti_visualization/pull/2 |
| pyautolabs.github.io | https://github.com/PyAutoLabs/pyautolabs.github.io/pull/29 |
| PyAutoMind | https://github.com/PyAutoLabs/PyAutoMind/pull/475 |
| PyAutoBrain | https://github.com/PyAutoLabs/PyAutoBrain/pull/483 |

CI was judged once at each exact head: no failures observed; pending, skipped and absent checks are not green. The corresponding CI snapshots and local validation artifacts are preserved in the session scratch evidence. No timers, watchers or automatic merge subscriptions remain.

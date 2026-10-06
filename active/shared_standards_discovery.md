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

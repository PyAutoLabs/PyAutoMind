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

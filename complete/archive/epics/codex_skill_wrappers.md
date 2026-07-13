# Codex wrappers for PyAuto agent workflows

Type: maintenance
Target: PyAutoBrain
Difficulty: large
Autonomy: supervised
Priority: normal
Status: phased

## Original request

> yes, make SKILL.md wrappers for PyAutoBrain and any other repos you see a Claude bias

## Phases

1. [PyAutoBrain agent wrappers and dual-harness installer](../maintenance/pyautobrain/codex_brain_skill_wrappers.md)
2. [Cross-organ Codex skill wrappers](../maintenance/pyautobrain/codex_organ_skill_wrappers.md)
3. [Normalize profiling skill metadata](../maintenance/autolens_profiling/codex_skill_metadata.md)

Phase 2 depends on the dual-harness installer and wrapper conventions established
by phase 1. Phase 3 was added when independent review found legacy underscore
metadata in `profile_likelihood`; it waits for the active profiling worktree
claims to clear. `admin_jammy` was audited and no longer hosts skills.

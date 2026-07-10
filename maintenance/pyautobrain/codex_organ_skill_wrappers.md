# Add Codex wrappers across the remaining PyAuto organs

Type: maintenance
Target: PyAutoBrain
Repos:
- @PyAutoMind
- @PyAutoHeart
- @PyAutoBuild
Difficulty: medium
Autonomy: safe
Priority: normal
Status: formalised

Depends on: `maintenance/pyautobrain/codex_brain_skill_wrappers.md`

## Original request

> yes, make SKILL.md wrappers for PyAutoBrain and any other repos you see a Claude bias

## Scope

Apply the phase-1 wrapper and installer contract to command-only canonical
skills in PyAutoMind, PyAutoHeart, and PyAutoBuild. Update ownership and usage
wording that assumes Claude is the only harness. Preserve Heart's intentional
reference-only `/health` legs as non-top-level skills.

## Acceptance criteria

- `spawn`, `review_release`, `verify_install`, and `pre_build` are Codex skills.
- Existing Claude command behavior remains available.
- Cross-organ ownership documentation describes both harnesses.
- All wrappers pass the same validation and isolated installer tests as phase 1.

# Eyes gallery: extract gallery/ from autolens_workspace_test scripts tree

Type: refactor
Target: pyautobrain
Repos:
- PyAutoBrain
- autolens_workspace_test
Difficulty: easy
Autonomy: supervised
Priority: low
Status: formalised
Blocked-by: draft/refactor/autolens_workspace_test/mirror_restructure_and_cull.md (do after the restructure settles)

Small follow-on to the Phase 2 restructure. `scripts/gallery/`
(gallery_build.py + gallery_run.sh) is a build tool for the Eyes agent, not a
test — but it is the ONE move with cross-repo breakage risk, so it was
excluded from the restructure and gets its own task.

**Coupling map (2026-07-23 survey):**
- PyAutoBrain Eyes hard-codes `scripts/gallery/gallery_run.sh` /
  `gallery_build.py` relative to the workspace root it is pointed at:
  `agents/conductors/eyes/_eyes.py:207` (root), `:84` (output/gallery),
  plus eyes.sh, AGENTS.md:16,25, skills/eyes/{SKILL.md,eyes.md},
  skills/COMMANDS.md, tests/test_eyes_conductor.py.
- gallery_build.py assumes its own depth (`parents[2]`); gallery_run.sh does
  `cd $(dirname)/../..` and enumerates `scripts/<domain>/visualization*.py`.
- It renders the domain visualization scripts IN PLACE, so gallery must live
  in (or be pointed at) the workspace holding those scripts.

**The task.** Decide placement and repoint everything in one lockstep change:
either (a) keep gallery inside the test workspace but outside `scripts/`
(e.g. `gallery/` at repo root, so the scripts tree is tests-only), or
(b) move the harness into PyAutoBrain's Eyes agent and parameterise the
workspace root. Option (a) is smaller and keeps the render-in-place
invariant; recommend (a) unless the Eyes design argues otherwise. Update the
`# PERMANENT` no_run entry, all PyAutoBrain path references, and
test_eyes_conductor.py in the same change. Also address the survey's
gallery-tier oddity while here: gallery_build.py ran standalone in the
release sweep and failed as a "test" (documented sys.exit(1), July RED
blocker autolens_workspace_test#195) — after the move, ensure no runner can
pick it up as a script again.

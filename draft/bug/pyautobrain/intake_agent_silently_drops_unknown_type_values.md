# Intake Agent silently drops unknown Type values and overrides declared Target and Repos

Type: bug
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: safe
Priority: medium
Status: formalised
Consequence: glance
Witness: a pytest that feeds each of the four inputs above through the intake decision and asserts the written header equals the declared header, the path is under the declared target, and `Type: hygiene` raises/flags — red on main, green after the fix.
Review-minutes: 3
Unattended: ready

Observed across five /intake runs on 2026-09-16 (config-priors-drift follow-ups, config-yaml-comments prompt). The Intake (Conception) Agent, `PyAutoBrain/agents/conductors/intake/_intake.py`, mishandles declared headers in four ways, each requiring a hand fix of the written file:
1. A declared `Type: hygiene` is not in WORK_TYPES (`agents/faculties/sizing/_sizing.py`, valid home is `maintenance`) and is DROPPED SILENTLY — the decision then infers `feature` or `docs` with no warning that the declaration was rejected. An unknown declared Type should be an explicit error or a visible "(declared: hygiene → unknown, using maintenance)" note.
2. A declared `Target:` is overridden by the repo scraper (`Target: autogalaxy` → PyAutoArray; `Target: autofit` → PyAutoArray; `Target: workspaces` → PyAutoFit) and the file is re-homed under the wrong folder, although the decision prints Type/Difficulty/Autonomy/Priority as "(declared)". Target should be honoured the same way.
3. A declared `Repos:` list is reordered, its names rewritten, and superset entries added from prose mentions — including a phantom `workspaces` repo that is not a repo — instead of being taken as written.
4. When the header block is the first line of the input, the header line itself becomes the title/slug (`draft/bug/autogalaxy/target_autogalaxy.md`), and the raw header block is duplicated into the body below the real header.

Fix: honour declared Target and Repos exactly as Type/Difficulty/Autonomy/Priority are honoured; make an unknown declared Type an explicit error naming the valid set; derive the title from the first non-header line; do not echo the header block into the body. Add unit tests for each of the four inputs above. Related memory of traps: TargetIgn (declared Target ignored), hdr×5 (agent mangles declared headers).

Witness: a pytest that feeds each of the four inputs above through the intake decision and asserts the written header equals the declared header, the path is under the declared target, and `Type: hygiene` raises/flags — red on main, green after the fix.

<!-- formalised by the Intake (Conception) Agent on 2026-09-16 from user-intake -->

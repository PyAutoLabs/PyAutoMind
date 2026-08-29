# Finish the science-project memory propagation: autofit_assistant sync and autocti_assistant birth-substitution gaps

Type: maintenance
Target: PyAutoBrain
Repos:
- autocti_assistant
- autofit_assistant
- autolens_assistant
- PyAutoBrain
Difficulty: medium
Autonomy: supervised
Priority: medium
Status: formalised

# Finish the science-project memory propagation: autofit_assistant sync and autocti_assistant birth-substitution gaps

Type: maintenance
Difficulty: medium
Autonomy: supervised
Priority: medium

Follow-up to PyAutoBrain#315 (science-project memory), whose work sits on the pushed
`feature/science-project-memory` branches in PyAutoBrain and the three assistant cells.
Blocked-by: those #315 branches merging first — do not start this until they are on main,
because both legs below build directly on the `clone sync` lever that #315 introduces.

Leg (a) — the autofit_assistant copy. #315 deliberately stopped at a dry run for it and
posted the report on the issue: 1 hunk applied, 2 created, 4 rejected across four generic
files (AGENTS.md, skills/start-new-project.md, wiki/project/README.md,
wiki/project/_profile_template.md). Name-normalised divergence from the reference copy is
193 / 221 / 56 / 101 changed lines respectively. A human must read that report first and
decide, file by file, which of that divergence is deliberate domain adaptation (fitting and
inference framing that should be preserved) and which is drift that should be reconciled.
Once that call is made, apply the `pyauto-brain clone sync` from the reference copy in
autolens_assistant to autofit_assistant, hand-resolving the rejected hunks the same way #315
resolved them for the other cells.

Leg (b) — autocti_assistant birth-time substitution gaps. Two artefacts of the clone birth
survived the propagation: wiki/project/_profile_template.md still carries a
"Lensing background" heading, and the start-new-project scaffold still names the
`$AUTOLENS_ASSISTANT` variable. Fix these at source, in the reference substitution rules of
the clone conductor, so that both `clone sync` and a fresh birth handle the heading text and
the assistant-path variable — not by hand-editing the two files in the cell. Then re-sync
autocti_assistant so the corrected substitutions land there, and confirm no sibling cell
carries the same two gaps.

Done when: autofit_assistant's four generic files are reconciled per the human decision,
the clone conductor's substitution rules cover both gap classes with test coverage, and
autocti_assistant is re-synced clean.

<!-- formalised by the Intake (Conception) Agent on 2026-08-28 from file:/tmp/claude-1000/-home-jammy-Code-PyAutoLabs/069a02ef-b14f-4a43-b0c3-92e461ddef66/scratchpad/intake_followup.md -->

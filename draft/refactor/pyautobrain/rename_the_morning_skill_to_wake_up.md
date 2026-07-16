# Rename the morning skill to wake_up (PyAutoBrain)

Type: refactor
Target: PyAutoBrain
Repos:
- PyAutoBrain
Difficulty: small
Autonomy: supervised
Priority: normal
Status: formalised

Rename the morning skill to wake_up in @PyAutoBrain (skills/morning/ -> skills/wake_up/), adjusting all linked files accordingly (symlinks in ~/.claude/commands and ~/.claude/skills, COMMANDS.md, AGENTS.md, AUTONOMY.md, bin/overnight_status.sh, nightly.sh references) so it fits the PyAutoScientist organism analogy. The skill is proving very valuable; keep behaviour identical. Include a short assessment of what else the skill could absorb without becoming information overload.

<!-- formalised by the Intake (Conception) Agent on 2026-07-16 from user-intake -->

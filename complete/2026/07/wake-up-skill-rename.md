## wake-up-skill-rename
- issue: https://github.com/PyAutoLabs/PyAutoBrain/issues/114 (closed)
- completed: 2026-07-16
- library-pr: https://github.com/PyAutoLabs/PyAutoBrain/pull/115 (merged 6caa6c4, merge commit)
- repos: PyAutoBrain
- summary: Renamed the /morning composition skill to /wake_up to fit the organism analogy (the organism wakes: syncs its body, checks its vitals, remembers what it was doing). Pure behaviour-preserving rename: skills/morning/ -> skills/wake_up/ (body file + SKILL.md name), /morning references updated in COMMANDS.md, AGENTS.md, AUTONOMY.md, bin/overnight_status.sh and nightly.sh comments. Deliberately untouched: Heart's morning_health/morning_status Slack webhooks (separately named automation), historical Mind records, time-of-day prose, and the SKILL.md discovery trigger "morning status/cleanup pass". Post-merge: bin/install.sh re-run refreshed the ~/.claude surfaces; stale morning symlinks pruned.

## Original prompt

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

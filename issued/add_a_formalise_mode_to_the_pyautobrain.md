# Add a formalise mode to the PyAutoBrain intake agent

Type: feature
Target: PyAutoBrain
Repos:
- PyAutoBrain
- PyAutoMind
Difficulty: medium
Autonomy: supervised
Priority: normal
Status: formalised

Add a formalise mode to the PyAutoBrain intake agent. It walks the PyAutoMind prompts the census flags as headerless or with missing header fields and retroactively formalises them: classify and size each prompt body via the shared sizing faculty, then insert or complete the light metadata header in place, preserving the original text verbatim. This is the planned follow-up previously codenamed repair; formalise is the better word because raw prompts are intended word-vomit awaiting conception, not defects. The taxonomy folder stays authoritative for Type/Target; where the classifier disagrees with the folder, report a re-home suggestion but never move or delete files. Dry-run proposes, --apply writes. Touches intake agent code in PyAutoBrain and rewrites prompt files in PyAutoMind.

<!-- formalised by the Intake (Conception) Agent on 2026-07-08 from user-intake -->

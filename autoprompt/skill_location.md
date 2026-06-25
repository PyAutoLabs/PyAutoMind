Audit ownership and location of PyAuto development workflow skills.

Context

The PyAuto development workflow currently uses Claude skills / commands such as:

start_dev
start_library
start_workspace
ship_library
ship_workspace
pyauto-status
handoff
related workflow / release / development skills

Some of these may currently live under:

PyAutoLabs/.agents/skills

but that path may contain symlinks, installed copies, or generated local state.

Before redesigning these skills, determine their canonical source location and move them into the correct GitHub repository if needed.

Goal

Identify where the development workflow skills truly live, whether they are tracked in Git, and which repository should own them.

Tasks
Inspect local skill locations.

Check:

PyAutoLabs/.agents/skills
~/.claude/skills
~/.claude/commands
PyAutoMind/skills
PyAutoBrain/skills
PyAutoBuild/skills
PyAutoHeart/skills
admin_jammy/skills

Also inspect any install scripts that create symlinks or copy skills.

Determine canonical ownership.

For each development workflow skill, identify:

actual source path,
whether it is a symlink,
target of the symlink,
owning Git repository,
whether the source is tracked by Git,
whether installed copies are stale.
Decide the correct owning repo.

Use this ownership rule:

PyAutoMind owns intent/task registry skills.
PyAutoBrain owns reasoning / agent orchestration skills.
PyAutoBuild owns execution / release / build skills.
PyAutoHeart owns health / validation / readiness skills.
admin_jammy should not own canonical PyAuto organism workflow skills unless there is a clear transitional reason.

For workflow skills such as:

start_dev
start_library
start_workspace
ship_library
ship_workspace

decide whether they should live in PyAutoBrain, PyAutoBuild, or be split.

Likely direction:

planning / routing portions should move to PyAutoBrain,
execution portions should remain in PyAutoBuild,
task registry updates should interface with PyAutoMind,
health gates should interface with PyAutoHeart.
Do not redesign the skills yet.

This prompt is only for ownership and location cleanup.

Do not substantially rewrite behaviour.

If moving skills

If a skill is in the wrong canonical repo:

move the source files,
update install scripts,
update symlinks,
update documentation,
preserve command names,
avoid breaking existing workflows.
Report findings.

Create a concise ownership table:

Skill | Current source | Symlink? | Current owner | Recommended owner | Action taken
Validation

Run relevant install/status checks.

Verify that the commands still resolve after any move.

PR

Create one PR titled:

Audit and canonicalise PyAuto workflow skill ownership